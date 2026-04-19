#!/usr/bin/env python3
"""
Self-verification script for OTTO verdict JSON files.
Run: python3 validate_otto_verdict.py <article_number>
"""

import json
import re
import sys
from pathlib import Path

from shared.verdict_validator import validate

ARTICLE_PATTERN = re.compile(r"^\d{6,12}$")


def validate_article_number(article_number: str) -> str:
    if not ARTICLE_PATTERN.match(article_number):
        raise ValueError(f"Invalid article number: {article_number}")
    return article_number


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_otto_verdict.py <article_number>")
        sys.exit(1)

    try:
        article_number = validate_article_number(sys.argv[1])
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    path = Path("otto-verdicts") / f"{article_number}_verdict.json"

    if not path.exists():
        print(f"ERROR: Verdict file not found: {path}")
        sys.exit(1)

    try:
        with open(path) as f:
            verdict = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Malformed JSON in {path}: {e}")
        sys.exit(1)

    errors = validate(verdict, id_field="article_number")

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s) in {path}:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print(f"OK — {path} is valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
