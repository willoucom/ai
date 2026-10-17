---
name: issue-create
description: Create an issue on the forge of the repository — draft its title and body from the given description (or the conversation) in the language of the existing issues and in the issue template of the repository, propose its labels, show the draft, create it after agreement, then stop. Use when the user asks to create, open or write an issue (`/wj:issue-create`, `/wj:issue-create <description>`). GitHub (`gh`) or GitLab (`glab`), depending on `origin`.
---

# issue-create

Optional argument: a description of the issue, in free text. Without an
argument, take the description from the conversation. If neither gives one,
ask for it.

The skill writes the issue, it does not work on it: it reads no code and
writes no line. It stops after creating the issue.

## 1. The forge

As in `issue-process`: `github.com` → `gh`, a GitLab instance → `glab`, whose
help (`glab <command> --help`) is read before each command. Otherwise, say so
and stop.

## 2. The type

An issue is either a **bug** or a **feature**. Deduce the type from the
description; if it does not settle it, ask.

- A **bug** is functional and/or technical: the observed behaviour, the
  expected one, and, when the description gives them, the technical facts
  (error, log, component).
- A **feature** is **functional only**: what the user must be able to do and
  the expected result. No implementation, no technical choice, no file, class
  or table name.

## 3. The template

The issue is written **in a template of the repository**, which is mandatory:

- GitHub: `.github/ISSUE_TEMPLATE/` (Markdown templates or `.yml` forms),
  or `.github/ISSUE_TEMPLATE.md`;
- GitLab: `.gitlab/issue_templates/`.

Choose the template that matches the type of section 2. Several match, or
none clearly does → list them and ask.

The repository has no template → say so, and propose the basic template of
the type, from the `templates/` directory of this skill: `bug.md` or
`feature.md`. Its headings are written in the language of section 4. The
draft is written in it only after agreement.

Follow the template exactly: its sections, in its order, with its headings.
A `.yml` form is rendered as one `### <label>` heading per field, in the
order of the form. Labels, assignees or a title prefix the template imposes
are kept.

## 4. The language

Write in the language of the existing issues of the repository: read the last
ones (`gh issue list --state all --limit 20`, or the `glab` equivalent). The
repository has no issue → ask.

## 5. The draft

- **Title**: short, it states what must be done.
- **Body**: the template filled from the description. It describes **what
  must be done**, and nothing of what is not done: no discarded option, no
  rejected alternative, no assumed limitation, no justification of a
  non-choice. A section of the template the description does not fill is
  asked about, not invented.
- **Labels**: proposed among the labels of the repository (`gh label list`,
  or the `glab` equivalent), with those of the template. No label is created.

Show the title, the body and the labels, then **wait for agreement**. A
change asked for → show the whole draft again, and wait again. No creation
without agreement on the last draft shown.

## 6. The creation

Write the body to a file in the scratchpad directory with the Write tool,
then create the issue from that file (`gh issue create --title <title>
--body-file <file> --label <label>`, or the `glab` equivalent).

## 7. End

Report the number and the link of the created issue, then **stop**.
