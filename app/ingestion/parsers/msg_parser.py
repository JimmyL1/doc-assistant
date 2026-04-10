from pathlib import Path

from langchain_core.documents import Document


def parse_msg(file_path: str | Path) -> list[Document]:
    import extract_msg

    file_path = Path(file_path)
    with extract_msg.openMsg(str(file_path)) as msg:
        sender = msg.sender or ""
        to = msg.to or ""
        subject = msg.subject or ""
        date = str(msg.date) if msg.date is not None else ""
        body = msg.body or ""

    content = (
        f"From: {sender}\n"
        f"To: {to}\n"
        f"Subject: {subject}\n"
        f"Date: {date}\n"
        f"\n"
        f"{body}"
    )

    return [Document(
        page_content=content,
        metadata={"source": file_path.name, "file_type": "msg", "page": 0},
    )]
