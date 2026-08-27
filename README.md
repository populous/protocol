# Protocol — Arithmetic

A Python implementation of the arithmetic expression evaluator defined in `contract/arithmetic.contract.json`.

## Project structure

```
src/
  arithmetic/
    __init__.py     # public API: normalize(), evaluate(), ExpressionError
    normalizer.py   # dialect alias → canonical operator (+, -, *, /)
    evaluator.py    # tokenizer, recursive-descent parser, evaluator

tests/
  test_contract.py  # contract-driven tests (loads contract/arithmetic.contract.json)

contract/
  arithmetic.contract.json  # canonical test contract

pyproject.toml    # project metadata + pytest configuration
```

## Python version

Python **3.11** or later is required.

## Running the tests

```bash
pip install pytest
python -m pytest
```

## Example usage

```python
from arithmetic import evaluate

print(evaluate("2 + 3 * 4"))      # 14
print(evaluate("(2 plus 3) × 4")) # 20
print(evaluate("8 ÷ 2 ÷ 2"))      # 2
```

The `evaluate` function accepts dialect aliases (`plus`, `add`, `minus`, `sub`, `times`, `mul`, `div`, `×`, `÷`) in addition to the canonical operators (`+`, `-`, `*`, `/`).
