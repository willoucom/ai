---
name: lint-markdown
description: Lint every Markdown file of the repository against `.markdownlint.jsonc`, fix what the linter cannot fix, and run it again until it reports nothing. Use before committing a change that touches a Markdown file.
allowed-tools:
  - Bash(npx --yes markdownlint-cli2 --fix "**/*.md" "#**/node_modules" "#**/.venv" "#.claude/worktrees")
---

# Lint the Markdown files

Lint the Markdown files of the repository, from its root, with exactly this
command, alone in its call:

```bash
npx --yes markdownlint-cli2 --fix "**/*.md" "#**/node_modules" "#**/.venv" "#.claude/worktrees"
```

The globs take every Markdown file of the tree, tracked or not, except the
dependencies under `node_modules` and `.venv`, and the worktrees under
`.claude/worktrees`: each holds a whole checkout of its own, whose work in
progress `--fix` would otherwise rewrite. A single command, rather than
`git ls-files` piped into `xargs`, is what the `allowed-tools` rule above can
approve.

`--fix` rewrites what can be fixed automatically. Whatever the command still
reports is fixed by hand, with the editing tool, and the command is run again,
until it reports nothing.
