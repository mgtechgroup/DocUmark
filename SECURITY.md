# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report security issues directly by using
[GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You will receive a response within 72 hours.

## Security Architecture

DocUmark enforces a **fail-closed** security model:

- All input files are virus-scanned (VirusTotal API) before conversion
- Prompt injection patterns are detected and blocked
- Flagged files are quarantined to `~/.documark/quarantine/`
- All security events are logged to `~/.documark/security.log`
- Threats are reported to VirusTotal for community benefit
- Scan errors block the file — errors never allow files through

See [docs/SECURITY-ARCHITECTURE.md](docs/SECURITY-ARCHITECTURE.md) for full details.

## Dependency Security

- Dependencies are pinned and audited with `pip-audit`
- Dependabot auto-creates PRs for dependency updates weekly
- CI runs `pip-audit --strict` on every push to `main`
