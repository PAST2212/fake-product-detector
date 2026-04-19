#!/usr/bin/env python3
"""
Yandex Reverse Image Search for counterfeit detection.

Searches Yandex Images and extracts marketplace matches from results.
Yandex often finds Chinese marketplace listings (AliExpress, DHgate, Temu)
that Google misses.

Note: Yandex loads results via JavaScript. For full automated results,
use the --browser flag with Playwright installed.
"""

import argparse
import json
import re
import sys
import time
from urllib.parse import quote, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install requests beautifulsoup4")
    sys.exit(1)


MARKETPLACE_PATTERNS = {
    "aliexpress": r"aliexpress\.com",
    "dhgate": r"dhgate\.com",
    "temu": r"temu\.com",
    "amazon": r"amazon\.",
    "ebay": r"ebay\.",
    "wish": r"wish\.com",
    "gearbest": r"gearbest\.com",
    "lightinthebox": r"lightinthebox\.com",
    "miniinthebox": r"miniinthebox\.com",
    "etsy": r"etsy\.com",
    "walmart": r"walmart\.com",
    "target": r"target\.com",
    "nordstrom": r"nordstrom\.com",
    "zara": r"zara\.com",
    "hm": r"hm\.com",
    "otto": r"otto\.de",
    "mediamarkt": r"mediamarkt\.de",
    "saturn": r"saturn\.de",
}


def build_yandex_url(image_url: str, include_cbir: bool = True) -> str:
    """Build Yandex image search URL from image URL."""
    encoded_url = quote(image_url, safe="")
    base_url = f"https://yandex.com/images/search?url={encoded_url}"
    if include_cbir:
        return f"{base_url}&rpt=imageview"
    return base_url


def extract_domains_from_html(html_content: str) -> list[dict]:
    """Extract domains/marketplaces from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    results = []

    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if not href.startswith("http"):
            continue

        try:
            parsed = urlparse(href)
            domain = parsed.netloc.lower()

            if domain.startswith("www."):
                domain = domain[4:]

            for marketplace, pattern in MARKETPLACE_PATTERNS.items():
                if re.search(pattern, domain, re.IGNORECASE):
                    results.append({
                        "marketplace": marketplace,
                        "domain": domain,
                        "url": href
                    })
                    break
        except Exception:
            continue

    seen = set()
    unique_results = []
    for r in results:
        key = r["domain"]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return unique_results


def search_with_requests(
    image_url: str,
    timeout: int = 30,
    max_retries: int = 3,
    backoff_base: float = 1.5,
) -> dict:
    """Basic HTTP-based search (limited due to JS rendering)."""
    search_url = build_yandex_url(image_url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://yandex.com/images/",
        "Origin": "https://yandex.com",
    }

    response = None
    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = requests.get(search_url, headers=headers, timeout=timeout)
            response.raise_for_status()
            last_error = None
            break
        except requests.RequestException as e:
            last_error = e
            status = getattr(getattr(e, "response", None), "status_code", None)
            if status is not None and 400 <= status < 500 and status not in (408, 429):
                break
            if attempt < max_retries - 1:
                time.sleep(backoff_base ** attempt)

    if last_error is not None or response is None:
        return {
            "success": False,
            "error": str(last_error) if last_error else "no response",
            "search_url": search_url,
            "matches": [],
            "method": "requests"
        }

    matches = extract_domains_from_html(response.text)

    grouped = {}
    for match in matches:
        marketplace = match["marketplace"]
        if marketplace not in grouped:
            grouped[marketplace] = {
                "marketplace": marketplace,
                "count": 0,
                "domains": [],
                "sample_url": match["url"]
            }
        grouped[marketplace]["count"] += 1
        if match["domain"] not in grouped[marketplace]["domains"]:
            grouped[marketplace]["domains"].append(match["domain"])

    return {
        "success": True,
        "search_url": search_url,
        "image_url": image_url,
        "method": "requests",
        "js_rendered": False,
        "note": "Results may be incomplete due to JavaScript rendering. Use --browser for full results.",
        "total_matches": len(matches),
        "marketplace_summary": list(grouped.values()),
        "raw_matches": matches
    }


def search_with_browser(image_url: str, timeout: int = 60) -> dict:
    """Playwright-based search (full JavaScript rendering)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "Playwright not installed. Run: pip install playwright && playwright install chromium",
            "search_url": None,
            "matches": [],
            "method": "browser"
        }

    search_url = build_yandex_url(image_url)
    matches = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            try:
                page.goto(search_url, wait_until="networkidle", timeout=timeout * 1000)
                time.sleep(3)

                page_content = page.content()
                matches = extract_domains_from_html(page_content)

                page.wait_for_timeout(2000)

            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "search_url": search_url,
                    "matches": [],
                    "method": "browser"
                }
            finally:
                page.close()
        finally:
            browser.close()

    grouped = {}
    for match in matches:
        marketplace = match["marketplace"]
        if marketplace not in grouped:
            grouped[marketplace] = {
                "marketplace": marketplace,
                "count": 0,
                "domains": [],
                "sample_url": match["url"]
            }
        grouped[marketplace]["count"] += 1
        if match["domain"] not in grouped[marketplace]["domains"]:
            grouped[marketplace]["domains"].append(match["domain"])

    return {
        "success": True,
        "search_url": search_url,
        "image_url": image_url,
        "method": "browser",
        "js_rendered": True,
        "total_matches": len(matches),
        "marketplace_summary": list(grouped.values()),
        "raw_matches": matches
    }


def search_yandex_image(image_url: str, use_browser: bool = False, timeout: int = 60) -> dict:
    """
    Search Yandex Images for a product image and return marketplace matches.

    Args:
        image_url: URL of the image to search
        use_browser: Use Playwright for full JS rendering
        timeout: Request timeout in seconds

    Returns:
        Dict with search results and marketplace matches
    """
    if use_browser:
        return search_with_browser(image_url, timeout)
    return search_with_requests(image_url, timeout)


def main():
    parser = argparse.ArgumentParser(
        description="Search Yandex Images and extract marketplace matches for counterfeit detection."
    )
    parser.add_argument(
        "--image-url", "-i",
        required=True,
        help="URL of the product image to search"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file (optional)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "summary"],
        default="summary",
        help="Output format (default: summary)"
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Use Playwright for full JavaScript-rendered results (requires playwright)"
    )

    args = parser.parse_args()

    result = search_yandex_image(args.image_url, use_browser=args.browser)

    if args.format == "json" or args.output:
        output = json.dumps(result, indent=2)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        else:
            print(output)
    else:
        print(f"Yandex Image Search Results")
        print(f"=" * 50)
        print(f"Image: {result.get('image_url', 'N/A')}")
        print(f"Method: {result.get('method', 'N/A')}")
        print(f"Search URL: {result.get('search_url', 'N/A')}")
        print()

        if not result.get("success"):
            print(f"Error: {result.get('error', 'Unknown error')}")
            if "Playwright not installed" in result.get('error', ''):
                print("\nTo enable full results, install Playwright:")
                print("  pip install playwright")
                print("  playwright install chromium")
            sys.exit(1)

        if result.get("note"):
            print(f"Note: {result['note']}")
            print()

        summary = result.get("marketplace_summary", [])

        if not summary:
            print("No marketplace matches found.")
        else:
            print("Marketplace Matches:")
            print("-" * 50)
            for item in summary:
                domains = ", ".join(item["domains"])
                print(f"  [{item['marketplace'].upper()}] {item['count']} match(es)")
                print(f"    Domains: {domains}")
                print(f"    Sample: {item['sample_url']}")
                print()

        print(f"Total matches: {result.get('total_matches', 0)}")
        print(f"\nFull results: {result.get('search_url', '')}")


if __name__ == "__main__":
    main()