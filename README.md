# course-cheatsheet-maker

`course-cheatsheet-maker` 是一个可安装的 Codex 风格 skill，用于把课程资料转换成紧凑的 A4 横向 cheatsheet。

它可以帮助 coding agent：

- 从 PDF、PPTX、DOCX、TXT 和 Markdown 课程文件中提取文本；
- 区分知识类资料和题目类资料；
- 构建可追踪的候选知识单元；
- 根据课程强调内容和考核证据对主题重要性进行排序；
- 在渲染前创建可检查的工作文件；
- 渲染可打印的三栏和四栏 HTML cheatsheet。

HTML/CSS 是排版的权威来源。PDF 导出是可选的，通常通过浏览器打印对话框完成。

## 这个仓库包含什么

这个 GitHub 仓库包含两部分：

1. 可复用的 runtime skill package 文件；以及
2. 位于 `courses/COURSE_NAME/` 的课程 starter scaffold。

包含这个 starter scaffold 是为了让第一次使用的用户可以直接看到所需课程文件夹结构，而不需要手动创建每一个文件夹。它不是真实课程，也不应该包含公开课程资料。

`courses/COURSE_NAME/` 内隐藏的 `.gitkeep` 文件是允许存在的。它们只是为了让 Git 跟踪空的 starter scaffold 文件夹；它们不是真实课程资料，也不算生成输出。

`README.md`、`QUICK_START.md` 和 `INSTALL.md` 等仓库文档只面向 GitHub 用户和安装者。它们属于这个仓库，但不属于安装后的 runtime skill folder。

## 仓库结构

公开仓库可以包含文档和仓库元数据：

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
  README.md
  QUICK_START.md
  INSTALL.md
  LICENSE
  .gitignore
```

路径作用：

| 路径 | 用途 |
|---|---|
| `SKILL.md` | Codex 或其他 coding agent 使用的核心 skill 指令。 |
| `requirements.txt` | 可选的 Python 文本提取依赖。 |
| `scripts/` | 用于提取、候选单元构建、HTML 渲染、PDF 指引和验证的辅助脚本。 |
| `assets/` | HTML 模板和渲染资源。 |
| `references/` | skill 使用的评分规则和指导文档。 |
| `courses/COURSE_NAME/` | 面向第一次使用者的空 starter scaffold。 |
| `README.md`, `QUICK_START.md`, `INSTALL.md` | 仅为仓库文档。不要把这些复制到安装后的 runtime skill folder 中。 |

## 安装后的 Skill 结构

安装后，全局 skill 文件夹应该只包含 runtime package：

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

安装后的 skill 文件夹不应该包含 `README.md`、`QUICK_START.md`、`INSTALL.md`、`LICENSE`、`.gitignore`、`.git/` 或 `__pycache__/` 等仅属于仓库的文件。

## Skill 位置与课程项目位置

请把这两个位置分开：

1. **全局 skill 安装文件夹**：包含可复用的 skill package 和空的 `courses/COURSE_NAME/` scaffold。
2. **私人课程项目文件夹**：包含你的真实课堂笔记、课件、quiz、past paper、生成的 working 文件和生成的 outputs。

典型的全局 skill 位置：

```text
~/.agents/skills/course-cheatsheet-maker/
```

在 Windows 上，这通常对应：

```text
C:\Users\<your-username>\.agents\skills\course-cheatsheet-maker\
```

真实课程资料应该放在你自己的私人课程项目中，而不是全局 skill 安装目录里。一个私人课程项目可以长这样：

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
注意：`COMP7503` 只是示例。请在所有路径和 prompt 中把它替换成你的真实课程文件夹名。
把已安装的 `courses/COURSE_NAME/` scaffold 当作模板使用。将它复制到你的私人课程项目中，并把副本重命名为你的真实课程名，例如 `COMP7503`、`MATH101` 或 `DATABASE`。

## 快速使用

请查看 [QUICK_START.md](QUICK_START.md) 获取第一次运行指南。简短版本如下：

1. 按照 [INSTALL.md](INSTALL.md) 安装 skill。
2. 将 `~/.agents/skills/course-cheatsheet-maker/courses/COURSE_NAME/` 复制到你自己的课程项目中，例如 `courses/COMP7503/`。
3. 将资料放入：

```text
courses/COMP7503/materials/knowledge/
courses/COMP7503/materials/questions/
```

注意：`COMP7503` 只是示例。请在所有路径和 prompt 中把它替换成你的真实课程文件夹名。

4. 在你的课程项目根目录打开 Codex，并使用：

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

5. 查看生成的 HTML 文件：

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

## 课程资料应该放在哪里

把知识类资料放在：

```text
courses/COURSE_NAME/materials/knowledge/
```

适合放入 `knowledge/` 的资料包括 lecture slides、lecture notes、handouts、textbook excerpts、tutorial explanations 和 review notes。

把题目类或考核相关资料放在：

```text
courses/COURSE_NAME/materials/questions/
```

适合放入 `questions/` 的资料包括 quizzes、assignments、tutorial questions、workshop questions、problem sets、sample exams、mock exams 和 past papers。

`knowledge/` 和 `questions/` 内部支持子文件夹。

## 参数概览

| 参数 | 取值 | 推荐默认值 | 含义 |
|---|---|---|---|
| `workflow_mode` | `safe-review`, `full-auto` | 首次使用推荐 `full-auto` | 控制自动化程度。 |
| `layout` | `3col`, `4col` | `3col` | 用于检查和验证的首选布局。Full Auto 仍会渲染两个 HTML 文件。 |
| `target_pages` | 正整数 | `1` | 内容预算，不是精确的打印页数保证。 |
| `coverage_mode` | `exam-compact`, `balanced-standard`, `comprehensive-review` | `balanced-standard` | 控制纳入哪些主题。 |
| `detail_mode` | `simple`, `balanced`, `detailed` | `balanced` | 控制已纳入主题的细节程度。 |

推荐预设：

| 使用场景 | 参数 |
|---|---|
| 一页考前速记 sheet | `target_pages = 1`, `coverage_mode = exam-compact`, `detail_mode = simple` |
| 默认复习 sheet | `target_pages = 1`, `coverage_mode = balanced-standard`, `detail_mode = balanced` |
| 两页综合复习 | `target_pages = 2`, `coverage_mode = comprehensive-review`, `detail_mode = balanced` |
| 先检查，之后再渲染 | `workflow_mode = safe-review`, 其他参数按需设置 |

## 工作流概览

```text
course materials
  -> extract_materials.py
working/extracted/
  -> build_candidate_units.py
working/candidate_units.jsonl
  -> Codex reasoning with SKILL.md
working/run_config.md
working/knowledge_units.md
working/topic_map.md
working/importance_ranking.md
working/topic_evidence_map.md
working/cheatsheet_content.md
  -> build_html.py
outputs/cheatsheet_3col.html
outputs/cheatsheet_4col.html
  -> optional browser PDF export
```

`build_html.py` 只会把已有的 `working/cheatsheet_content.md` 文件渲染成 HTML。它不会分析课程资料，也不会决定主题重要性。

## 要求

推荐使用 Python 3.9+。

`requirements.txt` 中的依赖是可选的文本提取辅助工具：

```text
pymupdf
python-pptx
python-docx
```

只有当你需要完整的 PDF、PPTX 和 DOCX 文本提取支持时才安装它们。

OCR 有意不包含在范围内。没有可选中文本的扫描版 PDF 会被报告为没有可提取文本。

## 版权说明

不要把以下内容提交到公开仓库：

- 受版权保护的课程资料；
- 从课程资料中提取的文本；
- 基于私人课程资料生成的 `working/` 文件；
- 基于私人课程资料生成的 `outputs/` 文件。

仓库中的 `courses/COURSE_NAME/` 文件夹应该保持为空 scaffold。除非你有权发布源资料和生成的衍生内容，否则请保持真实课程项目私有。

## 许可证

MIT License。请查看 [LICENSE](LICENSE)。


---

# course-cheatsheet-maker

`course-cheatsheet-maker` is an installable Codex-style skill for turning course materials into compact A4 landscape cheatsheets.

It helps a coding agent:

- extract text from PDF, PPTX, DOCX, TXT, and Markdown course files;
- separate knowledge sources from question-like sources;
- build traceable candidate knowledge units;
- rank topic importance from course emphasis and assessment evidence;
- create reviewable working files before rendering;
- render printable 3-column and 4-column HTML cheatsheets.

HTML/CSS is the source of truth for layout. PDF export is optional and is usually done from the browser print dialog.

## What This Repository Contains

This GitHub repository contains two things:

1. the reusable runtime skill package files; and
2. a starter course scaffold at `courses/COURSE_NAME/`.

The starter scaffold is included so first-time users can see the required course folder shape without creating every folder by hand. It is not a real course, and it should not contain public course materials.

Hidden `.gitkeep` files inside `courses/COURSE_NAME/` are allowed. They only keep empty starter scaffold folders tracked by Git; they are not real course materials and do not count as generated outputs.

Repository documentation files such as `README.md`, `QUICK_START.md`, and `INSTALL.md` are for GitHub users and installers only. They belong in this repository, but they are not part of the installed runtime skill folder.

## Repository Structure

The public repository may include documentation and repository metadata:

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
  README.md
  QUICK_START.md
  INSTALL.md
  LICENSE
  .gitignore
```

Path roles:

| Path | Purpose |
|---|---|
| `SKILL.md` | Core skill instructions used by Codex or another coding agent. |
| `requirements.txt` | Optional Python extraction dependencies. |
| `scripts/` | Helper scripts for extraction, candidate-unit building, HTML rendering, PDF guidance, and validation. |
| `assets/` | HTML templates and rendering assets. |
| `references/` | Rubrics and guidance used by the skill. |
| `courses/COURSE_NAME/` | Empty starter scaffold for first-time users. |
| `README.md`, `QUICK_START.md`, `INSTALL.md` | Repository documentation only. Do not copy these into the installed runtime skill folder. |

## Installed Skill Structure

After installation, the global skill folder should contain only the runtime package:

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

The installed skill folder should not include repository-only files such as `README.md`, `QUICK_START.md`, `INSTALL.md`, `LICENSE`, `.gitignore`, `.git/`, or `__pycache__/`.

## Skill Location vs. Course Project Location

Keep these two locations separate:

1. **Global skill installation folder**: contains the reusable skill package and the empty `courses/COURSE_NAME/` scaffold.
2. **Private course project folder**: contains your real lecture notes, slides, quizzes, past papers, generated working files, and generated outputs.

Typical global skill location:

```text
~/.agents/skills/course-cheatsheet-maker/
```

On Windows, this usually corresponds to:

```text
C:\Users\<your-username>\.agents\skills\course-cheatsheet-maker\
```

Real course materials should live in your own private course project, not inside the global skill install directory. A private course project can look like this:

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
Important: `COMP7503` is only an example. Replace it with your real course folder name everywhere.
Use the installed `courses/COURSE_NAME/` scaffold as a template. Copy it into your private course project and rename the copy to your real course name, such as `COMP7503`, `MATH101`, or `DATABASE`.

## Quick Use

See [QUICK_START.md](QUICK_START.md) for the first-run guide. The short version is:

1. Install the skill by following [INSTALL.md](INSTALL.md).
2. Copy `~/.agents/skills/course-cheatsheet-maker/courses/COURSE_NAME/` into your own course project, for example `courses/COMP7503/`.
3. Put materials into:

```text
courses/COMP7503/materials/knowledge/
courses/COMP7503/materials/questions/
```

Important: `COMP7503` is only an example. Replace it with your real course folder name everywhere.

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

5. Check the generated HTML files:

```text
courses/COMP7503/outputs/cheatsheet_3col.html
courses/COMP7503/outputs/cheatsheet_4col.html
```

## Where Course Materials Go

Put knowledge sources in:

```text
courses/COURSE_NAME/materials/knowledge/
```

Good `knowledge/` sources include lecture slides, lecture notes, handouts, textbook excerpts, tutorial explanations, and review notes.

Put question-like or assessment-related sources in:

```text
courses/COURSE_NAME/materials/questions/
```

Good `questions/` sources include quizzes, assignments, tutorial questions, workshop questions, problem sets, sample exams, mock exams, and past papers.

Subfolders inside `knowledge/` and `questions/` are supported.

## Parameter Overview

| Parameter | Values | Recommended Default | Meaning |
|---|---|---|---|
| `workflow_mode` | `safe-review`, `full-auto` | `full-auto` for first use | Controls automation level. |
| `layout` | `3col`, `4col` | `3col` | Preferred layout for review and validation. Full Auto still renders both HTML files. |
| `target_pages` | positive integer | `1` | Content budget, not an exact printed-page guarantee. |
| `coverage_mode` | `exam-compact`, `balanced-standard`, `comprehensive-review` | `balanced-standard` | Controls which topics are included. |
| `detail_mode` | `simple`, `balanced`, `detailed` | `balanced` | Controls how much detail included topics receive. |

Recommended presets:

| Use Case | Parameters |
|---|---|
| One-page exam cram sheet | `target_pages = 1`, `coverage_mode = exam-compact`, `detail_mode = simple` |
| Default review sheet | `target_pages = 1`, `coverage_mode = balanced-standard`, `detail_mode = balanced` |
| Two-page comprehensive review | `target_pages = 2`, `coverage_mode = comprehensive-review`, `detail_mode = balanced` |
| Review first, render later | `workflow_mode = safe-review`, other parameters as needed |

## Workflow Overview

```text
course materials
  -> extract_materials.py
working/extracted/
  -> build_candidate_units.py
working/candidate_units.jsonl
  -> Codex reasoning with SKILL.md
working/run_config.md
working/knowledge_units.md
working/topic_map.md
working/importance_ranking.md
working/topic_evidence_map.md
working/cheatsheet_content.md
  -> build_html.py
outputs/cheatsheet_3col.html
outputs/cheatsheet_4col.html
  -> optional browser PDF export
```

`build_html.py` only renders an existing `working/cheatsheet_content.md` file into HTML. It does not analyze course materials or decide topic importance.

## Requirements

Python 3.9+ is recommended.

The dependencies in `requirements.txt` are optional extraction helpers:

```text
pymupdf
python-pptx
python-docx
```

Install them only when you want full PDF, PPTX, and DOCX text extraction support.

OCR is intentionally out of scope. Scanned PDFs with no selectable text will be reported as having no extractable text.

## Copyright Note

Do not commit the following to a public repository:

- copyrighted course materials;
- text extracted from course materials;
- generated `working/` files based on private course materials;
- generated `outputs/` files based on private course materials.

The repository's `courses/COURSE_NAME/` folder should stay as an empty scaffold. Keep real course projects private unless you have permission to publish both the source materials and generated derivatives.

## License

MIT License. See [LICENSE](LICENSE).
