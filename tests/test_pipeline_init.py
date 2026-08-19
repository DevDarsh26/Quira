import pytest
from quira import quiraPipeline, UserSession
from quira.providers.llm.openai import OpenAIProvider
from quira.providers.vector.qdrant import QdrantStore

def test_pipeline_init_pal(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    pipeline = quiraPipeline(
        vector_store="qdrant",
        cache="memory",
        llm="openai/gpt-4o"
    )
    assert isinstance(pipeline.llm.primary, OpenAIProvider)
    assert isinstance(pipeline.vector_store.primary, QdrantStore)
    
def test_user_session():
    session = UserSession("user_123")
    assert session.user_id == "user_123"
    assert session.context_pool == []
