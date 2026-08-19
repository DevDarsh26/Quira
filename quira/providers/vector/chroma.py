import asyncio
from typing import Any, List, Dict, Optional
from quira.providers.base import VectorStore

class ChromaStore(VectorStore):
    def __init__(self, client: Any = None, path: str = "./chroma_db"):
        """
        Adapter for ChromaDB.
        Accepts a pre-initialized Chroma client OR initializes a persistent client.
        """
        if client:
            self.client = client
        else:
            try:
                import chromadb
                self.client = chromadb.PersistentClient(path=path)
            except ImportError:
                raise ImportError("ChromaDB not installed. Run `pip install quira[chroma]`")

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        loop = asyncio.get_event_loop()
        
        def _do_search():
            collection = self.client.get_or_create_collection(name=collection_name)
            results = collection.query(
                query_embeddings=[query_vector],
                n_results=limit,
                include=["metadatas"]
            )
            hits = []
            if results and "ids" in results and results["ids"]:
                # Chroma returns lists of lists for multiple query embeddings
                ids = results["ids"][0]
                metadatas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else [{}] * len(ids)
                
                for i in range(len(ids)):
                    hits.append({"id": ids[i], "payload": metadatas[i]})
            return hits
            
        return await loop.run_in_executor(None, _do_search)

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        loop = asyncio.get_event_loop()
        
        def _do_upsert():
            collection = self.client.get_or_create_collection(name=collection_name)
            
            ids = [str(p["id"]) for p in points]
            embeddings = [p["vector"] for p in points]
            metadatas = [p.get("payload", {}) for p in points]
            
            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
        await loop.run_in_executor(None, _do_upsert)
