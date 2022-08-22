# Log Level Extension


## Attributes

### loglevelname 

- Type: `String`
- Description: Human readable representation of the log level
- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be lowercase
  - RECOMMENDED values include `critical` ,`error`, `warning`, `info`, `debug`, and
   `verbose` , but  others MAY be used
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

All syslog log records SHOULD assign the severity level to `loglevelnum`. In addition to that

The corresponding `loglevelname`s to each of the `loglevelnums` are:

| `loglevelnum` | `loglevelname` |
| ------------- | -------------- |
| 0             | `emergency`    |
| 1             | `alert`        |
| 2             | `critical`     |
| 3             | `error`        |
| 4             | `warning`      |
| 5             | `notice`       |
| 7             | `info`         |
| 8             | `debug`        |



### Windows Event Log
, `Error`, `Warning`, `Information` and `Verbose` 

Binding SHOULD NOT depend on the internal `Level` integer value of the log record as it defined by the windows event producer. 

Instead cloud event producers SHOULD use the following `loglevelnum`s instead of the winlog values

| `loglevelnum` | `loglevelname` | `Event Log Name` |
| ------------- | -------------- | ---------------- |
| 2             | `critical`     | `Critical`       |
| 3             | `error`        | `Error`          |
| 4             | `warning`      | `Warning`        |
| 7             | `info`         | `Information`    |
| 8             | `verbose`      | `Verbose`        |




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