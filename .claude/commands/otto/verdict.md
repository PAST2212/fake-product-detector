---
name: otto-verdict
description: Final counterfeit verdict for an OTTO.de product.
tools: Task, Bash
---

Synthesize OTTO evidence into a final verdict via the `otto-fake-product-classifier` agent.

## Usage
`/otto-verdict [article-number]`

## Dispatch
Invoke `otto-fake-product-classifier`. The agent reads the four on-disk artifacts (listing, reviews, images, seller) and writes `otto-verdicts/{article_number}_verdict.json`.

The classifier loads `counterfeit-methodology` and `otto-patterns` skills itself. Do not restate weights/thresholds here.

Enforce return contract: ONLY `{path, verdict, confidence, composite_score, top_2_flags}`.

## Post-step (bash)
```bash
python3 validate_otto_verdict.py {article_number} && python3 generate_otto_report.py {article_number}
```
Verdict schema: `.claude/rules/api-conventions.md`. Fix any validator errors before the HTML step.
