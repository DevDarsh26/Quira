# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - Unreleased (Edge, GraphRAG & Provider Expansion)

### Added
- **Quira Edge (Zero-Server Mode)**: Added embedded databases `DuckDBStore` and `SQLiteVecStore`. Passing `edge_mode=True` allows local execution without external dependencies.
- **GraphRAG Capabilities**: Added `GraphStore` abstraction and automatic Entity-Relationship triplet extraction during ingestion. Performs multi-hop Knowledge Graph traversal in parallel with standard retrieval.
- **Agentic Routing**: Zero-latency heuristics that intercept conversational queries (e.g., "Hi") and instantly return canned responses, completely bypassing the vector database and LLM to save tokens and latency.
- **Provider Abstraction Layer Expansion**: Added native support for 5 new enterprise vector databases: **pgvector**, **MongoDB Atlas Vector Search**, **Elasticsearch**, **FAISS**, and **Neo4j**.
- **Unified Hybrid DB (Neo4j)**: `Neo4jStore` implements *both* `VectorStore` and `GraphStore`, allowing it to serve as a single unified backend for both semantic search and GraphRAG pipelines.

## [2.2.0] - 2026-08-03 (Performance & Academic Validation)

### Added
- **Academic Benchmarking Suite**: Added comprehensive RAG benchmarking scripts (`run_triviaqa.py`, `run_popqa.py`, `run_hotpotqa.py`, `run_coqa.py`) to validate Quira against General QA, Hallucination, Multi-hop Logic, and Conversational RAG datasets.
- **Zero-Cost Lexical Intent Debouncing**: Integrated `difflib.SequenceMatcher` to mathematically calculate structural intent changes during streaming input, skipping vector database queries if intent remains above 90% similarity.
- **Speculative Retrieval Toggle**: Added `enable_speculative_retrieval` as an explicit configuration parameter to the `quiraPipeline` constructor, allowing enterprises to hard-disable predictive fetching.


## [1.0.0] - 2026-07-25 (Enterprise Edition)

### Added
- **Session Persistence Backend**: Built `SessionStore` (with `MemorySessionStore` and `RedisSessionStore`) to enable horizontal scaling and persistent cross-session context beyond ephemeral WebSockets. `UserSession` is now referenced seamlessly by string IDs.
- **Enterprise Provenance & Citations**: Context Tetris now injects rigorous tracking tags (`[Source: X | ID: Y]`). System prompts force the LLM to provide zero-config hallucination-free citations.
- **Dynamic Tokenization Routing**: Removed hardcoded OpenAI `tiktoken` lock-in. Built a dynamic `count_tokens` math layer into the `LLMProvider` abstraction, preventing context window overflows across all open/closed source models.
- **Native Observability**: Shipped zero-config telemetry hooks (`quira/core/telemetry.py`). Automatically binds to **LangSmith** (`@traceable`) or **OpenTelemetry** if installed, degrading gracefully to standard Python logging without overhead.
- **Prompt Injection Sanitization**: Implemented an ultra-fast escaping layer tailored for streaming to neutralize malicious payloads without stripping legitimate code symbols.
- **Concurrency & Race Condition Safety**: Integrated `AsyncDebouncer` in the speculative retrieval module to actively cancel stale WebSocket prediction queries, preventing database spikes during rapid typing.

### Changed
- The main pipeline methods (`process_submission`, `handle_typing_event`) now natively accept string `session_id`s in addition to `UserSession` objects to natively support standard REST/stateless architectures.

## [0.2.2] - 2026-06-22

### Added
- **Streaming Output**: Added `process_submission_stream` and `process_submission_stream_sync` to yield real-time LLM text generation.
- **Multi-Format Ingestion**: Extended `DocumentIngestor` to natively parse `.html`, `.docx`, `.csv`, `.md`, and `.txt` via the `ingest_file` method.
- **Regular Expression Fallback for Context Tetris**: Replaced the hard dependency on `spacy` with a fallback regular expression heuristic to keep density scoring functional in lightweight setups.

### Changed
- **Provider Abstraction Layer (PAL)**: Deprecated and removed legacy constructor arguments (`qdrant_client`, `redis_client`, `groq_client`) from `quiraPipeline`. You can now initialize the pipeline using string identifiers (e.g. `vector_store="qdrant"`).
- **Documentation**: Substantially updated `README.md` and the Next.js website with an end-to-end tutorial, explicit debugging steps, and dependency explanations.

## [0.2.1] - 2026-06-15

### Added
- Initial implementation of the Provider Abstraction Layer (PAL) supporting Qdrant, Pinecone, Chroma, Weaviate, Redis, OpenAI, Anthropic, Groq, and Ollama.
- Sync wrappers for primary async pipeline methods.

## [0.1.0] - 2026-05-01

### Added
- Initial Release of Quira with Speculative Retrieval, Context Tetris, Differential Context, and PyMuPDF Ingestion.
