"""Write the page of every plugin of the marketplace into pages/plugins/.

Each page joins the README.md of the plugin, written by hand, to a reference
read from the files Claude Code loads: plugin.json and the plugins it
depends on, the SKILL.md of each
skill, hooks.json, the output styles and the other Markdown files at the root
of the plugin. git ignores pages/plugins/: the build rewrites it from the
plugins every time, so the reference never describes a former state of them.
"""

import json
import posixpath
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "pages" / "plugins"
SOURCE_URL = "https://github.com/willoucom/ai/blob/main"

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
# Only the single-line fields at the top level: the skills and output styles
# need nothing else, and the standard library has no YAML parser.
FIELD = re.compile(r"^([A-Za-z][\w-]*): (.+)$", re.MULTILINE)
RELATIVE_LINK = re.compile(r"\]\((?!https?://|#)([^)]+)\)")
HEADING = re.compile(r"^#+ ")
FENCE = re.compile(r"^(```|~~~)")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        raise


def split_frontmatter(text: str, path: Path) -> tuple[dict[str, str], str]:
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError(f"{path} has no frontmatter")
    return dict(FIELD.findall(match.group(1))), text[match.end():]


def demote(markdown: str, levels: int) -> str:
    """Push every heading outside a code block down by `levels`."""
    lines = []
    in_fence = False
    for line in markdown.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence and HEADING.match(line):
            line = "#" * levels + line
        lines.append(line)
    return "\n".join(lines)


def link_to_source(markdown: str, path: Path) -> str:
    """Point the relative links of the file at `path` to its repository.

    They lead to files of the plugins, which the site does not hold.
    """
    base = path.parent.relative_to(ROOT).as_posix()

    def absolute(match: re.Match[str]) -> str:
        target = posixpath.normpath(posixpath.join(base, match.group(1)))
        return f"]({SOURCE_URL}/{target})"

    return RELATIVE_LINK.sub(absolute, markdown)


def strip_title(markdown: str) -> str:
    lines = markdown.lstrip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def included(path: Path, levels: int) -> str:
    try:
        return demote(link_to_source(read_text(path), path), levels).strip()
    except OSError:
        raise


def skills_section(plugin: str, source: Path) -> list[str]:
    paths = sorted(source.glob("skills/*/SKILL.md"))
    if not paths:
        return []
    section = ["## Skills"]
    for path in paths:
        try:
            meta, _ = split_frontmatter(read_text(path), path)
        except (OSError, ValueError):
            raise
        url = f"{SOURCE_URL}/{path.parent.relative_to(ROOT).as_posix()}"
        section += [
            f"### `/{plugin}:{meta['name']}`",
            meta["description"],
            f"[Source]({url})",
        ]
    return section


def dependencies_section(manifest: dict) -> list[str]:
    names = manifest.get("dependencies", [])
    if not names:
        return []
    items = [f"- [{name}]({name}.md)" for name in names]
    return ["## Installs", "\n".join(items)]


def hooks_section(source: Path) -> list[str]:
    path = source / "hooks" / "hooks.json"
    if not path.exists():
        return []
    try:
        hooks = json.loads(read_text(path))["hooks"]
    except (OSError, ValueError):
        raise
    rows = ["| Event | Matcher | Command |", "| --- | --- | --- |"]
    for event, groups in hooks.items():
        for group in groups:
            matcher = f"`{group['matcher']}`" if "matcher" in group else "every"
            for hook in group["hooks"]:
                rows.append(f"| `{event}` | {matcher} | `{hook['command']}` |")
    return ["## Hooks", "\n".join(rows)]


def output_styles_section(source: Path) -> list[str]:
    section = []
    for path in sorted(source.glob("output-styles/*.md")):
        try:
            meta, body = split_frontmatter(read_text(path), path)
        except (OSError, ValueError):
            raise
        section += [
            f"## Output style `{meta['name']}`",
            meta["description"],
            demote(link_to_source(body, path), 2).strip(),
        ]
    return section


def other_files_section(source: Path) -> list[str]:
    section = []
    for path in sorted(source.glob("*.md")):
        if path.name == "README.md":
            continue
        try:
            section.append(included(path, 1))
        except OSError:
            raise
    return section


def plugin_page(manifest: dict, source: Path) -> str:
    plugin = manifest["name"]
    page = [f"# {plugin}", manifest["description"]]
    readme = source / "README.md"
    try:
        if readme.exists():
            page.append(strip_title(included(readme, 0)))
        page += dependencies_section(manifest)
        page += skills_section(plugin, source)
        page += hooks_section(source)
        page += output_styles_section(source)
        page += other_files_section(source)
    except (OSError, ValueError):
        raise
    return "\n\n".join(page) + "\n"


def main() -> None:
    try:
        marketplace = json.loads(read_text(ROOT / ".claude-plugin" / "marketplace.json"))
        shutil.rmtree(OUT, ignore_errors=True)
        OUT.mkdir(parents=True)
        rows = ["| Plugin | What it does |", "| --- | --- |"]
        for entry in marketplace["plugins"]:
            source = ROOT / entry["source"]
            manifest = json.loads(read_text(source / ".claude-plugin" / "plugin.json"))
            name = manifest["name"]
            (OUT / f"{name}.md").write_text(plugin_page(manifest, source), encoding="utf-8")
            rows.append(f"| [{name}]({name}.md) | {manifest['description']} |")
        index = "# Plugins\n\n" + "\n".join(rows) + "\n"
        (OUT / "index.md").write_text(index, encoding="utf-8")
    except (OSError, ValueError):
        raise


if __name__ == "__main__":
    main()
