import asyncio
import os
from dotenv import load_dotenv

from quira.core.pipeline import quiraPipeline, UserSession
from quira.modules.ingestion import DocumentIngestor
from quira.providers.vector.supabase_store import SupabaseStore

async def main():
    print("🤖 Welcome to the Quira Chatbot Tester!")
    
    # 1. Load environment variables (SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY)
    load_dotenv()
    
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_KEY"):
        print("⚠️ Warning: SUPABASE_URL or SUPABASE_SERVICE_KEY is missing from your environment variables.")
        print("Please set them up to connect to your Vector Database.")
        return

    print("\n⏳ Initializing Quira Pipeline (Supabase + LiteLLM)...")
    
    # 2. Initialize the pipeline
    pipeline = quiraPipeline(
        vector_store="supabase", # Uses the SupabaseStore we built!
        cache="memory",
        llm="litellm/openai/gpt-4o"
    )

    # 3. Optional: Ingest some dummy data
    user_id = "test_user_01"
    session = UserSession(user_id=user_id)
    
    print("📚 Ingesting sample knowledge base...")
    ingestor = DocumentIngestor(pipeline.vector_store, pipeline.embed_func)
    
    sample_text = """
    Quira is a next-generation Retrieval Augmented Generation framework built in Python. 
    It features Speculative Retrieval, which fetches context before the user finishes typing.
    It also features Context Tetris, a highly optimized multi-dimensional scoring algorithm.
    """
    await ingestor.ingest_text(user_id, sample_text)
    print("✅ Knowledge base ingested!\n")

    # 4. Start the CLI Chatbot Loop
    print("💬 Chatbot is ready! Type 'exit' or 'quit' to stop.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input(f"\nYou ({user_id}): ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            print(f"🤖 Quira (GPT-4o): ", end="", flush=True)
            
            # Using the streaming submission to get real-time tokens!
            async for chunk in pipeline.process_submission_stream(session, user_input):
                print(chunk, end="", flush=True)
            print() # newline after answer completes

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
