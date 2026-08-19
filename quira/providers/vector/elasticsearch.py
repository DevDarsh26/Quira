import os
import logging
from typing import Any, Dict, List
from quira.providers.base import VectorStore

logger = logging.getLogger("quira.providers.elasticsearch")

class ElasticsearchStore(VectorStore):
    """Elasticsearch implementation of the VectorStore interface using kNN."""
    
    def __init__(self, connection_string: str = None):
        try:
            from elasticsearch import AsyncElasticsearch
            self.client_class = AsyncElasticsearch
        except ImportError:
            raise ImportError("elasticsearch not installed. Run `pip install quira[elasticsearch]`")
            
        self.connection_string = connection_string or os.getenv("ELASTICSEARCH_URL")
        if not self.connection_string:
            raise ValueError("ELASTICSEARCH_URL must be set.")
            
        self.client = self.client_class(self.connection_string)

    async def _ensure_index(self, index_name: str, dim: int):
        exists = await self.client.indices.exists(index=index_name)
        if not exists:
            mapping = {
                "mappings": {
                    "properties": {
                        "vector": {
                            "type": "dense_vector",
                            "dims": dim,
                            "index": True,
                            "similarity": "cosine"
                        },
                        "payload": {
                            "type": "object",
                            "enabled": False
                        }
                    }
                }
            }
            await self.client.indices.create(index=index_name, body=mapping)

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        dim = len(points[0].get("vector", []))
        await self._ensure_index(collection_name, dim)
        
        operations = []
        for point in points:
            operations.append({"index": {"_index": collection_name, "_id": str(point.get("id"))}})
            operations.append({
                "vector": point.get("vector"),
                "payload": point.get("payload", {})
            })
            
        await self.client.bulk(body=operations, refresh=True)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        exists = await self.client.indices.exists(index=collection_name)
        if not exists:
            return []
            
        query = {
            "knn": {
                "field": "vector",
                "query_vector": query_vector,
                "k": limit,
                "num_candidates": limit * 5
            },
            "_source": ["payload"]
        }
        
        response = await self.client.search(index=collection_name, body=query, size=limit)
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "id": hit["_id"],
                "payload": hit["_source"].get("payload", {}),
                "score": hit["_score"]
            })
        return results
