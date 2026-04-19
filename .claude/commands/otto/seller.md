---
name: otto-seller
description: OTTO.de seller legitimacy, German regulatory, and ethics due diligence.
tools: Task
---

Investigate an OTTO seller via the `otto-seller-investigator` agent.

## Usage
`/otto-seller [seller-id | article-number]`

## Dispatch
Invoke `otto-seller-investigator`. If given an article number, the agent reads `seller_id` from the listing JSON. It curl-fetches the seller profile, parses, and writes `otto-sellers/{seller_id}_profile.json`.

Enforce return contract: ONLY `{path, seller_type, verified_seller, has_impressum, ethics_severity, top_risk_indicator}`. Never ask for the full profile back.

## German regulatory (preserve)
Impressum, VAT ID (`USt-IdNr.`), Handelsregister, CE/GS marking, GPSR responsible person. Load `otto-patterns` skill for full context.
