from vectorstore import query_chunks
from llm import generate_answer

def retrieve_and_answer(query: str):
    """
    Retrieve relevant chunks and generate an answer.
    """
    chunks = query_chunks(query)
    context = "\n".join(chunks)
    return generate_answer(query, context)
