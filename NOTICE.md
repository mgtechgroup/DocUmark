# DocUmark Security Notice

> **This notice applies to all users, contributors, and AI systems interacting with DocUmark.**

---

## Security Is The Core Structure

DocUmark is a document processing system that handles untrusted input files from
any source. Security is not an optional layer — it is the **foundational architecture**
of every component in this system.

**All file processing is fail-closed.**
If a security check cannot be completed, the file is blocked. There is no fallback
path that allows an unscanned file through.

---

## What DocUmark Protects Against

### 1. Malicious Documents (Viruses, Malware)
Every input file is:
- **Size-checked** — files over 50 MB are blocked (DoS prevention)
- **Extension-blocked** — executables, scripts, and binaries are always rejected
- **MIME-type-checked** — file type is validated independently of extension
- **Hash-checked against VirusTotal** — SHA-256 compared against millions of known threats

### 2. Prompt Injection Attacks
Documents may contain hidden text designed to hijack AI systems that process them.
DocUmark detects and blocks:
- "Ignore all previous instructions" variants
- Role/identity hijacking ("You are now...", "Act as...")
- Hidden HTML comment instructions
- Unicode RTL override characters (invisible text attacks)
- Null byte injection
- Token smuggling patterns (`<|token|>`)
- Data exfiltration URL patterns
- Code execution patterns embedded in document text

### 3. Poisoned AI/ML Datasets
When building training datasets, a single malicious document can corrupt an entire
dataset or embed adversarial examples. DocUmark's pre-conversion security gate
ensures only verified-clean content reaches the Markdown output and PNG encoder.

---

## What Happens When a Threat Is Detected

1. **Immediate stop** — processing halts; the file never reaches any converter
2. **Quarantine** — file is moved to `~/.documark/quarantine/` (sandboxed, never processed)
3. **Structured log** — event recorded in `~/.documark/security.log` (JSON, permanent)
4. **AV report** — file hash submitted to VirusTotal for community benefit (if API key set)

---

## Security Responsibilities

### Users
- Keep DocUmark and all dependencies updated: `pip install --upgrade documark && pip-audit`
- Set `DOCUMARK_VT_API_KEY` for cloud-based virus scanning (get a free key at virustotal.com)
- Review `~/.documark/security.log` regularly
- Report security vulnerabilities privately — see [SECURITY.md](SECURITY.md)

### Contributors
- **Never bypass `check_file()`** — all file processing must enter through the security gate
- New converters must not execute embedded scripts, macros, or external commands
- New injection patterns require a test in `tests/test_security.py` before merging
- Do not add network calls that could exfiltrate file content
- Dependency additions require `pip-audit` approval in CI

### AI Systems Using DocUmark via MCP
- The MCP server enforces the same security pipeline as the CLI — no bypass is possible
- All tool calls that process files will run `check_file()` before any conversion
- Quarantined files are never returned as output — the tool returns an error instead

---

## Known Limitations

| Limitation | Status |
|-----------|--------|
| VirusTotal requires API key for cloud scanning | Free key available at virustotal.com |
| New/zero-day malware not in VT database | File submitted to VT; blocked pending scan (fail-closed) |
| Local heuristic (no API key) is extension/MIME only | Upgrade: set DOCUMARK_VT_API_KEY |
| Injection patterns are regex-based | YARA rule support planned for v0.2.0 |
| Binary files (DOCX, PDF) read as UTF-8 for injection scan | False negatives possible for binary-encoded injections |

---

## Reporting Security Issues

**Do NOT open a public GitHub issue for security vulnerabilities.**

Use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) or see [SECURITY.md](SECURITY.md).

---

## Version

This notice applies to DocUmark v0.1.0 and all subsequent versions until superseded.
Last updated: 2026-04-19
