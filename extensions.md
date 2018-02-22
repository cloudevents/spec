# Registered Extensions

The `extensions` field of a Cloud Event holds additional metadata in an event.
This field may be both used for experimental features not yet ready for
standardization or for fields that are domain-specific and not suitable for
standardization.

To encourage common design patterns where they make sense, an event source MAY
choose to use a registered extension. When using an extension with a registered
name, an event source SHOULD behave consistently with the description.

## jwtClaims
* Type: Object
* Description: If the Event Source supports JWT authentication, this extension
  allows the Source to provide the identity of the user who triggered the
  occurrence of the Event. The jwt_claims extension is unsigned and decoded
  claims portion of a JWT. This allows event systems to forward identity
  information without sufficient information to authorize further requests.
  An empty object MAY be used to indicate that the Event was triggered by an
  anonymous user. For more information about JWTs, see 
  [jwt.io/introduction](https://jwt.io/introduction).
* Constraints:
  * OPTIONAL
  * If empty, MUST indicate that the Event was triggered by an anonymous user.
  * The 
  [registered claim names](https://tools.ietf.org/html/rfc7519#section-4.1)
   of JWTs (e.g. 'iss', 'sub', 'aud', and 'exp') are reserved and MUST 
   have the same meaning as RFC3519 when present.
* Examples:

```json
// Actual value of the user signed in with Firebase Auth in the project
// "inlined-junkdrawer". The user has signed in using Google as an
// identity provider and their email address "inlined@google.com".
{
  "iss": "https://securetoken.google.com/inlined-junkdrawer",
  "name": "Thomas Bouldin",
  "picture": "https://lh4.googleusercontent.com/-_LyEJyXZklU/AAAAAAAAAAI/AAAAAAAAAW4/hiJ6WHKP8AI/photo.jpg",
  "aud": "inlined-junkdrawer",
  "auth_time": 1519171715,
  "user_id": "TSNVi5u1tyRhSCbhtIXbk9Go9IK2",
  "sub": "TSNVi5u1tyRhSCbhtIXbk9Go9IK2",
  "iat": 1519171715,
  "exp": 1519175315,
  "email": "inlined@google.com",
  "email_verified": true,
  "firebase": {
    "identities": {
      "google.com": [
        "113635245217169028038"
      ],
      "email": [
        "inlined@google.com"
      ]
    },
    "sign_in_provider": "google.com"
  }
}
```