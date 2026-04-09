from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from config.settings import settings

# Module-level singleton — Chroma client holds an open connection to the DB
_vector_store_instance = None


def get_vector_store():
    global _vector_store_instance
    if _vector_store_instance is None:
        from langchain_chroma import Chroma
        from app.core.embeddings import get_embeddings
        _vector_store_instance = Chroma(
            collection_name=settings.collection_name,
            embedding_function=get_embeddings(),
            persist_directory=settings.chroma_persist_dir,
        )
    return _vector_store_instance


def add_documents(docs: list[Document]) -> int:
    get_vector_store().add_documents(docs)
    return len(docs)


def as_retriever(k: int = None) -> VectorStoreRetriever:
    # Fall back to the configured default if k is not specified
    if k is None:
        k = settings.retrieval_k
    return get_vector_store().as_retriever(search_kwargs={"k": k})


def get_document_count() -> int:
    result = get_vector_store().get()
    return len(result["ids"])
