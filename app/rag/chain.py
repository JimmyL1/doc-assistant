from langchain_core.documents import Document
from app.rag.prompts import RAG_PROMPT
from app.core.llm import get_llm
from app.core.vector_store import as_retriever


def _format_docs(docs: list[Document]) -> str:
    # Format retrieved chunks into a single context string with source labels
    parts = []
    for doc in docs:
        source = doc.metadata.get("source", "未知來源")
        page = doc.metadata.get("page", "")
        page_info = f"（第 {page + 1} 頁）" if page != "" else ""
        parts.append(f"【來源：{source}{page_info}】\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def query(question: str, k: int = None) -> dict:
    # Step 1: retrieve relevant chunks from the vector store
    retriever = as_retriever(k)
    source_docs = retriever.invoke(question)
    context = _format_docs(source_docs)

    # Step 2: send context + question to the LLM and get an answer
    messages = RAG_PROMPT.format_messages(context=context, question=question)
    response = get_llm().invoke(messages)
    answer = response.content if isinstance(response.content, str) else str(response.content)

    return {
        "answer": answer,
        "source_documents": source_docs,
        "question": question,
    }
