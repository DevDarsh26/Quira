import asyncio
from typing import Any, List, Optional
from quira.providers.base import LLMProvider

class GroqProvider(LLMProvider):
    def __init__(self, client: Any = None, api_key: Optional[str] = None, default_model: str = "llama-3.1-8b-instant", embed_func: Optional[Any] = None):
        """
        Groq Provider Adapter.
        """
        self.default_model = default_model
        
        if client:
            self.client = client
        else:
            try:
                from groq import AsyncGroq
                self.client = AsyncGroq(api_key=api_key)
            except ImportError:
                raise ImportError("groq client not installed. Run `pip install quira[groq]`")
                
        # Groq currently does not have a widely used native embedding API in the standard python SDK, 
        # so we fallback to fastembed unless an embed_func is provided.
        if embed_func:
            self._embed_func = embed_func
        else:
            from fastembed import TextEmbedding
            model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
            self._embed_func = lambda text: list(model.embed([text]))[0]

    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if asyncio.iscoroutinefunction(self.client.chat.completions.create):
            response = await self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages
            )
        else:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model or self.default_model,
                    messages=messages
                )
            )
            
        return response.choices[0].message.content

    def embed(self, text: str) -> List[float]:
        emb = self._embed_func(text)
        if hasattr(emb, "tolist"):
            return emb.tolist()
        return list(emb)
