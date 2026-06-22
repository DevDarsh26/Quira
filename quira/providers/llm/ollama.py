import asyncio
from typing import Any, List, Optional
from quira.providers.base import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self, client: Any = None, host: str = "http://localhost:11434", default_model: str = "llama3", default_embed_model: str = "nomic-embed-text", embed_func: Optional[Any] = None):
        """
        Ollama Provider Adapter.
        """
        self.default_model = default_model
        self.default_embed_model = default_embed_model
        
        if client:
            self.client = client
        else:
            try:
                import ollama
                self.client = ollama.AsyncClient(host=host)
            except ImportError:
                raise ImportError("ollama client not installed. Run `pip install quira[ollama]`")
                
        self._custom_embed_func = embed_func
        self._sync_host = host

    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if asyncio.iscoroutinefunction(self.client.chat):
            response = await self.client.chat(
                model=model or self.default_model,
                messages=messages
            )
            return response["message"]["content"]
        else:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat(
                    model=model or self.default_model,
                    messages=messages
                )
            )
            return response["message"]["content"]

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if asyncio.iscoroutinefunction(self.client.chat):
            response = await self.client.chat(
                model=model or self.default_model,
                messages=messages,
                stream=True
            )
            async for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]
        else:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat(
                    model=model or self.default_model,
                    messages=messages,
                    stream=True
                )
            )
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]

    def embed(self, text: str) -> List[float]:
        if self._custom_embed_func:
            emb = self._custom_embed_func(text)
            if hasattr(emb, "tolist"):
                return emb.tolist()
            return list(emb)
            
        import ollama
        sync_client = ollama.Client(host=self._sync_host)
        response = sync_client.embeddings(model=self.default_embed_model, prompt=text)
        return response["embedding"]
