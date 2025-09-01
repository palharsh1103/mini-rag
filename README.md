# RAG System - AI Document QA

📚 **RAG (Retrieval-Augmented Generation) System**  
A full-stack AI application to **upload documents**, ask questions, and receive **AI-generated answers with citations**.

---

## Features

- Upload files: TXT, PDF, CSV, DOCX (up to 200MB per file)  
- Automatic document processing and chunking  
- AI-powered question answering with citation support  
- Integration with multiple AI models (OpenAI, Cohere, Google Generative AI)  
- Vector database support with Pinecone for semantic search  
- Streamlit frontend for easy interaction  

---

## Tech Stack

- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Database / Vector Store:** Pinecone  
- **AI Models:** OpenAI, Cohere, Google Generative AI  
- **Other Libraries:** python-dotenv, python-multipart, tiktoken  

---

## Installation


clone the repository
git clone https://github.com/palharsh1103/mini-rag.git
cd mini-rag

Create a virtual environment

python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux


Install dependencies

pip install -r backend/new_requirements.txt

Environment Setup

Create a .env file in backend/ and add:

OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
GOOGLE_API_KEY=your_google_generative_api_key
PINECONE_API_KEY=your_pinecone_api_key

Run the Application
Backend (FastAPI)
cd backend
uvicorn app:app --reload --port 8000


API available at: http://127.0.0.1:8000

Frontend (Streamlit)
cd frontend
streamlit run app.py


UI available at: http://localhost:8501

Docker Deployment

Build Docker image

docker build -t rag-app .


Run Docker container

docker run -p 8000:8000 -p 8501:8501 rag-app


Backend → http://localhost:8000

Frontend → http://localhost:8501

Docker Deployment

Build Docker image

docker build -t rag-app .


Run Docker container

docker run -p 8000:8000 -p 8501:8501 rag-app


Backend → http://localhost:8000

Frontend → http://localhost:8501
