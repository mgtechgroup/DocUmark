# DocUmark Architecture

## Overview

```
Input Files (bulk or single: PDF, DOCX, TXT, HTML, ...)
        │
        ▼
┌─────────────────────────┐
│    Security Layer       │  src/documark/security/
│  (pre-processing gate)  │  scanner.py   → VirusTotal API hash check
│                         │  injection.py → YARA-style pattern detection
│                         │  quarantine.py → sandboxed isolation + log
│                         │  reporter.py  → VirusTotal AV reporting
└────────┬────────────────┘
         │ CLEAN only (fail-closed: errors = blocked)
         ▼
┌─────────────────────────┐
│    Bulk Processor       │  src/documark/bulk.py
│  (parallel batch)       │  ThreadPoolExecutor, recursive dir walk
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│    Converter Layer      │  src/documark/converters/
│  (format parsers)       │  pdf.py | docx.py | txt.py | html.py
└────────┬────────────────┘
         │  raw Markdown string
         ▼
┌─────────────────────────┐
│    Optimizer Layer      │  src/documark/optimizer.py
│  (clean + normalize)    │  headings, whitespace, lists
└────────┬────────────────┘
         │  clean .md string
         ▼
┌─────────────────────────┐
│    Organizer Layer      │  src/documark/organizer.py
│  (file output)          │  writes .md, mirrors directory structure
└────────┬────────────────┘
         │  .md files on disk
         ▼
┌─────────────────────────┐
│    PNG Encoder          │  src/documark/png_encoder.py
│  (optional step)        │  visual render OR binary pixel encoding
└─────────────────────────┘
         │
         ▼
    PNG Dataset Files

         ▲ (all above accessible via)
┌─────────────────────────┐
│    MCP Server           │  src/documark/mcp_server.py
│  (AI platform bridge)   │  Claude Code / Anthropic API / any MCP client
└─────────────────────────┘
```

## Security Layer (Fail-Closed)

All files enter via `check_file()` in `src/documark/security/__init__.py`.
Any exception during scanning → file is blocked (never allowed through).

1. **`scanner.py`** — SHA-256 hash lookup on VirusTotal API v3. Falls back to dangerous-extension heuristics without API key.
2. **`injection.py`** — Regex + YARA-style rules detect prompt injection, hidden instructions, Unicode tricks, exfiltration attempts.
3. **`quarantine.py`** — Moves flagged file to `~/.documark/quarantine/`. Appends structured JSON event to `~/.documark/security.log`.
4. **`reporter.py`** — Submits hash/file to VirusTotal. Logs report outcome to `~/.documark/reports.log`.

## Converter Layer

Each converter exports a single function:

```python
def convert(file_path: str) -> str:
    """Return the file contents as a raw Markdown string."""
```

The `__init__.py` registry maps extensions → converter functions.

## Optimizer Layer

`optimizer.py` normalizes raw Markdown:
- Collapses 3+ blank lines to 2
- Strips trailing whitespace from all lines
- Fixes heading spacing (`##Title` → `## Title`)
- Normalizes line endings
- Always ends with a single trailing newline

## Bulk Processor

`bulk.py` collects all supported files from a path (optionally recursive),
runs `check_file()` on each, then dispatches clean files to `convert_file()`
using `ThreadPoolExecutor`. Returns `{"converted", "quarantined", "errors"}` counts.

## PNG Encoder

Two modes, both lossless PNG:

### Visual Mode
Renders Markdown lines as text on a white canvas using Pillow.
Multi-page: numbered `_001.png`, `_002.png`, etc.
Use case: vision-language model training, OCR datasets.

### Binary Mode
Encodes raw UTF-8 bytes into RGB pixel values (3 bytes/pixel).
Header pixel `(0,0)` stores total byte count.
Fully recoverable via `decode_png()`.
Use case: compact lossless text storage, binary dataset archives.

## MCP Server

`mcp_server.py` wraps all DocUmark capabilities as MCP tools over stdio.
Runs as a subprocess; any MCP-compatible AI platform can connect.
All tools enforce the security layer — no bypass possible via MCP.
