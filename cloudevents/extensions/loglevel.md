# Log Level Extension



## Attributes

### levelname (or loglevelname)

- Type: `String`
- Description: Human readable representation of  the log level
- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be uppercase
  - MAY be `INFO`
  - SHOULD NOT be `INFORMATION`
  - MAY be `ERROR`
  - SHOULD NOT be `ERR`
  - MAY be `WARNING`
  - SHOULD NOT be `WARN`
  - SHOULD have a one-to-one relationship with a distinct levelnum in the scope of the producer

### levelnum (or loglevelnum)

- Type: `Integer`

- Description: Number representation of the level of the event, the higher the level is the event has a higher importance

  ​		The meaning of each value is defined by the producer. 

- Constraints

  - OPTIONAL
  - if present, MUST NOT be negative
