<div align="center">

# Query AI

**RAG-powered document intelligence. Ask anything about your documents.**

Upload PDFs, Word docs, Markdown, or CSVs — then ask questions in plain English.
Query AI retrieves semantically relevant content using vector embeddings and answers with Groq-powered LLaMA 3.3 70B.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://thequeryai.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

[**Try the live demo →**](https://thequeryai.streamlit.app/)

---

<!-- Add a demo GIF here: ![Demo](assets/demo.gif) -->

</div>

---

## What it does

Query AI gives you a conversational interface for three types of analysis:

**Document Intelligence** — Upload one or more files and ask questions across all of them. The system chunks, embeds, and indexes your content in ChromaDB, then retrieves semantically relevant passages to answer your query with source attribution.

**Text Intelligence** — Paste any text and run instant summarization, sentiment analysis, keyword extraction, or Q&A.

**Code Intelligence** — Paste source code and get explanations, bug detection, improvement suggestions, or generated test cases.

---

## Architecture

```
                ┌──────────────────────────┐
                │     Streamlit Frontend   │
                │  (Chat Interface & UI)   │
                └─────────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │   Input Processing     │
                  │  Documents / Text / Code│
                  └─────────────┬──────────┘
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
      Document Pipeline    Text Analysis      Code Analysis
      ─────────────────
      PDF/DOCX/TXT/MD/CSV
      Text Extraction
      Recursive Chunking
      SentenceTransformer
       Embeddings (MiniLM)
      ChromaDB Indexing
      Semantic Retrieval
             │
             └──────────────────┬──────────────────┘
                                ▼
                      Groq LLM — Llama 3.3 70B
                                │
                                ▼
                   Context-Aware Response + Sources
```

---

## Design decisions

**Why ChromaDB over Pinecone/Weaviate?**
Lightweight, zero-infrastructure, and fully local — ideal for a portfolio project where startup time and simplicity matter. Trade-off: not horizontally scalable for enterprise workloads.

**Why `all-MiniLM-L6-v2` over larger embedding models?**
Fast inference, compact vectors, and strong semantic search quality at a fraction of the compute cost. Trade-off: larger models (e.g. `bge-large`) may improve retrieval precision on technical domains.

**Why Groq + Llama 3.3 70B over OpenAI?**
Sub-second inference latency and no per-token cost ceiling during development. Trade-off: dependent on external API availability and rate limits.

**Why `RecursiveCharacterTextSplitter` over fixed-length chunking?**
Preserves paragraph and sentence boundaries using a hierarchy of separators, with overlap to reduce context fragmentation at chunk edges. This consistently outperforms naive fixed-size slicing on retrieval tasks.

**Why Streamlit for the frontend?**
Fastest path from RAG logic to interactive UI — Streamlit's session state integrates cleanly with a chat loop. Trade-off: for production systems, a FastAPI backend + React frontend would offer more control and scalability.

---

## Features

| Feature | Detail |
|---|---|
| Multi-format ingestion | PDF, DOCX, TXT, Markdown, CSV |
| Multi-document reasoning | Ask questions that span across all uploaded files |
| Semantic search | Vector similarity retrieval — not keyword matching |
| Source attribution | Responses reference the exact chunks they came from |
| Text intelligence | Summarize, sentiment, keyword extraction, Q&A |
| Code intelligence | Explain, debug, improve, generate tests |
| Chat history | Auto-titled conversations with follow-up context |
| Error handling | Validation for empty files, bad formats, API failures |

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Frontend | Streamlit |
| LLM | Groq API — Llama 3.3 70B |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector store | ChromaDB |
| PDF parsing | PyMuPDF |
| DOCX parsing | python-docx |
| Text chunking | LangChain `RecursiveCharacterTextSplitter` |
| Data processing | Pandas |
| Testing | pytest |

---

## Getting started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
git clone https://github.com/mrpatil1260/query-ai.git
cd query-ai

python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Add your Groq API key to .env
```

```env
GROQ_API_KEY=your_api_key_here
```

### Run

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Testing

```bash
pytest
```

Unit tests cover document chunking, embedding generation, ChromaDB indexing and retrieval, multi-format extraction, text analysis, and code analysis services.

---

## Project structure

```
query-ai/
│
├── app/
│   ├── components/        # Streamlit UI components
│   ├── services/          # RAG pipeline, text & code analysis
│   ├── api/               # API layer
│   └── models/            # Data models
│
├── data/
│   ├── uploads/           # Temporary file storage
│   └── chroma_db/         # Persistent vector index
│
├── tests/                 # pytest unit tests
├── streamlit_app.py       # App entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## Example use cases

- **Resume screening** — Upload 5 resumes, ask "Which candidate has the most Python experience?"
- **Research synthesis** — Upload 3 papers, ask "What do all these agree on about attention mechanisms?"
- **Contract review** — Upload a legal PDF, ask "What are the termination clauses?"
- **CSV exploration** — Upload sales data, ask "Which region had the highest Q3 revenue?"
- **Code review** — Paste a function, ask "What edge cases does this miss?"

---

## Roadmap

- [ ] FastAPI REST backend (`POST /upload`, `POST /query`)
- [ ] Hybrid search — BM25 + vector with reciprocal rank fusion
- [ ] Streaming LLM responses
- [ ] Reranking with cross-encoder models
- [ ] Docker + docker-compose setup
- [ ] Persistent conversation history (SQLite)
- [ ] Retrieval quality evaluation pipeline

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built by **[Prasad Patil](https://github.com/mrpatil1260)** · [LinkedIn](https://linkedin.com/in/your-profile)

*Demonstrates practical skills in Python, Generative AI, RAG, vector databases, semantic search, and LLM-powered applications.*

</div>