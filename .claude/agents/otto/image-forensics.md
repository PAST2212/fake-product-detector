---
name: otto-image-forensics
description: Perceptual hashing and reverse search for OTTO.de product images.
tools: Read, Write, Bash, Grep, Glob
---

Detect stolen/counterfeit product images on OTTO.

## Workflow

1. Read `image_ids` from `otto-products/{article_number}_listing.json`.
2. Download ≤3 images:
   ```bash
   mkdir -p otto-images/{article_number}
   curl -sL --max-time 30 "https://i.otto.de/i/otto/{image_id}?w=1200" -o otto-images/{article_number}/img_{n}.jpg
   ```
3. Compute `phash`, `dhash`, `ahash`, `whash` via `imagehash` (Python).
4. Extract EXIF via PIL (`Make`, `Software`, `DateTimeOriginal`, `Copyright`).
5. Reverse search — gated by price/seller risk:
   - Cheap: brand site, Idealo, Check24 (EU / authorized).
   - Expensive (only if already suspicious): AliExpress, DHgate, Temu, eBay Kleinanzeigen via Yandex (best for Chinese sites).

## Cross-marketplace interpretation
- Same image on AliExpress/DHgate/Temu at fraction of price → strong counterfeit
- Same image on Amazon.de at similar price → likely legitimate multi-channel
- Image only on OTTO → ambiguous

## Required output → `otto-images/{article_number}_forensics.json`

- `article_number`, `image_count_analyzed`
- `phash_list`, `dhash_list` (hash strings only)
- `exif_summary: {has_exif, camera_make, software, has_copyright}`
- `brand_site_match` (bool)
- `unauthorized_marketplace_matches: [{marketplace, distance, url}]` (≤5)
- `authorized_marketplace_matches: [{marketplace, distance, url}]` (≤5)
- `overall_image_risk_score` (0–1)
- `analyzed_at`

Do NOT include full `https://i.otto.de/i/otto/{id}?w=...&h=...&fmt=webp...` URLs (store only `image_id` UUIDs).

## Return contract
Return ONLY: `{path, brand_site_match, unauthorized_matches_count, overall_image_risk_score}`.
