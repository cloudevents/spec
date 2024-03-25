# CloudEvents SQL Expression Language - Version 0.1-wip

## Abstract

The goal of this specification is to define a SQL-like expression language which can be used to express predicates on
CloudEvent instances.

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to Subscriptions API](#12-relation-to-the-subscriptions-api)

2. [Language syntax](#2-language-syntax)

- 2.1. [Expression](#21-expression)
- 2.2. [Value identifiers and literals](#22-value-identifiers-and-literals)
- 2.3. [Operators](#23-operators)
- 2.4. [Function invocations](#24-function-invocations)

3. [Language semantics](#3-language-semantics)

- 3.1. [Type system](#31-type-system)
- 3.2. [CloudEvent context identifiers and types](#32-cloudevent-context-identifiers-and-types)
- 3.3. [Errors](#33-errors)
- 3.4. [Operators](#34-operators)
- 3.5. [Functions](#35-functions)
- 3.6. [Evaluation of the expression](#36-evaluation-of-the-expression)
- 3.7. [Type casting](#37-type-casting)

4. [Implementation suggestions](#4-implementation-suggestions)

- 4.1. [Error handling](#41-error-handling)

5. [Examples](#5-examples)
6. [References](#6-references)

## 1. Introduction

CloudEvents SQL expressions (also known as CESQL) allow computing values and matching of CloudEvent attributes against complex expressions
that lean on the syntax of Structured Query Language (SQL) `WHERE` clauses. Using SQL-derived expressions for message
filtering has widespread implementation usage because the Java Message Service (JMS) message selector syntax also leans
on SQL. Note that neither the SQL standard (ISO 9075) nor the JMS standard nor any other SQL dialect is used as a
normative foundation or to constrain the expression syntax defined in this specification, but the syntax is informed by
them.

CESQL is a _[Total pure functional programming language][total-programming-language-wiki]_ in order to guarantee the
termination of the evaluation of the expression. It features a type system correlated to the [CloudEvents type
system][ce-type-system], and it features boolean and arithmetic operations, as well as built-in functions for string
manipulation.

The language is not constrained to a particular execution environment, which means it might run in a source, in a
producer, or in an intermediary, and it can be implemented using any technology stack.

The CloudEvents Expression Language assumes the input always includes, but is not limited to, a single valid and
type-checked CloudEvent instance. An expression MUST NOT mutate the value of the input CloudEvent instance, nor any of
the other input values. The evaluation of an expression observes the concept of [referential
transparency][referential-transparency-wiki]. The output of a CESQL expression evaluation is always a _boolean_, an _integer_ or a _string_, and it might include an error.

The CloudEvents Expression Language doesn't support the handling of the data field of the CloudEvent instances, due to
its polymorphic nature and complexity. Users that need this functionality ought to use other more appropriate tools.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to the Subscriptions API

The CESQL can be used as a [filter dialect][subscriptions-filter-dialect] to filter on the input values.

When used as a filter predicate, the expression output value is always cast to a boolean value.

<!-- TODO -->

## 2. Language syntax

The grammar of the language is defined using the EBNF Notation from [W3C XML specification][ebnf-xml-spec].

Although in the EBNF keywords are defined using uppercase characters, they are case-insensitive. For example:

```
int(hop) < int(ttl) and int(hop) < 1000
```

Has the same syntactical meaning of:

```
INT(hop) < INT(ttl) AND INT(hop) < 1000
```

### 2.1 Expression

The root of the expression is the `expression` rule:

```ebnf
expression ::= value-identifier | boolean-literal | unary-operation | binary-operation | function-invocation | like-operation | exists-operation | in-operation | ( "(" expression ")" )
```

Nested expressions MUST be correctly parenthesized.

### 2.2. Value identifiers and literals

Value identifiers in CESQL MUST follow the same restrictions of the [Attribute Naming
Convention][ce-attribute-naming-convention] from the CloudEvents spec. A value identifier MUST NOT be greater than 20
characters in length.

```ebnf
lowercase-char ::= [a-z]
value-identifier ::= ( lowercase-char | digit ) ( lowercase-char | digit )*
```

CESQL defines 3 different literal kinds: integer numbers, `true` or `false` booleans, and `''` or `""` delimited strings.

```ebnf
digit ::= [0-9]
number-literal ::= digit+

boolean-literal ::= "true" | "false" (* Case insensitive *)

string-literal ::= ( "'" ( [^'] | "\'" )* "'" ) | ( '"' ( [^"] | '\"' )* '"')

literal ::= number-literal | boolean-literal | string-literal
```

Because string literals can be either `''` or `""` delimited, in the former case, the `'` has to be escaped, while in
the latter the `"` has to be escaped.

### 2.3. Operators

CESQL defines boolean unary and binary operators, arithmetic unary and binary operators, and the `LIKE`, `IN`, `EXISTS`
operators.

```ebnf
not-operator ::= "NOT"
unary-logic-operator ::= not-operator
binary-logic-operator ::= "AND" | "OR" | "XOR"

unary-numeric-operator ::= "-"
binary-comparison-operator ::= "=" | "!=" | "<>" | ">=" | "<=" | "<" | ">"
binary-numeric-arithmetic-operator ::= "+" | "-" | "*" | "/" | "%"

like-operator ::= "LIKE"
exists-operator ::= "EXISTS"
in-operator ::= "IN"

unary-operation ::= (unary-numeric-operator | unary-logic-operator) expression

binary-operation ::= expression (binary-comparison-operator | binary-numeric-arithmetic-operator | binary-logic-operator) expression

like-operation ::= expression not-operator? like-operator string-literal

exists-operation ::= exists-operator value-identifier

set-expression ::= "(" expression ("," expression)* ")"
in-operation ::= expression not-operator? in-operator set-expression
```

### 2.4. Function invocations

CESQL supports n-ary function invocation:

```ebnf
char ::= [A-Z] | [a-z]
argument ::= expression

function-identifier ::= char ( "_" | char )*

argument-list ::= argument ("," argument)*
function-invocation ::= function-identifier "(" argument-list? ")"
```

## 3. Language semantics

### 3.1. Type system

The type system contains 3 _primitive_ types:

- _String_: Sequence of Unicode characters.
- _Integer_: A whole number in the range -2,147,483,648 to +2,147,483,647 inclusive. This is the range of a signed,
  32-bit, twos-complement encoding.
- _Boolean_: A boolean value of "true" or "false".

The types _URI_, _URI Reference_, and _Timestamp_ ([defined in the CloudEvents specification][ce-type-system]) are represented as
_String_.

The type system also includes _Set_, which is an unordered collection of _Strings_ of arbitrary length. This type can
be used in the `IN` operator.

### 3.2. CloudEvent context identifiers and types

Each CloudEvent context attribute and extension MUST be addressable from an expression using its identifier, as defined
by the spec. For example, using `id` in an expression will address the CloudEvent [id attribute][ce-id-attribute].

Unless otherwise specified, every attribute and extension MUST be represented by the _String_ type as its initial type.
Through implicit type casting, the user can convert the addressed value instances to _Integer_ and
_Boolean_.

When addressing an attribute not included in the input event, the subexpression referencing the missing attribute MUST evaluate to `false`.
For example, `true AND (missingAttribute = "")` would evaluate to `false` as the subexpression `missingAttribute = ""` would be false.

### 3.3. Errors

Because every operator and function is total, an expression evaluation flow is defined statically and cannot be modified
by expected or unexpected errors. Nevertheless CESQL includes the concept of errors: when an expression is evaluated, in
case an error arises, the evaluator collects a list of errors, referred in this spec as _error list_, which is then
returned together with the evaluated value of the CESQL expression.

Whenever possible, some error checks SHOULD be done at compile time by the expression evaluator, in order to prevent
runtime errors.

### 3.4. Operators

The following tables show the operators that MUST be supported by a CESQL evaluator.

All the operators in the following tables are listed in precedence order.

#### 3.4.1. Unary operators

Corresponds to the syntactic rule `unary-operation`:

| Definition                  | Semantics                       |
| --------------------------- | ------------------------------- |
| `NOT x: Boolean -> Boolean` | Returns the negate value of `x` |
| `-x: Integer -> Integer`    | Returns the minus value of `x`  |

#### 3.4.2. Binary operators

Corresponds to the syntactic rule `binary-operation`:

| Definition                              | Semantics                                                                                                  |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `x = y: Boolean x Boolean -> Boolean`   | Returns `true` if the values of `x` and `y` are equal                                                      |
| `x != y: Boolean x Boolean -> Boolean`  | Same as `NOT (x = y)`                                                                                      |
| `x <> y: Boolean x Boolean -> Boolean`  | Same as `NOT (x = y)`                                                                                      |
| `x AND y: Boolean x Boolean -> Boolean` | Returns the logical and of `x` and `y`                                                                     |
| `x OR y: Boolean x Boolean -> Boolean`  | Returns the logical or of `x` and `y`                                                                      |
| `x XOR y: Boolean x Boolean -> Boolean` | Returns the logical xor of `x` and `y`                                                                     |
| `x = y: Integer x Integer -> Boolean`   | Returns `true` if the values of `x` and `y` are equal                                                      |
| `x != y: Integer x Integer -> Boolean`  | Same as `NOT (x = y)`                                                                                      |
| `x <> y: Integer x Integer -> Boolean`  | Same as `NOT (x = y)`                                                                                      |
| `x < y: Integer x Integer -> Boolean`   | Returns `true` if `x` is strictly less than `y`                                                            |
| `x <= y: Integer x Integer -> Boolean`  | Returns `true` if `x` is less than or equal to `y`                                                         |
| `x > y: Integer x Integer -> Boolean`   | Returns `true` if `x` is strictly greater than `y`                                                         |
| `x >= y: Integer x Integer -> Boolean`  | Returns `true` if `x` is greater or equal to `y`                                                           |
| `x * y: Integer x Integer -> Integer`   | Returns the product of `x` and `y`                                                                         |
| `x / y: Integer x Integer -> Integer`   | Returns the truncated division of `x` and `y`. Returns `0` and raises an error if `y = 0`                  |
| `x % y: Integer x Integer -> Integer`   | Returns the remainder of the truncated division of `x` and `y`. Returns `0` and raises an error if `y = 0` |
| `x + y: Integer x Integer -> Integer`   | Returns the sum of `x` and `y`                                                                             |
| `x - y: Integer x Integer -> Integer`   | Returns the difference of `x` and `y`                                                                      |
| `x = y: String x String -> Boolean`     | Returns `true` if the values of `x` and `y` are equal                                                      |
| `x != y: String x String -> Boolean`    | Same as `NOT (x = y)`                                                                                      |
| `x <> y: String x String -> Boolean`    | Same as `NOT (x = y)`                                                                                      |

The modulo and divisions MUST follow the [truncated divisions definition][modulo-operation-wiki], that is:

- The remainder of the modulo MUST have the same sign as the dividend.
- The quotient MUST be rounded towards zero, _truncating_ the decimal part.

The AND and OR operators MUST be short-circuit evaluated. This means that whenever the left operand of the AND operation evaluates to `false`, the right operand MUST NOT be evaluated.
Similarly, whenever the left operand of the OR operation evaluates to `true`, the right operand MUST NOT be evaluated.

#### 3.4.3. Like operator

| Definition                                       | Semantics                                           |
| ------------------------------------------------ | --------------------------------------------------- |
| `x LIKE pattern: String x String -> Boolean`     | Returns `true` if the value x matches the `pattern` |
| `x NOT LIKE pattern: String x String -> Boolean` | Same as `NOT (x LIKE PATTERN)`                      |

The pattern of the `LIKE` operator can contain:

- `%` represents zero, one, or multiple characters
- `_` represents a single character

For example, the pattern `_b*` will accept values `ab`, `abc`, `abcd1` but won't accept values `b` or `acd`.

Both `%` and `_` can be escaped with `\`, in order to be matched literally. For example, the pattern `abc\%` will match
`abc%` but won't match `abcd`.

#### 3.4.4. Exists operator

| Definition                          | Semantics                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `EXISTS identifier: Any -> Boolean` | Returns `true` if the attribute `identifier` exists in the input CloudEvent |

Note: `EXISTS` MUST always return `true` for the REQUIRED context attributes because the input CloudEvent is always
assumed valid, e.g. `EXISTS id` MUST always return `true`.

#### 3.4.5. In operator

| Definition                                             | Semantics                                                                  |
| ------------------------------------------------------ | -------------------------------------------------------------------------- |
| `x IN (y1, y2, ...): Any x Any^n -> Boolean`     | Returns `true` if `x` is equal to an element in the _Set_ of `yN` elements |
| `x NOT IN (y1, y2, ...): Any x Any^n -> Boolean` | Same as `NOT (x IN set)`                                                   |

The matching is done using the same semantics of the equal `=` operator, but using `x` type as the target type for the implicit type casting.

### 3.5. Functions

CESQL provides the concept of function, and defines some built-in that every engine MUST implement. An engine SHOULD also allow users to define their custom functions.

A function is identified by its name, its parameters and the return value. A function can be variadic, that is the arity is not fixed.

CESQL allows overloading, that is the engine MUST be able to distinguish between two functions defined with the same name but different arity.
Because of implicit casting, no functions with the same name and same arity but different types are allowed.

An overload on a variadic function is allowed only if the number of initial fixed arguments is greater than the maximum arity for that particular function name. Only one variadic overload is allowed.

For example, the following definitions are valid:

* `ABC(x): String -> Integer`: Unary function (arity 1). 
* `ABC(x, y): String x String -> Integer`: Binary function (arity 2).
* `ABC(x, y, z, ...): String x String x String x String^n -> Integer`: n-ary function (variable arity), but the initial fixed arguments are at least 3.

But the following are invalid, so the engine MUST reject them:

* `ABC(x...): String^n -> Integer`: n-ary function (variable arity), but there are no initial fixed arguments.
* `ABC(x, y, z): String x String x String -> Integer`: Ternary function (arity 3).

When a function invocation cannot be dispatched, the return value is undefined.

The following tables show the built-in functions that MUST be supported by a CESQL evaluator.

#### 3.5.1. Built-in String manipulation

| Definition                                                 | Semantics                                                                                                                                                                                                                  |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LENGTH(x): String -> Integer`                             | Returns the character length of the String `x`.                                                                                                                                                                            |
| `CONCAT(x1, x2, ...): String^n -> String`                  | Returns the concatenation of `x1` up to `xN`.                                                                                                                                                                              |
| `CONCAT_WS(delimiter, x1, x2, ...): String x String^n -> String`                  | Returns the concatenation of `x1` up to `xN`, using the `delimiter`.                                                                                                                                |
| `LOWER(x): String -> String`                               | Returns `x` in lowercase.                                                                                                                                                                                                  |
| `UPPER(x): String -> String`                               | Returns `x` in uppercase.                                                                                                                                                                                                  |
| `TRIM(x): String -> String`                                | Returns `x` with leading and trailing trimmed whitespaces.                                                                                                                                                                 |
| `LEFT(x, y): String x Integer -> String`                   | Returns a new string with the first `y` characters of `x`, or returns `x` if `LENGTH(x) <= y`. Returns `x` if `y < 0` and raises an error.                                                                                 |
| `RIGHT(x, y): String x Integer -> String`                  | Returns a new string with the last `y` characters of `x` or returns `x` if `LENGTH(x) <= y`. Returns `x` if `y < 0` and raises an error.                                                                                   |
| `SUBSTRING(x, pos): String x Integer x Integer -> String`  | Returns the substring of `x` starting from index `pos` (included) up to the end of `x`. Characters' index starts from `1`. If `pos` is negative, the beginning of the substring is `pos` characters from the end of the string. If `pos` is 0, then returns the empty string. Returns the empty string and raises an error if `pos > LENGTH(x) OR pos < -LENGTH(x)`. |
| `SUBSTRING(x, pos, len): String x Integer x Integer -> String` | Returns the substring of `x` starting from index `pos` (included) of length `len`. Characters' index starts from `1`. If `pos` is negative, the beginning of the substring is `pos` characters from the end of the string. If `pos` is 0, then returns the empty string. If `len` is greater than the maximum substring starting at `pos`, then return the maximum substring. Returns the empty string and raises an error if `pos > LENGTH(x) OR pos < -LENGTH(x)` or if `len` is negative. |

#### 3.5.2. Built-in Math functions

| Definition                                                 | Semantics                                                                                                                                                                                                                  |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ABS(x): Integer -> Integer` | Returns the absolute value of `x` |

### 3.6. Evaluation of the expression

Operators MUST be evaluated in order, where the parenthesized expressions have the highest priority over all the other
operators.

AND and OR operations MUST be short-circuit evaluated. When the left operand of the AND operation evaluates to `false`, the right operand MUST NOT be evaluated. Similarly, when the 
left operand of the OR operation evalues to `true`, the right operand MUST NOT be evaluated.

#### 3.7. Type casting

When the argument types of an operator/function invocation don't match the signature of the operator/function being invoked, the CESQL engine MUST try to perform an implicit cast.

This section defines an **ambiguous** operator/function as an operator/function that is overloaded with another
operator/function definition with same symbol/name and arity but different parameter types.

A CESQL engine MUST apply the following implicit casting rules in order:

1. If the operator/function is unary (argument `x`):
   1. If it's not ambiguous, cast `x` to the parameter type.
   1. If it's ambiguous, raise an error and the cast result is undefined.
1. If the operator is binary (left operand `x` and right operand `y`):
   1. If it's not ambiguous, cast `x` and `y` to the corresponding parameter types.
   1. If it's ambiguous, use the `y` type to search, in the set of ambiguous operators, every definition of the operator
      using the `y` type as the right parameter type:
      1. If such operator definition exists and is unique, cast `x` to the type of the left parameter
      1. Otherwise, raise an error and the cast results are undefined
1. If the function is n-ary with `n > 1`:
   1. If it's not ambiguous, cast all the arguments to the corresponding parameter types.
   1. If it's ambiguous, raise an error and the cast results are undefined.
1. If the operator is n-ary with `n > 2`:
   1. If it's not ambiguous, cast all the operands to the target type.
   1. If it's ambiguous, raise an error and the cast results are undefined.

For the `IN` operator, a special rule is defined: the left argument MUST be used as the target type to eventually cast the set elements.

For example, assuming `MY_STRING_PREDICATE` is a unary predicate accepting a _String_ parameter and returning a
_Boolean_, this expression:

```
MY_STRING_PREDICATE(sequence + 10)
```

MUST be evaluated as follows:

1. `sequence` is cast to _Integer_ using the same semantics of `INT`
1. `sequence + 10` is executed
1. `sequence + 10` result is cast to _String_ using the same semantics of `STRING`
1. `MY_STRING_PREDICATE` is invoked with the result of the previous point as input.

Another example, in this expression `sequence` is cast to _Integer_:

```
sequence = 10
```

`=` is an arity-2 ambiguous operator, because it's defined for `String x String`, `Boolean x Boolean` and
`Integer x Integer`. Because the right operand of the operator is an _Integer_ and there is only one `=` definition
which uses the type _Integer_ as the right parameter, `sequence` is cast to _Integer_.

## 4. Implementation suggestions

This section is meant to provide some suggestions while implementing and adopting the CloudEvents Expression Language.
It's non-normative, hence none of the below text is mandatory.

### 4.1. Error handling

Because CESQL expressions are total, they always define a return value, included in the [type system](#31-type-system), even after an error occurs.

When evaluating an expression, the evaluator can operate in two _modes_, in relation to error handling:

* Fail fast mode: When an error is triggered, the evaluation is interrupted and returns the error, without any result.
* Complete evaluation mode: When an error is triggered, the evaluation is continued, and the evaluation of the expression returns both the result and the error(s).

Choosing which evaluation mode to adopt and implement depends on the use case.

## 5. Examples

_CloudEvent including a subject_

```
EXISTS subject
```

_CloudEvent including the extension 'firstname' with value 'Francesco'_

```
firstname = 'Francesco'
```

_CloudEvent including the extension 'firstname' with value 'Francesco' or the subject with value 'Francesco'_

```
firstname = 'Francesco' OR subject = 'Francesco'
```

_CloudEvent including the extension 'firstname' with value 'Francesco' and extension 'lastname' with value 'Guardiani',
or the subject with value 'Francesco Guardiani'_

```
(firstname = 'Francesco' AND lastname = 'Guardiani') OR subject = 'Francesco Guardiani'
```

_CloudEvent including the extension 'sequence' with numeric value 10_

```
sequence = 10
```

_CloudEvent including the extension 'hop' and 'ttl', where 'hop' is smaller than 'ttl'_

```
hop < ttl
```

## 6. References

- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels

[rfc2119]: https://tools.ietf.org/html/rfc2119
[total-programming-language-wiki]: https://en.wikipedia.org/wiki/Total_functional_programming
[referential-transparency-wiki]: https://en.wikipedia.org/wiki/Referential_transparency
[ce-attribute-naming-convention]: ../cloudevents/spec.md#naming-conventions
[ce-type-system]: ../cloudevents/spec.md#type-system
[ce-id-attribute]: ../cloudevents/spec.md#id
[subscriptions-filter-dialect]: ../subscriptions/spec.md#3241-filter-dialects
[ebnf-xml-spec]: https://www.w3.org/TR/REC-xml/#sec-notation
[modulo-operation-wiki]: https://en.wikipedia.org/wiki/Modulo_operation
