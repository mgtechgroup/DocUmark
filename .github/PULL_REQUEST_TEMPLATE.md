## Summary

Briefly describe what this PR does and why.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Security improvement
- [ ] Documentation update
- [ ] Refactor
- [ ] Other: ___

## Related Issue

Closes #(issue number)

## Security Checklist

- [ ] All file processing goes through `check_file()` — no bypass
- [ ] No new network calls that exfiltrate file content
- [ ] New injection patterns (if any) have tests in `tests/test_security.py`
- [ ] No hardcoded secrets or API keys

## Testing

- [ ] All existing tests pass (`pytest tests/ -v`)
- [ ] New tests added for new functionality
- [ ] Security tests pass (`pytest tests/test_security.py -v`)
- [ ] Manual test: describe what you tested

## Checklist

- [ ] Code follows PEP 8 (`ruff check src/ tests/`)
- [ ] Type hints added to new public functions
- [ ] Relevant `.md` docs updated
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] Commit messages follow Conventional Commits
