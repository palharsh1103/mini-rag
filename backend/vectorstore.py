import os
from dotenv import load_dotenv
from pinecone import Pinecone
from embeddings import embed_text

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def upsert_chunks(chunks, metadata: dict):
    """
    Store text chunks in Pinecone with embeddings.
    """
    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        vectors.append((f"id-{i}", embedding, {**metadata, "text": chunk}))
    index.upsert(vectors=vectors)

def query_chunks(query: str, top_k: int = 3):
    """
    Search for relevant chunks from Pinecone.
    """
    query_embedding = embed_text(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]
