# wj-plugins

**Claude Code plugins that keep Claude on the request, guard its shell
commands and its commits, and take an issue from creation to merge.**

**[Read the documentation](https://www.willou.com/ai/)**

## What you get

- **[wj-behavior](plugins/wj-behavior/)**: Claude does what you asked, and
  nothing more, and never credits itself in your commits.
- **[wj-guard](plugins/wj-guard/)**: Bash commands you can approve at a
  glance, one simple command at a time.
- **[wj-code-style](plugins/wj-code-style/)**: your code-style rules, from
  the first message of every session.
- **[wj](plugins/wj/)**: one issue, one worktree, one VS Code window, from
  its creation to its merge.

## Install

```bash
claude plugin marketplace add willoucom/ai
claude plugin install all@wj-plugins
```

[`all`](plugins/all/) installs every plugin. Each plugin also works on its
own: the [install page](https://www.willou.com/ai/install/) shows how to
install only the ones you want, and how to update them.

## Documentation

The site is built from [`docs/`](docs/): `gen.py` writes the page of each
plugin from its `README.md` and from the files Claude Code loads, then
Zensical builds the site. To preview it, from `docs/`:

```bash
uv sync
uv run python gen.py
uv run zensical serve
```
