"""
DocUmark MCP Server — exposes DocUmark as AI-callable tools via the
Model Context Protocol (MCP). Compatible with Claude Code and any
MCP stdio client.

Run: python -m documark.mcp_server
or:  documark serve-mcp
"""
import asyncio
import json
import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from documark.bulk import bulk_convert
from documark.security import check_file
from documark.png_encoder import encode_png, decode_png
from documark.converters import convert_file

app = Server("documark")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_file",
            description="Convert a single document (PDF, DOCX, TXT, HTML) to Markdown. Security-scanned before conversion.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the input file"},
                    "output_dir": {"type": "string", "description": "Output directory for the .md file", "default": "."},
                    "vt_api_key": {"type": "string", "description": "VirusTotal API key (optional)"},
                },
                "required": ["file_path"],
            },
        ),
        types.Tool(
            name="bulk_convert",
            description="Convert all supported documents in a folder to Markdown. Each file is security-scanned. Returns converted/quarantined/error counts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File or directory path"},
                    "output_dir": {"type": "string", "description": "Output directory", "default": "."},
                    "recursive": {"type": "boolean", "description": "Recurse into subdirectories", "default": False},
                    "vt_api_key": {"type": "string", "description": "VirusTotal API key (optional)"},
                },
                "required": ["path"],
            },
        ),
        types.Tool(
            name="encode_png",
            description="Encode a Markdown file as PNG dataset image(s). Modes: visual (rendered page), binary (pixel-encoded text), or both.",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_path": {"type": "string", "description": "Path to the .md file"},
                    "output_dir": {"type": "string", "description": "Output directory for PNGs", "default": "."},
                    "mode": {"type": "string", "enum": ["visual", "binary", "both"], "default": "visual"},
                },
                "required": ["md_path"],
            },
        ),
        types.Tool(
            name="decode_png",
            description="Decode a binary-mode PNG back to Markdown (lossless).",
            inputSchema={
                "type": "object",
                "properties": {
                    "png_path": {"type": "string", "description": "Path to the binary PNG"},
                    "output_dir": {"type": "string", "description": "Output directory for recovered .md", "default": "."},
                },
                "required": ["png_path"],
            },
        ),
        types.Tool(
            name="security_check",
            description="Run a full security check (virus scan + prompt injection detection) on a file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file to check"},
                    "vt_api_key": {"type": "string", "description": "VirusTotal API key (optional)"},
                },
                "required": ["file_path"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        vt_key = arguments.get("vt_api_key") or os.environ.get("DOCUMARK_VT_API_KEY")

        if name == "convert_file":
            sec = check_file(arguments["file_path"], vt_key)
            if not sec["safe"]:
                return [types.TextContent(type="text", text=json.dumps({"error": "file_blocked", "reason": sec["reason"]}))]
            result = convert_file(arguments["file_path"], arguments.get("output_dir", "."))
            return [types.TextContent(type="text", text=json.dumps({"output": result}))]

        elif name == "bulk_convert":
            result = bulk_convert(
                arguments["path"],
                output_dir=arguments.get("output_dir", "."),
                recursive=arguments.get("recursive", False),
                vt_api_key=vt_key,
            )
            return [types.TextContent(type="text", text=json.dumps(result))]

        elif name == "encode_png":
            paths = encode_png(
                arguments["md_path"],
                arguments.get("output_dir", "."),
                arguments.get("mode", "visual"),
            )
            return [types.TextContent(type="text", text=json.dumps({"outputs": paths}))]

        elif name == "decode_png":
            path = decode_png(arguments["png_path"], arguments.get("output_dir", "."))
            return [types.TextContent(type="text", text=json.dumps({"output": path}))]

        elif name == "security_check":
            result = check_file(arguments["file_path"], vt_key)
            return [types.TextContent(type="text", text=json.dumps(result))]

        else:
            return [types.TextContent(type="text", text=json.dumps({"error": f"unknown tool: {name}"}))]

    except Exception as exc:
        return [types.TextContent(type="text", text=json.dumps({"error": str(exc)}))]


async def _main() -> None:
    async with stdio_server() as streams:
        await app.run(*streams, app.create_initialization_options())


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
