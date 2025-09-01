import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def embed_text(text: str):
    """
    Generate embeddings using Gemini.
    """
    model = "models/embedding-001"  # Gemini embedding model
    result = genai.embed_content(model=model, content=text)
    return result["embedding"]

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
