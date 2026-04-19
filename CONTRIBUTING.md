# Contributing to DocUmark

Thank you for your interest in contributing! All skill levels are welcome.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/DocUmark.git
   cd DocUmark
   ```
3. Set up the dev environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```
4. Create a feature branch:
   ```bash
   git checkout -b feat/my-feature
   ```

## Running Tests

```bash
pytest tests/ -v
```

All tests must pass before submitting a PR.

## Security Requirements

DocUmark enforces strict security standards. All contributors must:

- Never bypass the security layer — all file processing must go through `check_file()`
- Not add any network calls that could exfiltrate file content
- Report suspected vulnerabilities privately (see [SECURITY.md](SECURITY.md))
- Ensure new converters do not execute embedded scripts or macros

## Pull Request Guidelines

- One feature or fix per PR
- Include tests for new functionality
- Update relevant `.md` docs if behavior changes
- Follow [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat:` new feature
  - `fix:` bug fix
  - `docs:` documentation only
  - `chore:` maintenance
  - `security:` security improvement

## Adding a New Converter

1. Create `src/documark/converters/<format>.py`
2. Implement the `convert(file_path: str) -> str` function
3. Register it in `src/documark/converters/__init__.py`
4. Add tests in `tests/test_converters.py`
5. Add the format to `docs/FORMATS.md`

## Adding a New Injection Detection Pattern

1. Add a tuple `("pattern_name", re.compile(...))` to `_INJECTION_PATTERNS` in `src/documark/security/injection.py`
2. Add a test in `tests/test_security.py` that catches the new pattern
3. Document the pattern in `docs/SECURITY-ARCHITECTURE.md`

## Code Style

- PEP 8 (enforced via `ruff`)
- Type hints on all public functions
- No docstrings for obvious functions; one-line comments only for non-obvious logic

## Reporting Issues

Use the GitHub issue templates:
- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)
