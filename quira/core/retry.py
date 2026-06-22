import asyncio
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger("quira.retry")

def is_permanent_error(e: Exception) -> bool:
    error_str = str(e).lower()
    if any(code in error_str for code in ["401", "403", "404", "unauthorized", "forbidden", "not found"]):
        return True
    return False

def with_retry(max_attempts: int = 3, base_delay: float = 0.5):
    """
    Exponential backoff retry decorator for async functions.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts or is_permanent_error(e):
                        if is_permanent_error(e):
                            logger.error(f"Permanent error detected for {func.__name__}: {e}. Failing fast.")
                        raise e
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(f"Attempt {attempt} failed for {func.__name__} with error: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator

def with_retry_sync(max_attempts: int = 3, base_delay: float = 0.5):
    """
    Exponential backoff retry decorator for sync functions.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import time
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts or is_permanent_error(e):
                        if is_permanent_error(e):
                            logger.error(f"Permanent error detected for {func.__name__}: {e}. Failing fast.")
                        raise e
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(f"Attempt {attempt} failed for {func.__name__} with error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator
