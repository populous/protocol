"""
Arithmetic parser, normalizer, and evaluator.

Implements the arithmetic spec (docs/arithmetic-spec.md):
  - Normalizes dialect aliases to canonical tokens (per registers/arithmetic.registers.yaml)
  - Parses canonical tokens into an AST
  - Evaluates the AST to an integer result

Supported operations: add (+), sub (-), mul (*), div (/)
Grouping: parentheses
Operands: non-negative integer literals
Precedence: mul/div > add/sub, left-associative
"""

import re
from typing import Iterator

# ---------------------------------------------------------------------------
# Dialect normalization
# ---------------------------------------------------------------------------

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

# Regex that matches any alias (word or symbol).  The word boundary (\b) is
# used for alphabetic aliases; symbol replacements are just literal matches.
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


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"\s*(\d+|[+\-*/()])\s*")
_VALID_CHARS = re.compile(r"^[\d\s+\-*/()]+$")

# Token kinds
INT    = "INT"
ADD_OP = "ADD_OP"
SUB_OP = "SUB_OP"
MUL_OP = "MUL_OP"
DIV_OP = "DIV_OP"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
EOF    = "EOF"

_CHAR_KIND: dict[str, str] = {
    "+": ADD_OP,
    "-": SUB_OP,
    "*": MUL_OP,
    "/": DIV_OP,
    "(": LPAREN,
    ")": RPAREN,
}


class Token:
    __slots__ = ("kind", "value")

    def __init__(self, kind: str, value: str) -> None:
        self.kind = kind
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.kind!r}, {self.value!r})"


class LexError(ValueError):
    pass


class SyntaxError_(ValueError):
    pass


def tokenize(text: str) -> list[Token]:
    """
    Tokenize a normalized arithmetic expression.

    Raises LexError for unknown tokens, SyntaxError_ for invalid sequences.
    """
    if not _VALID_CHARS.match(text):
        # Find the offending character for a better message.
        for ch in text:
            if not re.match(r"[\d\s+\-*/()]", ch):
                raise LexError(f"unknown token: {ch!r}")
        raise LexError("unknown token")

    tokens: list[Token] = []
    pos = 0
    n = len(text)
    while pos < n:
        m = _TOKEN_RE.match(text, pos)
        if not m:
            raise LexError(f"unknown token at position {pos}")
        tok = m.group(1)
        if tok.isdecimal():
            tokens.append(Token(INT, tok))
        else:
            tokens.append(Token(_CHAR_KIND[tok], tok))
        pos = m.end()

    tokens.append(Token(EOF, ""))
    return tokens


# ---------------------------------------------------------------------------
# Parser  (recursive-descent, mirrors ArithmeticParser.g4)
# ---------------------------------------------------------------------------

class ParseError(ValueError):
    pass


class _Parser:
    """Recursive-descent parser for canonical arithmetic tokens."""

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    # -- helpers ----------------------------------------------------------

    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _consume(self, kind: str | None = None) -> Token:
        tok = self._tokens[self._pos]
        if kind and tok.kind != kind:
            raise ParseError(
                f"syntax error: expected {kind} but got {tok.kind!r} ({tok.value!r})"
            )
        self._pos += 1
        return tok

    # -- grammar rules ----------------------------------------------------

    def parse(self) -> tuple:
        node = self._expr()
        if self._peek().kind != EOF:
            raise ParseError(
                f"syntax error: unexpected token {self._peek().value!r}"
            )
        return node

    def _expr(self) -> tuple:
        return self._add_sub()

    def _add_sub(self) -> tuple:
        left = self._mul_div()
        while self._peek().kind in (ADD_OP, SUB_OP):
            op = self._consume()
            right = self._mul_div()
            left = (op.kind, left, right)
        return left

    def _mul_div(self) -> tuple:
        left = self._primary()
        while self._peek().kind in (MUL_OP, DIV_OP):
            op = self._consume()
            right = self._primary()
            left = (op.kind, left, right)
        return left

    def _primary(self) -> tuple:
        tok = self._peek()
        if tok.kind == INT:
            self._consume()
            return (INT, int(tok.value))
        if tok.kind == LPAREN:
            self._consume(LPAREN)
            node = self._expr()
            if self._peek().kind != RPAREN:
                raise ParseError("syntax error: unclosed parenthesis")
            self._consume(RPAREN)
            return node
        if tok.kind == EOF:
            raise ParseError("syntax error: unexpected end of expression")
        raise ParseError(f"syntax error: unexpected token {tok.value!r}")


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------

def _eval(node: tuple) -> int:
    kind = node[0]
    if kind == INT:
        return node[1]
    if kind == ADD_OP:
        return _eval(node[1]) + _eval(node[2])
    if kind == SUB_OP:
        return _eval(node[1]) - _eval(node[2])
    if kind == MUL_OP:
        return _eval(node[1]) * _eval(node[2])
    if kind == DIV_OP:
        left, right = _eval(node[1]), _eval(node[2])
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return left // right
    raise ValueError(f"unknown AST node kind: {kind!r}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class ExpressionError(ValueError):
    pass


def evaluate(expression: str) -> int:
    """
    Normalize, parse, and evaluate an arithmetic expression string.

    Returns the integer result.
    Raises ExpressionError on syntax or unknown-token errors.
    """
    normalized = normalize(expression)
    try:
        tokens = tokenize(normalized)
    except LexError as exc:
        raise ExpressionError(str(exc)) from exc

    try:
        ast = _Parser(tokens).parse()
    except ParseError as exc:
        raise ExpressionError(str(exc)) from exc

    try:
        return _eval(ast)
    except ZeroDivisionError as exc:
        raise ExpressionError(str(exc)) from exc
