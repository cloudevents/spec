<!--
---
linkTitle: "Continuous Deployment Events"
weight: 60
hide_summary: true
icon: "fa-solid fa-satellite-dish"
description: >
   Continuous Deployment Events
---
-->
# Continuous Deployment Events

Continuous Deployment (CD) events are related to continuous deployment pipelines and their target environments. These events can be emitted by environments to report where software artifacts such as services, binaries, daemons, jobs or embedded software are running.

## Subjects

This specification defines two subjects in this stage: `environment` and `service`. The term `service` is used to represent a running Artifact. A `service` can represent a binary that is running, a daemon, an application, a docker container. The term `environment` represent any platform which has all the means to run a `service`.

| Subject | Description | Predicates |
|---------|-------------|------------|
| [`environment`](#environment) | An environment where to run services | [`created`](#environment-created), [`modified`](#environment-modified), [`deleted`](#environment-deleted)|
| [`service`](#service) | A service | [`deployed`](#service-deployed), [`upgraded`](#service-upgraded), [`rolledback`](#service-rolledback), [`removed`](#service-removed), [`published`](#service-published)|

### `environment`

An `environment` is a platform which may run a `service`.

| Field | Type | Description | Examples |
|-------|------|-------------|----------|
| id    | `String` | See [id](spec.md#id-subject)| `1234`, `maven123`, `builds/taskrun123` |
| source | `URI-Reference` | See [source](spec.md#source-subject) | `staging/tekton`, `tekton-dev-123`|
| name | `String` | Name of the environment | `dev`, `staging`, `production`, `ci-123`|
| url | `String` | URL to reference where the environment is located | `https://my-cluster.zone.my-cloud-provider`|

### `service`

A `service` can represent for example a binary that is running, a daemon, an application or a docker container.

| Field | Type | Description | Examples |
|-------|------|-------------|----------|
| id    | `String` | See [id](spec.md#id-subject)| `service/myapp`, `daemonset/myapp` |
| source | `URI-Reference` | See [source](spec.md#source-subject) | `staging/tekton`, `tekton-dev-123`|
| environment | `Object` ([`environment`](#environment)) | Reference for the environment where the service runs | `{"id": "1234"}`, `{"id": "maven123, "source": "tekton-dev-123"}` |
| artifactId | `Purl` | Identifier of the artifact deployed with this service |  `pkg:oci/myapp@sha256%3A0b31b1c02ff458ad9b7b81cbdf8f028bd54699fa151f221d1e8de6817db93427`, `pkg:golang/mygit.com/myorg/myapp@234fd47e07d1004f0aed9c` |

## Events

### [`environment created`](conformance/environment_created.json)

This event represents an environment that has been created. Such an environment can be used to deploy services in.

- Event Type: __`dev.cdevents.environment.created.0.3.0`__
- Predicate: created
- Subject: [`environment`](#environment)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `tenant1/12345-abcde`, `namespace/pipelinerun-1234` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| name | `String` | Name of the environment | `dev`, `staging`, `production`, `ci-123`| |
| url | `String` | URL to reference where the environment is located | `https://my-cluster.zone.my-cloud-provider`| |

### [`environment modified`](conformance/environment_modified.json)

This event represents an environment that has been modified.

- Event Type: __`dev.cdevents.environment.modified.0.3.0`__
- Predicate: modified
- Subject: [`environment`](#environment)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `tenant1/12345-abcde`, `namespace/pipelinerun-1234` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| name | `String` | Name of the environment | `dev`, `staging`, `production`, `ci-123`| |
| url | `String` | URL to reference where the environment is located | `https://my-cluster.zone.my-cloud-provider`| |

### [`environment deleted`](conformance/environment_deleted.json)

This event represents an environment that has been deleted.```

- Event Type: __`dev.cdevents.environment.deleted.0.3.0`__
- Predicate: deleted
- Subject: [`environment`](#environment)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `tenant1/12345-abcde`, `namespace/pipelinerun-1234` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| name | `String` | Name of the environment | `dev`, `staging`, `production`, `ci-123`| |

### [`service deployed`](conformance/service_deployed.json)

This event represents a new instance of a service that has been deployed

- Event Type: __`dev.cdevents.service.deployed.0.3.0`__
- Predicate: deployed
- Subject: [`service`](#service)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `service/myapp`, `daemonset/myapp` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| environment | `Object` ([`environment`](#environment)) | Reference for the environment where the service runs | `{"id": "1234"}`, `{"id": "maven123, "source": "tekton-dev-123"}` | ✅ |
| artifactId | `Purl` | Identifier of the artifact deployed with this service |  `0b31b1c02ff458ad9b7b81cbdf8f028bd54699fa151f221d1e8de6817db93427`, `927aa808433d17e315a258b98e2f1a55f8258e0cb782ccb76280646d0dbe17b5`, `six-1.14.0-py2.py3-none-any.whl` | ✅ |

### [`service upgraded`](conformance/service_upgraded.json)

This event represents an existing instance of a service that has been upgraded to a new version

- Event Type: __`dev.cdevents.service.upgraded.0.3.0`__
- Predicate: upgraded
- Subject: [`service`](#service)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `service/myapp`, `daemonset/myapp` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| environment | `Object` ([`environment`](#environment)) | Reference for the environment where the service runs | `{"id": "1234"}`, `{"id": "maven123, "source": "tekton-dev-123"}` | ✅ |
| artifactId | `Purl` | Identifier of the artifact deployed with this service |`pkg:oci/myapp@sha256%3A0b31b1c02ff458ad9b7b81cbdf8f028bd54699fa151f221d1e8de6817db93427`, `pkg:golang/mygit.com/myorg/myapp@234fd47e07d1004f0aed9c` | ✅ |

### [`service rolledback`](conformance/service_rolledback.json)

This event represents an existing instance of a service that has been rolled back to a previous version

- Event Type: __`dev.cdevents.service.rolledback.0.3.0`__
- Predicate: rolledback
- Subject: [`service`](#service)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `service/myapp`, `daemonset/myapp` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| environment | `Object` ([`environment`](#environment)) | Reference for the environment where the service runs | `{"id": "1234"}`, `{"id": "maven123, "source": "tekton-dev-123"}` | ✅ |
| artifactId | `Purl` | Identifier of the artifact deployed with this service |  `pkg:oci/myapp@sha256%3A0b31b1c02ff458ad9b7b81cbdf8f028bd54699fa151f221d1e8de6817db93427`, `pkg:golang/mygit.com/myorg/myapp@234fd47e07d1004f0aed9c` | ✅ |

### [`service removed`](conformance/service_removed.json)

This event represents the removal of a previously deployed service instance and is thus not longer present in the specified environment

- Event Type: __`dev.cdevents.service.removed.0.3.0`__
- Predicate: removed
- Subject: [`service`](#service)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `service/myapp`, `daemonset/myapp` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| environment | `Object` ([`environment`](#environment)) | Reference for the environment where the service runs | `{"id": "1234"}`, `{"id": "maven123, "source": "tekton-dev-123"}` | ✅ |

### [`service published`](conformance/service_published.json)

This event represents an existing instance of a service that has an accessible URL for users to interact with it. This event can be used to let other tools know that the service is ready and also available for consumption.

- Event Type: __`dev.cdevents.service.published.0.3.0`__
- Predicate: published
- Subject: [`service`](#service)

| Field | Type | Description | Examples | Required |
|-------|------|-------------|----------|----------------------------|
| id    | `String` | See [id](spec.md#id-subject)| `service/myapp`, `daemonset/myapp` | ✅ |
| source | `URI-Reference` | See [source](spec.md#source-subject) | | |
| environment | `Object` ([`environment`](#environment)) | Reference for the environment where the service runs | `{"id": "1234"}`, `{"id": "maven123, "source": "tekton-dev-123"}` | ✅ |
