# wj-plugins

**Claude Code plugins that keep Claude on the request, guard its shell
commands and its commits, and take an issue from creation to merge.**

```bash
claude plugin marketplace add willoucom/ai
claude plugin install wj@wj-plugins
```

## Why use them

**Claude does what you asked, and nothing more.**
The output style of [wj](plugins/wj.md) sets a lean working discipline: no
bonus feature, the simplest solution, small deliveries, a question when the
request is ambiguous, a source for every claim, and a stop before anything
irreversible.

**Commands you can approve at a glance.**
[wj](plugins/wj.md) refuses the compound, multi-line, file-writing and
inline-script Bash commands, and tells Claude how to rewrite them as one
simple command.

**A clean commit history.**
[wj](plugins/wj.md) refuses a commit whose subject does not follow
Conventional Commits, or whose message credits an AI tool as an author or
holds an external reference.

**Your code-style rules, from the first message.**
[wj](plugins/wj.md) gives Claude its code-style rules at the start of every
session, for the code it writes and the code it reviews.

**One issue, one worktree, one window.**
[wj](plugins/wj.md) drafts an issue in the template of the repository, opens
it in its own worktree and VS Code window, and merges it after your
confirmation once its CI passes.

## Get started

[Install](install.md) shows how to install the plugin and how to update it.
