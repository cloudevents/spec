grammar CESQLParser;

import CESQLLexer;

// Entrypoint
cesql: expression EOF;

// Structure of operations, function invocations and expression
functionInvocation
    : functionIdentifier LR_BRACKET functionParameterList RR_BRACKET
    ;

unaryOperation
    : unaryLogicOperator expression #unarylogicExpression
    | unaryNumericOperator expression # unaryNumericExpression
    ;

expression
    : functionInvocation #functionInvocationExpression
    | unaryOperation #unaryExpression
    // LIKE, EXISTS and IN takes precedence over all the other operators
    | expression notOperator? likeOperator stringLiteral #likeExpression
    | existsOperator identifier #existsExpression
    | expression notOperator? inOperator setExpression #inExpression
    // Numeric operations
    | expression (STAR | DIVIDE | MODULE) expression #binaryMultiplicativeExpression
    | expression (PLUS | MINUS) expression #binaryAdditiveExpression
    // Comparison operations
    | expression binaryComparisonOperator expression #binaryComparisonExpression
    // Logic operations
    |<assoc=right> expression binaryLogicOperator expression #binaryLogicExpression
    // Subexpressions and atoms
    | LR_BRACKET expression RR_BRACKET #subExpression
    | atom #atomExpression
    ;

atom
    : booleanLiteral #booleanAtom
    | integerLiteral #integerAtom
    | stringLiteral #stringAtom
    | identifier #identifierAtom
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
