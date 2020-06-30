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
   [Contribution Acceptance](../SDK.md#contribution-acceptance)
5. Issues and PRs are triaged (labeled, commented, reviewed, etc) regularly

We define a project `cloudevents/sdk-x` _not actively maintained_ if:

6. Issues and/or PRs are not being triaged from `sdk-x-mantainers` for 2 months
7. Security patches are not being **released** from `sdk-x-mantainers` for 1
   months from CVE disclosures

It may happen that there has been no necessary activity within the SDK for at
least 4 months. The other SDK maintainers will evaluate what "no necessary
activity" means, but often this could mean "no commits", or "no issue
discussions". However, if the SDK is stable and does not need to be update then
it might be determined that it current state is acceptable.

To prevent the project from becoming _not actively maintained_, the community
MAY takes the following actions:

- Temporary security patches delivered by an _sdk maintainer_ not part of
  `sdk-x-maintainers` group
- Handover of the project to a new maintainer
- Archive the project

### Security patches

If a project `cloudevents/sdk-x` meets _healthy_ criteria 1, 2, 4, but the
`sdk-x-maintainers` group is not actively performing security patches as defined
in criteria 7, the community could decide to entitle one or more members from
the larger _sdk maintainers_ group to perform security patches and release new
minor versions of the project.

Because the people entitled to perform security patches need write permissions
on the repository, the community must temporarily grant these permissions. After
the release of the patch, these permissions must be revoked.

Because of the urgent nature of security patches, an _informal_ vote during the
CloudEvents SDK meeting is enough to assign the security patch to the _sdk
maintainer(s)_ who volunteers to take care of it.

NOTE: this process is valid only for security patches, not for bugs or
enhancements.

### Handover to a new maintainer/group of maintainers

If a project is not meeting the criteria 1, 2, 4, 5, 6, 7, the community MAY
decides to handover the project to a new maintainer/group of maintainers. The
community can perform the handover to a new maintainer if all the following
conditions are met:

- A vote to add the new maintainer must have **already taken place** with all
  people entitled to vote abstaining.
- One of the following conditions had been met:
  - The new maintainer(s) already meet the requirements enlisted in
    [New maintainers section](#new-maintainers)
  - The new maintainer(s) performed the required PRs, Reviews and Code changes
    to meet the [New maintainers criteria](#new-maintainers) but they were
    unable to merge them due to inactivity of the current maintainer(s).

The new maintainer must show the good will to keep the project healthy and
community could ask for an eventual plan to improve the quality of the project.

Once a new maintainer is identified, the community can proceed with a vote to
handover the project using the
[Asynchronous voting process](#asynchronous-voting-process). If more than one
new maintainer wants to maintain the project, separate voting process must be
done for all of them, and all of them must follow the same voting criteria (and
not the ones from [New maintainers section](#new-maintainers)).

The voting criteria are:

- 1 week to vote
- At least 2/3 of the votes cast agree to the proposal
- All _sdk maintainers_ are entitled to vote

### Archive a project

If a project is not following the criteria 1, 2, 4, 5, 6, 7, the community MAY
decides to archive the project. Prior to archiving, the community SHOULD first
consider performing a search for a new maintainer to
[handover the project](#handover-to-a-new-maintainergroup-of-maintainers).

If no new maintainer is found, the community can proceed to archive the project
using the [Asynchronous voting process](#asynchronous-voting-process).

The voting criteria are:

- 2 weeks to vote
- At least 2/3 of the votes cast agree to the proposal
- All _sdk maintainers_ are entitled to vote

## Asynchronous voting process

In order to ensure the democratic management of debates in the community, we
define an asynchronous voting process using GitHub issues.

The voting is defined by:

- The proposed community change to vote
- The set of people/groups entitled to vote
- A voting period
- The percentage of agreements required to accept the change
- A voting manager, a member of the community entitled to manage the vote. The
  voting manager must be part of people entitled to vote.

To start a vote, the voting manager opens an issue in the
[CloudEvents Spec](https://github.com/cloudevents/spec/issues) with:

- A binary question to be voted on
- Github IDs of people who are entitled to vote
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
writing on the issue the results. Votes after the expiration date must not be
considered; To calculate the agreement percentage, the voting manager should
account the people who have expressed a vote, without taking in account the
abstentions.

If the vote passes, the voting manager should proceed with the change. If the
vote does not pass, then a new vote for the same change must NOT happen for the
next 6 months.

This voting process must be used only to resolve the issues identified in this
document:

- Change to the rules in this document
- Add a new maintainer
- Handover of a project to a new maintainer
- Archive a project
