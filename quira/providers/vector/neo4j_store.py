import os
import logging
from typing import Any, Dict, List
from quira.providers.base import VectorStore
from quira.providers.graph.base import GraphStore

logger = logging.getLogger("quira.providers.neo4j")

class Neo4jStore(VectorStore, GraphStore):
    """Neo4j hybrid store implementing BOTH VectorStore and GraphStore."""
    
    def __init__(self, uri: str = None, username: str = None, password: str = None):
        try:
            from neo4j import AsyncGraphDatabase
            self.driver_cls = AsyncGraphDatabase
        except ImportError:
            raise ImportError("neo4j driver not installed. Run `pip install quira[neo4j]`")
            
        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = username or os.getenv("NEO4J_USERNAME", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD", "password")
        
        self.driver = self.driver_cls.driver(uri, auth=(user, password))

    async def _close(self):
        await self.driver.close()

    # --- VECTOR STORE METHODS ---
    async def _ensure_vector_index(self, collection_name: str, dim: int):
        query = f"""
        CREATE VECTOR INDEX {collection_name}_vector IF NOT EXISTS
        FOR (n:Chunk) ON (n.embedding)
        OPTIONS {{indexConfig: {{
         `vector.dimensions`: {dim},
         `vector.similarity_function`: 'cosine'
        }}}}
        """
        async with self.driver.session() as session:
            await session.run(query)

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        dim = len(points[0].get("vector", []))
        await self._ensure_vector_index(collection_name, dim)
        
        query = """
        UNWIND $points AS point
        MERGE (c:Chunk {id: point.id, collection: $collection_name})
        SET c.embedding = point.vector,
            c.payload = point.payload
        """
        async with self.driver.session() as session:
            await session.run(query, points=points, collection_name=collection_name)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        query = f"""
        CALL db.index.vector.queryNodes('{collection_name}_vector', $limit, $vector)
        YIELD node, score
        WHERE node.collection = $collection_name
        RETURN node.id AS id, node.payload AS payload, score
        """
        async with self.driver.session() as session:
            result = await session.run(query, limit=limit, vector=query_vector)
            records = await result.data()
            
        return [{
            "id": r["id"],
            "payload": r.get("payload", {}),
            "score": r["score"]
        } for r in records]

    # --- GRAPH STORE METHODS ---
    async def add_triplets(self, triplets: List[Dict[str, str]]) -> None:
        if not triplets:
            return
            
        query = """
        UNWIND $triplets AS t
        MERGE (s:Entity {name: toLower(t.subject)})
        MERGE (o:Entity {name: toLower(t.object)})
        WITH s, o, t
        CALL apoc.create.relationship(s, toUpper(replace(t.relation, ' ', '_')), {}, o) YIELD rel
        RETURN count(*)
        """
        async with self.driver.session() as session:
            try:
                # Requires APOC for dynamic relationship types
                await session.run(query, triplets=triplets)
            except Exception as e:
                logger.warning(f"Neo4j APOC not installed or query failed. Fallback to generic relation. {e}")
                fb_query = """
                UNWIND $triplets AS t
                MERGE (s:Entity {name: toLower(t.subject)})
                MERGE (o:Entity {name: toLower(t.object)})
                MERGE (s)-[r:RELATED_TO {type: t.relation}]->(o)
                """
                await session.run(fb_query, triplets=triplets)

    async def get_neighbors(self, query: str, max_hops: int = 2) -> List[Dict[str, Any]]:
        # Basic heuristic: extract words, find entities, return their relationships
        words = [w.lower() for w in query.split() if len(w) > 3]
        if not words:
            return []
            
        query_str = """
        MATCH (s:Entity)-[r]-(o:Entity)
        WHERE any(w in $words WHERE s.name CONTAINS w OR o.name CONTAINS w)
        RETURN s.name AS subject, type(r) AS relation, o.name AS object
        LIMIT 20
        """
        
        async with self.driver.session() as session:
            result = await session.run(query_str, words=words)
            records = await result.data()
            
        return [{
            "subject": r["subject"],
            "relation": r["relation"],
            "object": r["object"]
        } for r in records]
