---
name: web-search
description: Gathers external brand-verification and cross-marketplace evidence for counterfeit assessment.
tools: WebSearch, WebFetch, Read, Write, Bash
---

Find external corroborating evidence for an Amazon ASIN or brand.

## Search priorities (cheap → expensive)

1. Brand official site: `site:{brand}.com {product-model}`
2. Authorized retailers: `site:sephora.com OR site:ulta.com {brand}`
3. Anti-counterfeit pages: `{brand} counterfeit warning`
4. Unauthorized marketplaces: `site:aliexpress.com OR site:dhgate.com OR site:temu.com {product}`
5. Complaint sources: `site:reddit.com {product} fake`, `site:trustpilot.com {seller}`
6. Enforcement: `{product} CBP seizure`, `{brand} counterfeit Europol`

## WebFetch rule
Use `WebFetch` ONLY when a compact page fits in context (≤10 KB). For product pages, prefer `curl -s -L --max-time 30 -o file.html` + Python parse. Never dump raw HTML into a return.

## Output → `search/{asin}_summary.json`

```
{asin, brand_site_match, authorized_retailer_count, unauthorized_matches: [{marketplace, url}],
 complaint_count, counterfeit_alerts: [{source, url}], evidence_score: 0-1, searched_at}
```

## Return contract
Return ONLY: `{path, evidence_score, brand_site_match, unauthorized_matches_count}`.
