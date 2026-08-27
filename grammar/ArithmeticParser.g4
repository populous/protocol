parser grammar ArithmeticParser;

options { tokenVocab=ArithmeticTokens; }

/*
Structure-only parser grammar.
Dialect/surface variants are normalized upstream.
*/

parse
    : expr EOF
    ;

expr
    : expr op=(MUL_OP | DIV_OP) expr # MulDivExpr
    | expr op=(ADD_OP | SUB_OP) expr # AddSubExpr
    | LPAREN expr RPAREN             # ParenExpr
    | INT                            # IntExpr
    ;
