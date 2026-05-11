# Sample Style Notes

These examples show writing density and block style only. They are not course content and should not be copied into a real course cheatsheet unless the actual course materials support them.

## Dense Bilingual Blocks

[A] **CLT 中心极限定理**  
Def: iid/weakly dep + n large + finite Var => sample mean approx Normal.  
Formula: `Z=(Xbar-mu)/(sigma/sqrt(n)) ~ N(0,1)`; sigma unknown -> use `s`.  
Trap: n 大不自动解决 biased sampling; skew/heavy-tail 需要更大 n.

[A] **Hypothesis test 流程**  
Procedure: 写 H0/H1 -> choose statistic -> p-value -> compare alpha -> conclusion in context.  
Q: p-value 是什么? A: under H0, observing as/more extreme data 的概率.  
Trap: p-value 不是 H0 为真的概率.

[B] **Bias vs Variance**  
Compare: bias = systematic error; variance = sensitivity to sample.  
Trap: low training error + high test error => overfit/high variance.

## Compact Table Style

| Concept | Use when | Watch |
| --- | --- | --- |
| t-test | sigma unknown, mean inference | normal-ish / n enough |
| chi-square | counts/categories | expected count too small |

## Tone

- Keep lines short.
- Mix Chinese labels with English formulas/terms.
- Prefer symbols, arrows, and abbreviations after defining them once.
