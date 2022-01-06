# AWS Simple Storage Service CloudEvents Adapter

This document describes how to convert
[AWS S3 events](https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html)
into CloudEvents.

AWS S3 event documentation:
https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html

All S3 events are converted into CloudEvents using the
same pattern as described in the following table:

| CloudEvents Attribute | Value                                           |
| :-------------------- | :---------------------------------------------- |
| `id`                  | "responseElements.x-amz-request-id" + `.` + "responseElements.x-amz-id-2" |
| `source`              | "eventSource" value + `.` + "awsRegion" value + `.` + "s3.buckets.name" value  |
| `specversion`         | `1.0`                                           |
| `type`                | `com.amazonaws.s3.` + "eventName" value         |
| `datacontenttype`     | S3 event type (e.g. `application/json`)         |
| `dataschema`          | Omit                                            |
| `subject`             | "s3.object.key" value                           |
| `time`                | "eventTime" value                               |
| `data`                | S3 event                                        |

Comments:
- While the "eventSource" value will always be static (`aws:s3`) when
  the event is coming from S3, if some other cloud provider is supporting
  the S3 event format it is expected that this value will not be
  `aws:s3` for them - it is expected to be something specific to their
  environment.
- Consumers of these events will therefore be able to know if the event
  is an S3 type of event (regardless of whether it is coming from S3 or
  an S3-compatible provider) by detecting the `com.amazonaws.s3` prefix
  on the `type` attribute.
