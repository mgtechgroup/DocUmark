# Usage Guide

All file operations are security-scanned automatically before processing.

## Convert a Single File

```bash
documark convert report.pdf
```

Output: `report.md` in the current directory.

## Convert with Custom Output Path

```bash
documark convert report.pdf --output ./converted/
```

## Bulk Convert an Entire Folder

```bash
documark convert ./documents/ --output ./markdown/
```

DocUmark mirrors the source directory structure in the output.
All files are security-scanned before conversion; unsafe files are quarantined.

## Recursive Bulk Convert

```bash
documark convert ./documents/ --output ./markdown/ --recursive
```

## Run Security Check Only (no conversion)

```bash
documark security-check ./suspicious-file.pdf
```

Output:

```
Security check: PASS — clean
  engine: virustotal
  sha256: abc123...
```

Or if flagged:

```
Security check: BLOCKED — prompt injection detected: ignore_previous
  File quarantined to: ~/.documark/quarantine/1745000000_suspicious-file.pdf
  Logged to: ~/.documark/security.log
```

## View Security Log

```bash
cat ~/.documark/security.log
```

Each line is a structured JSON event:

```json
{"timestamp": "2026-04-19T12:00:00+00:00", "original_path": "/tmp/bad.txt", "quarantine_path": "~/.documark/quarantine/...", "reason": {...}}
```

## Export as PNG Dataset — Visual Mode

Renders each `.md` file as a formatted PNG image page.

```bash
documark png ./markdown/ --mode visual --output ./dataset/
```

## Export as PNG Dataset — Binary Mode

Encodes the raw text of each `.md` file into PNG pixel data (lossless).

```bash
documark png ./markdown/ --mode binary --output ./dataset/
```

## Both PNG Modes at Once

```bash
documark png ./markdown/ --mode both --output ./dataset/
```

## Decode Binary PNG back to Markdown

```bash
documark decode ./dataset/report_binary.png --output ./recovered/
```

## Start MCP Server (AI Platform Integration)

```bash
documark serve-mcp
```

This starts the DocUmark MCP server over stdio.
See [MCP-CONNECTOR.md](MCP-CONNECTOR.md) for AI platform setup.

## All CLI Options

```
documark convert [OPTIONS] PATH

  Options:
    --output PATH    Output directory (default: current dir)
    --recursive      Convert subdirectories recursively
    --help           Show this message and exit.

documark security-check [OPTIONS] FILE_PATH

  Options:
    --help           Show this message and exit.

documark png [OPTIONS] PATH

  Options:
    --mode [visual|binary|both]  PNG encoding mode (default: visual)
    --output PATH                Output directory
    --help                       Show this message and exit.

documark decode [OPTIONS] PNG_FILE

  Options:
    --output PATH    Output directory for recovered .md file
    --help           Show this message and exit.

documark serve-mcp

  Starts the DocUmark MCP server for AI platform integration.
```
