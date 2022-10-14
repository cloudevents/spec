# Link Verification

We check that the link verification works correctly

This is the reason we have a `<!-- no verify specs -->` here

## Things we check for

We are checking that all the links are referenced correctly

#### My Title

[This links to my title](#my-title)

[This links to non existing title](#non-existing)

## HTTP links

[404 link](https://google.com/non-existing-page)

[normal http link](http://github.com)

[normal https link](https://github.com)

[non existing website](http://non-existing-website.sadkjaskldjalksjd)

## Mail links

[dummy@dummy.com](mailto:dummy@dummy.com)

## Local Links to other files

[link to existing file](README.md)

[link to existing segment in a file](README.md#fake-docs)

[link to non-existing segment in a file](README.md#non-existing)

[link to non-existing file](non-existing.md)

## bookmarks

[link to existing bookmark][github]
[link to non existing bookmark][non-existing]

[github]: https://github.com/
