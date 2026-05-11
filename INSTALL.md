# Install

This repository is an installable Codex-style skill. Install it so the final folder contains `SKILL.md` directly.

The release install intentionally includes both:

1. the reusable skill files used by Codex or another agent; and
2. the bundled empty `courses/COURSE_NAME` starter scaffold.

The installed skill folder must include the bundled empty `courses/COURSE_NAME` scaffold. It is included so new users do not need to manually create the required course folders before their first run.

## For Humans

If you want Codex or another coding agent to install this skill for you, copy and paste this prompt:

```text
Install and validate the course-cheatsheet-maker skill by following this guide:
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/INSTALL.md
```

## Repository And Raw Files
Because this skill includes required folders such as scripts/, assets/, references/, and courses/, agents should clone or download the full repository whenever possible. Installing only individual raw files is not sufficient for a complete install.

Expected public repository:

```text
https://github.com/tsukiR1n/course-cheatsheet-maker
```

Raw entry files:

```text
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/SKILL.md
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/requirements.txt
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/README.md
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/QUICK_START.md
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/INSTALL.md
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/LICENSE
```

Agents should download or copy these files and folders into:

```text
~/.agents/skills/course-cheatsheet-maker/
```

Required folders to copy:

```text
scripts/
assets/
references/
courses/
```

Recommended installed files, if present:

```text
README.md
QUICK_START.md
INSTALL.md
LICENSE
```

If the final GitHub repository location changes, use the same folder layout and keep `SKILL.md` directly inside the installed skill directory.

## Agent Installation Target

For Codex-style setups, install this repository into:

```text
~/.agents/skills/course-cheatsheet-maker/
```

The installed folder must look like:

```text
~/.agents/skills/course-cheatsheet-maker/
  SKILL.md
  README.md
  QUICK_START.md
  INSTALL.md
  LICENSE
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

`courses/COURSE_NAME` is a bundled empty starter scaffold and should be installed with the skill. It is a template included for user convenience, not a real course name and not a place to commit real course materials. Users can copy or rename it for actual private courses, such as `courses/COMP7503` or `courses/MATH101`.

Real course materials should not be committed to a public repository.

Do not install the repository one level too deep. For example, this is wrong:

```text
~/.agents/skills/course-cheatsheet-maker/course-cheatsheet-maker/SKILL.md
```

## Dependencies

Install optional extraction dependencies with:

```bash
python -m pip install -r ~/.agents/skills/course-cheatsheet-maker/requirements.txt
```

The extraction script can also check and install missing optional dependencies automatically unless `COURSE_CHEATSHEET_NO_AUTO_INSTALL=1` is set.

## Validation

After installation, validate the skill layout:

```bash
SKILL_DIR="$HOME/.agents/skills/course-cheatsheet-maker"
test -f "$SKILL_DIR/SKILL.md"
test -d "$SKILL_DIR/scripts"
test -d "$SKILL_DIR/assets"
test -d "$SKILL_DIR/references"
test -d "$SKILL_DIR/courses"
test -d "$SKILL_DIR/courses/COURSE_NAME"
test -d "$SKILL_DIR/courses/COURSE_NAME/materials/knowledge"
test -d "$SKILL_DIR/courses/COURSE_NAME/materials/questions"
test -d "$SKILL_DIR/courses/COURSE_NAME/working"
test -d "$SKILL_DIR/courses/COURSE_NAME/outputs"
python -m py_compile "$SKILL_DIR"/scripts/*.py
```

Windows PowerShell:

```powershell
$env:SKILL_DIR="$HOME\.agents\skills\course-cheatsheet-maker"
Test-Path "$env:SKILL_DIR\SKILL.md"
Test-Path "$env:SKILL_DIR\scripts"
Test-Path "$env:SKILL_DIR\assets"
Test-Path "$env:SKILL_DIR\references"
Test-Path "$env:SKILL_DIR\courses"
Test-Path "$env:SKILL_DIR\courses\COURSE_NAME"
Test-Path "$env:SKILL_DIR\courses\COURSE_NAME\materials\knowledge"
Test-Path "$env:SKILL_DIR\courses\COURSE_NAME\materials\questions"
Test-Path "$env:SKILL_DIR\courses\COURSE_NAME\working"
Test-Path "$env:SKILL_DIR\courses\COURSE_NAME\outputs"
python -m py_compile "$env:SKILL_DIR\scripts\build_candidate_units.py" "$env:SKILL_DIR\scripts\build_html.py" "$env:SKILL_DIR\scripts\ensure_dependencies.py" "$env:SKILL_DIR\scripts\export_pdf.py" "$env:SKILL_DIR\scripts\extract_materials.py" "$env:SKILL_DIR\scripts\validate_workflow.py"
```

If compilation fails, fix the installation before using the skill.
