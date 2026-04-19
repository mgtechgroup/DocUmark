# Python API Reference

You can use DocUmark as a library in your own Python projects.

## Import

```python
from documark import convert_file, optimize, encode_png, decode_png
from documark.security import check_file
from documark.bulk import bulk_convert
```

---

## `check_file(file_path, vt_api_key=None) -> dict`

Run the full security pre-check on a file.

```python
from documark.security import check_file

result = check_file("report.pdf", vt_api_key="your_vt_key")
# {"safe": True, "reason": "clean", "details": {...}}

result = check_file("malicious.txt")
# {"safe": False, "reason": "prompt injection detected: ignore_previous", "details": {...}}
```

**Returns:** `{"safe": bool, "reason": str, "details": dict}`

---

## `convert_file(file_path, output_dir=".") -> str`

Convert a single file to Markdown. **Does not run security check** — call `check_file()` first or use `bulk_convert()`.

```python
from documark import convert_file

md_path = convert_file("report.pdf", output_dir="./converted/")
# "./converted/report.md"
```

**Raises:** `ValueError` if the file extension is not supported.

---

## `bulk_convert(path, output_dir=".", recursive=False, vt_api_key=None, max_workers=4) -> dict`

Convert all supported files in a path. **Runs security check on every file.**

```python
from documark.bulk import bulk_convert

result = bulk_convert(
    "./documents/",
    output_dir="./markdown/",
    recursive=True,
    vt_api_key="your_key",
    max_workers=8,
)
# {"converted": ["./markdown/a.md"], "quarantined": ["./docs/bad.txt: injection..."], "errors": []}
```

---

## `optimize(md_text) -> str`

Normalize and clean a Markdown string.

```python
from documark import optimize

clean = optimize("##Badly   formatted heading\n\n\n\nText")
# "## Badly formatted heading\n\nText\n"
```

---

## `encode_png(md_path, output_dir, mode="visual") -> list[str]`

Encode a `.md` file as PNG dataset image(s).

```python
from documark import encode_png

paths = encode_png("report.md", "./dataset/", mode="visual")
# ["./dataset/report_visual_001.png"]

paths = encode_png("report.md", "./dataset/", mode="binary")
# ["./dataset/report_binary.png"]

paths = encode_png("report.md", "./dataset/", mode="both")
# ["./dataset/report_visual_001.png", "./dataset/report_binary.png"]
```

---

## `decode_png(png_path, output_dir=".") -> str`

Decode a binary-mode PNG back to a `.md` file.

```python
from documark import decode_png

md_path = decode_png("./dataset/report_binary.png", output_dir="./recovered/")
# "./recovered/report.md"
```

**Raises:** If pixel header is malformed (wrong PNG mode).
