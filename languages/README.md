# Instructions for CloudEvents Specification in Multi-languages

<!-- no verify-specs -->

## Abstract

This page contains information about how to translate a document from scratch, 
definition of roles and responsibilities as well as guidelines that translators 
and reviewers should follow.

## Status of this document

This is a working draft. Changes could be made anytime.

## Table of Contents

- [Roles](#roles)
- [How to translate](#how-to-translate)
- [How to add a new language](#how-to-add-a-new-language)
- [Translation style guide](#translation-style-guide)

## Roles

There are two categories of roles:

1. **Translator.** This is anyone who participates in the translation of any 
   CloudEvents documents. One becomes a formal translator once a Pull Request (PR) 
   of their translation is merged.

2. **Reviewer.** A reviewer is the one who is responsible for reviewing new translations 
   and answering related issues.

### Translators

A translator can start translating by following [the translation instructions](#how-to-translate).
Translators should follow the [translation style guide](#translation-style-guide).

### Reviewers

Anyone, who builds [a new language structure](#how-to-add-a-new-language), will be the first reviewer
of that language.

Reviewers should track translation state of each document by editing 
`languages/{language-code}/translations.md` file.

There are 4 types of status:
- Ready to start: any document is ready to be translated stay in this state.
- Started: indicating someone is translating this document
- PR reviewing: a translator finished the translation, and the work is being reviewed.
- PR merged: the translation is successfully merged into the `spec` repository.

Initially, the last edit time will be the time when the translation is merged.
Reviewers should ensure translations are up-to-date with the English version as it changes, meanwhile 
update the last edit time as well. 

The following rules govern adding and removing reviewers:

- Reviewers can be proposed via a PR to edit the `languages/{language-code}/reviewer.md` file.

- Reviewers can be removed via a PR to edit the `languages/{language-code}/reviewer.md` file.

## How to add a new language 

This section is mainly for anyone who needs to build a new language structure.

Firstly, check the [language list](languages.md) to see if the language
you'd like to translate into already exists. If it doesn't exist, 
and there is not a PR indicating someone is currently working on it,
then you can start to add a new one.

### Step 1. Create a PR to edit the languages.md

Before starting to do any actual works, you should create a PR to edit the
[language list](languages.md), adding a new language item to avoid redundant works from others.

### Step 2. Build the structure locally

After you cloned the repo to your local environment, you should create a directory 
under `languages` directory, named after the specific 
[language code](http://www.lingoes.net/en/translator/langcode.htm).

Then, copy all original documents except `languages` directory to `languages/{language-code}`.

*Note*: there is no need to copy project-related files(i.e.,LICENSE, OWNERS).

For example:
```
copy cloudevents/spec.md to languages/zh-CN/cloudevents/spec.md
copy README.md to languages/zh-CN/README.md
......
```
You should also clear English content of copied documents to indicate 
that the document is ready to be translated.

The [translation list](zh-CN/translations.md)
should be copied to `languages/{language-code}`.
It lists all information(including reviewers, translators and translations) about this languages.

### Step 3. Create a new PR to upload the new structure

Once you finished build the structure locally, you can create a PR to upload the changes.

## How to translate

### Step 1. Choose a document to translate 

Admins will open issues to publish translation assignments 
once the PR of "building a new language structure" is discussed and merged.

A translator then can find a document to translate by filtering issues based on 
`{language-code}-translation` label.

You can comment in the issue to ask admins to assign the task to you.

You're expected to finish translation within one week. The task can be assigned to
others after one week.

### Step 2. Submit your translation

A translator must submit translation via a Pull Request(PR). See details in how to 
[submit a Pull Request](../community/CONTRIBUTING.md#suggesting-a-change).

### Step 3. Edit your translation

A reviewer might give their suggestions in your PR. 
Translators can discuss with the reviewer about translation details.

Remember, a translation will not be merged until reviewers give their LGTM.

## Translation style guide
- Only translate textual documents (generally Markdown files with a .md extension).
  Other document formats (.json, .yaml, .g4) will not be translated.
- Code blocks within md documents are not translated.
- Well-known technical terms ("JSON", "HTTP", "SDK", "Kafka", etc) are not translated.
- Always add a space between an English word and other language word.