# Pull Request Guidelines

<!-- no verify-specs -->

Here you will find step by step guidance for creating, submitting and updating
a pull request for an SDK repository. We hope it will help you have an easy time
managing your work and a positive, satisfying experience when contributing
your code. Thanks for getting involved! :rocket:

* [Getting Started](#getting-started)
* [Branches](#branches)
* [Commit Messages](#commit-messages)
* [Staying current with main](#staying-current-with-main)
* [Submitting and Updating a Pull Request](#submitting-and-updating-your-pull-request)
* [Congratulations!](#congratulations)

## Getting Started

When creating a pull request, first fork the repository and clone it to your
local development environment. Then add the repository as the upstream.

```console
git clone https://github.com/mygithuborg/sdk-[lang].git
cd sdk-[lang]
git remote add upstream https://github.com/cloudevents/sdk-sdk-[lang].git
```

## Branches

The first thing you'll need to do is create a branch for your work.
If you are submitting a pull request that fixes or relates to an existing
GitHub issue, you can use this in your branch name to keep things organized.
For example, if you were to create a pull request to fix
[this error with `httpAgent`](https://github.com/cloudevents/sdk-javascript/issues/48)
you might create a branch named `48-fix-http-agent-error`.

```console
git fetch upstream
git reset --hard upstream/main
git checkout FETCH_HEAD
git checkout -b 48-fix-http-agent-error
```

## Commit Messages

Please follow the
[Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#summary).
The first line of your commit should be prefixed with a type, be a single
sentence with no period, and succinctly indicate what this commit changes.

All commit message lines should be kept to fewer than 80 characters if possible.

An example of a good commit message.

```log
docs: remove 0.1, 0.2 spec support from README
```

### Signing your commits

Each commit must be signed. Use the `--signoff` flag for your commits.

```console
git commit --signoff
```

This will add a line to every git commit message:

    Signed-off-by: Joe Smith <joe.smith@email.com>

Use your real name (sorry, no pseudonyms or anonymous contributions.)

The sign-off is a signature line at the end of your commit message. Your
signature certifies that you wrote the patch or otherwise have the right to pass
it on as open-source code. See [developercertificate.org](http://developercertificate.org/)
for the full text of the certification.

Be sure to have your `user.name` and `user.email` set in your git config.
If your git config information is set properly then viewing the `git log`
for your commit will look something like this:

```
Author: Joe Smith <joe.smith@email.com>
Date:   Thu Feb 2 11:41:15 2018 -0800

    Update README

    Signed-off-by: Joe Smith <joe.smith@email.com>
```

Notice the `Author` and `Signed-off-by` lines match. If they don't your PR will
be rejected by the automated DCO check.

## Staying Current with `main`

As you are working on your branch, changes may happen on `main`. Before
submitting your pull request, be sure that your branch has been updated
with the latest commits.

```console
git fetch upstream
git rebase upstream/main
```

This may cause conflicts if the files you are changing on your branch are
also changed on main. Error messages from `git` will indicate if conflicts
exist and what files need attention. Resolve the conflicts in each file, then
continue with the rebase with `git rebase --continue`.

If you've already pushed some changes to your `origin` fork, you'll
need to force push these changes.

```console
git push -f origin 48-fix-http-agent-error
```

## Submitting and Updating Your Pull Request

Before submitting a pull request, you should make sure that all of the tests
successfully pass.

Once you have sent your pull request, `main` may continue to evolve
before your pull request has landed. If there are any commits on `main`
that conflict with your changes, you may need to update your branch with
these changes before the pull request can land. Resolve conflicts the same
way as before.

```console
git fetch upstream
git rebase upstream/main
# fix any potential conflicts
git push -f origin 48-fix-http-agent-error
```

This will cause the pull request to be updated with your changes, and
CI will rerun.

A maintainer may ask you to make changes to your pull request. Sometimes these
changes are minor and shouldn't appear in the commit log. For example, you may
have a typo in one of your code comments that should be fixed before merge.
You can prevent this from adding noise to the commit log with an interactive
rebase. See the [git documentation](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
for details.

```console
git commit -m "fixup: fix typo"
git rebase -i upstream/main # follow git instructions
```

Once you have rebased your commits, you can force push to your fork as before.

## Congratulations!

Congratulations! You've done it! We really appreciate the time and energy
you've given to the project. Thank you.
