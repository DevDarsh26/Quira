import asyncio
import time
from typing import Optional, Dict, Tuple
from quira.providers.base import CacheBackend

class InMemoryCache(CacheBackend):
    def __init__(self):
        # Store dict of key -> (value, expire_at)
        self._cache: Dict[str, Tuple[str, float]] = {}

    async def get(self, key: str) -> Optional[str]:
        if key not in self._cache:
            return None
            
        value, expire_at = self._cache[key]
        if expire_at > 0 and time.time() > expire_at:
            del self._cache[key]
            return None
            
        return value

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        expire_at = time.time() + ttl_seconds if ttl_seconds else 0.0
        self._cache[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
