import pytest
from quira.core.session import UserSession

class TestUserSession:
    """Tests for UserSession state management."""

    def test_session_creation(self):
        session = UserSession(user_id="test_user")
        assert session.user_id == "test_user"
        assert session.context_pool == []
        assert session.conversation_history == []
        assert session.turn_count == 0
        assert session.current_draft_query == ""

    def test_session_with_custom_fields(self):
        session = UserSession(user_id="user_42", turn_count=5)
        assert session.user_id == "user_42"
        assert session.turn_count == 5

    def test_session_pool_update(self):
        session = UserSession(user_id="test_user")
        session.context_pool.append({"id": "1", "text": "chunk1"})
        assert len(session.context_pool) == 1
        assert session.context_pool[0]["id"] == "1"
