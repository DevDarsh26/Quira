import re
from typing import Optional

# A simple set of regex patterns to identify purely conversational intents
CONVERSATIONAL_PATTERNS = [
    r"^(hi|hello|hey|greetings|good\s(morning|afternoon|evening|night))[\s\W]*$",
    r"^(how\sare\syou|what's\sup|how's\sit\sgoing)[\s\W]*$",
    r"^(thanks|thank\syou|appreciate\sit|awesome|great|cool)[\s\W]*$",
    r"^(bye|goodbye|see\sya|talk\sto\syou\slater)[\s\W]*$",
    r"^(who\sare\syou|what\sare\syou)[\s\W]*$"
]

def is_conversational_query(query: str) -> bool:
    """
    Zero-latency heuristic to determine if a query is purely conversational.
    Returns True if the query matches known conversational patterns.
    """
    clean_query = query.strip().lower()
    for pattern in CONVERSATIONAL_PATTERNS:
        if re.match(pattern, clean_query):
            return True
    return False

def get_canned_conversational_response(query: str) -> Optional[str]:
    """
    Returns a fast canned response for very common conversational queries.
    If none matches perfectly, returns None (allowing a fast LLM call to handle it).
    """
    clean_query = query.strip().lower()
    if re.match(r"^(hi|hello|hey|greetings)[\s\W]*$", clean_query):
        return "Hello! How can I help you today?"
    if re.match(r"^(thanks|thank\syou)[\s\W]*$", clean_query):
        return "You're welcome! Let me know if you need anything else."
    if re.match(r"^(bye|goodbye)[\s\W]*$", clean_query):
        return "Goodbye! Have a great day!"
    if re.match(r"^(who\sare\syou|what\sare\syou)[\s\W]*$", clean_query):
        return "I am Quira, your AI assistant powered by advanced Retrieval Augmented Generation."
    return None
