# Gitlab CloudEvents Adapter

This document describes how to convert
[Gitlab webhook events](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#events)
into a CloudEvents.

Gitlab webhook event documentation:
https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#events

Each section below describes how to determine the CloudEvents attributes
based on the specified event.

## Push Event

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID |
| `source`              | "repository.homepage" value              |
| `specversion`         | `0.3-wip`                                |
| `type`                | `com.gitlab.push`                        |
| `datacontentencoding` | Omit                                     |
| `datacontenttype`     | `application/json`                       |
| `schemaurl`           | Omit                                     |
| `subject`             | "checkout_sha" value                     |
| `time`                | Current time                             |
| `data`                | Content of HTTP request body             |

## Tag Event

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID |
| `source`              | "repository.homepage" value              |
| `specversion`         | `0.3-wip`                                |
| `type`                | `com.gitlab.tag_push`                    |
| `datacontentencoding` | Omit                                     |
| `datacontenttype`     | `application/json`                       |
| `schemaurl`           | Omit                                     |
| `subject`             | "ref" value                              |
| `time`                | Current time                             |
| `data`                | Content of HTTP request body             |

## Issue Event

| CloudEvents Attribute | Value                                                 |
| :-------------------- | :---------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID              |
| `source`              | "repository.homepage" value                           |
| `specversion`         | `0.3-wip`                                             |
| `type`                | `com.gitlab.issue.` + "object_attributes.state" value |
| `datacontentencoding` | Omit                                                  |
| `datacontenttype`     | `application/json`                                    |
| `schemaurl`           | Omit                                                  |
| `subject`             | "object_attributes.iid" value                         |
| `time`                | Current time                                          |
| `data`                | Content of HTTP request body                          |

## Comment on Commit Event

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID |
| `source`              | "commit.url" value                       |
| `specversion`         | `0.3-wip`                                |
| `type`                | `com.gitlab.note.commit`                 |
| `datacontentencoding` | Omit                                     |
| `datacontenttype`     | `application/json`                       |
| `schemaurl`           | Omit                                     |
| `subject`             | "object_attributes.id" value             |
| `time`                | "object_attributes.created_at" value     |
| `data`                | Content of HTTP request body             |

## Comment on Merge Request Event

| CloudEvents Attribute | Value                                                        |
| :-------------------- | :----------------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID                     |
| `source`              | "object_attributes.url" value, without the `#note\_...` part |
| `specversion`         | `0.3-wip`                                                    |
| `type`                | `com.gitlab.note.merge_request`                              |
| `datacontentencoding` | Omit                                                         |
| `datacontenttype`     | `application/json`                                           |
| `schemaurl`           | Omit                                                         |
| `subject`             | "object_attributes.id" value                                 |
| `time`                | "object_attributes.created_at` value                         |
| `data`                | Content of HTTP request body                                 |

## Comment on Issue Event

| CloudEvents Attribute | Value                                                       |
| :-------------------- | :---------------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID                    |
| `source`              | "object_attributes.url" value without the `#note\_...` part |
| `specversion`         | `0.3-wip`                                                   |
| `type`                | `com.gitlab.note.issue`                                     |
| `datacontentencoding` | Omit                                                        |
| `datacontenttype`     | `application/json`                                          |
| `schemaurl`           | Omit                                                        |
| `subject`             | "object_attributes.id" value                                |
| `time`                | "object_attributes.created_at" value                        |
| `data`                | Content of HTTP request body                                |

## Comment on Code Snippet Event

| CloudEvents Attribute | Value                                                       |
| :-------------------- | :---------------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID                    |
| `source`              | "object_attributes.url" value without the `#note\_...` part |
| `specversion`         | `0.3-wip`                                                   |
| `type`                | `com.gitlab.note.snippet`                                   |
| `datacontentencoding` | Omit                                                        |
| `datacontenttype`     | `application/json`                                          |
| `schemaurl`           | Omit                                                        |
| `subject`             | "object_attributes.id" value                                |
| `time`                | "object_attributes.created_at" value                        |
| `data`                | Content of HTTP request body                                |

## Merge Request Event

| CloudEvents Attribute | Value                                                          |
| :-------------------- | :------------------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID                       |
| `source`              | "repository.homepage" value                                    |
| `specversion`         | `0.3-wip`                                                      |
| `type`                | `com.gitlab.merge_request.` + "object_attributes.action" value |
| `datacontentencoding` | Omit                                                           |
| `datacontenttype`     | `application/json`                                             |
| `schemaurl`           | Omit                                                           |
| `subject`             | "object_attributes.iid" value                                  |
| `time`                | "object_attributes.created_at" value                           |
| `data`                | Content of HTTP request body                                   |

## Wiki Page Event

| CloudEvents Attribute | Value                                                      |
| :-------------------- | :--------------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID                   |
| `source`              | "project.web_url" value                                    |
| `specversion`         | `0.3-wip`                                                  |
| `type`                | `com.gitlab.wiki_page.` + "object_attributes.action" value |
| `datacontentencoding` | Omit                                                       |
| `datacontenttype`     | `application/json`                                         |
| `schemaurl`           | Omit                                                       |
| `subject`             | "object_attributes.slug" value                             |
| `time`                | Current time                                               |
| `data`                | Content of HTTP request body                               |

## Pipeline Event

| CloudEvents Attribute | Value                                                     |
| :-------------------- | :-------------------------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID                  |
| `source`              | "project.web_url" value                                   |
| `specversion`         | `0.3-wip`                                                 |
| `type`                | `com.gitlab.pipeline.` + "object_attributes.status" value |
| `datacontentencoding` | Omit                                                      |
| `datacontenttype`     | `application/json`                                        |
| `schemaurl`           | Omit                                                      |
| `subject`             | "object_attributes.id" value                              |
| `time`                | Current time                                              |
| `data`                | Content of HTTP request body                              |

## Job Event

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | Generate a new unique value, e.g. a UUID |
| `source`              | "repository.homepage" value              |
| `specversion`         | `0.3-wip`                                |
| `type`                | `com.gitlab.job.` + "job_status" value   |
| `datacontentencoding` | Omit                                     |
| `datacontenttype`     | `application/json`                       |
| `schemaurl`           | Omit                                     |
| `subject`             | "job_id" value                           |
| `time`                | Current time                             |
| `data`                | Content of HTTP request body             |

