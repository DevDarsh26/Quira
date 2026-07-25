import pytest
from quira.core.session import UserSession
from quira.providers.session.memory import MemorySessionStore

@pytest.mark.asyncio
async def test_memory_session_store():
    store = MemorySessionStore()
    
    # Get a fresh session
    session = await store.get_session("user123")
    assert session.user_id == "user123"
    assert session.context_pool == []
    
    # Modify session
    session.context_pool = [{"id": "doc1", "text": "hello"}]
    session.turn_count = 5
    
    # Save session
    await store.save_session(session)
    
    # Retrieve it again
    retrieved = await store.get_session("user123")
    assert retrieved.user_id == "user123"
    assert retrieved.turn_count == 5
    assert len(retrieved.context_pool) == 1
    assert retrieved.context_pool[0]["text"] == "hello"

    # Test unknown user
    unknown = await store.get_session("user999")
    assert unknown.user_id == "user999"
    assert unknown.context_pool == []
