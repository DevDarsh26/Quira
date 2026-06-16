import asyncio
from typing import List, Any, Optional

try:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.documents import Document
    from pydantic import Field
except ImportError:
    raise ImportError("LangChain is not installed. Run `pip install quira[integrations]`")

from quira.core.pipeline import quiraPipeline
from quira.core.session import UserSession

class QuiraRetriever(BaseRetriever):
    """
    LangChain Retriever that wraps the quiraPipeline.
    Note: Quira's process_submission returns a generated string (RAG answer).
    If you want raw documents instead, you should use Quira as a full chain/engine,
    or modify this to return ContextTetris chunks.
    Here we wrap the output as a single Document for compatibility, or you can
    override it to return the context_pool.
    """
    
    pipeline: quiraPipeline = Field(description="The Quira pipeline instance")
    user_id: str = Field(default="langchain_user", description="The user ID for the session")
    session: UserSession = Field(default_factory=lambda: None)
    
    def __init__(self, pipeline: quiraPipeline, user_id: str = "langchain_user", **kwargs: Any):
        super().__init__(pipeline=pipeline, user_id=user_id, **kwargs)
        self.session = UserSession(user_id=self.user_id)

    def _get_relevant_documents(self, query: str, *, run_manager: Any = None) -> List[Document]:
        # We use the sync wrapper
        answer = self.pipeline.process_submission_sync(self.session, query)
        
        # In a real integration, you might want to extract the actual chunks from session.context_pool
        # and return them as LangChain Documents. For now, we return the generated answer as a doc,
        # plus the context pool as metadata.
        
        docs = []
        for chunk in self.session.context_pool:
            docs.append(Document(
                page_content=chunk.get("text", ""),
                metadata={
                    "quira_id": chunk.get("id"),
                    "hit_count": chunk.get("hit_count", 0),
                    "tetris_score": chunk.get("tetris_score", 0.0)
                }
            ))
            
        return docs

    async def _aget_relevant_documents(self, query: str, *, run_manager: Any = None) -> List[Document]:
        # Async version
        answer = await self.pipeline.process_submission(self.session, query)
        
        docs = []
        for chunk in self.session.context_pool:
            docs.append(Document(
                page_content=chunk.get("text", ""),
                metadata={
                    "quira_id": chunk.get("id"),
                    "hit_count": chunk.get("hit_count", 0),
                    "tetris_score": chunk.get("tetris_score", 0.0)
                }
            ))
            
        return docs
