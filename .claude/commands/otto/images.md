---
name: otto-images
description: Image forensics and reverse search for OTTO.de products.
tools: Task
---

Run image forensics via the `otto-image-forensics` agent.

## Usage
`/otto-images [article-number | otto.de URL]`

## Dispatch
Invoke `otto-image-forensics`. The agent reads image IDs from `otto-products/{article_number}_listing.json`, downloads ≤3 images via `curl`, computes perceptual hashes, runs gated reverse search, and writes `otto-images/{article_number}_forensics.json`.

Enforce return contract: ONLY `{path, brand_site_match, unauthorized_matches_count, overall_image_risk_score}`. Never ask for hashes or URLs back.

## Gating
Brand / Idealo / Check24 first (cheap, authorized-EU). AliExpress / DHgate / Temu via Yandex only if other signals are already suspicious.
