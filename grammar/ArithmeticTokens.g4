lexer grammar ArithmeticTokens;

/*
Canonical token lexer.
Dialect symbols/words should be normalized before parse stage.
*/

ADD_OP : '+' ;
SUB_OP : '-' ;
MUL_OP : '*' ;
DIV_OP : '/' ;

LPAREN : '(' ;
RPAREN : ')' ;

INT : [0-9]+ ;

WS : [ \t\r\n]+ -> skip ;
