import asyncio
import time
import json
import logging
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
from datasets import load_dataset
from quira import quiraPipeline, UserSession

logger = logging.getLogger("evals")
logger.setLevel(logging.INFO)

async def run_evaluations():
    print("="*60)
    print("Quira Academic Benchmarks (TriviaQA / PopQA / CORAL)")
    print("="*60)
    print("Loading HuggingFace Datasets... (requires `pip install datasets`)\n")
    


    try:
        # We load a very small split for quick evaluation (e.g. first 50 questions)
        dataset = load_dataset("mandarjoshi/trivia_qa", "rc", split="validation[:50]")
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
        context_text = ""
        sr = item.get('search_results', {})
        if isinstance(sr, dict):
            snippets = sr.get('search_context', sr.get('SearchSnippet', []))
            if snippets:
                context_text += " ".join([str(s) for s in snippets])
        elif isinstance(sr, list):
            for d in sr:
                if isinstance(d, dict):
                    context_text += str(d.get('search_context', d.get('SearchSnippet', ''))) + " "
                    
        if not context_text:
            ep = item.get('entity_pages', {})
            if isinstance(ep, dict):
                descs = ep.get('wiki_context', ep.get('Description', []))
                if descs:
                    context_text += " ".join([str(d) for d in descs])
            elif isinstance(ep, list):
                for d in ep:
                    if isinstance(d, dict):
                        context_text += str(d.get('wiki_context', d.get('Description', ''))) + " "
        
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

        print(f"Q{idx+1}: {question[:50]}... | Latency: {latency_ms:.1f}ms | Correct: {'Yes' if is_correct else 'No'}")
        
    # Final Report
    if metrics["total_questions"] > 0:
        metrics["avg_latency_ms"] /= metrics["total_questions"]
        metrics["accuracy_pct"] = (metrics["exact_match_score"] / metrics["total_questions"]) * 100

    print("\n" + "="*60)
    print("FINAL EVALUATION REPORT")
    print("="*60)
    print(json.dumps(metrics, indent=4))
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_evaluations())
