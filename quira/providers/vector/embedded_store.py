import json
import logging
import sqlite3
import numpy as np
from typing import Any, Dict, List, Optional
from quira.providers.base import VectorStore

logger = logging.getLogger(__name__)

class SQLiteVecStore(VectorStore):
    """
    Embedded vector store using sqlite-vec or an in-memory numpy fallback if sqlite-vec is unavailable.
    """
    def __init__(self, db_path: str = "quira_edge.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.has_vec = False
        try:
            import sqlite_vec
            self.conn.enable_load_extension(True)
            sqlite_vec.load(self.conn)
            self.conn.enable_load_extension(False)
            self.has_vec = True
        except ImportError:
            logger.warning("sqlite-vec not found. Falling back to in-memory numpy exact search for SQLite.")
            self._mem_store = {}

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        if not self.has_vec:
            # Fallback to in-memory numpy
            if collection_name not in self._mem_store:
                return []
            
            q_vec = np.array(query_vector)
            results = []
            for id_, (vec, payload) in self._mem_store[collection_name].items():
                v = np.array(vec)
                sim = np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v) + 1e-9)
                results.append((sim, id_, payload, vec))
                
            results.sort(key=lambda x: x[0], reverse=True)
            
            return [{"id": r[1], "payload": r[2], "vector": r[3]} for r in results[:limit]]

        # Using sqlite-vec
        self._ensure_table(collection_name, len(query_vector))
        
        vec_bytes = np.array(query_vector, dtype=np.float32).tobytes()
        cursor = self.conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT id, payload_json 
                FROM {collection_name} 
                WHERE vector MATCH ? AND k = ? 
                ORDER BY distance
            """, (vec_bytes, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": str(row[0]),
                    "payload": json.loads(row[1]) if row[1] else {}
                })
            return results
        except sqlite3.OperationalError as e:
            logger.error(f"SQLite vec search error: {e}")
            return []

    def _ensure_table(self, collection_name: str, dim: int):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS {collection_name} USING vec0(
                id INTEGER PRIMARY KEY,
                vector float[{dim}],
                payload_json TEXT
            );
        """)
        self.conn.commit()

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        if not self.has_vec:
            if collection_name not in self._mem_store:
                self._mem_store[collection_name] = {}
            for p in points:
                self._mem_store[collection_name][p["id"]] = (p["vector"], p.get("payload", {}))
            return

        dim = len(points[0]["vector"])
        self._ensure_table(collection_name, dim)
        
        cursor = self.conn.cursor()
        for p in points:
            vec_bytes = np.array(p["vector"], dtype=np.float32).tobytes()
            # Attempt to extract an integer ID, or use a hash if string
            try:
                numeric_id = int(p["id"])
            except ValueError:
                numeric_id = hash(p["id"]) % ((1 << 63) - 1)
                
            cursor.execute(f"""
                INSERT OR REPLACE INTO {collection_name} (id, vector, payload_json) 
                VALUES (?, ?, ?)
            """, (numeric_id, vec_bytes, json.dumps(p.get("payload", {}))))
            
        self.conn.commit()


class DuckDBStore(VectorStore):
    """
    Embedded vector store using DuckDB.
    """
    def __init__(self, db_path: str = "quira_edge.duckdb"):
        try:
            import duckdb
        except ImportError:
            raise ImportError("Please install duckdb: pip install duckdb")
            
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        
        # Install and load VSS (Vector Similarity Search) if available
        try:
            self.conn.execute("INSTALL vss;")
            self.conn.execute("LOAD vss;")
            self.has_vss = True
        except Exception as e:
            logger.warning(f"DuckDB VSS extension not available: {e}. Will use exact array math.")
            self.has_vss = False

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        try:
            self.conn.execute(f"SELECT 1 FROM {collection_name} LIMIT 1")
        except Exception:
            return [] # Table does not exist

        dim = len(query_vector)
        vec_str = "[" + ",".join(map(str, query_vector)) + "]"
        
        if self.has_vss:
            query = f"""
            SELECT id, payload, array_cosine_similarity(vector, {vec_str}::FLOAT[{dim}]) as sim
            FROM {collection_name}
            ORDER BY sim DESC
            LIMIT {limit}
            """
        else:
             # DuckDB native array cosine distance might need specific syntax, but let's try a direct exact match if possible, 
             # or just load into memory if it's small. VSS is standard for duckdb vector search now.
             query = f"""
             SELECT id, payload, list_cosine_distance(vector, {vec_str}::DOUBLE[]) as dist
             FROM {collection_name}
             ORDER BY dist ASC
             LIMIT {limit}
             """
             
        try:
            results = self.conn.execute(query).fetchall()
        except Exception as e:
            logger.error(f"DuckDB search error: {e}")
            return []
            
        ret = []
        for row in results:
            ret.append({
                "id": str(row[0]),
                "payload": json.loads(row[1]) if row[1] else {}
            })
        return ret

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        if not points:
            return
            
        dim = len(points[0]["vector"])
        
        if self.has_vss:
            self.conn.execute(f"CREATE TABLE IF NOT EXISTS {collection_name} (id VARCHAR, vector FLOAT[{dim}], payload VARCHAR)")
        else:
            self.conn.execute(f"CREATE TABLE IF NOT EXISTS {collection_name} (id VARCHAR, vector DOUBLE[], payload VARCHAR)")
            
        insert_data = []
        for p in points:
            insert_data.append((str(p["id"]), p["vector"], json.dumps(p.get("payload", {}))))
            
        self.conn.executemany(
            f"INSERT INTO {collection_name} (id, vector, payload) VALUES (?, ?, ?)", 
            insert_data
        )
