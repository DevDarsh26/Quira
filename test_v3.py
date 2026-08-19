import asyncio
import os

from quira.core.pipeline import quiraPipeline
from quira.core.session import UserSession

async def test_v3_features():
    print("Testing Edge Mode and Agentic Routing...")
    pipeline = quiraPipeline(
        edge_mode=True, 
        edge_store="sqlite-vec",
        enable_agentic_routing=True,
        enable_graph_rag=True
    )
    
    # Test Agentic Routing short-circuit
    session = UserSession(user_id="test_user")
    ans = await pipeline.process_submission(session, "Hello there!")
    print(f"Agentic response: {ans}")
    assert "agentic_routing_hit" in pipeline.last_run_metrics
    print("Agentic routing passed.")
    
    # Test GraphRAG extraction
    print("Testing GraphRAG Ingestion...")
    text_to_ingest = "Eiffel Tower is located in Paris. Paris is the capital of France."
    chunks = await pipeline.ingest_text(text_to_ingest, user_id="test_user")
    print(f"Ingested {chunks} chunks.")
    
    # Test retrieval
    print("Testing GraphRAG retrieval...")
    ans = await pipeline.process_submission(session, "Where is the Eiffel Tower?")
    print(f"RAG response: {ans}")

if __name__ == "__main__":
    asyncio.run(test_v3_features())
