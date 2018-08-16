# Governance

This document describes the governance process under which the Serverless
Working Group (WG) will manage this repository.

## Working Group Meetings

In order to provide equitable rights to all Working Group members,
the following process will be followed:

* Official WG meetings will be announced at least a week in advance.
* Proposed changes to any document will be done via a Pull Request (PR).
* PRs will be reviewed during official WG meetings.
* During meetings, priority will be given to PRs that appear to be ready for
  a vote over those that appear to require discussions.
* PRs should not be merged if they have had substantial changes made within
  two days of the meeting.
  Rebases, typo fixes, etc. do not count as substantial.
  Note, administrivia PRs that do not materially modify WG output documents
  may be processed by WG admins as needed.
* Resolving PRs ("merging" or "closing with no action") will be done as a
  result of a motion made during a WG meeting, and approved.
* Reopening a PR can be done if new information is made available, and a
  motion to do so is approved.
* Any motion that does not have "unanimous consent" will result in a formal
  vote. See [Voting](#voting).

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

If a vote is taken during a WG meeting, the follow rules will be followed:

* There is only 1 vote per participating company, or nonaffiliated individual.
* Each participating company can assign a primary and secondary representative.
* A participating company, or nonaffiliated individual, attains voting rights
  by having any of their assigned representative(s) attend 3 out of the last
  4 meetings. They obtain voting rights after the 3rd meeting, not during.
* Only WG members with voting rights will be allowed to vote.
* A vote passes if more than 50% of the votes cast approve the motion.
* Only "yes" or "no" votes count, "abstain" votes do not count towards the
  total.
* Meeting attendance will be formally tracked
  [here](https://docs.google.com/spreadsheets/d/1bw5s9sC2ggYyAiGJHEk7xm-q2KG6jyrfBy69ifkdmt0/edit#gid=0).
  Members must acknowledge their presence verbally, meaning, adding yourself
  to the "Attendees" section of the Agenda document is not sufficient.
* When a vote is called, votes will be collected over the following week: 
  * Comment on the PR: "agree, yes, +1", "disagree, no, -1", or "abstain".
  * Any person is encouraged to vote with a statement of support or dissent to
    help undecided voters to reach a decision
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

