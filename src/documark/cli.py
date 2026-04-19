import os
import click
import documark
from documark.converters import convert_file
from documark.png_encoder import encode_png, decode_png
from documark.bulk import bulk_convert
from documark.security import check_file


@click.group()
@click.version_option(documark.__version__, prog_name="DocUmark")
def main() -> None:
    """DocUmark — security-first document converter for AI/ML pipelines."""


@main.command()
@click.argument("path")
@click.option("--output", default=".", help="Output directory")
@click.option("--recursive", is_flag=True, help="Recurse into subdirectories")
def convert(path: str, output: str, recursive: bool) -> None:
    """Convert a file or folder to Markdown (security-scanned)."""
    vt_key = os.environ.get("DOCUMARK_VT_API_KEY")
    if os.path.isdir(path):
        result = bulk_convert(path, output_dir=output, recursive=recursive, vt_api_key=vt_key)
        click.echo(f"Converted:    {len(result['converted'])} file(s)")
        click.echo(f"Quarantined:  {len(result['quarantined'])} file(s)")
        click.echo(f"Errors:       {len(result['errors'])} file(s)")
        for q in result["quarantined"]:
            click.echo(f"  [BLOCKED] {q}", err=True)
        for e in result["errors"]:
            click.echo(f"  [ERROR]   {e}", err=True)
    else:
        sec = check_file(path, vt_key)
        if not sec["safe"]:
            click.echo(f"BLOCKED: {sec['reason']}", err=True)
            raise SystemExit(1)
        out = convert_file(path, output)
        click.echo(f"Converted: {out}")


@main.command("security-check")
@click.argument("file_path")
def security_check_cmd(file_path: str) -> None:
    """Run a security check (virus + injection) on a file."""
    vt_key = os.environ.get("DOCUMARK_VT_API_KEY")
    result = check_file(file_path, vt_key)
    if result["safe"]:
        click.echo(f"Security check: PASS — {result['reason']}")
        for k, v in result["details"].items():
            click.echo(f"  {k}: {v}")
    else:
        click.echo(f"Security check: BLOCKED — {result['reason']}", err=True)
        raise SystemExit(1)


@main.command()
@click.argument("path")
@click.option("--mode", default="visual", type=click.Choice(["visual", "binary", "both"]))
@click.option("--output", default=".", help="Output directory")
def png(path: str, mode: str, output: str) -> None:
    """Encode Markdown file(s) as PNG dataset images."""
    if os.path.isdir(path):
        for fname in os.listdir(path):
            if fname.endswith(".md"):
                src = os.path.join(path, fname)
                for p in encode_png(src, output, mode):
                    click.echo(f"  Encoded: {p}")
    else:
        for p in encode_png(path, output, mode):
            click.echo(f"Encoded: {p}")


@main.command()
@click.argument("png_file")
@click.option("--output", default=".", help="Output directory")
def decode(png_file: str, output: str) -> None:
    """Decode a binary-mode PNG back to Markdown."""
    out = decode_png(png_file, output)
    click.echo(f"Decoded: {out}")


@main.command("serve-mcp")
def serve_mcp() -> None:
    """Start the DocUmark MCP server for AI platform integration."""
    from documark.mcp_server import main as mcp_main
    mcp_main()
