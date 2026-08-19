import logging
import asyncio
from typing import Any, Dict, List
from quira.providers.base import VectorStore

logger = logging.getLogger("quira.providers.faiss")

class FaissStore(VectorStore):
    """FAISS implementation of the VectorStore interface for ultra-fast local search."""
    
    def __init__(self):
        try:
            import faiss
            import numpy as np
            self.faiss = faiss
            self.np = np
        except ImportError:
            raise ImportError("faiss-cpu not installed. Run `pip install quira[faiss]`")
            
        self.indices = {}
        self.payloads = {}
        self.id_maps = {}

    def _ensure_index(self, collection_name: str, dim: int):
        if collection_name not in self.indices:
            # IndexFlatIP for Inner Product (Cosine similarity if normalized)
            self.indices[collection_name] = self.faiss.IndexFlatIP(dim)
            self.payloads[collection_name] = []
            self.id_maps[collection_name] = []

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        dim = len(points[0].get("vector", []))
        self._ensure_index(collection_name, dim)
        
        vectors = []
        for point in points:
            vec = self.np.array(point.get("vector"), dtype=self.np.float32)
            # Normalize vector for cosine similarity
            norm = self.np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
            
            self.id_maps[collection_name].append(point.get("id"))
            self.payloads[collection_name].append(point.get("payload", {}))
            
        vector_matrix = self.np.array(vectors, dtype=self.np.float32)
        
        def _add():
            self.indices[collection_name].add(vector_matrix)
            
        await asyncio.to_thread(_add)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        if collection_name not in self.indices:
            return []
            
        vec = self.np.array([query_vector], dtype=self.np.float32)
        norm = self.np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
            
        def _search():
            return self.indices[collection_name].search(vec, limit)
            
        distances, indices = await asyncio.to_thread(_search)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1:
                results.append({
                    "id": self.id_maps[collection_name][idx],
                    "payload": self.payloads[collection_name][idx],
                    "score": float(dist)
                })
        return results
