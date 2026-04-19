import re

# Each entry: (pattern_name, compiled_regex)
_INJECTION_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("ignore_previous", re.compile(r"ignore\s+(all\s+)?previous\s+instructions?", re.I)),
    ("system_override", re.compile(r"(you\s+are\s+now|act\s+as|pretend\s+you\s+are)\s+.{0,80}(ai|assistant|bot|gpt|llm)", re.I)),
    ("jailbreak_dan", re.compile(r"\bDAN\b.*\bdo\s+anything\s+now\b", re.I | re.S)),
    ("hidden_instruction", re.compile(r"<!--.*?(ignore|override|system|prompt).*?-->", re.I | re.S)),
    ("code_execution", re.compile(r"\b(eval|decode|base64)\s*\(", re.I)),
    ("exfiltration_attempt", re.compile(r"(send|post|fetch|curl|wget)\s+.{0,40}(http|https|ftp)://", re.I)),
    ("role_hijack", re.compile(r"(your\s+new\s+(role|purpose|goal|task|mission)\s+is|from\s+now\s+on\s+you)", re.I)),
    ("token_smuggling", re.compile(r"<\|[a-z_]+\|>", re.I)),
    ("null_byte", re.compile(r"\x00")),
    ("rtl_override", re.compile(r"[\u202e\u200f\u061c]")),
]


def detect_injection(text: str) -> dict:
    """
    Scan text for prompt injection and hidden instruction patterns.
    Returns {"detected": bool, "pattern": str | None, "matches": list[str]}.
    """
    matches_found: list[str] = []
    first_pattern: str | None = None

    for name, pattern in _INJECTION_PATTERNS:
        found = pattern.findall(text)
        if found:
            matches_found.append(f"{name}: {len(found)} match(es)")
            if first_pattern is None:
                first_pattern = name

    return {
        "detected": len(matches_found) > 0,
        "pattern": first_pattern,
        "matches": matches_found,
    }
