def convert(file_path: str) -> str:
    with open(file_path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.splitlines()
    if lines:
        lines[0] = f"# {lines[0]}"
    return "\n".join(lines)
