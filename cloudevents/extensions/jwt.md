# JWT Extension

This extension provides a way to map JWT (JSON Web Token) values in the formats of JWE
 (JSON Web Encryption) or JWS (JSON Web Signature).
 
JWE MAY be used to encrypt a CloudEvent data and JWS MAY be used to sign CloudEvent data

This extension does not support [JWE Json Serialization][jwe-json-serialization] 

When using [JWE Cipher Text][jwe-ciphertext] MUST be mapped onto `data` and
 `datacontenttype` MUST be set to `application/octet-stream`

## Attributes

### JOSE Attributes

#### jose
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
    
    <!--Q: Should we keep this?-->
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
    algorithms may not use an Authentication Tag, in which case this
    value is the empty octet sequence.

    <!--Q: Should we keep this?-->
    If this attribute does not exist consumers MAY assume that the value is empty
    an octet sequence
- Constraints:
  - OPTIONAL
  - MAY be an empty octet sequence
  
## References
  - [JWT for dummies](https://medium.facilelogin.com/jwt-jws-and-jwe-for-not-so-dummies-b63310d201a3)
  

[jwe-json-serialization]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-encrypted-key]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-initialization-vector]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-ciphertext]: https://www.rfc-editor.org/rfc/rfc7516#section-2
[jwe-authentication-tag]: https://www.rfc-editor.org/rfc/rfc7516#section-2