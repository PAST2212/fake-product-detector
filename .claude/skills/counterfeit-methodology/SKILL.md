---
name: counterfeit-methodology
description: Scoring framework, confidence thresholds, category base rates, and research-backed weights for counterfeit classification. Load when classifying a product or calculating a composite score.
---

# Counterfeit Scoring

## Weights (sum = 1.0; Composite = Σ weight × signal, each signal ∈ [0,1])

| Signal | Weight |
|--------|-------:|
| Fake topic score (review keywords) | 0.222 |
| Sentiment mismatch (stars vs text) | 0.167 |
| Unauthorized marketplace image match | 0.167 |
| Seller network centrality | 0.089 |
| Cross-ASIN / cross-listing image sharing | 0.089 |
| Shared reviewers | 0.078 |
| Account age | 0.056 |
| Feedback score | 0.056 |
| Seller count on listing | 0.044 |
| Price variance | 0.032 |

## Verdict thresholds

| Score | Verdict | Confidence |
|-------|---------|------------|
| <0.20 | LIKELY AUTHENTIC | High |
| 0.20–0.39 | LIKELY AUTHENTIC | Medium |
| 0.40–0.59 | UNCERTAIN | — |
| 0.60–0.79 | LIKELY COUNTERFEIT | Medium |
| ≥0.80 | LIKELY COUNTERFEIT | High |

Boundary 0.80 is inclusive. Never output confidence >0.95.

## Risk category mapping (from composite score)

| Composite   | `risk_category` |
|------------:|-----------------|
| < 0.20      | LOW             |
| 0.20 – 0.39 | LOW-MEDIUM      |
| 0.40 – 0.59 | MEDIUM          |
| 0.60 – 0.79 | MEDIUM-HIGH     |
| ≥ 0.80      | HIGH            |

## Category base rates + weight adjustments

| Category | Base rate | Upweight | Downweight |
|----------|-----------|----------|------------|
| Fragrances | HIGH | brand match, image forensics | — |
| Cosmetics | HIGH | fake topic, brand match | — |
| Electronics accessories | MEDIUM | image forensics | — |
| Clothing / Footwear | MEDIUM | cross-platform image match | — |
| Books | LOW | — | image forensics |
| Groceries | LOW | — | seller network |

## Key rules
- Price alone is a weak signal — counterfeits often price at or above authentic.
- Sentiment mismatch vs independent platforms (Trustpilot, PissedConsumer) is high-signal.
- Same image on AliExpress/DHgate/Temu at lower price → near-definitive counterfeit.
- High 1-star % + low 2-star % → suspicious distribution.
- If a signal's data file is missing → skip that term, reduce final confidence 10–15pp.
