# wj-behavior

## The output style

The output style
[`output-styles/wj-behavior.md`](output-styles/wj-behavior.md)
sets a lean working discipline: build only what is asked, choose the simplest
solution, deliver small increments, and ask a question when the request is
ambiguous, in a form that can be answered without rereading earlier messages.
It also sets rules on acting only on instruction, stopping on an irreversible
risk, sourcing every claim, reading versions at their source, keeping
measured values out of durable deliverables, writing the documentation, never
modifying a file on the default branch (`main` or `master`) without creating
a branch first, keeping the commit history of a branch free of fixes to its
own commits, following Conventional Commits 1.0.0 in commit messages,
rebasing a branch on the default branch of `origin` before pushing a PR/MR,
switching to the branch of a PR/MR before reviewing or resuming it, and
deleting the local branch of a PR/MR the user says was merged.

It is applied whenever the plugin is enabled (`force-for-plugin: true`), in
place of the style chosen with `/output-style`. It keeps the software
engineering instructions of Claude Code (`keep-coding-instructions: true`).
It applies to the main conversation and to forks, not to the other
subagents.

## The commit hook

A `PreToolUse` hook on the Bash tool,
[`hooks/check-commit.py`](hooks/check-commit.py),
reads the message of a `git commit` (from `-m`/`--message`, from the file of
`-F`/`--file`, and from `--trailer`) and refuses the commit when the message:

- has a subject that does not follow Conventional Commits 1.0.0,
  `<type>[(scope)][!]: <description>`; any type is accepted, as the
  specification allows;
- credits an AI tool as an author: a `Co-Authored-By` line, a
  `Generated with` marker, 🤖, or a trailer that names Claude or Anthropic;
  naming Claude Code as the subject of the change is allowed;
- holds an external reference: `#123`, `!123` or a URL.

Any other command, including `git push`, goes through. A refused commit is
cancelled, and Claude receives the reasons and rewrites the message. The PR/MR
texts are not checked: the output style covers them.

The check runs with `python3`. When `python3` is not installed, the entry
point [`hooks/check-commit.sh`](hooks/check-commit.sh) lets
every command through, and warns both the user and Claude that the commit
messages are not checked.

## Turn it off

To turn off the output style and the hook, disable the plugin:
`claude plugin disable wj-behavior@wj-plugins`.
