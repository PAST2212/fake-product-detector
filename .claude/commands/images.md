---
name: images
description: Reverse image search and image forensics.
tools: Task
---

Run image forensics via the `image-forensics` agent.

## Usage
`/images [ASIN | URL]`

## Dispatch
Invoke `image-forensics` with the ASIN. The agent reads image URLs from `products/{asin}_listing.json`, downloads ≤3 to `images/{asin}/`, computes hashes, runs gated reverse search (brand site → marketplaces), and writes `images/{asin}_forensics.json`.

Enforce return contract: ONLY `{path, brand_site_match, unauthorized_marketplace_matches_count, overall_image_risk_score}`. Never ask for hashes, URLs, or HTML back.

## Gating
Reverse image search is expensive. The agent runs brand/authorized-retailer checks first, and escalates to AliExpress/DHgate/Temu only if cheaper signals flag the product.
