# Amazon Simple Notification Service CloudEvents Adapter

This document describes how to convert [AWS SNS messages][sns-messages] into CloudEvents.

Amazon SNS MAY send a subscription confirmation, notification, or unsubscribe confirmation 
message to your HTTP/HTTPS endpoints.

Each section below describes how to determine the CloudEvents attributes
based on the specified type of SNS messages.

### Subscription Confirmation

| CloudEvents Attribute | Value                                           |
| :-------------------- | :---------------------------------------------- |
| `id`                  | "x-amz-sns-message-id" value |
| `source`              | "x-amz-sns-topic-arn" value |
| `specversion`         | `1.0`                                           |
| `type`                | `com.amazonaws.sns.` + "x-amz-sns-message-type" value    |
| `datacontenttype`     | `application/json`         |
| `dataschema`          | Omit                                            |
| `subject`             | Omit                        |
| `time`                | "Timestamp" value                               |
| `data`                | HTTP payload                                       |

### Notification

| CloudEvents Attribute | Value                                           |
| :-------------------- | :---------------------------------------------- |
| `id`                  | "x-amz-sns-message-id" value |
| `source`              | "x-amz-sns-subscription-arn" value |
| `specversion`         | `1.0`                                           |
| `type`                | `com.amazonaws.sns.` + "x-amz-sns-message-type" value    |
| `datacontenttype`     | `application/json`         |
| `dataschema`          | Omit                                            |
| `subject`             | "Subject" value (if present)                    |
| `time`                | "Timestamp" value                               |
| `data`                | HTTP payload                                       |

### Unsubscribe Confirmation

| CloudEvents Attribute | Value                                           |
| :-------------------- | :---------------------------------------------- |
| `id`                  | "x-amz-sns-message-id" value |
| `source`              | "x-amz-sns-subscription-arn" value |
| `specversion`         | `1.0`                                           |
| `type`                | `com.amazonaws.sns.` + "x-amz-sns-message-type" value    |
| `datacontenttype`     | `application/json`         |
| `dataschema`          | Omit                                            |
| `subject`             | Omit                    |
| `time`                | "Timestamp" value                               |
| `data`                | HTTP payload                                       |

[sns-messages]: https://docs.aws.amazon.com/sns/latest/dg/sns-message-and-json-formats.html