# Installation

## Requirements

- Python 3.13 or higher
- pip

## Install from PyPI (once published)

```bash
pip install documark
pip-audit  # verify no known CVEs in dependencies
```

## Install from Source

```bash
git clone https://github.com/mgtechgroup/DocUmark.git
cd DocUmark
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pip-audit                      # always audit after install
```

## Verify Installation

```bash
documark --version
```

Expected output: `DocUmark 0.1.0`

## Optional: VirusTotal API Key

For cloud-based virus scanning, set your VirusTotal API key:

```bash
# Linux/macOS
export DOCUMARK_VT_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:DOCUMARK_VT_API_KEY = "your_api_key_here"
```

Get a free API key at [virustotal.com](https://www.virustotal.com/).

Without a key, DocUmark uses local heuristics (extension blocking) only.

## Dependencies

| Package | Purpose |
|---------|---------|
| `pypdf` | PDF text extraction |
| `python-docx` | DOCX parsing |
| `markdown-it-py` | Markdown rendering |
| `Pillow` | PNG image generation |
| `click` | CLI framework |
| `requests` | VirusTotal API calls |
| `mcp` | MCP server for AI platform integration |

Dev dependencies: `pytest`, `pytest-asyncio`, `ruff`, `pip-audit`

## Keeping Dependencies Updated

DocUmark uses Dependabot to auto-create PRs for weekly dependency updates.
To manually update and audit:

```bash
pip install --upgrade -e ".[dev]"
pip-audit --strict
```
