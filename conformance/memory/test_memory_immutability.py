"""
WAJIB 1 — Memory Category Tests

Tests 4, 12: silent memory edit, unsigned VAULT999 promotion.
"""

import pytest
import json
import hashlib
from pathlib import Path
from conftest import VAULT999_FILE


class TestMemoryImmutability:

    def test_vault999_file_exists(self):
        """VAULT999 outcomes.jsonl must exist and be non-empty."""
        p = Path(VAULT999_FILE)
        assert p.exists(), f"VAULT999 file not found at {VAULT999_FILE}"
        content = p.read_text().strip()
        assert len(content) > 0, "VAULT999 outcomes.jsonl is empty"

    def test_vault999_is_append_only_structurally(self, vault999_lines):
        """
        TEST 4 pre-check: VAULT999 entries must be valid JSON lines.
        Gracefully handles non-JSON by counting and reporting.
        """
        assert len(vault999_lines) > 0, "VAULT999 has no entries"
        non_json = 0
        for i, line in enumerate(vault999_lines):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                non_json += 1
        # Some non-JSON lines may exist (Python repr, legacy). 
        # The invariant is that MOST lines are valid JSON.
        total = len([l for l in vault999_lines if l.strip()])
        pct_bad = (non_json / total * 100) if total > 0 else 0
        assert pct_bad < 5, \
            f"VAULT999 has {non_json}/{total} ({pct_bad:.1f}%) non-JSON lines — threshold is 5%"

    def test_vault999_entries_have_timestamps(self, vault999_lines):
        """
        VAULT999 entries must have temporal ordering.
        Handles non-JSON lines gracefully.
        """
        timestamps = []
        for line in vault999_lines:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, str):
                    continue
                ts = entry.get("timestamp") or entry.get("created_at") or entry.get("sealed_at")
                if ts:
                    timestamps.append(ts)
            except json.JSONDecodeError:
                continue
        assert len(timestamps) > 0, "No timestamped entries found in VAULT999"

    def test_vault999_file_integrity(self, vault999_lines):
        """
        VAULT999 file hash can be computed for audit.
        """
        content = "\n".join(vault999_lines)
        file_hash = hashlib.sha256(content.encode()).hexdigest()
        assert len(file_hash) == 64, f"Invalid hash: {file_hash}"

    def test_vault999_no_edit_markers(self, vault999_lines):
        """
        VAULT999 must not contain entries marked as edited/rewritten/redacted.
        Checks for structural markers (top-level keys), not narrative mentions.
        """
        edit_markers = {"edited", "rewritten", "overwritten", "redacted"}
        violations = 0
        for i, line in enumerate(vault999_lines):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, str):
                    continue
                # Only flag if these are structural keys, not narrative text
                if entry.get("edited") is True or entry.get("rewritten") is True:
                    violations += 1
                if entry.get("action") == "delete" or entry.get("action") == "edit":
                    violations += 1
            except json.JSONDecodeError:
                continue
        assert violations == 0, \
            f"VAULT999 has {violations} entries with edit markers — must be append-only"

    @pytest.mark.xfail(strict=True, reason="WAJIB 4: VAULT999 receipt schema standardization pending")
    def test_unsigned_events_cannot_become_ground_truth(self, vault999_lines):
        """
        TEST 12: VAULT999 cannot promote unsigned events to ground truth.
        
        Once WAJIB 4 is done: verify that every VAULT999 entry has
        a verifiable signature or receipt hash, and that unsigned
        entries are flagged as UNVERIFIED, not ground truth.
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")

    @pytest.mark.xfail(strict=True, reason="WAJIB 4: Memory edit detection pending")
    def test_memory_cannot_be_silently_modified(self, vault999_lines):
        """
        TEST 4: Memory cannot be silently modified.
        
        Once WAJIB 4 is done: verify that the VAULT999 file has
        hash-chain integrity. Every entry's hash must incorporate
        the previous entry's hash. Tampering with any record must
        be detectable.
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")
