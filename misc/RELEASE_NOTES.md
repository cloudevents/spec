# CloudEvents Release Notes

## v1.0.2 - 2022/02/03

- Add C# namespace option to proto - #937
- Tweak SDK requirements wording - #915
- Re-organized repo directory structure - #904/#905
- Translate CE specs into Chinese - #899/#898
- Explicitly state application/json defaulting when serializing - #881
- Add PowerShell SDK to the list of SDKs - #875
- WebHook "Origin" header concept clashes with RFC6454 - #870
- Clarify data encoding in JSON format with a JSON datacontenttype - #861
- Webhook-Allowed-Origin instead of Webhook-Request-Origin - #836
- Clean-up of Sampled Rate Extension - #832
- Remove the conflicting sentence in Kafka Binding - #823/#813
- Fix the sentences conflict in Kafka Binding - #814
- Clarify HTTP header value encoding and decoding requirements - #793
- Expand versioning suggestions in Primer - #799
- Add support for protobuf batch format - #801
- Clarify HTTP header value encoding and decoding requirements - #816
- Primer guidance for dealing with errors - #763
- Information Classification Extension - #785
- Clarify the role of partitioning extension in Kafka - #727

## v1.0.1 - 2020/12/12
- Add protobuf format as a sub-protocol - #721
- Allow JSON values to be null, meaning unset - #713
- [Primer] Adding a Non-Goal w.r.t Security - #712
- WebSockets protocol binding - #697
- Clarify difference between message mode and HTTP content mode - #672
- add missing sdks to readme - #666
- New sdk maintainers rules - #665
- move sdk governance and cleanup - #663
- Bring 'datadef' definition into line with specification - #658
- Add CoC and move some governance docs into 'community' - #656
- Add blog post around understanding Cloud Events interactions - #651
- SDK governance draft - #649
- docs: add common processes for SDK maintainers and contributors - #648
- Adding Demo for Cloud Events Orchestration - #646
- Clarified MUST requirement for JSON format - #644
- Re-Introducing Protocol Buffer Representation - #626
- Closes #615 - #616
- Reworked Distributed Tracing Extension - #607
- Minor updates to Cloud Events Primer - #600
- Kafka clarifications - #599
- Proprietary binding spec inclusion guide - #595
- Adding link to Pub/Sub binding - #588
- Add some clarity around SDK milestones - #584
- How to determine binary CE vs random non-CE message - #577
- Adding Visual Studio Code extension to community open-source doc - #573
- Specify encoding of kafka header keys and values and message key - #572
- Fix distributed tracing example - #569
- Paragraph about nested events to the primer - #567
- add rules for changing Admins- #564
- Updating JSON Schema - #563
- Say it's ok to ignore non-MUST recommendations - at your own risk - #562
- Update Distributed Tracing extension spec links - #550
- Add Ruby SDK to SDK lists - #548

## v1.0.0 - 2019/10/24
- Use "producer" and "consumer" instead of "sender" and "receiver"
- Clarification that intermediaries should forward optional attributes
- Remove constraint that attribute names must start with a letter
- Remove suggestion that attributes names should be descriptive and terse
- Clarify that a single occurrence may result in more than one event
- Add an Event Data section (replacing `data`), making event data a top level
  concept rather than an attribute
- Introduce an Event Format section
- Define structured-mode and binary-mode messages
- Define protocol binding
- Add extension attributes into "context attributes" description
- Move mention of attribute serialization mechanism from "context attributes"
  description into "type system"
- Change "transport" to "protocol" universally
- Introduce the Boolean, URI and URI-reference types for attributes
- Remove the Any and Map types for attributes
- Clarify which Unicode characters are permitted in String attributes
- Require all context attribute values to be one of the listed types,
  and state that they may be presented as native types or strings.
- Require `source` to be non-empty; recommend an absolute URI
- Update version number from 0.3 to 1.0
- Clarify that `type` is related to "the originating occurrence"
- Remove `datacontentencoding` section
- Clarify handling of missing `datacontenttype` attribute
- Rename `schemaurl` to `dataschema`, and change type from URI-reference to URI
- Constrain `dataschema` to be non-empty (when present)
- Add details of how `time` can be generated when it can't be determined,
  specifically around consistency within a source
- Add details of extension context attribute handling
- Add recommendation that CloudEvent receivers pass on non-CloudEvent metadata
- Sample CloudEvent no longer has a JSON object as a sample extension value
