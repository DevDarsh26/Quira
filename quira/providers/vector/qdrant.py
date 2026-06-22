import asyncio
from typing import Any, List, Dict, Optional
from quira.providers.base import VectorStore

class QdrantStore(VectorStore):
    def __init__(self, client: Any = None, url: str = ":memory:", api_key: Optional[str] = None):
        """
        Adapter for Qdrant.
        Accepts a pre-initialized client OR initializes one if url is provided.
        """
        if client:
            self.client = client
        else:
            try:
                from qdrant_client import QdrantClient
                if url == ":memory:":
                    self.client = QdrantClient(location=":memory:", api_key=api_key)
                else:
                    self.client = QdrantClient(url=url, api_key=api_key)
            except ImportError:
                raise ImportError("Qdrant client not installed. Run `pip install quira[qdrant]`")

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        # Qdrant client might be async or sync depending on how it was initialized
        if asyncio.iscoroutinefunction(self.client.search):
            hits = await self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
        else:
            loop = asyncio.get_event_loop()
            hits = await loop.run_in_executor(
                None,
                lambda: self.client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=limit
                )
            )
        
        return [{"id": hit.id, "payload": hit.payload} for hit in hits]

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        try:
            from qdrant_client.models import PointStruct
        except ImportError:
            raise ImportError("Qdrant client not installed. Run `pip install quira[qdrant]`")
            
        qdrant_points = [
            PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p.get("payload", {})
            ) for p in points
        ]
        
        if asyncio.iscoroutinefunction(self.client.upsert):
            await self.client.upsert(
                collection_name=collection_name,
                points=qdrant_points
            )
        else:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.upsert(
                    collection_name=collection_name,
                    points=qdrant_points
                )
            )
