---
name: issue-finish
description: Finish work on an issue opened by `issue-start` — wait for the CI of the PR/MR of the `issue-<n>` branch, rebase-merge it after confirmation, stop the stack of the worktree, remove the worktree and the branches, update the local default branch. Use when the user asks to finish, merge or clean up an issue (`/wj:issue-finish`, the number taken from the `issue-<n>` worktree the session is in, or `/wj:issue-finish 41`). GitHub (`gh`) or GitLab (`glab`), depending on `origin`.
---

# issue-finish

Optional argument: the number of the issue to finish (e.g. `41`), written
`<n>` below. Without a number, take `<n>` from the name of the current
directory, a `<repository>/.claude/worktrees/issue-<n>` worktree, and state
it. If the current directory is not such a worktree, say so and stop.

Everything relates to the `issue-<n>` branch and to the
`<repository>/.claude/worktrees/issue-<n>` worktree created by `issue-start`.

## 1. The forge

As in `issue-process`: `github.com` → `gh`, a GitLab instance → `glab`, whose
help (`glab <command> --help`) is read before each command. Otherwise, say so
and stop.

## 2. The PR/MR

Find the one whose source branch is `issue-<n>`
(`gh pr list --head issue-<n> --state open`, or the `glab` equivalent).

- None → say so and ask for the correct issue number.
- Several → list them and ask which one.

## 3. The CI

Follow the CI to its end (`gh pr checks <pr> --watch --fail-fast`, or the
`glab` equivalent).

- A failed job → **stop**: name it, with the link to its run. Fix nothing.
- Everything green → report each job and its state, skipped jobs included.

## 4. The merge — after confirmation

CI green, **ask for confirmation** before merging, recalling what a push to
the default branch triggers according to the CI of the repository
(publication, deployment…). No merge without that agreement, even if the user
launched the skill.

- Merge **with a rebase** (`gh pr merge <pr> --rebase`, or the `glab`
  equivalent). If the forge refuses the rebase, say so and stop: do not
  change method.
- Check the merged state (`gh pr view <pr> --json state,mergedAt`).

## 5. The cleanup

In this order, the worktree designated by its absolute path. A step that asks
waits for the answer before the next one.

1. **Stop the stack** of the worktree, as the documentation of the repository
   prescribes, and remove what belongs to its project.
   - The documentation does not say how to stop it → ask.
   - A volume or a resource the documentation says is shared between
     checkouts (external cache…) → **keep it**.
2. **Leave the worktree**: bring the session back to the main repository with
   the `ExitWorktree` tool, `action: "keep"` — the directory the session is in
   cannot be removed. Without an active worktree session, it does nothing.
3. **Remove the worktree**: `git worktree remove <path>`.
   - It refuses (modified or untracked files) → show what remains and ask. No
     `--force` without agreement.
4. **Remove the local branch**: `git branch -D issue-<n>` — after a rebase
   merge the SHAs differ, and `-d` normally refuses.
5. **Check the remote branch**: `git ls-remote --heads origin issue-<n>`.
   - It still finds it → report it and ask before removing it.
   - It finds nothing → nothing to do.

## 6. The local default branch

In the main repository, if it is on the default branch and clean:
`git pull --rebase`. Otherwise, say so, and touch nothing.

## 7. End

Report, each point with the command that observed it:

- the state of the PR/MR (`state`, `mergedAt` read at the end of section 4),
  and the head commit of the default branch after the merge;
- the absence of the worktree (`git worktree list`), of the containers and
  volumes of the project, of the local and remote `issue-<n>` branches;
- the presence of the shared resources preserved;
- the commit the local default branch is on.

The other worktrees present are reported in one sentence, without touching
them.
