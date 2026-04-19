---
name: amazon-patterns
description: Amazon-specific counterfeit patterns: FBA/FBM signals, seller hijacking, review manipulation, ASIN red flags. Load when investigating an Amazon listing or seller.
---

# Amazon Counterfeit Patterns

## Fulfillment risk

| Fulfillment + seller | Risk |
|----------------------|------|
| Sold & fulfilled by brand | Lowest |
| FBA, sold by brand | Low (commingling risk in high-counterfeit categories) |
| FBA, third-party | Medium (seller can inject into FBA pool) |
| FBM, unknown seller | High |
| Dropship from CN address | High |

**FBA commingling:** in fragrances/cosmetics, brand FBA inventory can be mixed with counterfeiter units unless brand enforces "manufacturer barcode" requirement. Operationalize via: (1) seller name ≠ brand AND fulfillment = FBA AND category ∈ {fragrances, cosmetics}; (2) negative review keywords: `different packaging`, `smells off`, `batch code mismatch`, `andere Verpackung`; (3) third-party seller on a brand-owned ASIN without "Ships from Amazon, sold by {Brand}".

## Seller hijacking (primary injection vector)
Third-party sellers listing on a brand's ASIN at lower price without Prime. Check:
- Seller count on ASIN
- Any priced below brand?
- Does buy box switch to third party?

## Review manipulation

| Tactic | Signal |
|--------|--------|
| Influencer seeding (paid 5-star cohort) | Burst of similarly-worded positive reviews |
| Review gating (Raycon pattern) | External rating << Amazon rating |
| Vine abuse | Early reviews disproportionately positive |
| Duplicate clusters | Same reviewer text across ASINs |
| VP manipulation | Counterfeiter buys own product for VP badge |

## ASIN red flags
- Frequent title/brand-name changes (search hijacking)
- Category misclassified to evade brand registry
- Images change without version update (listing hijack)
- Seller-written Q&A answers posing as customers
- "Frequently bought together" ties to known counterfeit accessories

## Cross-platform evidence

| Source | What to check |
|--------|---------------|
| AliExpress / DHgate / Temu | Same images at fraction of price |
| PissedConsumer / Trustpilot | Rating discrepancy vs Amazon |
| BBB | Complaint volume + brand response |
| Reddit (r/Counterfeit, r/Fraud) | Community reports |
| Niche forums (Head-Fi, etc.) | Expert teardown reports |
| CBP seizure records | Brand in US Customs seizures |
| Google Reverse Image | Earliest indexed use |

## Impersonation-site pattern
Fake brand sites (`brand-uk.com`, `brand.online`, etc.): social-media ads on brand keywords, CN ship, no returns. Check `site:*.com inurl:{brand}` and `scampulse.com` / `ScamAdviser`.
