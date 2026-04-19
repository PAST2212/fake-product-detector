---
name: otto-reviews
description: German NLP analysis of OTTO.de reviews.
tools: Task
---

Run German-language review NLP via the `otto-review-analyst` agent.

## Usage
`/otto-reviews [article-number | otto.de URL]`

## Dispatch
Invoke `otto-review-analyst`. Raw review text is stored to `scraped/`; aggregated signals written to `otto-reviews/{article_number}_analysis.json`.

Enforce return contract: ONLY `{path, total_reviews, fake_topic_score, sentiment_mismatch_score, rating_inflation_gap}`. Never ask for review text back.

## Key German terms
`gefälscht`, `Fälschung`, `Nachahmung`, `Imitat`, `Plagiat`, `nicht original`, `andere Verpackung`. Full term list in the agent definition.

Cross-platform comparison with Idealo / Check24 / Trustpilot ratings to detect rating inflation.
