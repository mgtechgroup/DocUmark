# DocUmark MCP Connector

DocUmark includes a built-in **MCP (Model Context Protocol) server** that
exposes its capabilities as tools callable by any AI platform that supports
the Model Context Protocol — including Claude Code, the Anthropic API, and
any other MCP-compatible AI system.

## Quick Start

### Claude Code

Add DocUmark to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "documark": {
      "command": "python",
      "args": ["-m", "documark.mcp_server"],
      "env": {
        "DOCUMARK_VT_API_KEY": "your_virustotal_key_here"
      }
    }
  }
}
```

Then in Claude Code, DocUmark tools are available immediately. You can ask Claude to:
- "Convert this PDF to Markdown"
- "Run a security check on this file"
- "Bulk convert my documents folder"

### Anthropic API (any Claude model)

Run the MCP server and connect via stdio transport:

```bash
# Terminal 1: start the server
python -m documark.mcp_server

# Or via CLI
documark serve-mcp
```

Connect using the Anthropic MCP client library or any stdio MCP client.

### Any MCP-Compatible AI Platform

DocUmark uses the standard `mcp` Python SDK and communicates over **stdio transport**.
Any platform that supports MCP stdio can connect directly.

## Available Tools

| Tool | Description |
|------|-------------|
| `convert_file` | Convert a single file to Markdown (security-scanned first) |
| `bulk_convert` | Convert all files in a folder (parallel, all security-scanned) |
| `encode_png` | Encode Markdown as PNG dataset (visual, binary, or both) |
| `decode_png` | Decode a binary-mode PNG back to Markdown |
| `security_check` | Run full security check (virus + injection) on any file |

## Tool Schemas

### `convert_file`

```json
{
  "file_path": "string (required) — absolute path to input file",
  "output_dir": "string (optional, default: '.') — output directory",
  "vt_api_key": "string (optional) — VirusTotal API key"
}
```

### `bulk_convert`

```json
{
  "path": "string (required) — file or directory path",
  "output_dir": "string (optional, default: '.')",
  "recursive": "boolean (optional, default: false)",
  "vt_api_key": "string (optional)"
}
```

### `encode_png`

```json
{
  "md_path": "string (required) — path to .md file",
  "output_dir": "string (optional, default: '.')",
  "mode": "string (optional) — 'visual', 'binary', or 'both'"
}
```

### `decode_png`

```json
{
  "png_path": "string (required) — path to binary PNG",
  "output_dir": "string (optional, default: '.')"
}
```

### `security_check`

```json
{
  "file_path": "string (required) — path to file to check",
  "vt_api_key": "string (optional)"
}
```

## Security

All MCP tools enforce the same security pipeline as the CLI:
- Virus scan via VirusTotal (requires `DOCUMARK_VT_API_KEY`)
- Prompt injection detection on all text content
- Automatic quarantine + logging of flagged files
- Fail-closed: tool errors return `{"error": "..."}` and block processing

There is **no way to bypass the security layer through the MCP interface**.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `DOCUMARK_VT_API_KEY` | VirusTotal API key for cloud-based virus scanning |

## Portability

DocUmark's MCP server is model-agnostic by design:
- No AI-provider-specific dependencies
- Standard JSON tool schemas (no proprietary extensions)
- Works over any stdio connection
- Compatible with: Claude Code, Anthropic API, any MCP stdio client

Future transport: HTTP/SSE for remote deployments.
