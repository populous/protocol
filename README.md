# Protocol

## Arithmetic contract tests

Run tests locally:

```bash
npm ci
npm test
```

The test runner loads contract cases from `/contract/arithmetic.contract.json`, normalizes dialect input using `/registers/arithmetic.registers.yaml`, and evaluates expressions against expected results.
