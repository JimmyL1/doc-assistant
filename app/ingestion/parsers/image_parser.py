from pathlib import Path
import base64
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from config.settings import settings

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

_MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def parse_image(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    media_type = _MEDIA_TYPES.get(suffix, "image/png")

    # Read image and encode as base64 for the vision API
    with open(file_path, "rb") as f:
        image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    # Use Claude Vision to extract a text description suitable for RAG indexing
    llm = ChatAnthropic(model=settings.llm_model, api_key=settings.anthropic_api_key, max_tokens=1024)
    message = HumanMessage(content=[
        {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": image_b64},
        },
        {
            "type": "text",
            "text": (
                "請詳細描述這張圖片的所有內容，包括：\n"
                "1. 所有可見的文字、標題、標籤\n"
                "2. 圖表數據與數值\n"
                "3. 技術規格、元件名稱、連線關係\n"
                "4. 圖例說明\n"
                "請用繁體中文回答，盡量保留所有細節，以便後續語意搜尋。"
            ),
        },
    ])

    response = llm.invoke([message])
    description = response.content if isinstance(response.content, str) else str(response.content)

    return [Document(
        page_content=description,
        metadata={
            "source": file_path.name,
            "file_type": "image",
            "image_format": suffix.lstrip("."),
            "page": 0,
        },
    )]
