"""Validate a course-cheatsheet-maker course workflow.

The validator checks extraction coverage, run configuration, reasoning artifacts,
rendered HTML, anti-fabrication language, page-budget heuristics, and renderer
scope. It does not replace Codex's semantic analysis of extracted course text.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


REQUIRED_WORKING_FILES = [
    "topic_map.md",
    "importance_ranking.md",
    "cheatsheet_content.md",
]
REQUIRED_OUTPUTS = [
    ("cheatsheet_3col.html", "column-count: 3"),
    ("cheatsheet_4col.html", "column-count: 4"),
]
COVERAGE_MODES = ["exam-compact", "balanced-standard", "comprehensive-review"]
DETAIL_MODES = ["detailed", "balanced", "simple"]
LAYOUTS = ["3col", "4col"]
DEFAULT_LAYOUT = "3col"
DEFAULT_TARGET_PAGES = 1
DEFAULT_COVERAGE_MODE = "balanced-standard"
DEFAULT_DETAIL_MODE = "balanced"
DEFAULT_PRINT_SCALE = 0.84
COLUMN_BUDGETS = {
    "3col": {
        "columns": 3,
        "chars_per_column": 8000,
        "healthy_ranges": {
            1: (20000, 25000),
            2: (44000, 50000),
            3: (68000, 75000),
        },
    },
    "4col": {
        "columns": 4,
        "chars_per_column": 7000,
        "healthy_ranges": {
            1: (24000, 30000),
            2: (52000, 60000),
            3: (80000, 90000),
        },
    },
}
CALIBRATED_3COL_PAGE_BUDGETS = {
    1: {
        "floor": 14000,
        "target_min": 16000,
        "target_max": 18000,
        "soft_ceiling": 20000,
        "hard_ceiling": 22000,
        "topic_min": 35,
        "topic_max": 45,
    },
    2: {
        "floor": 34000,
        "target_min": 36000,
        "target_max": 38000,
        "soft_ceiling": 40000,
        "hard_ceiling": 41000,
        "topic_min": 75,
        "topic_max": 85,
    },
    3: {
        "floor": 44000,
        "target_min": 48000,
        "target_max": 52000,
        "soft_ceiling": 55000,
        "hard_ceiling": 58000,
        "topic_min": 95,
        "topic_max": 115,
    },
    4: {
        "floor": 60000,
        "target_min": 64000,
        "target_max": 70000,
        "soft_ceiling": 74000,
        "hard_ceiling": 78000,
        "topic_min": 115,
        "topic_max": 135,
    },
    5: {
        "floor": 76000,
        "target_min": 82000,
        "target_max": 88000,
        "soft_ceiling": 93000,
        "hard_ceiling": 98000,
        "topic_min": 130,
        "topic_max": 150,
    },
    6: {
        "floor": 92000,
        "target_min": 100000,
        "target_max": 108000,
        "soft_ceiling": 114000,
        "hard_ceiling": 120000,
        "topic_min": 145,
        "topic_max": 170,
    },
}
MOJIBAKE_MARKERS = [
    "姣",
    "鍗",
    "鐜",
    "鏂",
    "澶",
    "淇",
    "伅",
    "閲",
    "璁",
    "绠",
    "鐔",
    "涓",
    "笌",
]
MOJIBAKE_MIN_TOTAL_HITS = 3
MOJIBAKE_MIN_DISTINCT_MARKERS = 2
RUN_CONFIG_FIELDS = [
    "workflow_mode",
    "layout",
    "target_pages",
    "coverage_mode",
    "detail_mode",
]
RUN_CONFIG_SECTIONS = [
    "User-specified parameters",
    "Defaulted parameters",
    "Conflict resolution",
    "Selection Plan",
]
SUPPORTED_TEXT = {".md", ".txt"}
SUPPORTED_BINARY = {".pdf", ".pptx", ".docx"}
SUPPORTED_EXTENSIONS = SUPPORTED_TEXT | SUPPORTED_BINARY
NO_PAST_SAMPLE_CAVEAT = (
    "没有提供往年卷，因此重要程度主要基于 PPT/Notes 强调、"
    "Quiz/Assignment/Workshop/Tutorial 出现频率、知识点基础性和可考性判断。"
)
PAST_SAMPLE_RE = re.compile(
    r"(past[_ -]?paper|final[_ -]?exam|(?<![a-z])exam[_ -]?\d{4}|"
    r"sample[_ -]?exam|mock[_ -]?exam|practice[_ -]?exam)",
    re.IGNORECASE,
)
UNSUPPORTED_PREDICTIONS = [
    "will definitely appear",
    "definitely appear",
    "一定会考",
    "必考",
]
PRELIMINARY_MARKERS = [
    "preliminary",
    "filename",
    "filenames",
    "extraction report",
    "extraction_report.md",
    "extraction failed",
    "text was not extracted",
    "no selectable text",
    "only filenames",
    "coverage is based on filenames",
    "内容覆盖为初步",
    "初步",
]
CONFIDENT_DETAIL_MARKERS = [
    "Formula:",
    "Def:",
    "Procedure:",
    "Compare:",
    "Algorithm",
    "Theorem",
    "past-paper pattern",
    "exam pattern",
]
SCORE_LINE_RE = re.compile(
    r"Scores:\s*"
    r"(?=.*(?:Knowledge emphasis|Lecture coverage)\s*=\s*[0-3])"
    r"(?=.*(?:Question evidence|Exam evidence)\s*=\s*[0-3])"
    r"(?=.*(?:Testability|Testability/formula value)\s*=\s*[0-3])"
    r"(?=.*Dependency\s*=\s*[0-3])"
    r"(?=.*Error risk\s*=\s*[0-3])"
    r"(?=.*Total\s*=\s*(?:[0-9]|1[0-5]))",
    re.IGNORECASE,
)
DETAIL_MODE_RE = re.compile(
    r"(?:Detail mode|Recommended detail):\s*(detailed|balanced|simple|minimal/simple|minimal|omit)",
    re.IGNORECASE,
)
PRIORITY_RE = re.compile(r"Priority:\s*([ABCR])\b", re.IGNORECASE)
TOTAL_SCORE_RE = re.compile(r"Total\s*=\s*(\d+)", re.IGNORECASE)
MODE_LINE_RE = re.compile(
    r"\b(workflow_mode|layout|target_pages|coverage_mode|detail_mode)\s*[:=]\s*([A-Za-z0-9_-]+)",
    re.IGNORECASE,
)
FILENAME_ONLY_HIGH_PRIORITY_RE = re.compile(
    r"Priority:\s*[AB][\s\S]{0,500}?filename-only",
    re.IGNORECASE,
)
SOURCE_ID_RE = re.compile(r"\b[KQ]\d{2}\b")
EXTRACTED_UNITS_RE = re.compile(
    r"\b\d+\s+(?:page|pages|slide|slides|chunk|chunks|paragraph|paragraphs|table|tables)\b",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[\u3400-\u9fff]")
TOPIC_LINE_RE = re.compile(r"^Topic:\s*(.+)$", re.MULTILINE)
WORD_RE = re.compile(r"[a-z0-9]{4,}", re.IGNORECASE)
TOPIC_STOP_WORDS = {
    "and",
    "with",
    "from",
    "into",
    "the",
    "topic",
    "priority",
    "quality",
    "examples",
}


@dataclass(frozen=True)
class MaterialFile:
    source_folder: str
    relative_path: str
    path: Path
    suffix: str


@dataclass(frozen=True)
class ExtractedRecord:
    source_id: str
    source_folder: str
    relative_path: str
    status: str
    inferred_source_type: str
    extracted_units: str
    path: Path


@dataclass(frozen=True)
class PrintPageResult:
    actual_pages: int | None
    skipped_reason: str | None = None


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate course-cheatsheet-maker workflow artifacts and outputs."
    )
    parser.add_argument("course_name", help="Course folder name under --root.")
    parser.add_argument("--root", default="courses", help="Courses root directory.")
    parser.add_argument(
        "--mode",
        choices=["safe-review", "full-auto"],
        default="full-auto",
        help="safe-review skips required HTML output checks; full-auto requires rendered HTML.",
    )
    parser.add_argument(
        "--coverage-mode",
        choices=COVERAGE_MODES,
        default=DEFAULT_COVERAGE_MODE,
        help=(
            "Content coverage mode used for warning heuristics. "
            f"Default: {DEFAULT_COVERAGE_MODE}."
        ),
    )
    parser.add_argument(
        "--detail-mode",
        choices=DETAIL_MODES,
        default=DEFAULT_DETAIL_MODE,
        help=(
            "Content detail mode used for warning heuristics. "
            f"Default: {DEFAULT_DETAIL_MODE}."
        ),
    )
    parser.add_argument(
        "--layout",
        choices=LAYOUTS,
        default=DEFAULT_LAYOUT,
        help=f"Preferred layout for warning heuristics. Default: {DEFAULT_LAYOUT}.",
    )
    parser.add_argument(
        "--target-pages",
        type=positive_int,
        default=DEFAULT_TARGET_PAGES,
        help=(
            "Integer page budget for warning heuristics. "
            f"Default: {DEFAULT_TARGET_PAGES}."
        ),
    )
    parser.add_argument(
        "--check-print-pages",
        action="store_true",
        help=(
            "Optionally render the selected HTML to PDF and compare actual PDF "
            "pages with --target-pages. Falls back to character heuristics if "
            "the optional print tool is unavailable."
        ),
    )
    parser.add_argument(
        "--print-scale",
        type=float,
        default=DEFAULT_PRINT_SCALE,
        help=(
            "Scale used by optional print-page validation. "
            f"Default: {DEFAULT_PRINT_SCALE}."
        ),
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_error(errors: list[str], message: str) -> None:
    errors.append(f"ERROR: {message}")


def add_warning(warnings: list[str], message: str) -> None:
    warnings.append(f"WARNING: {message}")


def contains_any(text: str, needles: list[str]) -> list[str]:
    lowered = text.lower()
    hits = []
    for needle in needles:
        if needle.lower() in lowered:
            hits.append(needle)
    return hits


def extracted_page_count(records: dict[tuple[str, str], ExtractedRecord]) -> int:
    total = 0
    for record in records.values():
        match = re.search(r"\b(\d+)\s+pages?\b", record.extracted_units, re.IGNORECASE)
        if match:
            total += int(match.group(1))
    return total


def record_page_count(record: ExtractedRecord) -> int:
    match = re.search(r"\b(\d+)\s+pages?\b", record.extracted_units, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def is_administrative_source(record: ExtractedRecord) -> bool:
    text = f"{record.relative_path} {record.inferred_source_type}".casefold()
    administrative_terms = [
        "administrative",
        "course information",
        "course_information",
        "syllabus",
        "assessment",
        "grading",
        "outline",
        "logistics",
    ]
    return any(term in text for term in administrative_terms)


def priority_for_total(total: int) -> str:
    if total >= 11:
        return "A"
    if total >= 7:
        return "B"
    if total >= 4:
        return "C"
    return "R"


def iter_priority_blocks(importance_text: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"^Priority:\s*[ABCR]\b", importance_text, re.MULTILINE | re.IGNORECASE)]
    blocks: list[str] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(importance_text)
        blocks.append(importance_text[start:end])
    return blocks


def extract_declared_modes(text: str) -> dict[str, str]:
    modes: dict[str, str] = {}
    for match in MODE_LINE_RE.finditer(text):
        modes[match.group(1).lower()] = match.group(2).lower()
    return modes


def topic_count(content_text: str) -> int:
    return len(TOPIC_LINE_RE.findall(content_text))


def ranked_topic_count(importance_text: str) -> int:
    return len(iter_priority_blocks(importance_text))


def candidate_unit_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in read_text(path).splitlines() if line.strip())


def min_topic_count_for_pages(target_pages: int) -> int:
    budget = calibrated_3col_budget(target_pages)
    if budget:
        return budget["topic_min"]
    if target_pages > 6:
        return extrapolated_3col_budget(target_pages)["topic_min"]
    return 20


def layout_columns(layout: str) -> int:
    return int(COLUMN_BUDGETS[layout]["columns"])


def min_chars_for_page_budget(layout: str, target_pages: int) -> int:
    budget = COLUMN_BUDGETS[layout]
    total_slots = target_pages * int(budget["columns"])
    required_filled_columns = max(1, total_slots - 1)
    return required_filled_columns * int(budget["chars_per_column"])


def healthy_char_range(layout: str, target_pages: int) -> tuple[int, int] | None:
    ranges = COLUMN_BUDGETS[layout]["healthy_ranges"]
    return ranges.get(target_pages) if isinstance(ranges, dict) else None


def calibrated_3col_budget(target_pages: int) -> dict[str, int] | None:
    return CALIBRATED_3COL_PAGE_BUDGETS.get(target_pages)


def extrapolated_3col_budget(target_pages: int) -> dict[str, int]:
    page_6 = CALIBRATED_3COL_PAGE_BUDGETS[6]
    extra_pages = max(0, target_pages - 6)
    return {
        "floor": page_6["floor"] + extra_pages * 16000,
        "target_min": page_6["target_min"] + extra_pages * 18000,
        "target_max": page_6["target_max"] + extra_pages * 18000,
        "soft_ceiling": page_6["soft_ceiling"] + extra_pages * 19000,
        "hard_ceiling": page_6["hard_ceiling"] + extra_pages * 20000,
        "topic_min": page_6["topic_min"] + extra_pages * 15,
        "topic_max": page_6["topic_max"] + extra_pages * 20,
    }


def mojibake_marker_counts(text: str) -> dict[str, int]:
    return {marker: text.count(marker) for marker in MOJIBAKE_MARKERS if marker in text}


def likely_mojibake_hits(text: str) -> dict[str, int]:
    counts = mojibake_marker_counts(text)
    total_hits = sum(counts.values())
    distinct_markers = len(counts)
    if (
        total_hits >= MOJIBAKE_MIN_TOTAL_HITS
        or distinct_markers >= MOJIBAKE_MIN_DISTINCT_MARKERS
    ):
        return counts
    return {}


def validate_mojibake_warning(
    label: str,
    text: str,
    warnings: list[str],
) -> None:
    hits = likely_mojibake_hits(text)
    if not hits:
        return
    total_hits = sum(hits.values())
    add_warning(
        warnings,
        f"{label} contains repeated likely mojibake markers "
        f"({total_hits} total hits across {len(hits)} marker types); "
        "bilingual Topic headings with mojibake are not valid Chinese output. "
        "In Full Auto, repair cheatsheet_content.md and rerender HTML.",
    )


def selected_html_output(output_dir: Path, layout: str) -> Path:
    return output_dir / f"cheatsheet_{layout}.html"


def count_pdf_pages(pdf_path: Path) -> tuple[int | None, str | None]:
    try:
        import fitz  # type: ignore
    except ImportError:
        fitz = None  # type: ignore

    if fitz is not None:
        try:
            with fitz.open(pdf_path) as document:
                return document.page_count, None
        except Exception as exc:  # pragma: no cover - environment dependent
            return None, f"PyMuPDF could not count PDF pages: {exc}"

    try:
        from PyPDF2 import PdfReader  # type: ignore
    except ImportError:
        return None, "no PDF page counter is available; install PyMuPDF or PyPDF2 for optional print-page validation"

    try:
        reader = PdfReader(str(pdf_path))
        return len(reader.pages), None
    except Exception as exc:  # pragma: no cover - environment dependent
        return None, f"PyPDF2 could not count PDF pages: {exc}"


def render_pdf_with_optional_playwright(
    html_path: Path,
    pdf_path: Path,
    print_scale: float,
) -> str | None:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return "optional browser PDF renderer unavailable: Python Playwright is not installed"

    try:
        with sync_playwright() as playwright:
            launch_errors = []
            browser = None
            for channel in ("chrome", "msedge", None):
                try:
                    browser = playwright.chromium.launch(
                        channel=channel,
                        headless=True,
                    )
                    break
                except Exception as exc:  # pragma: no cover - environment dependent
                    label = channel or "bundled chromium"
                    launch_errors.append(f"{label}: {exc}")
            if browser is None:
                return "browser launch failed: " + " | ".join(launch_errors)

            try:
                page = browser.new_page()
                page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
                page.emulate_media(media="print")
                page.pdf(
                    path=str(pdf_path),
                    format="A4",
                    landscape=True,
                    print_background=True,
                    scale=print_scale,
                    prefer_css_page_size=True,
                )
            finally:
                browser.close()
    except Exception as exc:  # pragma: no cover - environment dependent
        return f"PDF generation failed: {exc}"

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        return "PDF generation produced no output"
    return None


def check_print_pages(
    html_path: Path,
    print_scale: float,
) -> PrintPageResult:
    if not html_path.exists():
        return PrintPageResult(None, f"selected HTML output is missing: {html_path}")
    if print_scale <= 0:
        return PrintPageResult(None, f"--print-scale must be positive, got {print_scale}")

    with tempfile.TemporaryDirectory(prefix="course-cheatsheet-print-") as temp_dir:
        pdf_path = Path(temp_dir) / "cheatsheet-print-check.pdf"
        render_error = render_pdf_with_optional_playwright(
            html_path=html_path,
            pdf_path=pdf_path,
            print_scale=print_scale,
        )
        if render_error:
            return PrintPageResult(None, render_error)

        page_count, count_error = count_pdf_pages(pdf_path)
        if count_error:
            return PrintPageResult(None, count_error)
        return PrintPageResult(page_count, None)


def normalized_words(text: str) -> set[str]:
    return {
        match.group(0).casefold()
        for match in WORD_RE.finditer(text)
        if match.group(0).casefold() not in TOPIC_STOP_WORDS
    }


def topic_label_from_block(block: str) -> str:
    match = re.search(r"^Topic:\s*(.+)$", block, re.MULTILINE)
    if not match:
        return ""
    label = match.group(1).strip()
    label = re.sub(r"\[[ABCR]\]\s*$", "", label).strip()
    return label.split("/", 1)[0].strip()


def a_topic_labels(importance_text: str) -> list[str]:
    labels = []
    for block in iter_priority_blocks(importance_text):
        priority_match = PRIORITY_RE.search(block)
        if not priority_match or priority_match.group(1).upper() != "A":
            continue
        label = topic_label_from_block(block)
        if label:
            labels.append(label)
    return labels


def count_source_topics(evidence_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    sections = re.split(r"(?m)^##\s+", evidence_text)
    for section in sections:
        source_ids = set(SOURCE_ID_RE.findall(section))
        for source_id in source_ids:
            counts[source_id] = counts.get(source_id, 0) + 1
    return counts


def material_files(directory: Path, source_folder: str) -> list[MaterialFile]:
    if not directory.exists():
        return []
    files = []
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        files.append(
            MaterialFile(
                source_folder=source_folder,
                relative_path=path.relative_to(directory).as_posix(),
                path=path,
                suffix=path.suffix.lower(),
            )
        )
    return files


def parse_front_matter(path: Path) -> dict[str, str]:
    text = read_text(path)
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
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
    return metadata


def extracted_records(
    extracted_root: Path, warnings: list[str]
) -> dict[tuple[str, str], ExtractedRecord]:
    records: dict[tuple[str, str], ExtractedRecord] = {}
    if not extracted_root.exists():
        return records
    for path in sorted(extracted_root.rglob("*.md")):
        metadata = parse_front_matter(path)
        source_id = metadata.get("source_id", "")
        source_folder = metadata.get("source_folder", "")
        relative_path = metadata.get("relative_path", "")
        status = metadata.get("status", "")
        inferred_source_type = metadata.get("inferred_source_type", "")
        extracted_units = metadata.get("extracted_units", "")
        if not source_folder or not relative_path or not status:
            add_warning(warnings, f"extracted file lacks required metadata: {path}")
            continue
        records[(source_folder, relative_path)] = ExtractedRecord(
            source_id=source_id,
            source_folder=source_folder,
            relative_path=relative_path,
            status=status,
            inferred_source_type=inferred_source_type,
            extracted_units=extracted_units,
            path=path,
        )
    return records


def validate_renderer_scope(skill_root: Path, errors: list[str]) -> None:
    script = skill_root / "scripts" / "build_html.py"
    try:
        tree = ast.parse(read_text(script), filename=str(script))
    except SyntaxError as exc:
        add_error(errors, f"build_html.py has a syntax error: {exc}")
        return

    suspicious_strings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            normalized = node.value.replace("\\", "/").lower()
            if (
                "materials/" in normalized
                or normalized == "materials"
                or "working/extracted" in normalized
                or normalized == "extracted"
                or "topic_evidence_map.md" in normalized
            ):
                suspicious_strings.append(node.value)

    if suspicious_strings:
        joined = ", ".join(repr(value) for value in suspicious_strings[:3])
        add_error(
            errors,
            f"build_html.py appears to reference source materials or extracted text: {joined}",
        )


def report_documents_failure(report_text: str, material: MaterialFile) -> bool:
    if not report_text:
        return False
    if material.relative_path not in report_text:
        return False
    statuses = ["failed", "unsupported", "no_selectable_text"]
    return any(status in report_text for status in statuses)


def validate_report_shape(
    report_text: str,
    records: dict[tuple[str, str], ExtractedRecord],
    errors: list[str],
) -> None:
    if not records:
        return
    for header in ["Source ID", "Extracted units"]:
        if header not in report_text:
            add_error(errors, f"extraction_report.md is missing `{header}` column")
    for record in records.values():
        if not SOURCE_ID_RE.fullmatch(record.source_id):
            add_error(errors, f"extracted file lacks valid source_id: {record.path}")
        if not EXTRACTED_UNITS_RE.search(record.extracted_units):
            add_error(errors, f"extracted file lacks extracted_units: {record.path}")
        if record.source_id and record.source_id not in report_text:
            add_error(errors, f"extraction_report.md omits source ID {record.source_id}")
        if record.extracted_units and record.extracted_units not in report_text:
            add_error(
                errors,
                f"extraction_report.md omits extracted units for {record.source_id}",
            )


def validate_extracted_locators(
    materials: list[MaterialFile],
    records: dict[tuple[str, str], ExtractedRecord],
    errors: list[str],
) -> None:
    for material in materials:
        record = records.get((material.source_folder, material.relative_path))
        if not record or record.status not in {"success", "no_selectable_text"}:
            continue
        extracted_text = read_text(record.path)
        if material.suffix == ".pdf" and "## Page " not in extracted_text:
            add_error(errors, f"PDF extraction lacks page markers: {record.path}")
        if material.suffix == ".pptx" and "## Slide " not in extracted_text:
            add_error(errors, f"PPTX extraction lacks slide markers: {record.path}")
        if material.suffix == ".docx" and "## Document Text" not in extracted_text:
            add_error(errors, f"DOCX extraction lacks document text marker: {record.path}")


def validate_extraction(
    materials: list[MaterialFile],
    working_dir: Path,
    working_text: str,
    mode: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    supported = [
        material for material in materials if material.suffix in SUPPORTED_EXTENSIONS
    ]
    binary = [material for material in supported if material.suffix in SUPPORTED_BINARY]
    report_path = working_dir / "extraction_report.md"
    report_text = read_text(report_path) if report_path.exists() else ""

    if binary and not report_path.exists():
        add_error(errors, "binary source files exist but working/extraction_report.md is missing")

    records = extracted_records(working_dir / "extracted", warnings)
    if report_text:
        validate_report_shape(report_text, records, errors)
    validate_extracted_locators(supported, records, errors)

    successful_binary = 0
    extraction_issues: list[MaterialFile] = []

    for material in supported:
        record = records.get((material.source_folder, material.relative_path))
        if record:
            if record.status == "success" and material.suffix in SUPPORTED_BINARY:
                successful_binary += 1
            elif record.status in {"failed", "unsupported", "no_selectable_text"}:
                extraction_issues.append(material)
            elif record.status not in {
                "success",
                "failed",
                "unsupported",
                "no_selectable_text",
            }:
                add_error(
                    errors,
                    f"unknown extraction status for {material.relative_path}: {record.status}",
                )
            continue

        if report_documents_failure(report_text, material):
            extraction_issues.append(material)
            continue

        add_error(
            errors,
            f"supported material has neither extracted Markdown nor documented failure: "
            f"{material.source_folder}/{material.relative_path}",
        )

    if not binary:
        return

    has_preliminary_label = bool(contains_any(working_text, PRELIMINARY_MARKERS))
    all_binary_missing = successful_binary == 0
    some_binary_failed = bool(extraction_issues)

    if all_binary_missing:
        if has_preliminary_label:
            add_warning(
                warnings,
                "binary source extraction produced no successful text; working files label coverage as preliminary",
            )
        else:
            add_error(
                errors,
                "binary source extraction produced no successful text but working files are not preliminary",
            )
    elif some_binary_failed:
        if has_preliminary_label:
            add_warning(
                warnings, "some binary source extraction failed; preliminary coverage is documented"
            )
        else:
            add_error(
                errors,
                "some binary extraction failed but working files do not label coverage as preliminary",
            )

    if (all_binary_missing or some_binary_failed) and not has_preliminary_label:
        detail_hits = contains_any(working_text, CONFIDENT_DETAIL_MARKERS)
        if detail_hits:
            add_error(
                errors,
                f"working files contain confident detailed content while extraction is incomplete: {detail_hits}",
            )

    if mode == "full-auto" and all_binary_missing and not has_preliminary_label:
        add_error(errors, "Full Auto Mode cannot pass with filename-only analysis and no preliminary caveat")


def validate_importance_ranking(
    importance_text: str,
    question_files: list[MaterialFile],
    records: dict[tuple[str, str], ExtractedRecord],
    errors: list[str],
    warnings: list[str],
) -> None:
    if not SCORE_LINE_RE.search(importance_text):
        add_error(errors, "importance_ranking.md is missing score lines")
    if not DETAIL_MODE_RE.search(importance_text):
        add_error(errors, "importance_ranking.md is missing detail/recommended detail lines")
    if FILENAME_ONLY_HIGH_PRIORITY_RE.search(importance_text):
        add_error(errors, "filename-only evidence must not rank as A or B")

    validate_priority_score_consistency(importance_text, warnings)

    exam_source_types = {
        "past_paper",
        "final_exam",
        "sample_exam",
        "mock_exam",
        "practice_exam",
    }
    has_past_or_sample = any(
        PAST_SAMPLE_RE.search(material.relative_path) for material in question_files
    )
    has_past_or_sample = has_past_or_sample or any(
        record.source_folder == "questions"
        and record.status == "success"
        and record.inferred_source_type in exam_source_types
        for record in records.values()
    )
    if not has_past_or_sample and NO_PAST_SAMPLE_CAVEAT not in importance_text:
        add_error(errors, "missing required no-past-paper/sample-exam caveat")


def validate_evidence_map(
    working_dir: Path,
    records: dict[tuple[str, str], ExtractedRecord],
    mode: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    evidence_map = working_dir / "topic_evidence_map.md"
    if mode != "full-auto":
        return
    if not evidence_map.exists():
        add_error(errors, f"missing required Full Auto evidence map: {evidence_map}")
        return

    text = read_text(evidence_map)
    if not text.strip():
        add_error(errors, f"evidence map is empty: {evidence_map}")
    if "# Topic Evidence Map" not in text:
        add_error(errors, "topic_evidence_map.md is missing its standard heading")
    if records and not SOURCE_ID_RE.search(text):
        add_error(errors, "topic_evidence_map.md does not reference source IDs")
    if len(text.split()) > 1800:
        add_warning(warnings, "topic_evidence_map.md is long; keep evidence entries concise")


def validate_bilingual_topic_labels(content_text: str, warnings: list[str]) -> None:
    topic_lines = [match.group(1).strip() for match in TOPIC_LINE_RE.finditer(content_text)]
    if len(topic_lines) < 2:
        return

    has_bilingual_lookup_label = any(
        "/" in line and CJK_RE.search(line.split("/", 1)[1]) for line in topic_lines
    )
    if not has_bilingual_lookup_label:
        add_warning(
            warnings,
            "cheatsheet_content.md has multiple Topic lines but no bilingual `/ 中文` lookup labels",
        )


def validate_candidate_units_shape(path: Path, warnings: list[str]) -> None:
    if not path.exists():
        return

    malformed = 0
    role_issues = 0
    last_line_number = 0
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        last_line_number = line_number
        if not line.strip():
            continue
        try:
            unit = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue

        source_folder = unit.get("source_folder")
        inferred_source_type = unit.get("inferred_source_type")
        unit_role = unit.get("unit_role")
        expected_role = (
            "question_evidence_unit"
            if source_folder == "questions"
            else "knowledge_unit"
            if source_folder == "knowledge"
            else None
        )
        if not source_folder or not inferred_source_type or not unit_role:
            role_issues += 1
        elif expected_role and unit_role != expected_role:
            role_issues += 1

        if malformed + role_issues >= 5:
            break

    if malformed:
        add_warning(
            warnings,
            f"candidate_units.jsonl contains malformed JSONL rows, first issue near line {last_line_number}",
        )
    if role_issues:
        add_warning(
            warnings,
            "candidate_units.jsonl should clearly distinguish knowledge units from question evidence units",
        )


def validate_mode_metadata(
    working_text: str,
    mode: str,
    layout: str,
    target_pages: int,
    coverage_mode: str,
    detail_mode: str,
    warnings: list[str],
) -> None:
    declared = extract_declared_modes(working_text)
    expected = {
        "workflow_mode": mode,
        "layout": layout,
        "target_pages": str(target_pages),
        "coverage_mode": coverage_mode,
        "detail_mode": detail_mode,
    }
    for key, value in expected.items():
        declared_value = declared.get(key)
        if declared_value and declared_value != value:
            add_warning(
                warnings,
                f"{key} metadata says `{declared_value}` but validator was run with `{value}`",
            )


def validate_run_config(
    working_dir: Path,
    mode: str,
    layout: str,
    target_pages: int,
    coverage_mode: str,
    detail_mode: str,
    errors: list[str],
    warnings: list[str],
) -> str:
    path = working_dir / "run_config.md"
    if not path.exists():
        add_error(errors, f"missing required run configuration: {path}")
        return ""

    text = read_text(path)
    if not text.strip():
        add_error(errors, f"run configuration is empty: {path}")
        return text

    declared = extract_declared_modes(text)
    for field in RUN_CONFIG_FIELDS:
        if field not in declared:
            add_error(errors, f"run_config.md is missing `{field}`")

    for section in RUN_CONFIG_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE | re.IGNORECASE):
            add_error(errors, f"run_config.md is missing `{section}` section")

    expected = {
        "workflow_mode": mode,
        "layout": layout,
        "target_pages": str(target_pages),
        "coverage_mode": coverage_mode,
        "detail_mode": detail_mode,
    }
    for key, value in expected.items():
        declared_value = declared.get(key)
        if declared_value and declared_value != value:
            add_warning(
                warnings,
                f"run_config.md says {key} `{declared_value}` but validator was run with `{value}`",
            )

    return text


def validate_priority_score_consistency(
    importance_text: str,
    warnings: list[str],
) -> None:
    for block in iter_priority_blocks(importance_text):
        priority_match = PRIORITY_RE.search(block)
        total_match = TOTAL_SCORE_RE.search(block)
        if not priority_match or not total_match:
            continue
        priority = priority_match.group(1).upper()
        total = int(total_match.group(1))
        expected = priority_for_total(total)
        if priority != expected:
            topic_match = re.search(r"^Topic:\s*(.+)$", block, re.MULTILINE)
            topic = topic_match.group(1).strip() if topic_match else "unknown topic"
            add_warning(
                warnings,
                f"priority-score mismatch: {topic} has Total={total} but Priority {priority}; expected {expected}",
            )


def validate_page_budget_warnings(
    working_dir: Path,
    layout: str,
    target_pages: int,
    content_text: str,
    importance_text: str,
    actual_print_pages: int | None,
    warnings: list[str],
) -> None:
    content_chars = len(content_text)
    if layout == "3col":
        budget = calibrated_3col_budget(target_pages)
        if budget is None:
            budget = extrapolated_3col_budget(target_pages)
            add_warning(
                warnings,
                "3col page-budget ranges are calibrated only for target_pages 1-6; "
                f"using conservative extrapolated warnings for target_pages={target_pages}",
            )

        if content_text.strip():
            range_label = (
                f"floor {budget['floor']}, target {budget['target_min']}-{budget['target_max']}, "
                f"soft ceiling {budget['soft_ceiling']}, hard ceiling {budget['hard_ceiling']}"
            )
            if content_chars < budget["floor"]:
                message = (
                    "cheatsheet_content.md may under-fill target_pages: "
                    f"{content_chars} chars < calibrated 3col floor {budget['floor']} "
                    f"for {target_pages} page(s) ({range_label})"
                )
                if actual_print_pages == target_pages:
                    message = "sparse target output: actual printed pages matched target_pages, " + message
                add_warning(warnings, message)
            elif content_chars < budget["target_min"]:
                add_warning(
                    warnings,
                    "cheatsheet_content.md is acceptable but sparse for the calibrated 3col page budget: "
                    f"{content_chars} chars is below target range {budget['target_min']}-{budget['target_max']} "
                    f"for {target_pages} page(s); use real evidence, not filler, if repairing",
                )
            elif content_chars <= budget["target_max"]:
                pass
            elif content_chars <= budget["soft_ceiling"]:
                add_warning(
                    warnings,
                    "cheatsheet_content.md is dense for the calibrated 3col page budget and may slightly overflow: "
                    f"{content_chars} chars > target range {budget['target_min']}-{budget['target_max']} "
                    f"for {target_pages} page(s)",
                )
            elif content_chars <= budget["hard_ceiling"]:
                add_warning(
                    warnings,
                    "cheatsheet_content.md is near the calibrated 3col hard ceiling: "
                    f"{content_chars} chars > soft ceiling {budget['soft_ceiling']} "
                    f"for {target_pages} page(s)",
                )
            else:
                add_warning(
                    warnings,
                    "cheatsheet_content.md is likely to overflow the calibrated 3col page budget: "
                    f"{content_chars} chars > hard ceiling {budget['hard_ceiling']} "
                    f"for {target_pages} page(s)",
                )
    else:
        columns = layout_columns(layout)
        total_slots = target_pages * columns
        required_filled_columns = max(1, total_slots - 1)
        chars_per_column = int(COLUMN_BUDGETS[layout]["chars_per_column"])
        expected_min_chars = min_chars_for_page_budget(layout, target_pages)
        healthy_range = healthy_char_range(layout, target_pages)
        expected_max_chars = target_pages * 26000
        if healthy_range:
            expected_max_chars = max(expected_max_chars, int(healthy_range[1] * 1.15))
        if content_text.strip() and content_chars < expected_min_chars:
            message = (
                "cheatsheet_content.md may under-fill target_pages using less-tested 4col column heuristics: "
                f"{content_chars} chars < column-slot soft minimum {expected_min_chars} "
                f"for {target_pages} page(s) in {layout} "
                f"({required_filled_columns}/{total_slots} columns, "
                f"{chars_per_column} chars/column)"
            )
            if actual_print_pages == target_pages:
                message = (
                    "sparse target output: actual printed pages matched target_pages, "
                    + message
                )
            add_warning(warnings, message)
        if content_chars > expected_max_chars:
            add_warning(
                warnings,
                "cheatsheet_content.md may overflow target_pages using less-tested 4col heuristics: "
                f"{content_chars} chars > heuristic maximum {expected_max_chars}",
            )
        if healthy_range and content_text.strip() and content_chars < healthy_range[0]:
            add_warning(
                warnings,
                "cheatsheet_content.md is below the less-tested 4col healthy page-budget range: "
                f"{content_chars} chars < {healthy_range[0]}-{healthy_range[1]} chars "
                f"for {target_pages} page(s) in {layout}; use real evidence, not filler, if repairing",
            )

    topics = topic_count(content_text)
    if layout == "3col":
        minimum_topics = min_topic_count_for_pages(target_pages)
    elif target_pages <= 1:
        minimum_topics = 20
    elif target_pages == 2:
        minimum_topics = 35
    elif target_pages == 3:
        minimum_topics = 50
    else:
        minimum_topics = 50 + (target_pages - 3) * 12
    if topics < minimum_topics:
        add_warning(
            warnings,
            "topic count may be low for target_pages: "
            f"{topics} Topic lines < heuristic minimum {minimum_topics}",
        )

    candidates = candidate_unit_count(working_dir / "candidate_units.jsonl")
    ranked_topics = ranked_topic_count(importance_text)
    if candidates >= 100 and ranked_topics <= 20:
        add_warning(
            warnings,
            "possible over-compression: "
            f"{candidates} candidate units collapsed into {ranked_topics} ranked topics",
        )

    content_words = normalized_words(content_text)
    for label in a_topic_labels(importance_text):
        label_words = normalized_words(label)
        if label_words and not (label_words & content_words):
            add_warning(
                warnings,
                f"important A topic may be missing from cheatsheet_content.md: {label}",
            )


def validate_print_page_warnings(
    result: PrintPageResult,
    target_pages: int,
    print_scale: float,
    warnings: list[str],
) -> None:
    if result.skipped_reason:
        add_warning(
            warnings,
            "print-page validation skipped; falling back to column-based character thresholds: "
            f"{result.skipped_reason}",
        )
        return

    if result.actual_pages is None:
        add_warning(
            warnings,
            "print-page validation skipped; falling back to column-based character thresholds",
        )
        return

    if result.actual_pages < target_pages:
        add_warning(
            warnings,
            "actual printed-page underfill: "
            f"{result.actual_pages} page(s) < target_pages {target_pages} at print scale {print_scale}",
        )
    elif result.actual_pages > target_pages:
        add_warning(
            warnings,
            "actual printed-page overflow: "
            f"{result.actual_pages} page(s) > target_pages {target_pages} at print scale {print_scale}",
        )


def validate_coverage_warnings(
    working_dir: Path,
    records: dict[tuple[str, str], ExtractedRecord],
    knowledge_files: list[MaterialFile],
    mode: str,
    coverage_mode: str,
    content_text: str,
    warnings: list[str],
) -> None:
    candidate_units = working_dir / "candidate_units.jsonl"
    knowledge_units = working_dir / "knowledge_units.md"

    if mode == "full-auto":
        if not candidate_units.exists():
            add_warning(warnings, f"missing Full Auto candidate units: {candidate_units}")
        if not knowledge_units.exists():
            add_warning(warnings, f"missing Full Auto knowledge units: {knowledge_units}")

    validate_candidate_units_shape(candidate_units, warnings)

    pages = extracted_page_count(records)
    if pages > 200 and len(content_text) < 12000:
        add_warning(
            warnings,
            "output may under-cover course materials: extracted_pages > 200 and cheatsheet_content.md < 12000 chars",
        )

    major_knowledge_count = sum(
        1
        for record in records.values()
        if record.source_folder == "knowledge"
        and record_page_count(record) > 0
        and not is_administrative_source(record)
    )
    if major_knowledge_count > 5 and topic_count(content_text) < 20:
        add_warning(
            warnings,
            "topic count may be too low for the amount of material: major knowledge PDFs > 5 and final Topic count < 20",
        )

    if coverage_mode == "exam-compact" and pages > 300:
        add_warning(
            warnings,
            "exam-compact may be too aggressive for large courses with more than 300 extracted pages",
        )

    evidence_map = working_dir / "topic_evidence_map.md"
    if not evidence_map.exists():
        return
    source_topic_counts = count_source_topics(read_text(evidence_map))
    current_knowledge_names = {material.relative_path for material in knowledge_files}
    current_knowledge_names.update(Path(material.relative_path).name for material in knowledge_files)
    for record in records.values():
        if record.source_folder != "knowledge":
            continue
        if (
            record.relative_path not in current_knowledge_names
            and Path(record.relative_path).name not in current_knowledge_names
        ):
            continue
        page_count = record_page_count(record)
        if page_count <= 30 or is_administrative_source(record):
            continue
        represented_topics = source_topic_counts.get(record.source_id, 0)
        if represented_topics < 2:
            add_warning(
                warnings,
                f"possible source under-coverage: {record.source_id} `{record.relative_path}` has {page_count} pages but fewer than 2 final topics",
            )


def validate_course(
    course_name: str,
    root: Path,
    mode: str,
    layout: str,
    target_pages: int,
    coverage_mode: str,
    detail_mode: str,
    check_print_pages_enabled: bool = False,
    print_scale: float = DEFAULT_PRINT_SCALE,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    course_root = root / course_name
    materials = course_root / "materials"
    knowledge_dir = materials / "knowledge"
    questions_dir = materials / "questions"
    working_dir = course_root / "working"
    output_dir = course_root / "outputs"

    required_dirs = [course_root, knowledge_dir, questions_dir, working_dir]
    if mode == "full-auto":
        required_dirs.append(output_dir)
    for directory in required_dirs:
        if not directory.exists():
            add_error(errors, f"missing required directory: {directory}")

    knowledge_files = material_files(knowledge_dir, "knowledge")
    question_files = material_files(questions_dir, "questions")
    all_materials = knowledge_files + question_files
    if not knowledge_files:
        add_warning(warnings, "materials/knowledge has no files")
    if not question_files:
        add_warning(warnings, "materials/questions has no files")

    working_text = ""
    working_mtime = None
    for name in REQUIRED_WORKING_FILES:
        path = working_dir / name
        if not path.exists():
            add_error(errors, f"missing required working file: {path}")
            continue
        text = read_text(path)
        if not text.strip():
            add_error(errors, f"working file is empty: {path}")
        working_text += "\n" + text
        working_mtime = max(working_mtime or path.stat().st_mtime, path.stat().st_mtime)

    topic_map = working_dir / "topic_map.md"
    if topic_map.exists():
        topic_text = read_text(topic_map)
        for material in all_materials:
            if (
                Path(material.relative_path).name not in topic_text
                and material.relative_path not in topic_text
            ):
                add_error(
                    errors,
                    f"topic_map.md does not mention material source: {material.source_folder}/{material.relative_path}",
                )
        stale_names = re.findall(r"`([^`\n]{1,160})`", topic_text)
        material_names = {material.relative_path for material in all_materials} | {
            Path(material.relative_path).name for material in all_materials
        }
        for name in stale_names:
            suffix = Path(name).suffix.lower()
            if (
                suffix in SUPPORTED_EXTENSIONS
                and not name.startswith("working/")
                and name not in material_names
            ):
                add_warning(warnings, f"topic_map.md mentions non-current material file: {name}")

    if working_mtime is not None:
        newest_material = max([material.path.stat().st_mtime for material in all_materials] or [0])
        if newest_material > working_mtime:
            add_warning(warnings, "some materials are newer than the working artifacts")

    records = extracted_records(working_dir / "extracted", warnings)
    content_path = working_dir / "cheatsheet_content.md"
    content_text = read_text(content_path) if content_path.exists() else ""
    if content_text:
        validate_mojibake_warning(str(content_path), content_text, warnings)
    run_config_text = validate_run_config(
        working_dir=working_dir,
        mode=mode,
        layout=layout,
        target_pages=target_pages,
        coverage_mode=coverage_mode,
        detail_mode=detail_mode,
        errors=errors,
        warnings=warnings,
    )

    validate_mode_metadata(
        working_text + "\n" + run_config_text,
        mode,
        layout,
        target_pages,
        coverage_mode,
        detail_mode,
        warnings,
    )
    validate_coverage_warnings(
        working_dir=working_dir,
        records=records,
        knowledge_files=knowledge_files,
        mode=mode,
        coverage_mode=coverage_mode,
        content_text=content_text,
        warnings=warnings,
    )

    importance = working_dir / "importance_ranking.md"
    importance_text = ""
    if importance.exists():
        importance_text = read_text(importance)
        validate_importance_ranking(
            importance_text, question_files, records, errors, warnings
        )

    validate_evidence_map(working_dir, records, mode, errors, warnings)

    prediction_hits = contains_any(working_text, UNSUPPORTED_PREDICTIONS)
    if prediction_hits:
        add_error(errors, f"working files contain unsupported prediction language: {prediction_hits}")

    validate_extraction(all_materials, working_dir, working_text, mode, errors, warnings)

    if mode == "safe-review":
        if importance_text:
            validate_page_budget_warnings(
                working_dir=working_dir,
                layout=layout,
                target_pages=target_pages,
                content_text=content_text,
                importance_text=importance_text,
                actual_print_pages=None,
                warnings=warnings,
            )
        return errors, warnings

    validate_bilingual_topic_labels(content_text, warnings)
    for output_name, column_marker in REQUIRED_OUTPUTS:
        output_path = output_dir / output_name
        if not output_path.exists():
            add_error(errors, f"missing required HTML output: {output_path}")
            continue
        html = read_text(output_path)
        for marker in [
            "{{COURSE_NAME}}",
            "{{SOURCE_NOTE}}",
            "{{CONTENT_HTML}}",
            "{{GENERATED_AT}}",
        ]:
            if marker in html:
                add_error(errors, f"{output_path} still contains template marker {marker}")
        for marker in ["A4 landscape", column_marker, f"{course_name} cheatsheet"]:
            if marker not in html:
                add_error(errors, f"{output_path} missing rendered marker: {marker}")
        if "Topic Evidence Map" in html:
            add_error(errors, f"{output_path} should not include topic_evidence_map.md")
        if content_text:
            first_heading = next(
                (
                    line.lstrip("# ").strip()
                    for line in content_text.splitlines()
                    if line.startswith("#")
                ),
                "",
            )
            if first_heading and first_heading not in html:
                add_error(errors, f"{output_path} does not contain cheatsheet content heading")
        validate_mojibake_warning(str(output_path), html, warnings)

    print_result = PrintPageResult(None, None)
    if check_print_pages_enabled:
        print_result = check_print_pages(
            selected_html_output(output_dir, layout),
            print_scale,
        )
        validate_print_page_warnings(print_result, target_pages, print_scale, warnings)

    if importance_text:
        validate_page_budget_warnings(
            working_dir=working_dir,
            layout=layout,
            target_pages=target_pages,
            content_text=content_text,
            importance_text=importance_text,
            actual_print_pages=print_result.actual_pages,
            warnings=warnings,
        )

    return errors, warnings


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    skill_root = Path(__file__).resolve().parents[1]
    errors, warnings = validate_course(
        args.course_name,
        root,
        args.mode,
        args.layout,
        args.target_pages,
        args.coverage_mode,
        args.detail_mode,
        args.check_print_pages,
        args.print_scale,
    )
    validate_renderer_scope(skill_root, errors)

    for warning in warnings:
        print(warning)
    for error in errors:
        print(error)

    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"Validation passed: 0 error(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
