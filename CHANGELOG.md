# Changelog

All notable changes to DocUmark will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
DocUmark follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial project scaffold
- Security layer: virus scanning (VirusTotal API), prompt injection detection, sandboxed quarantine, AV reporting
- PDF, DOCX, TXT, HTML → Markdown converters
- Markdown optimizer and formatter
- File organizer with directory mirroring
- Bulk upload and parallel conversion system with security pre-pass
- PNG dataset encoder (visual rendering and binary pixel-encoding modes)
- Binary PNG decoder (lossless roundtrip)
- CLI via `click` with `convert`, `bulk`, `png`, `decode`, `security-check`, `serve-mcp` commands
- MCP server for AI platform integration (Claude Code, Anthropic API, all MCP clients)
- Auto-update dependency system: Dependabot + pip-audit CI
- Fail-closed security design (scan errors block files, never allow through)

---

## [0.1.0] — 2026-04-19

- Initial release
