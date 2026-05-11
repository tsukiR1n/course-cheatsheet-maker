# course-cheatsheet-maker

[中文](#中文) | [English](#english)

---

## 中文

`course-cheatsheet-maker` 是一个可安装的 Codex 风格 skill，用于根据课程材料生成紧凑的 A4 横版课程 cheatsheet。

它可以帮助 Agent：

- 从 PDF、PPTX、DOCX、TXT、Markdown 等课程材料中提取文本；
- 构建可追溯的候选知识单元；
- 结合知识类材料和题目类材料推断 topic 重要性；
- 生成可人工检查的中间分析产物；
- 渲染 3 栏和 4 栏的可打印 HTML cheatsheet。

HTML/CSS 是最终版式的 source of truth。PDF 导出是可选步骤，应尽量保持 HTML 打印版式不变。

> **重要说明：** 正确安装本 skill 时，应同时包含 `courses/COURSE_NAME/`。它是随仓库发布的空 starter scaffold，用来提供 `materials/knowledge/`、`materials/questions/`、`working/` 和 `outputs/` 这些目录。请只把它当作模板，不要把真实课程材料提交到公开仓库。

---

## 这个仓库是什么

这个仓库既包含可安装的 skill 文件，也包含一个随 release 安装的空课程目录模板。

```text
course-cheatsheet-maker/
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
  INSTALL.md
  QUICK_START.md
  README.md
```

其中：

| 路径 | 作用 |
|---|---|
| `SKILL.md` | skill 的核心说明文件，Codex/Agent 会根据它执行工作流。 |
| `scripts/` | 提取材料、构建候选单元、渲染 HTML、验证输出的辅助脚本。 |
| `assets/` | 3 栏和 4 栏 HTML 模板。 |
| `references/` | 重要性评分、内容压缩和版式规范。 |
| `courses/COURSE_NAME/` | 空课程模板，用于让新用户知道课程材料应该怎么放。 |

`courses/COURSE_NAME/` 是模板，不是固定课程名。实际使用时，你可以把它复制或改名为真实课程名，例如 `COMP7503`、`MATH101` 或 `DATABASE`。

---

## Skill 安装位置和课程材料位置

请区分两个位置：

1. **skill 安装位置**：放 `SKILL.md`、`scripts/`、`assets/` 等文件，也应包含空的 `courses/COURSE_NAME/` starter scaffold。
2. **课程材料位置**：放你自己的 lecture notes、slides、quiz、past paper 等课程文件。

Codex 风格的全局 skill 安装位置通常是：

```text
~/.agents/skills/course-cheatsheet-maker/
```

Windows 上通常对应：

```text
C:\Users\<your-username>\.agents\skills\course-cheatsheet-maker\
```

真实课程材料不要放进全局 skill 安装目录。推荐放在你自己的课程项目中，例如：

全局 skill 安装中可以包含空的 `courses/COURSE_NAME` scaffold，但真实课程材料应保留在你的私有课程项目中。

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

如果你只是本地测试，也可以直接在本仓库中复制 `courses/COURSE_NAME/` 模板进行测试；但不要把真实课程材料提交到公开仓库。

---

## 快速使用

详细步骤请查看 [`QUICK_START.md`](QUICK_START.md)。最短流程如下：

1. 按照 [`INSTALL.md`](INSTALL.md) 安装并验证 skill。
2. 复制课程模板：

```bash
mkdir -p courses
cp -r "$HOME/.agents/skills/course-cheatsheet-maker/courses/COURSE_NAME" courses/COMP7503
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force courses
Copy-Item -Recurse "$HOME\.agents\skills\course-cheatsheet-maker\courses\COURSE_NAME" "courses\COMP7503"
```

3. 放入课程材料：

```text
courses/COMP7503/materials/knowledge/
courses/COMP7503/materials/questions/
```

4. 在课程项目根目录打开 Codex，并使用：

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

5. 查看输出：

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

---

## 课程材料应该放在哪里

知识类材料放入：

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

题目类材料放入：

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

`knowledge/` 和 `questions/` 内部可以继续创建子文件夹。

---

## 参数总览

| 参数 | 可选值 | 推荐默认值 | 说明 |
|---|---|---|---|
| `workflow_mode` | `safe-review`, `full-auto` | `full-auto` for Quick Start | 工作流模式。`full-auto` 会自动完成提取、分析、渲染和验证；`safe-review` 适合先检查中间文件再继续。 |
| `layout` | `3col`, `4col` | `3col` | 首选检查版式。Full Auto 仍会生成 3 栏和 4 栏两个 HTML。 |
| `target_pages` | 正整数 | `1` | 内容预算，不是绝对 PDF 页数保证。页数越少压缩越强。 |
| `coverage_mode` | `exam-compact`, `balanced-standard`, `comprehensive-review` | `balanced-standard` | 控制 topic 覆盖范围。 |
| `detail_mode` | `simple`, `balanced`, `detailed` | `balanced` | 控制已选 topic 的细节程度。 |

推荐组合：

| 使用场景 | 参数 |
|---|---|
| 考前一页速记 | `target_pages = 1`, `coverage_mode = exam-compact`, `detail_mode = simple` |
| 默认复习版 | `target_pages = 1`, `coverage_mode = balanced-standard`, `detail_mode = balanced` |
| 两页全面复习版 | `target_pages = 2`, `coverage_mode = comprehensive-review`, `detail_mode = balanced` |
| 先人工检查再生成 | `workflow_mode = safe-review`, 其他参数按需要设置 |

更详细的参数解释见 [`QUICK_START.md`](QUICK_START.md)。

---

## 工作流概览

```text
course materials
  ↓ extract_materials.py
working/extracted/
  ↓ build_candidate_units.py
working/candidate_units.jsonl
  ↓ Codex reasoning with SKILL.md
working/run_config.md
working/knowledge_units.md
working/topic_map.md
working/importance_ranking.md
working/topic_evidence_map.md
working/cheatsheet_content.md
  ↓ build_html.py
outputs/cheatsheet_3col.html
outputs/cheatsheet_4col.html
  ↓ optional browser export
PDF
```

注意：`build_html.py` 只负责把已经存在的 `working/cheatsheet_content.md` 渲染成 HTML。它不会自动分析课程材料，也不会自动决定哪些 topic 重要。

---

## 环境要求

推荐使用 Python 3.9+。

可选文本提取依赖列在 `requirements.txt` 中：

```text
pymupdf
python-pptx
python-docx
```

OCR 暂不属于本 skill 的范围。对于没有可选中文本的扫描版 PDF，脚本会报告该文件没有可提取文本。

---

## 版权提醒

不要将以下内容提交到公开仓库：

- 有版权的课程材料；
- 从课程材料中提取出的文本；
- 基于私有课程材料生成的 `working/` 文件；
- 基于私有课程材料生成的最终 HTML/PDF 输出。

本仓库中的 `courses/COURSE_NAME/` 只应保留空模板或 `.gitkeep` 占位文件。真实课程项目应保持私有，除非你已经获得发布源材料和衍生产物的授权。

---

## License

MIT License. See [`LICENSE`](LICENSE).

---

# English

`course-cheatsheet-maker` is an installable Codex-style skill for creating compact A4 landscape course cheatsheets from course materials.

It helps an agent:

- extract text from PDFs, PPTX, DOCX, TXT, Markdown, and similar course files;
- build traceable candidate knowledge units;
- infer topic importance from both knowledge sources and question-like sources;
- create reviewable intermediate artifacts;
- render printable 3-column and 4-column HTML cheatsheets.

HTML/CSS is the source of truth for layout. PDF export is optional and should preserve the printed HTML layout as closely as possible.

> **Important:** A correct installation includes `courses/COURSE_NAME/`. This bundled empty starter scaffold provides `materials/knowledge/`, `materials/questions/`, `working/`, and `outputs/` so beginners do not have to create those folders by hand. Keep it as a template, and do not commit real course materials to a public repository.

---

## What This Repository Contains

This repository contains both the installable skill files and an empty course scaffold that is included in the release install.

```text
course-cheatsheet-maker/
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
  INSTALL.md
  QUICK_START.md
  README.md
```

Path roles:

| Path | Purpose |
|---|---|
| `SKILL.md` | Core skill instructions used by Codex/Agent. |
| `scripts/` | Helper scripts for extraction, candidate-unit building, HTML rendering, and validation. |
| `assets/` | 3-column and 4-column HTML templates. |
| `references/` | Importance ranking, content compression, and layout guidelines. |
| `courses/COURSE_NAME/` | Empty course scaffold showing where course materials should go. |

`courses/COURSE_NAME/` is a template, not a fixed course name. In real use, copy or rename it to your actual course name, such as `COMP7503`, `MATH101`, or `DATABASE`.

---

## Skill Location vs. Course Material Location

Keep these two locations separate:

1. **Skill installation location**: contains `SKILL.md`, `scripts/`, `assets/`, related skill files, and the empty `courses/COURSE_NAME/` starter scaffold.
2. **Course material location**: contains your own lecture notes, slides, quizzes, past papers, and other course files.

For Codex-style setups, a typical global skill installation path is:

```text
~/.agents/skills/course-cheatsheet-maker/
```

On Windows, this usually corresponds to:

```text
C:\Users\<your-username>\.agents\skills\course-cheatsheet-maker\
```

Do not put real course materials inside the global skill installation directory.

The global skill install may include the empty `courses/COURSE_NAME` scaffold, but real course materials should stay in your private course project.

A recommended private course project looks like this:

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

For a quick local test, you may copy the bundled `courses/COURSE_NAME/` scaffold inside this repository. Do not commit real course materials to a public repository.

---

## Quick Use

See [`QUICK_START.md`](QUICK_START.md) for detailed steps. Minimal flow:

1. Install and validate the skill using [`INSTALL.md`](INSTALL.md).
2. Copy the course scaffold:

```bash
mkdir -p courses
cp -r "$HOME/.agents/skills/course-cheatsheet-maker/courses/COURSE_NAME" courses/COMP7503
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force courses
Copy-Item -Recurse "$HOME\.agents\skills\course-cheatsheet-maker\courses\COURSE_NAME" "courses\COMP7503"
```

3. Put course materials in:

```text
courses/COMP7503/materials/knowledge/
courses/COMP7503/materials/questions/
```

4. Open Codex from your course project root and use:

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

5. Check the outputs:

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

---

## Where Course Materials Go

Put knowledge sources in:

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

Subfolders inside `knowledge/` and `questions/` are supported.

---

## Parameter Overview

| Parameter | Values | Recommended Default | Meaning |
|---|---|---|---|
| `workflow_mode` | `safe-review`, `full-auto` | `full-auto` for Quick Start | Workflow mode. `full-auto` runs extraction, analysis, rendering, and validation automatically. `safe-review` is better when you want to inspect intermediate artifacts before continuing. |
| `layout` | `3col`, `4col` | `3col` | Preferred layout for review and validation. Full Auto still renders both 3-column and 4-column HTML files. |
| `target_pages` | positive integer | `1` | Content budget, not an absolute PDF page guarantee. Fewer pages means stronger compression. |
| `coverage_mode` | `exam-compact`, `balanced-standard`, `comprehensive-review` | `balanced-standard` | Controls topic coverage. |
| `detail_mode` | `simple`, `balanced`, `detailed` | `balanced` | Controls how much detail selected topics receive. |

Recommended presets:

| Use Case | Parameters |
|---|---|
| One-page exam cram sheet | `target_pages = 1`, `coverage_mode = exam-compact`, `detail_mode = simple` |
| Default review sheet | `target_pages = 1`, `coverage_mode = balanced-standard`, `detail_mode = balanced` |
| Two-page comprehensive review | `target_pages = 2`, `coverage_mode = comprehensive-review`, `detail_mode = balanced` |
| Review first, render later | `workflow_mode = safe-review`, other parameters as needed |

See [`QUICK_START.md`](QUICK_START.md) for more detailed parameter explanations.

---

## Workflow Overview

```text
course materials
  ↓ extract_materials.py
working/extracted/
  ↓ build_candidate_units.py
working/candidate_units.jsonl
  ↓ Codex reasoning with SKILL.md
working/run_config.md
working/knowledge_units.md
working/topic_map.md
working/importance_ranking.md
working/topic_evidence_map.md
working/cheatsheet_content.md
  ↓ build_html.py
outputs/cheatsheet_3col.html
outputs/cheatsheet_4col.html
  ↓ optional browser export
PDF
```

Note: `build_html.py` only renders an existing `working/cheatsheet_content.md` file into HTML. It does not analyze course materials or decide which topics are important.

---

## Requirements

Python 3.9+ is recommended.

Optional extraction dependencies are listed in `requirements.txt`:

```text
pymupdf
python-pptx
python-docx
```

OCR is intentionally out of scope. Scanned PDFs with no selectable text will be reported as having no extractable text.

---

## Copyright Note

Do not commit the following to a public repository:

- copyrighted course materials;
- text extracted from course materials;
- generated `working/` files based on private course materials;
- final HTML/PDF outputs based on private course materials.

The bundled `courses/COURSE_NAME/` should only contain an empty scaffold or `.gitkeep` placeholder files. Keep real course projects private unless you have permission to publish both the source materials and generated derivatives.

---

## License

MIT License. See [`LICENSE`](LICENSE).
