import os
import logging
from typing import Any, Dict, List
from quira.providers.base import VectorStore

logger = logging.getLogger("quira.providers.mongodb")

class MongoDBStore(VectorStore):
    """MongoDB Atlas Vector Search implementation of the VectorStore interface."""
    
    def __init__(self, connection_string: str = None, database_name: str = "quira_db"):
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            self.client_class = AsyncIOMotorClient
        except ImportError:
            raise ImportError("motor not installed. Run `pip install quira[mongodb]`")
            
        self.connection_string = connection_string or os.getenv("MONGODB_URI")
        if not self.connection_string:
            raise ValueError("MONGODB_URI must be set.")
            
        self.client = self.client_class(self.connection_string)
        self.db = self.client[database_name]

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        collection = self.db[collection_name]
        operations = []
        try:
            from pymongo import UpdateOne
        except ImportError:
            pass

        for point in points:
            pid = point.get("id")
            doc = {
                "_id": pid,
                "id": pid,
                "vector": point.get("vector"),
                "payload": point.get("payload", {})
            }
            operations.append(UpdateOne({"_id": pid}, {"$set": doc}, upsert=True))
            
        if operations:
            await collection.bulk_write(operations)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        collection = self.db[collection_name]
        
        # Note: This requires a vector search index created in Atlas with the name 'default'
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "default",
                    "path": "vector",
                    "queryVector": query_vector,
                    "numCandidates": limit * 10,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "id": 1,
                    "payload": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        results = []
        async for doc in collection.aggregate(pipeline):
            results.append({
                "id": doc.get("id"),
                "payload": doc.get("payload", {}),
                "score": doc.get("score", 0.0)
            })
            
        return results
