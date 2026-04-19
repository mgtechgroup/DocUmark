def convert(file_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(file_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    combined = "\n\n---\n\n".join(pages)
    title = (
        reader.metadata.title
        if reader.metadata and reader.metadata.title
        else "Document"
    )
    return f"# {title}\n\n{combined}"
