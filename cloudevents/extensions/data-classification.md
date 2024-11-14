# Data Classification Extension

CloudEvents might contain payload which is subjected to data protection
regulations like GDPR or HIPAA. For intermediaries and consumers knowing how
event payload is classified, which data protection regulation applies and how
payload is categorized, enables compliant processing of an event.

This extension defines attributes to describe to
[consumers](../spec.md#consumer) or [intermediaries](../spec.md#intermediary)
how an event and its payload is classified, category of the payload and any
applicable data protection regulations.

These attributes are intended for classification on an event and payload level
and not on `data` field level. Classification on field level is best defined in
the schema specified via the `dataschema` attribute.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is used.
For example, an attribute being marked as "REQUIRED" does not mean it needs to
be in all CloudEvents, rather it needs to be included only when this extension
is being used.

## Attributes

### dataclassification

- Type: `String`
- Description: Data classification level for the event payload within the
  context of a `dataregulation`. Typical labels are: `public`, `internal`,
  `confidential`, `restricted`.
- Constraints:
  - REQUIRED
  - SHOULD be applicable to data protection regulation.

### dataregulation

- Type: `String`
- Description: A comma-delimited list of applicable data protection regulations.
  For example: `GDPR`, `HIPAA`, `PCI-DSS`, `ISO-27001`, `NIST-800-53`, `CCPA`.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty string

### datacategory

- Type: `String`
- Description: Data category of the event payload within the context of a
  `dataregulation` and `dataclassification`. For GDPR personal data typical  
  labels are: `non-sensitive`, `standard`, `sensitive`, `special-category`. For
  US personal data this could be: `sensitive-pii`, `non-sensitive-pii`,
  `non-pii`. And for personal health information under HIPAA: `phi`.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be applicable to data regulation and classification.

## Usage

When this extension is used, producers MUST set the value of the
`dataclassification` attribute. When applicable the `dataregulation` and
`datacategory` attributes MAY be set to provide additional details on the
classification context.

Intermediaries and consumers SHOULD take these attributes into account and act
accordingly to data regulations and/or internal policies when processing the
event and payload.

Intermediaries SHOULD NOT modify the `dataclassification`, `dataregulation`, and
`datacategory` attributes.

## Use cases

Examples where data classification of events can be useful are:

- When an event contains PII or restricted information and therefore processing
  by intermediaries or consumers MUST adhere to certain policies. For example
  having separate processing pipelines by sensitivity or having logging,
  auditing and access policies based upon classification.
- When an event payload is subjected to regulation and therefore retention
  policies apply. For example, having event retention policies based upon data
  classification or to enable automated data purging durable topics.