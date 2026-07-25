import asyncio
import time
import hashlib
import logging
from typing import Any, List, Dict, Optional, Callable
import json

from quira.modules.debouncer import AsyncDebouncer

import numpy as np

logger = logging.getLogger("quira.speculative")
logger.setLevel(logging.INFO)
# For simplicity, ensure a stream handler is attached so tests/users see logs
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

from quira.providers.base import VectorStore, CacheBackend

class SpeculativeRetriever:
    """
    Module 1 - Speculative Retrieval:
    Detects typing, debounces based on speed, searches VectorStore, and caches in CacheBackend.
    """
    def __init__(self, user_id: str, vector_store: VectorStore, cache: CacheBackend, embed_func: Optional[Any] = None):
        self.user_id = user_id
        self.vector_store = vector_store
        self.cache = cache
        
        if embed_func:
            self.embed_func = embed_func
        else:
            try:
                from fastembed import TextEmbedding
                model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
                self.embed_func = lambda text: list(model.embed([text]))[0]
            except ImportError:
                raise ImportError("FastEmbed is not installed. Run `pip install quira[local-embed]` or provide a custom embed_func.")
        
        self._last_keystroke_time: float = 0.0
        self._last_query_len: int = 0
        self.debouncer = AsyncDebouncer()
        
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
        
        # Concurrency control for local embeddings and vector store searches
        self._search_lock = asyncio.Lock()

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
        
        logger.info(f"User {self.user_id}: keystroke received, scheduling debounce for {int(debounce_delay*1000)}ms")
        
        async def _run_search():
            await self._speculative_task(partial_query)
            
        await self.debouncer.debounce(self.user_id, _run_search, delay=debounce_delay)

    async def _speculative_task(self, partial_query: str) -> None:
        logger.info(f"User {self.user_id}: debounce fired, starting speculative search")
        
        # If a search/embedding is already running, abort this speculative update
        # to prevent CPU/GPU spikes with local embedding models.
        if self._search_lock.locked():
            logger.info(f"User {self.user_id}: Search already in progress, aborting to prevent CPU/GPU spikes")
            self._stats["searches_aborted"] += 1
            return
            
        async with self._search_lock:
            try:
                # Offload synchronous embedding to a thread to avoid blocking the event loop
                current_emb = await asyncio.to_thread(self.embed_func, partial_query)
            except asyncio.CancelledError:
                return
            except Exception as e:
                logger.error(f"Speculative embedding failed: {e}")
                return
            
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
            
            # Cache results
            query_hash = self._hash_query(partial_query)
            cache_key = f"user:{self.user_id}:speculative:{query_hash}"
            
            await self.cache.set(cache_key, json.dumps(results), ttl_seconds=600)

    async def _perform_search(self, embedding: np.ndarray) -> List[Dict[str, Any]]:
        """Search against VectorStore with timeout to prevent dangling connections."""
        try:
            coro = self.vector_store.search(
                collection_name=f"quira_{self.user_id}",
                query_vector=embedding.tolist() if hasattr(embedding, "tolist") else list(embedding),
                limit=10
            )
            # Add strict timeout
            hits = await asyncio.wait_for(coro, timeout=5.0)
            return hits
        except asyncio.TimeoutError:
            logger.warning("VectorStore search timed out")
            return []
        except asyncio.CancelledError:
            # Re-raise so the debouncer wrapper can handle it
            raise
        except Exception as e:
            logger.warning(f"Search failed, returning empty context: {e}")
            return []

    async def on_submit(self, full_query: str) -> List[Dict[str, Any]]:
        """Called when the user hits enter."""
        start_time = time.time()
        
        query_hash = self._hash_query(full_query)
        cache_key = f"user:{self.user_id}:speculative:{query_hash}"
        
        # Check cache
        try:
            cached = await self.cache.get(cache_key)
        except Exception as e:
            logger.warning(f"Cache get failed: {e}")
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
        
        try:
            current_emb = await asyncio.to_thread(self.embed_func, full_query)
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return []
            
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
