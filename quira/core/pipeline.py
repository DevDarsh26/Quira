import asyncio
import logging
import nest_asyncio
from typing import Any, Dict, List, Optional, Union

from quira.modules.speculative import SpeculativeRetriever
from quira.modules.differential import DifferentialRetriever
from quira.modules.tetris import ContextTetris
from quira.modules.ingestion import DocumentIngestor
from quira.core.session import UserSession

from quira.providers.base import VectorStore, CacheBackend, LLMProvider
from quira.providers.vector import QdrantStore, PineconeStore, ChromaStore, WeaviateStore
from quira.providers.cache import RedisCache, InMemoryCache, DiskCache
from quira.providers.llm import GroqProvider, OpenAIProvider, AnthropicProvider, OllamaProvider
from quira.providers.fallback import FallbackVectorStore, FallbackLLMProvider

logger = logging.getLogger("quira.pipeline")

# Apply nest_asyncio to allow asyncio.run() within an already running loop
nest_asyncio.apply()

class quiraPipeline:
    """
    Unified pipeline that wraps all modules of quira.
    Now supports Provider Abstraction Layer.
    """
    def __init__(
        self, 
        vector_store: Union[str, VectorStore, Any] = "qdrant",
        cache: Union[str, CacheBackend, Any] = "memory",
        llm: Union[str, LLMProvider, Any] = "groq/llama-3.1-8b-instant",
        embed_func: Optional[Any] = None,
        spacy_model: Optional[Any] = None,
        # Legacy compat params (for backward compatibility)
        qdrant_client: Optional[Any] = None,
        redis_client: Optional[Any] = None,
        groq_client: Optional[Any] = None,
        # Fallbacks
        fallback_vector_store: Union[str, VectorStore, Any, None] = None,
        fallback_llm: Union[str, LLMProvider, Any, None] = None,
    ):
        # Resolve Vector Store
        if qdrant_client:
            self.vector_store = QdrantStore(client=qdrant_client)
        elif isinstance(vector_store, VectorStore):
            self.vector_store = vector_store
        elif isinstance(vector_store, str):
            v_type = vector_store.lower()
            if v_type == "qdrant":
                self.vector_store = QdrantStore()
            elif v_type == "pinecone":
                self.vector_store = PineconeStore()
            elif v_type == "chroma":
                self.vector_store = ChromaStore()
            elif v_type == "weaviate":
                self.vector_store = WeaviateStore()
            else:
                raise ValueError(f"Unknown vector_store string: {vector_store}")
        else:
            # Fallback for raw clients passed as positional/kwargs without the specific name
            self.vector_store = QdrantStore(client=vector_store)

        if fallback_vector_store:
            if isinstance(fallback_vector_store, VectorStore):
                fb_vs = fallback_vector_store
            elif isinstance(fallback_vector_store, str):
                v_type = fallback_vector_store.lower()
                if v_type == "qdrant":
                    fb_vs = QdrantStore()
                elif v_type == "pinecone":
                    fb_vs = PineconeStore()
                elif v_type == "chroma":
                    fb_vs = ChromaStore()
                elif v_type == "weaviate":
                    fb_vs = WeaviateStore()
                else:
                    raise ValueError(f"Unknown fallback_vector_store string: {fallback_vector_store}")
            else:
                fb_vs = QdrantStore(client=fallback_vector_store)
            self.vector_store = FallbackVectorStore(primary=self.vector_store, fallback=fb_vs)
        else:
            # Wrap with FallbackVectorStore anyway to get the retry logic
            self.vector_store = FallbackVectorStore(primary=self.vector_store)

        # Resolve Cache
        if redis_client:
            self.cache = RedisCache(client=redis_client)
        elif isinstance(cache, CacheBackend):
            self.cache = cache
        elif isinstance(cache, str):
            c_type = cache.lower()
            if c_type == "redis":
                self.cache = RedisCache()
            elif c_type == "memory":
                self.cache = InMemoryCache()
            elif c_type == "disk":
                self.cache = DiskCache()
            else:
                raise ValueError(f"Unknown cache string: {cache}")
        else:
            self.cache = RedisCache(client=cache)

        # Resolve LLM
        if groq_client:
            self.llm = GroqProvider(client=groq_client, embed_func=embed_func)
        elif isinstance(llm, LLMProvider):
            self.llm = llm
        elif isinstance(llm, str):
            parts = llm.split("/", 1)
            provider_name = parts[0].lower()
            model_name = parts[1] if len(parts) > 1 else None
            
            if provider_name == "groq":
                self.llm = GroqProvider(default_model=model_name or "llama-3.1-8b-instant", embed_func=embed_func)
            elif provider_name == "openai":
                self.llm = OpenAIProvider(default_model=model_name or "gpt-4o", embed_func=embed_func)
            elif provider_name == "anthropic":
                self.llm = AnthropicProvider(default_model=model_name or "claude-3-5-sonnet-20240620", embed_func=embed_func)
            elif provider_name == "ollama":
                self.llm = OllamaProvider(default_model=model_name or "llama3", embed_func=embed_func)
            else:
                raise ValueError(f"Unknown LLM provider string: {llm}")
        else:
            self.llm = GroqProvider(client=llm, embed_func=embed_func)

        if fallback_llm:
            if isinstance(fallback_llm, LLMProvider):
                fb_llm = fallback_llm
            elif isinstance(fallback_llm, str):
                parts = fallback_llm.split("/", 1)
                provider_name = parts[0].lower()
                model_name = parts[1] if len(parts) > 1 else None
                
                if provider_name == "groq":
                    fb_llm = GroqProvider(default_model=model_name or "llama-3.1-8b-instant", embed_func=embed_func)
                elif provider_name == "openai":
                    fb_llm = OpenAIProvider(default_model=model_name or "gpt-4o", embed_func=embed_func)
                elif provider_name == "anthropic":
                    fb_llm = AnthropicProvider(default_model=model_name or "claude-3-5-sonnet-20240620", embed_func=embed_func)
                elif provider_name == "ollama":
                    fb_llm = OllamaProvider(default_model=model_name or "llama3", embed_func=embed_func)
                else:
                    raise ValueError(f"Unknown fallback_llm string: {fallback_llm}")
            else:
                fb_llm = GroqProvider(client=fallback_llm, embed_func=embed_func)
            self.llm = FallbackLLMProvider(primary=self.llm, fallback=fb_llm)
        else:
            # Wrap with FallbackLLMProvider anyway to get the retry logic
            self.llm = FallbackLLMProvider(primary=self.llm)

        # Default embed func if none provided, taken from the LLM provider
        self.embed_func = embed_func if embed_func else self.llm.embed

        # Module 0 (Ingestion)
        self.ingestor = DocumentIngestor(self.vector_store, self.embed_func)
        # Module 1
        self.speculative = SpeculativeRetriever("default_user", self.vector_store, self.cache, embed_func=self.embed_func)
        # Module 2
        self.tetris = ContextTetris(self.llm, spacy_model)
        # Module 3
        self.differential = DifferentialRetriever("default_user", self.vector_store, embed_func=self.embed_func)

    # --- ASYNC METHODS ---
    async def handle_typing_event(self, session: UserSession, keystroke_stream: str) -> None:
        """Module 1: Detects typing via WebSocket and speculatively searches after debounce."""
        self.speculative.user_id = session.user_id # update user id dynamically
        await self.speculative.on_keystroke(keystroke_stream)

    async def process_submission(self, session: UserSession, final_query: str) -> str:
        """
        Orchestrates Differential Retrieval and Context Tetris.
        """
        self.differential.user_id = session.user_id
        
        # Check speculative cache first via on_submit
        speculative_results = await self.speculative.on_submit(final_query)
        
        # Module 3: Differential Retrieval - get new chunks
        # If speculative returned hits, we can inject them to differential pool 
        # (For simplicity here, we rely on DifferentialRetriever querying VectorStore directly, 
        # but in a highly optimized flow we'd pass speculative_results to it)
        new_chunks = await self.differential.retrieve(final_query)
        
        # Module 2: Context Tetris - score, compress, and order
        emb = self.embed_func(final_query)
        packed_context = await self.tetris.pack(session.context_pool + new_chunks, emb)
        
        # Update session pool
        session.context_pool = self.differential.get_context_pool()
        
        # Compile prompt
        context_str = "\n\n".join([c.get("text", "") for c in packed_context.chunks])
        sys_prompt = "You are a helpful AI assistant. Use the provided context to answer the user's query."
        prompt = f"Context:\n{context_str}\n\nQuery: {final_query}"
        
        # Generate final answer
        answer = await self.llm.complete(prompt=prompt, system_prompt=sys_prompt)
        return answer

    async def ingest_text(self, text: str, user_id: str = "default_user", chunk_size: int = 1000, overlap: int = 200) -> int:
        return await self.ingestor.ingest_text(user_id, text, chunk_size, overlap)

    async def ingest_pdf(self, file_path: str, user_id: str = "default_user", chunk_size: int = 1000, overlap: int = 200) -> int:
        return await self.ingestor.ingest_pdf(user_id, file_path, chunk_size, overlap)


    # --- SYNC WRAPPERS ---
    def handle_typing_event_sync(self, session: UserSession, keystroke_stream: str) -> None:
        asyncio.run(self.handle_typing_event(session, keystroke_stream))

    def process_submission_sync(self, session: UserSession, final_query: str) -> str:
        return asyncio.run(self.process_submission(session, final_query))

    def ingest_text_sync(self, text: str, user_id: str = "default_user", chunk_size: int = 1000, overlap: int = 200) -> int:
        return asyncio.run(self.ingest_text(text, user_id, chunk_size, overlap))

    def ingest_pdf_sync(self, file_path: str, user_id: str = "default_user", chunk_size: int = 1000, overlap: int = 200) -> int:
        return asyncio.run(self.ingest_pdf(file_path, user_id, chunk_size, overlap))
