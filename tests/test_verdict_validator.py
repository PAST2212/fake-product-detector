import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.verdict_validator import VALID_RISK, VALID_VERDICTS, validate


def _base_amazon() -> dict:
    return {
        "asin": "B0TESTASIN",
        "product_title": "Something",
        "verdict": "LIKELY AUTHENTIC",
        "confidence": 0.8,
        "composite_score": 0.2,
        "risk_category": "LOW",
    }


def _base_otto() -> dict:
    return {
        "article_number": "123456789",
        "product_title": "Etwas",
        "verdict": "UNCERTAIN",
        "confidence": 0.5,
        "composite_score": 0.5,
        "risk_category": "MEDIUM",
    }


class ValidatorTests(unittest.TestCase):
    def test_amazon_minimal_is_valid(self):
        self.assertEqual(validate(_base_amazon(), "asin"), [])

    def test_otto_minimal_is_valid(self):
        self.assertEqual(validate(_base_otto(), "article_number"), [])

    def test_missing_id_field_flagged_per_platform(self):
        errors = validate({}, "asin")
        self.assertIn("Missing required field: 'asin'", errors)
        errors_otto = validate({}, "article_number")
        self.assertIn("Missing required field: 'article_number'", errors_otto)

    def test_wrong_type_for_confidence(self):
        v = _base_amazon()
        v["confidence"] = "high"
        errors = validate(v, "asin")
        self.assertTrue(any("confidence" in e and "wrong type" in e for e in errors))

    def test_confidence_out_of_range(self):
        v = _base_amazon()
        v["confidence"] = 1.5
        errors = validate(v, "asin")
        self.assertTrue(any("confidence 1.5 out of range" in e for e in errors))

    def test_composite_score_out_of_range(self):
        v = _base_amazon()
        v["composite_score"] = -0.1
        errors = validate(v, "asin")
        self.assertTrue(any("composite_score -0.1 out of range" in e for e in errors))

    def test_invalid_verdict_string(self):
        v = _base_amazon()
        v["verdict"] = "MAYBE"
        errors = validate(v, "asin")
        self.assertTrue(any("Invalid verdict 'MAYBE'" in e for e in errors))

    def test_invalid_risk_category(self):
        v = _base_amazon()
        v["risk_category"] = "EXTREME"
        errors = validate(v, "asin")
        self.assertTrue(any("Invalid risk_category 'EXTREME'" in e for e in errors))

    def test_all_valid_risk_categories_accepted(self):
        for rc in VALID_RISK:
            v = _base_amazon()
            v["risk_category"] = rc
            self.assertEqual(validate(v, "asin"), [], f"risk_category={rc} should be valid")

    def test_all_valid_verdicts_accepted(self):
        for vd in VALID_VERDICTS:
            v = _base_amazon()
            v["verdict"] = vd
            self.assertEqual(validate(v, "asin"), [], f"verdict={vd} should be valid")

    def test_evidence_summary_must_be_dict(self):
        v = _base_amazon()
        v["evidence_summary"] = ["nope"]
        errors = validate(v, "asin")
        self.assertIn("evidence_summary must be a dict", errors)

    def test_evidence_summary_side_must_be_list(self):
        v = _base_amazon()
        v["evidence_summary"] = {"for_authentic": "single string"}
        errors = validate(v, "asin")
        self.assertTrue(any("evidence_summary.for_authentic must be a list" in e for e in errors))

    def test_recommendations_must_be_list(self):
        v = _base_amazon()
        v["recommendations"] = "first; second"
        errors = validate(v, "asin")
        self.assertIn("recommendations must be a list", errors)

    def test_risk_flags_require_flag_and_severity(self):
        v = _base_amazon()
        v["risk_flags"] = [{"detail": "orphan"}]
        errors = validate(v, "asin")
        self.assertTrue(any("risk_flags[0] missing 'flag' key" in e for e in errors))
        self.assertTrue(any("risk_flags[0] missing 'severity' key" in e for e in errors))

    def test_risk_flags_entry_must_be_dict(self):
        v = _base_amazon()
        v["risk_flags"] = ["bare string"]
        errors = validate(v, "asin")
        self.assertIn("risk_flags[0] must be a dict", errors)

    def test_buying_verdict_must_be_dict(self):
        v = _base_amazon()
        v["buying_verdict"] = ["x"]
        errors = validate(v, "asin")
        self.assertIn("buying_verdict must be a dict", errors)


if __name__ == "__main__":
    unittest.main()
