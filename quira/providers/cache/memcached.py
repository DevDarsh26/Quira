import os
import aiomcache
from typing import Optional

from quira.providers.base import CacheBackend

class MemcachedProvider(CacheBackend):
    def __init__(self, host: str = "127.0.0.1", port: int = 11211):
        self.host = host
        self.port = port
        self.client = aiomcache.Client(host, port)
        
    async def get(self, key: str) -> Optional[str]:
        val = await self.client.get(key.encode('utf-8'))
        if val is not None:
            return val.decode('utf-8')
        return None

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        if ttl_seconds is None:
            ttl_seconds = 0 # 0 means forever in memcached
        await self.client.set(key.encode('utf-8'), value.encode('utf-8'), exptime=ttl_seconds)

    async def delete(self, key: str) -> None:
        await self.client.delete(key.encode('utf-8'))
