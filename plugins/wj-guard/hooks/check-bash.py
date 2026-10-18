#!/usr/bin/env python3
"""PreToolUse hook of the Bash tool: refuse multi-line, compound, file-writing or inline-script
commands, and the forms that make Claude Code ask for a confirmation.

A refused command exits with code 2: Claude Code cancels the call and hands the
message written on stderr back to Claude, which rewrites the command.
"""
import json
import os
import re
import shlex
import sys

PUNCTUATION = "();<>|&"
HEREDOCS = {"<<", "<<-", "<<<"}
OUTPUT_REDIRECTIONS = {">", ">>", ">|", "&>", "&>>", ">&"}
WRAPPERS = {"rtk", "sudo"}
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
SED_IN_PLACE = re.compile(r"-[nrEsuz]*i|--in-place")
PERL_IN_PLACE = re.compile(r"-[aelnpsSwWX0-9]*i")
INTERPRETERS = re.compile(r"python[0-9.]*|bash|sh|zsh")
INTERPRETER_VALUE_OPTIONS = {"-o", "+o", "-O", "+O", "-W", "-X"}
INLINE_SCRIPT_OPTION = re.compile(r"-[A-Za-z]*c[A-Za-z]*")
JQ_SLICE = re.compile(r"\[[^\]]*:[^\]]*\]")


def expansions(command):
    """Return the shell expansions written outside single quotes."""
    found = set()
    quote = None
    i = 0
    while i < len(command):
        char = command[i]
        if quote == "'":
            if char == "'":
                quote = None
        elif char == "\\":
            i += 1
        elif char == "'" and quote is None:
            quote = "'"
        elif char == '"':
            quote = None if quote == '"' else '"'
        elif char == "`":
            found.add("`…`")
        elif char == "$":
            following = command[i + 1 : i + 2]
            if following == "(":
                found.add("$(…)")
            elif following == "{" or re.fullmatch(r"[A-Za-z0-9_@*#?$!-]", following):
                found.add("$VAR")
        i += 1
    return found


def is_punctuation(token):
    return all(char in PUNCTUATION for char in token)


def segments(tokens):
    """Split the tokens into simple commands, on every shell operator."""
    segment = []
    for token in tokens:
        if is_punctuation(token) and token not in OUTPUT_REDIRECTIONS | HEREDOCS and any(
            char in token for char in ";|&"
        ):
            yield segment
            segment = []
        else:
            segment.append(token)
    yield segment


def program_and_arguments(segment):
    """Return the program of a simple command, past wrappers and assignments."""
    words = list(segment)
    while words and (words[0] in WRAPPERS or ASSIGNMENT.match(words[0])):
        words.pop(0)
    return (words[0], words[1:]) if words else (None, [])


def changes_environment(segment):
    """Tell whether a simple command starts with `env` or with `VAR=value`."""
    words = list(segment)
    while words and words[0] in WRAPPERS:
        words.pop(0)
    return bool(words) and (words[0] == "env" or ASSIGNMENT.match(words[0]) is not None)


def writes_in_place(program, arguments):
    if program == "sed":
        return any(SED_IN_PLACE.match(argument) for argument in arguments)
    if program == "perl":
        return any(PERL_IN_PLACE.match(argument) for argument in arguments)
    if program in {"awk", "gawk"}:
        pairs = zip(arguments, arguments[1:])
        return any(argument in {"-iinplace", "--include=inplace"} for argument in arguments) or any(
            option in {"-i", "--include"} and value in {"inplace", "inplace.awk"} for option, value in pairs
        )
    if program == "tee":
        return any(not argument.startswith("-") and argument != "/dev/null" for argument in arguments)
    return False


def runs_inline_script(program, arguments):
    """Tell whether an interpreter runs a script given on its command line (`python3 -c`, `bash -c`)."""
    if program is None or not INTERPRETERS.fullmatch(os.path.basename(program)):
        return False
    words = iter(arguments)
    for word in words:
        if word in INTERPRETER_VALUE_OPTIONS:
            next(words, None)
        elif word == "--" or word == "-m" or not word.startswith(("-", "+")):
            return False
        elif not word.startswith("--") and INLINE_SCRIPT_OPTION.fullmatch(word):
            return True
    return False


def names_dev_null(arguments):
    """Tell whether arguments pass `/dev/null` to the program itself, not as the target of a redirection.

    `/dev/null` is outside the working directories: while `permissions.blockReadsOutsideWorkingDirectories`
    is on, Claude Code asks for a confirmation on an argument that names it, even in auto mode and
    whatever the permission rules.
    """
    previous = None
    for word in arguments:
        if previous not in OUTPUT_REDIRECTIONS | {"<"} and (
            word == "/dev/null" or (word.startswith("-") and word.endswith("/dev/null"))
        ):
            return True
        previous = word
    return False


def slices_in_jq(arguments):
    """Tell whether a `--jq`/`-q` expression of `gh` slices an array with `[m:n]`.

    Claude Code asks for a confirmation on such an expression, even in auto mode.
    """
    words = iter(arguments)
    for word in words:
        if word in {"-q", "--jq"}:
            expression = next(words, "")
        elif word.startswith("--jq="):
            expression = word[len("--jq=") :]
        elif word.startswith("-q"):
            expression = word[len("-q") :]
        else:
            continue
        if JQ_SLICE.search(expression):
            return True
    return False


def problems(command):
    found = []
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return ["command impossible to parse (unbalanced quotes?)"]

    if "\n" in command:
        found.append(
            "newline: one Bash call is one line; write a multi-line text in a file with the Write tool, "
            "and pass that file to the program (`gh pr create --body-file`, `git commit -F`, etc.)"
        )
    operators = sorted(
        {
            token
            for token in tokens
            if is_punctuation(token)
            and token not in OUTPUT_REDIRECTIONS | HEREDOCS
            and any(char in token for char in ";|&")
        }
    )
    if operators:
        found.append(
            f"operators {' '.join(operators)}: one Bash call runs one simple command; "
            "for a sequence, write a script on disk and run it with one simple command"
        )
    if any(token in HEREDOCS for token in tokens):
        found.append("heredoc: write the file with the Write tool")
    if expansions(command):
        found.append(
            f"expansions {' '.join(sorted(expansions(command)))}: write the value itself in the command, "
            "or put the logic in a script on disk"
        )
    for operator, target in zip(tokens, tokens[1:] + [""]):
        if operator in OUTPUT_REDIRECTIONS and target != "/dev/null" and not (operator == ">&" and target.isdigit()):
            found.append(f"redirection `{operator} {target}`: write the file with the Write tool")
    for segment in segments(tokens):
        if changes_environment(segment):
            found.append(
                "environment change (`env`, `VAR=value`): write a script on disk that sets it, "
                "and run that script with one simple command"
            )
        program, arguments = program_and_arguments(segment)
        if program == "cd":
            found.append("`cd`: put the absolute path in the command itself (`git -C`, etc.)")
        elif writes_in_place(program, arguments):
            found.append(f"`{program}` writes a file: change the file with the Edit or Write tool")
        elif runs_inline_script(program, arguments):
            found.append(
                f"`{program}` runs an inline script: write the script in a file with the Write tool, "
                "and run that file with one simple command"
            )
        elif program == "curl" and names_dev_null(arguments):
            found.append(
                "`curl` passes `/dev/null` as an argument, which makes Claude Code ask for a confirmation; "
                'to get only the HTTP status, use `curl -s -I -w "%{http_code}\\n" <url>`'
            )
        elif program == "gh" and slices_in_jq(arguments):
            found.append(
                "`--jq` slices with `[m:n]`, which makes Claude Code ask for a confirmation; "
                "use `limit(n; .[])` instead of `.[0:n][]`"
            )
    return found


def main():
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    found = problems(command)
    if found:
        print("Command refused, rewrite it:\n- " + "\n- ".join(found), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
