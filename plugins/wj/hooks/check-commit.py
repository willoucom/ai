#!/usr/bin/env python3
"""PreToolUse hook of the Bash tool: refuse a `git commit` whose subject does not follow
Conventional Commits 1.0.0, or whose message credits an AI tool as an author or holds an external
reference.

The message is read from `-m`/`--message`, from the file of `-F`/`--file`, and from `--trailer`.
A refused command exits with code 2: Claude Code cancels the call and hands the message written
on stderr back to Claude, which rewrites the commit message.
"""
import json
import os
import re
import shlex
import sys

PUNCTUATION = "();<>|&"
REDIRECTIONS_AND_HEREDOCS = {">", ">>", ">|", "&>", "&>>", ">&", "<<", "<<-", "<<<"}
WRAPPERS = {"rtk", "sudo"}
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
GIT_VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"}
COMMIT_VALUE_OPTIONS = {
    "--message",
    "--file",
    "--trailer",
    "--author",
    "--date",
    "--template",
    "--reuse-message",
    "--reedit-message",
    "--fixup",
    "--squash",
    "--cleanup",
    "--pathspec-from-file",
}
COMMIT_SHORT_VALUE_OPTIONS = "mFctC"
COMMIT_SHORT_OPTIONAL_VALUE_OPTIONS = "Su"
CO_AUTHOR = re.compile(r"^[ \t]*co-authored-by[ \t]*:.*$", re.IGNORECASE | re.MULTILINE)
MARKERS = re.compile(r"generated with|🤖", re.IGNORECASE)
TRAILER = re.compile(r"^[A-Za-z0-9-]+\s*:\s")
AI_NAME = re.compile(r"\b(claude|anthropic)\b", re.IGNORECASE)
EXTERNAL_REFERENCES = re.compile(r"(?<![\w&])#\d+\b|(?<!\w)!\d+\b|https?://[^\s)>\]]+")
CONVENTIONAL_SUBJECT = re.compile(r"[A-Za-z]+(\([^()]+\))?!?: \S")


def is_punctuation(token):
    return all(char in PUNCTUATION for char in token)


def segments(tokens):
    """Split the tokens into simple commands, on every shell operator."""
    segment = []
    for token in tokens:
        if is_punctuation(token) and token not in REDIRECTIONS_AND_HEREDOCS and any(char in token for char in ";|&"):
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


def commit_arguments(arguments, cwd):
    """Return the arguments of `git … commit` and the directory git runs in, or None for another subcommand."""
    directory = cwd
    words = iter(arguments)
    for word in words:
        if word in GIT_VALUE_OPTIONS:
            value = next(words, "")
            if word == "-C":
                directory = os.path.join(directory, value)
        elif not word.startswith("-"):
            return (list(words), directory) if word == "commit" else None
    return None


def message_parts(arguments, directory):
    """Return the message texts, the message files and the trailers given to `git commit`."""
    texts, trailers = [], []
    words = iter(arguments)
    for word in words:
        if word == "--":
            break
        if word.startswith("--"):
            name, separator, value = word.partition("=")
            if name not in COMMIT_VALUE_OPTIONS:
                continue
            if not separator:
                value = next(words, "")
        elif word.startswith("-") and len(word) > 1:
            name, value = None, None
            for position, char in enumerate(word[1:], start=1):
                if char in COMMIT_SHORT_OPTIONAL_VALUE_OPTIONS:
                    break
                if char in COMMIT_SHORT_VALUE_OPTIONS:
                    name, value = "-" + char, word[position + 1 :] or next(words, "")
                    break
            if name is None:
                continue
        else:
            continue
        if name in {"--message", "-m"}:
            texts.append(value)
        elif name in {"--file", "-F"} and value != "-":
            try:
                with open(os.path.join(directory, value), encoding="utf-8", errors="replace") as file:
                    texts.append(file.read())
            except OSError:
                pass
        elif name == "--trailer":
            trailers.append(value)
    return "\n\n".join(texts), trailers


def trailer_block(message):
    """Return the lines of the last paragraph of the message when they are all trailers."""
    paragraphs = [paragraph for paragraph in re.split(r"\n\s*\n", message.strip()) if paragraph.strip()]
    if len(paragraphs) < 2:
        return []
    lines = [line for line in paragraphs[-1].splitlines() if line.strip()]
    return lines if all(TRAILER.match(line) for line in lines) else []


def problems(message, trailers):
    found = []
    subject = message.strip().splitlines()[0] if message.strip() else ""
    if subject and not CONVENTIONAL_SUBJECT.match(subject):
        found.append(
            f"subject `{subject}`: a commit message follows Conventional Commits 1.0.0, "
            "with a subject `<type>[(scope)][!]: <description>`"
        )
    attributions = CO_AUTHOR.findall(message) + MARKERS.findall(message)
    attributions += [line for line in trailer_block(message) + trailers if AI_NAME.search(line) or CO_AUTHOR.match(line)]
    for attribution in dict.fromkeys(attribution.strip() for attribution in attributions):
        found.append(
            f"attribution `{attribution}`: a commit message credits no AI tool as an author, "
            "with no Co-Authored-By line, no `Generated with` marker, no 🤖 and no trailer naming Claude or Anthropic"
        )
    for reference in dict.fromkeys(EXTERNAL_REFERENCES.findall(message)):
        found.append(
            f"external reference `{reference}`: a commit message holds no ticket, MR/PR reference or URL; "
            "it goes in the description of the PR/MR"
        )
    return found


def main():
    hook_input = json.load(sys.stdin)
    command = hook_input.get("tool_input", {}).get("command", "")
    cwd = hook_input.get("cwd") or os.getcwd()
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return
    found = []
    for segment in segments(tokens):
        program, arguments = program_and_arguments(segment)
        if program is None or os.path.basename(program) != "git":
            continue
        commit = commit_arguments(arguments, cwd)
        if commit is not None:
            found += problems(*message_parts(*commit))
    if found:
        print("Commit refused, rewrite its message:\n- " + "\n- ".join(found), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
