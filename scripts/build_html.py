"""Render course cheatsheet markdown-like content into printable HTML.

This script is intentionally small and stdlib-only. It does not inspect course
materials, rank topics, or create reasoning artifacts. Codex/the agent should
write working/cheatsheet_content.md first, then this script renders it.
"""

from __future__ import annotations

import argparse
import html
import re
from datetime import datetime
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"
DEFAULT_SOURCE_NOTE = "Rendered from cheatsheet_content.md; verify evidence notes before printing."


COMPACT_LINE_PREFIXES = {
    "Formula": "formula",
    "Def": "definition",
    "Trap": "trap",
    "Q": "qa",
    "A": "qa",
    "Compare": "compare",
    "Procedure": "procedure",
}

GROUP_START_PREFIXES = {"Topic", "Q"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render working/cheatsheet_content.md into 3-column and 4-column "
            "A4 landscape cheatsheet HTML. This does not analyze course materials."
        )
    )
    parser.add_argument("course_name", help="Course folder name under --root.")
    parser.add_argument(
        "--root",
        default="courses",
        help="Courses root directory. Default: courses",
    )
    parser.add_argument(
        "--content",
        help="Optional path to cheatsheet_content.md. Defaults to COURSE/working/cheatsheet_content.md.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing HTML outputs without prompting. Currently outputs are always regenerated.",
    )
    return parser.parse_args()


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"\[(A|B|C|R)\]",
        lambda match: f'<span class="priority-{match.group(1).lower()}">{match.group(1)}</span>',
        escaped,
    )
    return escaped


def close_list(html_lines: list[str], in_list: bool) -> bool:
    if in_list:
        html_lines.append("</ul>")
    return False


def split_tagged_line(line: str) -> tuple[str, str, str] | None:
    for prefix, class_name in COMPACT_LINE_PREFIXES.items():
        marker = f"{prefix}:"
        if line.startswith(marker):
            return prefix, class_name, line[len(marker) :].strip()
    if line.startswith("Topic:"):
        return "Topic", "topic", line[len("Topic:") :].strip()
    return None


def render_tag(prefix: str, class_name: str, body: str) -> str:
    return (
        f'<span class="tagged {class_name}">'
        f'<strong class="tag-label">{prefix}:</strong> {inline_markup(body)}'
        "</span>"
    )


def render_paragraph(line: str) -> str:
    tagged = split_tagged_line(line)
    if tagged:
        prefix, class_name, body = tagged
        return f'<p class="compact-line">{render_tag(prefix, class_name, body)}</p>'
    return f"<p>{inline_markup(line)}</p>"


def markdown_like_to_html(content: str) -> str:
    html_lines: list[str] = []
    in_list = False
    in_table = False
    table_lines: list[str] = []
    current_group: list[str] = []

    def flush_table() -> None:
        nonlocal in_table, table_lines
        if in_table:
            html_lines.append("<pre>")
            html_lines.append(html.escape("\n".join(table_lines), quote=False))
            html_lines.append("</pre>")
            table_lines = []
            in_table = False

    def flush_group() -> None:
        nonlocal current_group
        if current_group:
            html_lines.append('<p class="topic-group">')
            html_lines.append(" ".join(current_group))
            html_lines.append("</p>")
            current_group = []

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_table()
            flush_group()
            in_list = close_list(html_lines, in_list)
            continue

        if stripped.startswith("|"):
            in_list = close_list(html_lines, in_list)
            flush_group()
            in_table = True
            table_lines.append(stripped)
            continue

        flush_table()

        if stripped.startswith("### "):
            flush_group()
            in_list = close_list(html_lines, in_list)
            html_lines.append(f"<h3>{inline_markup(stripped[4:].strip())}</h3>")
        elif stripped.startswith("## "):
            flush_group()
            in_list = close_list(html_lines, in_list)
            html_lines.append(f"<h2>{inline_markup(stripped[3:].strip())}</h2>")
        elif stripped.startswith("# "):
            flush_group()
            in_list = close_list(html_lines, in_list)
            html_lines.append(f"<h2>{inline_markup(stripped[2:].strip())}</h2>")
        elif stripped.startswith("- "):
            flush_group()
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{inline_markup(stripped[2:].strip())}</li>")
        else:
            tagged = split_tagged_line(stripped)
            if tagged:
                prefix, class_name, body = tagged
                if prefix in GROUP_START_PREFIXES:
                    flush_group()
                if current_group:
                    current_group.append(render_tag(prefix, class_name, body))
                elif prefix in GROUP_START_PREFIXES:
                    current_group.append(render_tag(prefix, class_name, body))
                else:
                    in_list = close_list(html_lines, in_list)
                    html_lines.append(render_paragraph(stripped))
            else:
                flush_group()
                in_list = close_list(html_lines, in_list)
                html_lines.append(render_paragraph(stripped))

    flush_table()
    flush_group()
    close_list(html_lines, in_list)
    return "\n".join(f"    {line}" for line in html_lines)


def remove_redundant_title(content: str, course_name: str) -> str:
    lines = content.splitlines()
    if not lines:
        return content

    first = lines[0].strip()
    normalized = re.sub(r"\s+", " ", first.lstrip("#").strip()).casefold()
    expected = f"{course_name} cheatsheet".casefold()
    if first.startswith("#") and normalized == expected:
        return "\n".join(lines[1:]).lstrip()
    return content


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    rendered = read_text(template_path)
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def main() -> int:
    args = parse_args()
    course_root = Path(args.root) / args.course_name
    content_path = (
        Path(args.content)
        if args.content
        else course_root / "working" / "cheatsheet_content.md"
    )

    if not course_root.exists():
        print(f"ERROR: Course folder not found: {course_root}")
        return 2

    if not content_path.exists():
        print(f"ERROR: Missing cheatsheet content: {content_path}")
        print(
            "Run the skill workflow first to create working/topic_map.md, "
            "working/importance_ranking.md, and working/cheatsheet_content.md."
        )
        return 2

    content_text = remove_redundant_title(read_text(content_path), args.course_name)
    content_html = markdown_like_to_html(content_text)
    output_dir = course_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    source_note = DEFAULT_SOURCE_NOTE
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    replacements = {
        "COURSE_NAME": html.escape(args.course_name, quote=False),
        "SOURCE_NOTE": html.escape(source_note, quote=False),
        "CONTENT_HTML": content_html,
        "GENERATED_AT": html.escape(generated_at, quote=False),
    }

    outputs = [
        (ASSETS / "a4-landscape-3col-template.html", output_dir / "cheatsheet_3col.html"),
        (ASSETS / "a4-landscape-4col-template.html", output_dir / "cheatsheet_4col.html"),
    ]

    for template_path, output_path in outputs:
        existed = output_path.exists()
        output_path.write_text(
            render_template(template_path, replacements),
            encoding="utf-8",
        )
        action = "Updated" if existed else "Created"
        print(f"{action} {output_path}")

    if args.force:
        print("--force supplied; outputs were regenerated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
