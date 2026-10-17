---
name: issue-finish
description: Finish work on an issue opened by `issue-start` — wait for the CI of the PR/MR of the `issue-<n>` branch, rebase-merge it after confirmation, stop the stack of the worktree, remove the worktree and the branches, update the local default branch. Use when the user asks to finish, merge or clean up an issue (`/wj:issue-finish 41`). GitHub (`gh`) or GitLab (`glab`), depending on `origin`.
---

# issue-finish

Argument: the issue number, `<n>`. Without a number, ask for it.

Everything relates to the `issue-<n>` branch and to the
`<repository>/.claude/worktrees/issue-<n>` worktree created by `issue-start`.

## 1. The forge

As in `issue-process`: `github.com` → `gh`, a GitLab instance → `glab`, whose
help (`glab <command> --help`) is read before each command. Otherwise, say so
and stop.

## 2. The PR/MR

Find the one whose source branch is `issue-<n>`
(`gh pr list --head issue-<n> --state open`, or the `glab` equivalent). None,
or several → say so and ask.

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

In this order, the worktree designated by its absolute path:

1. **The stack**: stop it and remove what belongs to the project of the
   worktree, as the documentation of the repository prescribes. A volume or a
   resource the documentation says is shared between checkouts (external
   cache…) **is not removed**. If the documentation does not say how to stop
   the stack, ask.
2. **The worktree**: first bring the session back to the main repository
   (`ExitWorktree` tool with `action: "keep"`; without an active worktree
   session, it does nothing), since the directory the session is in cannot be
   removed. Then `git worktree remove <path>`. If it refuses (modified or
   untracked files), show what remains and ask: no `--force` without
   agreement.
3. **The local branch**: `git branch -D issue-<n>` — after a rebase merge the
   SHAs differ, and `-d` normally refuses.
4. **The remote branch**: if `git ls-remote --heads origin issue-<n>` still
   finds it, report it and ask before removing it.

## 6. The local default branch

In the main repository, if it is on the default branch and clean:
`git pull --rebase`. Otherwise, say so, and touch nothing.

## 7. End

Report, each point with the command that observed it:

- the merged state of the PR/MR and its commit;
- the absence of the worktree (`git worktree list`), of the containers and
  volumes of the project, of the local and remote `issue-<n>` branches;
- the presence of the shared resources preserved;
- the commit the local default branch is on.

The other worktrees present are reported in one sentence, without touching
them.
