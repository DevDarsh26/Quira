import logging
from typing import Any, Dict, List, Tuple
from .base import GraphStore

logger = logging.getLogger(__name__)

class LocalGraphStore(GraphStore):
    """
    Lightweight, local in-memory Graph store using NetworkX.
    """
    def __init__(self):
        try:
            import networkx as nx
            self.G = nx.MultiDiGraph()
            self.has_nx = True
        except ImportError:
            logger.warning("networkx not installed. GraphRAG will use a basic dictionary fallback.")
            self.has_nx = False
            self.fallback_graph = {}

    async def add_triplets(self, triplets: List[Tuple[str, str, str, Dict[str, Any]]]) -> None:
        if not triplets:
            return
            
        if self.has_nx:
            for sub, rel, obj, meta in triplets:
                self.G.add_edge(sub, obj, relation=rel, **meta)
        else:
            for sub, rel, obj, meta in triplets:
                if sub not in self.fallback_graph:
                    self.fallback_graph[sub] = []
                self.fallback_graph[sub].append((rel, obj, meta))

    async def get_neighbors(self, entity: str, max_hops: int = 1) -> List[Dict[str, Any]]:
        results = []
        if self.has_nx:
            import networkx as nx
            if entity not in self.G:
                return results
            
            # Simple BFS up to max_hops
            visited = set([entity])
            queue = [(entity, 0)]
            
            while queue:
                current, hop = queue.pop(0)
                if hop >= max_hops:
                    continue
                    
                for neighbor in self.G.successors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, hop + 1))
                        # Record edge
                        edge_data = self.G.get_edge_data(current, neighbor)
                        if edge_data:
                            for k, v in edge_data.items():
                                results.append({
                                    "subject": current,
                                    "relation": v.get("relation"),
                                    "object": neighbor,
                                    "metadata": {key: val for key, val in v.items() if key != "relation"}
                                })
                                
                for neighbor in self.G.predecessors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, hop + 1))
                        edge_data = self.G.get_edge_data(neighbor, current)
                        if edge_data:
                            for k, v in edge_data.items():
                                results.append({
                                    "subject": neighbor,
                                    "relation": v.get("relation"),
                                    "object": current,
                                    "metadata": {key: val for key, val in v.items() if key != "relation"}
                                })
        else:
            # Basic dictionary traversal
            if entity in self.fallback_graph:
                for rel, obj, meta in self.fallback_graph[entity]:
                    results.append({
                        "subject": entity,
                        "relation": rel,
                        "object": obj,
                        "metadata": meta
                    })
        return results

    async def search_entities(self, query: str) -> List[str]:
        # Simple substring matching
        q = query.lower()
        matches = []
        
        if self.has_nx:
            for node in self.G.nodes():
                if q in str(node).lower():
                    matches.append(node)
        else:
            for node in self.fallback_graph.keys():
                if q in str(node).lower():
                    matches.append(node)
                    
        return matches
