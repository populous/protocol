"""
Contract tests for the arithmetic evaluator.

Loads contract/arithmetic.contract.json and verifies every case.
Run with:  python -m pytest test_arithmetic_contract.py -v
       or: python test_arithmetic_contract.py
"""

import json
import pathlib
import unittest

from arithmetic import evaluate, ExpressionError

CONTRACT = json.loads(
    (pathlib.Path(__file__).parent / "contract" / "arithmetic.contract.json").read_text(encoding="utf-8")
)


def _make_test(case: dict):
    name      = case["name"]
    expr      = case["input"]
    expect    = case.get("expect")
    expect_err = case.get("expectError")

    if expect is not None:
        def test(self):
            result = evaluate(expr)
            self.assertEqual(
                result,
                expect["result"],
                f"[{name}] evaluate({expr!r}) = {result!r}, want {expect['result']!r}",
            )
    else:
        def test(self):
            with self.assertRaises(ExpressionError) as ctx:
                evaluate(expr)
            msg = str(ctx.exception).lower()
            self.assertIn(
                expect_err.lower(),
                msg,
                f"[{name}] expected error containing {expect_err!r}, got {msg!r}",
            )

    test.__name__ = f"test_{name}"
    return test


# Dynamically build a TestCase with one method per contract case.
_tests = {f"test_{case['name']}": _make_test(case) for case in CONTRACT["cases"]}
ArithmeticContractTests = type("ArithmeticContractTests", (unittest.TestCase,), _tests)

# Make the class visible at module level so unittest discovery can find it.
globals()["ArithmeticContractTests"] = ArithmeticContractTests


if __name__ == "__main__":
    unittest.main(verbosity=2)
