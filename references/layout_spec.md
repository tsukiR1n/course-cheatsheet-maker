# Layout Spec

HTML/CSS is the source of truth for the cheatsheet. The target is A4 landscape HTML that prints cleanly. Do not change template CSS, font sizes, spacing, or column layout to solve content underfill; selection and expansion are controlled by integer `target_pages`, `coverage_mode`, and `detail_mode`.

`layout` is `3col` or `4col`. Full Auto renders both HTML outputs, while `layout` tells validation and review which output is the primary target.

`target_pages` is an integer bounded content/page budget in scripts and artifacts. User-facing "4+" means `target_pages >= 4`. It is not an exact printed-page guarantee and must not directly change `detail_mode`.

## Font Stack

Use:

```css
"Calibri", "DengXian", "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif
```

## 3-Column Layout

- Page: A4 landscape.
- Margin: 5mm.
- Body font size: about 8.5px.
- Line height: about 1.02 to 1.06.
- Columns: 3.
- Column gap: about 3.5mm.

## 4-Column Layout

- Page: A4 landscape.
- Margin: 4.5mm to 5mm.
- Body font size: about 8px.
- Line height: about 1.00 to 1.04.
- Columns: 4.
- Column gap: about 2.8mm.

## Compact Inline Label Style

Render high-value cue lines as one-line compact paragraphs, not separate block headings. The label stays bold and visually distinct, and the content starts immediately after the label:

```html
<p class="compact-line definition"><strong>Def:</strong> content</p>
<p class="compact-line formula"><strong>Formula:</strong> content</p>
<p class="compact-line trap"><strong>Trap:</strong> content</p>
<p class="compact-line qa"><strong>Q:</strong> content</p>
<p class="compact-line qa"><strong>A:</strong> content</p>
<p class="compact-line compare"><strong>Compare:</strong> content</p>
<p class="compact-line procedure"><strong>Procedure:</strong> content</p>
```

Keep `.compact-line` margins and padding very small so labels and content read like fixed-line-height Word cheatsheet rows. Use narrow left borders or subtle backgrounds for scanning, but avoid large callout boxes.

## Required Classes

- `.topic`
- `.compact-line`
- `.definition`
- `.formula`
- `.compare`
- `.trap`
- `.qa`
- `.procedure`
- `.source-note`
- `.muted`
- `.priority-a`
- `.priority-b`
- `.priority-c`
- `.priority-r`

## Print Rules

- Keep backgrounds light and printable.
- Use narrow borders and compact spacing.
- Avoid decorative cards, large hero text, and screen-only interactions.
- Prefer dense formulas, short Chinese-English notes, compact Q&A, traps, and comparison points.
- Use `break-inside: avoid` for topic blocks, but allow long content to flow when needed.

## Coverage Budget Guidance

These ratios guide content planning before rendering; they are not hard CSS/page-fitting rules:

- `exam-compact`: 70% core exam topics, 15% lecture coverage topics, 10% traps/formulas/comparisons, 5% backup examples.
- `balanced-standard`: 50% core exam topics, 25% lecture coverage topics, 15% backup examples, 10% traps/formulas/comparisons.
- `comprehensive-review`: 35% core exam topics, 35% lecture coverage topics, 20% backup examples, 10% traps/formulas/comparisons.

## Page Budget Guidance

Calibrated `3col` character ranges:

| target_pages | floor | target range | soft ceiling | hard ceiling | topic target |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 14,000 | 16,000-18,000 | 20,000 | 22,000 | 35-45 |
| 2 | 34,000 | 36,000-38,000 | 40,000 | 41,000 | 75-85 |
| 3 | 44,000 | 48,000-52,000 | 55,000 | 58,000 | 95-115 |
| 4 | 60,000 | 64,000-70,000 | 74,000 | 78,000 | 115-135 |
| 5 | 76,000 | 82,000-88,000 | 93,000 | 98,000 | 130-150 |
| 6 | 92,000 | 100,000-108,000 | 114,000 | 120,000 | 145-170 |

These are guidance ranges, not hard content-generation requirements. Do not invent topics just to hit a topic count. For `target_pages > 6`, use conservative extrapolation and treat the result as less calibrated. For `4col`, keep the older column-slot heuristic and document it as less tested than `3col`.

For fixed `detail_mode`, increasing `target_pages` should first increase topic coverage, then add high-value traps, compact examples, comparison tables, and Q/A. If the page budget is tight, preserve requested detail for A topics first, then compress B/C topics and optional support blocks.

Optional print-page validation is final verification only. Normal generation should primarily use calibrated character ranges and should not repeatedly loop through expensive print checks unless explicitly requested.
