---
name: image-forensics
description: Perceptual hashing and cross-platform reverse search to detect stolen/counterfeit product images.
tools: Read, Write, Bash, Grep, Glob
---

Detect image reuse across unauthorized marketplaces. Gate expensive searches behind cheaper signals.

## Workflow

1. Read image URLs from `products/{asin}_listing.json` (first 3 images only).
2. Download with `curl -sL --max-time 30 "$URL" -o images/{asin}/img_{n}.jpg`. Skip if already on disk.
3. Compute `phash`, `dhash`, `ahash` via Python `imagehash`.
4. Extract EXIF via PIL (`Make`, `Software`, `DateTimeOriginal`). Missing EXIF is weak signal; matching EXIF across sellers is strong.
5. Reverse search — gated:
   - **Cheap first:** brand official site (`site:{brand}.com`) + 2 authorized retailers.
   - **If price/seller flags are already high:** unauthorized marketplaces (AliExpress, DHgate, Temu) via Yandex (best for Chinese sites) or Google.
6. Match distance thresholds (Hamming): `0–2` exact, `3–10` near, `11–15` possible, `≥16` no match.

## Required output → `images/{asin}_forensics.json`

- `asin`, `image_count_analyzed`
- `phash_list`, `dhash_list` (arrays of hash strings, NOT URLs)
- `exif_factory_fingerprint_score` (0–1; cross-seller match)
- `brand_site_match` (bool)
- `unauthorized_marketplace_matches` — array of `{marketplace, distance, url}` (≤5 entries)
- `cross_asin_image_sharing_count` (other ASINs using same hash)
- `overall_image_risk_score` (0–1)
- `analyzed_at`

Do NOT include: base64 image data, full marketplace HTML, search-engine result pages.

## Return contract
Return ONLY: `{path, brand_site_match, unauthorized_marketplace_matches_count, overall_image_risk_score}`.
