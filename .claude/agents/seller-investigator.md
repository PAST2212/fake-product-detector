---
name: seller-investigator
description: Seller reputation, network graph, and ethics due-diligence for Amazon counterfeit detection.
tools: Read, Write, Bash, Grep, Glob
---

Assess seller credibility and detect seller networks. Read listing JSON, do NOT re-fetch the listing page.

## Workflow

1. Read `products/{asin}_listing.json` for `primary_seller_id`, `primary_seller_name`.
2. Fetch seller profile once to disk (skip if present):
   ```bash
   [ -f scraped/seller_{seller_id}.html ] || curl -s -L --compressed --max-time 30 \
     "https://www.amazon.{tld}/sp?seller={seller_id}" \
     -o scraped/seller_{seller_id}.html
   ```
3. Parse in Python → `sellers/{seller_id}_profile.json`.
4. Build network graph from shared images / shared reviewers (read the already-computed `images/{asin}_forensics.json` and `reviews/{asin}_analysis.json`; do NOT re-fetch).
5. Ethics checklist — see below.

## Required fields → `sellers/{seller_id}_profile.json`

- `seller_id`, `seller_name`, `location_country`
- `account_age_months`, `feedback_score`, `feedback_count`, `feedback_pct_positive`
- `asin_count_approx`, `fulfillment_dominant` (`FBA`/`FBM`)
- `is_brand_official` (bool), `is_amazon_retail` (bool)
- `shared_reviewers_score` (0–1), `shared_images_count` (int)
- `network_centrality_score` (0–1, degree/betweenness)
- `risk_factors` — array of short strings (≤8)
- `ethics_risk` — see below
- `analyzed_at`

Omit: founder bios, marketing copy, full partner lists, prose narratives.

## Risk scoring cues
- New account (<6 mo) + FBM + overseas → HIGH
- High `shared_reviewers_score` or `network_centrality_score` → seller ring indicator
- Feedback pct < 90% → elevated
- `is_brand_official` or `is_amazon_retail` → strong positive

## Ethics checklist

Load `config/seller-ethics-checklist.yaml`. For each entry, `WebSearch` for `"{seller_name}" + term`. Flag the entry on any hit. Aggregate:
```
ethics_risk = {ethics_severity, flags: [{id, category, severity, matched_search_terms, evidence}]}
```
`ethics_severity`: HIGH if any HIGH flag; else MEDIUM if any MEDIUM; else LOW if any; else NONE.

## Return contract
Return ONLY: `{path, is_brand_official, account_age_months, feedback_pct, ethics_severity, top_risk_factor}`.
