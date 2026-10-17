---
name: issue-process
description: Process an issue in the `issue-<n>` worktree created by `issue-start` — move the session into that worktree, start the stack, read the issue, then stop. Use in the window opened by `issue-start`, to begin the work on its issue (`/wj:issue-process 41`). GitHub (`gh`) or GitLab (`glab`), depending on `origin`.
---

# issue-process

Argument: the issue number `<n>`, an integer (`41`). Without a number, ask
for it. If the argument is not a number, ask for it.

The skill **prepares** the work, it does not do it: it drafts no plan, reads
no code and writes no line. It stops after reading the issue.

## 1. The forge

Read `git remote get-url origin` from the main repository:

- the host is `github.com` → `gh`;
- the host is a GitLab instance → `glab`. Before each `glab` command, read its
  help (`glab <command> --help`): its options are not written from memory;
- otherwise, or if the tool is not installed → say so and stop.

## 2. The worktree

The worktree is the one created by `issue-start`. Path:
`<repository>/.claude/worktrees/issue-<n>`. Branch: `issue-<n>`.

1. Check that the path is a worktree of the repository (`git worktree list`).
   If it is not: **touch nothing**, report it and ask.
2. Check that its branch is `issue-<n>` (`git -C <path> branch --show-current`).
   If it is not: **touch nothing**, report it and ask.
3. Move the session into the worktree, unless it already runs in it:
   `EnterWorktree` tool with `path` = `<path>`.

Every command that follows designates the worktree by its absolute path.

## 3. The stack

Start the stack as the documentation of the repository prescribes it
(`AGENTS.md`, `README`, `docs/`): the launch command and what it prepares
(dependencies, directories, volumes). If nothing says how, **ask**, do not
guess.

- A command that stays in the foreground (servers) is run in the background.
- Observe that it answers, at the address the documentation gives for this
  checkout: a launch that was not seen answering is not a successful launch.
  If the launch command reports by itself that the stack answers, its report
  is the observation: no other check is run. On failure, show the output and
  stop.

## 4. The issue

Read the issue with its comments (`gh issue view <n> --comments`, or the
`glab` equivalent).

## 5. End

Report, then **stop**:

- the path of the worktree and its branch;
- the address where the stack answers, and the command that observed it;
- what the issue asks for and the method it imposes, if any;
- every discrepancy observed between the issue and the repository, in one
  sentence each.

What follows — plan, implementation — waits for the user's instruction.

## 6. What follows, when the issue imposes a published plan

If the method of the issue requires a plan to be published before any change:

- the questions the reading raises — an option to decide, an unforeseen case,
  a discrepancy between the issue and the repository — are asked **in the
  conversation**, numbered, and the publication waits for the answers;
- the published plan incorporates those answers and **contains no question**,
  no option to decide, no point "to confirm";
- a permission to carry on ("carry on", "go ahead") does not cover publishing
  a plan that still contains a question: stop and ask the questions.
