# Links verification

We check that the link verification works correctly

This is the reason we have a `<!-- no verify specs -->` here

## Things we check for

We are checking that all the links are referenced correctly

#### My Title

[This links to my title](#my-title)

[This links to non existing title](#non-existing)

## Local Links to other files

[link to existing file](README.md)

[link to existing segment in a file](README.md#fake-docs)

[link to non-existing segment in a file](READMEmd#non-existing)

[link to non-existing file](non-existing.md)

## bookmarks

[link to existing bookmark][github]
[link to non existing bookmark][non-existing]

[github]: https://github.com/
