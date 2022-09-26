# Cryptography Extension

## Abstract

Some CloudEvents MAY contain encrypted or cryptographically-signed `data`. The "plain"
data which was encrypted or signed data usually differs in format from the plain data.

Events with encrypted or signed `data` values create a few problems:
 - [`datacontenttype`](../spec.md#datacontenttype) MUST hold the content type of 
 the encrypted buffer, and not the plain data. 
- [`dataschema`](../spec.md#dataschema) MUST hold the schema of the encrypted buffer, 
 and not the the schema of the plain data

This means consumers and intermediaries cannot route and validate events based on 
the `datacontenttype` and `dataschema` attributes as they do with "normal" events.

To solve this problem this extension proposes the attributes 
[`cryptdatacontenttype`](#cryptdatacontenttype)  and 
[`cryptdataschema`](#cryptdataschema) to provide a way for describing this needed 
metadata.

## Terminology

### Plain data
Data which was fed to the cryptographic algorithm which produced the given event
 `data` value
 
Examples:
 - Data before it was encrypted
 - Data before it was signed   
 
 
## Attributes
### cryptdatacontenttype
- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: Content type of the plain data value.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
- For Media Type examples see
  [IANA Media Types](http://www.iana.org/assignments/media-types/media-types.xhtml)


#### cryptdataschema

- Type: `URI`
- Description: Identifies the schema that the plain data adheres to. Incompatible
  changes to the schema SHOULD be reflected by a different URI. See
  [Versioning of CloudEvents in the Primer](../primer.md#versioning-of-cloudevents)
  for more information.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI
  
  
# Decryption and Signature Removal
When the event `data` is decrypted or has it's signature removed.
The values of `cryptdatacontenttype` and `ctyptdataschema` MUST be removed and placed
inside the `datacontenttype` and `dataschema` attributes respectively.
 
This applies only in the case that the decryption or signature removal is preformed by
an intermediary which intends to replace the value of `data` with the plain data value. 