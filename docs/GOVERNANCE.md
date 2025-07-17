# Governance

<!-- no verify-specs -->

This document describes the governance process under which the CloudEvents
project will manage this repository.

## Table of Contents & References

- [Meetings](#meetings)
- [Membership](#membership)
  -  [Admins](#admins)
- [PRs](#prs)
- [Voting](#voting)
- [Release Process and Versioning](#release-process-and-versioning)
- [Additional Information](#additional-information)

For easy reference, additional documentation related to how this project,
and its subprojects, operate are listed below:
  - [Contributing](CONTRIBUTING.md)
    - [List of contributors to the project](contributors.md)
  - [Project Releases](RELEASES.md)
  - [Project Roadmap](ROADMAP.md)
  - [SDK Governance](SDK-GOVERNANCE.md)
    - [SDK Maintainer Guidlines](SDK-maintainer-guidelines.md)
    - [SDK PR Guidlines](SDK-PR-guidelines.md)

## Meetings

In order to provide equitable rights to all members, the following process will
be followed:

- Official conference calls will be announced at least a week in advance.
- Official face-to-face meetings will be announced at least 4 weeks in advance.
- Proposed changes to any document will be done via a Pull Request (PR).
- PRs will be reviewed during official meetings, but off-line reviews (LGTMs,
  NOT LGTMs) and comments are strongly encouraged to gauge the group's opinion
  on the proposed change prior to the meeting.
- During meetings, priority will be given to PRs that appear to be ready for a
  vote over those that appear to require discussions. See [PRs](#prs) for more
  information.
- PRs should not be merged if they have had substantial changes made within two
  days of the meeting. Rebases, typo fixes, etc. do not count as substantial.
  Note, administrivia PRs that do not materially modify output documents may be
  processed by admins as needed.
- Resolving PRs ("merging" or "closing with no action") will be done as a result
  of a motion made during a meeting, and approved.
- Reopening a PR can be done if new information is made available, and a motion
  to do so is approved.
- Any motion that does not have "unanimous consent" will result in a formal
  vote. See [Voting](#voting).

## Membership

There are three categories of project membership:

1. **Member.** This is anyone who participates in the group's activities in any
   of our communication channels (email, github issues/PRs, meetings, etc.). No
   formal registration process is needed.

2. **Voting Member.** See the [Voting](#voting) section below for more
   information on how the list of Voting Members are determined. During the
   normal operations of the group, Voting Members and Members are the same with
   respect to influence over the groups actions. The rights associated with
   being a Voting Member only apply in the event of a formal vote being taken.

3. **Admin.** Admins are Members of the group but have the ability to perform
   administrative actions on behalf of the group. For example, manage the
   website, github repos and moderate the meetings. Their actions should be done
   with the knowledge and consent of the group. They also have the ability to
   merge/close PRs, but only per the group's approval. See the
   [OWNERS](../OWNERS) file for the current list of Admins.

### Admins

Since the role of an 'Admin' is mainly administrative, the list of Members
within this group should not need to change regularly. The following rules
govern adding and removing Admins:

- New Admins can be proposed via a PR to edit the [OWNERS](../OWNERS) file.
  Normal PR voting rules apply.
- Admins can be removed via a PR to edit the [OWNERS](../OWNERS) file. Normal
  PR voting rules apply.
- Admins can request to be removed via a PR to edit the [OWNERS](../OWNERS)
  file.  Since the group can not force an Admin to continue in that role, the PR
  does not follow the normal voting rules and can be merged by any of the
  Admins, including the person requesting to be removed. The exception to
  this "self-merge" aspect is when they are the last Admin. See next bullet.
- If a PR to edit the list of Admins would result in there not being any
  Admins remaining, then the state of the project would need to be decided
  first since a project without any Admins might imply that the project should
  be shutdown.

## PRs

Typically, PRs are expected to meet the following criteria prior to being
merged:

- The author of the PR indicates that it is ready for review by asking for it to
  be discussed in an upcoming meeting - eg. by adding it to the agenda document.
- All comments have been addressed.
- PRs that have objections/concerns will be discussed off-line by interested
  parties. A resolution, updated PR, will be expected from those talks.

Anyone is welcome to comment on PRs, not just Admins, voting members or
regular call participants. The goal of the project is consensus and broad
community support, so community input is strongly encouraged.

## Voting

If a vote is taken, the follow rules will be followed:

- There is only 1 vote per participating company, or nonaffiliated individual.
- Each participating company can assign a primary and secondary representative.
- A participating company, or nonaffiliated individual, attains voting rights by
  having any of the entity's assigned representative(s), in aggregate, attend 3
  out of the last 4 meetings. The people listed as "primary" or "alternate" for
  an entity can be changed no more than once a month and can be changed by
  notifying one of the admins. The entity obtains voting rights after the 3rd
  meeting, not during.
- A "primary" or "alternate" member may request a leave-of-absence via an
  e-mail to the mailing list, or a message to the
  [public slack channel](../README.md#communications), prior to the absence.
  An acceptable absence would include situations where the person is not
  officially working at all, such as being on vacation, taking a sabbatical or
  there is a public holiday. However, situations such as a scheduling conflict
  would not apply. Absence from meetings during a leave-of-absence will not
  impact their voting rights.
- Only members with voting rights will have their vote counted towards the
  decision.
- A vote passes if more than 50% of the votes cast approve the motion.
- Only "yes" or "no" votes count, "abstain" votes do not count towards the
  total.
- Meeting attendance will be formally tracked
  [here](https://docs.google.com/spreadsheets/d/1bw5s9sC2ggYyAiGJHEk7xm-q2KG6jyrfBy69ifkdmt0/edit#gid=0).
  Members must acknowledge their presence verbally, meaning, adding yourself to
  the "Attendees" section of the Agenda document is not sufficient. An Admin
  will be responsible for updating the spreadsheet.
- When a vote is called, unless all voting members have voted, the vote will be
  tallied no less than one week after calling the vote.
- Voting process:
  - Comment on the PR: "YES VOTE", "NO VOTE", or "ABSTAIN".
  - Any person is encouraged to vote with a statement of support or dissent to
    help undecided voters to reach a decision
  - Comments are welcome from non-members
  - Voting tally will reflect the above qualification and recorded in PR

## Release Process and Versioning

The specifications produced will adhere to the following:

- The versioning scheme used will follow [semver](https://semver.org/).

- Specifications will be grouped into logical units and released at the same
  time, with the same version number. This is true regardless of whether each
  individual document actually changed during the release cycle. The
  determination of the number of groups, and which document belongs in a group,
  can change over time.

- Since changing the CloudEvents `specversion` string could have a significant
  impact on implementations, all non-breaking changes will be made as
  "patch" version updates - this allows for the value "on the wire" to remain
  unchanged. If a breaking change is introduced the normal semver rules will
  apply and the "major" version number will change. The net effect of this is
  that the "minor" version number will always be zero and the `specversion`
  string will always be of the form `X.0`.

Note that these rules do not apply to unversioned documents, such as the
[documented extensions](../cloudevents/extensions/README.md).

To create a new release:

- Periodically the group will examine the list of extensions to determine
  if any action should be taken (e.g. removed due to it being stale). The
  creation of a new release will be the reminder to do this check. If any
  changes are needed then PRs will be created and reviewed by the group.

- For the most part we try to only use a single branch ("main") for our work.
  Git branches will be used as a way to snapshot/tag releases. While we hope
  to not push new commits to these branches, in practice, it is possible that
  changes to a release might be needed without "picking up" other changes that
  might have been commited to "main". Creating the branch during the release
  process will makes this easier to manage should the need should arise.

- Determine the new release version string. It should be of the form:
  `<subject>/vX.Y.Z`, e.g. `cloudevents/v1.0.4` or `subscriptions/v1.0.0`.

- Create a PR (for the "main" branch") that:
  - Modifies the repo's files to use the new version string appended with
    `-rc#` as appropriate. Make sure to remove all `-wip` suffixes as needed.
  - Merge the PR.
  - Initiate a final review/test of the release.

- A "release candidate" tag will be created with the new release version
  string but with a suffix of `-rc#` (release candidate). This will indicate
  that the authors believe it is ready for final review/testing. This will be
  true for updates to existing specifications and for new specifications.

- When review/testing is completed, create a PR (for the "main" branch") that:
  - Modifies the repo's files to use the new version string (w/o `-rc#`) as
    appropriate.
  - Update [RELEASES.md](RELEASES.md) to mention the new release, and
    reference the yet-to-be-created release tag.
  - Update the appropriate `*/RELEASE_NOTES.md` file with the changes
    for the release. The list can be generated via:
    `git log --pretty=format:%s main...v0.1 | grep -v "Merge pull"`
    by replacing "v0.1" with the name of the previous release. Or, use github's
    [new release](https://github.com/cloudevents/spec/releases/new) process
    to generate the list w/o actually creating the release yet.

- Merge the PR.
  - Note that the link checker should fail since any references to the new
    release tag will not be valid yet. This is expected.

- Create a new branch with the same name as the new release version string
  appended with `-branch` (e.g. `<subject>/vX.Y.Z-branch`).
  - Use Github to create a
    [new release](https://github.com/cloudevents/spec/releases/new).
    During that process, create a new tag with the new release version
    string (e.g. `<subject>/vX.Y.Z`) w/o any suffix.
  - Rerun the github CI actions from the previous PR and the "main" branch as
    they should all pass now; as a sanity check.

- Create an "announcement" highlighting the key features of the new release
  and any potential noteworthy activities of the group:
  - Send it to the mailing lists.
  - Announce the release on our [X account](http://x.com/cloudeventsio).
  - Add it to the "announcement" section of our
    [website](https://cloudevents.io/).

- If an update to a release is needed, create a PR for the appropriate
  branches (including "main"), and merge when ready. For any release that's
  updated, you'll need to move the tag for that release to point to the HEAD
  of that branch. We'll eventually setup a Github action to automatically do
  it but for now you can do it via the CLI:
  - `git pull` to make sure you have all latest branches and tags
  - `git tag -d vX.Y.Z` to delete the old tag for the release
  - `git tag vX.Y.Z vX.Y.Z-branch` to create a new tag for the HEAD of the
    release branch
  - `git push REMOTE vX.Y.Z -f` to force the tag to updated in the github repo

## Additional Information

- We adhere to the CNCF's
  [Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md) guidelines
