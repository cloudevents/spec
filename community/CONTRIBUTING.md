# Contributing to CloudEvents

<!-- no verify-specs -->

This page contains information about reporting issues, how to suggest changes as
well as the guidelines we follow for how our documents are formatted.

## Table of Contents

- [Contributing to CloudEvents](#contributing-to-cloudevents)
  - [Table of Contents](#table-of-contents)
  - [Reporting an Issue](#reporting-an-issue)
  - [Suggesting a Change](#suggesting-a-change)
    - [Assigning and Owning work](#assigning-and-owning-work)
    - [Sign your work](#sign-your-work)
  - [Spec Formatting Conventions](#spec-formatting-conventions)

## Reporting an Issue

To report an issue, or to suggest an idea for a change that you haven't had time
to write-up yet, open an [issue](https://github.com/cloudevents/spec/issues). It
is best to check our existing
[issues](https://github.com/cloudevents/spec/issues) first to see if a similar
one has already been opened and discussed.

## Suggesting a Change

To suggest a change to this repository, submit a
[pull request](https://github.com/cloudevents/spec/pulls)(PR) with the complete
set of changes you'd like to see. See the
[Spec Formatting Conventions](#spec-formatting-conventions) section for the
guidelines we follow for how documents are formatted.

Please use [conventional commits](https://conventionalcommits.org) when writing
commit messages.

Each PR must be signed per the following section.

### Assigning and Owning work

If you want to own and work on an issue, add a comment or “#dibs” it asking
about ownership. A maintainer will then add the Assigned label and modify the
first comment in the issue to include `Assigned to: @person`

### Sign your work

The sign-off is a simple line at the end of the explanation for the patch. Your
signature certifies that you wrote the patch or otherwise have the right to pass
it on as an open-source patch. The rules are pretty simple: if you can certify
the below (from [developercertificate.org](http://developercertificate.org/)):

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

Then you just add a line to every git commit message:

    Signed-off-by: Joe Smith <joe.smith@email.com>

Use your real name (sorry, no pseudonyms or anonymous contributions.)

If you set your `user.name` and `user.email` git configs, you can sign your
commit automatically with `git commit -s`.

Note: If your git config information is set properly then viewing the `git log`
information for your commit will look something like this:

```
Author: Joe Smith <joe.smith@email.com>
Date:   Thu Feb 2 11:41:15 2018 -0800

    Update README

    Signed-off-by: Joe Smith <joe.smith@email.com>
```

Notice the `Author` and `Signed-off-by` lines match. If they don't your PR will
be rejected by the automated DCO check.

## Spec Formatting Conventions

Documents in this repository will adhere to the following rules:

- Lines are wrapped at 80 columns (when possible)
- Specifications will use [RFC2119](https://tools.ietf.org/html/rfc2119)
  keywords to indicate normative requirements
