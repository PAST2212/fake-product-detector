#!/usr/bin/env python3
"""PostToolUse validator — only runs on verdict JSONs, exits non-zero on failure."""

import json
import sys
from datetime import datetime
from pathlib import Path

VERDICT_DIRS = ("verdicts/", "otto-verdicts/")
ERROR_LOG = Path(".hook-errors.log")


def _extract_filepath() -> str | None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return None
    tool_input = payload.get("tool_input") or {}
    return tool_input.get("file_path") or tool_input.get("notebook_path")


def main():
    filepath = _extract_filepath()
    if not filepath:
        sys.exit(0)

    if not any(d in filepath for d in VERDICT_DIRS) or not filepath.endswith(".json"):
        sys.exit(0)

    path = Path(filepath)
    if not path.exists() or path.stat().st_size == 0:
        sys.exit(0)

    try:
        with open(path) as f:
            json.load(f)
    except json.JSONDecodeError as e:
        msg = f"[{datetime.now().isoformat()}] Invalid verdict JSON {filepath}: {e}\n"
        with ERROR_LOG.open("a", encoding="utf-8") as log:
            log.write(msg)
        sys.stderr.write(f"ERROR: Invalid verdict JSON — see {ERROR_LOG}\n")
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
