import csv
from pathlib import Path

from langchain_core.documents import Document


def parse_csv(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)

    rows: list[list[str]] = []
    for encoding in ("utf-8", "cp950"):
        try:
            with file_path.open(newline="", encoding=encoding) as f:
                reader = csv.reader(f)
                rows = list(reader)
            break
        except UnicodeDecodeError:
            continue

    if not rows:
        raise ValueError(f"No content could be read from '{file_path.name}'")

    headers = rows[0]
    lines: list[str] = [" | ".join(headers)]

    for row in rows[1:]:
        if all(cell.strip() == "" for cell in row):
            continue
        parts = [
            f"{headers[i]}: {cell}" if i < len(headers) else cell
            for i, cell in enumerate(row)
        ]
        lines.append(" | ".join(parts))

    text = "\n".join(lines)

    return [Document(
        page_content=text,
        metadata={
            "source": file_path.name,
            "file_type": "csv",
            "page": 0,
        },
    )]
