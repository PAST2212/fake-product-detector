#!/usr/bin/env python3
"""Generate an HTML report from an OTTO verdict JSON file."""

import json
import re
import sys
from pathlib import Path

from shared.report_builder import OTTO, build_report

ARTICLE_PATTERN = re.compile(r"^\d{6,12}$")


def validate_article_number(article_number: str) -> str:
    if not ARTICLE_PATTERN.match(article_number):
        raise ValueError(f"Invalid article number: {article_number}")
    return article_number


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_otto_report.py <article_number>")
        sys.exit(1)

    try:
        article_number = validate_article_number(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    path = Path("otto-verdicts") / f"{article_number}_verdict.json"

    if not path.exists():
        print(f"Error: cannot find verdict file for '{article_number}'")
        sys.exit(1)

    try:
        with open(path) as f:
            verdict = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Malformed JSON in {path}: {e}")
        sys.exit(1)

    out_path = Path("otto-verdicts") / f"{article_number}_report.html"
    out_path.write_text(build_report(verdict, OTTO), encoding="utf-8")
    print(f"Report saved: {out_path}")
    print(f"Open with:   xdg-open {out_path}  (Linux) / open {out_path}  (macOS)")


if __name__ == "__main__":
    main()
