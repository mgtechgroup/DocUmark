# DocUmark

> Security-first document conversion to optimized Markdown — ready for AI, LLMs, and ML pipelines.

---

> [!CAUTION]
> **SECURITY IS THE CORE STRUCTURE OF THIS PROJECT.**
>
> Every file processed by DocUmark is **virus-scanned, injection-checked, and size-validated** before any conversion occurs.
> Threats are **immediately quarantined, logged, and reported** to antivirus databases.
> DocUmark is **fail-closed** — scan errors block files rather than allowing them through.
> There are no bypass paths. See [SECURITY-ARCHITECTURE.md](docs/SECURITY-ARCHITECTURE.md) and [NOTICE.md](NOTICE.md) for full details.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![Security: Fail-Closed](https://img.shields.io/badge/security-fail--closed-critical.svg)](docs/SECURITY-ARCHITECTURE.md)
[![Injection Detection](https://img.shields.io/badge/injection-detection-red.svg)](docs/SECURITY-ARCHITECTURE.md)
[![Virus Scanned](https://img.shields.io/badge/virus-scanned-success.svg)](docs/SECURITY-ARCHITECTURE.md)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-blueviolet.svg)](docs/MCP-CONNECTOR.md)
[![GitHub Issues](https://img.shields.io/github/issues/mgtechgroup/DocUmark)](https://github.com/mgtechgroup/DocUmark/issues)

## What is DocUmark?

DocUmark is a **security-first** document and file conversion system with one goal: convert every file format into clean, optimized Markdown (`.md`) — universally readable by humans, LLMs, and AI/ML systems alike.

**Security is the core structure.** Every file is virus-scanned and checked for prompt injection before conversion. Threats are quarantined, logged, and reported to antivirus databases automatically.

Once converted, files can be:

- **Organized** — auto-structured into clean directory trees
- **Optimized** — formatted for maximum LLM token efficiency
- **Bulk processed** — parallel conversion of entire folder trees
- **Exported as PNG datasets** — visual renders or binary pixel-encoded text for multimodal AI training
- **Used by any AI** — via a built-in MCP server compatible with Claude Code and all MCP-enabled platforms

## Security Features

| Feature | Description |
|---------|-------------|
| Virus scanning | SHA-256 hash checked against VirusTotal API before conversion |
| Prompt injection detection | YARA-style patterns catch hidden instructions, RTL tricks, null bytes |
| Sandboxed quarantine | Flagged files moved to `~/.documark/quarantine/`, never processed |
| Structured logging | Every security event logged to `~/.documark/security.log` |
| AV reporting | Threats reported to VirusTotal for community benefit |
| Fail-closed design | Scan errors = blocked, never allowed through |
| Dependency auditing | `pip-audit` runs on install and in CI; Dependabot auto-updates |

## Supported Input Formats

| Format | Extension |
|--------|-----------|
| Plain Text | `.txt` |
| PDF | `.pdf` |
| Microsoft Word | `.docx` |
| HTML | `.html`, `.htm` |
| More coming | see [FORMATS.md](docs/FORMATS.md) |

## Quick Start

```bash
pip install documark
pip-audit  # always audit dependencies after install
```

```bash
# Convert a single file (virus-scanned + injection-checked automatically)
documark convert report.pdf

# Bulk convert an entire folder (parallel, every file security-scanned)
documark convert ./documents/ --output ./markdown/ --recursive

# Run security check only (no conversion)
documark security-check ./suspicious-file.pdf

# Export as PNG dataset (visual rendered pages)
documark png ./markdown/ --mode visual --output ./dataset/

# Export as PNG dataset (binary pixel-encoded, lossless)
documark png ./markdown/ --mode binary --output ./dataset/

# Start MCP server for AI platform integration (Claude Code, etc.)
documark serve-mcp
```

## MCP Integration (Claude Code & all AI platforms)

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "documark": {
      "command": "python",
      "args": ["-m", "documark.mcp_server"],
      "env": {
        "DOCUMARK_VT_API_KEY": "your_virustotal_key"
      }
    }
  }
}
```

See [MCP-CONNECTOR.md](docs/MCP-CONNECTOR.md) for full integration guide.

## Security Pipeline (always active — cannot be disabled)

```
Every Input File
       |
       v
[1] Size Check  ─────────── > 50 MB ─────────────────┐
       |                                               |
       v                                               v
[2] Extension Block ─── .exe/.dll/.bat/etc ──────► QUARANTINE
       |                                               +
       v                                            LOG EVENT
[3] MIME Type Check ─── dangerous MIME ──────────► REPORT TO VT
       |
       v
[4] VirusTotal Hash ─── malicious/suspicious ────────►
       |
       v
[5] Prompt Injection ─── pattern match ──────────────►
       |
       v
   SAFE — Convert
```

All quarantine events are logged to `~/.documark/security.log`.
Threats are reported to VirusTotal when `DOCUMARK_VT_API_KEY` is set.
See [NOTICE.md](NOTICE.md) for the full security notice.

## Security Stats (Python API)

```python
from documark.security import security_stats
print(security_stats())
# {"total_quarantined": 3, "virus_malware": 1, "prompt_injection": 2, "scan_error": 0}
```

## Documentation

- [Security Notice](NOTICE.md) — **read first**
- [Security Architecture](docs/SECURITY-ARCHITECTURE.md)
- [Installation](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Supported Formats](docs/FORMATS.md)
- [PNG Datasets](docs/PNG-DATASETS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [MCP Connector](docs/MCP-CONNECTOR.md)
- [API Reference](docs/API.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All skill levels welcome.
Security improvements and new injection pattern submissions are especially valued.

## License

[MIT](LICENSE.md) © 2026 mgtechgroup
