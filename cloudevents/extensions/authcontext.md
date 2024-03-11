# Auth Context

This extension embeds information about the principal which triggered an
occurrence. This allows consumers of the
CloudEvent to perform user-dependent actions without requiring the user ID to
be embedded in the `data` or `source` field.

This extension is purely informational and is not intended to secure
CloudEvents.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute being marked as "REQUIRED" does not mean
it needs to be in all CloudEvents, rather it needs to be included only when 
this extension is being used.

## Attributes

### authtype
- Type: `String`
- Description: An enum representing the type of principal that triggered the
  occurrence. Valid values are:
  - `app_user`: An end user of an application. Examples include an AWS cognito,
    Google Cloud Identity Platform, or Azure Active Directory user.
  - `user`: A user account registered in the infrastructure. Examples include
    developer accounts secured by IAM in AWS, Google Cloud Platform, or Azure.
  - `service_account`: A non-user principal used to identify a service.
  - `api_key`: A non-user API key
  - `system`: An obscured identity used when a cloud platform or other system
    service triggers an event. Examples include a database record which
    was deleted based on a TTL.
  - `unauthenticated`: No credentials were used to authenticate the change that
    triggered the occurrence.
  - `unknown`: The type of principal cannot be determined and is unknown.
- Constraints
  - REQUIRED
  - This specification defines the following values, and it is RECOMMENDED that
    they be used. However, implementations MAY define additional values.

### authid
- Type: `String`
- Description: A unique identifier of the principal that triggered the
  occurrence. This might, for example, be a unique ID in an identity database
  (userID), an email of a platform user or service account, or the label for an
  API key.
- Constraints
  - OPTIONAL

### authclaims
- Type: `String`
- Description: A JSON string representing claims of the principal that triggered
  the event.
- Constraints
  - OPTIONAL
  - MUST NOT contain actual credentials sufficient for the Consumer to
    impersonate the principal directly.
  - MAY contain enough information that a Consumer can authenticate against an
    identity service to mint a credential impersonating the original principal.
