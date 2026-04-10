from pathlib import Path
from langchain_core.documents import Document


def parse_md(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    text = file_path.read_text(encoding="utf-8", errors="replace")

    sections = text.split("## ")
    # First element is everything before the first H2 (may be empty or preamble)
    # sections[0] is pre-H2 content; sections[1:] each start with the heading text
    h2_sections = sections[1:]

    if not h2_sections:
        return [Document(
            page_content=text.strip(),
            metadata={"source": file_path.name, "file_type": "md", "page": 0},
        )]

    documents = []
    section_index = 0
    for raw in h2_sections:
        content = raw.strip()
        if not content:
            continue
        documents.append(Document(
            page_content=content,
            metadata={"source": file_path.name, "file_type": "md", "page": section_index},
        ))
        section_index += 1

    return documents
