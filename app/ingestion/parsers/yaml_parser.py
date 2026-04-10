import yaml
from pathlib import Path
from langchain_core.documents import Document


def _flatten(obj, prefix: str = "") -> list[str]:
    """Recursively flatten a YAML object into key: value lines."""
    lines = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else str(k)
            lines.extend(_flatten(v, full_key))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            lines.extend(_flatten(item, f"{prefix}[{i}]"))
    else:
        lines.append(f"{prefix}: {obj}")
    return lines


def parse_yaml(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    raw = file_path.read_text(encoding="utf-8")

    docs_yaml = list(yaml.safe_load_all(raw))
    if not docs_yaml or all(d is None for d in docs_yaml):
        raise ValueError(f"No content found in YAML file: {file_path.name}")

    pieces = []
    for obj in docs_yaml:
        if obj is not None:
            pieces.extend(_flatten(obj))

    text = "\n".join(pieces)

    return [Document(
        page_content=text,
        metadata={
            "source": file_path.name,
            "file_type": "yaml",
            "page": 0,
        },
    )]
