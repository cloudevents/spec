lexer grammar CESQLLexer;

// NOTE:
// This grammar is case-sensitive, although CESQL keywords are case-insensitive.
// In order to implement case-insensitivity, check out
// https://github.com/antlr/antlr4/blob/master/doc/case-insensitive-lexing.md#custom-character-streams-approach

// Skip tab, carriage return and newlines

SPACE:                               [ \t\r\n]+    -> skip;

// Fragments for Literal primitives

fragment ID_LITERAL:                 [a-z0-9]+;
fragment DQUOTA_STRING:              '"' ( '\\'. | '""' | ~('"'| '\\') )* '"';
fragment SQUOTA_STRING:              '\'' ('\\'. | '\'\'' | ~('\'' | '\\'))* '\'';
fragment INT_DIGIT:                  [0-9];
fragment FN_LITERAL:                 [A-Z][A-Z_]*;

// Constructors symbols

LR_BRACKET:                          '(';
RR_BRACKET:                          ')';
COMMA:                               ',';
SINGLE_QUOTE_SYMB:                   '\'';
DOUBLE_QUOTE_SYMB:                   '"';

fragment QUOTE_SYMB
    : SINGLE_QUOTE_SYMB | DOUBLE_QUOTE_SYMB
    ;

// Operators
// - Logic

AND: 'AND';
OR: 'OR';
XOR: 'XOR';
NOT: 'NOT';

// - Arithmetics

STAR:                                '*';
DIVIDE:                              '/';
MODULE:                              '%';
PLUS:                                '+';
MINUS:                               '-';

// - Comparison

EQUAL:                        '=';
GREATER:                      '>';
LESS:                         '<';
EXCLAMATION:                  '!';

// Like, exists, in

LIKE: 'LIKE';
EXISTS: 'EXISTS';
IN: 'IN';

// Literals

STRING_LITERAL:                      DQUOTA_STRING | SQUOTA_STRING;
INTEGER_LITERAL:                     INT_DIGIT+;
BOOLEAN_LITERAL:                     'TRUE'| 'FALSE';

// Identifiers

IDENTIFIER:                                  ID_LITERAL;
FUNCTION_IDENTIFIER:                        FN_LITERAL;
