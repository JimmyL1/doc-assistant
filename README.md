# doc-assistant

A RAG (Retrieval-Augmented Generation) document Q&A system. Upload PDF, DOCX, or TXT documents and ask questions — Claude retrieves relevant chunks and generates grounded answers.

## Features

- Upload documents (PDF / DOCX / TXT)
- Semantic search via ChromaDB + HuggingFace embeddings (`all-MiniLM-L6-v2`)
- Answer generation via Claude (`claude-haiku-4-5-20251001`)
- FastAPI REST API
- Prepared v2 skeleton using LangGraph (`app/agents/`)

## Quick Start

### 1. Clone & install

```bash
git clone <repo-url>
cd doc-assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api...
```

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/upload` | Upload and ingest a document |
| GET | `/api/v1/documents` | List ingested documents |
| POST | `/api/v1/query` | Ask a question |
| GET | `/api/v1/health` | Health check + document count |

### Upload a document

```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@your_document.pdf"
```

### Ask a question

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

Response:

```json
{
  "answer": "...",
  "sources": [
    { "content": "...", "metadata": { "source": "doc.pdf", "page": 1 } }
  ]
}
```

## Configuration

All settings are in [config/settings.py](config/settings.py) and can be overridden via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *(required)* | Anthropic API key |
| `LLM_MODEL` | `claude-haiku-4-5-20251001` | Claude model ID |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `CHUNK_SIZE` | `1000` | Text chunk size (characters) |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVAL_K` | `4` | Number of chunks retrieved per query |

## Architecture

### Upload Pipeline

```
File (PDF/DOCX/TXT)
  → app/ingestion/loader.py       dispatches to format-specific parser
  → app/ingestion/parsers/        returns list[Document] with metadata
  → app/ingestion/splitter.py     RecursiveCharacterTextSplitter
  → app/core/embeddings.py        HuggingFace all-MiniLM-L6-v2
  → app/core/vector_store.py      Chroma, persisted to chroma_db/
```

### Query Pipeline

```
Question
  → app/rag/chain.py              orchestrates retrieval + generation
  → app/core/vector_store.py      semantic similarity search, k=4
  → app/rag/prompts.py            RAG_PROMPT template with context
  → app/core/llm.py               Claude via langchain-anthropic
  → QueryResponse (answer + source documents)
```

## Running Tests

```bash
pytest

# Single file
pytest tests/test_query.py

# Single test
pytest tests/test_query.py::test_function_name -v
```

## Project Structure

```
doc-assistant
├─ app
│  ├─ agents
│  │  ├─ README.md
│  │  └─ __init__.py
│  ├─ api
│  │  ├─ routes_documents.py
│  │  ├─ routes_query.py
│  │  └─ __init__.py
│  ├─ core
│  │  ├─ embeddings.py
│  │  ├─ llm.py
│  │  ├─ vector_store.py
│  │  └─ __init__.py
│  ├─ ingestion
│  │  ├─ loader.py
│  │  ├─ parsers
│  │  │  ├─ docx_parser.py
│  │  │  ├─ image_parser.py
│  │  │  ├─ pdf_parser.py
│  │  │  ├─ txt_parser.py
│  │  │  └─ __init__.py
│  │  ├─ splitter.py
│  │  └─ __init__.py
│  ├─ main.py
│  ├─ rag
│  │  ├─ chain.py
│  │  ├─ prompts.py
│  │  └─ __init__.py
│  ├─ schemas
│  │  ├─ models.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ config
│  ├─ settings.py
│  └─ __init__.py
├─ raw                  (sample documents for testing)
├─ tests
│  ├─ conftest.py
│  ├─ test_api.py
│  ├─ test_ingestion.py
│  ├─ test_vector_store.py
│  └─ __init__.py
├─ .env.example
├─ Procfile
├─ README.md
└─ requirements.txt
```

## Roadmap

- **v2**: LangGraph-based agent with multi-step reasoning and web search (`app/agents/`)
