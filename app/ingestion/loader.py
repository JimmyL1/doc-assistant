from pathlib import Path
from langchain_core.documents import Document
from app.ingestion.parsers.image_parser import SUPPORTED_IMAGE_EXTENSIONS

# All file types this system can ingest — single source of truth
SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"} | SUPPORTED_IMAGE_EXTENSIONS


def load_file(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    # Dispatch to the appropriate parser based on file extension
    if suffix == ".txt":
        from app.ingestion.parsers.txt_parser import parse_txt
        return parse_txt(file_path)
    elif suffix == ".pdf":
        from app.ingestion.parsers.pdf_parser import parse_pdf
        return parse_pdf(file_path)
    elif suffix == ".docx":
        from app.ingestion.parsers.docx_parser import parse_docx
        return parse_docx(file_path)
    elif suffix in SUPPORTED_IMAGE_EXTENSIONS:
        from app.ingestion.parsers.image_parser import parse_image
        return parse_image(file_path)
    else:
        raise ValueError(
            f"不支援的檔案格式：{suffix}。支援格式：{', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
