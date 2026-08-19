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
        use_query_points = hasattr(self.client, 'query_points')
        search_func = self.client.query_points if use_query_points else getattr(self.client, 'search', None)
        if search_func is None:
            raise AttributeError("QdrantClient has neither 'search' nor 'query_points' methods.")

        if asyncio.iscoroutinefunction(search_func):
            if use_query_points:
                hits_response = await search_func(
                    collection_name=collection_name,
                    query=query_vector,
                    limit=limit,
                    with_vectors=True
                )
                hits = hits_response.points if hasattr(hits_response, 'points') else hits_response
            else:
                hits = await search_func(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=limit,
                    with_vectors=True
                )
        else:
            loop = asyncio.get_event_loop()
            if use_query_points:
                hits_response = await loop.run_in_executor(
                    None,
                    lambda: search_func(
                        collection_name=collection_name,
                        query=query_vector,
                        limit=limit,
                        with_vectors=True
                    )
                )
                hits = hits_response.points if hasattr(hits_response, 'points') else hits_response
            else:
                hits = await loop.run_in_executor(
                    None,
                    lambda: search_func(
                        collection_name=collection_name,
                        query_vector=query_vector,
                        limit=limit,
                        with_vectors=True
                    )
                )
        
        return [{"id": hit.id, "payload": hit.payload, "vector": getattr(hit, "vector", None)} for hit in hits]

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
        
        if not points:
            return

        def _safe_upsert():
            from qdrant_client.models import VectorParams, Distance
            if not self.client.collection_exists(collection_name):
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=len(points[0]["vector"]), distance=Distance.COSINE)
                )
            self.client.upsert(
                collection_name=collection_name,
                points=qdrant_points
            )

        if asyncio.iscoroutinefunction(self.client.upsert):
            from qdrant_client.models import VectorParams, Distance
            exists = self.client.collection_exists(collection_name)
            if asyncio.iscoroutine(exists):
                exists = await exists
            
            if not exists:
                create_task = self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=len(points[0]["vector"]), distance=Distance.COSINE)
                )
                if asyncio.iscoroutine(create_task):
                    await create_task
            await self.client.upsert(
                collection_name=collection_name,
                points=qdrant_points
            )
        else:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _safe_upsert)
