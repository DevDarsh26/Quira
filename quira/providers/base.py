from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional, Union

class VectorStore(ABC):
    """Abstract base class for vector databases."""
    
    @abstractmethod
    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search the vector store for nearest neighbors.
        Returns a list of dicts with at least 'id' and 'payload'.
        """
        pass
        
    @abstractmethod
    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        """
        Upsert points into the vector store.
        Each point is a dict with 'id', 'vector', and 'payload'.
        """
        pass

class CacheBackend(ABC):
    """Abstract base class for caching systems."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Retrieve a string from cache by key."""
        pass
        
    @abstractmethod
    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        """Store a string in cache with an optional TTL in seconds."""
        pass
        
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a key from cache."""
        pass

class LLMProvider(ABC):
    """Abstract base class for Large Language Models."""
    
    @abstractmethod
    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        """Generate a text completion given a prompt."""
        pass
        
    @abstractmethod
    async def stream(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        """Generate a text completion stream given a prompt, yielding strings incrementally."""
        pass
        
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text.
        This is synchronous as many local embedding models (e.g. fastembed) are synchronous,
        and it's often used heavily in CPU-bound contexts.
        """
        pass
