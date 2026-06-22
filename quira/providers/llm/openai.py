import asyncio
from typing import Any, List, Optional
from quira.providers.base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, client: Any = None, api_key: Optional[str] = None, default_model: str = "gpt-4o", default_embed_model: str = "text-embedding-3-small", embed_func: Optional[Any] = None):
        """
        OpenAI Provider Adapter.
        """
        self.default_model = default_model
        self.default_embed_model = default_embed_model
        
        if client:
            self.client = client
        else:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("openai client not installed. Run `pip install quira[openai]`")
                
        self._custom_embed_func = embed_func

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

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if asyncio.iscoroutinefunction(self.client.chat.completions.create):
            response = await self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                stream=True
            )
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            # Fallback for sync client
            import threading
            q = asyncio.Queue()
            loop = asyncio.get_event_loop()

            def producer():
                try:
                    response = self.client.chat.completions.create(
                        model=model or self.default_model,
                        messages=messages,
                        stream=True
                    )
                    for chunk in response:
                        if chunk.choices and chunk.choices[0].delta.content:
                            loop.call_soon_threadsafe(q.put_nowait, chunk.choices[0].delta.content)
                except Exception as e:
                    loop.call_soon_threadsafe(q.put_nowait, e)
                finally:
                    loop.call_soon_threadsafe(q.put_nowait, None)

            threading.Thread(target=producer, daemon=True).start()
            while True:
                item = await q.get()
                if item is None:
                    break
                if isinstance(item, Exception):
                    raise item
                yield item

    def embed(self, text: str) -> List[float]:
        if self._custom_embed_func:
            emb = self._custom_embed_func(text)
            if hasattr(emb, "tolist"):
                return emb.tolist()
            return list(emb)
            
        # Synchronous embedding fallback using the openai SDK directly
        from openai import OpenAI
        sync_client = OpenAI(api_key=self.client.api_key)
        response = sync_client.embeddings.create(
            input=text,
            model=self.default_embed_model
        )
        return response.data[0].embedding
