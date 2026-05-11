"""Print manual PDF export guidance for a cheatsheet HTML file.

PDF generation stays lightweight in v1. Use the browser print dialog so the
HTML/CSS remains the source of truth and no Playwright dependency is required.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show recommended browser settings for exporting cheatsheet HTML to PDF."
    )
    parser.add_argument("html_path", help="Path to cheatsheet_3col.html or cheatsheet_4col.html.")
    return parser.parse_args()


def suggested_pdf_path(html_path: Path) -> Path:
    return html_path.with_suffix(".pdf")


def main() -> int:
    args = parse_args()
    html_path = Path(args.html_path).resolve()

    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}")
        return 2

    if html_path.suffix.lower() not in {".html", ".htm"}:
        print(f"ERROR: Expected an HTML file, got: {html_path}")
        return 2

    print(f"HTML source: {html_path}")
    print(f"Suggested PDF target: {suggested_pdf_path(html_path)}")
    print("")
    print("Recommended browser print settings:")
    print("- Paper size: A4")
    print("- Orientation: Landscape")
    print("- Background graphics: Enabled")
    print("- Margins: Default or Minimum")
    print("- Scale: 100% first; reduce slightly only if content clips")
    print("")
    print("Playwright automation can be added later, but v1 intentionally has no browser dependency.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
