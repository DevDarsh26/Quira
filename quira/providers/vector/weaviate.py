import asyncio
from typing import Any, List, Dict, Optional
from quira.providers.base import VectorStore

class WeaviateStore(VectorStore):
    def __init__(self, client: Any = None, url: str = "http://localhost:8080"):
        """
        Adapter for Weaviate.
        """
        if client:
            self.client = client
        else:
            try:
                import weaviate
                self.client = weaviate.Client(url=url)
            except ImportError:
                raise ImportError("Weaviate client not installed. Run `pip install quira[weaviate]`")

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        # Capitalize class name per Weaviate conventions
        class_name = collection_name.capitalize()
        loop = asyncio.get_event_loop()
        
        def _do_search():
            result = (
                self.client.query
                .get(class_name, ["text", "created_at", "source"]) # Requested properties based on Quira usage
                .with_additional(["id"])
                .with_near_vector({
                    "vector": query_vector
                })
                .with_limit(limit)
                .do()
            )
            
            hits = []
            if "data" in result and "Get" in result["data"] and class_name in result["data"]["Get"]:
                for item in result["data"]["Get"][class_name]:
                    item_id = item.get("_additional", {}).get("id", "")
                    payload = {k: v for k, v in item.items() if k != "_additional"}
                    hits.append({"id": item_id, "payload": payload})
            return hits
            
        return await loop.run_in_executor(None, _do_search)

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        class_name = collection_name.capitalize()
        loop = asyncio.get_event_loop()
        
        def _do_upsert():
            # Ensure class exists
            if not self.client.schema.exists(class_name):
                self.client.schema.create_class({
                    "class": class_name,
                    "vectorizer": "none" # We provide our own vectors
                })
                
            with self.client.batch as batch:
                for p in points:
                    batch.add_data_object(
                        data_object=p.get("payload", {}),
                        class_name=class_name,
                        uuid=p["id"],
                        vector=p["vector"]
                    )
                    
        await loop.run_in_executor(None, _do_upsert)
