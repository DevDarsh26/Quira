from abc import ABC, abstractmethod
from typing import Optional
from quira.core.session import UserSession

class SessionStore(ABC):
    """Abstract base class for UserSession persistence backends."""
    
    @abstractmethod
    async def get_session(self, user_id: str) -> UserSession:
        """Retrieve a session by user_id, or create a new one if it doesn't exist."""
        pass
        
    @abstractmethod
    async def save_session(self, session: UserSession) -> None:
        """Persist the session state to the backend."""
        pass
