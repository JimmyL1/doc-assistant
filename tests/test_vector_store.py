from langchain_core.documents import Document
from app.core.vector_store import add_documents, as_retriever


def test_add_and_search():
    docs = [Document(
        page_content="人工智慧是電腦科學的一個分支，專注於建立智慧系統",
        metadata={"source": "test.txt", "file_type": "txt", "page": 0,
                  "chunk_index": 0, "total_chunks": 1},
    )]
    add_documents(docs)
    retriever = as_retriever(k=1)
    results = retriever.invoke("人工智慧")
    assert len(results) > 0
    assert "人工智慧" in results[0].page_content
