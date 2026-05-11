# Quick Start / 快速开始

[中文](#中文) | [English](#english)

---

## 中文

`course-cheatsheet-maker` 是一个可安装的 Codex-style skill，用于根据课程材料生成 A4 横版课程 cheatsheet。

这个 Quick Start 面向第一次使用的新用户。你只需要完成三件事：

1. 安装 skill；
2. 准备课程材料；
3. 复制使用 prompt 给 Codex。

---

## 1. 安装 Skill

请先把下面这段话复制给 Codex / 支持 skills 的 Agent：

```text
Install and validate the course-cheatsheet-maker skill by following this guide:
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/INSTALL.md
```

安装成功后，本地通常会出现这个目录：

```text
~/.agents/skills/course-cheatsheet-maker/
  SKILL.md
  requirements.txt
  scripts/
  assets/
  references/
```

Windows 上通常对应：

```text
C:\Users\<你的用户名>\.agents\skills\course-cheatsheet-maker\
```

注意：  
这个目录是 skill 的安装位置，不是你放课程材料的地方。

---

## 2. 创建课程项目

请新建一个单独的课程项目，例如：

```text
my-course-project/
  courses/
    COURSE_NAME/
      materials/
        knowledge/
        questions/
      working/
      outputs/
```

其中 `COURSE_NAME` 是你的课程文件夹名，可以改成真实课程名，例如：

```text
COMP7503
MATH101
DATABASE
```

例如：

```text
my-course-project/
  courses/
    COMP7503/
      materials/
        knowledge/
        questions/
      working/
      outputs/
```

---

## 3. 准备课程材料

把课程知识类材料放入：

```text
courses/COURSE_NAME/materials/knowledge/
```

适合放在 `knowledge/` 的材料包括：

```text
lecture slides
lecture notes
course handouts
textbook excerpts
tutorial explanations
review notes
```

把题目类材料放入：

```text
courses/COURSE_NAME/materials/questions/
```

适合放在 `questions/` 的材料包括：

```text
quiz
assignment
tutorial questions
workshop questions
problem sets
sample exams
mock exams
past papers
```

示例：

```text
courses/COMP7503/materials/knowledge/week01_slides.pdf
courses/COMP7503/materials/knowledge/week02_notes.pdf
courses/COMP7503/materials/questions/past_paper_2024.pdf
courses/COMP7503/materials/questions/workshop_03.pdf
```

不要把真实课程材料放进这个 skill 仓库。  
真实课程材料应该放在你自己的课程项目里。

---

## 4. 参数说明

你可以在 prompt 中调整以下参数。

| 参数 | 推荐默认值 | 说明 |
|---|---|---|
| `workflow_mode` | `full-auto` | 工作流模式。`full-auto` 表示自动完成提取、分析、生成和验证；`safe-review` 更适合想先检查中间分析结果再继续的情况。 |
| `layout` | `3col` | 输出版式。`3col` 是默认三栏 A4 横版；`4col` 更紧凑，但可读性可能下降。 |
| `target_pages` | `1` | 目标页数。可以设为 `1`、`2`、`3` 等。页数越少，压缩越强。 |
| `coverage_mode` | `balanced-standard` | 内容覆盖策略。新手建议使用 `balanced-standard`，在覆盖面和压缩度之间较平衡。 |
| `detail_mode` | `balanced` | topic 细节程度。新手建议使用 `balanced`。 |

新手推荐先使用这一组默认配置：

```text
workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced
```

如果你想要更完整的复习材料，可以把 `target_pages` 改成 `2` 或 `3`。

---

## 5. 使用 Skill 生成 Cheatsheet

在你的课程项目根目录打开 Codex。

也就是说，你应该在这个目录下打开 Codex：

```text
my-course-project/
```

然后复制下面这个 prompt 给 Codex。

请把 `COURSE_NAME` 替换成你的课程文件夹名：

```text
Use $course-cheatsheet-maker for COURSE_NAME.

My course materials are in:
courses/COURSE_NAME/materials/knowledge/
courses/COURSE_NAME/materials/questions/

workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced

Please run extraction, build candidate units, create all required working artifacts, generate cheatsheet_content.md, render both HTML outputs, and run validation.
```

例如，如果你的课程文件夹叫 `COMP7503`，就改成：

```text
Use $course-cheatsheet-maker for COMP7503.

My course materials are in:
courses/COMP7503/materials/knowledge/
courses/COMP7503/materials/questions/

workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced

Please run extraction, build candidate units, create all required working artifacts, generate cheatsheet_content.md, render both HTML outputs, and run validation.
```

---

## 6. 查看输出结果

生成结果会出现在：

```text
courses/COURSE_NAME/outputs/
```

通常会生成：

```text
courses/COURSE_NAME/outputs/cheatsheet_3col.html
courses/COURSE_NAME/outputs/cheatsheet_4col.html
```

其中：

- `cheatsheet_3col.html`：默认推荐版本，三栏 A4 横版；
- `cheatsheet_4col.html`：更紧凑版本，适合内容较多但可读性可能更低。

中间分析文件会出现在：

```text
courses/COURSE_NAME/working/
```

常见中间文件包括：

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

---

## 7. 导出 PDF

本 skill 的主要输出是 HTML。  
你可以用浏览器打开：

```text
courses/COURSE_NAME/outputs/cheatsheet_3col.html
```

然后使用浏览器打印功能导出 PDF：

```text
Ctrl + P / Cmd + P
Save as PDF
Paper size: A4
Layout: Landscape
Margins: None or Minimum
Background graphics: On
```

建议优先导出 `cheatsheet_3col.html`，因为它通常更稳定、更易读。

---

## 8. 常见误区

### 误区 1：直接运行 `build_html.py` 就能自动生成 cheatsheet

不可以。

`build_html.py` 只负责把已经写好的：

```text
working/cheatsheet_content.md
```

渲染成 HTML。

它不会自动分析课程材料，也不会自动决定哪些内容应该放进 cheatsheet。

真正的材料理解、topic ranking、内容筛选、压缩和 `cheatsheet_content.md` 写作，需要由 Codex 按照 `$course-cheatsheet-maker` 的工作流完成。

### 误区 2：把课程材料放进 skill 仓库

不要这样做。

skill 仓库只放 skill 本身：

```text
SKILL.md
scripts/
assets/
references/
```

你的课程材料应该放在自己的课程项目里：

```text
my-course-project/courses/COURSE_NAME/materials/
```

### 误区 3：在错误的目录打开 Codex

请在课程项目根目录打开 Codex，而不是在 skill 仓库里打开。

正确：

```text
my-course-project/
```

不推荐：

```text
~/.agents/skills/course-cheatsheet-maker/
```

---

## 9. Advanced: Manual Script Commands

新手一般不需要手动运行这些命令。  
推荐先使用上面的 Codex prompt。

下面的命令主要适合调试或高级用户。

这些脚本不会替代 Agent 的推理步骤。尤其是 `build_html.py` 要求 `working/cheatsheet_content.md` 已经存在。

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

---

## English

`course-cheatsheet-maker` is an installable Codex-style skill for creating compact A4 landscape course cheatsheets from course materials.

This Quick Start is for first-time users. You only need to do three things:

1. install the skill;
2. prepare your course materials;
3. copy the usage prompt to Codex.

---

## 1. Install The Skill

First, copy this prompt to Codex or another Agent that supports skills:

```text
Install and validate the course-cheatsheet-maker skill by following this guide:
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/INSTALL.md
```

After installation, you should typically have:

```text
~/.agents/skills/course-cheatsheet-maker/
  SKILL.md
  requirements.txt
  scripts/
  assets/
  references/
```

On Windows, this usually corresponds to:

```text
C:\Users\<your-username>\.agents\skills\course-cheatsheet-maker\
```

Important:  
This is the skill installation directory. It is not where you should put your course materials.

---

## 2. Create A Course Project

Create a separate course project, for example:

```text
my-course-project/
  courses/
    COURSE_NAME/
      materials/
        knowledge/
        questions/
      working/
      outputs/
```

`COURSE_NAME` is your course folder name. You can replace it with a real course name, such as:

```text
COMP7503
MATH101
DATABASE
```

Example:

```text
my-course-project/
  courses/
    COMP7503/
      materials/
        knowledge/
        questions/
      working/
      outputs/
```

---

## 3. Prepare Course Materials

Put course knowledge sources in:

```text
courses/COURSE_NAME/materials/knowledge/
```

Good sources for `knowledge/` include:

```text
lecture slides
lecture notes
course handouts
textbook excerpts
tutorial explanations
review notes
```

Put question-like sources in:

```text
courses/COURSE_NAME/materials/questions/
```

Good sources for `questions/` include:

```text
quiz
assignment
tutorial questions
workshop questions
problem sets
sample exams
mock exams
past papers
```

Example:

```text
courses/COMP7503/materials/knowledge/week01_slides.pdf
courses/COMP7503/materials/knowledge/week02_notes.pdf
courses/COMP7503/materials/questions/past_paper_2024.pdf
courses/COMP7503/materials/questions/workshop_03.pdf
```

Do not put real course materials into this skill repository.  
Real course materials should live in your own course project.

---

## 4. Parameters

You can adjust these parameters in the prompt.

| Parameter | Recommended Default | Meaning |
|---|---|---|
| `workflow_mode` | `full-auto` | Workflow mode. `full-auto` runs extraction, analysis, rendering, and validation automatically. `safe-review` is better if you want to review intermediate artifacts before final rendering. |
| `layout` | `3col` | Output layout. `3col` is the default A4 landscape three-column layout. `4col` is denser but may be less readable. |
| `target_pages` | `1` | Target page count, such as `1`, `2`, or `3`. Fewer pages means stronger compression. |
| `coverage_mode` | `balanced-standard` | Coverage strategy. Beginners should use `balanced-standard` for a balanced tradeoff between coverage and compression. |
| `detail_mode` | `balanced` | Detail level per topic. Beginners should use `balanced`. |

Recommended beginner defaults:

```text
workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced
```

If you want a more complete review sheet, set `target_pages` to `2` or `3`.

---

## 5. Use The Skill To Generate A Cheatsheet

Open Codex from your course project root.

That means you should open Codex in:

```text
my-course-project/
```

Then copy this prompt to Codex.

Replace `COURSE_NAME` with your actual course folder name:

```text
Use $course-cheatsheet-maker for COURSE_NAME.

My course materials are in:
courses/COURSE_NAME/materials/knowledge/
courses/COURSE_NAME/materials/questions/

workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced

Please run extraction, build candidate units, create all required working artifacts, generate cheatsheet_content.md, render both HTML outputs, and run validation.
```

For example, if your course folder is `COMP7503`, use:

```text
Use $course-cheatsheet-maker for COMP7503.

My course materials are in:
courses/COMP7503/materials/knowledge/
courses/COMP7503/materials/questions/

workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced

Please run extraction, build candidate units, create all required working artifacts, generate cheatsheet_content.md, render both HTML outputs, and run validation.
```

---

## 6. Check The Outputs

Rendered outputs will appear in:

```text
courses/COURSE_NAME/outputs/
```

Usually, the skill generates:

```text
courses/COURSE_NAME/outputs/cheatsheet_3col.html
courses/COURSE_NAME/outputs/cheatsheet_4col.html
```

Meaning:

- `cheatsheet_3col.html`: recommended default output, A4 landscape with three columns;
- `cheatsheet_4col.html`: denser output, useful for more content but potentially less readable.

Intermediate artifacts will appear in:

```text
courses/COURSE_NAME/working/
```

Common working artifacts include:

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

---

## 7. Export To PDF

The main output of this skill is HTML.  
You can open:

```text
courses/COURSE_NAME/outputs/cheatsheet_3col.html
```

Then export it through your browser’s print dialog:

```text
Ctrl + P / Cmd + P
Save as PDF
Paper size: A4
Layout: Landscape
Margins: None or Minimum
Background graphics: On
```

`cheatsheet_3col.html` is usually the recommended export target because it is more stable and readable.

---

## 8. Common Mistakes

### Mistake 1: Expecting `build_html.py` to generate the cheatsheet by itself

It cannot.

`build_html.py` only renders an existing:

```text
working/cheatsheet_content.md
```

into HTML.

It does not analyze course materials or decide what should appear on the cheatsheet.

Material understanding, topic ranking, content selection, compression, and `cheatsheet_content.md` writing must be done by Codex following the `$course-cheatsheet-maker` workflow.

### Mistake 2: Putting course materials into the skill repository

Do not do this.

The skill repository should only contain the skill itself:

```text
SKILL.md
scripts/
assets/
references/
```

Your course materials should live in your own course project:

```text
my-course-project/courses/COURSE_NAME/materials/
```

### Mistake 3: Opening Codex from the wrong directory

Open Codex from your course project root, not from the skill repository.

Correct:

```text
my-course-project/
```

Not recommended:

```text
~/.agents/skills/course-cheatsheet-maker/
```

---

## 9. Advanced: Manual Script Commands

Beginners usually do not need to run these commands manually.  
Use the Codex prompt above first.

These scripts do not replace the Agent reasoning step. In particular, `build_html.py` requires `working/cheatsheet_content.md` to already exist.

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