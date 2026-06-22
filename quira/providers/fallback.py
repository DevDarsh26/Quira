import logging
from typing import Any, List, Dict, Optional
from quira.providers.base import VectorStore, LLMProvider
from quira.core.retry import with_retry, with_retry_sync
from quira.exceptions import VectorStoreUnavailableError, LLMProviderError

logger = logging.getLogger("quira.fallback")

class FallbackVectorStore(VectorStore):
    def __init__(self, primary: VectorStore, fallback: Optional[VectorStore] = None):
        self.primary = primary
        self.fallback = fallback

    @with_retry(max_attempts=3, base_delay=0.5)
    async def _search_primary(self, collection_name: str, query_vector: List[float], limit: int):
        return await self.primary.search(collection_name, query_vector, limit)

    @with_retry(max_attempts=3, base_delay=0.5)
    async def _upsert_primary(self, collection_name: str, points: List[Dict[str, Any]]):
        return await self.primary.upsert(collection_name, points)

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        try:
            return await self._search_primary(collection_name, query_vector, limit)
        except Exception as e:
            if self.fallback:
                logger.warning(f"Primary vector store failed: {e}. Switching to fallback.")
                try:
                    return await self.fallback.search(collection_name, query_vector, limit)
                except Exception as fallback_e:
                    logger.error(f"Fallback vector store also failed: {fallback_e}")
                    raise VectorStoreUnavailableError("Both primary and fallback vector stores failed.", {"primary_error": str(e), "fallback_error": str(fallback_e)})
            else:
                raise VectorStoreUnavailableError("Primary vector store failed and no fallback available.", {"error": str(e)})

    async def upsert(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        try:
            await self._upsert_primary(collection_name, points)
        except Exception as e:
            if self.fallback:
                logger.warning(f"Primary vector store failed during upsert: {e}. Switching to fallback.")
                try:
                    await self.fallback.upsert(collection_name, points)
                except Exception as fallback_e:
                    logger.error(f"Fallback vector store also failed during upsert: {fallback_e}")
                    raise VectorStoreUnavailableError("Both primary and fallback vector stores failed during upsert.", {"primary_error": str(e), "fallback_error": str(fallback_e)})
            else:
                raise VectorStoreUnavailableError("Primary vector store failed during upsert and no fallback available.", {"error": str(e)})

class FallbackLLMProvider(LLMProvider):
    def __init__(self, primary: LLMProvider, fallback: Optional[LLMProvider] = None):
        self.primary = primary
        self.fallback = fallback

    @with_retry(max_attempts=3, base_delay=0.5)
    async def _complete_primary(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        return await self.primary.complete(prompt, system_prompt, model)

    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        try:
            return await self._complete_primary(prompt, system_prompt, model)
        except Exception as e:
            if self.fallback:
                logger.warning(f"Primary LLM provider failed: {e}. Switching to fallback.")
                try:
                    return await self.fallback.complete(prompt, system_prompt, model)
                except Exception as fallback_e:
                    logger.error(f"Fallback LLM provider also failed: {fallback_e}")
                    raise LLMProviderError("Both primary and fallback LLM providers failed.", {"primary_error": str(e), "fallback_error": str(fallback_e)})
            else:
                raise LLMProviderError("Primary LLM provider failed and no fallback available.", {"error": str(e)})

    async def _stream_primary(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        async for chunk in self.primary.stream(prompt, system_prompt, model):
            yield chunk

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        try:
            async for chunk in self._stream_primary(prompt, system_prompt, model):
                yield chunk
        except Exception as e:
            if self.fallback:
                logger.warning(f"Primary LLM provider failed during streaming: {e}. Switching to fallback.")
                try:
                    async for chunk in self.fallback.stream(prompt, system_prompt, model):
                        yield chunk
                except Exception as fallback_e:
                    logger.error(f"Fallback LLM provider also failed during streaming: {fallback_e}")
                    raise LLMProviderError("Both primary and fallback LLM providers failed during streaming.", {"primary_error": str(e), "fallback_error": str(fallback_e)})
            else:
                raise LLMProviderError("Primary LLM provider failed during streaming and no fallback available.", {"error": str(e)})

    @with_retry_sync(max_attempts=3, base_delay=0.5)
    def _embed_primary(self, text: str) -> List[float]:
        return self.primary.embed(text)

    def embed(self, text: str) -> List[float]:
        try:
            return self._embed_primary(text)
        except Exception as e:
            if self.fallback:
                logger.warning(f"Primary LLM provider failed during embedding: {e}. Switching to fallback.")
                try:
                    return self.fallback.embed(text)
                except Exception as fallback_e:
                    logger.error(f"Fallback LLM provider also failed during embedding: {fallback_e}")
                    raise LLMProviderError("Both primary and fallback LLM providers failed during embedding.", {"primary_error": str(e), "fallback_error": str(fallback_e)})
            else:
                raise LLMProviderError("Primary LLM provider failed during embedding and no fallback available.", {"error": str(e)})
