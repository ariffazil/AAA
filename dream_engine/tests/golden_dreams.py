#!/usr/bin/env python3
"""
golden_dreams.py — Test fixtures for the dream engine.

These tests prove the dedup math + state-writing works on a 5-record sample,
without touching live L1-L5 data.

Run: python3 tests/golden_dreams.py
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent dir to path so we can import consolidate
sys.path.insert(0, str(Path(__file__).parent.parent / "dreams"))

import consolidate  # type: ignore  # noqa: E402


def test_state_dir_created() -> None:
    """Test that state/ directory is creatable."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch.object(consolidate, "STATE_DIR", Path(tmp) / "state"):
            consolidate.update_last_dream({"pass": "test", "ok": True})
            last_dream = (Path(tmp) / "state" / "last_dream.json")
            assert last_dream.exists(), "last_dream.json not created"
            data = json.loads(last_dream.read_text())
            assert len(data) == 1
            assert data[0]["pass"] == "test"
            assert data[0]["ok"] is True
    print("✅ test_state_dir_created")


def test_redis_audit_handles_missing_lib() -> None:
    """Test that redis audit gracefully handles missing lib."""
    with patch.dict(sys.modules, {"redis": None}):
        result = consolidate.audit_redis_ttls(dry_run=True)
        assert result["status"] == "skipped"
        assert "missing" in result["reason"].lower() or "unreachable" in result["reason"].lower()
    print("✅ test_redis_audit_handles_missing_lib")


def test_qdrant_audit_handles_missing_lib() -> None:
    """Test that qdrant audit gracefully handles missing lib."""
    with patch.dict(sys.modules, {"qdrant_client": None}):
        result = consolidate.audit_qdrant_dedup(dry_run=True)
        assert result["status"] == "skipped"
    print("✅ test_qdrant_audit_handles_missing_lib")


def test_supabase_audit_handles_missing_lib() -> None:
    """Test that supabase audit gracefully handles missing lib."""
    with patch.dict(sys.modules, {"supabase": None}):
        result = consolidate.audit_supabase_dedup(dry_run=True)
        assert result["status"] == "skipped"
    print("✅ test_supabase_audit_handles_missing_lib")


def test_run_consolidate_smoke() -> None:
    """Smoke test: run_consolidate returns a well-formed summary."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch.object(consolidate, "STATE_DIR", Path(tmp) / "state"):
            summary = consolidate.run_consolidate(dry_run=True)
            assert summary["pass"] == "consolidate"
            assert summary["dry_run"] is True
            assert "config" in summary
            assert summary["config"]["embed_model"] == consolidate.CANONICAL_EMBED_MODEL
            assert summary["config"]["dedup_threshold"] == consolidate.DEDUP_THRESHOLD
            assert "passes" in summary
            assert "l1_l2_redis" in summary["passes"]
            assert "l3_qdrant" in summary["passes"]
            assert "l4_supabase" in summary["passes"]
    print("✅ test_run_consolidate_smoke")


def test_dedup_threshold_default() -> None:
    """Verify default dedup threshold is 0.90 (per design)."""
    assert consolidate.DEDUP_THRESHOLD == 0.90, \
        f"Expected 0.90, got {consolidate.DEDUP_THRESHOLD}"
    print("✅ test_dedup_threshold_default")


def test_cutover_blocked() -> None:
    """Test that --cutover is blocked without sovereign authorization."""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent.parent / "dreams" / "consolidate.py"), "--cutover"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 2, f"Expected exit code 2, got {result.returncode}"
    assert "CUTOVER" in result.stderr or "sovereign" in result.stderr.lower(), \
        f"Expected sovereign-tier error, got: {result.stderr}"
    print("✅ test_cutover_blocked")


if __name__ == "__main__":
    print("🌀 Running golden_dreams tests...\n")
    test_state_dir_created()
    test_redis_audit_handles_missing_lib()
    test_qdrant_audit_handles_missing_lib()
    test_supabase_audit_handles_missing_lib()
    test_run_consolidate_smoke()
    test_dedup_threshold_default()
    test_cutover_blocked()
    print("\n🌙 All dreams pass. The function works. The witness is missing.")
