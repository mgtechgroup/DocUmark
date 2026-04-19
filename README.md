# DocUmark

> Security-first document conversion to optimized Markdown — ready for AI, LLMs, and ML pipelines.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![Security: Fail-Closed](https://img.shields.io/badge/security-fail--closed-red.svg)](docs/SECURITY-ARCHITECTURE.md)
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
```

```bash
# Convert a single file (security-scanned automatically)
documark convert report.pdf

# Bulk convert an entire folder (parallel, all files security-scanned)
documark convert ./documents/ --output ./markdown/ --recursive

# Export as PNG dataset (visual)
documark png ./markdown/ --mode visual --output ./dataset/

# Export as PNG dataset (binary pixel-encoded)
documark png ./markdown/ --mode binary --output ./dataset/

# Run security check only
documark security-check ./suspicious-file.pdf

# Start MCP server for AI platform integration
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

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Supported Formats](docs/FORMATS.md)
- [PNG Datasets](docs/PNG-DATASETS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Security Architecture](docs/SECURITY-ARCHITECTURE.md)
- [MCP Connector](docs/MCP-CONNECTOR.md)
- [API Reference](docs/API.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All skill levels welcome.

## License

[MIT](LICENSE.md) © 2026 mgtechgroup
