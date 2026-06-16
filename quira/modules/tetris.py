import time
import math
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import tiktoken

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
    Compresses based on score using an LLM.
    U-shape ordering for optimal LLM attention.
    """
    def __init__(self, llm_provider: LLMProvider, spacy_model: Any = None):
        self.llm = llm_provider
        self.nlp = spacy_model
        
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.tokenizer = None
            
        self._stats = {
            "initial_chunks": 0,
            "selected_chunks": 0,
            "rejected_chunks": 0,
            "compressed_chunks": 0,
            "tokens_saved": 0,
            "utilization_pct": 0.0
        }

    def _count_tokens(self, text: str) -> int:
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        return len(text.split()) * 1.3 # Rough approximation if tiktoken fails

    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        norm = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        if norm == 0:
            return 0.0
        return float(np.dot(emb1, emb2) / norm)

    def score_chunk(self, chunk: Dict[str, Any], query_embedding: np.ndarray, selected_embeddings: List[np.ndarray]) -> ChunkScore:
        # Relevance
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
        uniqueness = 1.0
        if selected_embeddings and len(chunk_emb) > 0:
            max_sim = max(self._cosine_similarity(chunk_emb, se) for se in selected_embeddings)
            uniqueness = max(0.0, 1.0 - max_sim)
            
        # Density
        text = chunk.get("text", "")
        tokens = self._count_tokens(text)
        if tokens == 0 or not self.nlp:
            density = 0.0
        else:
            doc = self.nlp(text)
            # count entities and numbers
            ent_count = len([ent for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "CARDINAL"}])
            density = min(1.0, ent_count / max(1, (tokens / 100)))

        return ChunkScore(relevance, recency, uniqueness, density)

    async def compress_chunk(self, chunk: Dict[str, Any], level: str) -> Dict[str, Any]:
        text = chunk.get("text", "")
        
        preserved_str = ""
        if self.nlp:
            doc = self.nlp(text)
            preserved = []
            for ent in doc.ents:
                if ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "CARDINAL"}:
                    preserved.append(ent.text)
            preserved_str = ", ".join(set(preserved))
        
        if level == "light":
            prompt = f"Remove filler sentences but keep all facts, numbers, and entities. MUST PRESERVE: {preserved_str}\n\nText: {text}"
        else:
            prompt = f"Reduce to 2-3 sentence summary. MUST PRESERVE all named entities, numbers, dates: {preserved_str}\n\nText: {text}"

        try:
            compressed_text = await self.llm.complete(prompt=prompt)
        except Exception as e:
            logger.warning(f"Compression failed, using original text: {e}")
            compressed_text = text

        orig_tokens = self._count_tokens(text)
        new_tokens = self._count_tokens(compressed_text)
        if new_tokens < orig_tokens:
            self._stats["tokens_saved"] += (orig_tokens - new_tokens)
            self._stats["compressed_chunks"] += 1
            
        new_chunk = chunk.copy()
        new_chunk["text"] = compressed_text
        return new_chunk

    async def pack(self, chunks: List[Dict[str, Any]], query_embedding: np.ndarray, token_budget: int = 120000) -> PackedContext:
        logger.info(f"Scoring {len(chunks)} chunks for query...")
        self._stats["initial_chunks"] = len(chunks)
        
        budget = token_budget - 2500 # Reserve 2000 for answer + 500 for system prompt
        current_tokens = 0
        
        selected_chunks = []
        selected_embeddings = []
        
        pool = chunks.copy()
        
        while pool and current_tokens < budget:
            # Score all chunks in pool
            best_idx = -1
            best_score = -1.0
            best_chunk_score = None
            
            for i, chunk in enumerate(pool):
                score = self.score_chunk(chunk, query_embedding, selected_embeddings)
                if score.final_score > best_score:
                    best_score = score.final_score
                    best_idx = i
                    best_chunk_score = score
                    
            best_chunk = pool.pop(best_idx)
            best_chunk["tetris_score"] = best_score
            
            # Determine compression level
            if best_score > 0.85:
                processed_chunk = best_chunk
            else:
                level = "light" if best_score >= 0.65 else "heavy"
                processed_chunk = await self.compress_chunk(best_chunk, level)
                
            chunk_tokens = self._count_tokens(processed_chunk.get("text", ""))
            
            if current_tokens + chunk_tokens <= budget:
                selected_chunks.append(processed_chunk)
                selected_embeddings.append(np.array(processed_chunk.get("embedding", [])))
                current_tokens += chunk_tokens
            else:
                self._stats["rejected_chunks"] += 1

        self._stats["selected_chunks"] = len(selected_chunks)
        self._stats["rejected_chunks"] += len(pool)
        self._stats["utilization_pct"] = (current_tokens / budget) * 100 if budget > 0 else 0
        
        logger.info(f"Selected {self._stats['selected_chunks']} chunks (rejected {self._stats['rejected_chunks']} as redundant or low score)")
        logger.info(f"Compressed {self._stats['compressed_chunks']} chunks (saved {self._stats['tokens_saved']} tokens)")
        logger.info(f"Context utilization: {int(self._stats['utilization_pct'])}% of budget used")
        
        ordered = self._u_shape_order(selected_chunks)
        
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
