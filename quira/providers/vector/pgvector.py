import os
import json
import logging
from typing import Any, Dict, List
from quira.providers.base import VectorStore

logger = logging.getLogger("quira.providers.pgvector")

class PGVectorStore(VectorStore):
    """PostgreSQL pgvector implementation of the VectorStore interface using asyncpg."""
    
    def __init__(self, connection_string: str = None):
        try:
            import asyncpg
            from pgvector.asyncpg import register_vector
            self.asyncpg = asyncpg
            self.register_vector = register_vector
        except ImportError:
            raise ImportError("pgvector or asyncpg not installed. Run `pip install quira[postgres]`")
            
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("PG connection string must be provided or DATABASE_URL must be set.")
            
        self._pool = None

    async def _get_pool(self):
        if self._pool is None:
            self._pool = await self.asyncpg.create_pool(self.connection_string)
            async with self._pool.acquire() as conn:
                await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                await self.register_vector(conn)
        return self._pool

    async def _ensure_table(self, collection_name: str, dim: int):
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            # We assume collection_name is safe (no SQL injection)
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {collection_name} (
                    id TEXT PRIMARY KEY,
                    embedding vector({dim}),
                    payload JSONB
                )
            """)

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        dim = len(points[0].get("vector", []))
        await self._ensure_table(collection_name, dim)
        
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            for point in points:
                pid = str(point.get("id"))
                vec = point.get("vector")
                payload = json.dumps(point.get("payload", {}))
                
                await conn.execute(f"""
                    INSERT INTO {collection_name} (id, embedding, payload)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE SET 
                        embedding = EXCLUDED.embedding,
                        payload = EXCLUDED.payload;
                """, pid, vec, payload)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            # Check if table exists
            try:
                # Use exact L2 distance or cosine distance (<=> for cosine)
                rows = await conn.fetch(f"""
                    SELECT id, payload, embedding <=> $1 AS distance
                    FROM {collection_name}
                    ORDER BY distance
                    LIMIT $2;
                """, query_vector, limit)
            except self.asyncpg.exceptions.UndefinedTableError:
                return []
                
        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "payload": json.loads(row["payload"]) if row["payload"] else {},
                "score": 1.0 - row["distance"] # rough conversion to similarity
            })
        return results
