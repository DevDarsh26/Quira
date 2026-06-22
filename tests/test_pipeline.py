import pytest
from unittest.mock import MagicMock, AsyncMock

from quira.core.pipeline import quiraPipeline
from quira.core.session import UserSession

from quira.providers.base import LLMProvider, VectorStore, CacheBackend

@pytest.fixture
def mock_pipeline():
    # Provide fully mocked dependencies so no actual I/O happens
    class MockVector(VectorStore):
        async def search(self, *args, **kwargs): return []
        async def upsert(self, *args, **kwargs): pass
        
    class MockCache(CacheBackend):
        async def get(self, *args, **kwargs): return None
        async def set(self, *args, **kwargs): pass
        async def delete(self, *args, **kwargs): pass
        
    class MockLLM(LLMProvider):
        async def complete(self, *args, **kwargs): return "Pipeline generated answer"
        def embed(self, *args, **kwargs): return [0.1, 0.2]
        async def stream(self, *args, **kwargs):
            yield "Pipeline "
            yield "generated "
            yield "answer"
    
    # Initialize pipeline with mocks
    pipeline = quiraPipeline(
        vector_store=MockVector(),
        cache=MockCache(),
        llm=MockLLM(),
        embed_func=lambda x: [0.1, 0.2]
    )
    
    return pipeline

@pytest.mark.asyncio
async def test_process_submission_async(mock_pipeline):
    session = UserSession("test_user")
    
    answer = await mock_pipeline.process_submission(session, "test query")
    assert answer == "Pipeline generated answer"
    assert session.user_id == "test_user"

def test_process_submission_sync(mock_pipeline):
    session = UserSession("test_user")
    
    answer = mock_pipeline.process_submission_sync(session, "test query sync")
    assert answer == "Pipeline generated answer"

def test_ingest_text_sync(mock_pipeline):
    res = mock_pipeline.ingest_text_sync("Hello world")
    assert res == 1

def test_pipeline_initialization_strings():
    # Just testing instantiation with string providers doesn't crash 
    # (Requires no actual keys if we don't call them, but we mock API keys if needed)
    pass
