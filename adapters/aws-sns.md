# AWS Simple Notification Service CloudEvents Adapter

This document describes how to convert
[AWS SNS notifications](https://docs.aws.amazon.com/sns/latest/api/Welcome.html)
into a CloudEvents.

AWS SNS notification documentation:
https://docs.aws.amazon.com/sns/latest/api/Welcome.html

All SNS notifications are converted into CloudEvents using the
same pattern as described in the following table:

| CloudEvents Attribute | Value                                           |
| :-------------------- | :---------------------------------------------- |
| `id`                  | "x-amz-sns-message-id" value                    |
| `source`              | "x-amz-sns-topic-arn" value                     |
| `specversion`         | `0.3-wip`                                       |
| `type`                | `com.amazonaws.aws.` + "x-amz-sns-message-type" value |
| `datacontentencoding` | Omit                                            |
| `datacontenttype`     | "Content-Type" value                            |
| `schemaurl`           | Omit                                            |
| `subject`             | "x-amz-sns-subscription-arn" value              |
| `time`                | Current time                                    |
| `data`                | Content of HTTP request body                    |

