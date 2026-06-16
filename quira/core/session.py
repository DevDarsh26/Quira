from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
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
