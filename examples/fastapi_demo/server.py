import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uuid
import os

# Set dummy keys if missing so we can at least initialize the app (for demo purposes)
if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = "dummy_key_for_demo_if_missing"

from quira.core.pipeline import quiraPipeline
from quira.core.session import UserSession

app = FastAPI(title="Quira Speculative RAG Demo")

# Initialize Pipeline (using memory cache and qdrant vector store)
pipeline = quiraPipeline(
    vector_store="qdrant",
    cache="memory",
    llm="groq/llama-3.1-8b-instant"
)

# In-memory session store
sessions = {}

# Serve the HTML client
@app.get("/")
async def get():
    with open("client.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    # Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
        
    try:
        if file.filename.endswith(".pdf"):
            chunks = await pipeline.ingest_pdf(temp_path, user_id="demo_user")
        else:
            with open(temp_path, "r", encoding="utf-8") as f:
                text = f.read()
            chunks = await pipeline.ingest_text(text, user_id="demo_user")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return {"status": "success", "chunks_ingested": chunks}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    # Initialize User Session
    session = UserSession(user_id="demo_user", websocket=websocket)
    sessions[client_id] = session
    
    try:
        while True:
            # Receive keystroke
            data = await websocket.receive_text()
            # Feed into speculative retriever
            await pipeline.handle_typing_event(session, data)
            # In a real app, you might want to send back an ack or partial UI updates
            await websocket.send_json({"status": "speculative_search_triggered", "query": data})
            
    except WebSocketDisconnect:
        del sessions[client_id]

class QueryRequest(BaseModel):
    client_id: str
    query: str

@app.post("/query")
async def process_query(req: QueryRequest):
    if req.client_id not in sessions:
        return JSONResponse(status_code=400, content={"error": "Invalid client_id. Must connect via WS first."})
        
    session = sessions[req.client_id]
    
    # Run Context Tetris + LLM Generation
    answer = await pipeline.process_submission(session, req.query)
    
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
