# Install

This is the authoritative installation guide for Codex and other coding agents.

Install `course-cheatsheet-maker` as a clean runtime skill package. Do not copy the whole repository into the installed skill folder. Instead, clone or download the repository to a temporary source folder, then copy only the runtime allowlist into:

```text
~/.agents/skills/course-cheatsheet-maker/
```

## Runtime Allowlist

Copy exactly these files and folders into the installed skill folder:

```text
SKILL.md
requirements.txt
scripts/
assets/
references/
courses/
```

Keep `courses/COURSE_NAME/` because it is the starter scaffold required for first-time users.

Hidden `.gitkeep` files inside `courses/COURSE_NAME/` are allowed. They only keep empty starter scaffold folders tracked by Git; they are not real course materials and do not count as generated outputs.

Do not copy:

```text
README.md
QUICK_START.md
INSTALL.md
LICENSE
.gitignore
.git/
__pycache__/
real course materials
generated working/ or outputs/ from real courses
```

Repository docs such as `README.md`, `QUICK_START.md`, and `INSTALL.md` are useful in GitHub, but they are not part of the installed runtime skill folder.

## Expected Installed Folder

The final installed folder must look like this:

```text
~/.agents/skills/course-cheatsheet-maker/
  SKILL.md
  requirements.txt
  scripts/
  assets/
  references/
  courses/
    COURSE_NAME/
      materials/
        knowledge/
        questions/
      working/
      outputs/
```

`courses/COURSE_NAME/` is a starter scaffold, not a real course. Users should copy it into their own private course project, for example `courses/COMP7503/`, before adding real materials.

Do not install the repository one level too deep. This layout is wrong:

```text
~/.agents/skills/course-cheatsheet-maker/course-cheatsheet-maker/SKILL.md
```

`SKILL.md` must be directly inside:

```text
~/.agents/skills/course-cheatsheet-maker/SKILL.md
```

## Install On macOS / Linux / Git Bash

These commands clone the repository to a temporary folder, copy only the runtime allowlist, remove accidental `__pycache__/` folders, and validate the final layout.

```bash
set -euo pipefail

REPO_URL="https://github.com/tsukiR1n/course-cheatsheet-maker.git"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
SRC_DIR="$TMP_DIR/course-cheatsheet-maker"
INSTALL_DIR="$HOME/.agents/skills/course-cheatsheet-maker"

git clone "$REPO_URL" "$SRC_DIR"

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

cp "$SRC_DIR/SKILL.md" "$INSTALL_DIR/"
cp "$SRC_DIR/requirements.txt" "$INSTALL_DIR/"
cp -R "$SRC_DIR/scripts" "$INSTALL_DIR/"
cp -R "$SRC_DIR/assets" "$INSTALL_DIR/"
cp -R "$SRC_DIR/references" "$INSTALL_DIR/"
cp -R "$SRC_DIR/courses" "$INSTALL_DIR/"

python -m py_compile "$INSTALL_DIR"/scripts/*.py

find "$INSTALL_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +

test -f "$INSTALL_DIR/SKILL.md"
test -f "$INSTALL_DIR/requirements.txt"
test -d "$INSTALL_DIR/scripts"
test -d "$INSTALL_DIR/assets"
test -d "$INSTALL_DIR/references"
test -d "$INSTALL_DIR/courses"
test -d "$INSTALL_DIR/courses/COURSE_NAME"
test -d "$INSTALL_DIR/courses/COURSE_NAME/materials/knowledge"
test -d "$INSTALL_DIR/courses/COURSE_NAME/materials/questions"
test -d "$INSTALL_DIR/courses/COURSE_NAME/working"
test -d "$INSTALL_DIR/courses/COURSE_NAME/outputs"

test ! -e "$INSTALL_DIR/README.md"
test ! -e "$INSTALL_DIR/QUICK_START.md"
test ! -e "$INSTALL_DIR/INSTALL.md"
test ! -e "$INSTALL_DIR/LICENSE"
test ! -e "$INSTALL_DIR/.gitignore"
test ! -e "$INSTALL_DIR/.git"
test ! -e "$INSTALL_DIR/course-cheatsheet-maker/SKILL.md"
test -z "$(find "$INSTALL_DIR" -type d -name "__pycache__" -print -quit)"

echo "course-cheatsheet-maker installed cleanly at $INSTALL_DIR"
```

## Install On Windows PowerShell

These commands do the same clean allowlist installation on Windows.

```powershell
$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/tsukiR1n/course-cheatsheet-maker.git"
$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("course-cheatsheet-maker-install-" + [System.Guid]::NewGuid().ToString("N"))
$SourceDir = Join-Path $TempRoot "course-cheatsheet-maker"
$InstallDir = Join-Path $HOME ".agents\skills\course-cheatsheet-maker"

git clone $RepoUrl $SourceDir

if (Test-Path $InstallDir) {
  Remove-Item -LiteralPath $InstallDir -Recurse -Force
}
New-Item -ItemType Directory -Force $InstallDir | Out-Null

Copy-Item -LiteralPath (Join-Path $SourceDir "SKILL.md") -Destination $InstallDir
Copy-Item -LiteralPath (Join-Path $SourceDir "requirements.txt") -Destination $InstallDir
Copy-Item -LiteralPath (Join-Path $SourceDir "scripts") -Destination $InstallDir -Recurse
Copy-Item -LiteralPath (Join-Path $SourceDir "assets") -Destination $InstallDir -Recurse
Copy-Item -LiteralPath (Join-Path $SourceDir "references") -Destination $InstallDir -Recurse
Copy-Item -LiteralPath (Join-Path $SourceDir "courses") -Destination $InstallDir -Recurse

python -m py_compile `
  (Join-Path $InstallDir "scripts\build_candidate_units.py") `
  (Join-Path $InstallDir "scripts\build_html.py") `
  (Join-Path $InstallDir "scripts\ensure_dependencies.py") `
  (Join-Path $InstallDir "scripts\export_pdf.py") `
  (Join-Path $InstallDir "scripts\extract_materials.py") `
  (Join-Path $InstallDir "scripts\validate_workflow.py")

Get-ChildItem -LiteralPath $InstallDir -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  Remove-Item -Recurse -Force

$RequiredPaths = @(
  "SKILL.md",
  "requirements.txt",
  "scripts",
  "assets",
  "references",
  "courses",
  "courses\COURSE_NAME",
  "courses\COURSE_NAME\materials\knowledge",
  "courses\COURSE_NAME\materials\questions",
  "courses\COURSE_NAME\working",
  "courses\COURSE_NAME\outputs"
)

foreach ($Path in $RequiredPaths) {
  $FullPath = Join-Path $InstallDir $Path
  if (-not (Test-Path $FullPath)) {
    throw "Missing required path: $FullPath"
  }
}

$ForbiddenPaths = @(
  "README.md",
  "QUICK_START.md",
  "INSTALL.md",
  "LICENSE",
  ".gitignore",
  ".git",
  "course-cheatsheet-maker\SKILL.md"
)

foreach ($Path in $ForbiddenPaths) {
  $FullPath = Join-Path $InstallDir $Path
  if (Test-Path $FullPath) {
    throw "Repository-only or nested path should not be installed: $FullPath"
  }
}

$PycacheDir = Get-ChildItem -LiteralPath $InstallDir -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  Select-Object -First 1
if ($PycacheDir) {
  throw "__pycache__ directory should not be installed: $($PycacheDir.FullName)"
}

Remove-Item -LiteralPath $TempRoot -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "course-cheatsheet-maker installed cleanly at $InstallDir"
```

## Optional Python Dependencies

Basic installation is fast because Python extraction dependencies are optional.

Install them only when you want full PDF, PPTX, and DOCX extraction support:

```bash
python -m pip install -r ~/.agents/skills/course-cheatsheet-maker/requirements.txt
```

Windows PowerShell:

```powershell
python -m pip install -r "$HOME\.agents\skills\course-cheatsheet-maker\requirements.txt"
```

The extraction script may also check dependencies during use. OCR is not included.

## Standalone Validation

Run this any time you want to verify an existing installation.

macOS / Linux / Git Bash:

```bash
set -euo pipefail

INSTALL_DIR="$HOME/.agents/skills/course-cheatsheet-maker"

python -m py_compile "$INSTALL_DIR"/scripts/*.py

find "$INSTALL_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +

test -f "$INSTALL_DIR/SKILL.md"
test -f "$INSTALL_DIR/requirements.txt"
test -d "$INSTALL_DIR/scripts"
test -d "$INSTALL_DIR/assets"
test -d "$INSTALL_DIR/references"
test -d "$INSTALL_DIR/courses"
test -d "$INSTALL_DIR/courses/COURSE_NAME"
test -d "$INSTALL_DIR/courses/COURSE_NAME/materials/knowledge"
test -d "$INSTALL_DIR/courses/COURSE_NAME/materials/questions"
test -d "$INSTALL_DIR/courses/COURSE_NAME/working"
test -d "$INSTALL_DIR/courses/COURSE_NAME/outputs"

test ! -e "$INSTALL_DIR/README.md"
test ! -e "$INSTALL_DIR/QUICK_START.md"
test ! -e "$INSTALL_DIR/INSTALL.md"
test ! -e "$INSTALL_DIR/LICENSE"
test ! -e "$INSTALL_DIR/.gitignore"
test ! -e "$INSTALL_DIR/.git"
test ! -e "$INSTALL_DIR/course-cheatsheet-maker/SKILL.md"
test -z "$(find "$INSTALL_DIR" -type d -name "__pycache__" -print -quit)"

echo "Validation passed."
```

Windows PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$InstallDir = Join-Path $HOME ".agents\skills\course-cheatsheet-maker"

python -m py_compile `
  (Join-Path $InstallDir "scripts\build_candidate_units.py") `
  (Join-Path $InstallDir "scripts\build_html.py") `
  (Join-Path $InstallDir "scripts\ensure_dependencies.py") `
  (Join-Path $InstallDir "scripts\export_pdf.py") `
  (Join-Path $InstallDir "scripts\extract_materials.py") `
  (Join-Path $InstallDir "scripts\validate_workflow.py")

Get-ChildItem -LiteralPath $InstallDir -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  Remove-Item -Recurse -Force

$RequiredPaths = @(
  "SKILL.md",
  "requirements.txt",
  "scripts",
  "assets",
  "references",
  "courses",
  "courses\COURSE_NAME",
  "courses\COURSE_NAME\materials\knowledge",
  "courses\COURSE_NAME\materials\questions",
  "courses\COURSE_NAME\working",
  "courses\COURSE_NAME\outputs"
)

foreach ($Path in $RequiredPaths) {
  $FullPath = Join-Path $InstallDir $Path
  if (-not (Test-Path $FullPath)) {
    throw "Missing required path: $FullPath"
  }
}

$ForbiddenPaths = @(
  "README.md",
  "QUICK_START.md",
  "INSTALL.md",
  "LICENSE",
  ".gitignore",
  ".git",
  "course-cheatsheet-maker\SKILL.md"
)

foreach ($Path in $ForbiddenPaths) {
  $FullPath = Join-Path $InstallDir $Path
  if (Test-Path $FullPath) {
    throw "Repository-only or nested path should not be installed: $FullPath"
  }
}

$PycacheDir = Get-ChildItem -LiteralPath $InstallDir -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  Select-Object -First 1
if ($PycacheDir) {
  throw "__pycache__ directory should not be installed: $($PycacheDir.FullName)"
}

Write-Host "Validation passed."
```

If validation fails, fix the installed folder before using the skill. The most common problem is copying the whole repository instead of copying only the runtime allowlist.
