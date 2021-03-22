grammar CESQLParser;

import CESQLLexer;

// Entrypoint
cesql: expression EOF;

// Structure of operations, function invocations and expression
expression
    : functionIdentifier LR_BRACKET functionParameterList RR_BRACKET #functionInvocationExpression
    | unaryLogicOperator expression #unarylogicExpression
    | unaryNumericOperator expression # unaryNumericExpression
    | expression binaryLogicOperator expression #binaryLogicExpression
    | expression binaryComparisonOperator expression #binaryComparisonExpression
    | expression binaryNumericOperator expression #binaryNumericExpression
    | expression notOperator? likeOperator stringLiteral #likeExpression
    | existsOperator identifier #existsExpression
    | expression notOperator? inOperator setExpression #inExpression
    | LR_BRACKET expression RR_BRACKET #subExpression
    | atom #atomExpression
    ;

atom
    : booleanLiteral #booleanLiteralExpression
    | integerLiteral #integerLiteralExpression
    | stringLiteral #stringLiteralExpression
    | identifier #identifierExpression
    ;

// Identifiers

identifier: IDENTIFIER;
functionIdentifier: FUNCTION_IDENTIFIER;

// Literals

booleanLiteral: BOOLEAN_LITERAL;
stringLiteral: STRING_LITERAL;
integerLiteral: INTEGER_LITERAL;

// Operators

unaryNumericOperator
    : MINUS
    ;

notOperator
    : NOT
    ;

unaryLogicOperator
    : notOperator
    ;

binaryComparisonOperator
    : (EQUAL | EXCLAMATION EQUAL | LESS GREATER | GREATER EQUAL | LESS EQUAL | LESS | GREATER)
    ;

binaryNumericOperator
    : (STAR | DIVIDE | MODULE | PLUS | MINUS)
    ;

binaryLogicOperator
    : (AND | OR | XOR)
    ;

likeOperator
    : LIKE
    ;

existsOperator
    : EXISTS
    ;

inOperator
    : IN
    ;

// Functions

functionParameter
    : expression
    ;

functionParameterList
    : ( functionParameter ( COMMA functionParameter )* )?
    ;

// Sets

setExpression
    : expression ( COMMA expression )* // Non-empty set is not allowed
    ;
