# Log Level Extension


## Attributes

### loglevelname 

- Type: `String`
- Description: Human readable representation of the log level
- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be uppercase
  - RECOMMENDED values include `INFO`, `ERROR`, `WARNING`, `VERBOSE` and `DEBUG`, but
   others MAY be used
  - SHOULD have a many-to-one relationship with a distinct `loglevelnum` in the scope of
   the `source`

### loglevelnum 

- Type: `Integer`

- Description: A numerical representation of the level of importance of the event. 
    Conforms to the severity ordering specified by RFC5424: severity of all levels is
     assumed to be numerically ascending from most important to least important.
  This specification does not define "importance" or meaning of each value other than
  an event with a higher numerical value MUST be of more importance than an event with
  a lower numerical value in the same `source`.

- Constraints
  - OPTIONAL
  - if present, MUST NOT be negative


## Example Log Mappings

### Syslog RFC5424
```text
  0       Emergency: system is unusable
  1       Alert: action must be taken immediately
  2       Critical: critical conditions
  3       Error: error conditions
  4       Warning: warning conditions
  5       Notice: normal but significant condition
  6       Informational: informational messages
  7       Debug: debug-level messages
``` 

### Windows Event Log
`Critical`, `Error`, `Warning`, `Information` and `Verbose` 
Level num is dependent on producer but SHOULD  assumed to be numerically ascending
 from most important (`Critical`) to least important (`Verbose`)


### Serilog (.NET)
`Fatal`, `Error`, `Warning`, `Information`, `Debug` and `Verbose` 
No ordering is defined

### Python Logging
Level num iis numerically DESCENDING from most important (`CRITICAL`) to least
 important (`NOTSET`)

```json
 {
    "CRITICAL": 50,
    "FATAL": 50,
    "ERROR": 40,
    "WARN": 30,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0
}
```

### Winston (Javascript)
```json
{
  "error": 0,
  "warn": 1,
  "info": 2,
  "http": 3,
  "verbose": 4,
  "debug": 5,
  "silly": 6
}
```

### Spring (Java)
Spring supports 5 default log levels, `ERROR`, `WARN`, `INFO`, `DEBUG`, and `TRACE`, with `INFO` being the default log level configuration.

### Spdlog (C++)
```json
{
"trace": 0,
"debug": 1,
"info": 2,
"warn": 3,
"error": 4,
"critical": 5,
"off": 6
}
```
### Zap (Go)
Zap supports seven types of log levels which are  `Debug`, `Info`, `Warning`, `Error`,
 `DPanic`, `Panic`, and `Fatal`