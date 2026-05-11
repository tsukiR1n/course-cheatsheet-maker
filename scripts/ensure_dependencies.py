"""Ensure optional extraction dependencies are available for this interpreter."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


NO_AUTO_INSTALL_ENV = "COURSE_CHEATSHEET_NO_AUTO_INSTALL"


@dataclass(frozen=True)
class Dependency:
    package: str
    import_name: str


DEPENDENCIES = [
    Dependency(package="pymupdf", import_name="fitz"),
    Dependency(package="python-pptx", import_name="pptx"),
    Dependency(package="python-docx", import_name="docx"),
]


def is_available(import_name: str) -> bool:
    return importlib.util.find_spec(import_name) is not None


def requirements_path() -> Path:
    return Path(__file__).resolve().parents[1] / "requirements.txt"


def main() -> int:
    print(f"Dependency check using Python: {sys.executable}")

    missing: list[Dependency] = []
    for dependency in DEPENDENCIES:
        if is_available(dependency.import_name):
            print(f"available: {dependency.package} (import `{dependency.import_name}`)")
        else:
            print(f"missing: {dependency.package} (import `{dependency.import_name}`)")
            missing.append(dependency)

    if not missing:
        print("All extraction dependencies are available.")
        return 0

    if os.environ.get(NO_AUTO_INSTALL_ENV) == "1":
        print(
            f"Automatic dependency installation skipped because {NO_AUTO_INSTALL_ENV}=1."
        )
        print("Extraction will continue with graceful missing-dependency failures.")
        return 0

    req_path = requirements_path()
    command = [sys.executable, "-m", "pip", "install", "-r", str(req_path)]
    print("Installing missing extraction dependencies:")
    print(" ".join(command))

    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"Dependency installation failed with exit code {result.returncode}.")
        return result.returncode

    still_missing = [
        dependency
        for dependency in DEPENDENCIES
        if not is_available(dependency.import_name)
    ]
    if still_missing:
        names = ", ".join(
            f"{dependency.package} (import `{dependency.import_name}`)"
            for dependency in still_missing
        )
        print(f"Dependency installation completed, but imports are still missing: {names}")
        return 1

    print("Dependency installation succeeded; all extraction dependencies are available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
