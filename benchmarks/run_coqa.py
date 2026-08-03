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
    print("Quira Academic Benchmarks (CoQA - Conversational RAG)")
    print("="*60)
    
    try:
        # Load CoQA dataset
        dataset = load_dataset("coqa", split="validation[:10]")
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return

    try:
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

    print(f"Loaded {len(dataset)} stories. Starting evaluation loop...\n")

    for idx, item in enumerate(dataset):
        story = item['story']
        questions = item['questions']
        
        # CoQA schema might store answers slightly differently
        # Usually item['answers']['input_text'] or similar. 
        # We will try to extract them safely.
        answers_list = item.get('answers', {}).get('input_text', [])
        
        # fallback if schema is just a list
        if not answers_list and isinstance(item.get('answers'), list):
            answers_list = item['answers']
            
        session_id = f"eval_user_coqa_{idx}"
        session = UserSession(user_id=session_id)
        
        if story:
            await pipeline.ingest_text(story, user_id=session_id)
            
        for q_idx, question in enumerate(questions):
            # Sometimes CoQA questions are dicts
            if isinstance(question, dict) and 'input_text' in question:
                question_text = question['input_text']
            else:
                question_text = str(question)
                
            ans_text = str(answers_list[q_idx]) if q_idx < len(answers_list) else ""
            answers = [ans_text]
            
            # 1. Speculative Phase
            await pipeline.handle_typing_event(session, question_text[:int(len(question_text)*0.8)])
            
            # 2. Submission Phase
            start_time = time.time()
            response = await pipeline.process_submission(session, question_text)
            latency_ms = (time.time() - start_time) * 1000
            
            # 3. Accuracy Evaluation (Exact Match)
            response_lower = response.lower()
            is_correct = any(ans.lower() in response_lower for ans in answers if ans)
            
            metrics["total_questions"] += 1
            if is_correct:
                metrics["exact_match_score"] += 1
            metrics["avg_latency_ms"] += latency_ms
            metrics["total_tokens_saved"] += pipeline.last_run_metrics.get("tokens_saved", 0)

            print(f"Story {idx+1}, Q{q_idx+1}: {question_text[:40]}... | Latency: {latency_ms:.1f}ms | Correct: {'Yes' if is_correct else 'No'}")
        
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
