# SDK Maintainer's Guide

<!-- no verify-specs -->

This guide is meant to provide SDK maintainers with some recommended common
practices. New and existing SDK maintainers are encouraged to copy this file
to their repositories and adopt these guidelines so that contributors may
expect a common experience with each SDK.

## Tips

These tips are meant to help prevent issues and pull requests from becoming
stale and outdated.

* Stay on top of your own pull requests. PRs that languish for too long can become difficult to merge.
* Work from your own fork. As you are making contributions to the project, you should be working from your own fork just as outside contributors do. This keeps the branches in github to a minimum and reduces unnecessary CI runs.
* Proactively label issues and pull requests with relevant and descriptive labels.
* Actively review pull requests as they are submitted. A pull request should not go for more than a couple of days without a comment or review.
* Triage issues regularly.
  * If some issues are stale for too long because they are no longer valid/relevant or because the discussion reached no significant action items to perform, close the issue and invite users to reopen if they need it.
  * If some PRs are no longer valid due to conflicts, but the PR is still needed, ask the contributor to rebase their PR from the main branch.
  * If you find an issue that you want to create a pull request for, be sure to assign the issue to yourself so that other maintainers don't start working on it at the same time.
* Consider using GitHub actions to proactively label and eventually close older issues and pull requests as they become stale.

## Commit Messages

Use the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/)
when writing commit messages. This convention works nicely with [SemVer](http://semver.org/)
by describing features, fixes and breaking changes made in commit messages. By structuring
your commit messages in this way, they effectively communicate intent and effect of the
repository commits to consumers of your library.

Briefly, the structure of commit messages should be:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

When using `--signoff` on your commits, the footer will be your signoff. For example:

```
    Signed-off-by: Joe Smith <joe.smith@email.com>
```

See the Conventional Commits specification for additional details regarding the
structural details such as `type` and `scope` in your commit messages.

## Landing Pull Requests

When landing pull requests, be sure to check that the first line of the commit
uses an appropriate commit message prefix. For example if it is a documentation
change, use "docs:" as a prefix for the commit message. If there is more than
one commit, try to squash into a single commit. Usually this can just be done
with the GitHub UI when merging the PR. Use "Squash and merge". To help ensure
that everyone in the community has an opportunity to review and comment on pull
requests, it's often good to have some time after a pull request has been
submitted, and before it has landed.

Here are some guidelines around pull request approvals and timing.

* No pull request may land without passing all automated checks
* All pull requests require at least one approval from a maintainer before landing
* A pull request author may approve their own PR, but will need an additional approval to land it
* If a maintainer has submitted a pull request and it has not received approval from at least one other maintainer, it can be landed after 72 hours
* If a pull request has both approvals and requested changes, it can't be landed until those requested changes are resolved

## Branch Management

The `main` branch is the bleeding edge. New major versions of the library
are cut from this branch and tagged. If you intend to submit a pull request
you should use `main HEAD` as your starting point.

Each major release should result in a new branch and tag. For example, the
release of version 1.0.0 of the library will result in a `v1.0.0` tag on the
release commit, and a new branch `v1.x.y` for subsequent minor and patch
level releases of that major version. However, development will continue
apace on `main` for the next major version - e.g. 2.0.0. Version branches
are only created for each major version. Minor and patch level releases
are simply tagged.

