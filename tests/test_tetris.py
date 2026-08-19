import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock
from quira.modules.tetris import ContextTetris

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.complete = AsyncMock(return_value="Compressed summary.")
    llm.count_tokens = MagicMock(side_effect=lambda text: max(1, len(text.split())))
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

@pytest.mark.asyncio
async def test_compression_reduces_tokens(mock_llm):
    """Verify that compression actually reduces token count."""
    tetris = ContextTetris(mock_llm, None)
    
    # Create a substantial chunk with multiple sentences
    long_text = (
        "The United States of America was founded in 1776. "
        "George Washington served as the first president. "
        "The country has 50 states and a federal district. "
        "However, many people don't realize that the capital was not always Washington DC. "
        "In fact, the government is quite complex with many branches. "
        "There are various departments that handle different aspects of governance. "
        "The economy is one of the largest in the world. "
        "GDP growth has been steady over the past decades. "
        "Trade relationships span across multiple continents. "
        "Innovation and technology drive much of the economic output."
    )
    
    original_chunk = {
        "id": "test1",
        "text": long_text,
        "embedding": [1.0, 0.0]
    }
    
    compressed = await tetris.compress_chunk(original_chunk, score=0.5)
    
    orig_tokens = mock_llm.count_tokens(long_text)
    comp_tokens = mock_llm.count_tokens(compressed["text"])
    
    # Compressed must be shorter
    assert comp_tokens < orig_tokens
    # Stats should reflect savings
    assert tetris._stats["tokens_saved"] > 0
    assert tetris._stats["compressed_chunks"] > 0

@pytest.mark.asyncio
async def test_compression_preserves_entities(mock_llm):
    """Verify that compression preserves named entities and numbers."""
    tetris = ContextTetris(mock_llm, None)
    
    text_with_entities = (
        "IBM announced quarterly revenue of $14.5 billion on January 25, 2024. "
        "CEO Arvind Krishna highlighted strong performance in the cloud segment. "
        "This represents a 3% year-over-year growth rate. "
        "However, some analysts were disappointed by the results. "
        "The stock price fluctuated throughout the trading day. "
        "Many investors are watching the company's AI strategy closely."
    )
    
    chunk = {
        "id": "test2",
        "text": text_with_entities,
        "embedding": [1.0, 0.0]
    }
    
    compressed = await tetris.compress_chunk(chunk, score=0.6)
    compressed_text = compressed["text"]
    
    # Key entities and numbers must be preserved
    assert "IBM" in compressed_text
    assert "14.5" in compressed_text or "$14.5" in compressed_text
    assert "3%" in compressed_text or "3" in compressed_text

@pytest.mark.asyncio
async def test_no_hardcoded_chunk_limit(mock_llm):
    """Verify that more than 3 chunks can be selected when budget allows."""
    tetris = ContextTetris(mock_llm, None)
    
    query_emb = np.array([1.0, 0.0])
    pool = []
    # Create 8 small chunks (5 tokens each)
    for i in range(8):
        pool.append({
            "id": f"c{i}",
            "text": f"chunk {i} text here ok",
            "embedding": [1.0, float(i) * 0.01],
            "hit_count": 1
        })
    
    # Large budget should allow all chunks
    packed = await tetris.pack(pool, query_emb, skip_compression=True, token_budget=10000)
    
    # Without the old hardcoded limit of 3, we should get more chunks
    assert len(packed.chunks) > 3

@pytest.mark.asyncio
async def test_short_chunks_skip_compression(mock_llm):
    """Chunks under 50 tokens should not be compressed."""
    tetris = ContextTetris(mock_llm, None)
    
    short_chunk = {
        "id": "short1",
        "text": "A brief note.",
        "embedding": [1.0, 0.0]
    }
    
    result = await tetris.compress_chunk(short_chunk, score=0.3)
    assert result["text"] == "A brief note."

@pytest.mark.asyncio
async def test_textrank_extraction():
    """Test that TextRank extractive summarization works correctly."""
    mock_llm = MagicMock()
    mock_llm.count_tokens = MagicMock(side_effect=lambda text: max(1, len(text.split())))
    
    tetris = ContextTetris(mock_llm, None)
    
    text = (
        "Machine learning is a subset of artificial intelligence. "
        "It allows computers to learn from data. "
        "Deep learning uses neural networks with many layers. "
        "Random filler sentence with no real content. "
        "Neural networks are inspired by the human brain. "
        "Training requires large datasets and compute power."
    )
    
    preserved = {"Machine", "learning", "neural", "networks"}
    result = tetris._textrank_extract(text, preserved, target_ratio=0.5)
    
    # Result should be shorter than original
    assert len(result) < len(text)
    # Result should not be empty
    assert len(result) > 0

@pytest.mark.asyncio
async def test_stats_reset_on_each_pack(mock_llm):
    """Stats should be fresh for each pack() call, not accumulated."""
    tetris = ContextTetris(mock_llm, None)
    query_emb = np.array([1.0, 0.0])
    
    pool1 = [{"id": "c1", "text": "word " * 20, "embedding": [1.0, 0.0]}]
    await tetris.pack(pool1, query_emb, skip_compression=True)
    stats1_selected = tetris.get_stats()["selected_chunks"]
    
    pool2 = [{"id": "c2", "text": "word " * 20, "embedding": [1.0, 0.0]},
             {"id": "c3", "text": "word " * 20, "embedding": [0.9, 0.1]}]
    await tetris.pack(pool2, query_emb, skip_compression=True)
    stats2_selected = tetris.get_stats()["selected_chunks"]
    
    # Stats should reflect only the second pack call
    assert stats2_selected == 2
