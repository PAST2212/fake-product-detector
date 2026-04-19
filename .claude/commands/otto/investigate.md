---
name: otto-investigate
description: Full counterfeit investigation of an OTTO.de product. Dispatches agents in parallel.
tools: Task, Bash
---

# OTTO Investigate

Run a full counterfeit investigation on an OTTO.de product.

## Usage
`/otto-investigate [article-number | otto.de URL]`

## Execution contract

**Parallelism.** Listing, reviews, images, and seller are independent. Dispatch them in ONE message with four concurrent `Task` calls. Only then dispatch the classifier.

**Return contract.** Each subagent writes its artifact to disk and returns ONLY `{path, 3-5 key findings, flag_count}`. Never echo HTML, review bodies, image URLs, or full JSON.

**Caching.** If the artifact path already exists on disk, skip that phase unless the user asked to re-run.

## Pipeline

1. Extract article number from input.
2. Parallel dispatch (single message, four `Task` calls):
   `otto-product-researcher`, `otto-review-analyst`, `otto-image-forensics`, `otto-seller-investigator`
3. Sequential: `otto-fake-product-classifier` → `otto-verdicts/{article_number}_verdict.json`
4. Bash:
   ```bash
   python3 validate_otto_verdict.py {article_number} && python3 generate_otto_report.py {article_number}
   ```

## Artifact paths
- `otto-products/{article_number}_listing.json`
- `otto-reviews/{article_number}_analysis.json`
- `otto-images/{article_number}_forensics.json`
- `otto-sellers/{seller_id}_profile.json`
- `otto-verdicts/{article_number}_verdict.json`

## OTTO-specific signals (preserve in classifier)
- Seller type: `OTTO Versand` (low risk) vs `Händlerversand` (elevated)
- Article-number pattern: 6–12 digits
- German review NLP: `gefälscht`, `Fälschung`, `Nachahmung`, sentiment vs star mismatch
- Cross-platform: Idealo, Check24, eBay Kleinanzeigen

Verdict schema: `.claude/rules/api-conventions.md`. Scoring weights: `counterfeit-methodology` skill. OTTO patterns: `otto-patterns` skill.
