from pathlib import Path
from pydantic_settings import BaseSettings

# Project root directory, used to build absolute paths for data dirs
BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # LLM
    anthropic_api_key: str = ""
    llm_model: str = "claude-haiku-4-5-20251001"

    # Embeddings
    embedding_provider: str = "huggingface"  # "huggingface" or "openai"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    # Vector store
    chroma_persist_dir: str = str(BASE_DIR / "chroma_db")
    collection_name: str = "documents"

    # Ingestion
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval: number of chunks returned per query
    retrieval_k: int = 4

    model_config = {"env_file": str(BASE_DIR / ".env"), "env_file_encoding": "utf-8"}


settings = Settings()
