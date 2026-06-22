# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
