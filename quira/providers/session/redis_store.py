import json
import logging
from typing import Optional, Any
from quira.core.session import UserSession
from quira.providers.session.base import SessionStore

logger = logging.getLogger("quira.session.redis")

class RedisSessionStore(SessionStore):
    """Redis-backed session store for distributed horizontal scaling."""
    
    def __init__(self, client: Any = None, url: str = "redis://localhost:6379", prefix: str = "quira:session:"):
        self.prefix = prefix
        if client:
            self.client = client
        else:
            try:
                import redis.asyncio as redis
                self.client = redis.from_url(url)
            except ImportError:
                raise ImportError("Redis is not installed. Run `pip install redis`.")
                
    async def get_session(self, user_id: str) -> UserSession:
        try:
            data = await self.client.get(f"{self.prefix}{user_id}")
            if data:
                return UserSession.from_dict(json.loads(data))
        except Exception as e:
            logger.error(f"Failed to fetch session for {user_id}: {e}")
            
        # Return fresh session if not found or error
        return UserSession(user_id=user_id)
        
    async def save_session(self, session: UserSession) -> None:
        try:
            data = json.dumps(session.to_dict())
            await self.client.set(f"{self.prefix}{session.user_id}", data, ex=86400) # 24h TTL
        except Exception as e:
            logger.error(f"Failed to save session for {session.user_id}: {e}")
