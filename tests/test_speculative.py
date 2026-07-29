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
        return [{"id": "hit1", "payload": {"text": "sample text"}}]
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
    
    # The debouncer delays for ~2.5s for the first/slow keystrokes
    # Let's wait long enough for the LAST keystroke's debounce to fire, plus search time
    await asyncio.sleep(3.0)
    
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

@pytest.mark.asyncio
async def test_semantic_cache_hit(mock_vector_store, mock_cache):
    """Test that semantic cache hits work when submitted query is close to typed query."""
    call_count = 0
    
    def mock_embed(text):
        nonlocal call_count
        call_count += 1
        # Simulate embeddings that are semantically close
        if "quantum comp" in text.lower():
            return np.array([0.9, 0.1])
        elif "quantum computing" in text.lower():
            return np.array([0.91, 0.09])  # Very close to above
        return np.array([0.5, 0.5])
    
    spec = SpeculativeRetriever("user1", mock_vector_store, mock_cache, embed_func=mock_embed)
    
    # Simulate typing "quantum comp" which triggers speculative search
    await spec.on_keystroke("quantum comp")
    await asyncio.sleep(2.5)  # Wait for debounce + search to complete
    
    # Now submit "quantum computing" — should get semantic cache hit
    results = await spec.on_submit("quantum computing")
    
    stats = spec.get_stats()
    # Should be a semantic cache hit (not exact, but semantic)
    assert stats["cache_hits"] >= 1
    assert stats["semantic_cache_hits"] >= 1

@pytest.mark.asyncio
async def test_exact_cache_hit(mock_vector_store, mock_cache):
    """Test that exact SHA-256 cache hits work when query matches perfectly."""
    import json
    
    mock_results = [{"id": "hit1", "payload": {"text": "cached result"}}]
    
    # Mock cache to return a result for the exact hash
    async def mock_get(key):
        if "speculative:" in key:
            return json.dumps(mock_results)
        return None
    
    mock_cache.get = AsyncMock(side_effect=mock_get)
    
    spec = SpeculativeRetriever("user1", mock_vector_store, mock_cache, embed_func=lambda t: np.array([0.5, 0.5]))
    
    results = await spec.on_submit("test query")
    
    assert len(results) == 1
    assert results[0]["id"] == "hit1"
    stats = spec.get_stats()
    assert stats["cache_hits"] == 1

@pytest.mark.asyncio
async def test_no_fake_time_saved(mock_vector_store, mock_cache):
    """Verify time_saved_ms has no artificial +820ms padding."""
    import json
    
    mock_results = [{"id": "hit1"}]
    mock_cache.get = AsyncMock(return_value=json.dumps(mock_results))
    
    spec = SpeculativeRetriever("user1", mock_vector_store, mock_cache, embed_func=lambda t: np.array([0.5, 0.5]))
    
    await spec.on_submit("test query")
    
    stats = spec.get_stats()
    # time_saved_ms should be small (< 100ms for an in-memory cache hit), not inflated by 820ms
    assert stats["time_saved_ms"] < 100

@pytest.mark.asyncio
async def test_draft_pregeneration_disabled_by_default(mock_vector_store, mock_cache):
    """Draft pre-generation should not fire unless explicitly enabled."""
    mock_llm = MagicMock()
    mock_llm.complete = AsyncMock(return_value="Draft response")
    
    spec = SpeculativeRetriever(
        "user1", mock_vector_store, mock_cache,
        embed_func=lambda t: np.array([0.5, 0.5]),
        llm=mock_llm
    )
    
    # Default: enable_draft_pregeneration=False
    assert spec.enable_draft_pregeneration is False
    
    # Run speculative task — should NOT call LLM
    await spec.on_keystroke("hello world test")
    await asyncio.sleep(1.0)
    
    mock_llm.complete.assert_not_called()

@pytest.mark.asyncio 
async def test_cosine_similarity_helper(mock_vector_store, mock_cache):
    """Test the cosine similarity helper method."""
    spec = SpeculativeRetriever("user1", mock_vector_store, mock_cache, embed_func=lambda t: np.array([1, 0]))
    
    # Identical vectors
    sim = spec._cosine_similarity(np.array([1.0, 0.0]), np.array([1.0, 0.0]))
    assert abs(sim - 1.0) < 0.001
    
    # Orthogonal vectors
    sim = spec._cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    assert abs(sim) < 0.001
    
    # Zero vector
    sim = spec._cosine_similarity(np.array([0.0, 0.0]), np.array([1.0, 0.0]))
    assert sim == 0.0
