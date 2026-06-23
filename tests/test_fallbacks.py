import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from quira.providers.fallback import FallbackVectorStore, FallbackLLMProvider
from quira.exceptions import VectorStoreUnavailableError

@pytest.fixture
def failing_primary():
    primary = MagicMock()
    primary.search = AsyncMock(side_effect=Exception("Primary DB Down"))
    primary.complete = AsyncMock(side_effect=Exception("Primary LLM Down"))
    return primary
    
@pytest.fixture
def working_fallback():
    fallback = MagicMock()
    fallback.search = AsyncMock(return_value=[{"id": "fallback_chunk"}])
    fallback.complete = AsyncMock(return_value="Fallback answer")
    return fallback

@pytest.mark.asyncio
async def test_vector_store_fallback(failing_primary, working_fallback):
    # Shorten base delay for test speed
    fb_store = FallbackVectorStore(failing_primary, working_fallback)
    
    results = await fb_store.search("collection", [0.0, 1.0])
    
    assert len(results) == 1
    assert results[0]["id"] == "fallback_chunk"
    assert failing_primary.search.call_count == 3 # 1 initial + 2 retries
    working_fallback.search.assert_called_once()

@pytest.mark.asyncio
async def test_vector_store_no_fallback_total_failure(failing_primary):
    fb_store = FallbackVectorStore(failing_primary, fallback=None)
    
    with pytest.raises(VectorStoreUnavailableError) as exc_info:
        await fb_store.search("collection", [0.0, 1.0])
        
    assert "Primary vector store failed and no fallback available." in str(exc_info.value)
    assert failing_primary.search.call_count == 3

@pytest.mark.asyncio
async def test_llm_fallback(failing_primary, working_fallback):
    fb_llm = FallbackLLMProvider(failing_primary, working_fallback)
    
    answer = await fb_llm.complete("Hello")
    
    assert answer == "Fallback answer"
    assert failing_primary.complete.call_count == 3
    working_fallback.complete.assert_called_once()
