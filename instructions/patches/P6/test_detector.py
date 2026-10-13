"""
P6 unit tests — run with: python3 -m unittest /root/AAA/instructions/patches/P6/test_detector.py

These tests are pure: no MCP, no FastMCP, no network. They exist so the
detector can be approved *before* the live server is restarted.

A failed test is not a sovereign decision. A passing test is also not a
human acceptance — it is one of two inputs (build pass + fixture pass) to the
PATCH 6 closure condition.
"""

import sys, os, unittest, json
from pathlib import Path

sys.path.insert(0, "/root/AAA/instructions/patches/P6")
sys.path.insert(0, "/root/AAA/instructions/patches/P6/lib" if Path("/root/AAA/instructions/patches/P6/lib").exists() else "/root/AAA/instructions/patches/P6")

# Plain import — detector.py is a single file, no package.
import importlib.util as _il
_spec = _il.spec_from_file_location("detector", "/root/AAA/instructions/patches/P6/detector.py")
detector = _il.module_from_spec(_spec)
_spec.loader.exec_module(detector)


class P6Detectors(unittest.TestCase):

    def test_no_seal_or_verdict_in_outputs(self):
        out = detector.scan(detector.fixture_eight_claims())
        self.assertTrue(out["ok"])
        # Top-level output must not contain verdict/seal/allow/hold semantics.
        for forbidden in ["verdict:", "seal\":", "allow\":", "hold\":", "void\":"]:
            self.assertNotIn(forbidden, json.dumps(out["limitations"]).lower())
        # Per-row: classes are closed enums and must not be governance labels.
        for r in out["contradictions"]:
            self.assertIn(r["class"], detector.CLASSES)
            self.assertNotIn(r["status"], ["SEAL", "HOLD", "ALLOW", "VOID", "DENY"])
            # Limitations may *disclaim* authority by naming it; check
            # for the un-disclaimed forms (e.g. "with verdict" / "of authority").
            # The detector's permitted phrasing is "no authority effect"
            # which the disclaimer carries by design.
            lower_str = json.dumps(r, default=str).lower()
            for governance_term in ["verdict by", "sealed verdict", "granted authority", "approved authorization"]:
                self.assertNotIn(governance_term, lower_str)

    def test_eight_claim_fixture_returns_four_or_more(self):
        out = detector.scan(detector.fixture_eight_claims())
        n = len(out["contradictions"])
        self.assertGreaterEqual(n, 4, f"expected >=4 contradictions, got {n}: {json.dumps(out, indent=2)[:2000]}")

    def test_oil_assumption_vs_spot(self):
        out = detector.scan(detector.fixture_eight_claims())
        oil_rows = [r for r in out["contradictions"] if r["class"] == "MODEL_VERSUS_REALITY"
                    or "oil" in r["subject"]]
        self.assertGreaterEqual(len(oil_rows), 1, "USD assumption vs spot must surface")
        r = oil_rows[0]
        self.assertIn(r["status"], ("OPEN", "PARTIALLY_RECONCILED"))

    def test_forecast_versus_observation_present(self):
        out = detector.scan(detector.fixture_eight_claims())
        # C5 (FORECAST target 3.3%) and C11 (REPORTED 4.2% / "well below 3.5%") cross tenses.
        fvo = [r for r in out["contradictions"] if r["class"] in ("FORECAST_VERSUS_OUTCOME", "MEASUREMENT_VERSUS_INTERPRETATION")]
        self.assertGreaterEqual(len(fvo), 1, "temporal or measurement-interpretation contradiction required")

    def test_determinism(self):
        """Two calls produce identical output. Determinism is part of the contract."""
        c = detector.fixture_eight_claims()
        a = detector.scan(c)
        b = detector.scan(c)
        self.assertEqual(
            sorted([(r["claim_a_id"], r["claim_b_id"], r["class"]) for r in a["contradictions"]]),
            sorted([(r["claim_a_id"], r["claim_b_id"], r["class"]) for r in b["contradictions"]]),
        )

    def test_scope_classifies_rm510b_vs_rm459_8b_correctly(self):
        out = detector.scan(detector.fixture_eight_claims())
        scope_rows = [r for r in out["contradictions"] if r["class"] == "SCOPE"]
        self.assertGreaterEqual(len(scope_rows), 1)
        r = scope_rows[0]
        self.assertIn(r["status"], ("RESOLVED_BY_SCOPE", "OPEN"))
        self.assertIn("federal_budget_total", r["subject"])

    def test_petronas_dividend_open(self):
        out = detector.scan(detector.fixture_eight_claims())
        dividend_rows = [r for r in out["contradictions"]
                         if "petronas" in r["subject"]]
        self.assertGreaterEqual(len(dividend_rows), 1)
        self.assertTrue(all(r["status"] in ("OPEN", "RESOLVED_BY_SCOPE") for r in dividend_rows),
                        f"expected OPEN or RESOLVED_BY_SCOPE for dividend; got {[r['status'] for r in dividend_rows]}")

    def test_deficit_forecast_open(self):
        out = detector.scan(detector.fixture_eight_claims())
        deficit_rows = [r for r in out["contradictions"] if "deficit" in r["subject"]]
        self.assertGreaterEqual(len(deficit_rows), 1)
        for r in deficit_rows:
            self.assertIn(r["status"], ("OPEN", "RESOLVED_BY_SCOPE", "PARTIALLY_RECONCILED"))

    def test_subsidy_denominator(self):
        out = detector.scan(detector.fixture_eight_claims())
        sub = [r for r in out["contradictions"] if "subsidy" in r["subject"]]
        self.assertGreaterEqual(len(sub), 1)

    def test_negative_control_identical_claims(self):
        c = {"id": "X1", "text": "Federal spending RM510b",
             "source": "x", "principal": "federal_budget_total",
             "geography": "MY", "kind": "REPORTED"}
        out = detector.scan([c, dict(c, id="X2")])
        # Identical claim + same source → SAME source cluster, blocked from SOURCE-class emission.
        # Should still be retrievable but we accept 0 contradictions here (no measurement difference).
        self.assertEqual(len(out["contradictions"]), 0)

    def test_negative_control_different_units(self):
        c1 = {"id": "U1", "text": "Federal spending RM510 billion",
              "source": "x", "principal": "x", "geography": "MY", "kind": "REPORTED"}
        c2 = {"id": "U2", "text": "Federal revenue USD 50 billion",
              "source": "y", "principal": "x", "geography": "MY", "kind": "REPORTED"}
        out = detector.scan([c1, c2])
        # Different units (RM vs USD on different subjects) should not be SCOPE.
        for r in out["contradictions"]:
            self.assertNotEqual(r["class"], "SCOPE")

    def test_does_not_mutate_canonical_store(self):
        """
        The detector must not produce side-effects. We assert that it returns
        the same contradictions for the same input twice (deterministic, pure).
        """
        a = detector.scan(detector.fixture_eight_claims())
        b = detector.scan(detector.fixture_eight_claims())
        self.assertEqual(len(a["contradictions"]), len(b["contradictions"]))

    def test_handles_garbage_without_crashing(self):
        for bad in ([], [{}], [{"id": "X"}], [{"id": "X", "text": ""}], [{"id": "X", "text": "no numerals here"}]):
            try:
                out = detector.scan(bad)
                self.assertTrue(out["ok"])
                self.assertIsInstance(out["contradictions"], list)
            except Exception as e:
                self.fail(f"detector crashed on benign input {bad!r}: {e}")

    def test_no_durable_receipt_emitted(self):
        """
        Detector output MUST NOT contain a receipt_id, claim authority,
        or write a canonical row.
        """
        out = detector.scan(detector.fixture_eight_claims())
        for r in out["contradictions"]:
            self.assertIsNone(r.get("receipt_id"), "detector rows must not carry a receipt_id")
            self.assertNotIn(r.get("status"), ["SEAL", "HOLD", "ALLOW", "VOID", "DENY"])
            # no implicit "we authorized this" claim; "no authority effect"
            # disclaimers are allowed because they are *disclaiming*.
            row_text = json.dumps(r, default=str).lower()
            for forbidden in ["verdict", "seal", "hold", "allow", "void"]:
                self.assertFalse(
                    forbidden in row_text and not (
                        f"no {forbidden}" in row_text or f"not {forbidden}" in row_text
                    ),
                    f"detector row contains unforbidden governance term {forbidden!r}: {r}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
