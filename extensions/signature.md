# Signature Extension

This extension defines a standard mechanism to carry signatures allowing
event consumers to ensure the identity of the event producer and verify
the event-data has not been tampered with during transport.

This specification does not:

- Declare a mechanism for public key exchange.
- Declare a mechanism for public key selection during signature verification.
Implementors may consider leveraging the CloudEvent `source` as a method
of selection.

## Usage

This extension supports a few general usage models:

- Where the algorithm used to produce an attached signature needs to be shared.
- Where the `data` is signed with a detached signature.
- Where the CloudEvent context attributes are signed.

## Attributes

### sigdata

- Type: `Binary`
- Description: The binary signature generated for the event `data`.
- Constraints:

  - OPTIONAL

### sigdataalgo

- Type : `String`
- Description : The algorthim used to generate the `data` signature.
- Constraints:

  - OPTIONAL
  - *Should* be present when `sigdata` is present.

### sigattr

- Type: `Binary`
- Description : The binary signature generated for the CloudEvent context
attributes (as-per method described below).
- Constraints:

  - OPTIONAL

### sigattralgo

- Type: `String`
- Description : The alorithm used to generate the attribute signature
- Constraints:

  - OPTIONAL
  - *Should* be present when `sigattr` ifs present.

### sigattrtype

- Type: `String`
- Description: Defines the familly of attributes that participated in
the signing function. See [SigAttrType Values](sigattrtype-values)
- Constraints:

  - OPTIONAL
  - *MUST* be present when `sigattr` is present.

## SigAttrType Values

This specification defines the following values for `sigattrtype`. Additional
values MAY be defined by other specifications.

### REQUIRED

- When `sigattrtype` is set to `REQUIRED` it indicates that only *required*
context attributes particpated in the signing process.

### OPTIONAL

- When `sigattrtype` is set to `OPTIONAL` it indicates that the *required
and optional* context attributes participated in the signing process.

### ALL

- When `sigattrtype` is set to `ALL` it indicates that the *required, optional,
and extension* context attributes participated in the signing process.

NOTE: atributes defined by this extension *ARE NOT* considered during the
signing process.

## Attribute signing & verification process

- The set of attributes to be considered is constructed based on the scheme
defined by `sigattrtype`.

  - Any attribute with a null or empty value is ignored.
  - Atrributes defined in this extension are ignored.

- The selected attributes are sorted by name into acending alphabetical order.

- The string value of each attribute are concatenated according to sorted
order.

- The signature is generated from the UTF-8 byte representation of the
concatenated string.

[rfc4648]: https://tools.ietf.org/html/rfc4648