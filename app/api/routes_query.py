import asyncio
from fastapi import APIRouter
from app.schemas.models import QueryRequest, QueryResponse, HealthResponse, SourceDocument
from app.rag.chain import query as rag_query
from app.core.vector_store import get_document_count

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    # RAG query is CPU/IO bound — run in a thread to avoid blocking the event loop
    result = await asyncio.to_thread(rag_query, request.question, request.k)
    sources = [
        SourceDocument(content=doc.page_content, metadata=doc.metadata)
        for doc in result["source_documents"]
    ]
    return QueryResponse(answer=result["answer"], sources=sources)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    count = await asyncio.to_thread(get_document_count)
    return HealthResponse(status="ok", vector_store_count=count)
