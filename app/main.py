from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes_documents import router as documents_router
from app.api.routes_query import router as query_router
from app.core.vector_store import get_vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize vector store on startup so the first request isn't slow
    get_vector_store()
    yield


app = FastAPI(
    title="內部文件智慧助理",
    description="上傳文件後用自然語言問答的 RAG 系統",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(documents_router, prefix="/api/v1", tags=["documents"])
app.include_router(query_router, prefix="/api/v1", tags=["query"])
