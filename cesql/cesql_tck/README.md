# CloudEvents Expression Language TCK

Each file of this TCK contains a set of test cases, testing one or more specific features of the language.

The root file structure is composed by:

* `name`: Name of the test suite contained in the file
* `tests`: List of tests

Each test definition includes:

* `name`: Name of the test case
* `expression`: Expression to test.
* `result`: Expected result (OPTIONAL). Can be a boolean, an integer or a string.
* `error`: Expected error (OPTIONAL). If absent, no error is expected.
* `event`: Input event (OPTIONAL). If present, this is a valid event serialized in JSON format. If absent, when testing
  the expression, any valid event can be passed.
* `eventOverrides`: Overrides to the input event (OPTIONAL). This might be used when `event` is missing, in order to
  define only some specific values, while the other (REQUIRED) attributes can be any value.

The `error` values could be any of the following:

* `parse`: Error while parsing the expression
* `math`: Math error while evaluating a math operator
* `cast`: Casting error
* `missingFunction`: Addressed a missing function
* `functionEvaluation`: Error while evaluating a function
