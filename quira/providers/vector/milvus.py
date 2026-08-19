import os
import asyncio
from typing import Any, List, Dict
from pymilvus import MilvusClient

from quira.providers.base import VectorStore

class MilvusStore(VectorStore):
    def __init__(self, uri: str = "http://localhost:19530", token: str = ""):
        # uri can be a local path like "./milvus_demo.db" for Milvus Lite
        self.client = MilvusClient(uri=uri, token=token)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        # Milvus search is synchronous, run in thread to avoid blocking event loop
        def _search():
            res = self.client.search(
                collection_name=collection_name,
                data=[query_vector],
                limit=limit,
                output_fields=["text", "metadata"] # Assumes these fields exist
            )
            # res is a list of lists, outer list is for each query vector
            if not res or not res[0]:
                return []
                
            results = []
            for hit in res[0]:
                payload = hit.get("entity", {})
                results.append({
                    "id": hit["id"],
                    "score": hit["distance"],
                    "payload": payload
                })
            return results
            
        return await asyncio.to_thread(_search)

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        def _upsert():
            # Ensure collection exists (for simplicity, we assume schema is auto or pre-created)
            if not self.client.has_collection(collection_name=collection_name):
                # We do a basic create with auto_id=False. Real production needs proper schema setup.
                dim = len(points[0]["vector"]) if points and "vector" in points[0] else 1536
                self.client.create_collection(
                    collection_name=collection_name,
                    dimension=dim
                )
                
            data = []
            for p in points:
                # Milvus structure: dict with 'id', 'vector', plus other fields
                row = {
                    "id": p["id"],
                    "vector": p["vector"],
                }
                # merge payload
                if "payload" in p:
                    for k, v in p["payload"].items():
                        row[k] = v
                data.append(row)
                
            self.client.insert(collection_name=collection_name, data=data)
            
        await asyncio.to_thread(_upsert)
