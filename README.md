# ai

Claude Code plugin marketplace `wj-plugins`, which holds two plugins, `wj` and
`wj-guard`.

## Skills of the `wj` plugin

- `/wj:issue-create [<description>]`: drafts an issue from the description,
  or from the conversation, in the language of the existing issues and in an
  issue template of the repository (or, without one, in a basic template it
  proposes, from
  [`issue-create/templates/`](plugins/wj/skills/issue-create/templates/)),
  proposes its labels, and creates it after
  agreement. A bug issue is functional and/or technical, a feature issue is
  functional only.
- `/wj:issue-start <n>`: checks that the issue exists, creates the
  `issue-<n>` worktree from the up-to-date default branch, copies the `.env`
  into it, opens a new VS Code window on it, and opens a Claude Code tab in
  that window with `/wj:issue-process <n>` pre-filled.
- `/wj:issue-process <n>`: in the `issue-<n>` worktree, starts the stack and
  reads the issue.
- `/wj:issue-finish <n>`: waits for the CI of the PR/MR of the `issue-<n>`
  branch, rebase-merges it after confirmation, then removes the stack, the
  worktree and the branches.
- `/wj:lint-markdown`: lints every Markdown file of the repository against its
  `.markdownlint.jsonc`, and fixes what the linter reports.

The skills are in [`plugins/wj/skills/`](plugins/wj/skills/).

## Hook of the `wj-guard` plugin

A `PreToolUse` hook on the Bash tool,
[`plugins/wj-guard/hooks/check-bash.py`](plugins/wj-guard/hooks/check-bash.py),
refuses a command that:

- spans several lines, even inside quotes: a multi-line text, such as the
  body of a PR or of a commit, goes in a file written with the Write tool, and
  the file is passed to the program (`gh pr create --body-file`,
  `git commit -F`);
- chains several commands: `&&`, `||`, `;`, `|`, `|&`, `&`;
- holds a heredoc: `<<`, `<<-`, `<<<`;
- expands something outside single quotes: `$(…)`, `` `…` ``, `$VAR`,
  `${VAR}`;
- redirects an output to a file: `>`, `>>`, `>|`, `&>`, `&>>`, `>& file`
  (`/dev/null` and `2>&1` are allowed);
- runs `cd`;
- changes the environment of a command: `env`, `VAR=value`;
- writes a file with `sed -i`, `perl -i`, `awk -i inplace` or `tee`.

The command is parsed like the shell does: an operator inside quotes, in a
commit message for example, is not refused. A newline is refused everywhere,
because Claude Code asks for a confirmation on a multi-line command even when
its permission rules allow it. Leading `rtk` and `sudo` are
skipped to find the program.

A refused command is cancelled, and Claude receives the reasons and how to
rewrite it. To turn the hook off, disable the plugin:
`claude plugin disable wj-guard@wj-plugins`.

The check runs with `python3`. When `python3` is not installed, the
entry point [`check-bash.sh`](plugins/wj-guard/hooks/check-bash.sh) lets every
command through, and warns both the user and Claude that the commands are not
checked.

## Install

```bash
claude plugin marketplace add willoucom/ai
claude plugin install wj@wj-plugins
claude plugin install wj-guard@wj-plugins
```

The plugins are installed in the `user` scope: their skills and hooks apply to
every project of the machine.

## Update

The plugins have no `version`: every commit of this repository is a new
version.

```bash
claude plugin marketplace update wj-plugins
claude plugin update wj@wj-plugins
claude plugin update wj-guard@wj-plugins
```

The update applies at the next session, or after `/reload-plugins`.

## Check

```bash
claude plugin validate .
```
