# Log Level Extension

## Abstract
This extension defines attributes that MAY be included within a CloudEvent
to describe the "level" or "importance" of an event in relation to other events
produced by a unique event source.

Often systems produce events in form of logs, and these types of events usually share
a common concept of "log-level". This extension aims to provide a standard way for 
describing this property in a language agnostic form. 

Sharing a common way to describe importance of events allows for better monitoring 
systems, tooling and general log consumption.

In addition to defining the extension attributes, this document defines 
the concept of [Log Level Bindings](#log-level-bindings) - a standard way to map 
well-known log level names from different languages and frameworks 
onto the `loglevelname` and `loglevelnum` values defined in this spec. 

## Attributes

All attributes of this extension are OPTIONAL. however, when using this 
custom extension you MUST use at-least one of these OPTIONAL attributes. 

### loglevelname 

- Type: `String`
- Description: Human readable representation of the log level
- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be lowercase
  - RECOMMENDED values include `emergency`, `alert`, `critical`, `error`, 
    `warning`, `notice`, `info`, `debug`, and `verbose`, but  others MAY be used.
  - SHOULD have a one-to-one relationship with a distinct `loglevelnum` in the scope of
   the `source`

### loglevelnum 

- Type: `Integer`
- Description: A numerical representation of the level of importance of the event. 
  Conforms to the severity ordering specified by 
  [RFC5424](https://www.rfc-editor.org/rfc/rfc5424.html#section-6.2.1): severity of
  all levels is assumed to be numerically ascending from most important to least
  important.
  This specification does not define "importance" or meaning of each value other than
  an event with a lower numerical value MUST be of more importance than an event with
  a higher numerical value in the same `source`.

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

## Log Level Bindings

A standard way to map well-known log level names from different languages and 
frameworks onto the `loglevelname` and `loglevelnum` values defined in this spec. 

Each binding defines the unique log name and/or log number in a framework and the 
corresponding RECOMMENDED `loglevelname` and `loglevelnum`.

### RECOMMENDED Log Bindings

#### Syslog

All syslog log records SHOULD assign the severity level to `loglevelnum`. 
In addition to that The corresponding `loglevelname`s to each of the severity values

| Syslog Severity | `loglevelname` | `loglevelnum` |
| --------------- | -------------- | ------------- |
| 0               | `emergency`    | 0             |
| 1               | `alert`        | 1             |
| 2               | `critical`     | 2             |
| 3               | `error`        | 3             |
| 4               | `warning`      | 4             |
| 5               | `notice`       | 5             |
| 6               | `info`         | 6             |
| 7               | `debug`        | 7             |

#### Windows Event Log
Binding SHOULD NOT depend on the internal `Level` integer value of the log 
record as it is defined by the windows event producer. 

Instead, cloudevent producers SHOULD use the following `loglevelnum`s instead of 
the windows event log record `Level` values.

| Windows Event Level | `loglevelname` | `loglevelnum` |
| ------------------- | -------------- | ------------- |
| `Critical`          | `critical`     | 2             |
| `Error`             | `error`        | 3             |
| `Warning`           | `warning`      | 4             |
| `Information`       | `info`         | 6             |
| `Verbose`           | `verbose`      | 8             |

#### Python
| Python Log Level | `loglevelname` | `loglevelnum` |
| ---------------- | -------------- | ------------- |
| `CRITICAL`       | `critical`     | 2             |
| `FATAL`          | `critical`     | 2             |
| `ERROR`          | `error`        | 3             |
| `WARN`           | `warning`      | 4             |
| `WARNING`        | `warning`      | 4             |
| `INFO`           | `info`         | 6             |
| `DEBUG`          | `debug`        | 7             |
| `NOTSET`         | `verbose`      | 8             |

#### Java (Spring)
| Sprint Log Level | `loglevelname` | `loglevelnum` |
| ---------------- | -------------- | ------------- |
| `ERROR`          | `error`        | 3             |
| `WARN`           | `warning`      | 4             |
| `INFO`           | `info`         | 6             |
| `DEBUG`          | `debug`        | 7             |
| `TRACE`          | `verbose`      | 8             |

#### .NET (Serilog)
| Serilog Log Level | `loglevelname` | `loglevelnum` |
| ----------------- | -------------- | ------------- |
| `Fatal`           | `critical`     | 2             |
| `Error`           | `error`        | 3             |
| `Warning`         | `warning`      | 4             |
| `Information`     | `info`         | 6             |
| `Debug`           | `debug`        | 7             |
| `Verbose`         | `verbose`      | 8             |

#### Javascript (Winston)
| Winston Log Level | `loglevelname` | `loglevelnum` |
| ----------------- | -------------- | ------------- |
| `error`           | `error`        | 3             |
| `warn`            | `warning`      | 4             |
| `info`            | `info`         | 6             |
| `http`            | `http`         | 7             |
| `verbose`         | `verbose`      | 8             |
| `debug`           | `debug`        | 9             |
| `silly`           | `silly`        | 10            |

#### C++ (Spdlog)
| Spdlog Log Level | `loglevelname` | `loglevelnum` |
| ---------------- | -------------- | ------------- |
| `critical`       | `critical`     | 2             |
| `error`          | `error`        | 3             |
| `warn`           | `warning`      | 4             |
| `info`           | `info`         | 6             |
| `debug`          | `debug`        | 7             |
| `trace`          | `verbose`      | 8             |

#### Go (Zap)
| Zap Log Level | `loglevelname` | `loglevelnum` |
| ------------- | -------------- | ------------- |
| `Fatal`       | `fatal`        | 1             |
| `Panic`       | `critical`     | 2             |
| `DPanic`      | `critical`     | 2             |
| `error`       | `error`        | 3             |
| `warn`        | `warning`      | 4             |
| `info`        | `info`         | 6             |
| `debug`       | `debug`        | 7             |