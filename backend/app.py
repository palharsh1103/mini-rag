import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Request
from pydantic import BaseModel
from embeddings import chunk_text
from vectorstore import upsert_chunks
from retriever import retrieve_and_answer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
print("Gemini API Key:", os.getenv("GEMINI_API_KEY"))
print("Pinecone API Key:", os.getenv("PINECONE_API_KEY"))

app = FastAPI()

# --- Upload Endpoint ---
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    chunks = chunk_text(text)
    upsert_chunks(chunks, {"source": file.filename})
    return {"status": "uploaded", "chunks": len(chunks)}

# --- Query Request Model ---
class QueryRequest(BaseModel):
    query: str

# --- Query Endpoint ---
@app.post("/query/")
async def query_endpoint(
    request: Request,
    query_form: str = Form(None)
):
    # Try JSON first
    try:
        data = await request.json()
        query = data.get("query")
    except Exception:
        query = None

    # If not JSON, try form
    if not query and query_form:
        query = query_form

    if not query:
        return {"error": "No query provided"}

    # Run retriever
    answer = retrieve_and_answer(query)
    return {"answer": answer}

# --- Run server ---
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
