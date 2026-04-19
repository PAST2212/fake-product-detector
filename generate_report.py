#!/usr/bin/env python3
"""Generate an HTML report from an Amazon verdict JSON file."""

import json
import re
import sys
from pathlib import Path

from shared.report_builder import AMAZON, build_report

ASIN_PATTERN = re.compile(r"^[A-Z0-9]{10}$")


def validate_asin(asin: str) -> str:
    asin = asin.upper()
    if not ASIN_PATTERN.match(asin):
        raise ValueError(f"Invalid ASIN: {asin}")
    return asin


def main():
    if len(sys.argv) < 2:
        verdict_dir = Path("verdicts")
        jsons = list(verdict_dir.glob("*_verdict.json"))
        if not jsons:
            print("Usage: python generate_report.py <verdict_json_or_asin>")
            sys.exit(1)
        jsons.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        path = jsons[0]
        print(f"No argument given — using most recent verdict: {path}")
    else:
        arg = sys.argv[1]
        path = Path(arg)
        if not path.exists():
            try:
                validated_arg = validate_asin(arg)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
            path = Path("verdicts") / f"{validated_arg}_verdict.json"
        if not path.exists():
            print(f"Error: cannot find verdict file for '{arg}'")
            sys.exit(1)

    try:
        with open(path) as f:
            verdict = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Malformed JSON in {path}: {e}")
        sys.exit(1)

    asin_from_verdict = verdict.get("asin", "")
    if isinstance(asin_from_verdict, str) and ASIN_PATTERN.match(asin_from_verdict.upper()):
        out_asin = asin_from_verdict.upper()
    else:
        stem = path.stem.replace("_verdict", "").upper()
        if not ASIN_PATTERN.match(stem):
            print("Error: could not determine valid ASIN from verdict or filename")
            sys.exit(1)
        out_asin = stem
    out_path = Path("verdicts") / f"{out_asin}_report.html"

    out_path.write_text(build_report(verdict, AMAZON), encoding="utf-8")
    print(f"Report saved: {out_path}")
    print(f"Open with:   xdg-open {out_path}  (Linux) / open {out_path}  (macOS)")


if __name__ == "__main__":
    main()
