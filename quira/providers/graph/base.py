from abc import ABC, abstractmethod
from typing import Any, List, Dict, Tuple, Optional

class GraphStore(ABC):
    """Abstract base class for Graph storage (Knowledge Graph)."""
    
    @abstractmethod
    async def add_triplets(self, triplets: List[Tuple[str, str, str, Dict[str, Any]]]) -> None:
        """
        Add entity-relationship triplets.
        Format: (subject, relation, object, metadata)
        """
        pass
        
    @abstractmethod
    async def get_neighbors(self, entity: str, max_hops: int = 1) -> List[Dict[str, Any]]:
        """
        Get neighboring nodes and relationships for a given entity up to max_hops.
        Returns a list of dicts representing the connected sub-graph.
        """
        pass
        
    @abstractmethod
    async def search_entities(self, query: str) -> List[str]:
        """
        Fuzzy search or exact match for entities in the graph based on a query string.
        """
        pass
