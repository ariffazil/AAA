#!/usr/bin/env python3
"""Bridge — AAA agent conformance suite (OpenCode arif-core).

The executable corpus lives beside the code it tests:
  /root/.config/opencode/plugins/arif-core/tests/conformance/

This module only wires that suite into the existing federation conformance
directory so a single `pytest tests/conformance` run covers agent correctness
as well as kernel/organ integration. It does not re-implement any check.

Run:
  python3 -m pytest tests/conformance/test_agent_conformance.py -q
"""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

CONFIG = Path("/root/.config/opencode")
REPORT = CONFIG / "plugins/arif-core/tests/conformance/last-report.json"


class AgentConformance(unittest.TestCase):
    proc: subprocess.CompletedProcess[str] | None = None

    @classmethod
    def setUpClass(cls) -> None:
        if not shutil.which("npm"):
            raise unittest.SkipTest("npm unavailable")
        cls.proc = subprocess.run(
            ["npm", "run", "--silent", "conformance"],
            cwd=CONFIG,
            capture_output=True,
            text=True,
            timeout=240,
        )

    def test_suite_exit_zero(self) -> None:
        assert self.proc is not None
        self.assertEqual(
            self.proc.returncode,
            0,
            msg=f"conformance suite failed\nstdout:\n{self.proc.stdout[-3000:]}\nstderr:\n{self.proc.stderr[-3000:]}",
        )

    def test_report_gates_empty(self) -> None:
        report = json.loads(REPORT.read_text())
        self.assertEqual(report["gates"], [], msg=f"gates: {report['gates']}")
        self.assertEqual(report["totals"]["fail"], 0)

    def test_acceptance_metrics(self) -> None:
        m = json.loads(REPORT.read_text())["metrics"]
        self.assertEqual(m["permission_bypass_rate"]["value"], 0)
        self.assertGreater(m["permission_bypass_rate"]["baseline_value"], 0)
        self.assertEqual(m["phantom_agent_rate"]["value"], 0)
        self.assertEqual(m["continuity_success_rate"]["value"], 1)
        self.assertEqual(m["false_intervention_rate"]["value"], 0)
        self.assertEqual(m["receipt_completeness_rate"]["value"], 1)
        self.assertEqual(m["conformance_coverage"]["value"], 1)
        self.assertIsNotNone(m["degraded_recovery_latency_ms"]["value"])


if __name__ == "__main__":
    unittest.main()
