import xml.etree.ElementTree as ET
from pathlib import Path
from langchain_core.documents import Document


def parse_xml(file_path: str | Path) -> list[Document]:
    file_path = Path(file_path)
    tree = ET.parse(str(file_path))
    root = tree.getroot()

    pieces = []
    for element in root.iter():
        if element.text and element.text.strip():
            pieces.append(element.text.strip())
        if element.tail and element.tail.strip():
            pieces.append(element.tail.strip())
        # Also capture attribute values for attribute-heavy XML (e.g. org charts)
        for attr_val in element.attrib.values():
            if attr_val.strip():
                pieces.append(attr_val.strip())

    if not pieces:
        raise ValueError(f"No text content found in XML file: {file_path.name}")

    text = "\n".join(pieces)

    return [Document(
        page_content=text,
        metadata={
            "source": file_path.name,
            "file_type": "xml",
            "page": 0,
            "root_tag": root.tag,
        },
    )]
