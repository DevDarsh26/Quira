import asyncio
import logging
from typing import Any, Dict, List

from quira.modules.speculative import SpeculativeRetriever
from quira.modules.differential import DifferentialRetriever
from quira.modules.tetris import ContextTetris
from quira.modules.ingestion import DocumentIngestor
from quira.core.session import UserSession

logger = logging.getLogger("quira.pipeline")

class quiraPipeline:
    """
    Unified pipeline that wraps all modules of quira.
    """
    def __init__(self, qdrant_client: Any, redis_client: Any, groq_client: Any, embed_func: Any, spacy_model: Any):
        # Module 0 (Ingestion)
        self.ingestor = DocumentIngestor(qdrant_client, embed_func)
        # Module 1
        self.speculative = SpeculativeRetriever("default_user", qdrant_client, redis_client, embed_func=embed_func)
        # Module 2
        self.tetris = ContextTetris(groq_client, spacy_model)
        # Module 3
        self.differential = DifferentialRetriever("default_user", qdrant_client, embed_func=embed_func)
        
        # Core clients
        self.qdrant = qdrant_client
        self.redis = redis_client
        self.groq = groq_client

    async def handle_typing_event(self, session: UserSession, keystroke_stream: str) -> None:
        """
        Module 1: Detects typing via WebSocket and speculatively searches after 400ms.
        """
        await self.speculative.on_keystroke(keystroke_stream)

    async def process_submission(self, session: UserSession, final_query: str) -> str:
        """
        Called when the user hits enter.
        Orchestrates Differential Retrieval and Context Tetris.
        """
        # Module 3: Differential Retrieval - get new chunks
        new_chunks = await self.differential.retrieve(final_query)
        
        # Module 2: Context Tetris - score, compress, and order
        emb = self.differential.embed_func(final_query)
        packed_context = await self.tetris.pack(session.context_pool + new_chunks, emb)
        
        # Generate final answer using self.groq and the packed_context
        # Placeholder for LLM invocation
        answer = "This is a speculatively retrieved, context-tetris compressed, differentially fetched answer."
        
        return answer
