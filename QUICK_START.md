# Quick Start

Install `course-cheatsheet-maker` globally as a skill first. Keep real course materials in a separate course project.

## Recommended: Copy This Prompt To Codex

Beginners should use the agent prompt first instead of manually running all scripts blindly. The scripts do not replace the agent reasoning step: the agent still needs to inspect extracted material, infer source types, create rankings, and write `working/cheatsheet_content.md`.

Copy this prompt and replace `COURSE_NAME` with your course folder name:

```text
Use $course-cheatsheet-maker for COURSE_NAME.

My course materials are in:
courses/COURSE_NAME/materials/knowledge/
courses/COURSE_NAME/materials/questions/

Use full-auto mode.
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced

Please run extraction, build candidate units, create all required working artifacts, generate cheatsheet_content.md, render both HTML outputs, and run validation.
```

Important: `build_html.py` requires `working/cheatsheet_content.md` to already exist. It only renders prepared content; it does not analyze course materials or decide what should appear on the cheatsheet.

## 1. Create A Course Project

From your course project root, create:

```text
courses/COURSE_NAME/
  materials/
    knowledge/
    questions/
  working/
  outputs/
```

Put course knowledge sources in:

```text
courses/COURSE_NAME/materials/knowledge/
```

Put question-like sources in:

```text
courses/COURSE_NAME/materials/questions/
```

Examples of question-like sources include quizzes, assignments, tutorials, workshops, problem sets, sample exams, mock exams, and past papers.

## 2. Run From The Course Project Root

Use a `SKILL_DIR` variable so commands do not depend on where the skill repository was originally cloned.

Unix shell:

```bash
SKILL_DIR="$HOME/.agents/skills/course-cheatsheet-maker"

python "$SKILL_DIR/scripts/extract_materials.py" COURSE_NAME --root courses
python "$SKILL_DIR/scripts/build_candidate_units.py" COURSE_NAME --root courses
python "$SKILL_DIR/scripts/build_html.py" COURSE_NAME --root courses
python "$SKILL_DIR/scripts/validate_workflow.py" COURSE_NAME --root courses --mode full-auto --layout 3col --target-pages 1 --coverage-mode balanced-standard --detail-mode balanced
```

Windows PowerShell:

```powershell
$env:SKILL_DIR="$HOME\.agents\skills\course-cheatsheet-maker"

python "$env:SKILL_DIR\scripts\extract_materials.py" COURSE_NAME --root courses
python "$env:SKILL_DIR\scripts\build_candidate_units.py" COURSE_NAME --root courses
python "$env:SKILL_DIR\scripts\build_html.py" COURSE_NAME --root courses
python "$env:SKILL_DIR\scripts\validate_workflow.py" COURSE_NAME --root courses --mode full-auto --layout 3col --target-pages 1 --coverage-mode balanced-standard --detail-mode balanced
```

The agent still performs the course reasoning steps. The scripts handle extraction, deterministic candidate-unit building, rendering, and validation.

## 3. Expected Working Artifacts

Before rendering, a real course workflow should create or verify:

```text
courses/COURSE_NAME/working/extracted/
courses/COURSE_NAME/working/extraction_report.md
courses/COURSE_NAME/working/candidate_units.jsonl
courses/COURSE_NAME/working/knowledge_units.md
courses/COURSE_NAME/working/topic_map.md
courses/COURSE_NAME/working/importance_ranking.md
courses/COURSE_NAME/working/topic_evidence_map.md
courses/COURSE_NAME/working/cheatsheet_content.md
```

Full Auto rendering writes:

```text
courses/COURSE_NAME/outputs/cheatsheet_3col.html
courses/COURSE_NAME/outputs/cheatsheet_4col.html
```

## 4. Keep Public Repositories Clean

Do not commit copyrighted course materials, extracted course text, private working artifacts, rendered HTML outputs, or exported PDFs into this skill repository.
