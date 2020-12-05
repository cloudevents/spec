# Error CloudEvents Adapter

This document describes how to Errors events into a CloudEvents.

## Table of Contents

- [Error CloudEvents Adapter](#error-cloudevents-adapter)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Context Attributes Extension](#context-attributes-extension)
    - [dataschema](#dataschema)
    - [data](#data)
  - [Event Data](#event-data)
    - [errormessage](#errormessage)
    - [errorlink](#errorlink)
    - [metadata](#metadata)
  - [Example](#example)

## Purpose

Errors are everywhere. However, error's producers tend to describe errors
differently.

The lack of a common way of describing errors means developers are continually
re-learning how to consume errors. That also limits the potential for libraries,
tooling, and infrastructure to aid of error data across delivery environments,
like SDK or logger systems. The portability and productivity that can be
achieved from error data are hindered overall.

This ADR is a specification for describing error data in standard formats to
provide interoperability across services, platforms, and systems.

## Context Attributes Extension

### dataschema

- Constraints:
  - REQUIRED
  - MUST be https://github.com/cloudevents/spec/tree/v1.0/adapters/error/dataschema.json"

### data

- Constraints:
  - REQUIRED

## Event Data

### errormessage

- Type: String
- Description: contains a generic description of the error condition in English.
  It is intended for a human audience. Simple programs display the message
  directly to the end user if they encounter an error condition they don't know
  how or don't care to handle. Sophisticated programs with more exhaustive error
  handling and proper internationalization are more likely to ignore the error
  message.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

### errorlink

- Type: URI
- Description: URL to documentation related to the error.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

### metadata

- Type: Object
- Description: The metadata associated to the error.
- Constraints:
  - OPTIONAL
  - If present, MUST be an object

## Example

The following example shows a CloudEvent Error serialized as JSON:

```json
{
    "specversion" : "1.x-wip",
    "id" : "YH9UUdlCjQztui7untrQE",
    "type" : "com.straw-hat-team.sso.not_found",
    "source" : "https://github.com/straw-hat-team/sso",
    "time" : "2018-04-05T17:31:00Z",
    "subject" : "/account",
    "datacontenttype" : "application/json",
    "data" : "{
      \"errormessage\":\"Resource not found\",
      \"errorlink\":\"https://github.com/straw-hat-team/sso/docs/errors/E0000008.md\",
      \"metadata\":{
        \"account_id\":\"something\"
      }
    }"
}
```

You may use a `subject` that identify particular field from the input data.
The following example shows a CloudEvent Error serialized as JSON:

```jsonc
{
    "specversion" : "1.x-wip",
    "id" : "e8QIbN7KDaQDSagrWM8d8",
    "type" : "com.straw-hat-team.payment.insufficient_fund",
    "source" : "https://github.com/straw-hat-team/payment",
    "time" : "2018-04-05T17:31:00Z",
    "subject" : "/payment/amount",
    "datacontenttype" : "application/json",
    "data" : "{
      \"errormessage\":\"You can not transfer an amount greater than the current balance\",
      \"errorlink\":\"https://github.com/straw-hat-team/payment/docs/errors/E0000001.md\",
      \"metadata\":{
        \"amount_requested\":\"500000\",
        \"current_balance\":\"200000\"
      }
    }"
}
```
