# wj

## The output style

The output style
[`output-styles/wj-behavior.md`](output-styles/wj-behavior.md)
sets a lean working discipline: build only what is asked, choose the simplest
solution, deliver small increments, and ask a question when the request is
ambiguous, in a form that can be answered without rereading earlier messages.
It also sets rules on numbering every question asked to the user `Q1`, `Q2`…
from `Q1` in each response, AskUserQuestion included, and reading a bare
number in an answer as an item of the subject, on acting only on instruction,
submitting to the user the
trade-offs between two defensible principles, stopping on an irreversible
risk, sourcing every claim, reading versions at their source, keeping
measured values out of durable deliverables, writing the documentation, never
modifying a file on the default branch (`main` or `master`) without creating
a branch first, keeping the commit history of a branch free of fixes to its
own commits, following Conventional Commits 1.0.0 in commit messages,
rebasing a branch on the default branch of `origin` before pushing a PR/MR,
switching to the branch of a PR/MR before reviewing or resuming it, and
deleting the local branch of a PR/MR the user says was merged.

It is applied whenever the plugin is enabled (`force-for-plugin: true`), in
place of the style chosen with `/output-style`. It keeps the software
engineering instructions of Claude Code (`keep-coding-instructions: true`).
It applies to the main conversation and to forks, not to the other
subagents.

## The Bash hook

A `PreToolUse` hook on the Bash tool,
[`hooks/check-bash.py`](hooks/check-bash.py), refuses a command that:

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
- writes a file with `sed -i`, `perl -i`, `awk -i inplace` or `tee`;
- runs an inline script with `python -c`, `python3 -c`, `bash -c`, `sh -c` or
  `zsh -c`: the script goes in a file written with the Write tool, and that
  file is run;
- passes `/dev/null` as an argument of `curl` (`-o /dev/null`): while
  `permissions.blockReadsOutsideWorkingDirectories` is on, Claude Code asks
  for a confirmation on this path outside the working directories, even in
  auto mode; `curl -s -I -w "%{http_code}\n" <url>` gets the HTTP status
  alone;
- slices an array with `[m:n]` in the `--jq`/`-q` expression of `gh`: Claude
  Code asks for a confirmation on it, even in auto mode; `limit(n; .[])`
  replaces `.[0:n][]`.

The command is parsed like the shell does: an operator inside quotes, in a
commit message for example, is not refused. A newline is refused everywhere,
because Claude Code asks for a confirmation on a multi-line command even when
its permission rules allow it. Leading `rtk` and `sudo` are
skipped to find the program.

A refused command is cancelled, and Claude receives the reasons and how to
rewrite it.

## The commit hook

A second `PreToolUse` hook on the Bash tool,
[`hooks/check-commit.py`](hooks/check-commit.py),
reads the message of a `git commit` (from `-m`/`--message`, from the file of
`-F`/`--file`, and from `--trailer`) and refuses the commit when the message:

- has a subject that does not follow Conventional Commits 1.0.0,
  `<type>[(scope)][!]: <description>`; any type is accepted, as the
  specification allows;
- credits an AI tool as an author: a `Co-Authored-By` line, a
  `Generated with` marker, 🤖, or a trailer that names Claude or Anthropic;
  naming Claude Code as the subject of the change is allowed;
- holds an external reference: `#123`, `!123` or a URL.

Any other command, including `git push`, goes through. A refused commit is
cancelled, and Claude receives the reasons and rewrites the message. The PR/MR
texts are not checked: the output style covers them.

## Without python3

Both hooks run with `python3`. When `python3` is not installed, their entry
points [`hooks/check-bash.sh`](hooks/check-bash.sh) and
[`hooks/check-commit.sh`](hooks/check-commit.sh) let every command through,
and warn both the user and Claude that the commands and the commit messages
are not checked.

## The code-style rules

A `SessionStart` hook adds the code-style rules of
[`code-style.md`](code-style.md) to the context of Claude, at the start of a
session and after a resume, a `/clear` or a compaction. Claude applies them to
the code it writes and to the code it reviews.

## The issue skills

`/wj:issue-create` writes the issue in an issue template of the repository
or, without one, in a basic template it proposes, from
[`skills/issue-create/templates/`](skills/issue-create/templates/). A bug
issue is functional and/or technical, a feature issue is functional only.

The issue skills work with GitHub (`gh`) or GitLab (`glab`), depending on the
`origin` remote of the repository.

## Turn it off

To turn off the output style, the hooks and the skills, disable the plugin:
`claude plugin disable wj@wj-plugins`.
