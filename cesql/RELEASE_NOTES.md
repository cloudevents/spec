# CESQL Release Notes

<!-- no verify-specs -->

## v1.0.0 - 2024/06/13
This is the v1 release of the specification! CESQL v1 provides users with the
ability to write and execute queries against CloudEvents. This allows for
computing values and matchins of CloudEvent attributes against complex
expressions that lean on the syntax of Structured Query Language (SQL).

Notable changes between the WIP draft and the v1 specification are:
- Specify error types
- Clarify return values of expressions that encounter errors
- Clarify that missing attributes result in an error and the expression
  returning it's default value
- Add support for boolean to integer and integer to boolean type casting
- Clarify the order of operations
- Clarify how user defined functions work
- Define the default "zero" values for the built in types
- Clarify that string comparisons are case sensitive
- Specify which characters are treated as whitespace for the TRIM function
- Specify that functions must still return values along with errors, as well as
  the behaviour when user defined function do not do this correctly
- For the fail fast error handling mode, expressions now return the zero value
  for their return type when they encounter an error, rather than undefined
