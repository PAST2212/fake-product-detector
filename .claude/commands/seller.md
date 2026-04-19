---
name: seller
description: Amazon seller reputation, network analysis, and ethics due diligence.
tools: Task
---

Investigate an Amazon seller via the `seller-investigator` agent.

## Usage
`/seller [seller-id | ASIN]`

## Dispatch
Invoke `seller-investigator`. If given an ASIN, the agent reads `primary_seller_id` from `products/{asin}_listing.json`. The agent writes `sellers/{seller_id}_profile.json`.

Enforce return contract: ONLY `{path, is_brand_official, account_age_months, feedback_pct, ethics_severity, top_risk_factor}`. Never ask for the full profile JSON back.

## Ethics checklist
The agent loads `config/seller-ethics-checklist.yaml` and WebSearches `"{seller_name}" + term` for each entry. `ethics_severity` is computed from the highest-severity hit.
