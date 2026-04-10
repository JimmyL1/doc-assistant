import email
import email.header
import re
from pathlib import Path

from langchain_core.documents import Document


def _decode_header(value: str) -> str:
    """Decode an RFC 2047-encoded header value to a plain string."""
    parts = email.header.decode_header(value)
    decoded = []
    for chunk, charset in parts:
        if isinstance(chunk, bytes):
            decoded.append(chunk.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(chunk)
    return "".join(decoded)


def parse_eml(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    raw = file_path.read_bytes()
    msg = email.message_from_bytes(raw)

    from_header = _decode_header(msg.get("From", ""))
    to_header = _decode_header(msg.get("To", ""))
    subject_header = _decode_header(msg.get("Subject", ""))
    date_header = msg.get("Date", "")

    body = ""
    if msg.is_multipart():
        plain_part = None
        html_part = None
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain" and plain_part is None:
                plain_part = part
            elif ct == "text/html" and html_part is None:
                html_part = part
        chosen = plain_part or html_part
        if chosen is not None:
            payload = chosen.get_payload(decode=True)
            charset = chosen.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace") if isinstance(payload, bytes) else (payload or "")
            if chosen.get_content_type() == "text/html":
                text = re.sub(r"<[^>]+>", "", text)
            body = text
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or "utf-8"
        text = payload.decode(charset, errors="replace") if isinstance(payload, bytes) else (payload or "")
        if msg.get_content_type() == "text/html":
            text = re.sub(r"<[^>]+>", "", text)
        body = text

    content = (
        f"From: {from_header}\n"
        f"To: {to_header}\n"
        f"Subject: {subject_header}\n"
        f"Date: {date_header}\n"
        f"\n"
        f"{body}"
    )

    return [Document(
        page_content=content,
        metadata={"source": file_path.name, "file_type": "eml", "page": 0},
    )]
