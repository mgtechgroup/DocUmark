import os


def write_md(md_text: str, source_path: str, output_dir: str) -> str:
    base = os.path.splitext(os.path.basename(source_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{base}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    return out_path
