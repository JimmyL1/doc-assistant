from pathlib import Path
from langchain_core.documents import Document
from app.ingestion.parsers.image_parser import SUPPORTED_IMAGE_EXTENSIONS

# All file types this system can ingest — single source of truth
SUPPORTED_EXTENSIONS = (
    {".txt", ".pdf", ".docx", ".xlsx", ".xls", ".csv", ".pptx",
     ".eml", ".msg", ".html", ".htm", ".md", ".json", ".xml",
     ".rtf", ".yaml", ".yml"}
    | SUPPORTED_IMAGE_EXTENSIONS
)


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
    elif suffix in {".xlsx", ".xls"}:
        from app.ingestion.parsers.xlsx_parser import parse_xlsx
        return parse_xlsx(file_path)
    elif suffix == ".csv":
        from app.ingestion.parsers.csv_parser import parse_csv
        return parse_csv(file_path)
    elif suffix == ".pptx":
        from app.ingestion.parsers.pptx_parser import parse_pptx
        return parse_pptx(file_path)
    elif suffix == ".eml":
        from app.ingestion.parsers.eml_parser import parse_eml
        return parse_eml(file_path)
    elif suffix == ".msg":
        from app.ingestion.parsers.msg_parser import parse_msg
        return parse_msg(file_path)
    elif suffix in {".html", ".htm"}:
        from app.ingestion.parsers.html_parser import parse_html
        return parse_html(file_path)
    elif suffix == ".md":
        from app.ingestion.parsers.md_parser import parse_md
        return parse_md(file_path)
    elif suffix == ".json":
        from app.ingestion.parsers.json_parser import parse_json
        return parse_json(file_path)
    elif suffix == ".xml":
        from app.ingestion.parsers.xml_parser import parse_xml
        return parse_xml(file_path)
    elif suffix == ".rtf":
        from app.ingestion.parsers.rtf_parser import parse_rtf
        return parse_rtf(file_path)
    elif suffix in {".yaml", ".yml"}:
        from app.ingestion.parsers.yaml_parser import parse_yaml
        return parse_yaml(file_path)
    elif suffix in SUPPORTED_IMAGE_EXTENSIONS:
        from app.ingestion.parsers.image_parser import parse_image
        return parse_image(file_path)
    else:
        raise ValueError(
            f"不支援的檔案格式：{suffix}。支援格式：{', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
