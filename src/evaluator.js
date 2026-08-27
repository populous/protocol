function tokenize(input) {
  const tokens = [];
  let index = 0;

  while (index < input.length) {
    const ch = input[index];

    if (/\s/.test(ch)) {
      index += 1;
      continue;
    }

    if (/[0-9]/.test(ch)) {
      let end = index + 1;
      while (end < input.length && /[0-9]/.test(input[end])) {
        end += 1;
      }
      tokens.push({ type: 'INT', value: Number(input.slice(index, end)) });
      index = end;
      continue;
    }

    if (ch === '+' || ch === '-' || ch === '*' || ch === '/' || ch === '(' || ch === ')') {
      tokens.push({ type: ch, value: ch });
      index += 1;
      continue;
    }

    throw new Error('unknown token');
  }

  return tokens;
}

function evaluateExpression(input) {
  const tokens = tokenize(input);
  let pos = 0;

  function current() {
    return tokens[pos];
  }

  function consume(type) {
    if (current() && current().type === type) {
      pos += 1;
      return true;
    }
    return false;
  }

  function parseFactor() {
    const token = current();
    if (!token) {
      throw new Error('syntax error');
    }

    if (consume('INT')) {
      return token.value;
    }

    if (consume('(')) {
      const value = parseExpr();
      if (!consume(')')) {
        throw new Error('syntax error');
      }
      return value;
    }

    throw new Error('syntax error');
  }

  function parseTerm() {
    let value = parseFactor();

    while (current() && (current().type === '*' || current().type === '/')) {
      const op = current().type;
      pos += 1;
      const rhs = parseFactor();
      if (op === '*') {
        value *= rhs;
      } else {
        value /= rhs;
      }
    }

    return value;
  }

  function parseExpr() {
    let value = parseTerm();

    while (current() && (current().type === '+' || current().type === '-')) {
      const op = current().type;
      pos += 1;
      const rhs = parseTerm();
      if (op === '+') {
        value += rhs;
      } else {
        value -= rhs;
      }
    }

    return value;
  }

  const result = parseExpr();
  if (pos !== tokens.length) {
    throw new Error('syntax error');
  }

  return result;
}

module.exports = {
  evaluateExpression,
};
