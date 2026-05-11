# Quick Start / 快速开始

[中文](#中文) | [English](#english)

---

## 中文

`course-cheatsheet-maker` 是一个可安装的 Codex 风格 skill，用于根据课程材料生成 A4 横版课程 cheatsheet。

这个 Quick Start 面向第一次使用的新用户。你需要完成四件事：

1. 安装 skill；
2. 从 `courses/COURSE_NAME/` 复制一个课程模板；
3. 放入课程材料；
4. 把使用 prompt 复制给 Codex。

---

## 0. 先理解两个目录

这个项目里有两个容易混淆的概念：

| 概念 | 作用 | 示例 |
|---|---|---|
| skill 安装目录 | 放 `SKILL.md`、`scripts/`、`assets/` 等 skill 文件 | `~/.agents/skills/course-cheatsheet-maker/` |
| 课程目录 | 放你的真实课程材料和生成结果 | `courses/COMP7503/` |

本仓库现在自带一个空模板：

```text
courses/COURSE_NAME/
  materials/
    knowledge/
    questions/
  working/
  outputs/
```

`COURSE_NAME` 只是占位名。实际使用时，请复制或改名成真实课程名，例如 `COMP7503`。

---

## 1. 安装 Skill

先按照 `INSTALL.md` 安装并验证 skill。

你也可以把下面这段话复制给 Codex / 支持 skills 的 Agent：

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

这个目录是 skill 的安装位置，不是课程材料目录。

---

## 2. 创建课程目录

本仓库已经提供了一个空课程模板：

```text
courses/COURSE_NAME/
```

第一次使用时，可以复制这个模板。

macOS / Linux / Git Bash：

```bash
cp -r courses/COURSE_NAME courses/COMP7503
```

Windows PowerShell：

```powershell
Copy-Item -Recurse courses\COURSE_NAME courses\COMP7503
```

复制后结构应该类似：

```text
courses/COMP7503/
  materials/
    knowledge/
    questions/
  working/
  outputs/
```

如果你不想在 skill 仓库里测试，也可以在自己的私有课程项目里创建同样的结构：

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
courses/COMP7503/materials/knowledge/
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
courses/COMP7503/materials/questions/
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

`knowledge/` 和 `questions/` 内部可以继续创建子文件夹。

不要把真实课程材料提交到公开仓库。如果这个仓库要发布到 GitHub，请确保 `.gitignore` 会忽略真实材料、`working/` 和 `outputs/` 中的生成结果。

---

## 4. 参数说明

你可以在 prompt 中调整以下五个参数。

### 4.1 `workflow_mode`

控制自动化程度。

| 值 | 含义 | 适合场景 |
|---|---|---|
| `full-auto` | 自动完成提取、候选单元构建、topic 分析、cheatsheet 内容生成、HTML 渲染和验证。 | 新手第一次跑完整流程。 |
| `safe-review` | 先生成并检查中间分析文件，再决定是否继续渲染最终 HTML。 | 课程材料很多、你想先看 topic ranking 是否合理。 |

Quick Start 推荐显式使用：

```text
workflow_mode = full-auto
```

### 4.2 `layout`

控制首选检查版式。

| 值 | 含义 |
|---|---|
| `3col` | 3 栏 A4 横版，默认推荐，更稳定、更易读。 |
| `4col` | 4 栏 A4 横版，更紧凑，但可读性可能下降。 |

注意：Full Auto 通常仍会生成两个 HTML：

```text
cheatsheet_3col.html
cheatsheet_4col.html
```

`layout` 主要决定优先检查和验证哪个版本。

### 4.3 `target_pages`

控制总内容预算。

```text
target_pages = 1
```

它不是绝对 PDF 页数保证，而是内容压缩目标。页数越少，内容筛选越严格；页数越多，覆盖面越广。

常见选择：

| 值 | 适合场景 |
|---|---|
| `1` | 考前速查、强压缩 cheatsheet。 |
| `2` | 更完整的复习版，适合 comprehensive review。 |
| `3` | 覆盖更多 topic，但内容会明显变长。 |

### 4.4 `coverage_mode`

控制 topic 选择范围。

| 值 | 含义 |
|---|---|
| `exam-compact` | 偏考试重点，优先保留高频、高证据、高风险 topic。 |
| `balanced-standard` | 默认平衡模式，在覆盖面和压缩度之间折中。 |
| `comprehensive-review` | 尽量覆盖更多 lecture/topic，适合系统复习。 |

内部 ranking 通常会把 topic 分成：

| 类别 | 含义 |
|---|---|
| A | 必须掌握，高价值、高证据、高风险 topic。 |
| B | 重要 topic，通常应保留。 |
| C | 较低优先级或补充 topic，根据页数选择代表性内容。 |
| R | 参考类或低频内容，通常只在多页或特殊需要时保留。 |

### 4.5 `detail_mode`

控制每个已选 topic 写多细。

| 值 | 含义 |
|---|---|
| `simple` | 更像速查表，定义、公式、关键词优先，解释很少。 |
| `balanced` | 默认模式，兼顾概念、公式、陷阱、简短例子。 |
| `detailed` | 更像学习版，对重要 topic 给更多解释和对比。 |

注意：`coverage_mode` 决定“选哪些 topic”，`detail_mode` 决定“选中的 topic 写多细”。

---

## 5. 推荐参数组合

### 考前一页速记

```text
workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = exam-compact
detail_mode = simple
```

### 默认复习版

```text
workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced
```

### 两页全面复习版

```text
workflow_mode = full-auto
layout = 3col
target_pages = 2
coverage_mode = comprehensive-review
detail_mode = balanced
```

### 先检查 topic ranking 再生成

```text
workflow_mode = safe-review
layout = 3col
target_pages = 2
coverage_mode = comprehensive-review
detail_mode = balanced
```

---

## 6. 使用 Skill 生成 Cheatsheet

在课程项目根目录打开 Codex。

如果你的课程结构是：

```text
my-course-project/
  courses/
    COMP7503/
      materials/
        knowledge/
        questions/
```

那么你应该在这个目录打开 Codex：

```text
my-course-project/
```

然后复制下面这个 prompt 给 Codex：

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

如果你的课程名不是 `COMP7503`，请把 prompt 里的 `COMP7503` 全部替换成你的课程文件夹名。

---

## 7. 查看输出结果

生成结果会出现在：

```text
courses/COMP7503/outputs/
```

通常会生成：

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

其中：

- `cheatsheet_3col.html`：默认推荐版本，三栏 A4 横版；
- `cheatsheet_4col.html`：更紧凑版本，适合内容较多但可读性可能更低。

中间分析文件会出现在：

```text
courses/COMP7503/working/
```

常见中间文件包括：

```text
courses/COMP7503/working/run_config.md
courses/COMP7503/working/extracted/
courses/COMP7503/working/extraction_report.md
courses/COMP7503/working/candidate_units.jsonl
courses/COMP7503/working/knowledge_units.md
courses/COMP7503/working/topic_map.md
courses/COMP7503/working/importance_ranking.md
courses/COMP7503/working/topic_evidence_map.md
courses/COMP7503/working/cheatsheet_content.md
```

---

## 8. 什么是 `--root`

手动运行脚本时，你会看到：

```text
--root courses
```

`--root` 的意思是：**包含课程文件夹的上一级目录**。

例如：

```text
courses/COMP7503/
```

这里：

```text
course_name = COMP7503
--root = courses
```

所以命令写成：

```bash
python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root courses
```

如果你的课程目录在别的地方，例如：

```text
/private/my-course-project/courses/COMP7503/
```

你可以先进入：

```text
/private/my-course-project/
```

然后仍然使用：

```bash
python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root courses
```

或者从任意目录显式传入完整路径：

```bash
python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root /private/my-course-project/courses
```

一句话总结：`--root` 指向“装着课程文件夹的目录”，不是 skill 安装目录。

---

## 9. 导出 PDF

本 skill 的主要输出是 HTML。

你可以用浏览器打开：

```text
courses/COMP7503/outputs/cheatsheet_3col.html
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

## 10. 常见误区

### 误区 1：直接运行 `build_html.py` 就能自动生成 cheatsheet

不可以。

`build_html.py` 只负责把已经写好的：

```text
working/cheatsheet_content.md
```

渲染成 HTML。

它不会自动分析课程材料，也不会自动决定哪些内容应该放进 cheatsheet。材料理解、topic ranking、内容筛选、压缩和 `cheatsheet_content.md` 写作，需要由 Codex 按照 `$course-cheatsheet-maker` 的工作流完成。

### 误区 2：把真实课程材料提交到公开仓库

不要这样做。

`courses/COURSE_NAME/` 是空模板。真实材料只应保留在本地或私有项目中。

### 误区 3：在错误的目录打开 Codex

推荐在课程项目根目录打开 Codex，例如：

```text
my-course-project/
```

不推荐在全局 skill 安装目录里操作：

```text
~/.agents/skills/course-cheatsheet-maker/
```

### 误区 4：把 `target_pages` 理解成绝对页数保证

`target_pages` 是内容预算和压缩目标，不是绝对打印页数保证。最终 PDF 页数仍可能受到浏览器、字体、缩放、纸张设置等影响。

---

## 11. Advanced: 手动脚本命令

新手一般不需要手动运行这些命令，推荐先使用上面的 Codex prompt。

下面的命令主要适合调试或高级用户。这些脚本不会替代 Agent 的推理步骤，尤其是 `build_html.py` 要求 `working/cheatsheet_content.md` 已经存在。

macOS / Linux / Git Bash：

```bash
SKILL_DIR="$HOME/.agents/skills/course-cheatsheet-maker"

python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root courses
python "$SKILL_DIR/scripts/build_candidate_units.py" COMP7503 --root courses
python "$SKILL_DIR/scripts/build_html.py" COMP7503 --root courses
python "$SKILL_DIR/scripts/validate_workflow.py" COMP7503 --root courses --mode full-auto --layout 3col --target-pages 1 --coverage-mode balanced-standard --detail-mode balanced
```

Windows PowerShell：

```powershell
$env:SKILL_DIR="$HOME\.agents\skills\course-cheatsheet-maker"

python "$env:SKILL_DIR\scripts\extract_materials.py" COMP7503 --root courses
python "$env:SKILL_DIR\scripts\build_candidate_units.py" COMP7503 --root courses
python "$env:SKILL_DIR\scripts\build_html.py" COMP7503 --root courses
python "$env:SKILL_DIR\scripts\validate_workflow.py" COMP7503 --root courses --mode full-auto --layout 3col --target-pages 1 --coverage-mode balanced-standard --detail-mode balanced
```

---

# English

`course-cheatsheet-maker` is an installable Codex-style skill for creating A4 landscape course cheatsheets from course materials.

This Quick Start is for first-time users. You need to do four things:

1. install the skill;
2. copy a course scaffold from `courses/COURSE_NAME/`;
3. put in your course materials;
4. copy the usage prompt to Codex.

---

## 0. Understand The Two Directories First

There are two concepts that are easy to confuse:

| Concept | Purpose | Example |
|---|---|---|
| Skill installation directory | Contains `SKILL.md`, `scripts/`, `assets/`, and other skill files. | `~/.agents/skills/course-cheatsheet-maker/` |
| Course directory | Contains your real course materials and generated outputs. | `courses/COMP7503/` |

This repository now includes an empty scaffold:

```text
courses/COURSE_NAME/
  materials/
    knowledge/
    questions/
  working/
  outputs/
```

`COURSE_NAME` is only a placeholder. In real use, copy or rename it to an actual course name, such as `COMP7503`.

---

## 1. Install The Skill

First, install and validate the skill using `INSTALL.md`.

You can also copy this prompt to Codex or another Agent that supports skills:

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

This is the skill installation directory, not the course material directory.

---

## 2. Create A Course Directory

This repository already provides an empty course scaffold:

```text
courses/COURSE_NAME/
```

For first use, copy this scaffold.

macOS / Linux / Git Bash:

```bash
cp -r courses/COURSE_NAME courses/COMP7503
```

Windows PowerShell:

```powershell
Copy-Item -Recurse courses\COURSE_NAME courses\COMP7503
```

After copying, the structure should look like:

```text
courses/COMP7503/
  materials/
    knowledge/
    questions/
  working/
  outputs/
```

If you do not want to test inside the skill repository, create the same structure in your own private course project:

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

Put knowledge sources in:

```text
courses/COMP7503/materials/knowledge/
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
courses/COMP7503/materials/questions/
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

Subfolders inside `knowledge/` and `questions/` are supported.

Do not commit real course materials to a public repository. If this repository is published on GitHub, make sure `.gitignore` excludes real materials, generated `working/` files, and generated `outputs/` files.

---

## 4. Parameters

You can adjust the following five parameters in the prompt.

### 4.1 `workflow_mode`

Controls automation level.

| Value | Meaning | Best For |
|---|---|---|
| `full-auto` | Runs extraction, candidate-unit building, topic analysis, cheatsheet content generation, HTML rendering, and validation. | First complete run for beginners. |
| `safe-review` | Creates intermediate analysis artifacts first so you can inspect them before final rendering. | Large course sets or cases where you want to review topic ranking first. |

Quick Start recommends explicitly using:

```text
workflow_mode = full-auto
```

### 4.2 `layout`

Controls the preferred layout for review.

| Value | Meaning |
|---|---|
| `3col` | 3-column A4 landscape layout. Recommended default; usually more stable and readable. |
| `4col` | 4-column A4 landscape layout. Denser, but may be less readable. |

Note: Full Auto usually still generates both HTML files:

```text
cheatsheet_3col.html
cheatsheet_4col.html
```

`layout` mainly decides which version should be prioritized for review and validation.

### 4.3 `target_pages`

Controls the total content budget.

```text
target_pages = 1
```

It is not an absolute PDF page guarantee. It is a compression target. Fewer pages means stricter selection; more pages means wider coverage.

Common choices:

| Value | Best For |
|---|---|
| `1` | Compact exam cram sheet. |
| `2` | More complete review sheet, especially for comprehensive review. |
| `3` | Wider topic coverage, but much longer content. |

### 4.4 `coverage_mode`

Controls topic selection coverage.

| Value | Meaning |
|---|---|
| `exam-compact` | Exam-focused. Prioritizes frequent, well-supported, high-risk topics. |
| `balanced-standard` | Default balanced mode between coverage and compression. |
| `comprehensive-review` | Covers more lectures/topics for systematic review. |

Internally, topic ranking usually uses these classes:

| Class | Meaning |
|---|---|
| A | Must-know, high-value, well-supported, or high-risk topics. |
| B | Important topics that should usually be kept. |
| C | Lower-priority or supporting topics; representative ones are selected depending on page budget. |
| R | Reference or low-frequency material; usually included only for multi-page or special cases. |

### 4.5 `detail_mode`

Controls how much detail selected topics receive.

| Value | Meaning |
|---|---|
| `simple` | Quick-reference style. Definitions, formulas, and keywords first; minimal explanations. |
| `balanced` | Default mode. Balances concepts, formulas, traps, and compact examples. |
| `detailed` | Study-guide style. Adds more explanation and comparison for important topics. |

Important: `coverage_mode` decides which topics are selected. `detail_mode` decides how much detail selected topics receive.

---

## 5. Recommended Presets

### One-page exam cram sheet

```text
workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = exam-compact
detail_mode = simple
```

### Default review sheet

```text
workflow_mode = full-auto
layout = 3col
target_pages = 1
coverage_mode = balanced-standard
detail_mode = balanced
```

### Two-page comprehensive review

```text
workflow_mode = full-auto
layout = 3col
target_pages = 2
coverage_mode = comprehensive-review
detail_mode = balanced
```

### Review topic ranking before final rendering

```text
workflow_mode = safe-review
layout = 3col
target_pages = 2
coverage_mode = comprehensive-review
detail_mode = balanced
```

---

## 6. Use The Skill To Generate A Cheatsheet

Open Codex from your course project root.

If your course structure is:

```text
my-course-project/
  courses/
    COMP7503/
      materials/
        knowledge/
        questions/
```

Then open Codex in:

```text
my-course-project/
```

Copy this prompt to Codex:

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

If your course is not named `COMP7503`, replace every `COMP7503` in the prompt with your actual course folder name.

---

## 7. Check The Outputs

Rendered outputs will appear in:

```text
courses/COMP7503/outputs/
```

Usually, the skill generates:

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

Meaning:

- `cheatsheet_3col.html`: recommended default output, A4 landscape with three columns;
- `cheatsheet_4col.html`: denser output, useful for more content but potentially less readable.

Intermediate artifacts will appear in:

```text
courses/COMP7503/working/
```

Common working artifacts include:

```text
courses/COMP7503/working/run_config.md
courses/COMP7503/working/extracted/
courses/COMP7503/working/extraction_report.md
courses/COMP7503/working/candidate_units.jsonl
courses/COMP7503/working/knowledge_units.md
courses/COMP7503/working/topic_map.md
courses/COMP7503/working/importance_ranking.md
courses/COMP7503/working/topic_evidence_map.md
courses/COMP7503/working/cheatsheet_content.md
```

---

## 8. What `--root` Means

When running scripts manually, you will see:

```text
--root courses
```

`--root` means: **the parent directory that contains your course folder**.

For example:

```text
courses/COMP7503/
```

Here:

```text
course_name = COMP7503
--root = courses
```

So the command is:

```bash
python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root courses
```

If your course directory is elsewhere, for example:

```text
/private/my-course-project/courses/COMP7503/
```

You can first enter:

```text
/private/my-course-project/
```

Then still use:

```bash
python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root courses
```

Or pass the full path from anywhere:

```bash
python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root /private/my-course-project/courses
```

In one sentence: `--root` points to the directory that contains your course folder. It is not the skill installation directory.

---

## 9. Export To PDF

The main output of this skill is HTML.

Open this file in a browser:

```text
courses/COMP7503/outputs/cheatsheet_3col.html
```

Then use the browser print dialog to export PDF:

```text
Ctrl + P / Cmd + P
Save as PDF
Paper size: A4
Layout: Landscape
Margins: None or Minimum
Background graphics: On
```

Prefer `cheatsheet_3col.html` first because it is usually more stable and readable.

---

## 10. Common Mistakes

### Mistake 1: Running only `build_html.py` and expecting a full cheatsheet

This will not work.

`build_html.py` only renders an existing:

```text
working/cheatsheet_content.md
```

into HTML.

It does not analyze course materials or decide which topics should be included. Material understanding, topic ranking, selection, compression, and `cheatsheet_content.md` writing must be done by Codex using the `$course-cheatsheet-maker` workflow.

### Mistake 2: Committing real course materials to a public repository

Do not do this.

`courses/COURSE_NAME/` is an empty scaffold. Real course materials should stay local or private.

### Mistake 3: Opening Codex in the wrong directory

Open Codex from the course project root, for example:

```text
my-course-project/
```

Do not operate from the global skill installation directory:

```text
~/.agents/skills/course-cheatsheet-maker/
```

### Mistake 4: Treating `target_pages` as an absolute page guarantee

`target_pages` is a content budget and compression target, not an absolute print-page guarantee. Final PDF pages may still be affected by browser, font, scale, paper, and margin settings.

---

## 11. Advanced: Manual Script Commands

Beginners usually do not need to run these commands manually. Use the Codex prompt above first.

These commands are mainly for debugging or advanced users. They do not replace the Agent reasoning steps. In particular, `build_html.py` requires `working/cheatsheet_content.md` to already exist.

macOS / Linux / Git Bash:

```bash
SKILL_DIR="$HOME/.agents/skills/course-cheatsheet-maker"

python "$SKILL_DIR/scripts/extract_materials.py" COMP7503 --root courses
python "$SKILL_DIR/scripts/build_candidate_units.py" COMP7503 --root courses
python "$SKILL_DIR/scripts/build_html.py" COMP7503 --root courses
python "$SKILL_DIR/scripts/validate_workflow.py" COMP7503 --root courses --mode full-auto --layout 3col --target-pages 1 --coverage-mode balanced-standard --detail-mode balanced
```

Windows PowerShell:

```powershell
$env:SKILL_DIR="$HOME\.agents\skills\course-cheatsheet-maker"

python "$env:SKILL_DIR\scripts\extract_materials.py" COMP7503 --root courses
python "$env:SKILL_DIR\scripts\build_candidate_units.py" COMP7503 --root courses
python "$env:SKILL_DIR\scripts\build_html.py" COMP7503 --root courses
python "$env:SKILL_DIR\scripts\validate_workflow.py" COMP7503 --root courses --mode full-auto --layout 3col --target-pages 1 --coverage-mode balanced-standard --detail-mode balanced
```
