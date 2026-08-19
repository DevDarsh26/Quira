import asyncio
import logging
from typing import Dict, Coroutine, Any, Callable

logger = logging.getLogger("quira.debouncer")

class AsyncDebouncer:
    """
    A robust asynchronous debouncer that safely cancels existing tasks 
    for a given key (e.g., user_id) before starting a new one.
    Prevents memory leaks and dangling background threads.
    """
    def __init__(self):
        self._tasks: Dict[str, asyncio.Task] = {}
        self._locks: Dict[str, asyncio.Lock] = {}

    def _get_lock(self, key: str) -> asyncio.Lock:
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def debounce(self, key: str, coro_func: Callable[[], Coroutine[Any, Any, None]], delay: float = 0.0) -> None:
        """
        Schedules a coroutine to run after `delay` seconds.
        If a task is already scheduled/running for `key`, it is immediately cancelled.
        """
        lock = self._get_lock(key)
        
        async with lock:
            if key in self._tasks:
                task = self._tasks[key]
                if not task.done():
                    logger.debug(f"Debouncer: Cancelling existing task for {key}")
                    task.cancel()
                    # Await cancellation to avoid "Task was destroyed but it is pending" errors
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                    except Exception as e:
                        logger.error(f"Debouncer: Error in cancelled task for {key}: {e}")
            
            # Start new task
            async def _wrapper():
                try:
                    if delay > 0:
                        await asyncio.sleep(delay)
                    await coro_func()
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    logger.error(f"Debouncer: Task execution failed for {key}: {e}")
                finally:
                    # Cleanup
                    if self._tasks.get(key) == asyncio.current_task():
                        del self._tasks[key]

            self._tasks[key] = asyncio.create_task(_wrapper())

    def cancel(self, key: str) -> None:
        """Manually cancel a pending task for a key."""
        if key in self._tasks:
            task = self._tasks[key]
            if not task.done():
                task.cancel()
