#!/bin/sh
# Entry point of the hook: run the check with python3, or, when python3 is
# missing, let the command through and warn both the user and Claude that
# commit messages are not checked.
if command -v python3 >/dev/null 2>&1; then
  exec python3 "${0%/*}/check-commit.py"
fi
printf '%s\n' '{"systemMessage": "wj commit check is off: python3 is not installed, so commit messages are not checked.", "hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "wj commit check is off: python3 is not installed, so this command was not checked. A commit message credits no AI tool as an author and holds no ticket, MR/PR reference or URL."}}'
