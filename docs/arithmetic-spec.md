# Arithmetic Spec (v0.2-draft)

## Purpose
Define canonical arithmetic structure and dialect normalization responsibilities.

## Scope
- Binary ops: add, sub, mul, div
- Grouping: parentheses
- Operand: integer literal

## Authority Model
- Canonical structure authority: `grammar/ArithmeticParser.g4`
- Canonical token authority: `grammar/ArithmeticTokens.g4`
- Dialect/alias authority: `registers/arithmetic.registers.yaml`
- Behavior verification authority: `contract/arithmetic.contract.json`

## Canonical Semantics
- Precedence: `MUL_OP`, `DIV_OP` > `ADD_OP`, `SUB_OP`
- Associativity: all binary ops are left-associative
- Parentheses override precedence

## Update Policy (Mandatory)
1. Update this spec
2. Update `ArithmeticParser.g4` (structure)
3. Update `ArithmeticTokens.g4` (canonical token set, if needed)
4. Update `arithmetic.registers.yaml` (dialect mapping)
5. Update `arithmetic.contract.json` (tests)
6. Run tests and attach evidence to PR

## Error Policy
Must fail:
- `2++3`
- `3/`
- `(2+3`
- Unknown token input, e.g. `2 foo 3`

## Definition of Done
- [ ] Grammar reflects canonical structure only
- [ ] Registers define dialect normalization
- [ ] Contract includes canonical + dialect equivalence + fail cases
- [ ] Tests pass locally/CI
- [ ] PR includes command/output evidence

## Branch/PR Policy
- Branch: `feature/<issue>-arith`
- No direct commit to `main`
- PR required, CI green, 1+ approval
- Recommended merge: squash

## Metadata
- Last updated: 2026-08-27
- Owner: TBD
