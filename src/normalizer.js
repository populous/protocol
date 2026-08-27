const CANONICAL_BY_TOKEN = {
  ADD_OP: '+',
  SUB_OP: '-',
  MUL_OP: '*',
  DIV_OP: '/',
  LPAREN: '(',
  RPAREN: ')',
};

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function getAliasMap(registers) {
  const result = new Map();
  const dialects = registers?.dialects || {};

  Object.entries(dialects).forEach(([token, aliases]) => {
    const canonical = CANONICAL_BY_TOKEN[token];
    if (!canonical || !Array.isArray(aliases)) {
      return;
    }

    aliases.forEach((alias) => {
      result.set(String(alias), canonical);
    });
  });

  return result;
}

function normalizeDialect(input, registers) {
  if (typeof input !== 'string') {
    throw new Error('syntax error');
  }

  const aliasMap = getAliasMap(registers);
  let output = input;

  const symbolAliases = [];
  const wordAliases = [];

  for (const [alias, canonical] of aliasMap.entries()) {
    if (/^[A-Za-z]+$/.test(alias)) {
      wordAliases.push([alias, canonical]);
    } else {
      symbolAliases.push([alias, canonical]);
    }
  }

  symbolAliases
    .sort((a, b) => b[0].length - a[0].length)
    .forEach(([alias, canonical]) => {
      output = output.replace(new RegExp(escapeRegex(alias), 'g'), canonical);
    });

  wordAliases
    .sort((a, b) => b[0].length - a[0].length)
    .forEach(([alias, canonical]) => {
      output = output.replace(new RegExp(`\\b${escapeRegex(alias)}\\b`, 'gi'), canonical);
    });

  return output.replace(/\s+/g, '');
}

module.exports = {
  normalizeDialect,
};
