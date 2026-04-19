# API Conventions

## Verdict JSON Schema

These are the fields enforced by `validate_verdict.py` / `validate_otto_verdict.py`.
Changes here must be mirrored in the validators, and vice versa.

Required fields for Amazon verdict:
- `asin` — Amazon product ID (string)
- `product_title` — string
- `verdict` — `"LIKELY AUTHENTIC"`, `"LIKELY COUNTERFEIT"`, or `"UNCERTAIN"`
- `confidence` — float 0.0–1.0
- `composite_score` — float 0.0–1.0
- `risk_category` — one of `HIGH`, `MEDIUM`, `LOW`, `LOW-MEDIUM`, `MEDIUM-HIGH`

Recommended optional fields for Amazon verdict:
- `seller_id`, `primary_seller` — seller identifiers
- `brand`, `actual_brand`
- `risk_flags` — array of `{flag, severity, detail}` dicts (`severity` ∈ `HIGH`/`MEDIUM`/`LOW`)
- `evidence_summary` — `{for_authentic: [...], against_authentic: [...]}`
- `recommendations` — list of strings
- `scored_signals` / `score_breakdown` — scoring detail for the report
- `buying_verdict`, `sources`, `verdict_rationale`, `confidence_notes`, `key_finding`
- `analyzed_at` / `investigation_date`

Required fields for OTTO verdict:
- `article_number` — OTTO article number (string of 6–12 digits)
- `product_title` — string
- `verdict` — `"LIKELY AUTHENTIC"`, `"LIKELY COUNTERFEIT"`, or `"UNCERTAIN"`
- `confidence` — float 0.0–1.0
- `composite_score` — float 0.0–1.0
- `risk_category` — one of `HIGH`, `MEDIUM`, `LOW`, `LOW-MEDIUM`, `MEDIUM-HIGH`

Recommended optional fields for OTTO verdict:
- `seller` — seller display name
- `seller_type` — one of `"OTTO"`, `"Brand Store"`, `"Marketplace"` (who the seller is)
- `fulfillment_type` — `"OTTO Versand"` or `"Händlerversand"` (who ships)
- `brand`
- `risk_flags`, `evidence_summary`, `recommendations`, `scored_signals`,
  `score_breakdown`, `buying_verdict`, `sources`, `verdict_rationale`,
  `confidence_notes`, `key_finding`, `analyzed_at` / `investigation_date`

## Data Extraction

- Listing data → `{type}_listing.json`
- Review analysis → `{type}_analysis.json`
- Image forensics → `{type}_forensics.json`
- Seller profile → `{type}_profile.json`
