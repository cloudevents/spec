# Cryptography Extension

## Abstract

Some CloudEvents MAY contain encrypted or cryptographically-signed `data`. The "plain"
data which was encrypted or signed data usually differs in format from the plain data.

This extension provides a standard way for expressing the properties of the plain data.

## Terminology

### Encrypted Data
Refers to a data which was encrypted with some sort of an encryption algorithm.
The encrypted data MAY contain additional metadata which is not the plain data.

This additional metadata MAY be encrypted as-well, or stored in a plain format.

Example for additional metadata:
- RSA encrypted AES key which is pre-appended to the AES encrypted plain data
- A Header containing the algorithm which was used to encrypt the data

This extension does not Impose any requirements on the encryption algorithm.

### Signed Data
A data which consists of a the plain data and additional metadata that contains a
signature.

### Plain data

Refers to the data as it were before application of the encryption algorithm or the
data which was signed (and does not include the signature).

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