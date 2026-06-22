import asyncio
import time
from typing import Optional, Dict, Tuple
from quira.providers.base import CacheBackend

class InMemoryCache(CacheBackend):
    def __init__(self, max_size: int = 1000):
        # Store dict of key -> (value, expire_at)
        self._cache: Dict[str, Tuple[str, float]] = {}
        self.max_size = max_size

    async def get(self, key: str) -> Optional[str]:
        if key not in self._cache:
            return None
            
        value, expire_at = self._cache[key]
        if expire_at > 0 and time.time() > expire_at:
            del self._cache[key]
            return None
            
        return value

    def _evict_if_needed(self):
        if len(self._cache) >= self.max_size:
            now = time.time()
            expired = [k for k, v in self._cache.items() if v[1] > 0 and now > v[1]]
            for k in expired:
                del self._cache[k]
                
            if len(self._cache) >= self.max_size:
                # Random eviction to keep size bounded
                keys_to_drop = list(self._cache.keys())[:200]
                for k in keys_to_drop:
                    del self._cache[k]

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        self._evict_if_needed()
        expire_at = time.time() + ttl_seconds if ttl_seconds else 0.0
        self._cache[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
