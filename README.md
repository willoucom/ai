# ai

Claude Code plugin marketplace `wj-plugins`, which holds a single plugin, `wj`.

## Skills of the `wj` plugin

| Skill | What it does |
| --- | --- |
| `/wj:issue-start <n>` | Creates the `issue-<n>` worktree from the up-to-date default branch, copies the `.env` into it, opens a new VS Code window on it, and opens a Claude Code tab in that window with `/wj:issue-process <n>` pre-filled. |
| `/wj:issue-process <n>` | In the `issue-<n>` worktree: starts the stack and reads the issue. |
| `/wj:issue-finish <n>` | Waits for the CI of the PR/MR of the `issue-<n>` branch, rebase-merges it after confirmation, then removes the stack, the worktree and the branches. |
| `/wj:lint-markdown` | Lints every Markdown file of the repository against its `.markdownlint.jsonc`, and fixes what the linter reports. |

The skills are in [`plugins/wj/skills/`](plugins/wj/skills/).

## Install

```bash
claude plugin marketplace add willoucom/ai
claude plugin install wj@wj-plugins
```

The plugin is installed in the `user` scope: its skills are available in every
project of the machine.

## Update

The plugin has no `version`: every commit of this repository is a new version.

```bash
claude plugin marketplace update wj-plugins
claude plugin update wj@wj-plugins
```

The update applies at the next session, or after `/reload-plugins`.

## Check

```bash
claude plugin validate .
```
