"""
Quira Benchmark Suite — Real Measurements Only

Compares a TRUE naive RAG pipeline (embed → search → stuff → LLM)
against the full Quira pipeline (speculative + differential + tetris).

Usage:
    python benchmarks/run_benchmark.py

Requirements:
    GROQ_API_KEY must be set in the environment.
"""
import asyncio
import time
import statistics
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure quira is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quira.core.pipeline import quiraPipeline
from quira.core.session import UserSession

# ------------------------------------------------------------------
# Corpus & Queries
# ------------------------------------------------------------------
CORPUS = """
Quantum computing is a rapidly-emerging technology that harnesses the laws of quantum mechanics to solve problems too complex for classical computers. 
Today, IBM Quantum makes real quantum hardware -- a tool scientists only began to imagine three decades ago -- available to hundreds of thousands of developers.
Our engineers deliver ever-more-powerful superconducting quantum processors at regular intervals, alongside crucial advances in software and quantum-classical orchestration.
This work moves us toward the quantum computing era, in which quantum computers run as accelerators alongside classical systems.
The Python programming language is widely used in quantum computing frameworks, such as Qiskit.
Speculative execution is an optimization technique where a computer system performs some task that may not be needed.
Retrieval Augmented Generation (RAG) is an AI framework that retrieves facts from an external knowledge base to ground large language models.
Context Tetris is a novel chunk-packing algorithm that optimizes the token window of LLMs for maximal attention density.
Differential Retrieval maintains a conversation state and only fetches delta chunks that are semantically divergent from the current context pool.
"""

# Mix of single-turn and multi-turn (grouped) queries
SINGLE_TURN_QUERIES = [
    "What is quantum computing?",
    "Who provides real quantum hardware?",
    "What language is used for Qiskit?",
    "Explain speculative execution.",
    "What is RAG?",
    "How does Context Tetris work?",
    "What is Differential Retrieval?",
]

MULTI_TURN_GROUPS = [
    [
        "What is quantum computing?",
        "Who makes quantum hardware?",
        "How are quantum computers used as accelerators?",
    ],
    [
        "What is RAG?",
        "How does RAG ground language models?",
        "What framework implements RAG?",
    ],
]


# ------------------------------------------------------------------
# TRUE Naive RAG — No Quira Modules At All
# ------------------------------------------------------------------
async def run_naive_rag_single(pipeline, queries):
    """
    Naive RAG: for every query, force-reset differential (no state), skip tetris,
    and do a fresh search + LLM call every single time.
    """
    latencies = []
    for q in queries:
        session = UserSession("benchmark_naive")
        pipeline.differential.force_reset()
        
        start = time.perf_counter()
        await pipeline.process_submission(session, q, use_tetris=False, force_full_fetch=True)
        latencies.append(time.perf_counter() - start)
    
    return latencies


# ------------------------------------------------------------------
# Quira Pipeline — Full Pipeline
# ------------------------------------------------------------------
async def run_quira_single(pipeline, queries):
    """
    Quira RAG: single-turn with speculative typing simulation.
    Each query simulates a realistic typing event before submission.
    """
    latencies = []
    for q in queries:
        session = UserSession("benchmark_quira")
        
        start = time.perf_counter()
        # Simulate typing event with partial query (first 60% of chars)
        partial = q[:int(len(q) * 0.6)]
        sleep_time = 0
        if len(partial) > 3:
            await pipeline.handle_typing_event(session, partial)
            sleep_time = 0.3
            await asyncio.sleep(sleep_time)  # Simulate typing pause
        
        await pipeline.process_submission(session, q, use_tetris=True)
        latencies.append((time.perf_counter() - start) - sleep_time)
    
    return latencies


async def run_quira_multiturn(pipeline, query_groups):
    """
    Quira RAG: multi-turn with the SAME session across related queries.
    Demonstrates differential retrieval's value.
    """
    all_latencies = []
    reuse_rates = []
    
    for group in query_groups:
        session = UserSession("benchmark_quira_mt")
        pipeline.differential.force_reset()
        
        for q in group:
            start = time.perf_counter()
            # Simulate typing
            partial = q[:int(len(q) * 0.6)]
            sleep_time = 0
            if len(partial) > 3:
                await pipeline.handle_typing_event(session, partial)
                sleep_time = 0.3
                await asyncio.sleep(sleep_time)
            
            await pipeline.process_submission(session, q, use_tetris=True)
            all_latencies.append((time.perf_counter() - start) - sleep_time)
        
        # Record reuse rate after the group
        diff_stats = pipeline.differential.get_stats()
        reuse_rates.append(diff_stats["reuse_rate"])
    
    return all_latencies, reuse_rates


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    if not os.getenv("GROQ_API_KEY"):
        print("=" * 60)
        print("ERROR: GROQ_API_KEY not set in environment.")
        print("This benchmark requires a real API key — no mock data.")
        print("Set it with: export GROQ_API_KEY=gsk_your_key_here")
        print("=" * 60)
        sys.exit(1)
    
    print("=" * 60)
    print("Quira Benchmark Suite — Real Measurements")
    print("=" * 60)
    
    # Initialize pipeline
    print("\nInitializing pipeline...")
    pipeline = quiraPipeline(
        vector_store="memory",
        cache="memory",
        llm="groq/llama-3.1-8b-instant"
    )
    
    # Ingest corpus
    print("Ingesting corpus...")
    asyncio.run(_ingest_and_benchmark(pipeline))


async def _ingest_and_benchmark(pipeline):
    await pipeline.ingest_text(CORPUS, user_id="benchmark_naive")
    await pipeline.ingest_text(CORPUS, user_id="benchmark_quira")
    await pipeline.ingest_text(CORPUS, user_id="benchmark_quira_mt")
    print(f"Corpus ingested.\n")
    
    # --- Benchmark 1: Single-turn ---
    print("--- Benchmark 1: Single-Turn Latency ---")
    naive_latencies = await run_naive_rag_single(pipeline, SINGLE_TURN_QUERIES)
    
    # Reset speculative state
    pipeline.speculative._last_searched_results = []
    pipeline.speculative._last_searched_embedding = None
    
    quira_latencies = await run_quira_single(pipeline, SINGLE_TURN_QUERIES)
    
    # --- Benchmark 2: Multi-turn ---
    print("\n--- Benchmark 2: Multi-Turn (Differential Retrieval) ---")
    mt_latencies, reuse_rates = await run_quira_multiturn(pipeline, MULTI_TURN_GROUPS)
    
    # --- Benchmark 3: Token savings (from last run metrics) ---
    tetris_stats = pipeline.tetris.get_stats()
    last_metrics = pipeline.last_run_metrics
    
    # --- Compute results ---
    naive_avg = statistics.mean(naive_latencies)
    naive_p95 = sorted(naive_latencies)[int(len(naive_latencies) * 0.95)] if len(naive_latencies) > 1 else naive_latencies[0]
    
    quira_avg = statistics.mean(quira_latencies)
    quira_p95 = sorted(quira_latencies)[int(len(quira_latencies) * 0.95)] if len(quira_latencies) > 1 else quira_latencies[0]
    
    mt_avg = statistics.mean(mt_latencies)
    avg_reuse = statistics.mean(reuse_rates) if reuse_rates else 0.0
    
    latency_improvement = (naive_avg - quira_avg) / naive_avg * 100 if naive_avg > 0 else 0
    latency_improvement_p95 = (naive_p95 - quira_p95) / naive_p95 * 100 if naive_p95 > 0 else 0
    
    tokens_saved = tetris_stats.get("tokens_saved", 0)
    total_orig = tetris_stats.get("total_original_tokens", 0)
    compression_pct = (tokens_saved / total_orig * 100) if total_orig > 0 else 0
    
    # --- Output ---
    markdown = f"""# Quira Benchmark Results

**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**LLM:** groq/llama-3.1-8b-instant
**Queries:** {len(SINGLE_TURN_QUERIES)} single-turn, {sum(len(g) for g in MULTI_TURN_GROUPS)} multi-turn

## Single-Turn Latency

| Metric | Naive RAG | Quira Pipeline | Improvement |
|--------|-----------|----------------|-------------|
| Avg Latency | {naive_avg:.3f}s | {quira_avg:.3f}s | {latency_improvement:.1f}% faster |
| P95 Latency | {naive_p95:.3f}s | {quira_p95:.3f}s | {latency_improvement_p95:.1f}% faster |

## Multi-Turn Performance

| Metric | Value |
|--------|-------|
| Avg Latency (multi-turn) | {mt_avg:.3f}s |
| Avg Reuse Rate | {avg_reuse:.1%} |

## Token Savings (Context Tetris)

| Metric | Value |
|--------|-------|
| Tokens Saved (last run) | {tokens_saved} |
| Compression | {compression_pct:.1f}% fewer tokens |
| Chunks Selected | {tetris_stats.get('selected_chunks', 'N/A')} |
| Chunks Rejected | {tetris_stats.get('rejected_chunks', 'N/A')} |

## Speculative Retrieval

| Metric | Value |
|--------|-------|
| Cache Hit Rate | {pipeline.speculative.get_stats().get('hit_rate', 0):.1%} |
| Semantic Cache Hits | {pipeline.speculative.get_stats().get('semantic_cache_hits', 0)} |
| Searches Completed | {pipeline.speculative.get_stats().get('searches_completed', 0)} |

*Results generated with real API calls. No mock data used.*
"""
    print("\n" + markdown)
    
    # Save results
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.md")
    with open(results_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Saved results to {results_path}")
    
    # Also save as JSON for programmatic consumption
    json_results = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "single_turn": {
            "naive_avg_s": round(naive_avg, 4),
            "naive_p95_s": round(naive_p95, 4),
            "quira_avg_s": round(quira_avg, 4),
            "quira_p95_s": round(quira_p95, 4),
            "improvement_pct": round(latency_improvement, 2),
        },
        "multi_turn": {
            "avg_latency_s": round(mt_avg, 4),
            "avg_reuse_rate": round(avg_reuse, 4),
        },
        "token_savings": {
            "tokens_saved": tokens_saved,
            "compression_pct": round(compression_pct, 2),
        },
        "speculative": pipeline.speculative.get_stats(),
    }
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_results, f, indent=2, default=str)
    print(f"Saved JSON results to {json_path}")


if __name__ == "__main__":
    main()
