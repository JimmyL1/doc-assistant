from pathlib import Path
from langchain_core.documents import Document
from striprtf.striprtf import rtf_to_text


def parse_rtf(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    raw = file_path.read_text(encoding="utf-8", errors="replace")
    text = rtf_to_text(raw).strip()

    if not text:
        raise ValueError(f"No text content found in RTF file: {file_path.name}")

    return [Document(
        page_content=text,
        metadata={
            "source": file_path.name,
            "file_type": "rtf",
            "page": 0,
        },
    )]
