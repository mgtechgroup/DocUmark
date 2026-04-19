from documark.converters.pdf import convert as _pdf
from documark.converters.docx import convert as _docx
from documark.converters.txt import convert as _txt
from documark.converters.html import convert as _html

_REGISTRY: dict[str, callable] = {
    ".pdf": _pdf,
    ".docx": _docx,
    ".txt": _txt,
    ".html": _html,
    ".htm": _html,
}


def convert_file(file_path: str, output_dir: str = ".") -> str:
    import os
    from documark.optimizer import optimize
    from documark.organizer import write_md

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in _REGISTRY:
        raise ValueError(f"Unsupported format: {ext}")

    raw_md = _REGISTRY[ext](file_path)
    clean_md = optimize(raw_md)
    return write_md(clean_md, file_path, output_dir)
