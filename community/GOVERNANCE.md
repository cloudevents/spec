# Governance

This document describes the governance process under which the CloudEvents
project will manage this repository.

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
  vote over those that appear to require discussions.
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

2. **Voting Member.** See the (Voting)[#voting]section below for more
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

## Voting

If a vote is taken during a meeting, the follow rules will be followed:

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
  would not apply. Absence from meetings during that time will not impact
  their voting rights.
- Only members with voting rights will be allowed to vote.
- A vote passes if more than 50% of the votes cast approve the motion.
- Only "yes" or "no" votes count, "abstain" votes do not count towards the
  total.
- Meeting attendance will be formally tracked
  [here](https://docs.google.com/spreadsheets/d/1bw5s9sC2ggYyAiGJHEk7xm-q2KG6jyrfBy69ifkdmt0/edit#gid=0).
  Members must acknowledge their presence verbally, meaning, adding yourself to
  the "Attendees" section of the Agenda document is not sufficient.
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

- The versioning scheme used will follow [semver](https://semver.org/)
- All normative specifications, and the Primer, will be grouped together into a
  single logical unit and released at the same time, at the same version number.
  This is true regardless of whether each individual document actually changed
  during the release cycle.
- When a new release of a specification is ready, it will be given a version
  number matching the appropriate semver version string but with a suffix of
  `-rc#` (release candidate). This will indicate that the authors believe it
  is ready for final release but it needs to go through a testing period to
  allow for broader testing before it promoted to its final version number.
  This will be true for updates to existing specifications and for new
  specifications.
- Since changing the CloudEvents `specversion` string could have a significant
  impact on implementations, all non-breaking changes will be made as
  "patch" version updates - this allows for the value "on the wire" to remain
  unchanged. If a breaking change is introduced the normal semver rules will
  apply and the "major" version number will change. The net effect of this is
  that the "minor" version number will always be zero and the `specversion`
  string will always be of the form `X.0`.
- Additionally, the working group has decided that "patch" changes that are
  trivial in nature (e.g. typos) can be merged directly into the latest
  release without a version number change and without creating a new formal
  "patch" branch/release. Non-trivial "patch" changes will necessitate the
  creation of a new "patch" branch (e.g. `1.0.2-wip`) and release cycle that
  will eventually result in an official "patch" release (e.g. `1.0.2`)

Note that these rules do not apply to the
[documented extensions](../cloudevents/documented-extensions.md).

To create a new release:

- Create a PR that modifies the [README](README.md), and all specifications (ie.
  \*.md files) that include a version string, to the new release version string.
  Make sure to remove `-wip` from all of the version strings.
- Merge the PR.
- Create a [new release](https://github.com/cloudevents/spec/releases/new):
  - Choose a "Tag version" of the form: `vX.Y`, e.g. `v0.1`
  - Target should be `master`, the default value
  - Release title should be the same as the Tag - `vX.Y`
  - Add some descriptive text, or the list of PRs that have been merged since
    the previous release. The git query to get the list commits since the last
    release is:
    `git log --pretty=format:%s master...v0.1 | grep -v "Merge pull"`.
    Just replace "v0.1" with the name of the previous release.
  - Press `Publish release` button
- Create a PR that modifies the version string in all of the files
  (but not the README.md table) to be the next version number with a `-wip`
  in it (e.g `v0.4-wip`).
- Merge the PR.
- Create an "announcement" highlighting the key features of the new release and
  any potential noteworthy activities of the group:
  - Send it to the mailing list
  - Announce the release on our
    [twitter account](http://twitter.com/cloudeventsio)
  - Add it to the "announcement" section of our
    [website](https://cloudevents.io/)

## Additional Information

- We adhere to the CNCF's
  [Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md) guidelines
