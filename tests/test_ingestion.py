import pytest
from pathlib import Path
from app.ingestion.loader import load_file
from app.ingestion.splitter import split_documents
from config.settings import settings

SAMPLE_DOCS = Path(__file__).parent.parent / "sample_docs"


# ---------------------------------------------------------------------------
# Plain text
# ---------------------------------------------------------------------------

def test_load_txt():
    docs = load_file(SAMPLE_DOCS / "engineering_onboarding.txt")
    assert len(docs) > 0
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "engineering_onboarding.txt"
    assert docs[0].metadata["file_type"] == "txt"


# ---------------------------------------------------------------------------
# PDF — each page becomes a separate Document
# ---------------------------------------------------------------------------

def test_load_pdf():
    docs = load_file(SAMPLE_DOCS / "api_integration_guide_v3.pdf")
    assert len(docs) > 0
    for doc in docs:
        assert doc.page_content.strip() != ""
        assert doc.metadata["source"] == "api_integration_guide_v3.pdf"
        assert doc.metadata["file_type"] == "pdf"
        assert isinstance(doc.metadata["page"], int)


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

def test_load_docx():
    docs = load_file(SAMPLE_DOCS / "board_meeting_minutes_q1_2025.docx")
    assert len(docs) > 0
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "board_meeting_minutes_q1_2025.docx"
    assert docs[0].metadata["file_type"] == "docx"


# ---------------------------------------------------------------------------
# XLSX — each sheet becomes a separate Document
# ---------------------------------------------------------------------------

def test_load_xlsx():
    docs = load_file(SAMPLE_DOCS / "sales_report_q1_2025.xlsx")
    assert len(docs) > 0
    for doc in docs:
        assert doc.page_content.strip() != ""
        assert doc.metadata["source"] == "sales_report_q1_2025.xlsx"
        assert doc.metadata["file_type"] == "xlsx"
        assert "sheet" in doc.metadata


def test_load_xls():
    docs = load_file(SAMPLE_DOCS / "employee_roster_2024_legacy.xls")
    assert len(docs) > 0
    assert docs[0].metadata["source"] == "employee_roster_2024_legacy.xls"
    assert docs[0].metadata["file_type"] == "xlsx"  # normalised to "xlsx"
    assert "sheet" in docs[0].metadata


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

def test_load_csv():
    docs = load_file(SAMPLE_DOCS / "customer_list_2025.csv")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "customer_list_2025.csv"
    assert docs[0].metadata["file_type"] == "csv"


# ---------------------------------------------------------------------------
# PPTX — each slide (with text) becomes a separate Document
# ---------------------------------------------------------------------------

def test_load_pptx():
    docs = load_file(SAMPLE_DOCS / "ai_strategy_2025.pptx")
    assert len(docs) > 0
    for doc in docs:
        assert doc.page_content.strip() != ""
        assert doc.metadata["source"] == "ai_strategy_2025.pptx"
        assert doc.metadata["file_type"] == "pptx"
        assert "slide" in doc.metadata


# ---------------------------------------------------------------------------
# EML
# ---------------------------------------------------------------------------

def test_load_eml():
    docs = load_file(SAMPLE_DOCS / "email_new_employee_welcome.eml")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "email_new_employee_welcome.eml"
    assert docs[0].metadata["file_type"] == "eml"


# ---------------------------------------------------------------------------
# MSG
# ---------------------------------------------------------------------------

def test_load_msg():
    docs = load_file(SAMPLE_DOCS / "msg_board_strategy_brief.msg")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "msg_board_strategy_brief.msg"
    assert docs[0].metadata["file_type"] == "msg"


# ---------------------------------------------------------------------------
# HTML / HTM — both normalised to file_type "html"
# ---------------------------------------------------------------------------

def test_load_html():
    docs = load_file(SAMPLE_DOCS / "annual_report_2024.html")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "annual_report_2024.html"
    assert docs[0].metadata["file_type"] == "html"


def test_load_htm():
    docs = load_file(SAMPLE_DOCS / "customer_support_faq.htm")
    assert len(docs) == 1
    assert docs[0].metadata["source"] == "customer_support_faq.htm"
    assert docs[0].metadata["file_type"] == "html"  # normalised to "html"


# ---------------------------------------------------------------------------
# Markdown — split by H2 sections
# ---------------------------------------------------------------------------

def test_load_md():
    docs = load_file(SAMPLE_DOCS / "api_developer_guide.md")
    assert len(docs) > 0
    for doc in docs:
        assert doc.page_content.strip() != ""
        assert doc.metadata["source"] == "api_developer_guide.md"
        assert doc.metadata["file_type"] == "md"


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------

def test_load_json():
    docs = load_file(SAMPLE_DOCS / "api_config_v3.json")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "api_config_v3.json"
    assert docs[0].metadata["file_type"] == "json"
    assert "item_count" in docs[0].metadata


# ---------------------------------------------------------------------------
# XML
# ---------------------------------------------------------------------------

def test_load_xml():
    docs = load_file(SAMPLE_DOCS / "product_catalog.xml")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "product_catalog.xml"
    assert docs[0].metadata["file_type"] == "xml"
    assert "root_tag" in docs[0].metadata


# ---------------------------------------------------------------------------
# RTF
# ---------------------------------------------------------------------------

def test_load_rtf():
    docs = load_file(SAMPLE_DOCS / "it_change_request_cr087.rtf")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "it_change_request_cr087.rtf"
    assert docs[0].metadata["file_type"] == "rtf"


# ---------------------------------------------------------------------------
# YAML / YML — both normalised to file_type "yaml"
# ---------------------------------------------------------------------------

def test_load_yaml():
    docs = load_file(SAMPLE_DOCS / "app_deployment_config.yaml")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "app_deployment_config.yaml"
    assert docs[0].metadata["file_type"] == "yaml"


def test_load_yml():
    docs = load_file(SAMPLE_DOCS / "monitoring_alert_rules.yml")
    assert len(docs) == 1
    assert docs[0].metadata["source"] == "monitoring_alert_rules.yml"
    assert docs[0].metadata["file_type"] == "yaml"  # normalised to "yaml"


# ---------------------------------------------------------------------------
# Image — requires Anthropic API key (skipped in CI without key)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not settings.anthropic_api_key, reason="Requires ANTHROPIC_API_KEY")
def test_load_image():
    docs = load_file(SAMPLE_DOCS / "employee_headcount_growth.png")
    assert len(docs) == 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"] == "employee_headcount_growth.png"
    assert docs[0].metadata["file_type"] == "image"
    assert docs[0].metadata["image_format"] == "png"


# ---------------------------------------------------------------------------
# Splitter
# ---------------------------------------------------------------------------

def test_split_adds_metadata():
    docs = load_file(SAMPLE_DOCS / "engineering_onboarding.txt")
    chunks = split_documents(docs)
    assert len(chunks) > 0
    assert "chunk_index" in chunks[0].metadata
    assert "total_chunks" in chunks[0].metadata
    assert chunks[0].metadata["total_chunks"] == len(chunks)


# ---------------------------------------------------------------------------
# Unsupported format
# ---------------------------------------------------------------------------

def test_unsupported_file_raises():
    with pytest.raises(ValueError, match="不支援"):
        load_file("test.xyz")
