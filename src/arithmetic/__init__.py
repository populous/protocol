"""
Arithmetic expression evaluator package.

Public API:
    normalize(text)   -- replace dialect aliases with canonical operators
    evaluate(expr)    -- evaluate an arithmetic expression string
    ExpressionError   -- raised on invalid input
"""

from .normalizer import normalize
from .evaluator import evaluate as _evaluate, ExpressionError


def evaluate(expression: str) -> int:
    """Normalize dialect aliases then evaluate the arithmetic expression."""
    return _evaluate(normalize(expression))

__all__ = ["normalize", "evaluate", "ExpressionError"]
