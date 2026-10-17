---
name: issue-start
description: Prepare an issue in a new VS Code window — create the `issue-<n>` worktree from the up-to-date default branch, copy the `.env` into it, open a new VS Code window on it, and open a Claude Code tab in that window with `/wj:issue-process <n>` pre-filled, then stop. Use when the user gives an issue number to work on ("let's take issue 41", `/wj:issue-start 41`).
---

# issue-start

Argument: the issue number, `<n>`. Without a number, ask for it.

The skill opens the window of the issue, it does not work on it: the current
session stays where it is, and reads neither the issue nor the code. The work
begins with `/wj:issue-process`, in the window it opens.

## 1. The worktree

- `git fetch origin`, then find the default branch (`git symbolic-ref
  refs/remotes/origin/HEAD`).
- Path: `<repository>/.claude/worktrees/issue-<n>`. Branch: `issue-<n>`.
- If that path or that branch already exists, locally or on `origin`:
  **touch nothing**, report it and ask.
- `git worktree add -b issue-<n> <path> origin/<default branch>`.

The worktree is created by `git worktree add` and not by `EnterWorktree`, to
keep the `issue-<n>` branch name that `issue-finish` depends on, and because
the current session does not move into it.

## 2. The `.env`

If a `.env` exists at the root of the main repository:

- check that it is ignored in the worktree
  (`git -C <path> check-ignore -q .env`);
- ignored → copy it to the root of the worktree;
- **not ignored → do not copy it**: it would leave with the next `git add`.
  Report it and ask.

Never display its content.

## 3. The VS Code window

```bash
code --new-window <path>
```

## 4. The Claude Code tab

Open the URI of the Claude Code extension,
`vscode://anthropic.claude-code/open?prompt=%2Fwj%3Aissue-process%20<n>`. It
opens a Claude Code tab in the VS Code window that has the focus, which is the
window opened at step 3, with `/wj:issue-process <n>` pre-filled in its input:
the `prompt` parameter fills the input, it does not send it.

- Under WSL:
  `powershell.exe -NoProfile -Command "Start-Process 'vscode://anthropic.claude-code/open?prompt=%2Fwj%3Aissue-process%20<n>'"`.
- On Linux: `xdg-open "vscode://anthropic.claude-code/open?prompt=%2Fwj%3Aissue-process%20<n>"`.
- On macOS: `open "vscode://anthropic.claude-code/open?prompt=%2Fwj%3Aissue-process%20<n>"`.

## 5. End

Report, then **stop**:

- the path of the worktree and its branch;
- whether the `.env` was copied;
- the commands that opened the window and the tab.
