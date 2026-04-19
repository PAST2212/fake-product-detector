---
name: verdict
description: Generate the final counterfeit verdict for an Amazon ASIN.
tools: Task, Bash
---

Synthesize evidence into a final verdict via the `fake-product-classifier` agent.

## Usage
`/verdict [ASIN]`

## Dispatch
Invoke `fake-product-classifier`. The agent reads the four on-disk artifacts (listing, reviews, images, seller) and writes `verdicts/{asin}_verdict.json`.

The classifier loads `counterfeit-methodology` (weights, thresholds, category base rates) and `amazon-patterns` (FBA/FBM, hijacking) itself — do not restate them here.

Enforce return contract: ONLY `{path, verdict, confidence, composite_score, top_2_flags}`.

## Post-step (bash, after subagent returns)
```bash
python3 validate_verdict.py {asin} && python3 generate_report.py {asin}
```
`validate_verdict.py` fields + schema: `.claude/rules/api-conventions.md`. Fix any validator errors before the HTML report step.
