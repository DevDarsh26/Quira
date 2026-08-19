"""
quira: Faster and smarter Retrieval Augmented Generation.

This library provides a unified quiraPipeline that wraps three core modules:
1. Speculative Retrieval (speculative.py): Detects typing via WebSocket, caches early searches.
2. Context Tetris (tetris.py): Scores, compresses, and optimally orders context chunks.
3. Differential Retrieval (differential.py): Minimizes redundant fetches across conversation turns.
"""

from .core.pipeline import quiraPipeline
from .core.session import UserSession

__all__ = ["quiraPipeline", "UserSession"]
