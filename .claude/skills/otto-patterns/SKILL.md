---
name: otto-patterns
description: OTTO.de-specific patterns — seller types, fulfillment signals, German regulatory context, cross-platform (Idealo/Check24). Load when investigating OTTO listing or seller.
---

# OTTO Counterfeit Patterns

## Seller type × fulfillment (risk hierarchy)

| Seller type | Display | Fulfillment | Risk |
|-------------|---------|-------------|------|
| OTTO first-party | `Verkauf und Versand durch OTTO` | OTTO Versand | Lowest |
| OTO subsidiary | `Verkauf und Versand durch OTO` | OTTO Versand | Very Low |
| Brand Store | `Verkauf durch Markenshop X, Versand durch OTTO` | OTTO Versand | Low-Medium |
| Marketplace (DE) | `Verkauf und Versand durch Händler` | Händlerversand | Medium |
| Marketplace (intl) | `Versand aus dem Ausland` | Händlerversand | High |

`Angebote von mehreren Händlern` on one listing → further elevated; each offer is a separate seller.

## German regulatory checks

| Check | Source | Missing = |
|-------|--------|-----------|
| Impressum | Seller profile | High risk |
| VAT ID (`USt-IdNr.`, `DE\d{9}`) | bzst.de | Medium risk (missing for DE seller) |
| Handelsregister | handelsregister.de | Medium risk |
| CE / GS mark | Product listing (if applicable) | Category-dependent |
| GPSR EU-responsible-person | Product listing (post-July-2024) | Medium-High risk |
| LUCID packaging register | verpackungsregister.org | Low-Medium |

## German review signals (keywords preserved in review-analyst agent)

Explicit fake: `gefälscht`, `Fälschung`, `Nachahmung`, `Imitat`, `Plagiat`, `nicht original`, `kein Original`
Mismatch: `andere Verpackung`, `keine Originalverpackung`, `nicht wie abgebildet`, `andere Qualität`
Gray market: `aus China`, `importiert`, `Drittland`, `nicht EU`

## Cross-platform evidence

| Platform | Check |
|----------|-------|
| Idealo.de | Same product across sellers |
| Check24.de | Seller reviews, price spread |
| eBay Kleinanzeigen | Common DE counterfeit outlet |
| Trustpilot.de | Brand/seller reviews in German |
| Amazon.de | Cross-platform presence |
| AliExpress / DHgate | Same images at lower prices |

## Commonly targeted DE brands
Fashion: Lascana, s.Oliver; Electronics: Sony, Apple, Samsung, Anker accessories; Cosmetics: Nivea, L'Oréal, Eucerin. Fashion/electronics/cosmetics are OTTO's highest-risk categories.

## Seller-network cues
- Keyword-stuffed names: `Günstig24`, `Welt-Shop`, `Store24`
- Shared addresses / identical catalogs across sellers
- Sequential registration dates
- International shipping + no DE business registration
