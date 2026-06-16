import asyncio
from typing import Any, List, Dict, Optional
from quira.providers.base import VectorStore

class PineconeStore(VectorStore):
    def __init__(self, client: Any = None, api_key: Optional[str] = None):
        """
        Adapter for Pinecone.
        Accepts a pre-initialized Pinecone client OR initializes one if api_key is provided.
        """
        if client:
            self.pc = client
        else:
            try:
                from pinecone import Pinecone
                if not api_key:
                    raise ValueError("PineconeStore requires an api_key if no client is provided.")
                self.pc = Pinecone(api_key=api_key)
            except ImportError:
                raise ImportError("Pinecone client not installed. Run `pip install quira[pinecone]`")

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        index = self.pc.Index(collection_name)
        # Pinecone's standard python client is synchronous
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: index.query(
                vector=query_vector,
                top_k=limit,
                include_metadata=True
            )
        )
        
        return [{"id": match.id, "payload": match.metadata or {}} for match in response.matches]

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        index = self.pc.Index(collection_name)
        
        # Pinecone expects tuples: (id, vector, metadata)
        vectors = [
            (p["id"], p["vector"], p.get("payload", {}))
            for p in points
        ]
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: index.upsert(vectors=vectors)
        )
