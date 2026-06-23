import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock
from quira.modules.tetris import ContextTetris

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.complete = AsyncMock(return_value="Compressed chunk output")
    return llm

@pytest.mark.asyncio
async def test_tetris_relevance_only(mock_llm):
    tetris = ContextTetris(mock_llm, None)
    
    query_emb = np.array([1.0, 0.0])
    chunk = {
        "id": "c1",
        "text": "Exact match content",
        "embedding": [1.0, 0.0]
    }
    
    score = tetris.score_chunk(chunk, query_emb, 0.0)
    assert score.relevance == 1.0
    assert score.uniqueness == 1.0
    assert score.final_score > 0.6

@pytest.mark.asyncio
async def test_tetris_uniqueness_penalty(mock_llm):
    tetris = ContextTetris(mock_llm, None)
    
    query_emb = np.array([1.0, 0.0])
    chunk1 = {
        "id": "c1",
        "text": "Exact match content",
        "embedding": [1.0, 0.0]
    }
    chunk2 = {
        "id": "c2",
        "text": "Exact match content 2",
        "embedding": [1.0, 0.0] # same embedding means duplicate info
    }
    
    score1 = tetris.score_chunk(chunk1, query_emb, 0.0)
    assert score1.final_score > 0.6
    
    # Simulate chunk1 was already selected (1.0 similarity cache)
    score2 = tetris.score_chunk(chunk2, query_emb, 1.0)
    
    # Uniqueness should heavily penalize chunk2
    assert score2.uniqueness < 0.2
    assert score2.final_score < score1.final_score

@pytest.mark.asyncio
async def test_tetris_packing_budget(mock_llm):
    tetris = ContextTetris(mock_llm, None)
    
    query_emb = np.array([1.0, 0.0])
    pool = []
    # Create 10 chunks of ~20 tokens each
    for i in range(10):
        pool.append({
            "id": f"c{i}",
            "text": "word " * 20, 
            "embedding": [1.0, 0.0],
            "hit_count": 1
        })
        
    packed = await tetris.pack(pool, query_emb, skip_compression=True, token_budget=2600)
    # Should pack some chunks before hitting limit
    assert len(packed.chunks) < 10
    assert len(packed.chunks) >= 3
