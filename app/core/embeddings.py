from langchain_core.embeddings import Embeddings
from config.settings import settings

# Module-level singleton — embedding model is expensive to load,
# so we initialize it once and reuse across all requests.
_embeddings_instance = None


def get_embeddings() -> Embeddings:
    global _embeddings_instance
    if _embeddings_instance is None:
        if settings.embedding_provider == "huggingface":
            # Lazy import: avoids loading heavy ML libraries until actually needed
            from langchain_huggingface import HuggingFaceEmbeddings
            _embeddings_instance = HuggingFaceEmbeddings(
                model_name=settings.embedding_model
            )
        else:
            raise ValueError(f"Unknown embedding provider: {settings.embedding_provider}")
    return _embeddings_instance
