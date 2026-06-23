📚 AI Knowledge Assistant (RAG-based LLM Application)

An AI-powered document question-answering system built with Python, Streamlit, ChromaDB, Sentence Transformers, and Groq LLM.

Upload any PDF and ask natural language questions about its contents. The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the document and generate accurate answers.

⸻

🚀 Features

* 📄 Upload PDF documents
* 🔍 Extract text from PDFs
* ✂️ Smart text chunking
* 🧠 Generate semantic embeddings
* 🗂️ Store embeddings in ChromaDB
* 🔎 Semantic search using vector similarity
* 🤖 AI-powered answers using Groq LLM
* 💬 Chat history
* 📚 View source chunks used for answers
* ⚡ Fast and responsive Streamlit interface

⸻

🛠️ Tech Stack

* Language: Python 3.12
* Frontend: Streamlit
* LLM: Groq (Llama 3.3 70B)
* Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
* Vector Database: ChromaDB
* PDF Processing: PyMuPDF
* Chunking: LangChain RecursiveCharacterTextSplitter
* Environment Management: python-dotenv

⸻

📂 Project Structure

ai-knowledge-assistant/
│
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── chunk_service.py
│   │   ├── embedding_service.py
│   │   ├── chroma_service.py
│   │   └── llm_service.py
│   └── main.py
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
├── tests/
├── streamlit_app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

⸻

🏗️ System Architecture

                PDF Upload
                     │
                     ▼
          PDF Text Extraction
                     │
                     ▼
             Text Chunking
                     │
                     ▼
       Sentence Transformer Embeddings
                     │
                     ▼
              ChromaDB Storage
                     │
                     ▼
          Semantic Similarity Search
                     │
                     ▼
         Retrieved Relevant Chunks
                     │
                     ▼
              Groq LLM (Llama)
                     │
                     ▼
              AI Generated Answer

⸻

⚙️ Installation

Clone the repository

git clone <your-github-repo-url>
cd ai-knowledge-assistant

Create a virtual environment

python -m venv .venv

Activate the environment

macOS / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

⸻

🔑 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key

⸻

▶️ Run the Application

streamlit run streamlit_app.py

Open:

http://localhost:8501

⸻

💡 Example Questions

* Summarize this document.
* What programming languages are mentioned?
* What projects are listed?
* What frameworks does the candidate know?
* What are the key skills discussed?

⸻

🧠 How It Works

1. Upload a PDF.
2. Extract text from the document.
3. Split the text into manageable chunks.
4. Generate embeddings for each chunk.
5. Store embeddings in ChromaDB.
6. Embed the user’s question.
7. Retrieve the most relevant chunks.
8. Send the retrieved context and question to the Groq LLM.
9. Display the generated answer.

⸻

📈 Future Enhancements

* Multi-document support
* User authentication
* Persistent chat sessions
* Citation-aware answers
* Cloud deployment
* Docker support
* FastAPI REST endpoints

⸻

👨‍💻 Author

Prasad Patil

Built as a portfolio project to demonstrate practical skills in Python, Generative AI, Retrieval-Augmented Generation (RAG), vector databases, and LLM integration.

ai-knowledge-assistant/
│
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── chunk_service.py
│   │   ├── embedding_service.py
│   │   ├── chroma_service.py
│   │   └── llm_service.py
│   └── main.py
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
├── tests/
├── streamlit_app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


                PDF Upload
                     │
                     ▼
          PDF Text Extraction
                     │
                     ▼
             Text Chunking
                     │
                     ▼
       Sentence Transformer Embeddings
                     │
                     ▼
              ChromaDB Storage
                     │
                     ▼
          Semantic Similarity Search
                     │
                     ▼
         Retrieved Relevant Chunks
                     │
                     ▼
              Groq LLM (Llama)
                     │
                     ▼
              AI Generated Answer