import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock
from quira.modules.differential import DifferentialRetriever

@pytest.fixture
def mock_vector_store():
    store = MagicMock()
    store.search = AsyncMock(return_value=[
        {"id": "c1", "payload": {"text": "chunk1", "embedding": [1.0, 0.0]}},
        {"id": "c2", "payload": {"text": "chunk2", "embedding": [0.0, 1.0]}}
    ])
    return store

@pytest.mark.asyncio
async def test_differential_state_management(mock_vector_store):
    def mock_embed(text):
        return np.array([1.0, 0.0])
        
    diff = DifferentialRetriever("user_state_test", mock_vector_store, embed_func=mock_embed)
    
    # Initial retrieve
    chunks = await diff.retrieve("query 1")
    assert diff.turn_count == 1
    assert len(diff.context_pool) == 2
    
    # Retrieve again with exact same query vector -> semantic delta is 0
    # Expected behavior: skip fetching redundant info
    chunks2 = await diff.retrieve("query 2")
    assert diff.turn_count == 2
    assert len(chunks2) == 0
    assert diff._stats["chunks_skipped"] == 2
    
    # Reset state
    diff.force_reset()
    assert diff.turn_count == 0
    assert len(diff.context_pool) == 0

@pytest.mark.asyncio
async def test_differential_new_information(mock_vector_store):
    def mock_embed(text):
        if text == "query 1":
            return np.array([1.0, 0.0])
        else:
            return np.array([-1.0, 0.0])
            
    diff = DifferentialRetriever("user_new_info", mock_vector_store, embed_func=mock_embed)
    
    # Query 1
    await diff.retrieve("query 1")
    
    # Query 2 (different vector)
    # Update mock to return new chunk
    mock_vector_store.search = AsyncMock(return_value=[
        {"id": "c3", "payload": {"text": "chunk3", "embedding": [-1.0, 0.0]}}
    ])
    chunks = await diff.retrieve("query 2")
    
    assert len(chunks) == 1
    assert chunks[0]["id"] == "c3"
    assert len(diff.context_pool) == 3 # c1, c2 from turn 1, c3 from turn 2
