const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const { loadContract, loadRegisters } = require('../src/contract-loader');
const { normalizeDialect } = require('../src/normalizer');
const { evaluateExpression } = require('../src/evaluator');

const repoRoot = path.join(__dirname, '..');
const contract = loadContract(repoRoot);
const registers = loadRegisters(repoRoot);

contract.cases.forEach((caseDef) => {
  test(caseDef.name, () => {
    if (caseDef.expectError) {
      assert.throws(
        () => {
          const normalized = normalizeDialect(caseDef.input, registers);
          evaluateExpression(normalized);
        },
        (error) => error && error.message === caseDef.expectError,
      );
      return;
    }

    const normalized = normalizeDialect(caseDef.input, registers);
    const result = evaluateExpression(normalized);

    assert.equal(result, caseDef.expect.result);

    if (caseDef.equivalentTo) {
      const normalizedEquivalent = normalizeDialect(caseDef.equivalentTo, registers);
      const equivalentResult = evaluateExpression(normalizedEquivalent);
      assert.equal(result, equivalentResult);
    }
  });
});
