"""
Dialect normalization for arithmetic expressions.

Replaces word/symbol aliases (e.g. "plus", "×") with their canonical
single-character operator tokens (+, -, *, /).
"""

import re

# Ordered longest-match aliases mapped to canonical single-character token.
# Derived from registers/arithmetic.registers.yaml dialects.
_DIALECT_MAP: list[tuple[str, str]] = sorted(
    [
        ("plus",  "+"),
        ("add",   "+"),
        ("minus", "-"),
        ("sub",   "-"),
        ("times", "*"),
        ("mul",   "*"),
        ("div",   "/"),
        ("×",     "*"),
        ("÷",     "/"),
    ],
    key=lambda p: len(p[0]),
    reverse=True,  # longest first so multi-char words match before shorter ones
)

_DIALECT_RE = re.compile(
    r"\b(?:" + "|".join(
        re.escape(alias) for alias, _ in _DIALECT_MAP if alias.isalpha()
    ) + r")\b"
    + r"|"
    + "|".join(
        re.escape(alias) for alias, _ in _DIALECT_MAP if not alias.isalpha()
    ),
    re.IGNORECASE,
)

_ALIAS_LOOKUP: dict[str, str] = {alias.lower(): canon for alias, canon in _DIALECT_MAP}


def normalize(text: str) -> str:
    """Replace dialect aliases with canonical operator characters."""
    def _replace(m: re.Match) -> str:
        return _ALIAS_LOOKUP[m.group(0).lower()]

    return _DIALECT_RE.sub(_replace, text)
