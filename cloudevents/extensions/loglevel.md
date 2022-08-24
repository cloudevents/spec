# Log Level Extension


## Attributes

### loglevelname 

- Type: `String`
- Description: Human readable representation of the log level
- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be lowercase
  - RECOMMENDED values include   `emergency`, `alert` , `critical` ,`error`, `warning`, `notice`, `info`, `debug`, and
     `verbose` , but  others MAY be used. The recommended 
  - SHOULD have a many-to-one relationship with a distinct `loglevelnum` in the scope of
   the `source`

### loglevelnum 

- Type: `Integer`

- Description: A numerical representation of the level of importance of the event. 
    Conforms to the severity ordering specified by [RFC5424](https://www.rfc-editor.org/rfc/rfc5424.html#section-6.2.1): severity of all levels is
     assumed to be numerically ascending from most important to least important.
  This specification does not define "importance" or meaning of each value other than
  an event with a lower numerical value MUST be of more importance than an event with
  a lower numerical value in the same `source`.

- Constraints
  - OPTIONAL
  - if present, MUST NOT be negative
  - RECOMMENDED values include
    - `0` for `emergency`
    - `1` for `alert`
    - `2` for `critical`
    - `3` for `error`
    - `4` for `warning`
    - `5` for `notice`
    - `6` for `info`
    - `7` for `debug`
    - `8` for `verbose`


## RECOMMENDED Log Mappings

### Syslog

All syslog log records SHOULD assign the severity level to `loglevelnum`. In addition to that

The corresponding `loglevelname`s to each of the severity values

| Syslog Severity | `loglevelname` |
| --------------- | -------------- |
| 0               | `emergency`    |
| 1               | `alert`        |
| 2               | `critical`     |
| 3               | `error`        |
| 4               | `warning`      |
| 5               | `notice`       |
| 7               | `info`         |
| 8               | `debug`        |



### Windows Event Log
Binding SHOULD NOT depend on the internal `Level` integer value of the log record as it defined by the windows event producer. 

Instead cloud event producers SHOULD use the following `loglevelnum`s instead of the winlog `Level` values

| Windows Event Level Name | `loglevelname` | `loglevelnum` |
| ------------------------ | -------------- | ------------- |
| `Critical`               | `critical`     | 2             |
| `Error`                  | `error`        | 3             |
| `Warning`                | `warning`      | 4             |
| `Information`            | `info`         | 7             |
| `Verbose`                | `verbose`      | 9             |

### Python Logging
|            | `loglevelname` | `loglevelnum` |
| ---------- | -------------- | ------------- |
| `CRITICAL` | `critical`     | 2             |
| `FATAL`    | `critical`     | 2             |
| `ERROR`    | `error`        | 3             |
| `WARN`     | `warning`      | 4             |
| `WARNING`  | `warning`      | 4             |
| `INFO`     | `info`         | 7             |
| `DEBUG`    | `debug`        | 8             |
| `NOTSET`   | `verbose`      | 9             |

### Spring (Java)

Spring supports 5 default log levels, `ERROR`, `WARN`, `INFO`, `DEBUG`, and `TRACE`, with `INFO` being the default log level configuration.

|         | `loglevelname` | `loglevelnum` |
| ------- | -------------- | ------------- |
| `ERROR` | `error`        | 3             |
| `WARN`  | `warning`      | 4             |
| `INFO`  | `info`         | 7             |
| `DEBUG` | `debug`        | 8             |
| `TRACE` | `verbose`      | 9             |

### Serilog (.NET)

`Fatal`, `Error`, `Warning`, `Information`, `Debug` and `Verbose` 

|               | `loglevelname` | `loglevelnum` |
| ------------- | -------------- | ------------- |
| `Fatal`       | `critical`     | 2             |
| `Error`       | `error`        | 3             |
| `Warning`     | `warning`      | 4             |
| `Information` | `info`         | 7             |
| `Debug`       | `debug`        | 8             |
| `Verbose`     | `verbose`      | 9             |

### Winston (Javascript)

| Winston Level Name | `loglevelname` | `loglevelnum` |
| ------------------ | -------------- | ------------- |
| `error`            | `error`        | 3             |
| `warn`             | `warning`      | 4             |
| `info`             | `info`         | 7             |
| `http`             | `http`         | 8             |
| `verbose`          | `verbose`      | 9             |
| `debug`            | `debug`        | 10            |
| `silly`            | `silly`        | 11            |



### Spdlog (C++)

| Spdlog  Level | `loglevelname` | `loglevelnum` |
| ------------- | -------------- | ------------- |
| `critical`    | `critical`     | 2             |
| `error`       | `error`        | 3             |
| `warn`        | `warning`      | 4             |
| `info`        | `info`         | 7             |
| `debug`       | `debug`        | 8             |
| `trace`       | `verbose`      | 9             |



### Zap (Go)
Zap supports seven types of log levels which are  `Debug`, `Info`, `Warning`, `Error`,
 `DPanic`, `Panic`, and `Fatal`

| Zap Level | `loglevelname` | `loglevelnum` |
| --------- | -------------- | ------------- |
| `Fatal`   | `fatal`        | 1             |
| `Panic`   | `critical`     | 2             |
| `DPanic`  | `critical`     | 2             |
| `error`   | `error`        | 3             |
| `warn`    | `warning`      | 4             |
| `info`    | `info`         | 7             |
| `debug`   | `debug`        | 8             |