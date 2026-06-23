from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import WebSocket

@dataclass
class UserSession:
    """
    Holds per-user in-memory state. 
    Lives in FastAPI WebSocket memory and dies when the user disconnects.
    Users NEVER see each other's documents or results.
    """
    user_id: str
    websocket: Optional[WebSocket] = None
    
    # Differential Retrieval state
    context_pool: List[Dict[str, Any]] = field(default_factory=list)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    turn_count: int = 0
    
    # Speculative Retrieval state
    current_draft_query: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the session state (omitting websocket)."""
        return {
            "user_id": self.user_id,
            "context_pool": self.context_pool,
            "conversation_history": self.conversation_history,
            "turn_count": self.turn_count,
            "current_draft_query": self.current_draft_query
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UserSession:
        """Deserializes session state."""
        session = cls(user_id=data["user_id"])
        session.context_pool = data.get("context_pool", [])
        session.conversation_history = data.get("conversation_history", [])
        session.turn_count = data.get("turn_count", 0)
        session.current_draft_query = data.get("current_draft_query", "")
        return session
