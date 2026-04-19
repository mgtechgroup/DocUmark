# DocUmark Security Architecture

## Core Principle: Fail-Closed

Every input file **must pass all security checks** before conversion begins.
Scan failures -> file is **BLOCKED**. There are no loopholes or fallback paths.

## Security Pipeline

```
Input File
    |
    v
[1] Virus / Malware Scan ---- FAIL ---> Quarantine + Log + Report to VirusTotal
    | PASS
    v
[2] Prompt Injection Detection -- FAIL ---> Quarantine + Log
    | PASS
    v
[3] Converter (safe file only)
```

If ANY step throws an exception -> treated as FAIL -> file is quarantined.

## Virus Scanning (`scanner.py`)

DocUmark uses **VirusTotal API v3** (when `DOCUMARK_VT_API_KEY` is set):

1. SHA-256 hash of the file is computed locally
2. Hash is looked up in VirusTotal's database
3. If flagged by any engine -> BLOCKED + quarantined + reported
4. If not in VT database -> file is uploaded for asynchronous scanning -> treated as **pending = BLOCKED** (fail-closed)
5. If VT returns clean -> cached in-memory for session

Without a VT key: dangerous extensions (`.exe`, `.dll`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.js`, `.jar`, `.sh`) are blocked locally.

**Set your API key:**

```bash
export DOCUMARK_VT_API_KEY=your_virustotal_api_key
```

## Prompt Injection Detection (`injection.py`)

YARA-style regex rules detect known attack patterns:

| Pattern Name | What it catches |
|---------|----------------|
| `ignore_previous` | "Ignore all previous instructions" variants |
| `system_override` | "You are now / Act as / Pretend you are [AI]" |
| `jailbreak_dan` | DAN-style jailbreak patterns |
| `hidden_instruction` | HTML comments containing override instructions |
| `base64_instruction` | Code evaluation or base64 decode calls embedded in documents |
| `exfiltration_attempt` | Network fetch commands plus a URL embedded in document text |
| `role_hijack` | "Your new role is..." / "From now on you..." |
| `token_smuggling` | Special token patterns used to inject model-level tokens |
| `null_byte` | Null byte injection (`\x00`) |
| `rtl_override` | Unicode RTL override characters (invisible text attacks) |

New patterns can be added to `_INJECTION_PATTERNS` in `injection.py`.
Each new pattern requires a test in `tests/test_security.py`.

## Quarantine (`quarantine.py`)

When a file is flagged:

1. **Moved** to `~/.documark/quarantine/<timestamp>_<filename>` (sandbox — never processed)
2. **Logged** to `~/.documark/security.log` as a structured JSON line:
   ```json
   {
     "timestamp": "2026-04-19T12:00:00+00:00",
     "original_path": "/path/to/file.pdf",
     "quarantine_path": "~/.documark/quarantine/1745000000_file.pdf",
     "reason": {"detected": true, "pattern": "ignore_previous", "matches": [...]}
   }
   ```
3. **Reported** to VirusTotal (if API key is set)

The quarantine directory is never scanned for conversion — files there are permanently isolated.

## AV Reporting (`reporter.py`)

Threats are reported to VirusTotal:
- File hash is submitted for community analysis
- If not already in VT database, the file is uploaded
- Report outcome is logged to `~/.documark/reports.log`

Future planned integrations: MISP, AbuseIPDB.

## Dependency Security

- All dependencies pinned in `pyproject.toml`
- `pip-audit` scans for known CVEs — runs in CI and can be run manually
- Dependabot configured to auto-create PRs for weekly updates
- CI blocks merges if `pip-audit` finds Critical/High CVEs

## Log Files

| File | Contents |
|------|---------|
| `~/.documark/security.log` | All quarantine events (JSON lines) |
| `~/.documark/reports.log` | All VirusTotal report submissions |

## Threat Model

| Threat | Mitigation |
|--------|-----------|
| Malicious document (virus/malware) | VirusTotal hash check + extension blocking |
| Prompt injection in document text | YARA-style pattern detection |
| Hidden Unicode tricks | RTL override + null byte detection |
| Poisoned training dataset | Pre-conversion scanning; only clean files converted |
| Supply chain attack (deps) | pip-audit + Dependabot weekly updates |
| Scan bypass attempt | Fail-closed: exceptions = blocked |
| MCP bypass attempt | MCP tools enforce the same security pipeline |
