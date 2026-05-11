# Importance Rubric

Use this rubric while writing `working/importance_ranking.md`. The ranking is an evidence-based prioritization, not an exam prediction.

## Source Model

Real courses use only two material folders:

- `materials/knowledge/`: course knowledge and emphasis sources.
- `materials/questions/`: assessment-like and practice sources whose specific type must be inferred.

Do not ask the user to split materials into detailed source-type folders. Use extracted text and source locators whenever available. Do not infer detailed document content from filenames alone.

Use five independent run parameters:

- `workflow_mode`: `safe-review` or `full-auto`; controlled by the user request or CLI `--mode` and used only for automation.
- `layout`: `3col` or `4col`; used for preferred review/validation layout. Full Auto still renders both HTML outputs.
- `target_pages`: integer bounded content/page budget. User-facing "4+" means `target_pages >= 4`; scripts and `run_config.md` record an integer. It controls total capacity, not per-topic detail.
- `coverage_mode`: `exam-compact`, `balanced-standard`, or `comprehensive-review`; controls topic inclusion. Default to `balanced-standard` when unspecified.
- `detail_mode`: `detailed`, `balanced`, or `simple`; controls verbosity of included topics. Default to `balanced` when unspecified.

Full Auto is not a content compactness signal. It only means the workflow continues through rendering and validation.

Resolve parameters and write `working/run_config.md` before extraction. Defaults are `workflow_mode=safe-review`, `layout=3col`, `target_pages=1`, `coverage_mode=balanced-standard`, and `detail_mode=balanced`. If the user asks for comprehensive/full review, cover all slides, or 全面复习 without a page count, use `coverage_mode=comprehensive-review` and `target_pages=2`, while keeping `detail_mode=balanced` unless detailed output is explicit.

Candidate units can include both knowledge and question extracted files, but every unit must distinguish `source_folder`, `inferred_source_type`, and `unit_role`. Treat question units as exam/practice evidence, not as normal lecture concepts.

## Source-Type Inference In `questions/`

Infer likely source type from filenames and extracted content:

| Signal | Inferred source type | Evidence strength |
| --- | --- | --- |
| `past_paper`, `final_exam`, `exam_2021` | Past/final exam | Strongest question evidence |
| `sample_exam`, `mock_exam`, `practice_exam` | Sample/mock/practice exam | Strongest or high question evidence |
| `quiz`, `weekly_quiz` | Quiz | Strong testability evidence |
| `assignment`, `homework` | Assignment | Medium-to-strong practice evidence |
| `problem_set`, `exercise_sheet` | Problem set/exercise sheet | Medium-to-strong practice evidence |
| `workshop` | Workshop | Practice evidence |
| `tutorial` | Tutorial | Practice evidence |
| unclear name or mixed content | Unknown question source | Weak-to-medium evidence only |

If extracted content contradicts the filename, prefer the content and record the uncertainty. Unknown question sources cannot exceed priority B unless extracted content clearly proves exam, quiz, assignment, tutorial, workshop, or problem-set structure.

## Coverage Modes

- `exam-compact`: A topics must be included; B topics should fit if space allows; C topics only if space allows; R topics omitted. Past/final/sample/mock exam evidence has strongest influence. Lecture-only topics may be compressed or omitted unless foundational.
- `balanced-standard`: default. A topics must be included; B topics should be included; C topics should be representatively included; R topics omitted. Lecture coverage decides minimum inclusion. Exam evidence strongly increases priority and usually justifies expanded treatment.
- `comprehensive-review`: not constrained to one A4 page. A and B topics must be included; C topics should be included if useful; R topics are generally omitted unless useful as appendix/reference material.

## Target Pages

Use `target_pages` as total bounded capacity, not an exact printed-page guarantee and not a signal to change `detail_mode`.

- `target_pages = 1`: 3col floor 14k chars, target 16k-18k; all A compact, selected high-value B, C 0-3 representative, R omit.
- `target_pages = 2`: 3col floor 34k chars, target 36k-38k; all A, most important B, C 6-12 representative, R omit.
- `target_pages = 3`: 3col floor 44k chars, target 48k-52k; all A, nearly all B, C 18-30 representative/useful, R 0-3 useful reference items only.
- `target_pages = 4-6`: progressively broader coverage; A and B all or nearly all, C most meaningful/useful topics, R useful reference/appendix items only.

For `coverage_mode = comprehensive-review` and `target_pages >= 2`, include representative C topics if meaningful C candidates exist. Do not reduce C topics to zero unless there are no meaningful C candidates; compress repeated examples, repeated traps, and Q/A first.

Coverage floor: each major knowledge PDF should normally have at least 2-4 represented concepts unless it is administrative, repetitive, or low-testability. The floor is a minimum safeguard, not a maximum cap. It must never cap A/B topics or high-importance lecture concepts.

## Topic Types

- `core_exam`: supported by question evidence and lectures; usually formulas, procedures, traps, and worked examples.
- `lecture_coverage`: heavily covered in lectures but little/no exam evidence; usually definitions, comparisons, mechanisms, or applications.
- `backup_example`: application cases, examples, or extended context; usually compact example-bank treatment.
- `foundational`: needed to understand later content; keep even if not directly examined.
- `administrative`: course logistics, grading, syllabus details; normally omitted from the cheatsheet.

## Score Dimensions

Score each topic from 0 to 3 in all five dimensions, for a total score out of 15.

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Lecture coverage | Absent from knowledge sources | Mentioned once or lightly | Repeated or clearly emphasized | Central across multiple knowledge sources or major lecture sections |
| Exam evidence | Absent from question sources | Appears only in unknown or weak practice source | Appears in quiz, assignment, tutorial, workshop, or problem set | Appears in past paper, final exam, sample exam, or mock exam |
| Testability/formula value | Hard to test directly | Definition-only or recognition-level | Short application, comparison, formula, or explanation possible | Multi-step calculation, algorithm, procedure, proof-like answer, or exam-style problem |
| Dependency | Isolated detail | Supports one local topic | Supports multiple topics | Foundational concept used across the course |
| Error risk | Straightforward | Minor detail risk | Common confusion or common mistake | Trap-heavy, formula-sensitive, unit-sensitive, or easily confused |

## Priority Bands

- A: total 11-15.
- B: total 7-10.
- C: total 4-6.
- R: total 0-3.

Priority equals importance only. Detail mode equals verbosity only. A topic must not be downgraded from A to B just because it can be summarized briefly. If the score is 11-15, keep Priority A and assign a compact recommended detail if the selected `detail_mode` requires it.

Allowed A overrides:

- If `Exam evidence = 3` and `Testability/formula value >= 2`, the topic can be A even if total score is slightly below 11.
- If `Lecture coverage = 3`, `Testability/formula value >= 2`, and `Dependency >= 2`, the topic can be A even without past-paper evidence.

Caps:

- Filename-only evidence cannot exceed C.
- Unknown question source evidence cannot exceed B unless extracted content clearly proves a stronger source structure.
- If extraction failed or evidence is incomplete, mark ranking and content preliminary.
- No topic may be described as guaranteed exam content.

Past paper, final exam, sample exam, and mock exam evidence is the strongest question evidence. Instructor review guides, final review slides, official revision checklists, and exam revision notes are high course-emphasis evidence, but still must not be described as guaranteed exam content.

Do not say "exam evidence decides detail level." Use this rule instead: lecture coverage decides minimum inclusion; exam evidence strongly increases priority and usually justifies expanded treatment; final verbosity is controlled by `detail_mode`.

Do not put source coverage directly into the importance score unless there is a strong reason. Prefer source coverage as a post-ranking review: after initial ranking, check whether each major source is represented, then promote the best candidate units from under-covered sources according to coverage mode and evidence quality.

## Detail Mode

Priority A/B/C/R determines importance and inclusion priority. Detail mode determines verbosity only.

Supported values:

- `detail_mode: detailed`
- `detail_mode: balanced`
- `detail_mode: simple`

| Priority | detailed | balanced | simple |
| --- | --- | --- | --- |
| A | detailed | detailed | detailed |
| B | detailed | detailed | simple |
| C | detailed | simple | minimal/simple |
| R | omit | omit | omit |

When the user does not specify a detail preference, use `detail_mode: balanced`. If the user asks for detailed output, use `detail_mode: detailed`. If the user asks for comprehensive output without explicitly asking for detailed explanations, keep `detail_mode: balanced` and use the comprehensive page default above. If the user asks for simple, concise, quick reference, 简洁, or 速查 output, use `detail_mode: simple`.

`target_pages` must not directly change `detail_mode`. For a fixed `detail_mode`, increasing `target_pages` should first increase topic coverage; after coverage is sufficient, add traps, compact examples, comparison tables, and Q/A. `target_pages=6` with `detail_mode=balanced` remains balanced writing, not detailed prose for every topic.

Page-budget validation is separate from A/B/C/R priority. Priority decides importance and inclusion pressure; it does not replace final checks that `cheatsheet_content.md` fills the requested printable page budget.

Do not add filler just to fill pages. If content under-fills the target, expand missing A/B topics first, then representative C topics, traps/confusions, compact examples, comparison tables, and Q/A blocks. If budget is tight, preserve requested detail for A topics first, then compress B/C topics and optional examples. Avoid over-merging candidate units into broad topics, especially when `target_pages >= 2`, `coverage_mode = comprehensive-review`, or `detail_mode = detailed`.

## Required Topic Format

Each ranked topic should include:

```text
Priority: A/B/C/R
Topic: English topic / 中文标签 [A]
Topic type: core_exam/lecture_coverage/backup_example/foundational/administrative
Scores: Lecture coverage=?, Exam evidence=?, Testability/formula value=?, Dependency=?, Error risk=?, Total=?
Evidence: brief source summary
Lecture coverage: low/medium/high with source IDs
Exam evidence: none/weak/medium/high with question source IDs
Recommended detail: detailed/simple/minimal/omit
Rationale: short reason
```

Use concise source summaries. Prefer source IDs and locators from `extraction_report.md` and extracted Markdown, such as `K01 Page 18-24` or `Q02 Slide 7`, when available.

Use concise bilingual topic labels by default in Topic lines, for example `Topic: Raw bit rate and file size / 原始比特率与文件大小 [A]`, `Topic: Entropy / 信息熵 [A]`, or `Topic: Huffman coding / 霍夫曼编码 [A]`. If the user asks in Chinese or requests Chinese/bilingual output, keep bilingual Topic headings. The Chinese part is a short lookup label only. Use compact English-first body text unless full Chinese is requested. Do not translate long explanations unless requested. If the user explicitly requests English-only output, bilingual labels may be omitted. Do not accept mojibake Topic labels such as `姣旂壒鐜囦笌...` as valid Chinese output.

If no past papers or sample exams are found in `questions/`, include this exact wording:

```text
没有提供往年卷，因此重要程度主要基于 PPT/Notes 强调、Quiz/Assignment/Workshop/Tutorial 出现频率、知识点基础性和可考性判断。
```

If materials are incomplete, state that the ranking is preliminary.

## Anti-Fabrication

- Never claim that a topic will definitely appear in the exam.
- Never invent past-paper patterns.
- Never treat a style reference as evidence.
- Do not quote long source passages in ranking or printable content.
- Cite evidence as source folder/source ID, inferred source type, and locator, not as unsupported certainty.
