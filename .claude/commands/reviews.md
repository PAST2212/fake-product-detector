---
name: reviews
description: NLP analysis of Amazon reviews for counterfeit signals.
tools: Task
---

Run review NLP via the `review-analyst` agent.

## Usage
`/reviews [ASIN | URL]`

## Dispatch
Invoke `review-analyst` with the ASIN. The agent fetches to `scraped/`, stores raw review text only on disk, and writes aggregated signals to `reviews/{asin}_analysis.json`.

Enforce return contract: ONLY `{path, total_reviews, fake_topic_score, sentiment_mismatch_score, top_flag}`. Never ask for review text or full JSON back.

## Notes
- Minimum 20 reviews for reliable scoring.
- "Fake" mentions may flag defective units, not counterfeits — the classifier handles category conditioning.
