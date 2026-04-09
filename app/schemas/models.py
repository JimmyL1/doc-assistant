from pydantic import BaseModel


class SourceDocument(BaseModel):
    content: str
    metadata: dict


class QueryRequest(BaseModel):
    question: str
    k: int | None = None  # override default retrieval_k from settings


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_added: int


class HealthResponse(BaseModel):
    status: str
    vector_store_count: int
