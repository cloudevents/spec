# Log Level Extension



## Attributes

### loglevelname 

- Type: `String`
- Description: Human readable representation of the log level
- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be uppercase
  - RECOMMENDED values include `INFO`, `ERROR`, `WARNING` and `DEBUG`, but others MAY
   be used
  - SHOULD have a one-to-one relationship with a distinct `loglevelnum` in the scope of
   the `source`

### loglevelnum 

- Type: `Integer`

- Description: A numerical representation of the level of importance of the event. 
  This specification does not define "importance" or meaning of each value other than
  an event with a higher numerical value MUST be of more importance than an event with
  a lower numerical value in the same `source`.

- Constraints
  - OPTIONAL
  - if present, MUST NOT be negative
