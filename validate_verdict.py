#!/usr/bin/env python3
"""
Self-verification script for Amazon verdict JSON files.
Run: python3 validate_verdict.py <asin>
"""

import json
import re
import sys
from pathlib import Path

from shared.verdict_validator import validate

ASIN_PATTERN = re.compile(r"^[A-Z0-9]{10}$")


def validate_asin(asin: str) -> str:
    asin = asin.upper()
    if not ASIN_PATTERN.match(asin):
        raise ValueError(f"Invalid ASIN: {asin}")
    return asin


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_verdict.py <asin>")
        sys.exit(1)

    try:
        asin = validate_asin(sys.argv[1])
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    path = Path("verdicts") / f"{asin}_verdict.json"

    if not path.exists():
        print(f"ERROR: Verdict file not found: {path}")
        sys.exit(1)

    try:
        with open(path) as f:
            verdict = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Malformed JSON in {path}: {e}")
        sys.exit(1)

    errors = validate(verdict, id_field="asin")

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s) in {path}:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print(f"OK — {path} is valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
