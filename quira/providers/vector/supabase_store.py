import asyncio
from typing import Any, List, Dict, Optional
from quira.providers.base import VectorStore

class SupabaseStore(VectorStore):
    def __init__(self, client: Any = None, url: Optional[str] = None, key: Optional[str] = None):
        """
        Adapter for Supabase (pgvector).
        Accepts a pre-initialized client OR initializes one if url and key are provided.
        """
        if client:
            self.client = client
        else:
            try:
                from supabase import create_client, Client
                if not url or not key:
                    raise ValueError("Supabase URL and API Key must be provided if client is not passed.")
                self.client: Client = create_client(url, key)
            except ImportError:
                raise ImportError("Supabase client not installed. Run `pip install supabase`")

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        # Usually Supabase handles pgvector through an RPC function.
        # We assume an RPC function named `match_documents` exists.
        loop = asyncio.get_event_loop()
        
        def _sync_search():
            response = self.client.rpc(
                "match_documents",
                {
                    "query_embedding": query_vector,
                    "match_threshold": 0.0, # adjust as needed
                    "match_count": limit,
                    "collection": collection_name # optional if you segment collections
                }
            ).execute()
            return response.data
            
        data = await loop.run_in_executor(None, _sync_search)
        
        # We need to map it back to the [{"id": ..., "payload": ...}] format
        return [
            {
                "id": hit.get("id"),
                "payload": hit.get("payload", hit.get("metadata", hit))
            } for hit in data
        ]

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        loop = asyncio.get_event_loop()
        
        def _sync_upsert():
            supabase_points = [
                {
                    "id": p["id"],
                    "embedding": p["vector"],
                    "payload": p.get("payload", {}),
                    "collection": collection_name
                } for p in points
            ]
            
            # Using the `documents` table by convention
            self.client.table("documents").upsert(supabase_points).execute()

        await loop.run_in_executor(None, _sync_upsert)
