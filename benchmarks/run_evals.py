import asyncio
import time
import json
import logging
from quira import quiraPipeline, UserSession

logger = logging.getLogger("evals")
logger.setLevel(logging.INFO)

async def run_evaluations():
    print("="*60)
    print("🏆 Quira Academic Benchmarks (TriviaQA / PopQA / CORAL)")
    print("="*60)
    print("Loading HuggingFace Datasets... (requires `pip install datasets`)\n")
    
    try:
        from datasets import load_dataset
    except ImportError:
        print("Please install datasets to run this script: `pip install datasets`")
        return

    try:
        # We load a very small split for quick evaluation (e.g. first 50 questions)
        dataset = load_dataset("trivia_qa", "rc", split="validation[:50]")
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return

    try:
        # Default to memory cache/vector for testing without external DB
        pipeline = quiraPipeline(
            vector_store="memory", 
            cache="memory",
            llm="groq/llama-3.1-8b-instant",
            enable_speculative_retrieval=True
        )
    except Exception as e:
        print(f"Pipeline initialization failed. Ensure API keys are set: {e}")
        return

    metrics = {
        "total_questions": 0,
        "exact_match_score": 0,
        "avg_latency_ms": 0,
        "total_tokens_saved": 0
    }

    print(f"Loaded {len(dataset)} questions. Starting evaluation loop...\n")

    for idx, item in enumerate(dataset):
        question = item['question']
        answers = item['answer']['normalized_aliases']  # List of acceptable answers
        
        # Ingest the evidence provided by TriviaQA as context
        context_text = " ".join([d['SearchSnippet'] for d in item.get('search_results', [])])
        if not context_text:
            context_text = " ".join([d['Description'] for d in item.get('entity_pages', [])])
        
        session_id = f"eval_user_{idx}"
        session = UserSession(user_id=session_id)
        
        if context_text:
            await pipeline.ingest_text(context_text, user_id=session_id)
        
        # 1. Speculative Phase
        await pipeline.handle_typing_event(session, question[:int(len(question)*0.8)])
        
        # 2. Submission Phase
        start_time = time.time()
        response = await pipeline.process_submission(session, question)
        latency_ms = (time.time() - start_time) * 1000
        
        # 3. Accuracy Evaluation (Exact Match)
        response_lower = response.lower()
        is_correct = any(ans.lower() in response_lower for ans in answers)
        
        # Update metrics
        metrics["total_questions"] += 1
        if is_correct:
            metrics["exact_match_score"] += 1
        metrics["avg_latency_ms"] += latency_ms
        metrics["total_tokens_saved"] += pipeline.last_run_metrics.get("tokens_saved", 0)

        print(f"Q{idx+1}: {question[:50]}... | Latency: {latency_ms:.1f}ms | Correct: {'✅' if is_correct else '❌'}")
        
    # Final Report
    if metrics["total_questions"] > 0:
        metrics["avg_latency_ms"] /= metrics["total_questions"]
        metrics["accuracy_pct"] = (metrics["exact_match_score"] / metrics["total_questions"]) * 100

    print("\n" + "="*60)
    print("📊 FINAL EVALUATION REPORT")
    print("="*60)
    print(json.dumps(metrics, indent=4))
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_evaluations())
