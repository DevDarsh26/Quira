import time
import logging
import asyncio
from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger("quira.differential")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

class GCReport:
    def __init__(self, evicted_count: int, protected_anchors: int):
        self.evicted_count = evicted_count
        self.protected_anchors = protected_anchors

from quira.providers.base import VectorStore

class DifferentialRetriever:
    """
    Module 3 - Differential Retrieval:
    - Maintains conversation state & context pool
    - Performs Divergence Checks to decide FULL, PARTIAL, or DIFFERENTIAL reset
    - Runs Delta Retrieval to fetch only genuinely new chunks
    - Garbage collects irrelevant chunks every 3 turns
    """
    def __init__(self, user_id: str, vector_store: VectorStore, embed_func: Optional[Any] = None):
        self.user_id = user_id
        self.vector_store = vector_store
        
        if embed_func:
            self.embed_func = embed_func
        else:
            try:
                from fastembed import TextEmbedding
                model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
                self.embed_func = lambda text: list(model.embed([text]))[0]
            except ImportError:
                raise ImportError("FastEmbed is not installed. Run `pip install quira[local-embed]` or provide a custom embed_func.")
        
        # Conversation state
        self.turns: List[Dict[str, Any]] = []  # [{"query": str, "embedding": np.ndarray, "timestamp": float}]
        self.context_pool: List[Dict[str, Any]] = [] # list of chunks
        self.anchor_chunks: set = set() # set of chunk ids
        
        self.turn_count = 0
        self._stats = {
            "reuse_rate": 0.0,
            "total_evictions": 0,
            "chunks_fetched": 0,
            "chunks_skipped": 0
        }

    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        norm = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        if norm == 0:
            return 0.0
        return float(np.dot(emb1, emb2) / norm)

    def force_reset(self) -> None:
        self.context_pool.clear()
        self.turns.clear()
        self.turn_count = 0
        logger.info(f"User {self.user_id}: Forced reset of differential retriever")

    def mark_as_anchor(self, chunk_ids: List[str]) -> None:
        for cid in chunk_ids:
            self.anchor_chunks.add(cid)

    def get_context_pool(self) -> List[Dict[str, Any]]:
        return self.context_pool

    async def retrieve(self, query: str) -> List[Dict[str, Any]]:
        self.turn_count += 1
        current_emb = self.embed_func(query)
        
        mode = "FRESH"
        if len(self.turns) > 0:
            prev_turn = self.turns[-1]
            sim = self._cosine_similarity(current_emb, prev_turn["embedding"])
            
            if sim > 0.6:
                mode = "DIFFERENTIAL"
                logger.info(f"Turn {self.turn_count}: similarity={sim:.2f}, DIFFERENTIAL mode")
            elif sim >= 0.3:
                mode = "PARTIAL RESET"
                logger.info(f"Turn {self.turn_count}: similarity={sim:.2f}, PARTIAL RESET mode")
                # Keep top 5 most relevant existing chunks
                if self.context_pool:
                    scored_pool = [
                        (self._cosine_similarity(current_emb, np.array(c.get("embedding", []))), c)
                        for c in self.context_pool
                    ]
                    scored_pool.sort(key=lambda x: x[0], reverse=True)
                    self.context_pool = [c for _, c in scored_pool[:5]]
                    # Anchors are not forcefully protected in partial reset unless we explicitly do so.
                    # The prompt says: "Keep top 5 most relevant existing chunks", we will stick to that.
            else:
                mode = "FULL RESET"
                logger.info(f"Turn {self.turn_count}: similarity={sim:.2f}, FULL RESET, pool cleared")
                self.context_pool.clear()
        else:
            logger.info(f"Turn {self.turn_count}: fresh retrieval, empty pool")
            
        self.turns.append({
            "query": query,
            "embedding": current_emb,
            "timestamp": time.time()
        })
        
        # Search VectorStore for top 15 candidates
        try:
            hits = await self.vector_store.search(
                collection_name=f"quira_{self.user_id}",
                query_vector=current_emb.tolist() if hasattr(current_emb, "tolist") else list(current_emb),
                limit=15
            )
            candidates = [{"id": hit["id"], "text": hit["payload"].get("text", ""), "embedding": np.array(hit["payload"].get("embedding", current_emb)), "hit_count": 0} for hit in hits]
        except Exception as e:
            logger.warning(f"Search failed, returning empty context: {e}")
            candidates = []
            
        # Differential Retrieval Logic
        new_chunks = []
        skipped = 0
        
        for cand in candidates:
            # Check if it already exists in pool
            already_have_it = False
            for pool_chunk in self.context_pool:
                if cand["id"] == pool_chunk["id"]:
                    already_have_it = True
                    pool_chunk["hit_count"] = pool_chunk.get("hit_count", 0) + 1
                    break
                # Or check similarity > 0.88
                pool_emb = np.array(pool_chunk.get("embedding", []))
                if len(pool_emb) > 0 and self._cosine_similarity(cand["embedding"], pool_emb) > 0.88:
                    already_have_it = True
                    pool_chunk["hit_count"] = pool_chunk.get("hit_count", 0) + 1
                    break
                    
            if already_have_it:
                skipped += 1
            else:
                new_chunks.append(cand)
                
        self._stats["chunks_fetched"] += len(new_chunks)
        self._stats["chunks_skipped"] += skipped
        
        if len(candidates) > 0:
            logger.info(f"Turn {self.turn_count}: {len(candidates)} candidates, {skipped} already in pool, fetching {len(new_chunks)} new")
            
        self.context_pool.extend(new_chunks)
        
        # Context pool management limit (50 max)
        self._enforce_pool_limit(current_emb)
        
        # Garbage Collection
        if self.turn_count > 0 and self.turn_count % 3 == 0:
            await self.garbage_collect()
            
        return new_chunks

    def _enforce_pool_limit(self, current_emb: np.ndarray) -> None:
        if len(self.context_pool) > 50:
            # Evict lowest scoring first, factoring in hit count as protection
            def score_for_eviction(chunk):
                # We want to evict LOWEST score.
                # Relevancy to current query + small bonus for hit count
                sim = self._cosine_similarity(current_emb, np.array(chunk.get("embedding", [])))
                hit_bonus = chunk.get("hit_count", 0) * 0.05
                return sim + hit_bonus
                
            # Sort by score ascending (lowest first)
            self.context_pool.sort(key=score_for_eviction)
            
            # Remove until we hit 50, but never remove anchors
            new_pool = []
            evicted = 0
            to_remove = len(self.context_pool) - 50
            
            for chunk in self.context_pool:
                if chunk["id"] in self.anchor_chunks or to_remove == 0:
                    new_pool.append(chunk)
                else:
                    to_remove -= 1
                    evicted += 1
                    self._stats["total_evictions"] += 1
                    
            self.context_pool = new_pool

    async def garbage_collect(self) -> GCReport:
        if len(self.turns) < 3 or not self.context_pool:
            return GCReport(0, 0)
            
        last_3 = self.turns[-3:]
        avg_emb = np.mean([t["embedding"] for t in last_3], axis=0)
        
        new_pool = []
        evicted = 0
        protected = 0
        
        for chunk in self.context_pool:
            is_anchor = chunk["id"] in self.anchor_chunks
            
            sim = self._cosine_similarity(avg_emb, np.array(chunk.get("embedding", [])))
            if sim < 0.35 and not is_anchor:
                evicted += 1
                self._stats["total_evictions"] += 1
                logger.info(f"Turn {self.turn_count}: GC evicted chunk {chunk['id']} (score {sim:.2f} < 0.35)")
            else:
                new_pool.append(chunk)
                if is_anchor and sim < 0.35:
                    protected += 1
                    logger.info(f"Turn {self.turn_count}: GC kept anchor chunk {chunk['id']} despite low score")
                    
        self.context_pool = new_pool
        logger.info(f"Turn {self.turn_count}: GC ran, evicted {evicted} chunks, {protected} anchor protected")
        return GCReport(evicted, protected)

    def get_stats(self) -> Dict[str, Any]:
        total = self._stats["chunks_fetched"] + self._stats["chunks_skipped"]
        reuse_rate = self._stats["chunks_skipped"] / total if total > 0 else 0.0
        return {
            "reuse_rate": reuse_rate,
            "pool_size": len(self.context_pool),
            "total_evictions": self._stats["total_evictions"],
            "anchor_count": len(self.anchor_chunks)
        }
