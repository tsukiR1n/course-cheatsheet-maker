# Content Compression Rules

Compress from the already completed `knowledge_units.md`, `topic_map.md`, and `importance_ranking.md`. Do not introduce new source-folder assumptions during compression.

Compress according to the selected integer `target_pages`, `coverage_mode`, and `detail_mode`. Every item should help answer, compute, compare, remember a core concept, connect a lecture-covered idea, or avoid a trap.

Full Auto is not a compression mode. Use `exam-compact` only for explicitly exam-focused, ultra-compact, or exam-only requests. A one-page request sets `target_pages = 1`; it does not automatically change `coverage_mode` unless the user also asks for exam-focused content.

`target_pages` is a bounded content/page budget, not an exact printed-page guarantee, and must be an integer in scripts and artifacts. User-facing "4+" means `target_pages >= 4`. It controls total capacity only; it must not directly change `detail_mode`.

## Keep

- Formulas with variable meanings, conditions, and units.
- Definitions that separate similar concepts.
- Procedures and decision rules.
- Comparison points.
- Traps, edge cases, and common mistakes.
- Short Q&A blocks for likely recall or application prompts.
- Representative high-coverage lecture concepts required by `coverage_mode`.
- Compact example banks when the topic type is `backup_example`.

## Cut

- Motivation, history, and long prose.
- Repeated wording from source material.
- Examples that do not show a reusable pattern.
- Unsupported exam predictions.

## Page Budget Policy

- `target_pages = 1`: 3col floor 14k chars, target 16k-18k, soft ceiling 20k, hard ceiling 22k; topic target 35-45; all A compact, selected high-value B, C 0-3 representative, R omit.
- `target_pages = 2`: 3col floor 34k chars, target 36k-38k, soft ceiling 40k, hard ceiling 41k; topic target 75-85; all A, most important B, C 6-12 representative, R omit.
- `target_pages = 3`: 3col floor 44k chars, target 48k-52k, soft ceiling 55k, hard ceiling 58k; topic target 95-115; all A, nearly all B, C 18-30 representative/useful, R 0-3 useful reference items only.
- `target_pages = 4`: 3col floor 60k chars, target 64k-70k, soft ceiling 74k, hard ceiling 78k; topic target 115-135.
- `target_pages = 5`: 3col floor 76k chars, target 82k-88k, soft ceiling 93k, hard ceiling 98k; topic target 130-150.
- `target_pages = 6`: 3col floor 92k chars, target 100k-108k, soft ceiling 114k, hard ceiling 120k; topic target 145-170.

These are guidance ranges, not hard content-generation requirements. Do not invent topics just to hit a topic count. If available candidate units are fewer than the topic target, use remaining space for compact examples, traps, comparisons, and Q/A.

For a fixed `detail_mode`, increasing `target_pages` should first increase topic coverage. After coverage is sufficient, extra space can be used for high-value support blocks: traps, compact examples, comparison tables, and Q/A. `target_pages=6` with `detail_mode=balanced` should still use balanced topic writing, not automatically turn every topic into detailed prose.

When `target_pages` is fixed, `detail_mode` controls per-topic expansion depth:

- `simple`: shorter explanations, so more topics can fit.
- `balanced`: balance topic coverage and explanation depth.
- `detailed`: A/B topics get fuller explanations, examples, traps, and comparisons; fewer C topics may fit.

If content under-fills `target_pages`, do not add filler. Expand in this order: missing A/B topics, representative C topics, common traps and confusions, compact examples, comparison tables, then Q/A blocks. If content risks overflowing, preserve the requested detail level for A topics first, then compress B/C topics and optional examples.

Page-budget validation uses calibrated `3col` character ranges for `target_pages` 1-6. For `target_pages > 6`, validation uses conservative extrapolation and warns that the range is less calibrated. For `4col`, keep the older column-slot heuristic and treat it as less tested than `3col`. Optional print-page validation is final verification; normal generation should primarily use calibrated character ranges and should not repeatedly loop through expensive print checks unless requested.

For `coverage_mode = comprehensive-review` and `target_pages >= 2`, include representative C topics if meaningful C candidates exist. Do not reduce C topics to zero unless there are no meaningful C candidates. Compress repeated examples, repeated traps, and Q/A before removing all representative C topics.

If content risks overflowing `target_pages`, preserve formulas, definitions, traps, and core procedures before examples. Keep A topics, compress B topics, include representative C topics, and omit R topics.

Do not over-merge candidate units into very broad topics, especially when `target_pages >= 2`, `coverage_mode = comprehensive-review`, or `detail_mode = detailed`. Preserve useful subtopics as selectable units when they support better page-budget selection.

## Bilingual Style

Prefer compact Chinese-English mixed notes when it improves density:

- `Def: consistency 一致性: n↑ 时 estimator -> true value; 不等于 unbiased.`
- `Formula: Var(aX+bY)=a^2Var(X)+b^2Var(Y)+2abCov(X,Y).`
- `Trap: p-value 小 => reject H0; 不是 H0 为假的概率.`
- `Q: 什么时候用 CLT? A: n large + independent-ish + finite variance.`

## Block Types

Valid bilingual Topic headings should use real UTF-8 Chinese, for example `Topic: Raw bit rate and file size / 原始比特率与文件大小 [A]` or `Topic: Entropy / 信息熵 [A]`. Use compact English-first body text unless full Chinese is requested. Do not accept mojibake labels such as `姣旂壒鐜囦笌...` as valid Chinese output.

- `Topic:` topic label or section cue.
- `Formula:` equation, conditions, variable meanings.
- `Def:` short definition plus contrast.
- `Trap:` common error or edge case.
- `Compare:` A vs B, use-when, key difference.
- `Procedure:` ordered solving steps.
- `Q:` and `A:` short exam-retrieval pair.

## Compact Inline Labels

Write cue labels and content on the same line whenever possible. The renderer treats these as compact inline rows with a bold label followed immediately by the content:

- `Def: content`
- `Formula: content`
- `Trap: content`
- `Q: content`
- `A: content`
- `Compare: content`
- `Procedure: content`

Do not write these labels as separate headings followed by a paragraph. Prefer one dense line per retrievable fact, formula, trap, comparison, or step sequence. Keep wording short enough to fit within the A4 3-column or 4-column layout without large vertical gaps.

## Priority Labels

Use priority labels in content when useful:

- `[A]` high evidence; must fit if possible.
- `[B]` solid evidence; include if space allows.
- `[C]` compact reminder.
- `[R]` reserve/omit unless there is space.

## Coverage Budgets

These are guidance, not hard limits:

- `exam-compact`: 70% core exam topics, 15% lecture coverage topics, 10% traps/formulas/comparisons, 5% backup examples.
- `balanced-standard`: 50% core exam topics, 25% lecture coverage topics, 15% backup examples, 10% traps/formulas/comparisons.
- `comprehensive-review`: 35% core exam topics, 35% lecture coverage topics, 20% backup examples, 10% traps/formulas/comparisons.

Formula-heavy courses may devote more space to formulas. Example-heavy courses may devote more space to backup examples.
