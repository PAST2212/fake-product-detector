---
name: investigate
description: Full counterfeit investigation for Amazon or OTTO.de products. Auto-detects platform and dispatches agents in parallel.
tools: Task, Bash
---

# Investigate

Run a full counterfeit investigation. Auto-detects Amazon vs OTTO.de from input.

## Usage
`/investigate [ASIN | article-number | product URL]`

## Platform detection
- Amazon: URL contains `amazon.` OR input matches `B0[A-Z0-9]{7,10}`
- OTTO: URL contains `otto.de` OR input is 6–12 digits

## Execution contract (read this before dispatching)

**Parallelism.** Listing, reviews, images, and seller are independent. Dispatch them in ONE message with four concurrent `Task` calls. Only then dispatch the classifier.

**Return contract for every subagent.** Each phase command already enforces this — do NOT paraphrase it back into the dispatch prompt. Each subagent must:
1. Write its artifact to the documented path on disk.
2. Return ONLY: `{path, 3-5 key findings, flag_count}`.
3. NEVER echo scraped HTML, review bodies, image URLs, or full JSON.

**Do NOT re-invoke sub-commands (`/listing`, `/reviews`, etc.).** Dispatch the named agent via `Task` directly. Sub-commands exist for standalone use, not orchestration.

**Caching.** If the artifact path already exists on disk, skip that phase unless the user asked to re-run.

## Pipeline

1. **Detect platform** from the input. Set `{id}` = ASIN or article number.
2. **Parallel dispatch** (single message, four Task calls):
   - Amazon: `product-researcher`, `review-analyst`, `image-forensics`, `seller-investigator`
   - OTTO: `otto-product-researcher`, `otto-review-analyst`, `otto-image-forensics`, `otto-seller-investigator`
3. **Classifier** (sequential, after step 2 completes):
   - Amazon: `fake-product-classifier` → `verdicts/{id}_verdict.json`
   - OTTO: `otto-fake-product-classifier` → `otto-verdicts/{id}_verdict.json`
4. **Validate + report** (bash, sequential):
   ```bash
   # Amazon
   python3 validate_verdict.py {id} && python3 generate_report.py {id}
   # OTTO
   python3 validate_otto_verdict.py {id} && python3 generate_otto_report.py {id}
   ```

## Artifact paths

| Phase | Amazon | OTTO |
|-------|--------|------|
| Listing | `products/{id}_listing.json` | `otto-products/{id}_listing.json` |
| Reviews | `reviews/{id}_analysis.json` | `otto-reviews/{id}_analysis.json` |
| Images | `images/{id}_forensics.json` | `otto-images/{id}_forensics.json` |
| Seller | `sellers/{seller_id}_profile.json` | `otto-sellers/{seller_id}_profile.json` |
| Verdict | `verdicts/{id}_verdict.json` | `otto-verdicts/{id}_verdict.json` |

Verdict schema lives in `.claude/rules/api-conventions.md` — do not re-specify it here.

## Notes
- Ethics checklist: seller agents load `config/seller-ethics-checklist.yaml` themselves.
- Scoring weights: classifier loads `counterfeit-methodology` skill itself.
- Platform patterns: classifier loads `amazon-patterns` or `otto-patterns` itself.
