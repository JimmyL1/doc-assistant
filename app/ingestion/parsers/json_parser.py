import json
from pathlib import Path
from langchain_core.documents import Document


def parse_json(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    raw = file_path.read_text(encoding="utf-8")
    data = json.loads(raw)

    if isinstance(data, list):
        item_count = len(data)
        text = "\n---\n".join(
            json.dumps(item, ensure_ascii=False, indent=2) for item in data
        )
    elif isinstance(data, dict):
        item_count = len(data)
        text = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        item_count = 1
        text = json.dumps(data, ensure_ascii=False)

    return [Document(
        page_content=text,
        metadata={
            "source": file_path.name,
            "file_type": "json",
            "page": 0,
            "item_count": item_count,
        },
    )]
