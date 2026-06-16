from typing import Any, Optional

try:
    from llama_index.core.query_engine import BaseQueryEngine
    from llama_index.core.schema import QueryBundle, NodeWithScore, TextNode
    from llama_index.core.base.response.schema import Response
except ImportError:
    raise ImportError("LlamaIndex is not installed. Run `pip install quira[integrations]`")

from quira.core.pipeline import quiraPipeline
from quira.core.session import UserSession

class QuiraQueryEngine(BaseQueryEngine):
    """
    LlamaIndex QueryEngine that wraps the quiraPipeline.
    Since Quira handles both retrieval and generation (Context Tetris -> LLM),
    it fits perfectly as a QueryEngine.
    """
    
    def __init__(self, pipeline: quiraPipeline, user_id: str = "llamaindex_user"):
        super().__init__(callback_manager=None)
        self.pipeline = pipeline
        self.user_id = user_id
        self.session = UserSession(user_id=self.user_id)

    def _query(self, query_bundle: QueryBundle) -> Response:
        query_str = query_bundle.query_str
        
        # Run sync wrapper
        answer = self.pipeline.process_submission_sync(self.session, query_str)
        
        # Construct source nodes from context pool
        source_nodes = []
        for chunk in self.session.context_pool:
            node = TextNode(
                text=chunk.get("text", ""),
                metadata={
                    "quira_id": chunk.get("id"),
                    "hit_count": chunk.get("hit_count", 0)
                }
            )
            score = chunk.get("tetris_score", 1.0)
            source_nodes.append(NodeWithScore(node=node, score=score))
            
        return Response(response=answer, source_nodes=source_nodes)

    async def _aquery(self, query_bundle: QueryBundle) -> Response:
        query_str = query_bundle.query_str
        
        # Run async method
        answer = await self.pipeline.process_submission(self.session, query_str)
        
        source_nodes = []
        for chunk in self.session.context_pool:
            node = TextNode(
                text=chunk.get("text", ""),
                metadata={
                    "quira_id": chunk.get("id"),
                    "hit_count": chunk.get("hit_count", 0)
                }
            )
            score = chunk.get("tetris_score", 1.0)
            source_nodes.append(NodeWithScore(node=node, score=score))
            
        return Response(response=answer, source_nodes=source_nodes)
