"""Shared verdict-validation logic for Amazon and OTTO verdict JSONs."""

VALID_VERDICTS = {"LIKELY AUTHENTIC", "LIKELY COUNTERFEIT", "UNCERTAIN"}
VALID_RISK = {"HIGH", "MEDIUM", "LOW", "LOW-MEDIUM", "MEDIUM-HIGH"}

_COMMON_REQUIRED = {
    "product_title": str,
    "verdict": str,
    "confidence": (int, float),
    "composite_score": (int, float),
    "risk_category": str,
}


def required_fields(id_field: str) -> dict:
    return {id_field: str, **_COMMON_REQUIRED}


def validate(verdict: dict, id_field: str) -> list[str]:
    errors: list[str] = []

    for field, expected_type in required_fields(id_field).items():
        if field not in verdict:
            errors.append(f"Missing required field: '{field}'")
            continue
        if not isinstance(verdict[field], expected_type):
            expected_name = (
                " or ".join(t.__name__ for t in expected_type)
                if isinstance(expected_type, tuple)
                else expected_type.__name__
            )
            errors.append(
                f"Field '{field}' has wrong type: got {type(verdict[field]).__name__}, "
                f"expected {expected_name}"
            )

    v = verdict.get("verdict", "")
    if v not in VALID_VERDICTS:
        errors.append(f"Invalid verdict '{v}' — must be one of: {', '.join(sorted(VALID_VERDICTS))}")

    rc = verdict.get("risk_category", "")
    if rc and rc not in VALID_RISK:
        errors.append(
            f"Invalid risk_category '{rc}' — should be one of: {', '.join(sorted(VALID_RISK))}"
        )

    conf = verdict.get("confidence")
    if isinstance(conf, (int, float)):
        if not (0.0 <= conf <= 1.0):
            errors.append(f"confidence {conf} out of range [0.0, 1.0]")
        elif conf > 0.95:
            errors.append(f"confidence {conf} exceeds 0.95 cap (methodology)")

    score = verdict.get("composite_score")
    if isinstance(score, (int, float)) and not (0.0 <= score <= 1.0):
        errors.append(f"composite_score {score} out of range [0.0, 1.0]")

    if "evidence_summary" in verdict:
        ev = verdict["evidence_summary"]
        if not isinstance(ev, dict):
            errors.append("evidence_summary must be a dict")
        else:
            for side in ("for_authentic", "against_authentic"):
                if side in ev and not isinstance(ev[side], list):
                    errors.append(
                        f"evidence_summary.{side} must be a list, got {type(ev[side]).__name__}"
                    )

    if "recommendations" in verdict and not isinstance(verdict["recommendations"], list):
        errors.append("recommendations must be a list")

    if "risk_flags" in verdict:
        flags = verdict["risk_flags"]
        if not isinstance(flags, list):
            errors.append("risk_flags must be a list")
        else:
            for i, flag in enumerate(flags):
                if not isinstance(flag, dict):
                    errors.append(f"risk_flags[{i}] must be a dict")
                    continue
                if "flag" not in flag:
                    errors.append(f"risk_flags[{i}] missing 'flag' key")
                if "severity" not in flag:
                    errors.append(f"risk_flags[{i}] missing 'severity' key")

    if "buying_verdict" in verdict and not isinstance(verdict["buying_verdict"], dict):
        errors.append("buying_verdict must be a dict")

    return errors
