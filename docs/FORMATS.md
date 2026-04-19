# Supported File Formats

## Input Formats

| Format | Extension(s) | Status | Converter |
|--------|-------------|--------|-----------|
| Plain Text | `.txt` | Stable | `converters/txt.py` |
| PDF | `.pdf` | Stable | `converters/pdf.py` |
| Microsoft Word | `.docx` | Stable | `converters/docx.py` |
| HTML | `.html`, `.htm` | Stable | `converters/html.py` |
| Rich Text Format | `.rtf` | Planned | — |
| OpenDocument Text | `.odt` | Planned | — |
| Markdown (passthrough) | `.md` | Stable | optimizer only |
| CSV / TSV | `.csv`, `.tsv` | Planned | — |
| JSON | `.json` | Planned | — |
| EPUB | `.epub` | Planned | — |

## Security: Blocked Extensions

These extensions are always blocked regardless of API key status:

| Extension | Reason |
|-----------|--------|
| `.exe` | Executable binary |
| `.dll` | Dynamic library |
| `.bat` | Windows batch script |
| `.cmd` | Windows command script |
| `.ps1` | PowerShell script |
| `.vbs` | VBScript |
| `.js` | JavaScript (standalone) |
| `.jar` | Java executable |
| `.sh` | Shell script |

## Output Format

All conversions produce `.md` files following the
[CommonMark specification](https://commonmark.org/).

## PNG Dataset Formats

| Mode | Output | Description |
|------|--------|-------------|
| Visual | `.png` (RGB image) | Rendered markdown as a formatted page image |
| Binary | `.png` (RGB image) | Raw UTF-8 text encoded into pixel R/G/B channels |

Both produce valid `.png` files. Binary-mode PNGs are losslessly decodable back to the original `.md`.

## Adding Support for a New Format

See the [Contributing Guide](../CONTRIBUTING.md#adding-a-new-converter).
