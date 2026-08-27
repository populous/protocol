"""
Contract tests for the arithmetic evaluator.

Loads contract/arithmetic.contract.json and verifies every case.
Run with:  python -m pytest
"""

import json
import pathlib
import pytest

from arithmetic import evaluate, ExpressionError

_CONTRACT_PATH = pathlib.Path(__file__).parents[1] / "contract" / "arithmetic.contract.json"
_CONTRACT = json.loads(_CONTRACT_PATH.read_text())


def _case_ids():
    return [case["name"] for case in _CONTRACT["cases"]]


def _cases():
    return _CONTRACT["cases"]


@pytest.mark.parametrize("case", _cases(), ids=_case_ids())
def test_contract_case(case):
    name = case["name"]
    expr = case["input"]
    expect = case.get("expect")
    expect_err = case.get("expectError")

    if expect is not None:
        result = evaluate(expr)
        assert result == expect["result"], (
            f"[{name}] evaluate({expr!r}) = {result!r}, want {expect['result']!r}"
        )
    else:
        with pytest.raises(ExpressionError) as exc_info:
            evaluate(expr)
        msg = str(exc_info.value).lower()
        assert expect_err.lower() in msg, (
            f"[{name}] expected error containing {expect_err!r}, got {msg!r}"
        )
