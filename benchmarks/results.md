# Quira Benchmark Results

**Date:** 2026-08-01 17:16:49
**LLM:** groq/llama-3.1-8b-instant
**Queries:** 7 single-turn, 6 multi-turn

## Single-Turn Latency

| Metric | Naive RAG | Quira Pipeline | Improvement |
|--------|-----------|----------------|-------------|
| Avg Latency | 0.616s | 0.980s | -59.2% faster |
| P95 Latency | 1.367s | 3.576s | -161.6% faster |

## Multi-Turn Performance

| Metric | Value |
|--------|-------|
| Avg Latency (multi-turn) | 3.376s |
| Avg Reuse Rate | 32.2% |

## Token Savings (Context Tetris)

| Metric | Value |
|--------|-------|
| Tokens Saved (last run) | 97 |
| Compression | 45.3% fewer tokens |
| Chunks Selected | 2 |
| Chunks Rejected | 0 |

## Speculative Retrieval

| Metric | Value |
|--------|-------|
| Cache Hit Rate | 0.0% |
| Semantic Cache Hits | 0 |
| Searches Completed | 7 |

*Results generated with real API calls. No mock data used.*
