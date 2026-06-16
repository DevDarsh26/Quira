import pytest
import numpy as np
import asyncio
from unittest.mock import AsyncMock, MagicMock

from quira.modules.differential import DifferentialRetriever
from quira.modules.tetris import ContextTetris
from quira.modules.ingestion import DocumentIngestor

@pytest.fixture
def mock_vector_store():
    store = MagicMock()
    # Mock search to return 2 simple chunks
    store.search = AsyncMock(return_value=[
        {"id": "c1", "payload": {"text": "chunk1", "embedding": [1.0, 0.0]}},
        {"id": "c2", "payload": {"text": "chunk2", "embedding": [0.0, 1.0]}}
    ])
    store.upsert = AsyncMock()
    return store

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.complete = AsyncMock(return_value="Compressed chunk")
    return llm

@pytest.mark.asyncio
async def test_differential_retriever(mock_vector_store):
    def mock_embed(text):
        return np.array([1.0, 0.0]) # same as chunk c1

    diff = DifferentialRetriever("user1", mock_vector_store, embed_func=mock_embed)
    
    # Turn 1: Fresh retrieval
    chunks = await diff.retrieve("query1")
    assert diff.turn_count == 1
    assert len(diff.context_pool) == 2
    
    # Turn 2: Exact same query embedding -> DIFFERENTIAL mode
    chunks2 = await diff.retrieve("query2")
    assert diff.turn_count == 2
    # Since candidates are exactly the same, they should be skipped
    assert len(chunks2) == 0
    assert diff._stats["chunks_skipped"] == 2

@pytest.mark.asyncio
async def test_context_tetris_scoring(mock_llm):
    tetris = ContextTetris(mock_llm, None)
    
    # Test scoring logic
    query_emb = np.array([1.0, 0.0])
    chunk = {
        "id": "c1",
        "text": "This is a test chunk with facts.",
        "embedding": [1.0, 0.0] # perfect relevance
    }
    
    score = tetris.score_chunk(chunk, query_emb, [])
    assert score.relevance == 1.0 # Cosine sim should be 1.0
    assert score.uniqueness == 1.0 # No previous chunks
    # Without spacy, density might be 0, but final score should still be high due to relevance and uniqueness
    assert score.final_score > 0.5

@pytest.mark.asyncio
async def test_ingestion(mock_vector_store):
    def mock_embed(text):
        return np.array([0.5, 0.5])
        
    ingestor = DocumentIngestor(mock_vector_store, embed_func=mock_embed)
    
    chunks = ingestor._chunk_text("A" * 1500, chunk_size=1000, overlap=200)
    assert len(chunks) == 2
    
    res = await ingestor.ingest_text("user1", "A" * 1500, chunk_size=1000, overlap=200)
    assert res == 2
    mock_vector_store.upsert.assert_called_once()
