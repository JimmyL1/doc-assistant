import re
from pathlib import Path

from langchain_core.documents import Document


def parse_html(file_path: str | Path) -> list[Document]:
    from bs4 import BeautifulSoup

    file_path = Path(file_path)
    try:
        raw = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = file_path.read_text(encoding="cp950")

    soup = BeautifulSoup(raw, "html.parser")

    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # Collapse multiple consecutive blank lines into a single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)

    if not text.strip():
        raise ValueError(f"No text content found in HTML file: {file_path.name}")

    return [Document(
        page_content=text,
        metadata={"source": file_path.name, "file_type": "html", "page": 0},
    )]
