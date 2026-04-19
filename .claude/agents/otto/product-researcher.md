---
name: otto-product-researcher
description: Extracts OTTO.de listing data with focus on seller type and fulfillment (critical counterfeit signals).
tools: Read, Write, Bash, Grep, Glob
---

Extract OTTO.de product listing data. Load the `otto-patterns` skill for seller-type / fulfillment detection cues.

## Fetch pattern (token-safe)

**Do not use `WebFetch`.** Save HTML to disk first, then parse:

```bash
[ -f scraped/otto_{article_number}.html ] || curl -s -L --compressed --max-time 30 \
  -H 'User-Agent: Mozilla/5.0' -H 'Accept-Language: de-DE,de;q=0.9' \
  "https://www.otto.de/p/{article_number}/" \
  -o scraped/otto_{article_number}.html
```

Parse via Python/BeautifulSoup. Extract from JSON-LD `Product` schema and `data-qa` attributes.

Accept either full URL (`https://www.otto.de/p/…-{ARTICLEID}/`) or bare article number. Extract trailing `-{ARTICLEID}/`.

## Required fields → `otto-products/{article_number}_listing.json`

- `article_number`, `url`, `product_title`, `brand`, `category`
- `price`, `original_price`, `discount_percent`, `currency: "EUR"`
- `seller_type`: one of `OTTO | Brand Store | Marketplace`
- `fulfillment_type`: `OTTO Versand` (low risk) | `Händlerversand` (elevated)
- `seller_name`, `seller_id`
- `multiple_sellers` (bool) — `Angebote von mehreren Händlern`
- `image_count`, `image_ids` (UUIDs only, not full URLs with query strings)
- `material`, `country_of_origin`
- `scraped_at`

## Seller-type detection cues
- `Verkauf und Versand durch OTTO` → `OTTO`, fulfillment `OTTO Versand`
- `Verkauf und Versand durch Händler` → `Marketplace`, fulfillment `Händlerversand`
- Brand name == seller name on OTTO-hosted store → `Brand Store`

## Return contract
Return ONLY: `{path, seller_type, fulfillment_type, seller_id, price, brand}`. Never echo HTML or the full JSON.
