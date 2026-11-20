# Schema and Endpoint Descriptor Profiles

These profiles define entries in a [Descriptor](descriptors.md). A
publication profile determines whether an operation uses either class and
whether it needs one entry or several. Neither class adds a CloudEvents
attribute.

The keywords "MUST" and "REQUIRED" have the meanings in
[RFC 2119](https://tools.ietf.org/html/rfc2119).

## Schema

A `schema` entry MUST link to a payload schema document at `url`, not its
Registry metadata. Use the linked document or the entry's bundled
`document`. A schema registry is not REQUIRED.

To select one schema, use the `schema` entry named by the publication
profile. If the profile supplies no name, one `schema` entry selects that
schema, no entries means absence, and multiple entries are ambiguous.
A specified name that is missing or has the wrong class is invalid, not
absence. An invalid or ambiguous selection, unsupported format, or
unavailable selected document MUST NOT cause fallback to another schema.
The event binding defines precedence between this entry and `dataschema`.

## Endpoint

An `endpoint` entry MUST link to a representation of endpoint metadata
at `url`. For an xRegistry [Endpoint Group][Endpoint Group], use the
Group's metadata URL. The entry does not authorize invoking the endpoint.

To select one endpoint, use the `endpoint` entry named by the publication
profile or the unique entry of that class if no name is supplied.
An absent entry, wrong class or ambiguous selection MUST be reported
when the operation needs that endpoint. The Consumer MUST NOT replace a
failed selection with an unrelated endpoint.

[Endpoint Group]: https://github.com/xregistry/spec/blob/main/endpoint/spec.md
