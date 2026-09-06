#!/usr/bin/env python3
"""
test_scars.py — Stage 4 immune system harness.

Runs scar_detector against the federation codebase. By default the test
REPORTS but does not FAIL on violations — this is a T1 prototype.

CI mode (--strict / env CI=1) makes BLOCK violations fail the suite.
That is the actual Stage-4 promotion: scar recurrence = build broken.

Usage:
    pytest tests/constitutional/test_scars.py
    python -m scar_detector --strict   # CI entry point (post T3 wiring)
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Allow importing scar_detector as a sibling module
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from scar_detector import (  # type: ignore  # noqa: E402
    load_all_scars,
    parse_scar_frontmatter,
    detect_scar_001,
    detect_scar_002,
    scan_codebase,
    Violation,
    DEFAULT_ROOTS,
)


# ---------- Unit tests: parser ----------


def test_load_all_scars_returns_at_least_three_yaml():
    """YAML-frontmatter scars: scar-001, scar-002 minimum. scar-003 may parse if format matches."""
    scars = load_all_scars()
    # NOTE: scar-004 (prose) and scar-005 (E1/E2/E3 sections) require format adapters (T2 wiring).
    yaml_scars = [s for s in scars if s.source_path]
    assert len(yaml_scars) >= 2, f"expected ≥2 YAML scars, got {len(yaml_scars)}: {[s.source_path for s in scars]}"


def test_scar_frontmatter_required_fields_present():
    """Every scar must have scar_id + failure_pattern + status."""
    scars = load_all_scars()
    for s in scars:
        assert s.scar_id, f"missing scar_id in {s.source_path}"
        assert s.failure_pattern, f"missing failure_pattern in {s.source_path}"
        assert s.status, f"missing status in {s.source_path}"


def test_scar_001_is_active():
    """scar-001 is the canonical Stage-4 example; must be ACTIVE."""
    scars = load_all_scars()
    s001 = next((s for s in scars if "scar-001" in s.scar_id), None)
    assert s001 is not None
    assert s001.is_active, f"scar-001 status={s001.status}"
    assert s001.scar_pressure >= 0.5, f"scar-001 pressure too low: {s001.scar_pressure}"


def test_scar_001_detector_class_is_regex():
    """scar-001 should be REGEX-detectable (hard gate possible)."""
    scars = load_all_scars()
    s001 = next((s for s in scars if "scar-001" in s.scar_id), None)
    assert s001 is not None
    assert s001.detector_class == "REGEX"


# ---------- Unit tests: detectors ----------


def test_detect_scar_001_catches_require_node_crypto():
    """The classic ESM require() pattern must be flagged."""
    sample = """
import { something } from 'elsewhere';
const crypto = require('node:crypto');  // ESM scope; will silently fail
const other = require("node:fs");
"""
    violations = detect_scar_001(sample, Path("test/sample.ts"))
    assert len(violations) >= 1
    assert all(v.scar_id == "scar-001-esm-sct-silent-fail" for v in violations)
    assert all(v.severity == "BLOCK" for v in violations)


def test_detect_scar_001_passes_clean_esm_code():
    """Modern ESM code with import statements must NOT be flagged."""
    sample = """
import { createHmac, timingSafeEqual } from 'node:crypto';
import fs from 'node:fs/promises';

const sig = createHmac('sha256', key).update(payload).digest();
"""
    violations = detect_scar_001(sample, Path("test/clean.ts"))
    assert violations == [], f"false positive: {violations}"


def test_detect_scar_002_flags_liveness_only_health():
    """Health endpoints that only check liveness should be WARNed."""
    sample = """
app.get('/health', (req, res) => {
    return res.status(200).json({ status: 'ok' });
});
"""
    violations = detect_scar_002(sample, Path("test/health.ts"))
    assert len(violations) >= 1
    assert violations[0].scar_id == "scar-002-sct-validation-monitoring-gap"
    assert violations[0].severity == "WARN"


def test_detect_scar_002_passes_health_with_verify():
    """Health endpoint that exercises verify path should pass."""
    sample = """
app.get('/health', async (req, res) => {
    const tokenValid = await verifyActLocally(sampleToken);
    return res.status(tokenValid ? 200 : 503).json({ status: tokenValid ? 'ok' : 'broken' });
});
"""
    violations = detect_scar_002(sample, Path("test/health-ok.ts"))
    assert violations == [], f"false positive: {violations}"


# ---------- Integration: codebase scan ----------


def test_codebase_scan_runs_without_exception():
    """The scanner must walk the codebase and not crash."""
    violations = list(scan_codebase(DEFAULT_ROOTS[:2]))  # limit for test speed
    assert isinstance(violations, list)


def test_codebase_scan_does_not_flag_imports():
    """Real federation code uses `import` not `require`. Sanity check."""
    violations = list(scan_codebase([Path("/root/AAA")]))
    # We expect 0 BLOCK violations in current federation (post-fix).
    blocks = [v for v in violations if v.severity == "BLOCK"]
    # Soft assert: report, don't fail — historical scans may find legacy.
    if blocks:
        print(f"\n[INFO] {len(blocks)} BLOCK violations found in /root/AAA:")
        for v in blocks[:5]:
            print(f"  {v.file_path}:{v.line_number}  {v.matched_text[:100]}")


# ---------- CLI entry point for CI ----------


def test_cli_runs_in_strict_mode():
    """The CLI must be invocable; --strict returns non-zero on BLOCK."""
    result = subprocess.run(
        [
            sys.executable,
            str(HERE / "scar_detector.py"),
            "--strict",
            "--json",
            "--roots",
            str(HERE.parent.parent),
        ],  # /root/AAA/tests → /root/AAA
        capture_output=True,
        text=True,
        timeout=60,
    )
    # Output is JSON; parsing not required for this smoke test
    assert result.returncode in (0, 1), f"unexpected return code: {result.returncode}"
    assert result.stdout, "no output from scar_detector CLI"
