import asyncio
from typing import Any, AsyncGenerator, Optional, List
from quira.providers.base import LLMProvider

class LiteLLMProvider(LLMProvider):
    def __init__(self, default_model: str = "openai/gpt-4o", embed_func: Optional[Any] = None, client: Any = None):
        """
        Provider using the litellm library, supporting 100+ LLMs.
        `default_model` should match litellm's expected format (e.g. "openai/gpt-4o", "anthropic/claude-3-5-sonnet-20240620")
        """
        self.default_model = default_model
        if embed_func:
            self._embed_func = embed_func
        else:
            try:
                from fastembed import TextEmbedding # type: ignore
                model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
                self._embed_func = lambda text: list(model.embed([text]))[0]
            except ImportError:
                raise ImportError("FastEmbed is not installed. Run `pip install quira[local-embed]` or provide a custom embed_func.")

    def embed(self, text: str) -> List[float]:
        return self._embed_func(text)

        try:
            import litellm # type: ignore
            self.litellm = litellm
        except ImportError:
            raise ImportError("litellm is not installed. Run `pip install litellm`")

    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        loop = asyncio.get_event_loop()
        def _sync_call():
            response = self.litellm.completion(
                model=model or self.default_model,
                messages=messages
            )
            return response.choices[0].message.content or ""
            
        return await loop.run_in_executor(None, _sync_call)

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> AsyncGenerator[str, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # We can use litellm.acompletion for async streaming
        response = await self.litellm.acompletion(
            model=model or self.default_model,
            messages=messages,
            stream=True
        )

        async for chunk in response:
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                yield content
