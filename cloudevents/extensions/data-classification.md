# Data Classification Extension

CloudEvents might contain payloads which are subjected to data protection
regulations like GDPR or HIPAA. For intermediaries and consumers knowing how
event payloads are classified, which data protection regulation applies and how
payloads are categorized, enables compliant processing of events.

This extension defines attributes to describe to
[consumers](../spec.md#consumer) or [intermediaries](../spec.md#intermediary)
how an event and its payload is classified, category of the payload and any
applicable data protection regulations.

These attributes are intended for classification at an event and payload level
and not at a `data` field level. Classification at a field level is best defined
in the schema specified via the `dataschema` attribute.

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
  context of a `dataregulation`. In situations where `dataregulation` is
  undefined or the data protection regulation does not define any labels, then
  RECOMMENDED labels are: `public`, `internal`, `confidential`, or
  `restricted`.
- Constraints:
  - REQUIRED

### dataregulation

- Type: `String`
- Description: A comma-delimited list of applicable data protection regulations.
  For example: `GDPR`, `HIPAA`, `PCI-DSS`, `ISO-27001`, `NIST-800-53`, `CCPA`.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty string without internal spaces. Leading and
    trailing spaces around each entry MUST be ignored.

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

## Usage

When this extension is used, producers MUST set the value of the
`dataclassification` attribute. When applicable the `dataregulation` and
`datacategory` attributes MAY be set to provide additional details on the
classification context.

When an implementation supports this extension, then intermediaries and
consumers MUST take these attributes into account and act accordingly to data
regulations and/or internal policies in processing the event and payload. If
intermediaries or consumers cannot meet such requirements, they MUST reject and
report an error through a protocol-level mechanism.

If intermediaries or consumers are unsure on how to interpret these attributes,
for example when they encounter an unknown classification level or data
regulation, they MUST assume they cannot meet requirements and MUST reject the
event and report an error through a protocol-level mechanism.

Intermediaries SHOULD NOT modify the `dataclassification`, `dataregulation`, and
`datacategory` attributes.

## Use cases

Examples where data classification of events can be useful are:

- When an event contains PII or restricted information and therefore processing
  by intermediaries or consumers need to adhere to certain policies. For example
  having separate processing pipelines by sensitivity or having logging,
  auditing and access policies based upon classification.
- When an event payload is subjected to regulation and therefore retention
  policies apply. For example, having event retention policies based upon data
  classification or to enable automated data purging of durable topics.

## Appendix Data Protection and Privacy Regulations

A catalog of common data protection and privacy regulation and abbreviations 
based upon UNCTAD (United Nations Conference on Trade and Development) 
information. As UNCTAD itself does not define any abbreviations, this 
is a non-exhaustive derivative list of most common regulations. For more 
information see [UNCTAD Data Protection and Privacy Legislation Worldwide](https://unctad.org/page/data-protection-and-privacy-legislation-worldwide).

| Region | Abbreviation | Full Name | Country |
|--------|--------------|-----------|---------|
| Africa | POPIA | Protection of Personal Information Act | South Africa |
| Africa | NDPR | Nigeria Data Protection Regulation | Nigeria |
| Africa | DPA-KE | Data Protection Act | Kenya |
| Africa | PDPL | Personal Data Protection Law | Egypt |
| Africa | GDPL | General Data Protection Law | Tunisia |
| Americas | LGPD | Lei Geral de Proteção de Dados | Brazil |
| Americas | LPDP | Ley de Protección de Datos Personales | Mexico |
| Americas | LOCDI | Ley Orgánica de Datos Personales | Argentina |
| Americas | CCPA | California Consumer Privacy Act | United States |
| Americas | CPRA | California Privacy Rights Act | United States |
| Americas | PIPEDA | Personal Information Protection and Electronic Documents Act | Canada |
| Americas | VCDPA | Virginia Consumer Data Protection Act | United States |
| Americas | CPA | Colorado Privacy Act | United States |
| Americas | UCPA | Utah Consumer Privacy Act | United States |
| Asia-Pacific | PDPA | Personal Data Protection Act | Singapore |
| Asia-Pacific | PIPA | Personal Information Protection Act | South Korea |
| Asia-Pacific | APPI | Act on the Protection of Personal Information | Japan |
| Asia-Pacific | DPDP | Personal Data Protection Bill | India |
| Asia-Pacific | PDPO | Personal Data (Privacy) Ordinance | Hong Kong |
| Asia-Pacific | DPA-MY | Data Protection Act | Malaysia |
| Asia-Pacific | PIPL | Personal Information Protection Law | China |
| Asia-Pacific | DPA-ID | Draft Data Protection Act | Indonesia |
| Europe | GDPR | General Data Protection Regulation | European Union |
| Middle East | PDPL | Personal Data Protection Law | Saudi Arabia |
| Middle East | PDPO | Personal Data Protection Ordinance | United Arab Emirates |
| Middle East | PDPD | Personal Data Protection Draft | Bahrain |
| Global/Multi-Regional | APEC-CBPR | Asia-Pacific Economic Cooperation Cross Border Privacy Rules | International |
| Global/Multi-Regional | ISO-27001 | Information Security Management | International |
| Global/Multi-Regional | ISO-27701 | Privacy Information Management | International |
| Industry-Specific | HIPAA | Health Insurance Portability and Accountability Act | United States |
| Industry-Specific | PCI-DSS | Payment Card Industry Data Security Standard | United States |
| Industry-Specific | NIST-800-53 | National Institute of Standards and Technology Framework | United States |
