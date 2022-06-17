# AWS Simple Storage Service CloudEvents Adapter

本文档介绍如何将 [AWS S3 events](https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html) 事件转换为 CloudEvents。

AWS S3 事件文档：
https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html

所有 S3 事件都通过下表中描述的模式转换为 CloudEvents：

| CloudEvents 属性 | 值                                                        |
| :-------------------- | :----------------------------------------------------------- |
| `id`                  | "responseElements.x-amz-request-id" + `.` + "responseElements.x-amz-id-2" |
| `source`              | "eventSource" value + `.` + "awsRegion" value + `.` + "s3.buckets.name" value |
| `specversion`         | `1.0`                                                        |
| `type`                | `com.amazonaws.s3.` + "eventName" value                      |
| `datacontenttype`     | S3 event type (e.g. `application/json`)                      |
| `dataschema`          | Omit                                                         |
| `subject`             | "s3.object.key" value                                        |
| `time`                | "eventTime" value                                            |
| `data`                | S3 event                                                     |

注释：
- 当事件来自 S3 时，“eventSource”将始终为固定值 (`aws:s3`)，但如果其他云厂商支持 S3 事件格式，则该值可能不会是 `aws:s3` - 而是特定于他们的环境的东西。

- 因此，这些事件的消费者将能够通过检测 `type` 属性上的 `com.amazonaws.s3` 前缀知道事件是否是 S3 类型的事件（无论它来自 S3 还是 S3 兼容的提供者）。