# Code style

Apply these rules to the code you write and to the code you review.

## Exceptions: propagation is never implicit

- Every exception that crosses a function or a method crosses it
  explicitly. A block that catches an exception to rethrow it unchanged is
  **not** a no-op to remove: it is the intended form. It shows, at the call
  site, which type of exception crosses the method, and it stops a type from
  starting to rise silently when the called code changes.
- Never suggest removing a catch-and-rethrow on the ground that the
  propagation would be the same without it, neither in a code review nor in
  code you write. A documentation annotation (`@throws`, `:raises:`,
  `# Errors`, a declarative `throws`) does not replace the block: depending on
  the language, it is not checked, or only at compile time.
