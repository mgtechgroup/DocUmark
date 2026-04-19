import math
import os
from PIL import Image, ImageDraw, ImageFont


def encode_png(md_path: str, output_dir: str, mode: str = "visual") -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    results: list[str] = []
    if mode in ("visual", "both"):
        results.extend(_encode_visual(md_text, base, output_dir))
    if mode in ("binary", "both"):
        results.append(_encode_binary(md_text, base, output_dir))
    return results


def decode_png(png_path: str, output_dir: str = ".") -> str:
    img = Image.open(png_path).convert("RGB")
    pixels = list(img.get_flattened_data())
    header = pixels[0]
    total_bytes = (header[0] << 16) | (header[1] << 8) | header[2]
    byte_data: list[int] = []
    for r, g, b in pixels[1:]:
        byte_data.extend([r, g, b])
        if len(byte_data) >= total_bytes:
            break
    text = bytes(byte_data[:total_bytes]).decode("utf-8")
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(png_path))[0].replace("_binary", "")
    out_path = os.path.join(output_dir, f"{base}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path


def _encode_binary(md_text: str, base: str, output_dir: str) -> str:
    raw = md_text.encode("utf-8")
    total = len(raw)
    side = math.ceil(math.sqrt((total + 3) / 3)) + 1
    pixels = [(0, 0, 0)] * (side * side)
    pixels[0] = ((total >> 16) & 0xFF, (total >> 8) & 0xFF, total & 0xFF)
    for i in range(0, total, 3):
        chunk = raw[i : i + 3]
        r = chunk[0] if len(chunk) > 0 else 0
        g = chunk[1] if len(chunk) > 1 else 0
        b = chunk[2] if len(chunk) > 2 else 0
        pixels[1 + i // 3] = (r, g, b)
    img = Image.new("RGB", (side, side))
    img.putdata(pixels)
    out_path = os.path.join(output_dir, f"{base}_binary.png")
    img.save(out_path, "PNG")
    return out_path


def _encode_visual(md_text: str, base: str, output_dir: str) -> list[str]:
    width, height = 1200, 1600
    font_size = 18
    margin = 60
    line_height = font_size + 6
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    lines = md_text.splitlines()
    max_lines_per_page = (height - 2 * margin) // line_height
    pages = [
        lines[i : i + max_lines_per_page]
        for i in range(0, max(1, len(lines)), max_lines_per_page)
    ]

    paths: list[str] = []
    for idx, page_lines in enumerate(pages, 1):
        img = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        y = margin
        for line in page_lines:
            draw.text((margin, y), line, fill=(20, 20, 20), font=font)
            y += line_height
        suffix = f"_{idx:03d}" if len(pages) > 1 else ""
        out_path = os.path.join(output_dir, f"{base}_visual{suffix}.png")
        img.save(out_path, "PNG")
        paths.append(out_path)
    return paths
