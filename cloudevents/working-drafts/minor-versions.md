# Allowing minor version numbers for the CloudEvents spec (and specversion attribute)

## Introduction

We're building up a backlog (currently not in a very organised way)
of things we would like to do with the CloudEvents spec in the
future. Some of these are *definitely* in the realm of a new major
version, but there has been discussion of some changes that could
legitimately be called a minor version - if we supported such a
thing. This proposal proposes a change to our spec versioning to
allow for minor versions.

Note: this document uses "event" as a shorthand for "CloudEvent" throughout for
simplicity. If any part of this document becomes part of the spec, we can
rewrite it appropriately.

## Is changing our mind about minor versions a breaking change?

The current spec describes the `specversion` attributes as follows:

> The version of the CloudEvents specification which the event uses.
> This enables the interpretation of the context. Compliant event
> producers MUST use a value of 1.0 when referring to this version of
> the specification.
> 
> Currently, this attribute will only have the 'major' and 'minor'
> version numbers included in it. This allows for 'patch' changes to
> the specification to be made without changing this property's value
> in the serialization. Note: for 'release candidate' releases a
> suffix might be used for testing purposes.

The GOVERNANCE.md doc states:

> Since changing the CloudEvents specversion string could have a
> significant impact on implementations, all non-breaking changes will
> be made as "patch" version updates - this allows for the value "on
> the wire" to remain unchanged. If a breaking change is introduced
> the normal semver rules will apply and the "major" version number
> will change. The net effect of this is that the "minor" version
> number will always be zero and the specversion string will always be
> of the form X.0.

I'd view the governance doc as rather less binding than the spec -
it's "current practice" rather than a promise.

Any SDK (and potentially other consuming code) that *expects* the
current documented will fail to parse a v1.1 (etc) event - and
that's probably okay. For maximum compatibility, publish v1.0
events for a while. But we don't even need a v1.1 right now, so
there's enough time for SDKs to start implementing the below
compatibility code *now*, and so hopefully by the time we actually
want a v1.1, the majority of deployed software will be able to
handle it.

## Out of scope (major)

There are probably many changes which could count as major, but I'd
like to call out the following explicitly:

- Any change to required attributes:
  - Adding
  - Removing
  - Changing type
  - Changing validation criteria
- Changes to the type system:
  - Adding types
  - Removing types
- Changes to attribute naming rules
- Breaking changes to CloudEvent formats

## Intended minor change

Fundamentally, the purpose of this proposal is to allow the
introduction of new *optional* attributes, which are
expected to usually have been documented extension attributes in the
past - in other words, a graduation process from "suggested as useful"
to "officially specified". However, there's no requirement for an
attribute to be a documented extension attribute before being added;
that's just an informal part of the usual process.

SemVer minor versions are intended for new features that don't break
existing code. How SemVer applies to specifications is less clear-cut
than how it applies to actual code. This document attempts to imagine
the impact of a change on various stakeholders.

For the purpose of this document, we'll consider a single new optional
attribute into version 1.1:

- Name: `xyz`
- Type: integer
- Constraints: value in the range 1-100 inclusive

Obviously this is entirely artificial, but it should be enough to help
find corner cases and problems.

## Logical compatibility

Every valid v1.1 event can be "rewritten" as a valid v1.0 event, but the reverse is not true.
A v1.0 event containing an `xyz` extension attribute with value "test" is valid,
but cannot be expressed as a valid v1.1 event. As there are no restrictions on
v1.0 extension attributes, there's no way that the v1.1 specification can *claim*
that all v1.0 events would be valid as v1.1 events, even if the addition
is only a previously-documented extension attribute. (Extension attribute documentation
is advisory, not mandatory.)

## Event producer

An event producer that doesn't know about v1.1 should create an event
with v1.0. If the code producing the event uses an SDK, then it's *possible*
that it will create a v1.1 event accidentally after an SDK upgrade - and that
could cause problems. (The SDK handling of minor versions is relatively
complex, and discussed later.) But if they produce a v1.0 event with an
`xyz` attribute with value "test", that's fine: it's still a valid v1.0 event.

An event producer that is aware of v1.1 should ensure that any use of the `xyz`
attribute is valid - in other words, it can't have values of "test"
(wrong type) or 123 (constraint violation). That would be an invalid v1.1 event
in the same way that specifying a `time` attribute value of "lunchtime" would be
invalid.

## Event proxies

Proxies which are unaware of v1.1 should be able to proxy v1.1 events without
any issues, *unless* they attach special meaning to unspecified attributes (whether
`xyz` or anything else). For example, a proxy which makes use of the `sequence` extension
attribute but isn't aware of v1.0 cannot safely assume that v1.1 events will use `sequence`
in the same way as v1.0. (`sequence` may become a core attribute with a particular meaning.)
The proxy could make a choice of:

- Expecting that the previous attribute *is* used in the same way, and treating
  it as per v1.0 events, with a suitable failure mode.
- Not attaching any significance to the attribute for v1.1 events, treating it as
  any other extension attribute.

There's no one-size-fits-all approach here.

## Event consumers

An event consumer that doesn't know about v1.1 should still be able to consume
a v1.1 event without any knowledge of the `xyz` attribute; it should be treated as a regular
extension attribute. However, the consumer does "know" that the event is v1.1, so can be aware
that `xyz` (and any other extension attributes) *may* be a core attribute in v1.1.
(In other words, they can distinguish between `xyz` appearing in a v1.0 event which is *definitely*
an extension attribute as the consumer is aware of all core v1.0 attribtes,
and `xyz` appearing in a v1.1 event which is *either* an extension attribute *or* a new optional
core attribute.)

## SDKs

If we adopt minor versions, SDKs should change to support them, so that (for example) an SDK
supporting v1.1 will *also* parse v1.2 events. We should keep track of which SDKs
(and which versions of those SDKs) support parsing v1.x events.

Different SDKs expose features very differently. This document is written from the perspective
of the C# SDK, but other viewpoints would be highly valued: please add feedback, particularly
if the approach suggested doesn't make sense for an SDK you're familiar with.

### Creating events: default version handling

It may sound natural to allow something like:

```csharp
var evt = new CloudEvent { Id = "..." };
```

... to just use the latest spec version that the SDK supports. However, this is a breaking change.
Consider:

```csharp
var evt = new CloudEvent
{
    Id = "...",
    ["xyz"] = "test"
};
```

When the SDK only supports v1.0, that creates a valid event. When the SDK supports v1.1 as well,
that would produce an invalid event or throw an exception, if the version is implicitly v1.1.
Instead, the SDK should *implicitly* use the latest version that was present when the first stable
version of the SDK came out, within its own current major version. In other words, if v1.1 ships
and a new SDK is created, that can default to v1.1 - and if an SDK creates its own new major version,
*that* can default to v1.1 as well... but in both cases that default should stay as v1.1 in new minor
SDK versions even after v1.2 ships.

An SDK *may* choose to provide a way of explicitly opting into the "latest supported" version:

```csharp
var evt = new CloudEvent(CloudEventsSpecVersion.Latest)
{
  
};
```

### Accessing attributes

If an SDK exposes core attributes in a distinct way from extension attributes (as shown above,
where `Id` is a strongly-typed property, whereas `["xyz"]` uses an indexer with a string literal)
then any attempt to use the "special" access should fail when accessing an attribute within
an event with a version that doesn't have that attribute as a core attribute. Example:

```csharp
// Create a v1.0 event
var evt = new CloudEvent(CloudEventsSpecVersion.V1_0);

// Try to access the new Xyz property, referring to the optional attribute introduced in
// v1.1: this should fail.
evt.Xyz = 1;

// Access the xyz attribute by name, as an extension attribute.
// This should work, even though the value wouldn't be valid in a v1.1 event.
evt["xyz"] = "test";

// Likewise accessing the property for an event parsed from elsewhere:
evt = httpRequest.ParseCloudEvent();
// If evt is v1.0, this should fail *even if it has an xyz attribute value that's valid in v1.1.
int xyz = evt.Xyz;
```

Setting a value within an event where the version indicates that the attribute *is* known should
validate the attribute value according to that version. Example:

```csharp
// Create a v1.1 event
var evt = new CloudEvent(CloudEventsSpecVersion.V1_1);

// This should work: 1 is a valid value, and xyz is known in v1.1
evt.Xyz = 1;

// This should fail: 123 is not a valid value for xyz in v1.1
evt.Xyz = 123;

// This should fail to compile, where that's feasible: xyz should always be an integer
evt.Xyz = "test";

// This should succeed at execution time
evt["xyz"] = 123;

// This should fail at execution time due to validation
evt["xyz"] = "test";

// This should fail at execution time due to validation
evt["xyz"] = 123;
```

### "Changing" event versions

An SDK may provide the ability to change the specversion of an event,
or (preferred) create a new object based on the old one. When "upgrading" an event's specversion,
the SDK should perform validation as if parsing the event from scratch. Examples:

```csharp
// Successful upgrade: no xyz value
var evt10 = new CloudEvent(CloudEventsSpecVersion.V1_0) { Id = "..." };
var evt11 = evt10.WithSpecVersion(CloudEventsSpecVersion.V1_1);

// Successful upgrade: valid value for xyz
var evt10 = new CloudEvent(CloudEventsSpecVersion.V1_0)
{
    Id = "...",
    ["xyz"] = 10
};
evt11 = evt10.WithSpecVersion(CloudEventsSpecVersion.V1_1);

// Failed upgrade: invalid value for xyz
var evt10 = new CloudEvent(CloudEventsSpecVersion.V1_0)
{
    Id = "...",
    ["xyz"] = "test"
};
evt11 = evt10.WithSpecVersion(CloudEventsSpecVersion.V1_1);

// Successful downgrade
var evt11 = new CloudEvent(CloudEventsSpecVersion.V1_1)
{
    Id = "...",
    Xyz = 10
};
evt10 = evt11.WithSpecVersion(CloudEventsSpecVersion.V1_0);
// Access to evt10.Xyz would fail as described above;
// access to evt10["xyz"] would return 10.
// Setting evt10["xyz"] to "test" or 123 could fail or succeed - it's
// up to the SDK to decide (and document!) whether downgrading retains constraints
// for attributes that were present in the original event.
// TODO: What about if Xyz hadn't been present before? Should evt10["xyz"] = "test" fail then?
```

Until we have a new major version, we probably don't want to specify whether
SDKs should allow upgrade/downgrade across major versions.

### Handling unknown versions

An SDK which supports minor versions **MUST** be able to parse events with
a minor version of which it's unaware, but **MUST NOT** parse events with a
*major* version of which it's unaware. In other words, a v1.1-aware SDK must
be able to parse a v1.2 event, but must reject any attempt to parse a v2.0 event.
This is because a v2.0 event might use an entirely different format or type system,
whereas a v1.2 event can always be understood in the v1.x type system, and all
attributes should be valid in the context of v1.1 and v1.0.

All SDKs must support all minor versions for each major version they support, up
to the highest minor version they're aware of. (So when spec version v1.2 is published, it's fine for
an SDK to only support v1.0 and v1.1, but it must not support *only* v1.1 or *only* v1.2.)

When parsing an event with an unknown minor version:

- All attribute values must be retained, with as much type information as is available
  (defaulting to string when type information is not available)
- Values of unknown attributes must be readable as if they're regular extension attributes
  (so a minor-version aware SDK that only supports v1.0 must allow access to `xyz` of
  a v1.1 event after receiving it)
- All attribute values must be validated according to the highest-known minor version
  within the same major version
- The original specversion must be retained, and available to SDK users
- If changing event versions is supported, the SDK should allow an event of an unknown minor
  version to be downgraded to a known minor version, but should *not* allow an event
  to be upgraded to an unknown minor version.

After an event with an unknown minor version has been parsed, an SDK *may* enforce that
extension attributes cannot be modified. This ensures that the SDK can serialize the event
and still end up with a valid event, assuming it was originally parsed from a valid event,
even if some attributes are changed by the user. That's fine so long as we know what values
are valid for those attributes. (Note: this requires that we never add any cross-validation
between attributes.)

## Overall compatibility

With the above in place *and* when using an SDK with minor versions, we get the result of:

- Being able to add new optional attributes in minor versions, including constraints
- Being able to consume events which we don't fully understand
- Being able to continue producing events of older versions, even if the same attribute values
  wouldn't be valid for later versions
- Being confident that we don't "break" events by modifying an event we don't fully understand
  in an invalid way, and then emitting it.

This feels like a reasonable justification for deeming such a change to be "backward compatible"
in a SemVer sense, as far as we possibly can.
