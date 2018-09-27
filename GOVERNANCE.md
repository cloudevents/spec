# Governance

This document describes the governance process under which the CloudEvents
project will manage this repository.

## Meetings

In order to provide equitable rights to all members,
the following process will be followed:

* Official conference calls will be announced at least a week in advance.
* Official face-to-face meetings will be announced at least 4 weeks in
  advance.
* Proposed changes to any document will be done via a Pull Request (PR).
* PRs will be reviewed during official meetings, but off-line reviews
  (LGTMs, NOT LGTMs) and comments are strongly encouraged to gauge the
  group's opinion on the proposed change prior to the meeting.
* During meetings, priority will be given to PRs that appear to be ready for
  a vote over those that appear to require discussions.
* PRs should not be merged if they have had substantial changes made within
  two days of the meeting.
  Rebases, typo fixes, etc. do not count as substantial.
  Note, administrivia PRs that do not materially modify output documents
  may be processed by admins as needed.
* Resolving PRs ("merging" or "closing with no action") will be done as a
  result of a motion made during a meeting, and approved.
* Reopening a PR can be done if new information is made available, and a
  motion to do so is approved.
* Any motion that does not have "unanimous consent" will result in a formal
  vote. See [Voting](#voting).

## Membership

There are three categories of project membership:
1 - Member. This is anyone who participates in the group's activities in any
    of our communication channels (email, github issues/PRs, meetings, etc.).
    No formal registration process is needed.
2 - Voting Member. See the (Voting)[#voting]section below for more information
    on how the list of Voting Members are determined. During the normal
    operations of the group, Voting Members and Members are the same with
    respect to influence over the groups actions. The rights associated with
    being a Voting Member only apply in the event of a formal vote being taken.
3 - Admin. Admins are Members of the group but have the ability to perform
    administrative actions on behalf of the group. For example, manage the
    website, github repos and moderate the meetings. Their actions should
    be done with the knowledge and consent of the group. They also have the
    ability to merge/close PRs, but only per the group's approval. See
    the [OWNERS](OWNERS) file for the current list of Admins.

## PRs

Typically, PRs are expected to meet the following criteria prior to being
merged:

* The author of the PR indicates that it is ready for review by asking for it
  to be discussed in an upcoming meeting - eg. by adding it to the agenda
  document.
* All comments have been addressed.
* PRs that have objections/concerns will be discussed off-line by interested
  parties. A resolution, updated PR, will be expected from those talks.

## Voting

If a vote is taken during a meeting, the follow rules will be followed:

* There is only 1 vote per participating company, or nonaffiliated individual.
* Each participating company can assign a primary and secondary representative.
* A participating company, or nonaffiliated individual, attains voting rights
  by having any of the entity's assigned representative(s) attend 3 out of the
  last 4 meetings. If the primary representative can not attend a meeting, the
  delegate's attendance is counted. The entity obtains voting rights after the
  3rd meeting, not during.
* Only members with voting rights will be allowed to vote.
* A vote passes if more than 50% of the votes cast approve the motion.
* Only "yes" or "no" votes count, "abstain" votes do not count towards the
  total.
* Meeting attendance will be formally tracked
  [here](https://docs.google.com/spreadsheets/d/1bw5s9sC2ggYyAiGJHEk7xm-q2KG6jyrfBy69ifkdmt0/edit#gid=0).
  Members must acknowledge their presence verbally, meaning, adding yourself
  to the "Attendees" section of the Agenda document is not sufficient.
* When a vote is called, unless all voting members have voted, the vote will be
  tallied no less than one week after calling the vote.
* Voting process:
  * Comment on the PR: "YES VOTE", "NO VOTE", or "ABSTAIN".
  * Any person is encouraged to vote with a statement of support or dissent to
    help undecided voters to reach a decision
  * Comments are welcome from non-members
  * Voting tally will reflect the above qualification and recorded in PR

## Release Process

To create a new release:
* Create a PR that modifies the [README](README.md), and all specifications
  (ie. *.md files) that include a version string, to the new release
  version string.
* Merge the PR.
* Create a [new release](https://github.com/cloudevents/spec/releases/new):
  * Choose a "Tag version" of the form: `vX.Y`, e.g. `v0.1`
  * Target should be `master`, the default value
  * Release title should be the same as the Tag - `vX.Y`
  * Add some descriptive text, or the list of PRs that have been merged
    since the previous release.
    The git query to get the list commits since the last release is:
    `git log --pretty=format:%s master...v0.1`.
    Just replace "v0.1" with the name of the previous release.
  * Press `Publish release` button

