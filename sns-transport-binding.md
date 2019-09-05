# Amazon SNS Transport Binding for CloudEvents - Version 0.4-wip

## Abstract

The [Amazon SNS][SNS] Transport Binding for CloudEvents 
defines how events are mapped to both SNS messages (and more specifically to
[SNS Publish API call][SNS-Publish]).

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to SNS](#12-relation-to-sns)
- 1.3. [Message structure](#13-message-structure)
- 1.4. [Security](#14-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [data](#21-data)
3. [SNS Publish API call Mapping](#3-sns-publish-api-call-mapping)
- 3.1. [TargetArn or TopicArn Parameter](#31-targetarn-or-topicarn-parameter)
- 3.2. [MessageAttributes Parameter](#32-messageattributes-parameter)
- 3.3. [Message Parameter in *string* mode](#33-message-parameter-in-string-mode)
- 3.4. [Message Parameter in *json* mode](#34-message-parameter-in-json-mode)
- 3.5. [Examples](#35-examples)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in the
SNS APIs.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to SNS

This specification does not prescribe rules constraining transfer or settlement
of event messages with SNS; it solely defines how CloudEvents are expressed
in the [SNS Publish API calls][SNS-Publish].

### 1.3. Message Structure

The specification defines two modes for transferring events:
*string* (if you want to send the same message to all transport protocols) 
and *json* (if you want to send different messages for each transport protocol).

Options *string* is used by default in [Amazon SNS][SNS]. Option *json* is set
by using `MessageStructure` request parameter, that if present must have 
`json` value.

In both modes, the value of the event `data` MUST be
placed:

1. as-is, if represented by UTF-8 encoded string
2. base64-encoded otherwise

The `ce_datacontenttype` message attribute value MUST declare its media type
(and `ce_datacontentencoding` message attribute MUST be present and set to 
`base64` if base64-encoded); all other event attributes MUST be mapped to the 
[SNS message attributes][SNS-Publish-Request].

The default content type for SNS is *applicatoin/json*. When `ce_datacontenttype`
attribute is omitted, data follows the JSON format's encoding rules. The data 
value can therefore be a JSON object, array, or value.

In the *string* content mode, the value of the event `data` MUST be
placed directly into the SNS Message request parameter.

In the *json* content mode, event `data` MUST be placed under `default` 
key of JSON payload. In the same time following delivery 
protocols MUST NOT override the default message:
- `sqs`
- `lambda`
- `http`
- `https`

### 1.4. Security

This specification does not introduce any new security features, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

### 2.1. data

`data` is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into SNS as defined in this
specification, SNS provides data available as a string.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data`
value is made available as [UTF-8][RFC3629] encoded JSON text.

## 3. SNS Publish API call Mapping

Message structure (*string* or *json*) is chosen by the sender of the 
event. It doesn't affect the receiver.

### 3.1 TargetArn or TopicArn Parameter

The value is just [Amazon Resource Name][ARN] of the [Amazon SNS][SNS] 
instance, that messages should be sent to. 

### 3.2 MessageAttributes Parameter

All [CloudEvents][CE] attributes and
[CloudEvent Attributes Extensions](primer.md#cloudevent-attribute-extensions) 
with exception of `data` MUST be individually mapped to and from the message 
attribute.

There is a limit of maximum 10 message attributes in [Amazon SNS][SNS] service.
Therefore number of [CloudEvents][CE] attributes MUST be less than or equal to 10 
and SHOULD be limited to the lowest possible value.    

#### 3.2.1 MessageAttributes Names

CloudEvent attributes MUST be prefixed with `ce_` for use in the
MessageAttributes.

Examples:

* `time` maps to `ce_time`
* `id` maps to `ce_id`
* `specversion` maps to `ce_specversion`

#### 3.2.2 Property Values

The value of each message attribute is constructed according to [SNS message
attribute value format][SNS-MessageAttributeValue] specification.

#### 3.2.3 Example

```json
{
  "MessageAttributes": {
    "ce_id": {
      "DataType": "String",
      "StringValue": "1234-1234-1234"
    },
    "ce_source": {
      "DataType": "String",
      "StringValue": "/mycontext/subcontext"
    },
    "ce_specversion": {
        "DataType": "String",
        "StringValue": "0.4-wip"
    },
    "ce_type": {
      "DataType": "String",
      "StringValue": "com.example.someevent"
    },
    "ce_time": {
      "DataType": "String",
      "StringValue": "2018-04-05T03:56:24Z"
    },
    "ce_datacontenttype": {
      "DataType": "String",
      "StringValue": "application/avro"
    },
    "custom-attribute": {
      "DataType": "String",
      "StringValue": "foo"
    },
    ...
    
  },
  ...
}
```




### 3.3. Message Parameter in *string* mode

The *string* mode is used by default in [Amazon SNS][SNS]. It uses the same
message for all transport protocols.


#### Example

```json
{
    "MessageAttributes": {
      ...,
      "ce_datacontenttype": {
        "DataType": "String",
        "StringValue": "application/avro"
      },
      "ce_datacontentencoding": {
        "DataType": "String",
        "StringValue": "base64"
      },
      ...
    },
    "Message": "...", // base64 encoded avro format
}
```

### 3.4. Message Parameter in *json* mode

Option json is set by using `MessageStructure` request parameter, that if 
present must have `json` value.

It allows to use non-standard formats of notification for transport protocols 
where CloudEvents specification makes no sense, e.g. ones, that deliver message 
to end user (email, user).

#### Example

```json
{
    "MessageAttributes": {
      ...,
      "ce_datacontenttype": {
        "DataType": "String",
        "StringValue": "application/avro"
      },
      "ce_datacontentencoding": {
        "DataType": "String",
        "StringValue": "base64"
      },
      ...
    },
    "MessageStructure": "json",
    "Message": {
        "default": "...", // base64 encoded avro format
        "email": "Sample message for email",
        "sms": "Sample message for SMS"
    }
}
```

### 3.5 Examples

#### 3.5.1 The simplest 

```json
{
  "TopicArn": "arn:aws:sns:us-east-2:1234567890:My-Topic",
  "MessageAttributes": {
    "ce_id": {
      "DataType": "String",
      "StringValue": "1234-1234-1234"
    },
    "ce_source": {
      "DataType": "String",
      "StringValue": "/mycontext/subcontext"
    },
    "ce_specversion": {
        "DataType": "String",
        "StringValue": "0.4-wip"
    },
    "ce_type": {
      "DataType": "String",
      "StringValue": "com.example.someevent"
    }
  },
  "Message": "Simple JSON value - string"
}
```


#### 3.5.2 Default JSON 

```json
{
  "TopicArn": "arn:aws:sns:us-east-2:1234567890:My-Topic",
  "MessageAttributes": {
    "ce_id": {
      "DataType": "String",
      "StringValue": "1234-1234-1234"
    },
    "ce_source": {
      "DataType": "String",
      "StringValue": "/mycontext/subcontext"
    },
    "ce_specversion": {
        "DataType": "String",
        "StringValue": "0.4-wip"
    },
    "ce_type": {
      "DataType": "String",
      "StringValue": "com.example.someevent"
    }
  },
  "Message": {
    "example": true,
    "foo": "bar"
  }
}
```


#### 3.5.3 Avro 

```json
{
    "TopicArn": "arn:aws:sns:us-east-2:1234567890:My-Topic",
    "MessageAttributes": {
        "ce_id": {
            "DataType": "String",
            "StringValue": "1234-1234-1234"
        },
        "ce_source": {
            "DataType": "String",
            "StringValue": "/mycontext/subcontext"
        },
        "ce_specversion": {
            "DataType": "String",
            "StringValue": "0.4-wip"
        },
        "ce_type": {
            "DataType": "String",
            "StringValue": "com.example.someevent"
        },
        "ce_time": {
            "DataType": "String",
            "StringValue": "2018-04-05T03:56:24Z"
        },
        "ce_datacontenttype": {
            "DataType": "String",
            "StringValue": "application/avro"
        },
        "ce_datacontentencoding": {
            "DataType": "String",
            "StringValue": "base64"
        },
        "customAttributeArray": {
            "DataType": "String.Array",
            "StringValue": "[\"foo\", \"bar\"]"
        }
    },
    "Message": "..." // base64 encoded avro format
}
```


## 4. References

- [SNS][SNS] Amazon Simple Notification Service
- [SNS Publish][SNS-Publish] SNS Publish API reference
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[CE]: ./spec.md
[ARN]: https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
[JSON-format]: ./json-format.md
[SNS]: https://docs.aws.amazon.com/sns/latest/api/Welcome.html
[SNS-Publish]: https://docs.aws.amazon.com/sns/latest/api/API_Publish.html
[SNS-Publish-Request]: https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters
[SNS-Message-Attributes]: https://docs.aws.amazon.com/sns/latest/dg/sns-message-attributes.html
[SNS-MessageAttributeValue]: https://docs.aws.amazon.com/sns/latest/api/API_MessageAttributeValue.html
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC7159]: https://tools.ietf.org/html/rfc7159
