# wj-plugins

**Claude Code plugins that keep Claude on the request, guard its shell
commands and its commits, and take an issue from creation to merge.**

**[Read the documentation](https://www.willou.com/ai/)**

## What you get

The [wj](plugins/wj/) plugin:

- Claude does what you asked, and nothing more, and never credits itself in
  your commits.
- Bash commands you can approve at a glance, one simple command at a time.
- Your code-style rules, from the first message of every session.
- One issue, one worktree, one VS Code window, from its creation to its
  merge.

## Install

```bash
claude plugin marketplace add willoucom/ai
claude plugin install wj@wj-plugins
```

The [install page](https://www.willou.com/ai/install/) shows how to update
it.

## Documentation

The site is built from [`docs/`](docs/): `gen.py` writes the page of each
plugin from its `README.md` and from the files Claude Code loads, then
Zensical builds the site. To preview it, from `docs/`:

```bash
uv sync
uv run python gen.py
uv run zensical serve
```
