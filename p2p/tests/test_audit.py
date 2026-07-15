"""F11 AUDIT — hash chain verification + tamper detection.

Stdlib only.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from p2p.audit import (
    GENESIS_HASH,
    AuditLog,
    _hash_row,
    verify_chain,
)
from p2p.protocol import new_message


def _mk_msg(i: int) -> dict[str, object]:
    return new_message(
        sender="333-AGI",
        recipient="888-APEX",
        verb="propose",
        payload={"i": i, "candidate": f"item-{i}"},
        blast_radius="LOW",
        requires_judgment=False,
        session_id=f"SEAL-test-{i}",
    )


# ── Tests ───────────────────────────────────────────────────────────────────


def test_append_10_messages_chain_ok(tmp_path: Path) -> None:
    audit_path = tmp_path / "audit.jsonl"
    log = AuditLog(audit_path)
    for i in range(10):
        msg = _mk_msg(i)
        log.append(
            sender=msg["from"],
            recipient=msg["to"],
            verb=msg["verb"],
            blast_radius=msg["blast_radius"],
            message=msg,
            session_id=msg.get("session_id"),
        )
    assert log.seq == 10
    ok, detail = verify_chain(audit_path)
    assert ok, detail


def test_hash_chains_depend_on_prev(tmp_path: Path) -> None:
    """Hash of row N depends on row N-1's hash."""
    audit_path = tmp_path / "audit.jsonl"
    log = AuditLog(audit_path)
    rows = []
    for i in range(3):
        msg = _mk_msg(i)
        r = log.append(
            sender=msg["from"],
            recipient=msg["to"],
            verb=msg["verb"],
            blast_radius=msg["blast_radius"],
            message=msg,
            session_id=msg.get("session_id"),
        )
        rows.append(r)
    # Each row's prev_hash == previous row's hash.
    assert rows[0]["prev_hash"] == GENESIS_HASH
    assert rows[1]["prev_hash"] == rows[0]["hash"]
    assert rows[2]["prev_hash"] == rows[1]["hash"]


def test_tamper_one_line_breaks_chain(tmp_path: Path) -> None:
    """Edit a message in row 5; verify_chain must return False."""
    audit_path = tmp_path / "audit.jsonl"
    log = AuditLog(audit_path)
    for i in range(10):
        msg = _mk_msg(i)
        log.append(
            sender=msg["from"],
            recipient=msg["to"],
            verb=msg["verb"],
            blast_radius=msg["blast_radius"],
            message=msg,
            session_id=msg.get("session_id"),
        )

    # Sanity: chain OK before tamper.
    ok, _ = verify_chain(audit_path)
    assert ok

    # Read all lines, mutate row index 5 (the 6th message).
    lines = audit_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 10
    target = json.loads(lines[5])
    target["message"]["payload"]["candidate"] = "TAMPERED"
    lines[5] = json.dumps(target, sort_keys=True, ensure_ascii=False)
    audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok, detail = verify_chain(audit_path)
    assert not ok, "tamper was not detected"
    assert "line_6" in detail or "hash_mismatch" in detail


def test_tamper_prev_hash_breaks_chain(tmp_path: Path) -> None:
    """Rewriting a row's prev_hash breaks the chain immediately."""
    audit_path = tmp_path / "audit.jsonl"
    log = AuditLog(audit_path)
    for i in range(5):
        msg = _mk_msg(i)
        log.append(
            sender=msg["from"],
            recipient=msg["to"],
            verb=msg["verb"],
            blast_radius=msg["blast_radius"],
            message=msg,
            session_id=msg.get("session_id"),
        )

    lines = audit_path.read_text(encoding="utf-8").splitlines()
    target = json.loads(lines[2])
    target["prev_hash"] = "sha256:" + "0" * 64
    lines[2] = json.dumps(target, sort_keys=True, ensure_ascii=False)
    audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok, detail = verify_chain(audit_path)
    assert not ok
    assert "prev_hash_mismatch" in detail


def test_append_reloads_last_seq(tmp_path: Path) -> None:
    """Reopening the audit log must continue from the last good seq."""
    audit_path = tmp_path / "audit.jsonl"
    log = AuditLog(audit_path)
    for i in range(4):
        msg = _mk_msg(i)
        log.append(
            sender=msg["from"],
            recipient=msg["to"],
            verb=msg["verb"],
            blast_radius=msg["blast_radius"],
            message=msg,
            session_id=msg.get("session_id"),
        )
    assert log.seq == 4

    log2 = AuditLog(audit_path)
    assert log2.seq == 4
    assert log2.last_hash == log.last_hash

    msg = _mk_msg(99)
    log2.append(
        sender=msg["from"],
        recipient=msg["to"],
        verb=msg["verb"],
        blast_radius=msg["blast_radius"],
        message=msg,
        session_id=msg.get("session_id"),
    )
    assert log2.seq == 5
    ok, _ = verify_chain(audit_path)
    assert ok


def test_empty_file_is_ok(tmp_path: Path) -> None:
    """No audit file yet, or an empty file, is treated as a clean chain."""
    audit_path = tmp_path / "does_not_exist.jsonl"
    ok, detail = verify_chain(audit_path)
    assert ok
    assert detail == "no_audit_file_yet"

    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    ok, detail = verify_chain(empty)
    assert ok
    assert detail == ""


def test_hash_row_deterministic() -> None:
    """Hash of identical inputs is identical (canonical JSON, sorted keys)."""
    inner = {
        "sender": "333-AGI",
        "recipient": "888-APEX",
        "verb": "ack",
        "blast_radius": "LOW",
        "session_id": None,
        "message": {"x": 1, "y": [1, 2, 3]},
        "outcome": "delivered",
    }
    a = _hash_row(GENESIS_HASH, inner)
    b = _hash_row(GENESIS_HASH, inner)
    assert a == b
    assert a.startswith("sha256:")