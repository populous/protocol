const fs = require('node:fs');
const path = require('node:path');
const yaml = require('js-yaml');

function loadJson(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(content);
}

function loadYaml(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  return yaml.load(content);
}

function loadContract(repoRoot) {
  const contractPath = path.join(repoRoot, 'contract', 'arithmetic.contract.json');
  return loadJson(contractPath);
}

function loadRegisters(repoRoot) {
  const registersPath = path.join(repoRoot, 'registers', 'arithmetic.registers.yaml');
  return loadYaml(registersPath);
}

module.exports = {
  loadContract,
  loadRegisters,
};
