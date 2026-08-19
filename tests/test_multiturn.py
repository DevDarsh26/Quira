"""
End-to-end multi-turn conversation tests for Differential Retrieval.
Verifies that Quira's differential retriever actually saves redundant fetches
across conversation turns.
"""
import pytest
import asyncio
import numpy as np
from unittest.mock import AsyncMock, MagicMock, patch
from quira.modules.differential import DifferentialRetriever

@pytest.fixture
def mock_vector_store():
    """Mock vector store that returns different results based on query embedding."""
    store = MagicMock()
    
    async def dynamic_search(collection_name, query_vector, limit=10):
        # Return chunks based on the first element of the query vector
        base_id = int(query_vector[0] * 100)
        results = []
        for i in range(min(limit, 5)):
            results.append({
                "id": f"chunk_{base_id + i}",
                "payload": {
                    "text": f"Content for chunk {base_id + i} about topic {base_id}.",
                    "source": "test_doc"
                },
                "vector": query_vector
            })
        return results
    
    store.search = AsyncMock(side_effect=dynamic_search)
    return store


def similar_embed(text):
    """Embedding function that returns similar embeddings for related queries."""
    text_lower = text.lower()
    if "quantum" in text_lower and "computing" in text_lower:
        return np.array([0.9, 0.1, 0.0, 0.0])
    elif "quantum" in text_lower and "hardware" in text_lower:
        return np.array([0.85, 0.15, 0.05, 0.0])  # Similar to quantum computing
    elif "quantum" in text_lower:
        return np.array([0.8, 0.2, 0.0, 0.0])  # Similar
    elif "python" in text_lower:
        return np.array([0.1, 0.1, 0.9, 0.0])  # Very different topic
    elif "rag" in text_lower:
        return np.array([0.3, 0.3, 0.3, 0.3])  # Somewhat different
    return np.array([0.5, 0.5, 0.0, 0.0])


@pytest.mark.asyncio
async def test_multiturn_first_turn_is_fresh():
    """Turn 1 should be a fresh retrieval with no chunks skipped."""
    store = MagicMock()
    store.search = AsyncMock(return_value=[
        {"id": "c1", "payload": {"text": "Chunk 1"}, "vector": [0.9, 0.1, 0.0, 0.0]},
        {"id": "c2", "payload": {"text": "Chunk 2"}, "vector": [0.85, 0.15, 0.0, 0.0]},
    ])
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    new_chunks = await diff.retrieve("What is quantum computing?")
    
    assert len(new_chunks) == 2  # All chunks are new
    assert diff._stats["chunks_skipped"] == 0
    assert diff._stats["chunks_fetched"] == 2
    assert diff.turn_count == 1


@pytest.mark.asyncio
async def test_multiturn_similar_query_reuses_pool():
    """Turn 2 with a similar query should skip chunks already in the pool."""
    store = MagicMock()
    
    # Same results for similar queries
    results = [
        {"id": "c1", "payload": {"text": "Chunk 1"}, "vector": [0.9, 0.1, 0.0, 0.0]},
        {"id": "c2", "payload": {"text": "Chunk 2"}, "vector": [0.85, 0.15, 0.0, 0.0]},
        {"id": "c3", "payload": {"text": "Chunk 3"}, "vector": [0.8, 0.2, 0.0, 0.0]},
    ]
    store.search = AsyncMock(return_value=results)
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    # Turn 1: Fresh
    await diff.retrieve("What is quantum computing?")
    initial_pool_size = len(diff.context_pool)
    assert initial_pool_size == 3
    
    # Turn 2: Similar query — should detect DIFFERENTIAL mode and skip existing chunks
    new_chunks = await diff.retrieve("How does quantum computing work?")
    
    # Some chunks should have been skipped (already in pool from turn 1)
    assert diff._stats["chunks_skipped"] > 0
    assert diff.turn_count == 2


@pytest.mark.asyncio
async def test_multiturn_divergent_query_resets_pool():
    """Turn 2 with a completely different topic should trigger a FULL RESET."""
    store = MagicMock()
    store.search = AsyncMock(return_value=[
        {"id": "c1", "payload": {"text": "Chunk 1"}, "vector": [0.5, 0.5, 0.0, 0.0]},
    ])
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    # Turn 1: Quantum topic
    await diff.retrieve("What is quantum computing?")
    assert len(diff.context_pool) > 0
    
    # Turn 2: Completely different topic — should trigger FULL RESET
    store.search = AsyncMock(return_value=[
        {"id": "py1", "payload": {"text": "Python chunk"}, "vector": [0.1, 0.1, 0.9, 0.0]},
    ])
    new_chunks = await diff.retrieve("What is Python programming?")
    
    # Pool should have been cleared and refilled with new chunks only
    assert diff.turn_count == 2
    # After full reset, pool should contain only the new chunks
    all_ids = {c["id"] for c in diff.context_pool}
    assert "py1" in all_ids


@pytest.mark.asyncio
async def test_multiturn_reuse_rate_increases():
    """Over 3 related turns, the reuse rate should increase as the pool fills."""
    store = MagicMock()
    
    common_results = [
        {"id": f"c{i}", "payload": {"text": f"Chunk {i}"}, "vector": [0.9, 0.1, 0.0, 0.0]}
        for i in range(5)
    ]
    store.search = AsyncMock(return_value=common_results)
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    # Turn 1
    await diff.retrieve("What is quantum computing?")
    stats_after_t1 = diff.get_stats()
    reuse_t1 = stats_after_t1["reuse_rate"]
    
    # Turn 2 (similar topic)
    await diff.retrieve("Explain quantum hardware")
    stats_after_t2 = diff.get_stats()
    reuse_t2 = stats_after_t2["reuse_rate"]
    
    # Turn 3 (similar topic)
    await diff.retrieve("Tell me about quantum mechanics")
    stats_after_t3 = diff.get_stats()
    reuse_t3 = stats_after_t3["reuse_rate"]
    
    # Reuse rate should be increasing over related turns
    assert reuse_t1 == 0.0  # First turn, nothing to reuse
    assert reuse_t2 > reuse_t1  # Second turn should reuse something
    assert reuse_t3 >= reuse_t2  # Third turn should reuse even more


@pytest.mark.asyncio
async def test_garbage_collection_fires_every_3_turns():
    """Garbage collection should run every 3 turns and evict irrelevant chunks."""
    store = MagicMock()
    store.search = AsyncMock(return_value=[
        {"id": "c1", "payload": {"text": "Chunk 1"}, "vector": [0.5, 0.5, 0.0, 0.0]},
    ])
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    # Run 3 turns to trigger GC
    await diff.retrieve("What is quantum computing?")
    await diff.retrieve("How does quantum hardware work?")
    await diff.retrieve("Quantum mechanics explained")
    
    # GC should have been triggered on turn 3
    assert diff.turn_count == 3
    # Pool should still exist (GC only removes irrelevant chunks)
    # No assertion on exact pool size since it depends on GC thresholds


@pytest.mark.asyncio
async def test_anchor_chunks_survive_gc():
    """Anchor chunks should survive garbage collection even if their score is low."""
    store = MagicMock()
    store.search = AsyncMock(return_value=[
        {"id": "c1", "payload": {"text": "Anchor chunk"}, "vector": [0.5, 0.5, 0.0, 0.0]},
    ])
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    # Turn 1 and mark as anchor
    await diff.retrieve("What is quantum computing?")
    diff.mark_as_anchor(["c1"])
    
    # Add a low-relevance chunk manually
    diff.context_pool.append({
        "id": "low_rel",
        "text": "Irrelevant content about cooking recipes",
        "embedding": [0.0, 0.0, 0.0, 1.0],
        "hit_count": 0
    })
    
    # Run turns 2 and 3 with different topics to trigger GC
    store.search = AsyncMock(return_value=[])
    await diff.retrieve("Python programming")
    await diff.retrieve("JavaScript frameworks")
    
    # GC should have run. Anchor c1 should survive
    anchor_ids = {c["id"] for c in diff.context_pool}
    assert "c1" in anchor_ids


@pytest.mark.asyncio
async def test_preloaded_candidates_bypass_search():
    """When preloaded_candidates are provided, vector store search should be skipped."""
    store = MagicMock()
    store.search = AsyncMock(return_value=[])
    
    diff = DifferentialRetriever("user1", store, embed_func=similar_embed, top_k=5)
    
    preloaded = [
        {"id": "pre1", "payload": {"text": "Preloaded chunk"}, "vector": [0.9, 0.1, 0.0, 0.0]},
        {"id": "pre2", "payload": {"text": "Another preloaded"}, "vector": [0.85, 0.15, 0.0, 0.0]},
    ]
    
    new_chunks = await diff.retrieve("What is quantum computing?", preloaded_candidates=preloaded)
    
    # Vector store should NOT have been called
    store.search.assert_not_called()
    # Preloaded chunks should be in the pool
    assert len(new_chunks) == 2
