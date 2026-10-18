# wj-guard

## What the hook refuses

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

## Without python3

The check runs with `python3`. When `python3` is not installed, the
entry point [`hooks/check-bash.sh`](hooks/check-bash.sh) lets every
command through, and warns both the user and Claude that the commands are not
checked.

## Turn it off

Disable the plugin: `claude plugin disable wj-guard@wj-plugins`.
