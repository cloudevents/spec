# JWT Extension

This extension provides a way to map JWT (JSON Web Token) values in the formats of JWE
 (JSON Web Encryption) or JWS (JSON Web Signature).
 
JWE MAY be used to encrypt a CloudEvent data and JWS MAY be used to sign CloudEvent data

This extension does not support [JWE Json Serialization][jwe-json-serialization] 

When using [JWE Cipher Text][jwe-ciphertext] MUST be mapped onto `data` and
 `datacontenttype` MUST be set to `application/octet-stream`

When using JWS the signed data MUST be decoded from base64url format and mapped onto
`data` in `Binary` format where `datacontenttype` is taken from the `cty` property
of the JOSE header, if no `cty` property exists `datacontenttype` MUST be set to `application/octet-stream`
  
## Attributes

### jose
- Type: `Binary`
- Description: utf-8 encoded JOSE Header value.
    Both JWS and JWE have JOSE Header definitions.
- Constraints:
  - REQUIRED
  - MUST be a non-empty octet sequence
- Examples:
  - `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9` (`{"alg": "HS256","typ": "JWT"}`)

### jwssignature
- Type: `Binary`
- Description: JWS Signature.
    Computed over the complete JOSE header and `data` value
- Constraints:
  - OPTIONAL
  - MUST be a non-empty octet sequence
- Examples:
  - `SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c` 

### jweencryptedkey
- Type: `Binary`
- Description : [JWE Encrypted Key][jwe-encrypted-key].
    Encrypted Content Encryption Key value. Note that for some algorithms, 
    the JWE Encrypted Key value is specified as being the empty octet sequence
    
    <!--Q: SHOULD we keep this?-->
    If this attribute does not exist consumers MAY assume that the value is empty
    an octet sequence
- Constraints:
  - OPTIONAL
  - MAY be an empty octet sequence

### jweinitvector
- Type: `Binary`
- Description: [JWE Initialization Vector][jwe-initialization-vector].
    Additional value to be integrity protected by the authenticated
    encryption operation.  This can only be present when using the JWE
    JSON Serialization.  (Note that this can also be achieved when
    using either the JWE Compact Serialization or the JWE JSON
    Serialization by including the AAD value as an integrity-protected
    Header Parameter value, but at the cost of the value being double
    base64url encoded.)
- Constraints:
  - OPTIONAL
  - MAY be an empty octet sequence


### jweauthtag 
- Type: `Binary`
- Description: [ JWE Authentication Tag][jwe-authentication-tag].
    Authentication Tag value resulting from authenticated encryption
    of the plaintext with Additional Authenticated Data.
    
    An output of an AEAD operation that ensures the integrity of the
    ciphertext and the Additional Authenticated Data.  Note that some
    algorithms MAY not use an Authentication Tag, in which case this
    value is the empty octet sequence.

    <!--Q: SHOULD we keep this?-->
    If this attribute does not exist consumers MAY assume that the value is empty
    an octet sequence
- Constraints:
  - OPTIONAL
  - MAY be an empty octet sequence

## Examples

### JWS

How to map a JWS signed data onto a CloudEvent

This is an example JWS value

```eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImN0eSI6ImFwcGxpY2F0aW9uL215Zm9ybWF0K2pzb24ifQ.eyJ2YWx1ZSI6IkhlbGxvIFdvcmxkIn0.xs78ebtFbrKWn7avnfOaV7MsA3tNe2Z7gyXN3Xba5KA0HJZd9jTz9rv6jftdyC9E0cuwXoAXysT_wIkVPPbxUQ```


It consists of 3 parts
  - The JOSE header
   `eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImN0eSI6ImFwcGxpY2F0aW9uL215Zm9ybWF0K2pzb24ifQ` (`{"alg": "HS512","typ": "JWT","cty": "application/myformat+json"}`)
  - The signed payload `eyJ2YWx1ZSI6IkhlbGxvIFdvcmxkIn0` (`{"value": "Hello World"}`)
  - The signature `xs78ebtFbrKWn7avnfOaV7MsA3tNe2Z7gyXN3Xba5KA0HJZd9jTz9rv6jftdyC9E0cuwXoAXysT_wIkVPPbxUQ`
  
We will decode all of these values using base64url (as defined by the spec) and
assign the resulting values in the following way: 

  - The JOSE header will be assigned to `jose`
  - The signed payload will be assigned to `data` in a binary form
  - `datacontentype` will be set to `application/myformat+json`
  - The signature
   `xs78ebtFbrKWn7avnfOaV7MsA3tNe2Z7gyXN3Xba5KA0HJZd9jTz9rv6jftdyC9E0cuwXoAXysT_wIkVPPbxUQ` will be assigned to `jwssignature`
  
### JWE

Here is an example JWE compact encoded value

`eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.-3z2QWPXgU3ZjjJysgX0ZetYqBP_GTDNhlR1OaDF4Z66f4rILsFG7ox_HW73YvNkoubpCTsE0uez6JHq3id0muOH7Zf0zydz.Ja5lUcRlp8_6bv4JqMgjWA.xT3GozwdSdJE5z1x_33-yg.C8VVM4NhkKLzfIsCwswQB08PkBNJCCsjbF8BEjXt-PQ`

This value is an encrypted `Hello World!` plaintext with the JWK of `{"k":"MKwYqAHLPx35ImzJwqU-4pFzjleyjOdYSl_BUwo9PKg","kty":"oct"}`

The value consists of 5 parts:
  - The JOSE header
   `eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0` 
  - The JWE encrypted key
   `-3z2QWPXgU3ZjjJysgX0ZetYqBP_GTDNhlR1OaDF4Z66f4rILsFG7ox_HW73YvNkoubpCTsE0uez6JHq3id0muOH7Zf0zydz`
  - The initialization vector `Ja5lUcRlp8_6bv4JqMgjWA`
  - The encrypted cipher text `xT3GozwdSdJE5z1x_33-yg`
  - The authentication tag `C8VVM4NhkKLzfIsCwswQB08PkBNJCCsjbF8BEjXt-PQ`

We will decode all of these values using base64url (as defined by the spec) and
assign the resulting values in the following way: 

  - The JOSE header will be assigned to `jose`
  - The JWE encrypted key will be assigned to `jweencryptedkey`
  - The initialization vector will be assigned to `jweinitvector`
  - The encrypted cipher text will be assigned to `data` in a binary form
  - `datacontentype` will be set to `application/octet-stream`
  - The authentication tag will be assigned to `jweauthtag`
  

## References
  - [JWT for dummies](https://medium.facilelogin.com/jwt-jws-and-jwe-for-not-so-dummies-b63310d201a3)
  

[jwe-json-serialization]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-encrypted-key]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-initialization-vector]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-ciphertext]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-authentication-tag]: https://www.rfc-editor.org/rfc/rfc7516#section-2