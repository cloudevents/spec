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
- [How to publish translation tasks](#how-to-publish-translation-tasks)  
- [Translation style guide](#translation-style-guide)

## Roles

There are two categories of roles:

1. **Translator.** This is anyone who participates in the translation of any 
   CloudEvents documents. One becomes a formal translator once a Pull Request (PR) 
   of their translation is merged.

2. **Reviewer.** A reviewer is responsible for checking new translations 
   and answering related issues.
   Typically, reviewers of each language are members of a Github team which is named 
   after the language code(i.e., zh-CN reviewers).

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
- PR merged: the translation is successfully merged into the spec.

Initially, the last edit time will be the time when the translation is merged.
Reviewers should ensure translations are up-to-date with the English version as it changes, meanwhile 
update the last edit time as well. 

The following rules govern adding and removing reviewers:

- Reviewers can be proposed via a PR to edit the `languages/{language-code}/reviewer.md` file.

- Reviewers can be removed via a PR to edit the `languages/{language-code}/reviewer.md` file.

## How to add a new language 

This section is mainly for anyone who needs to build a new language structure.

Fork [cloudevents/spec](https://github.com/cloudevents/spec/tree/main)
to your Github repo. 

Then check the [language list](languages.md) to see if the language
you'd like to translate into already exists. If it doesn't exist, you can start to add a new one.

### Step 1. build the structure

Create a directory under `languages` directory, named after the specific 
[language code](http://www.lingoes.net/en/translator/langcode.htm).

Add a new item to the [language list](languages.md), which linking to the directory 
you just created. 

### Step 2. copy documents to right location

Copy all original documents except `languages` directory to `languages/{language-code}`.
There is no need to copy project-related files(i.e.,LICENSE, OWNERS).

For example:
```
copy cloudevents/spec.md to languages/zh-CN/cloudevents/spec.md
copy README.md to languages/zh-CN/README.md
```

Clear content of copied documents to indicate that the document is ready to be translated.

Then copy the [reviewer list](zh-CN/reviewers.md) and the [translation list](zh-CN/translations.md)
to `languages/{language-code}`.

Check example structure [here](zh-CN).

## How to publish translation tasks

### Step 1. open a single issue referring to an untranslated document

Create an issue with label "{language-code}-translation" to publish a translation assignment.

Examples:
```
Issue tile:        docs: translate cloudevents/spec.md to zh-CN
Issue content:   
                   original document: 
                   https://github.com/cloudevents/spec/blob/main/README.md
                   target document: 
                   https://github.com/cloudevents/spec/blob/main/languages/zh-CN/README.md
```

A reviewer can assign the issue to anyone who comments to do the translation.

### Step 2. open an overall issue to list and track all tasks

Examples:
```
Issue tile:         docs: translation list to zh-CN
Issue content:   
                    cloudevents: 
                    Issue url: docs: translate cloudevents/spec.md to zh-CN
                    Issue url: docs: translate cloudevents/SDK.md to zh-CN
                    Issue url: docs: translate cloudevents/primer.md to zh-CN
     
                    cesql: 
                    Issue url: docs: translate cesql/spec.md to zh-CN
                    Issue url: docs: translate cesql/cesql_tck/README.md to zh-CN
                    ......
```

## How to translate

### Step 1. Choose a document to translate 

A translator can find a document to translate by filtering issues based on 
`{language-code}-translation` label.

Comment the issue to ask reviewers to assign the task to you.

You're expected to finish translation within one week. The task can be assigned to
others after one week.

### Step 2. submit your translation

A translator must submit translation via a Pull Request(PR). See details in how to 
[submit a Pull Request](../community/CONTRIBUTING.md#suggesting-a-change).

### Step 3. edit your translation

A reviewer might give their suggestions in your PR. 
Translators can discuss with the reviewer about translation details.

However, a translation will not be merged until reviewers give their LGTM.

## Translation style guide
- Only translate textual documents (generally Markdown files with a .md extension).
  Other document formats (.json, .yaml, .g4) will not be translated.
- Code blocks within md documents are not translated.
- Well-known technical terms ("JSON", "HTTP", "SDK", "Kafka", etc) are not translated.
- Always add a space between an English word and other language word.