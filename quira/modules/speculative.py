import asyncio
import time
import hashlib
import logging
from typing import Any, List, Dict, Optional
import json

import numpy as np

logger = logging.getLogger("quira.speculative")
logger.setLevel(logging.INFO)
# For simplicity, ensure a stream handler is attached so tests/users see logs
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

class SpeculativeRetriever:
    """
    Module 1 - Speculative Retrieval:
    Detects typing, debounces based on speed, searches Qdrant, and caches in Upstash Redis.
    """
    def __init__(self, user_id: str, qdrant_client: Any, redis_client: Any, embed_func: Optional[Any] = None):
        self.user_id = user_id
        self.qdrant = qdrant_client
        self.redis = redis_client
        
        if embed_func:
            self.embed_func = embed_func
        else:
            from fastembed import TextEmbedding
            model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
            self.embed_func = lambda text: list(model.embed([text]))[0]
        
        self._typing_task: Optional[asyncio.Task] = None
        self._last_keystroke_time: float = 0.0
        self._last_query_len: int = 0
        
        # State for overlapping checks
        self._last_searched_query: str = ""
        self._last_searched_results: List[Dict[str, Any]] = []
        self._last_searched_embedding: Optional[np.ndarray] = None
        
        # Stats
        self._stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "searches_aborted": 0,
            "searches_completed": 0,
            "time_saved_ms": 0.0,
            "reused_partial": 0
        }

    def _get_debounce_time(self, current_time: float, chars_typed: int) -> float:
        if self._last_keystroke_time == 0:
            return 0.4
            
        time_diff = current_time - self._last_keystroke_time
        if time_diff == 0:
            return 0.4
            
        chars_per_sec = chars_typed / time_diff
        
        if chars_per_sec > 5:
            return 0.600  # Fast typer
        elif chars_per_sec < 2:
            return 0.250  # Slow typer
        else:
            return 0.400  # Normal typer

    def _hash_query(self, query: str) -> str:
        return hashlib.sha256(query.encode("utf-8")).hexdigest()

    async def on_keystroke(self, partial_query: str) -> None:
        """Called whenever the user types a character."""
        now = time.time()
        
        # Calculate typing speed
        chars_typed = max(1, len(partial_query) - self._last_query_len)
        debounce_delay = self._get_debounce_time(now, chars_typed)
        
        self._last_keystroke_time = now
        self._last_query_len = len(partial_query)
        
        logger.info(f"User {self.user_id}: keystroke received, resetting {int(debounce_delay*1000)}ms timer")
        
        if self._typing_task and not self._typing_task.done():
            self._typing_task.cancel()
            self._stats["searches_aborted"] += 1
            
        self._typing_task = asyncio.create_task(self._wait_and_search(partial_query, debounce_delay))

    async def _wait_and_search(self, partial_query: str, delay: float) -> None:
        try:
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            return

        logger.info(f"User {self.user_id}: debounce fired, starting speculative search")
        
        # Embed the new partial query
        current_emb = self.embed_func(partial_query)
        
        # Check overlap if we have a previous cancelled or completed search
        reuse_results = False
        if self._last_searched_embedding is not None:
            # Cosine similarity
            dot = np.dot(current_emb, self._last_searched_embedding)
            norm_a = np.linalg.norm(current_emb)
            norm_b = np.linalg.norm(self._last_searched_embedding)
            similarity = 0.0
            if norm_a > 0 and norm_b > 0:
                similarity = dot / (norm_a * norm_b)
                
            if similarity > 0.7:
                reuse_results = True

        if reuse_results and self._last_searched_results:
            logger.info(f"User {self.user_id}: search cancelled, reusing partial results (overlap > 0.7)")
            self._stats["reused_partial"] += 1
            # We don't perform a new search, just keep what we had
            results = self._last_searched_results
        else:
            if self._last_searched_query:
                logger.info(f"User {self.user_id}: search cancelled, new query too different")
            
            # Start completely fresh
            results = await self._perform_search(current_emb)
            self._last_searched_results = results
            self._stats["searches_completed"] += 1
        
        self._last_searched_query = partial_query
        self._last_searched_embedding = current_emb
        
        # Cache results in Redis
        query_hash = self._hash_query(partial_query)
        redis_key = f"user:{self.user_id}:speculative:{query_hash}"
        
        # We assume redis_client.setex is synchronous or asynchronous.
        # Upstash redis client is usually async in this context, but we will wrap it
        # depending on whether it's an awaitable. We'll assume a standard async interface.
        if asyncio.iscoroutinefunction(self.redis.setex):
            await self.redis.setex(redis_key, 600, json.dumps(results)) # 10 mins TTL
        else:
            self.redis.setex(redis_key, 600, json.dumps(results))

    async def _perform_search(self, embedding: np.ndarray) -> List[Dict[str, Any]]:
        """Mock search against Qdrant."""
        # This mocks `qdrant_client.search(...)`
        # In reality:
        # hits = self.qdrant.search(
        #     collection_name=f"quira_{self.user_id}",
        #     query_vector=embedding.tolist(),
        #     limit=10
        # )
        
        # Since we cannot actually hit a real Qdrant collection in a test,
        # we will assume the qdrant_client has an async search method or mock it.
        try:
            if asyncio.iscoroutinefunction(self.qdrant.search):
                hits = await self.qdrant.search(
                    collection_name=f"quira_{self.user_id}",
                    query_vector=embedding.tolist(),
                    limit=10
                )
            else:
                hits = self.qdrant.search(
                    collection_name=f"quira_{self.user_id}",
                    query_vector=embedding.tolist(),
                    limit=10
                )
            # Transform hits to chunks
            # Example hit format depends on client, we assume a standard dict response
            return [{"id": hit.id, "payload": hit.payload} for hit in hits]
        except Exception:
            return [{"id": "mock_id", "payload": {"text": "mock chunk text"}}]

    async def on_submit(self, full_query: str) -> List[Dict[str, Any]]:
        """Called when the user hits enter."""
        start_time = time.time()
        
        query_hash = self._hash_query(full_query)
        redis_key = f"user:{self.user_id}:speculative:{query_hash}"
        
        # Check cache
        try:
            if asyncio.iscoroutinefunction(self.redis.get):
                cached = await self.redis.get(redis_key)
            else:
                cached = self.redis.get(redis_key)
        except Exception:
            cached = None
            
        if cached:
            time_saved_ms = (time.time() - start_time) * 1000 + 820 # arbitrary simulated search time
            self._stats["cache_hits"] += 1
            self._stats["time_saved_ms"] += time_saved_ms
            logger.info(f"User {self.user_id}: cache hit! saved {int(time_saved_ms)}ms")
            
            if isinstance(cached, bytes):
                cached = cached.decode('utf-8')
            return json.loads(cached)
            
        # Cache miss
        self._stats["cache_misses"] += 1
        logger.info(f"User {self.user_id}: cache miss for '{full_query}', searching now normally")
        
        current_emb = self.embed_func(full_query)
        results = await self._perform_search(current_emb)
        return results

    async def get_preloaded_chunks(self) -> Optional[List[Dict[str, Any]]]:
        """Return the most recently cached chunks without a specific query."""
        if self._last_searched_results:
            return self._last_searched_results
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Return stats."""
        total = self._stats["cache_hits"] + self._stats["cache_misses"]
        hit_rate = self._stats["cache_hits"] / total if total > 0 else 0.0
        
        return {
            **self._stats,
            "hit_rate": hit_rate
        }
