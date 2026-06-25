🧠 Query AI

Query AI is an AI-powered platform for document understanding, text analysis, and code intelligence. It provides a unified ChatGPT-style interface where users can upload documents, analyze text, inspect source code, and ask natural language questions powered by semantic search and large language models.

⸻

✨ Features

📄 Multi-Format Document Intelligence

Upload one or more documents and interact with them conversationally.

Supported Formats

* ✅ PDF (.pdf)
* ✅ Microsoft Word (.docx)
* ✅ Text (.txt)
* ✅ Markdown (.md)
* ✅ CSV (.csv)

Capabilities

* Automatic text extraction
* Smart document chunking
* Semantic embeddings generation
* Vector indexing with ChromaDB
* AI-powered question answering
* Multi-document understanding
* Cross-document comparison
* Source chunk references

⸻

💬 Unified Chat Interface

Query AI provides a ChatGPT-style conversational experience.

* Ask questions naturally
* Continue follow-up conversations
* Maintain context across interactions
* Automatically generate chat titles
* Start new conversations with one click

⸻

📝 Text Intelligence

Analyze any pasted text using AI.

Supported actions include:

* Summarization
* Sentiment Analysis
* Keyword Extraction
* Question Answering

⸻

💻 Code Intelligence

Paste source code and receive AI-powered insights.

Supported actions include:

* Explain Code
* Find Bugs
* Suggest Improvements
* Generate Tests

⸻

🔍 Semantic Search

Instead of keyword matching, Query AI retrieves information based on semantic meaning using vector embeddings, enabling more accurate and context-aware responses.

⸻

📚 Multi-Document Support

Upload multiple documents in the same session and ask questions across all of them.

For example:

* Compare two resumes
* Find differences between reports
* Identify common topics
* Ask questions requiring information from multiple files

⸻

🛠️ Tech Stack

Category	Technology
Language	Python
Frontend	Streamlit
LLM	Groq (Llama Models)
Embeddings	Sentence Transformers (all-MiniLM-L6-v2)
Vector Database	ChromaDB
PDF Processing	PyMuPDF
DOCX Processing	python-docx
Data Processing	Pandas
Text Chunking	LangChain RecursiveCharacterTextSplitter

⸻

📂 Project Structure

query-ai/
│
├── app/
│   ├── components/
│   ├── services/
│   ├── api/
│   └── models/
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .env

⸻

User
  │
  ▼
Streamlit UI
  │
  ▼
Document Upload
  │
  ▼
Text Extraction
  │
  ▼
Chunking
  │
  ▼
Embeddings
  │
  ▼
ChromaDB
  │
  ▼
Semantic Retrieval
  │
  ▼
Groq Llama 3.3 70B
  │
  ▼
Final Response


⸻


⚙️ Installation

git clone <your-repository-url>
cd query-ai
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

⸻

🔑 Environment Variables

Create a .env file:

GROQ_API_KEY=your_api_key_here

⸻

▶️ Run the Application

streamlit run streamlit_app.py

Then open:

http://localhost:8501

⸻

🚀 Workflow

1. Upload one or more supported documents.
2. Documents are automatically processed and indexed.
3. Ask questions in natural language.
4. Query AI performs semantic retrieval using vector embeddings.
5. The LLM generates context-aware responses.
6. Continue the conversation with follow-up questions.

You can also paste text or source code and use the built-in analysis features.

⸻

💡 Example Use Cases

* Resume analysis and comparison
* Research paper exploration
* Business document summarization
* Technical documentation assistance
* Code explanation and debugging
* AI-powered text summarization
* CSV data understanding
* Knowledge base search

⸻

🌟 Highlights

* ChatGPT-style interface
* Multi-format document support
* Multi-document reasoning
* AI-powered text intelligence
* AI-powered code intelligence
* Semantic search with embeddings
* ChromaDB vector storage
* Source-aware responses
* Clean and intuitive Streamlit UI

⸻

📄 License

This project is licensed under the MIT License.

⸻

👨‍💻 Author

Prasad Patil

Built as a portfolio project to demonstrate practical skills in Python, Generative AI, Retrieval-Augmented Generation (RAG), vector databases, semantic search, and LLM-powered applications.
