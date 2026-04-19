---
name: otto-listing
description: Extract OTTO.de product listing data.
tools: Task
---

Extract OTTO listing data via the `otto-product-researcher` agent.

## Usage
`/otto-listing [article-number | otto.de URL]`

## Dispatch
Invoke `otto-product-researcher`. The agent curl-fetches to `scraped/`, parses, and writes `otto-products/{article_number}_listing.json`.

Enforce return contract: ONLY `{path, seller_type, fulfillment_type, seller_id, price, brand}`. Never ask for full JSON or HTML back.

## Critical signals (seller_type, fulfillment_type)
- `OTTO` + `OTTO Versand` → lowest risk
- `Marketplace` + `Händlerversand` → elevated risk
- `multiple_sellers=true` → further elevated
