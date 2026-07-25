from typing import Dict, Optional
from quira.core.session import UserSession
from quira.providers.session.base import SessionStore

class MemorySessionStore(SessionStore):
    """In-memory session store (development only)."""
    
    def __init__(self):
        self._store: Dict[str, dict] = {}
        
    async def get_session(self, user_id: str) -> UserSession:
        if user_id in self._store:
            return UserSession.from_dict(self._store[user_id])
        return UserSession(user_id=user_id)
        
    async def save_session(self, session: UserSession) -> None:
        self._store[session.user_id] = session.to_dict()
