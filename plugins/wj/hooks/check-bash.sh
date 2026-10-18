#!/bin/sh
# Entry point of the hook: run the check with python3, or, when python3 is
# missing, let the command through and warn both the user and Claude that the
# guard is off.
if command -v python3 >/dev/null 2>&1; then
  exec python3 "${0%/*}/check-bash.py"
fi
printf '%s\n' '{"systemMessage": "wj Bash check is off: python3 is not installed, so Bash commands are not checked.", "hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "wj Bash check is off: python3 is not installed, so this Bash command was not checked. Keep to one simple command per call, without file writes."}}'
