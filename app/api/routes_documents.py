import asyncio
import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.models import UploadResponse
from app.ingestion.loader import load_file, SUPPORTED_EXTENSIONS
from app.ingestion.splitter import split_documents
from app.core.vector_store import add_documents, get_vector_store

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail=f"不支援的檔案格式：{suffix}。支援格式：{', '.join(SUPPORTED_EXTENSIONS)}",
        )

    content = await file.read()

    # Write to a temp file so parsers can open it by path.
    # delete=False avoids Windows file-lock issues; we clean up in finally.
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    tmp_path = Path(tmp.name)
    try:
        tmp.write(content)
        tmp.close()

        # Parse, split, and embed — all blocking I/O, so run in a thread
        docs = await asyncio.to_thread(load_file, tmp_path)
        original_name = Path(file.filename).name
        for doc in docs:
            doc.metadata["source"] = original_name
        chunks = await asyncio.to_thread(split_documents, docs)
        count = await asyncio.to_thread(add_documents, chunks)
    finally:
        tmp_path.unlink(missing_ok=True)

    return UploadResponse(message="上傳成功", filename=file.filename, chunks_added=count)


@router.get("/documents")
async def list_documents():
    vs = get_vector_store()
    results = vs.get()

    # Collect unique source filenames from chunk metadata
    sources = set()
    for metadata in results.get("metadatas", []):
        if metadata and "source" in metadata:
            sources.add(metadata["source"])

    return {"documents": sorted(sources), "total_chunks": len(results.get("ids", []))}
