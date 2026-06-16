import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from quira.providers.cache.memory import InMemoryCache
from quira.providers.llm.groq_provider import GroqProvider

@pytest.mark.asyncio
async def test_in_memory_cache():
    cache = InMemoryCache()
    await cache.set("key1", "val1", ttl_seconds=10)
    val = await cache.get("key1")
    assert val == "val1"
    
    await cache.delete("key1")
    val2 = await cache.get("key1")
    assert val2 is None

@pytest.mark.asyncio
async def test_groq_provider_mocked():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked answer"
    
    # We use asyncio.iscoroutinefunction in the adapter, so we need an AsyncMock
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    provider = GroqProvider(client=mock_client)
    
    answer = await provider.complete("Test prompt", system_prompt="Sys")
    assert answer == "Mocked answer"
    mock_client.chat.completions.create.assert_called_once()
    args, kwargs = mock_client.chat.completions.create.call_args
    assert kwargs["messages"][0]["role"] == "system"
    assert kwargs["messages"][1]["role"] == "user"

def test_groq_provider_embed():
    mock_embed_func = MagicMock(return_value=[0.1, 0.2, 0.3])
    provider = GroqProvider(client=MagicMock(), embed_func=mock_embed_func)
    emb = provider.embed("test text")
    assert emb == [0.1, 0.2, 0.3]
    mock_embed_func.assert_called_once_with("test text")
