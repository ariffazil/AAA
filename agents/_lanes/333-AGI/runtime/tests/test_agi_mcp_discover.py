"""Unit tests for agi_mcp_discover.

Stdlib only — uses unittest so pytest discovers it cleanly under
AAA/agents/_lanes/333-AGI/runtime/tests/.

F2 TRUTH: tests assert only what the code actually guarantees.
F4 CLARITY: cap-of-8 is a hard invariant — every test enforces it.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Add the runtime directory to sys.path so the test can import the
# module without requiring an installed package. This matches the
# convention used by other 333-AGI runtime modules under
# AAA/agents/_lanes/333-AGI/runtime/.
_RUNTIME_DIR = Path(__file__).resolve().parent.parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

from agi_mcp_discover import (  # noqa: E402  (path tweak above is intentional)
    ALWAYS_HOT,
    MAX_TOOLS,
    ON_DEMAND,
    classify_intent,
    discover,
)


class TestClassifyIntent(unittest.TestCase):
    """classify_intent: 6 sample intents → correct domain."""

    def test_geoscience_keyword(self) -> None:
        self.assertEqual(classify_intent("Screen basin for CCS site"), "geoscience")
        self.assertEqual(classify_intent("Interpret seismic section"), "geoscience")
        self.assertEqual(classify_intent("Petrophysics evaluation"), "geoscience")
        self.assertEqual(classify_intent("Prospect maturation"), "geoscience")

    def test_capital_keyword(self) -> None:
        self.assertEqual(classify_intent("Compute NPV for this deal"), "capital")
        self.assertEqual(classify_intent("Run IRR analysis"), "capital")
        self.assertEqual(classify_intent("Stock valuation check"), "capital")

    def test_engineering_keyword(self) -> None:
        self.assertEqual(classify_intent("Build and deploy the service"), "engineering")
        self.assertEqual(classify_intent("Run shell command"), "engineering")
        self.assertEqual(classify_intent("git commit"), "engineering")

    def test_vault_keyword(self) -> None:
        self.assertEqual(classify_intent("Seal this entry in the vault"), "vault")
        self.assertEqual(classify_intent("Archive the ledger"), "vault")

    def test_evidence_keyword(self) -> None:
        self.assertEqual(classify_intent("Research this topic on the web"), "evidence")
        self.assertEqual(classify_intent("Search the docs"), "evidence")

    def test_meta_fallback(self) -> None:
        # Unknown intent — falls through to meta (no domain keywords).
        self.assertEqual(classify_intent("hello there"), "meta")
        self.assertEqual(classify_intent(""), "meta")

    def test_case_insensitive(self) -> None:
        self.assertEqual(classify_intent("BASIN profile please"), "geoscience")
        self.assertEqual(classify_intent("Capital Markets"), "capital")


class TestDiscoverCap(unittest.TestCase):
    """discover: never returns more than MAX_TOOLS."""

    def test_each_domain_under_cap(self) -> None:
        for domain in ON_DEMAND:
            tools = discover(domain)
            self.assertLessEqual(
                len(tools),
                MAX_TOOLS,
                f"domain {domain!r} returned {len(tools)} tools (> {MAX_TOOLS})",
            )

    def test_unknown_domain_under_cap(self) -> None:
        tools = discover("not_a_real_domain")
        self.assertLessEqual(len(tools), MAX_TOOLS)

    def test_unknown_domain_equals_always_hot(self) -> None:
        tools = discover("anything_unknown_xyz")
        self.assertEqual(tools, list(ALWAYS_HOT))


class TestDiscoverHotTools(unittest.TestCase):
    """discover: ALWAYS_HOT is always present."""

    def test_hot_tools_for_every_known_domain(self) -> None:
        for domain in ON_DEMAND:
            tools = discover(domain)
            for hot in ALWAYS_HOT:
                self.assertIn(
                    hot,
                    tools,
                    f"hot tool {hot!r} missing from domain {domain!r}",
                )

    def test_hot_tools_for_unknown_domain(self) -> None:
        tools = discover("unknown")
        for hot in ALWAYS_HOT:
            self.assertIn(hot, tools)


class TestDiscoverInternals(unittest.TestCase):
    """Sanity checks on the underlying data structures."""

    def test_always_hot_size(self) -> None:
        # Hot tools must fit alongside ≥1 on-demand tool under the cap.
        self.assertLess(len(ALWAYS_HOT), MAX_TOOLS)

    def test_no_duplicate_tool_names(self) -> None:
        all_tools: set[str] = set()
        for t in ALWAYS_HOT:
            self.assertNotIn(t, all_tools)
            all_tools.add(t)
        for domain, tools in ON_DEMAND.items():
            for t in tools:
                self.assertNotIn(
                    t,
                    all_tools,
                    f"tool {t!r} duplicated across domains",
                )
                all_tools.add(t)


class TestDiscoverIntentParam(unittest.TestCase):
    """intent parameter is acknowledged (forward-compat) but optional."""

    def test_intent_none_does_not_crash(self) -> None:
        tools = discover("geoscience", None)
        self.assertLessEqual(len(tools), MAX_TOOLS)

    def test_intent_string_does_not_change_selection(self) -> None:
        # Current contract: domain-driven, intent unused for selection.
        tools_a = discover("capital", "tiny text")
        tools_b = discover("capital")
        self.assertEqual(tools_a, tools_b)


if __name__ == "__main__":
    unittest.main()
