# 快速开始（中文版）

本指南面向安装后的第一次使用者。它假设你想用 `course-cheatsheet-maker` 处理自己的私人课程资料。

重要概念：安装后的 skill 文件夹是可复用的 runtime package。你的真实课程文件应该放在你自己的课程项目里，而不是全局 skill 安装目录里。

## 第 1 步：安装 Skill

按照 [INSTALL.md](INSTALL.md) 安装 skill。

你也可以向 Codex 或其他 coding agent 发送：

```text
Install and validate the course-cheatsheet-maker skill by following this guide:
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/INSTALL.md
```

## 第 2 步：确认安装后的 Skill 文件夹是干净的

安装后，该文件夹应该只包含 runtime skill package：

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

安装后的文件夹不应该包含 `README.md`、`QUICK_START.md`、`INSTALL.md`、`LICENSE`、`.gitignore`、`.git/`、`__pycache__/`、真实课程资料，或来自真实课程的生成输出。

`courses/COURSE_NAME/` 只是 starter scaffold。它不是真实课程，也不是用来存放公开课程资料的位置。

`courses/COURSE_NAME/` 内隐藏的 `.gitkeep` 文件是允许存在的。它们只是为了让 Git 跟踪空的 starter scaffold 文件夹；它们不是真实课程资料，也不算生成输出。

## 第 3 步：复制 Starter Course Scaffold

创建你自己的课程项目文件夹，然后从已安装的 skill 文件夹中把 starter scaffold 复制到该项目里。

示例目标课程名：`COMP7503`。

macOS / Linux / Git Bash：

```bash
mkdir -p courses
cp -r "$HOME/.agents/skills/course-cheatsheet-maker/courses/COURSE_NAME" courses/COMP7503
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force courses
Copy-Item -LiteralPath "$HOME\.agents\skills\course-cheatsheet-maker\courses\COURSE_NAME" -Destination "courses\COMP7503" -Recurse -Force
```

复制后，你的私人课程项目应该长这样：

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

把 `COMP7503` 替换成你的真实课程文件夹名。

## 第 4 步：添加课程资料

把 lecture 和 knowledge sources 放在这里：

```text
courses/COMP7503/materials/knowledge/
```

适合的例子包括 lecture slides、lecture notes、review notes、handouts、textbook excerpts 和 tutorial explanations。

把 question-like 或 assessment-related sources 放在这里：

```text
courses/COMP7503/materials/questions/
```

适合的例子包括 quizzes、assignments、tutorial questions、workshop questions、problem sets、sample exams、mock exams 和 past papers。

示例：

```text
courses/COMP7503/materials/knowledge/week01_slides.pdf
courses/COMP7503/materials/knowledge/week02_notes.pdf
courses/COMP7503/materials/questions/past_paper_2024.pdf
courses/COMP7503/materials/questions/workshop_03.pdf
```

`knowledge/` 和 `questions/` 内部支持子文件夹。

## 第 5 步：运行示例 Prompt

从你的私人课程项目根目录打开 Codex：

```text
my-course-project/
```

然后发送这个 prompt：

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

如果你的课程文件夹不叫 `COMP7503`，请把 prompt 中每一个 `COMP7503` 替换成你的实际课程文件夹名。

## 检查输出

生成的 HTML 文件会出现在这里：

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

Working 和 traceability 文件会出现在这里：

```text
courses/COMP7503/working/
```

常见 working 文件包括：

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

## 新手说明

`workflow_mode = full-auto` 会在一个流程中运行提取、分析、渲染和验证。

`layout = 3col` 是推荐的初始布局。Full Auto 仍然会渲染 `cheatsheet_3col.html` 和 `cheatsheet_4col.html` 两个文件。

`target_pages = 1` 是内容预算，不是精确的页数保证。浏览器打印设置仍然可能影响最终 PDF 页数。

`coverage_mode` 控制包含哪些主题。`detail_mode` 控制已包含主题的细节量。

## 可选 PDF 导出

主要输出是 HTML。若要导出 PDF，请打开：

```text
courses/COMP7503/outputs/cheatsheet_3col.html
```

然后使用浏览器打印对话框：

```text
Ctrl + P / Cmd + P
Save as PDF
Paper size: A4
Layout: Landscape
Margins: None or Minimum
Background graphics: On
```

## 常见错误

不要把真实课程资料放进：

```text
~/.agents/skills/course-cheatsheet-maker/
```

不要只运行 `build_html.py` 然后期待它完成完整课程分析。该脚本只会渲染已经写好的 `working/cheatsheet_content.md`。

不要把私人课程资料、提取文本、`working/` 文件或生成的 `outputs/` 文件提交到公开仓库。


---

# Quick Start

This guide is for first-time users after installation. It assumes you want to use `course-cheatsheet-maker` with your own private course materials.

The important idea: the installed skill folder is the reusable runtime package. Your real course files should live in your own course project, not inside the global skill install directory.

## Step 1: Install The Skill

Install the skill by following [INSTALL.md](INSTALL.md).

You can also ask Codex or another coding agent:

```text
Install and validate the course-cheatsheet-maker skill by following this guide:
https://raw.githubusercontent.com/tsukiR1n/course-cheatsheet-maker/main/INSTALL.md
```

## Step 2: Confirm The Installed Skill Folder Is Clean

After installation, the folder should contain only the runtime skill package:

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

The installed folder should not contain `README.md`, `QUICK_START.md`, `INSTALL.md`, `LICENSE`, `.gitignore`, `.git/`, `__pycache__/`, real course materials, or generated outputs from real courses.

`courses/COURSE_NAME/` is only a starter scaffold. It is not a real course and it is not a place to store public course materials.

Hidden `.gitkeep` files inside `courses/COURSE_NAME/` are allowed. They only keep empty starter scaffold folders tracked by Git; they are not real course materials and do not count as generated outputs.

## Step 3: Copy The Starter Course Scaffold

Create your own course project folder, then copy the starter scaffold from the installed skill folder into that project.

Example target course name: `COMP7503`.

macOS / Linux / Git Bash:

```bash
mkdir -p courses
cp -r "$HOME/.agents/skills/course-cheatsheet-maker/courses/COURSE_NAME" courses/COMP7503
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force courses
Copy-Item -LiteralPath "$HOME\.agents\skills\course-cheatsheet-maker\courses\COURSE_NAME" -Destination "courses\COMP7503" -Recurse -Force
```

After copying, your private course project should look like:

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

Replace `COMP7503` with your real course folder name.

## Step 4: Add Course Materials

Put lecture and knowledge sources here:

```text
courses/COMP7503/materials/knowledge/
```

Good examples include lecture slides, lecture notes, review notes, handouts, textbook excerpts, and tutorial explanations.

Put question-like or assessment-related sources here:

```text
courses/COMP7503/materials/questions/
```

Good examples include quizzes, assignments, tutorial questions, workshop questions, problem sets, sample exams, mock exams, and past papers.

Example:

```text
courses/COMP7503/materials/knowledge/week01_slides.pdf
courses/COMP7503/materials/knowledge/week02_notes.pdf
courses/COMP7503/materials/questions/past_paper_2024.pdf
courses/COMP7503/materials/questions/workshop_03.pdf
```

Subfolders inside `knowledge/` and `questions/` are supported.

## Step 5: Run The Example Prompt

Open Codex from your private course project root:

```text
my-course-project/
```

Then send this prompt:

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

If your course folder is not named `COMP7503`, replace every `COMP7503` in the prompt with your actual course folder name.

## Check The Outputs

Generated HTML files appear here:

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

Working and traceability files appear here:

```text
courses/COMP7503/working/
```

Common working files include:

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

## Beginner Notes

`workflow_mode = full-auto` runs extraction, analysis, rendering, and validation in one flow.

`layout = 3col` is the recommended first layout. Full Auto still renders both `cheatsheet_3col.html` and `cheatsheet_4col.html`.

`target_pages = 1` is a content budget, not a perfect page guarantee. Browser print settings can still change the final PDF page count.

`coverage_mode` controls which topics are included. `detail_mode` controls how much detail included topics receive.

## Optional PDF Export

The main output is HTML. To export PDF, open:

```text
courses/COMP7503/outputs/cheatsheet_3col.html
```

Then use the browser print dialog:

```text
Ctrl + P / Cmd + P
Save as PDF
Paper size: A4
Layout: Landscape
Margins: None or Minimum
Background graphics: On
```

## Common Mistakes

Do not put real course materials inside:

```text
~/.agents/skills/course-cheatsheet-maker/
```

Do not run only `build_html.py` and expect full course analysis. That script only renders an already written `working/cheatsheet_content.md`.

Do not commit private course materials, extracted text, `working/` files, or generated `outputs/` files to a public repository.
