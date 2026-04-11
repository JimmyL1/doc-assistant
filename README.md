# doc-assistant

Have a pile of documents and questions about them? This tool lets you upload your files and ask questions in plain English — it finds the relevant parts and uses Claude to give you a grounded answer.

Under the hood it's a RAG (Retrieval-Augmented Generation) system: documents get broken into chunks, embedded into a vector database, and retrieved at query time so Claude answers from your actual content rather than making things up.

## What file types does it support?

Pretty much everything you'd encounter day-to-day:

| Category | Formats |
|----------|---------|
| Documents | PDF, DOCX, TXT, RTF, MD |
| Spreadsheets | CSV, XLSX |
| Presentations | PPTX |
| Data/Markup | JSON, XML, YAML, HTML |
| Email | EML, MSG |
| Images | PNG, JPG, JPEG, GIF, WEBP |

## Getting started

### Step 1 — Clone and install dependencies

```bash
git clone <repo-url>
cd doc-assistant

# Create a virtual environment (keeps your system Python clean)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Step 2 — Add your API key

```bash
cp .env.example .env
```

Open `.env` and paste your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api...
```

Don't have a key yet? Get one at [console.anthropic.com](https://console.anthropic.com).

### Step 3 — Start the server

```bash
uvicorn app.main:app --reload
```

The API is now running at `http://localhost:8000`.
Visit `http://localhost:8000/docs` for an interactive browser UI where you can try all the endpoints without writing any code.

## How to use it

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

You'll get back an answer and the source chunks it was drawn from:

```json
{
  "answer": "...",
  "sources": [
    { "content": "...", "metadata": { "source": "doc.pdf", "page": 1 } }
  ]
}
```

### Other endpoints

| Method | Path | What it does |
|--------|------|-------------|
| POST | `/api/v1/upload` | Upload and ingest a document |
| GET | `/api/v1/documents` | List all ingested documents |
| POST | `/api/v1/query` | Ask a question |
| GET | `/api/v1/health` | Check server status + document count |

## Configuration

All settings live in [config/settings.py](config/settings.py). You can override any of them with environment variables — no code change needed.

| Variable | Default | What it controls |
|----------|---------|-----------------|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `LLM_MODEL` | `claude-haiku-4-5-20251001` | Which Claude model generates answers |
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | HuggingFace model used for embeddings (50+ languages, including Chinese) |
| `CHUNK_SIZE` | `1000` | How large each text chunk is (characters) |
| `CHUNK_OVERLAP` | `200` | How much chunks overlap (helps preserve context at boundaries) |
| `RETRIEVAL_K` | `4` | How many chunks are retrieved per question |

## How it works

### Upload pipeline

When you upload a file, it goes through this chain:

```
Your file
  → app/ingestion/loader.py       picks the right parser for the format
  → app/ingestion/parsers/        extracts text + metadata
  → app/ingestion/splitter.py     splits text into overlapping chunks
  → app/core/embeddings.py        converts chunks to vectors (paraphrase-multilingual-MiniLM-L12-v2)
  → app/core/vector_store.py      stores vectors in ChromaDB (chroma_db/)
```

### Query pipeline

When you ask a question:

```
Your question
  → app/rag/chain.py              coordinates retrieval and generation
  → app/core/vector_store.py      finds the k most relevant chunks
  → app/rag/prompts.py            injects chunks into the prompt template
  → app/core/llm.py               sends to Claude, gets an answer back
  → response with answer + sources
```

## Running tests

```bash
# Run everything
pytest

# Run a specific file
pytest tests/test_query.py

# Run a specific test with verbose output
pytest tests/test_query.py::test_function_name -v
```

## Project layout

```
doc-assistant/
├── app/
│   ├── agents/          # v2 LangGraph agent (work in progress)
│   ├── api/             # FastAPI route handlers
│   ├── core/            # LLM, embeddings, vector store singletons
│   ├── ingestion/       # File loading, parsing, chunking
│   ├── rag/             # Retrieval chain and prompt templates
│   └── schemas/         # Request/response data models
├── config/              # Settings (Pydantic BaseSettings)
├── sample_docs/         # Sample files for testing
├── tests/
├── .env.example
└── requirements.txt
```

## What's next

**v2** will replace the simple retrieval chain with a LangGraph agent (`app/agents/`) capable of multi-step reasoning, deciding when to search the web, and handling more complex queries.
