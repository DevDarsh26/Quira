import os
import google.generativeai as genai
from typing import Optional, List
import asyncio

from quira.providers.base import LLMProvider

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, default_model: str = "models/gemini-1.5-pro"):
        api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY env var or pass explicitly.")
            
        genai.configure(api_key=api_key)
        self.default_model = default_model

    async def complete(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        model_name = model or self.default_model
        gemini_model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt if system_prompt else None
        )
        response = await gemini_model.generate_content_async(prompt)
        return response.text

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        model_name = model or self.default_model
        gemini_model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt if system_prompt else None
        )
        response = await gemini_model.generate_content_async(prompt, stream=True)
        async for chunk in response:
            yield chunk.text

    def embed(self, text: str) -> List[float]:
        # Google provides a separate embedding endpoint, usually "models/embedding-001"
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query",
        )
        return result['embedding']
