import time
import math
import logging
import re
from typing import List, Dict, Any, Optional, Callable
import numpy as np
import tiktoken

from quira.core.telemetry import trace_event

logger = logging.getLogger("quira.tetris")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

class ChunkScore:
    def __init__(self, relevance: float, recency: float, uniqueness: float, density: float):
        self.relevance = relevance
        self.recency = recency
        self.uniqueness = uniqueness
        self.density = density
        self.final_score = (
            relevance * 0.40 +
            recency * 0.20 +
            uniqueness * 0.25 +
            density * 0.15
        )

class PackedContext:
    def __init__(self, chunks: List[Dict[str, Any]], stats: Dict[str, Any]):
        self.chunks = chunks
        self.stats = stats

from quira.providers.base import LLMProvider

class ContextTetris:
    """
    Module 2 - Context Tetris:
    Picks the BEST chunks using 4-dimensional scoring.
    Compresses using a 3-tier strategy: TextRank extractive, entity-anchored,
    and optional LLM abstractive.
    U-shape ordering for optimal LLM attention.
    """
    def __init__(self, llm_provider: LLMProvider, spacy_model: Any = None,
                 density_func: Optional[Callable[[str], float]] = None,
                 compression_llm: Optional[LLMProvider] = None):
        self.llm = llm_provider
        self.nlp = spacy_model
        self.density_func = density_func
        self.compression_llm = compression_llm  # Optional cheap LLM for Tier 3 compression
        
        self._stats = {
            "initial_chunks": 0,
            "selected_chunks": 0,
            "rejected_chunks": 0,
            "compressed_chunks": 0,
            "tokens_saved": 0,
            "total_original_tokens": 0,
            "total_compressed_tokens": 0,
            "utilization_pct": 0.0
        }

    def _count_tokens(self, text: str) -> int:
        return self.llm.count_tokens(text)

    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        norm = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        if norm == 0:
            return 0.0
        return float(np.dot(emb1, emb2) / norm)

    # ----------------------------------------------------------------
    # Entity Extraction
    # ----------------------------------------------------------------
    def _extract_entities(self, text: str) -> set:
        """Extract named entities and important terms from text."""
        if self.nlp:
            doc = self.nlp(text)
            entities = set()
            for ent in doc.ents:
                if ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "DATE", "TIME",
                                  "PERCENT", "MONEY", "QUANTITY", "CARDINAL",
                                  "PRODUCT", "EVENT", "FAC", "NORP", "LAW"}:
                    entities.add(ent.text)
            return entities
        else:
            # Regex fallback: capitalized words, numbers, percentages, money
            found = re.findall(
                r'\b[A-Z][a-zA-Z0-9-]+(?:\s+[A-Z][a-zA-Z0-9-]+)*\b'  # Capitalized phrases
                r'|\b\d+(?:\.\d+)?%?\b'                                # Numbers/percentages
                r'|\$[\d,]+(?:\.\d+)?',                                 # Dollar amounts
                text
            )
            return set(found)

    # ----------------------------------------------------------------
    # Sentence Splitting
    # ----------------------------------------------------------------
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling common abbreviations."""
        # Split on sentence-ending punctuation followed by space + uppercase or end
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])|(?<=[.!?])\s*$', text)
        # Filter empty
        return [s.strip() for s in sentences if s.strip()]

    # ----------------------------------------------------------------
    # Tier 1: TextRank Extractive Summarization
    # ----------------------------------------------------------------
    def _textrank_extract(self, text: str, preserved_entities: set,
                          target_ratio: float = 0.55) -> str:
        """
        Sentence-level TextRank using TF-IDF cosine similarity graph.
        Selects the most central/informative sentences up to the target ratio.
        Gives bonus scores to sentences containing preserved entities.
        """
        sentences = self._split_sentences(text)
        n = len(sentences)
        
        if n <= 2:
            return text  # Too short to compress meaningfully
        
        target_tokens = int(self._count_tokens(text) * target_ratio)
        
        # Build word frequency vectors (simple TF)
        word_sets = []
        for s in sentences:
            words = re.findall(r'\b\w+\b', s.lower())
            word_sets.append(words)
        
        # Build vocabulary
        vocab = {}
        for words in word_sets:
            for w in words:
                if w not in vocab:
                    vocab[w] = len(vocab)
        
        if not vocab:
            return text
        
        # Build TF vectors
        vectors = np.zeros((n, len(vocab)))
        for i, words in enumerate(word_sets):
            for w in words:
                vectors[i][vocab[w]] += 1
            # Normalize
            norm = np.linalg.norm(vectors[i])
            if norm > 0:
                vectors[i] /= norm
        
        # Build similarity matrix
        sim_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                sim = float(np.dot(vectors[i], vectors[j]))
                sim_matrix[i][j] = sim
                sim_matrix[j][i] = sim
        
        # PageRank-style scoring (power iteration)
        damping = 0.85
        scores = np.ones(n) / n
        for _ in range(20):
            new_scores = np.ones(n) * (1 - damping) / n
            for i in range(n):
                col_sum = sim_matrix[:, i].sum()
                if col_sum > 0:
                    new_scores[i] += damping * (sim_matrix[:, i] @ scores) / col_sum
            scores = new_scores
        
        # Entity bonus: sentences containing preserved entities get a score boost
        preserved_lower = {e.lower() for e in preserved_entities}
        for i, s in enumerate(sentences):
            s_words = set(re.findall(r'\b\w+\b', s.lower()))
            overlap = s_words & preserved_lower
            if overlap:
                scores[i] *= (1.0 + 0.3 * len(overlap))
            # Bonus for sentences with numbers (often factual)
            if re.search(r'\d', s):
                scores[i] *= 1.15
        
        # Select top sentences by score, maintaining original order
        ranked_indices = np.argsort(scores)[::-1]
        selected_indices = set()
        current_tokens = 0
        
        for idx in ranked_indices:
            s_tokens = self._count_tokens(sentences[idx])
            if current_tokens + s_tokens <= target_tokens:
                selected_indices.add(idx)
                current_tokens += s_tokens
            if current_tokens >= target_tokens:
                break
        
        # Always include first sentence for context anchoring
        if 0 not in selected_indices:
            selected_indices.add(0)
        
        # Reconstruct in original order
        result_sentences = [sentences[i] for i in sorted(selected_indices)]
        return " ".join(result_sentences)

    # ----------------------------------------------------------------
    # Tier 2: Entity-Anchored Extraction
    # ----------------------------------------------------------------
    def _entity_anchored_extract(self, text: str, preserved_entities: set,
                                  target_ratio: float = 0.35) -> str:
        """
        Aggressive extraction: keep only sentences that contain preserved entities,
        numbers, or are the first/last sentence (for context anchoring).
        """
        sentences = self._split_sentences(text)
        n = len(sentences)
        
        if n <= 2:
            return text
        
        target_tokens = int(self._count_tokens(text) * target_ratio)
        preserved_lower = {e.lower() for e in preserved_entities}
        
        # Score each sentence by entity overlap + number presence
        scored = []
        for i, s in enumerate(sentences):
            s_words = set(re.findall(r'\b\w+\b', s.lower()))
            entity_overlap = len(s_words & preserved_lower)
            has_numbers = 1 if re.search(r'\d', s) else 0
            # Position bonus: first and last sentences
            position_bonus = 0.5 if (i == 0 or i == n - 1) else 0
            score = entity_overlap * 2 + has_numbers + position_bonus
            scored.append((i, score, s))
        
        # Sort by score descending, then select greedily
        scored.sort(key=lambda x: x[1], reverse=True)
        
        selected_indices = set()
        current_tokens = 0
        
        for idx, score, s in scored:
            if score <= 0 and len(selected_indices) >= 2:
                continue  # Skip sentences with no entities unless we have very few
            s_tokens = self._count_tokens(s)
            if current_tokens + s_tokens <= target_tokens:
                selected_indices.add(idx)
                current_tokens += s_tokens
        
        # Always include first sentence
        if 0 not in selected_indices:
            selected_indices.add(0)
        
        if not selected_indices:
            # Fallback: at least return first sentence
            return sentences[0]
        
        # Reconstruct in original order
        result_sentences = [sentences[i] for i in sorted(selected_indices)]
        return " ".join(result_sentences)

    # ----------------------------------------------------------------
    # Tier 3: LLM Abstractive Compression (optional)
    # ----------------------------------------------------------------
    async def _llm_compress(self, text: str, preserved_entities: set) -> str:
        """Use a cheap LLM to semantically compress text while preserving facts."""
        preserved_str = ", ".join(preserved_entities) if preserved_entities else "all facts"
        prompt = (
            f"Compress the following text to ~40% of its original length. "
            f"You MUST preserve all named entities, numbers, dates, and these "
            f"specific terms: {preserved_str}\n\n"
            f"Rules:\n"
            f"- Keep all factual claims\n"
            f"- Remove filler, redundancy, and hedging language\n"
            f"- Output ONLY the compressed text, nothing else\n\n"
            f"Text: {text}"
        )
        result = await self.compression_llm.complete(
            prompt=prompt,
            system_prompt="You are a precise text compressor. Output only the compressed text."
        )
        return result.strip()

    # ----------------------------------------------------------------
    # Chunk Scoring (unchanged logic, cleaner code)
    # ----------------------------------------------------------------
    def score_chunk(self, chunk: Dict[str, Any], query_embedding: np.ndarray, max_sim_cache: float) -> ChunkScore:
        # Relevance
        if "score" in chunk:
            relevance = float(chunk["score"])
        else:
            chunk_emb = np.array(chunk.get("embedding", []))
            if len(chunk_emb) == 0:
                relevance = 0.0
            else:
                relevance = self._cosine_similarity(query_embedding, chunk_emb)
            
        # Recency (half life = 180 days)
        created_at = chunk.get("created_at", time.time())
        days_ago = (time.time() - created_at) / (24 * 3600)
        recency = math.exp(-math.log(2) * max(0, days_ago) / 180)
        
        # Uniqueness
        uniqueness = max(0.0, 1.0 - max_sim_cache)
            
        # Density
        text = chunk.get("text", "")
        tokens = self._count_tokens(text)
        if tokens == 0:
            density = 0.0
        elif self.density_func:
            density = self.density_func(text)
        elif not self.nlp:
            # Fallback heuristic: count capitalized words, numbers, and basic entities
            ent_count = len(re.findall(r'\b[A-Z][a-zA-Z0-9-]+\b|\b\d+(?:\.\d+)?\b', text))
            density = min(1.0, ent_count / max(1, (tokens / 100)))
        else:
            doc = self.nlp(text)
            # count entities and numbers
            ent_count = len([ent for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "CARDINAL"}])
            density = min(1.0, ent_count / max(1, (tokens / 100)))

        return ChunkScore(relevance, recency, uniqueness, density)

    # ----------------------------------------------------------------
    # Compression Dispatch
    # ----------------------------------------------------------------
    @trace_event(name="quira.tetris.compress_chunk")
    async def compress_chunk(self, chunk: Dict[str, Any], score: float) -> Dict[str, Any]:
        """
        3-tier compression:
        - Tier 1 (score >= 0.7): Light TextRank extraction (~55% of original)
        - Tier 2 (score < 0.7): Heavy entity-anchored extraction (~35% of original)
        - Tier 3 (optional): LLM abstractive compression for low-score chunks
        """
        text = chunk.get("text", "")
        orig_tokens = self._count_tokens(text)
        
        # Skip compression for very short chunks
        if orig_tokens < 50:
            return chunk
        
        # Extract entities to preserve
        preserved = self._extract_entities(text)
        
        if score >= 0.7:
            # Tier 1: Light — keep most informative sentences
            compressed_text = self._textrank_extract(text, preserved, target_ratio=0.55)
        else:
            # Tier 2: Heavy — entity-anchored sentences only
            compressed_text = self._entity_anchored_extract(text, preserved, target_ratio=0.35)
        
        llm_cost_tokens = 0
        # Tier 3: Optional LLM abstractive (only if enabled and chunk is low-scoring)
        if self.compression_llm and score < 0.5 and orig_tokens >= 100:
            try:
                llm_result = await self._llm_compress(text, preserved)
                llm_tokens = self._count_tokens(llm_result)
                ext_tokens = self._count_tokens(compressed_text)
                
                # Approximate the cost of the LLM call: input tokens (prompt + text) + output tokens
                llm_cost_tokens = orig_tokens + 50 + llm_tokens
                
                # Only use LLM result if it's actually shorter
                if llm_tokens < ext_tokens:
                    compressed_text = llm_result
            except Exception as e:
                logger.warning(f"Tier 3 LLM compression failed (using extractive fallback): {e}")
        
        new_tokens = self._count_tokens(compressed_text)
        if new_tokens < orig_tokens:
            net_savings = (orig_tokens - new_tokens) - llm_cost_tokens
            self._stats["tokens_saved"] += net_savings
            self._stats["compressed_chunks"] += 1
            
        new_chunk = chunk.copy()
        new_chunk["text"] = compressed_text
        return new_chunk

    # ----------------------------------------------------------------
    # Main Packing Algorithm
    # ----------------------------------------------------------------
    @trace_event(name="quira.tetris.pack")
    async def pack(self, chunks: List[Dict[str, Any]], query_embedding: np.ndarray, token_budget: int = 120000, skip_compression: bool = False) -> PackedContext:
        import asyncio
        logger.info(f"Scoring {len(chunks)} chunks for query...")
        self._stats = {
            "initial_chunks": len(chunks),
            "selected_chunks": 0,
            "rejected_chunks": 0,
            "compressed_chunks": 0,
            "tokens_saved": 0,
            "total_original_tokens": 0,
            "total_compressed_tokens": 0,
            "utilization_pct": 0.0
        }
        
        budget = token_budget - 2500 # Reserve 2000 for answer + 500 for system prompt
        current_tokens = 0
        
        selected_chunks = []
        selected_embeddings = []
        
        pool = chunks.copy()
        max_sims = [0.0] * len(pool)
        
        # Track original tokens for metrics
        total_original_tokens = 0
        
        while pool and current_tokens < budget:
            # Score all chunks in pool (MMR-style greedy selection)
            best_idx = -1
            best_score = -1.0
            
            for i, chunk in enumerate(pool):
                score = self.score_chunk(chunk, query_embedding, max_sims[i])
                if score.final_score > best_score:
                    best_score = score.final_score
                    best_idx = i
            
            if best_idx < 0:
                break
                    
            best_chunk = pool.pop(best_idx)
            best_chunk["tetris_score"] = best_score
            best_sim = max_sims.pop(best_idx)
            
            chunk_tokens = self._count_tokens(best_chunk.get("text", ""))
            total_original_tokens += chunk_tokens
            
            if current_tokens + chunk_tokens <= budget:
                selected_chunks.append(best_chunk)
                new_emb = np.array(best_chunk.get("embedding", []))
                selected_embeddings.append(new_emb)
                current_tokens += chunk_tokens
                
                # Update uniqueness caches for remaining pool chunks
                if len(new_emb) > 0:
                    for i, pool_chunk in enumerate(pool):
                        pool_emb = np.array(pool_chunk.get("embedding", []))
                        if len(pool_emb) > 0:
                            sim = self._cosine_similarity(pool_emb, new_emb)
                            if sim > max_sims[i]:
                                max_sims[i] = sim
            else:
                self._stats["rejected_chunks"] += 1

        # Concurrent compression execution
        compression_tasks = []
        for chunk in selected_chunks:
            score = chunk["tetris_score"]
            if skip_compression:
                async def identity(c=chunk):
                    return c
                compression_tasks.append(identity())
            else:
                compression_tasks.append(self.compress_chunk(chunk, score))
                
        final_chunks = list(await asyncio.gather(*compression_tasks))
        
        actual_tokens = sum(self._count_tokens(c.get("text", "")) for c in final_chunks)
        
        self._stats["selected_chunks"] = len(final_chunks)
        self._stats["rejected_chunks"] += len(pool)
        self._stats["total_original_tokens"] = total_original_tokens
        self._stats["total_compressed_tokens"] = actual_tokens
        self._stats["utilization_pct"] = (actual_tokens / budget) * 100 if budget > 0 else 0
        
        logger.info(f"Selected {self._stats['selected_chunks']} chunks (rejected {self._stats['rejected_chunks']} as redundant or low score)")
        logger.info(f"Compressed {self._stats['compressed_chunks']} chunks (saved {self._stats['tokens_saved']} tokens)")
        logger.info(f"Token reduction: {total_original_tokens} -> {actual_tokens} tokens ({self._stats['tokens_saved']} saved)")
        logger.info(f"Context utilization: {int(self._stats['utilization_pct'])}% of budget used")
        
        ordered = self._u_shape_order(final_chunks)
        
        if ordered:
            preview = ordered[0].get("text", "")[:50].replace("\n", " ")
            logger.info(f"U-shape ordered. Top chunk: [{preview}...]")
            
        return PackedContext(ordered, self.get_stats())
        
    def _u_shape_order(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Chunks are already ordered by when they were picked (descending by dynamic score)
        n = len(chunks)
        if n <= 2:
            return chunks
            
        result = [None] * n
        result[0] = chunks[0]
        result[-1] = chunks[1]
        
        if n >= 3:
            result[1] = chunks[2]
        if n >= 4:
            result[-2] = chunks[3]
            
        if n > 4:
            for i, chunk in enumerate(chunks[4:]):
                result[2 + i] = chunk
                
        return result

    def get_stats(self) -> Dict[str, Any]:
        return self._stats.copy()
