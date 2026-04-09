from pathlib import Path
from langchain_core.documents import Document


def parse_txt(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    text = file_path.read_text(encoding="utf-8", errors="replace")
    return [Document(
        page_content=text,
        metadata={"source": file_path.name, "file_type": "txt", "page": 0},
    )]
