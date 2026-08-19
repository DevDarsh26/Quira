import asyncio
import functools
import logging

logger = logging.getLogger("quira.telemetry")

try:
    from langsmith import traceable as langsmith_trace
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

try:
    from opentelemetry import trace as otel_trace
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

def trace_event(name: str):
    """
    Dynamic telemetry decorator.
    Wraps the function in LangSmith and/or OpenTelemetry spans if installed.
    Otherwise falls back to standard structured JSON logging.
    """
    def decorator(func):
        wrapped_func = func
        
        # Apply LangSmith trace
        if LANGSMITH_AVAILABLE:
            wrapped_func = langsmith_trace(name=name)(wrapped_func)
            
        @functools.wraps(wrapped_func)
        async def async_wrapper(*args, **kwargs):
            span = None
            if OTEL_AVAILABLE:
                tracer = otel_trace.get_tracer(__name__)
                span = tracer.start_span(name)
                
            logger.info(f"Trace Event [{name}] started")
            try:
                result = await wrapped_func(*args, **kwargs)
                return result
            except Exception as e:
                if span:
                    span.record_exception(e)
                    span.set_status(otel_trace.Status(otel_trace.StatusCode.ERROR))
                logger.error(f"Trace Event [{name}] failed: {e}")
                raise e
            finally:
                logger.info(f"Trace Event [{name}] completed")
                if span:
                    span.end()
                    
        @functools.wraps(wrapped_func)
        def sync_wrapper(*args, **kwargs):
            span = None
            if OTEL_AVAILABLE:
                tracer = otel_trace.get_tracer(__name__)
                span = tracer.start_span(name)
                
            logger.info(f"Trace Event [{name}] started")
            try:
                result = wrapped_func(*args, **kwargs)
                return result
            except Exception as e:
                if span:
                    span.record_exception(e)
                    span.set_status(otel_trace.Status(otel_trace.StatusCode.ERROR))
                logger.error(f"Trace Event [{name}] failed: {e}")
                raise e
            finally:
                logger.info(f"Trace Event [{name}] completed")
                if span:
                    span.end()

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
        
    return decorator
