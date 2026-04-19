# Fake Product Detector

AI-powered counterfeit detection for Amazon and OTTO marketplace products using multi-agent analysis.
Developed at OTTO Group, Fraud Management department.

## Commands

### Amazon
| Command | Description |
|---------|-------------|
| `/investigate [ASIN]` | Full pipeline: listing + reviews + images + seller + verdict + HTML report |
| `/listing [ASIN]` | Extract and save listing data |
| `/reviews [ASIN]` | NLP analysis of reviews |
| `/images [ASIN]` | Image forensics and reverse search |
| `/seller [seller-id]` | Seller reputation and network analysis |
| `/verdict [ASIN]` | Classify and produce final verdict |

### OTTO.de
| Command | Description |
|---------|-------------|
| `/otto-investigate [article-number]` | Full pipeline for OTTO products |
| `/otto-listing [article-number]` | Extract OTTO listing data |
| `/otto-reviews [article-number]` | German NLP review analysis |
| `/otto-images [article-number]` | Image forensics for OTTO images |
| `/otto-seller [seller-id]` | OTTO seller investigation |
| `/otto-verdict [article-number]` | Classify and produce OTTO verdict |

## Data Storage

### Amazon
| Data type | Path |
|-----------|------|
| Listing metadata | `products/{asin}_listing.json` |
| Review analysis | `reviews/{asin}_analysis.json` |
| Image forensics | `images/{asin}_forensics.json` |
| Seller profile | `sellers/{seller_id}_profile.json` |
| Final verdict | `verdicts/{asin}_verdict.json` |
| HTML report | `verdicts/{asin}_report.html` |

### OTTO
| Data type | Path |
|-----------|------|
| Listing metadata | `otto-products/{article_number}_listing.json` |
| Review analysis | `otto-reviews/{article_number}_analysis.json` |
| Image forensics | `otto-images/{article_number}_forensics.json` |
| Seller profile | `otto-sellers/{seller_id}_profile.json` |
| Final verdict | `otto-verdicts/{article_number}_verdict.json` |
| HTML report | `otto-verdicts/{article_number}_report.html` |

### Shared
| Data type | Path |
|-----------|------|
| Raw scraped data | `scraped/` |
| Web search results | `search/` |

## After Every Verdict

Always run both of these after saving a verdict JSON:
```bash
# Amazon
python3 validate_verdict.py {asin}
python3 generate_report.py {asin}

# OTTO
python3 validate_otto_verdict.py {article_number}
python3 generate_otto_report.py {article_number}
```

## Gotchas

- Price is a **weak signal** — counterfeits often price at or above authentic products.
- Amazon: always check fulfillment type (FBA vs FBM) and whether the buy box belongs to the brand.
- OTTO: always check seller type — "OTTO Versand" is lowest risk, "Händlerversand" is elevated risk.
- Load the `counterfeit-methodology` skill for scoring weights and thresholds (platform-agnostic).
- Load the `amazon-patterns` skill for Amazon-specific red flags and seller hijacking patterns.
- Load the `otto-patterns` skill for OTTO-specific seller types, fulfillment signals, and German regulatory context.
- `validate_verdict.py` / `validate_otto_verdict.py` checks required verdict fields — fix any errors before generating the HTML report.
- Allowed `risk_category` values: `HIGH`, `MEDIUM`, `LOW`, `LOW-MEDIUM`, `MEDIUM-HIGH`. See `.claude/rules/api-conventions.md` for the full verdict schema.

## Agents Available

**Amazon:** `product-researcher` · `image-forensics` · `review-analyst` · `seller-investigator` · `fake-product-classifier` · `web-search` · `data-scraper`

**OTTO:** `otto-product-researcher` · `otto-image-forensics` · `otto-review-analyst` · `otto-seller-investigator` · `otto-fake-product-classifier`
