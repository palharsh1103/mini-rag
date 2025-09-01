import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from embeddings import chunk_text
from vectorstore import upsert_chunks
from retriever import retrieve_and_answer
from dotenv import load_dotenv
import os
import io
import pandas as pd
import docx
import PyPDF2

# Load environment variables
load_dotenv()
print("Environment loaded. Keys detected.")  # Avoid printing real keys

app = FastAPI()

# --- Upload Endpoint ---
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    raw = await file.read()

    try:
        if filename.endswith(".txt"):
            text = raw.decode("utf-8")

        elif filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)

        elif filename.endswith(".docx"):
            doc = docx.Document(io.BytesIO(raw))
            text = "\n".join(p.text for p in doc.paragraphs)

        elif filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(raw))
            text = df.to_string()

        else:
            return JSONResponse({"error": "Unsupported file type"}, status_code=400)

        chunks = chunk_text(text)
        upsert_chunks(chunks, {"source": file.filename})
        return {"status": "uploaded", "chunks": len(chunks)}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


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
