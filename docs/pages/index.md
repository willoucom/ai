# wj-plugins

**Claude Code plugins that keep Claude on the request, guard its shell
commands and its commits, and take an issue from creation to merge.**

```bash
claude plugin marketplace add willoucom/ai
claude plugin install all@wj-plugins
```

## Why use them

**Claude does what you asked, and nothing more.**
[wj-behavior](plugins/wj-behavior.md) sets a lean working discipline: no
bonus feature, the simplest solution, small deliveries, a question when the
request is ambiguous, a source for every claim, and a stop before anything
irreversible.

**Commands you can approve at a glance.**
[wj-guard](plugins/wj-guard.md) refuses the compound, multi-line,
file-writing and inline-script Bash commands, and tells Claude how to rewrite
them as one simple command.

**A clean commit history.**
[wj-behavior](plugins/wj-behavior.md) refuses a commit whose subject does not
follow Conventional Commits, or whose message credits an AI tool as an author
or holds an external reference.

**Your code-style rules, from the first message.**
[wj-code-style](plugins/wj-code-style.md) gives Claude its code-style rules at
the start of every session, for the code it writes and the code it reviews.

**One issue, one worktree, one window.**
[wj](plugins/wj.md) drafts an issue in the template of the repository, opens
it in its own worktree and VS Code window, and merges it after your
confirmation once its CI passes.

## Get started

[all](plugins/all.md) installs every plugin. Each plugin also works on its
own: [Install](install.md) shows how to install only the ones you want, and
how to update them.
