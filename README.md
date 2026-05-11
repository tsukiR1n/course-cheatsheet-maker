# course-cheatsheet-maker

一个可安装的 Codex 风格 skill，用于根据课程材料生成紧凑的 A4 横版课程 cheatsheet。

这个 skill 可以帮助 Agent：

- 从课程材料中提取文本；
- 构建可追溯的候选知识单元；
- 根据知识材料和题目类材料推断 topic 重要性；
- 生成复习用的中间分析产物；
- 渲染 3 栏和 4 栏的可打印 HTML cheatsheet。

HTML/CSS 是最终版式的 source of truth。PDF 导出是可选的，应尽量保持 HTML 打印版式不变。

## 可安装的 Skill 仓库

这个仓库用于作为 skill 安装，可以安装到全局 skills 目录，也可以安装到某个项目的 skills 目录中。

安装后的 skill 目录中必须直接包含 `SKILL.md`：

```text
course-cheatsheet-maker/
  SKILL.md
  requirements.txt
  scripts/
  assets/
  references/

对于 Codex 风格的设置，常见的全局安装位置是：

~/.agents/skills/course-cheatsheet-maker/

安装和验证步骤请查看 INSTALL.md。

新手使用流程
按照 INSTALL.md 安装这个 skill。
新建一个单独的课程项目。
将课程材料放入：
courses/COURSE_NAME/materials/knowledge/
courses/COURSE_NAME/materials/questions/
让 Codex 使用 $course-cheatsheet-maker。
在 courses/COURSE_NAME/outputs/ 中查看生成的 HTML 文件。
课程材料应该放在哪里

不要把真实课程材料放进这个公开 skill 仓库。

这个 skill 应该安装到全局 skills 目录，或者安装到单独项目的 skills 目录中。你的真实课程材料应该放在你自己的课程项目里，结构如下：

courses/COURSE_NAME/
  materials/
    knowledge/
    questions/
  working/
  outputs/

将 lecture notes、slides、textbook excerpts 和其他知识类材料放入：

materials/knowledge/

将 quiz、assignment、tutorial、workshop、problem set、sample exam 和 past paper 类材料放入：

materials/questions/

knowledge/ 和 questions/ 内部支持继续创建子文件夹。

重要版权提醒

不要将有版权的课程材料、提取后的课程文本、基于私有材料生成的 working 文件，或最终渲染出的课程输出提交到这个公开 skill 仓库中。

真实课程项目应保持私有，除非你已经获得发布源材料和衍生产物的授权。

examples/ 目录只包含空占位文件，用于展示推荐的课程文件夹结构。

快速开始

安装 skill 后，请新建一个单独的课程项目，并从该课程项目根目录运行脚本，或者显式传入 --root 参数。

Unix 和 Windows PowerShell 示例请查看 QUICK_START.md。

环境要求

推荐使用 Python 3.9+。

可选的文本提取依赖列在 requirements.txt 中：

pymupdf
python-pptx
python-docx

OCR 暂不属于本 skill 的范围。对于没有可选中文本的扫描版 PDF，脚本会报告该文件没有可提取文本。

License

MIT License。详情见 LICENSE。

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
