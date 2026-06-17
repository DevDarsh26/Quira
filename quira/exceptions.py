class QuiraError(Exception):
    """Base exception for all Quira errors."""
    def __init__(self, message: str, context: dict = None):
        super().__init__(message)
        self.context = context or {}

class VectorStoreUnavailableError(QuiraError):
    """Raised when the vector store is unavailable."""
    pass

class CacheUnavailableError(QuiraError):
    """Raised when the cache backend is unavailable."""
    pass

class LLMProviderError(QuiraError):
    """Raised when the LLM provider fails."""
    pass

class ContextOverflowError(QuiraError):
    """Raised when the context length exceeds the model's limit."""
    pass

class RetrievalTimeoutError(QuiraError):
    """Raised when retrieving context times out."""
    pass
