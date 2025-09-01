import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_answer(query: str, context: str = "") -> str:
    """
    Generate an answer using Gemini model with optional context.
    """
    prompt = f"""
    You are a helpful assistant. Use the provided context to answer the query.

    Context:
    {context}

    Query:
    {query}
    """

    response = model.generate_content(prompt)

    if response and response.candidates:
        return response.candidates[0].content.parts[0].text.strip()
    return "Sorry, I couldn't generate an answer."
