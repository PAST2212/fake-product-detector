---
name: listing
description: Extract Amazon product listing data.
tools: Task
---

Extract Amazon listing data via the `product-researcher` agent.

## Usage
`/listing [ASIN | URL]`

## Dispatch
Invoke the `product-researcher` subagent with the ASIN/URL. The agent handles fetching (`curl` to `scraped/{asin}.html`), parsing, and writing `products/{asin}_listing.json`.

Enforce the subagent's return contract: it must return ONLY `{path, seller_count, fulfillment_type, primary_seller_id, price, flags}`. Never ask for the full JSON or HTML back.

Output path: `products/{asin}_listing.json` (schema in `.claude/rules/api-conventions.md`).
