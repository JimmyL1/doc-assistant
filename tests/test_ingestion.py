import pytest
from pathlib import Path
from app.ingestion.loader import load_file
from app.ingestion.splitter import split_documents

SAMPLE_DIR = Path(__file__).parent / "sample_docs"


def test_load_txt():
    docs = load_file(SAMPLE_DIR / "engineering_onboarding.txt")
    assert len(docs) > 0
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "engineering_onboarding.txt"
    assert docs[0].metadata["file_type"] == "txt"


def test_split_adds_metadata():
    docs = load_file(SAMPLE_DIR / "engineering_onboarding.txt")
    chunks = split_documents(docs)
    assert len(chunks) > 0
    assert "chunk_index" in chunks[0].metadata
    assert "total_chunks" in chunks[0].metadata
    assert chunks[0].metadata["total_chunks"] == len(chunks)


def test_unsupported_file_raises():
    with pytest.raises(ValueError, match="不支援"):
        load_file("test.jpg")
