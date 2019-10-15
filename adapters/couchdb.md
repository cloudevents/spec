# CouchDB CloudEvents Adapter

This document describes how to convert:
- [CouchDB Document events](http://docs.couchdb.org/en/stable/api/database/changes.html) and
- [CouchDB Database events](http://docs.couchdb.org/en/stable/api/server/common.html#db-updates)

into CloudEvents.

Each section below describes how to determine the CloudEvents attributes
based on the event type.

## /db/_changes

### Update

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL / db_name             |
| `specversion`         | `1.0-rc1`                                |
| `type`                | `org.apache.couchdb.document.update`     |
| `datacontenttype`     | `application/json`                       |
| `dataschema`          | Omit                                     |
| `subject`             | `id` value                           |
| `time`                | Current time                             |
| `data`                | `changes` value (array of `revs`)           |

### Delete

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL / db_name             |
| `specversion`         | `1.0-rc1`                                |
| `type`                | `org.apache.couchdb.document.delete`     |
| `datacontenttype`     | `application/json`                       |
| `dataschema`          | Omit                                     |
| `subject`             | `id` value                               |
| `time`                | Current time                             |
| `data`                | `changes` value (array of `revs`)        |

## /_db_updates

### Create

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | The event sequence identifier|
| `source`              | The server URL    |
| `specversion`         | `1.0-rc1`                                |
| `type`                | `org.apache.couchdb.db.create`           |
| `dataschema`          | Omit                                     |
| `subject`             | The database name (db_name)              |
| `time`                | Current time                             |
| `data`                | Omit                      |

### Update

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | The event sequence identifier |
| `source`              | The server URL    |
| `specversion`         | `1.0-rc1`                                |
| `type`                | `org.apache.couchdb.document.update`           |
| `dataschema`          | Omit                                     |
| `subject`             | The database name (db_name)              |
| `time`                | Current time                             |
| `data`                | Empty                      |

### Delete

| CloudEvents Attribute | Value                                    |
| :-------------------- | :--------------------------------------- |
| `id`                  | The event sequence identifier |
| `source`              | The server URL    |
| `specversion`         | `1.0-rc1`                                |
| `type`                | `org.apache.couchdb.db.delete`           |
| `dataschema`          | Omit                                     |
| `subject`             | The database name (db_name)              |
| `time`                | Current time                             |
| `data`                | Empty                      |

