## SDK Community

The community is organized as follows:

- Every SDK has its own
  [Github Team](https://github.com/orgs/cloudevents/teams), for example
  `sdk-go-maintainers` is the group of mantainers for
  [cloudevents/sdk-go project](https://github.com/cloudevents/sdk-go)
- The union of all the `sdk-*-maintainers` assembles the _sdk maintainers_ group

## New maintainers

TBD

## Ensuring projects health

In order to ensure the health of the SDK projects, we define the following
actions. These are crucial to show the commitment of the community to develop
and support these libraries, which are an important part of the CloudEvents
ecosystem.

We define an SDK project _healthy_ if:

1. It works with the latest version of the programming language
2. It supports the latest versions of the integrated libraries/frameworks
3. It receives security patches regularly
4. It supports the last N-1 major versions of CloudEvents spec, as defined in
   [Contribution Acceptance](../SDK.md#Contribution-Acceptance)
5. Issues and PRs are triaged (labeled, commented, reviewed, etc) regularly

We define a project `cloudevents/sdk-x` _not actively maintained_ if:

6. No commits on master from `sdk-x-maintainers` since 4 months
7. Issues and/or PRs are not being triaged from `sdk-x-mantainers` since 2
   months
8. Security patches are not being **released** from `sdk-x-mantainers` since 1
   months from CVE disclosures

To prevent projects _not actively maintained_, we define different actions the
community might take:

- Temporary security patches delivered by an _sdk maintainer_ not part of
  `sdk-x-maintainers` group
- Handover of the project to a new maintainer
- Archive the project

### Security patches

If a project `cloudevents/sdk-x` meets _healthy_ criteria 1, 2, 4, but the
`sdk-x-maintainers` group is not actively performing security patches as defined
in criteria 8, the community could decide to entitle one or more members from
the larger _sdk maintainers_ group to perform security patches and release new
minor versions of the project.

Because the people entitled to perform security patches needs write rights on
the repo, the community MUST temporary assign him/them the rights to perform it.
After the release of the patch, these rights MUST be removed from the member(s)
who took care of it.

Because of the urgency nature of security patches, an _informal_ vote during the
CloudEvents SDK meeting is enough to assign the security patch to the _sdk
maintainer(s)_ which volunteers to take care of it.

NOTE: this process is valid only for security patches, not for bugs or
enhancements.

### Handover to a new maintainer/group of maintainers

It may happen that, if a project is not following the criteria 1, 2, 4, 5, 6, 7,
8, the community might decide to handover the project to a new maintainer/group
of maintainers. The community can perform the handover to a new maintainer
**iff** a voting process to add such maintainer was **already performed** with
100% of entitled people abstained and:

- Or the new maintainer(s) already meet the requirements enlisted in
  [New maintainers section](#new-maintainers),
- Or, because of the inactivity of the project due to criteria 7, the new
  maintainer(s) performed the required PRs/Reviews/Code changes to meet the
  [New maintainers criteria](#new-maintainers) but he/they wasn't/weren't able
  to merge them.

The new maintainer must show the good will to keep the project healthy and
community could ask for an eventual plan to improve the quality of the project.

As soon as the new maintainer is identified, the community can proceed to vote
to handover the project using the
[Asynchronous voting process](#asynchronous-voting-process). If more than one
new maintainer wants to handover the project, separate voting process must be
done for all of them, and both of them must follow the same voting criteria (and
not the ones from [New maintainers section](#new-maintainers)).

The voting criteria are:

- 1 week to vote
- 2/3 of the agreement to accept the vote
- All _sdk maintainers_ are entitled to vote

### Archive a project

It may happen that, if a project is not following the criteria 1, 2, 4, 5, 6, 7,
8, the community might decide to archive the project. Prior to archiving the
project, the community should consider first to search a new maintainer to
[handover the project](#handover-to-a-new-maintainergroup-of-maintainers).

If no new maintainer is found, the community can proceed to archive the project
using the [Asynchronous voting process](#asynchronous-voting-process).

The voting criteria are:

- 2 weeks to vote
- 2/3 of the agreement to accept the vote
- All _sdk maintainers_ are entitled to vote

## Asynchronous voting process

In order to ensure the democratic management of debates in the community, we
define an asynchronous voting process using GitHub issues.

The voting is defined by:

- The proposed community change to vote
- The set of people/groups entitled to vote
- A voting period
- The percentage of agreements required to accept the change
- A member of the community entitled to manage the vote, called voting manager.
  The voting manager MUST also be part of people entitled to vote.

To start a vote, the voting manager opens an issue in the
[CloudEvents Spec](https://github.com/cloudevents/spec/issues) with:

- The binary question which explains the change
- The tags to the entitled people/groups to vote (depending on the question)
- The expiration date of the vote
- The percentage of agreements to accept the change

For example:

> Question: Do you want to add "Paolo Rossi" @paolorossi as _sdk-go-maintainer_?
>
> Entitled to vote:
>
> - @sdk-go-maintainers
>
> Voting ends: 24th June 2020 12:00 CEST
>
> Required agreement: 50% + 1

Then every person entitled can vote, up to the expiration date, commenting on
the issue with a `+1` to express agreement or `-1` to express disagreement.
Every comment except `+1` and `-1` won't be taken in account, because we expect
that the voting process comes only after a debate on the change, developed on
the community channels and Serverless WG/CloudEvents SDK meetings. In order to
ensure visibility to the voting, people should be remembered to vote during
Serverless WG meetings and community channels (Slack, ...).

At the end of the voting period, the voting manager will count the votes,
writing on the issue the results. Votes after the expiration date MUST not be
considered; To calculate the agreement percentage, the voting manager should
account the people who have expressed a vote, without taking in account the
abstentions.

If the vote pass, the voting manager should proceed with the change. If the vote
does not pass, then a new voting for the same change can't be started for the
next 6 months.

This voting process MUST be used only to resolve the debates underlined in this
document:

- Change to the rules in this document
- Add a new maintainer
- Handover of a project to a new maintainer
- Archive a project
