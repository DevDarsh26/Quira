import asyncio
from typing import Any, List, Optional
from quira.providers.base import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self, client: Any = None, api_key: Optional[str] = None, default_model: str = "claude-3-5-sonnet-20240620", embed_func: Optional[Any] = None):
        """
        Anthropic Provider Adapter.
        """
        self.default_model = default_model
        
        if client:
            self.client = client
        else:
            try:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=api_key)
            except ImportError:
                raise ImportError("anthropic client not installed. Run `pip install quira[anthropic]`")
                
        if embed_func:
            self._embed_func = embed_func
        else:
            from fastembed import TextEmbedding
            model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
            self._embed_func = lambda text: list(model.embed([text]))[0]

    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "model": model or self.default_model,
            "max_tokens": 4096,
            "messages": messages
        }
        if system_prompt:
            kwargs["system"] = system_prompt
            
        if asyncio.iscoroutinefunction(self.client.messages.create):
            response = await self.client.messages.create(**kwargs)
        else:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.messages.create(**kwargs)
            )
            
        return response.content[0].text

    def embed(self, text: str) -> List[float]:
        emb = self._embed_func(text)
        if hasattr(emb, "tolist"):
            return emb.tolist()
        return list(emb)
