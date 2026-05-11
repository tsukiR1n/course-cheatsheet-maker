# course-cheatsheet-maker

An installable Codex-style skill for creating compact A4 landscape course cheatsheets from course materials.

The skill helps an agent:

- extract text from course materials;
- build traceable candidate units;
- infer topic importance from knowledge sources and question-like sources;
- prepare review artifacts;
- render 3-column and 4-column printable HTML cheatsheets.

HTML/CSS is the source of truth. PDF export is optional and should preserve the printed HTML layout.

## Installable Skill Repository

This repository is meant to be installed as a skill, either globally or inside a project skills folder. The installed skill directory must contain `SKILL.md` directly:

```text
course-cheatsheet-maker/
  SKILL.md
  requirements.txt
  scripts/
  assets/
  references/
```

For Codex-style setups, a typical global install location is:

```text
~/.agents/skills/course-cheatsheet-maker/
```

See `INSTALL.md` for installation and validation steps.

## Beginner Flow

1. Install the skill using `INSTALL.md`.
2. Create a separate course project.
3. Put course materials into `courses/COURSE_NAME/materials/knowledge/` and `courses/COURSE_NAME/materials/questions/`.
4. Ask Codex to use `$course-cheatsheet-maker`.
5. Check rendered HTML in `courses/COURSE_NAME/outputs/`.

## Where Course Materials Go

Do not put real course materials in this public skill repository.

The skill should be installed globally or into a separate project skills folder. Your actual course materials should live in your own course project, using this structure:

```text
courses/COURSE_NAME/
  materials/
    knowledge/
    questions/
  working/
  outputs/
```

Put lecture notes, slides, textbooks excerpts, and other knowledge sources under `materials/knowledge/`. Put quizzes, assignments, tutorials, workshops, problem sets, sample exams, and past-paper-like materials under `materials/questions/`.

Subfolders inside `knowledge/` and `questions/` are supported.

## Important Copyright Note

Do not commit copyrighted course materials, extracted course text, generated working files based on private materials, or rendered course outputs into this public skill repository. Keep real course projects private unless you have permission to publish the source materials and generated derivatives.

The `examples/` directory contains only empty placeholders showing the expected course folder shape.

## Quick Start

After installing the skill, create a separate course project and run the scripts from that project root, or pass `--root` explicitly. See `QUICK_START.md` for Unix and Windows PowerShell examples.

## Requirements

Python 3.9+ is recommended.

Optional extraction dependencies are listed in `requirements.txt`:

```text
pymupdf
python-pptx
python-docx
```

OCR is intentionally out of scope. Scanned PDFs with no selectable text will be reported as having no selectable text.

## License

MIT License. See `LICENSE`.
