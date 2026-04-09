from pathlib import Path
from langchain_core.documents import Document


def parse_pdf(file_path: str | Path) -> list[Document]:
    from pypdf import PdfReader
    file_path = Path(file_path)
    reader = PdfReader(str(file_path))
    docs = []

    # Each page becomes a separate Document to preserve page number metadata
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            docs.append(Document(
                page_content=text,
                metadata={"source": file_path.name, "file_type": "pdf", "page": i},
            ))

    if not docs:
        raise ValueError(f"無法從 {file_path.name} 擷取文字（可能是掃描版 PDF）")
    return docs
