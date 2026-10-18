# wj-code-style

## How the rules reach Claude

A `SessionStart` hook adds the code-style rules of
[`code-style.md`](code-style.md) to the context of Claude, at the start of a
session and after a resume, a `/clear` or a compaction. Claude applies them to
the code it writes and to the code it reviews.

## Turn it off

To turn the rules off, disable the plugin:
`claude plugin disable wj-code-style@wj-plugins`.
