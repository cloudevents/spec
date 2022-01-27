# CouchDB CloudEvents Adapter

This document describes how to convert:

- [CouchDB Document events](http://docs.couchdb.org/en/stable/api/database/changes.html) and
- [CouchDB Database events](http://docs.couchdb.org/en/stable/api/server/common.html#db-updates)

into CloudEvents.

Each section below describes how to determine the CloudEvents attributes
based on the event type.

## /db/\_changes

### Update

| CloudEvents Attribute | Value                                 |
| :-------------------- | :------------------------------------ |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL / `db`                 |
| `specversion`         | `1.0`                                 |
| `type`                | `org.apache.couchdb.document.updated` |
| `datacontenttype`     | `application/json`                    |
| `subject`             | The document identifier (`id`)        |
| `time`                | Current time                          |
| `data`                | `changes` value (array of `revs`)     |

### Delete

| CloudEvents Attribute | Value                                 |
| :-------------------- | :------------------------------------ |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL / `db`                 |
| `specversion`         | `1.0`                                 |
| `type`                | `org.apache.couchdb.document.deleted` |
| `datacontenttype`     | `application/json`                    |
| `subject`             | The document identifier (`id`)        |
| `time`                | Current time                          |
| `data`                | `changes` value (array of `revs`)     |

## /\_db_updates

### Create

| CloudEvents Attribute | Value                                 |
| :-------------------- | :------------------------------------ |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL                        |
| `specversion`         | `1.0`                                 |
| `type`                | `org.apache.couchdb.database.created` |
| `subject`             | The database name (`db_name`)         |
| `time`                | Current time                          |

### Update

| CloudEvents Attribute | Value                                 |
| :-------------------- | :------------------------------------ |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL                        |
| `specversion`         | `1.0`                                 |
| `type`                | `org.apache.couchdb.database.updated` |
| `subject`             | The database name (`db_name`)         |
| `time`                | Current time                          |

### Delete

| CloudEvents Attribute | Value                                 |
| :-------------------- | :------------------------------------ |
| `id`                  | The event sequence identifier (`seq`) |
| `source`              | The server URL                        |
| `specversion`         | `1.0`                                 |
| `type`                | `org.apache.couchdb.database.deleted` |
| `subject`             | The database name (`db_name`)         |
| `time`                | Current time                          |
