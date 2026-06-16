import asyncio
from typing import Any, Optional
from quira.providers.base import CacheBackend

class RedisCache(CacheBackend):
    def __init__(self, client: Any = None, url: str = "redis://localhost:6379"):
        if client:
            self.client = client
        else:
            try:
                import redis.asyncio as redis
                self.client = redis.from_url(url)
            except ImportError:
                raise ImportError("redis package not installed. Run `pip install quira[redis]`")

    async def get(self, key: str) -> Optional[str]:
        if asyncio.iscoroutinefunction(self.client.get):
            val = await self.client.get(key)
        else:
            loop = asyncio.get_event_loop()
            val = await loop.run_in_executor(None, self.client.get, key)
            
        if val is None:
            return None
        if isinstance(val, bytes):
            return val.decode("utf-8")
        return str(val)

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        if asyncio.iscoroutinefunction(self.client.set):
            await self.client.set(key, value, ex=ttl_seconds)
        else:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.client.set(key, value, ex=ttl_seconds))

    async def delete(self, key: str) -> None:
        if asyncio.iscoroutinefunction(self.client.delete):
            await self.client.delete(key)
        else:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.client.delete, key)
