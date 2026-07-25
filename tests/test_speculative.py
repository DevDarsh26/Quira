import pytest
import asyncio
import numpy as np
from unittest.mock import AsyncMock, MagicMock
from quira.modules.speculative import SpeculativeRetriever

@pytest.fixture
def mock_vector_store():
    store = MagicMock()
    # Need to make search a coroutine that waits a little so we can test cancellation
    async def mock_search(*args, **kwargs):
        await asyncio.sleep(0.1)
        return [{"id": "hit1"}]
    store.search = AsyncMock(side_effect=mock_search)
    return store

@pytest.fixture
def mock_cache():
    cache = MagicMock()
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock()
    return cache

@pytest.mark.asyncio
async def test_speculative_rapid_typing(mock_vector_store, mock_cache):
    def mock_embed(text):
        return np.array([0.5, 0.5])
        
    spec = SpeculativeRetriever("user1", mock_vector_store, mock_cache, embed_func=mock_embed)
    
    # Simulate rapid typing where debounce shouldn't fire until the end
    await spec.on_keystroke("h")
    await asyncio.sleep(0.05)
    await spec.on_keystroke("he")
    await asyncio.sleep(0.05)
    await spec.on_keystroke("hel")
    await asyncio.sleep(0.05)
    await spec.on_keystroke("hello")
    
    # The debouncer delays for ~0.4s for the first/slow keystrokes
    # Let's wait long enough for the LAST keystroke's debounce to fire, plus search time
    await asyncio.sleep(1.0)
    
    # We should only have performed ONE search because the earlier ones were aborted/debounced
    assert mock_vector_store.search.call_count == 1
    
    stats = spec.get_stats()
    assert stats["searches_completed"] == 1
    
    # Ensure debouncer doesn't leave lingering tasks
    assert len(spec.debouncer._tasks) == 0

@pytest.mark.asyncio
async def test_speculative_search_timeout(mock_vector_store, mock_cache):
    async def slow_search(*args, **kwargs):
        await asyncio.sleep(10.0) # Longer than 5.0s timeout
        return []
    
    mock_vector_store.search = AsyncMock(side_effect=slow_search)
    
    spec = SpeculativeRetriever("user1", mock_vector_store, mock_cache, embed_func=lambda t: np.array([1, 0]))
    
    # This should internally timeout without throwing an unhandled exception
    res = await spec._perform_search(np.array([1.0, 0.0]))
    assert res == []
