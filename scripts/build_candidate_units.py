"""Build deterministic candidate units from extracted course Markdown.

This script is intentionally coarse and stdlib-only. It chunks already
extracted Markdown into traceable units for Codex/the agent to refine into
semantic knowledge units. It does not rank topics, infer exam importance, or
merge concepts semantically.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MAX_CHARS = 2800
DEFAULT_MIN_CHARS = 900
DEFAULT_MAX_LOCATORS = 4
EXCERPT_CHARS = 900
MAX_KEYWORDS = 12
MAX_SIGNAL_LINES = 6

STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "are",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "can",
    "could",
    "does",
    "each",
    "from",
    "has",
    "have",
    "into",
    "its",
    "may",
    "more",
    "most",
    "not",
    "only",
    "other",
    "our",
    "out",
    "over",
    "page",
    "pages",
    "same",
    "should",
    "such",
    "than",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "this",
    "through",
    "use",
    "used",
    "using",
    "was",
    "were",
    "when",
    "where",
    "which",
    "with",
    "would",
}

LOCATOR_RE = re.compile(r"^##\s+(Page|Slide|Chunk)\s+(\d+)\s*$", re.MULTILINE)
MARKDOWN_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FRONT_MATTER_BOUNDARY = "---"


@dataclass(frozen=True)
class ExtractedDocument:
    path: Path
    metadata: dict[str, str]
    body: str


@dataclass(frozen=True)
class LocatedSection:
    locator_type: str
    locator_value: str
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build working/candidate_units.jsonl from extracted Markdown. "
            "This does not analyze topic importance."
        )
    )
    parser.add_argument("course_name", help="Course folder name under --root.")
    parser.add_argument("--root", default="courses", help="Courses root directory.")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help=f"Approximate maximum text characters per candidate unit. Default: {DEFAULT_MAX_CHARS}",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=DEFAULT_MIN_CHARS,
        help=f"Merge adjacent small locators until around this size. Default: {DEFAULT_MIN_CHARS}",
    )
    parser.add_argument(
        "--max-locators",
        type=int,
        default=DEFAULT_MAX_LOCATORS,
        help=f"Maximum page/slide/chunk locators per unit. Default: {DEFAULT_MAX_LOCATORS}",
    )
    parser.add_argument(
        "--knowledge-only",
        action="store_true",
        help="Only emit units from extracted knowledge sources.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_BOUNDARY:
        return {}, text

    metadata: dict[str, str] = {}
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == FRONT_MATTER_BOUNDARY:
            end_index = index
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = value[1:-1].replace('\\"', '"')
        metadata[key.strip()] = value

    body = "\n".join(lines[(end_index + 1) if end_index is not None else 0 :]).strip()
    return metadata, body


def load_documents(extracted_root: Path, include_questions: bool) -> list[ExtractedDocument]:
    folders = ["knowledge"]
    if include_questions:
        folders.append("questions")

    documents: list[ExtractedDocument] = []
    for folder in folders:
        folder_path = extracted_root / folder
        if not folder_path.exists():
            continue
        for path in sorted(folder_path.glob("*.md")):
            text = read_text(path)
            metadata, body = parse_front_matter(text)
            documents.append(ExtractedDocument(path=path, metadata=metadata, body=body))
    return documents


def clean_body(body: str) -> str:
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") or stripped == "## Extracted Text":
            continue
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def split_located_sections(body: str) -> list[LocatedSection]:
    body = clean_body(body)
    matches = list(LOCATOR_RE.finditer(body))
    if not matches:
        return [LocatedSection(locator_type="Document", locator_value="1", text=body)]

    sections: list[LocatedSection] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        text = body[start:end].strip()
        sections.append(
            LocatedSection(
                locator_type=match.group(1),
                locator_value=match.group(2),
                text=text,
            )
        )
    return sections


def section_len(section: LocatedSection) -> int:
    return len(section.text.strip())


def merge_sections(
    sections: list[LocatedSection],
    min_chars: int,
    max_chars: int,
    max_locators: int,
) -> list[list[LocatedSection]]:
    chunks: list[list[LocatedSection]] = []
    current: list[LocatedSection] = []
    current_len = 0

    for section in sections:
        next_len = section_len(section)
        should_flush = False
        if current:
            if current_len >= min_chars and current_len + next_len > max_chars:
                should_flush = True
            elif len(current) >= max_locators:
                should_flush = True

        if should_flush:
            chunks.append(current)
            current = []
            current_len = 0

        current.append(section)
        current_len += next_len

    if current:
        chunks.append(current)
    return chunks


def locator_range(sections: list[LocatedSection]) -> tuple[str, str, str]:
    locator_type = sections[0].locator_type if sections else "Document"
    values = [section.locator_value for section in sections]
    if not values:
        return locator_type, "", ""
    start = values[0]
    end = values[-1]
    page_range = start if start == end else f"{start}-{end}"
    return locator_type, start, page_range


def text_for_sections(sections: list[LocatedSection]) -> str:
    parts = []
    for section in sections:
        parts.append(f"## {section.locator_type} {section.locator_value}\n\n{section.text.strip()}")
    return "\n\n".join(part for part in parts if part.strip()).strip()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def excerpt(text: str) -> tuple[str, bool]:
    normalized = normalize_space(text)
    if len(normalized) <= EXCERPT_CHARS:
        return normalized, False
    return normalized[:EXCERPT_CHARS].rstrip() + "...", True


def keywords(text: str) -> list[str]:
    counts: dict[str, int] = {}
    first_seen: dict[str, int] = {}
    for index, match in enumerate(re.finditer(r"[A-Za-z][A-Za-z0-9+-]{2,}", text)):
        word = match.group(0).strip("-+").lower()
        if not word or word in STOPWORDS or len(word) < 3:
            continue
        counts[word] = counts.get(word, 0) + 1
        first_seen.setdefault(word, index)

    ranked = sorted(counts, key=lambda word: (-counts[word], first_seen[word], word))
    return ranked[:MAX_KEYWORDS]


def collect_signal_lines(text: str, patterns: list[re.Pattern[str]]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = normalize_space(raw_line)
        if not line or len(line) > 180:
            continue
        if any(pattern.search(line) for pattern in patterns):
            key = line.casefold()
            if key in seen:
                continue
            seen.add(key)
            lines.append(line)
            if len(lines) >= MAX_SIGNAL_LINES:
                break
    return lines


def formula_like_lines(text: str) -> list[str]:
    patterns = [
        re.compile(r"[A-Za-z0-9)\]]\s*=\s*[-+A-Za-z0-9(]"),
        re.compile(r"\b(log|sum|entropy|probability|ratio|rate|bits?|bytes?|hz|khz|db|fps)\b", re.IGNORECASE),
        re.compile(r"[-+*/^]|<=|>=|=>|->"),
    ]
    return collect_signal_lines(text, patterns)


def definition_like_lines(text: str) -> list[str]:
    patterns = [
        re.compile(r"\b(is|are|means|refers to|defined as|definition|called)\b", re.IGNORECASE),
        re.compile(r"^\s*[A-Z][A-Za-z0-9 /-]{2,40}\s*:\s+"),
    ]
    return collect_signal_lines(text, patterns)


def list_table_markers(text: str) -> list[str]:
    markers: list[str] = []
    if re.search(r"^\s*[-*+]\s+", text, re.MULTILINE):
        markers.append("bullets")
    if re.search(r"^\s*\d+[.)]\s+", text, re.MULTILINE):
        markers.append("numbered_list")
    if re.search(r"\S\s+\|\s+\S", text):
        markers.append("table_like")
    if re.search(r"^\s*(Procedure|Algorithm|Steps?)\b", text, re.IGNORECASE | re.MULTILINE):
        markers.append("procedure")
    return markers


def heading_for_text(text: str) -> str:
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        heading_match = MARKDOWN_HEADING_RE.match(line)
        if heading_match:
            heading = heading_match.group(1).strip()
            if heading and not heading.lower().startswith(("page ", "slide ", "chunk ")):
                return heading[:100]
            continue
        if line.lower().startswith("heading:"):
            return line.split(":", 1)[1].strip()[:100]
        if len(line) <= 80 and not line.endswith("."):
            return line[:100]
    return ""


def source_sort_key(document: ExtractedDocument) -> tuple[str, str]:
    source_id = document.metadata.get("source_id", "")
    relative_path = document.metadata.get("relative_path", document.path.name)
    return source_id, relative_path


def make_unit(
    document: ExtractedDocument,
    unit_index: int,
    sections: list[LocatedSection],
) -> dict[str, object]:
    metadata = document.metadata
    source_id = metadata.get("source_id", "")
    source_folder = metadata.get("source_folder", "")
    inferred_source_type = metadata.get("inferred_source_type", "")
    locator_type, start_locator, pages = locator_range(sections)
    chunk_text = text_for_sections(sections)
    unit_id = f"{source_id or 'S'}-C{unit_index:03d}"
    unit_excerpt, truncated = excerpt(chunk_text)
    unit_role = "question_evidence_unit" if source_folder == "questions" else "knowledge_unit"

    return {
        "unit_id": unit_id,
        "source_id": source_id,
        "source": source_id,
        "source_folder": source_folder,
        "inferred_source_type": inferred_source_type,
        "unit_role": unit_role,
        "relative_path": metadata.get("relative_path", document.path.name),
        "original_file": metadata.get("original_file", document.path.name),
        "status": metadata.get("status", ""),
        "unit_index": unit_index,
        "locator_type": locator_type,
        "start_locator": start_locator,
        "end_locator": sections[-1].locator_value if sections else "",
        "pages": pages,
        "heading": heading_for_text(chunk_text),
        "keywords": keywords(chunk_text),
        "formula_like_lines": formula_like_lines(chunk_text),
        "definition_like_lines": definition_like_lines(chunk_text),
        "list_table_markers": list_table_markers(chunk_text),
        "excerpt": unit_excerpt,
        "estimated_chars": len(chunk_text),
        "truncated": truncated,
    }


def build_units(
    documents: list[ExtractedDocument],
    min_chars: int,
    max_chars: int,
    max_locators: int,
) -> list[dict[str, object]]:
    units: list[dict[str, object]] = []
    for document in sorted(documents, key=source_sort_key):
        sections = split_located_sections(document.body)
        chunks = merge_sections(sections, min_chars, max_chars, max_locators)
        for unit_index, chunk in enumerate(chunks, start=1):
            units.append(make_unit(document, unit_index, chunk))
    return units


def run(
    course_name: str,
    root: Path,
    max_chars: int,
    min_chars: int,
    max_locators: int,
    knowledge_only: bool,
) -> int:
    course_root = root / course_name
    working_root = course_root / "working"
    extracted_root = working_root / "extracted"

    if not course_root.exists():
        print(f"ERROR: Course folder not found: {course_root}")
        return 2
    if not extracted_root.exists():
        print(f"ERROR: Extracted materials not found: {extracted_root}")
        print("Run extract_materials.py before build_candidate_units.py.")
        return 2

    documents = load_documents(extracted_root, include_questions=not knowledge_only)
    if not documents:
        print(f"ERROR: No extracted Markdown files found under {extracted_root}")
        return 2

    units = build_units(
        documents=documents,
        min_chars=max(1, min_chars),
        max_chars=max(1, max_chars),
        max_locators=max(1, max_locators),
    )

    output_path = working_root / "candidate_units.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for unit in units:
            handle.write(json.dumps(unit, ensure_ascii=False, sort_keys=True) + "\n")

    knowledge_count = sum(1 for unit in units if unit["unit_role"] == "knowledge_unit")
    question_count = sum(1 for unit in units if unit["unit_role"] == "question_evidence_unit")
    print(f"Wrote {output_path}")
    print(f"Candidate units: {len(units)} total, {knowledge_count} knowledge, {question_count} question evidence.")
    return 0


def main() -> int:
    args = parse_args()
    return run(
        course_name=args.course_name,
        root=Path(args.root),
        max_chars=args.max_chars,
        min_chars=args.min_chars,
        max_locators=args.max_locators,
        knowledge_only=args.knowledge_only,
    )


if __name__ == "__main__":
    sys.exit(main())
