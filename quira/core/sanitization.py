import html
import logging

logger = logging.getLogger("quira.sanitization")

def sanitize_input(text: str) -> str:
    """
    Sanitizes user input for real-time text streaming.
    HTML-escapes XML-like tags (e.g., <context>) to prevent prompt injection 
    and context bleeding without destroying legitimate code snippets.
    """
    if not text:
        return ""
    
    # HTML escape '<', '>', '&', '"', and '''
    sanitized = html.escape(text)
    
    return sanitized
