import asyncio
import os
import time
import json
from typing import Optional
from quira.providers.base import CacheBackend

class DiskCache(CacheBackend):
    def __init__(self, directory: str = ".quira_cache"):
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)

    def _get_path(self, key: str) -> str:
        # Sanitize key for filesystem
        safe_key = "".join([c if c.isalnum() else "_" for c in key])
        return os.path.join(self.directory, f"{safe_key}.json")

    async def get(self, key: str) -> Optional[str]:
        loop = asyncio.get_event_loop()
        
        def _read():
            path = self._get_path(key)
            if not os.path.exists(path):
                return None
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data["expire_at"] > 0 and time.time() > data["expire_at"]:
                        os.remove(path)
                        return None
                    return data["value"]
            except Exception:
                return None
                
        return await loop.run_in_executor(None, _read)

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        loop = asyncio.get_event_loop()
        
        def _write():
            path = self._get_path(key)
            expire_at = time.time() + ttl_seconds if ttl_seconds else 0.0
            data = {"value": value, "expire_at": expire_at}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
                
        await loop.run_in_executor(None, _write)

    async def delete(self, key: str) -> None:
        loop = asyncio.get_event_loop()
        
        def _delete():
            path = self._get_path(key)
            if os.path.exists(path):
                os.remove(path)
                
        await loop.run_in_executor(None, _delete)
