"""
Quira Test Suite
"""
import pytest
from quira import quiraPipeline, UserSession


class TestUserSession:
    """Tests for UserSession dataclass."""

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


class TestImports:
    """Tests that all modules are importable."""

    def test_import_pipeline(self):
        from quira.core.pipeline import quiraPipeline
        assert quiraPipeline is not None

    def test_import_session(self):
        from quira.core.session import UserSession
        assert UserSession is not None

    def test_import_speculative(self):
        from quira.modules.speculative import SpeculativeRetriever
        assert SpeculativeRetriever is not None

    def test_import_tetris(self):
        from quira.modules.tetris import ContextTetris
        assert ContextTetris is not None

    def test_import_differential(self):
        from quira.modules.differential import DifferentialRetriever
        assert DifferentialRetriever is not None

    def test_import_ingestion(self):
        from quira.modules.ingestion import DocumentIngestor
        assert DocumentIngestor is not None


class TestDocumentIngestor:
    """Tests for the chunking logic (no external services needed)."""

    def test_chunk_text_basic(self):
        from quira.modules.ingestion import DocumentIngestor
        ingestor = DocumentIngestor(qdrant_client=None, embed_func=None)
        text = "A" * 2500
        chunks = ingestor._chunk_text(text, chunk_size=1000, overlap=200)
        assert len(chunks) == 3
        assert all(len(c) <= 1000 for c in chunks)

    def test_chunk_text_short(self):
        from quira.modules.ingestion import DocumentIngestor
        ingestor = DocumentIngestor(qdrant_client=None, embed_func=None)
        chunks = ingestor._chunk_text("Hello world", chunk_size=1000, overlap=200)
        assert len(chunks) == 1
        assert chunks[0] == "Hello world"

    def test_chunk_text_empty(self):
        from quira.modules.ingestion import DocumentIngestor
        ingestor = DocumentIngestor(qdrant_client=None, embed_func=None)
        chunks = ingestor._chunk_text("", chunk_size=1000, overlap=200)
        assert len(chunks) == 0 or chunks == [""]
