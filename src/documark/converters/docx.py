def convert(file_path: str) -> str:
    from docx import Document

    doc = Document(file_path)
    lines: list[str] = []
    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()
        if not text:
            lines.append("")
            continue
        if style.startswith("Heading 1"):
            lines.append(f"# {text}")
        elif style.startswith("Heading 2"):
            lines.append(f"## {text}")
        elif style.startswith("Heading 3"):
            lines.append(f"### {text}")
        else:
            lines.append(text)
    return "\n\n".join(lines)
