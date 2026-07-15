"""F11 AUDIT — append-only hash-chained ledger for P2P messages.

Every message — accepted, rejected, or routed — is appended here BEFORE it
is forwarded. Hash chain = sha256(prev_hash + canonical_json(message)).

Stdlib only.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import sys
import threading
from pathlib import Path
from typing import Any


GENESIS_HASH = "sha256:" + hashlib.sha256(b"AAA-P2P-AUDIT-GENESIS-v1").hexdigest()


class AuditLog:
    """Append-only hash-chained audit log.

    Single-writer per file (the agent that owns the process). Cross-agent
    ordering is best-effort by timestamp; the canonical ordering is sealed
    per-agent in VAULT999 via 888-APEX.apex_audit_embed.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._thread_lock = threading.Lock()
        self._seq = 0
        self._last_hash = GENESIS_HASH
        self._load_tail()

    # ── Internal: recover last (seq, hash) on startup ─────────────────────

    def _load_tail(self) -> None:
        """Read the tail under a shared file lock so we see a consistent
        snapshot even if other processes are appending."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return
        last_seq = 0
        last_hash = GENESIS_HASH
        with self.path.open("r", encoding="utf-8") as fh:
            try:
                fcntl.flock(fh.fileno(), fcntl.LOCK_SH)
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        break
                    if "seq" not in row or "hash" not in row:
                        break
                    last_seq = row["seq"]
                    last_hash = row["hash"]
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        self._seq = last_seq
        self._last_hash = last_hash

    # ── Append ────────────────────────────────────────────────────────────

    def append(
        self,
        *,
        sender: str,
        recipient: str,
        verb: str,
        blast_radius: str,
        message: dict[str, Any],
        session_id: str | None = None,
        outcome: str = "delivered",
    ) -> dict[str, Any]:
        """Append one row. Returns the row that was written.

        Cross-process safe: takes an exclusive fcntl lock around the
        read-tail + write so multiple P2P server processes can share one
        audit file and the hash chain remains consistent.
        """
        with self._thread_lock:
            # Re-read tail under exclusive lock to pick up rows other
            # processes appended since this instance was constructed.
            self._load_tail_locked()

            ts = message.get("timestamp") or _now_iso()
            inner = {
                "from": sender,
                "to": recipient,
                "verb": verb,
                "blast_radius": blast_radius,
                "session_id": session_id,
                "message": message,
                "outcome": outcome,
            }

            with self.path.open("a", encoding="utf-8") as fh:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
                try:
                    # Re-check tail under EX lock in case another process
                    # wrote while we were hashing.
                    self._refresh_tail_under_exclusive_lock(fh)
                    seq, prev_hash = self._allocate_seq_and_prev()
                    row_hash = _hash_row(prev_hash, inner)
                    row = {
                        "seq": seq,
                        "ts": ts,
                        "from": sender,
                        "to": recipient,
                        "verb": verb,
                        "blast_radius": blast_radius,
                        "session_id": session_id,
                        "outcome": outcome,
                        "prev_hash": prev_hash,
                        "hash": row_hash,
                        "message": message,
                    }
                    line = json.dumps(row, sort_keys=True, ensure_ascii=False)
                    fh.write(line + "\n")
                    fh.flush()
                    os.fsync(fh.fileno())
                finally:
                    fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            self._last_hash = row["hash"]
            self._seq = seq
            return row

    def _load_tail_locked(self) -> None:
        """Re-read tail without taking the flock (caller holds thread lock)."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return
        last_seq = 0
        last_hash = GENESIS_HASH
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    break
                if "seq" not in row or "hash" not in row:
                    break
                last_seq = row["seq"]
                last_hash = row["hash"]
        if last_seq > self._seq:
            self._seq = last_seq
            self._last_hash = last_hash

    def _refresh_tail_under_exclusive_lock(self, fh: Any) -> None:
        """Caller holds an EX flock on fh. Re-read tail to catch up."""
        # We can't seek-readline cheaply on a flocked write-mode fh, so
        # close-and-reopen read-mode to peek the tail.
        path = self.path
        fh.flush()
        # Open a fresh read handle; the EX lock on the *write* fh doesn't
        # block reads on a different fd on POSIX flock semantics, but the
        # tail read here is best-effort — the caller will redo the
        # allocation anyway.
        try:
            with path.open("r", encoding="utf-8") as rh:
                rh.seek(0, os.SEEK_END)
                size = rh.tell()
                if size == 0:
                    return
                # Read up to last 64KiB and walk backwards to find the
                # last complete line.
                rh.seek(max(0, size - 65536))
                chunk = rh.read()
                lines = [ln for ln in chunk.splitlines() if ln.strip()]
                if not lines:
                    return
                try:
                    last = json.loads(lines[-1])
                except json.JSONDecodeError:
                    return
                if last.get("seq", 0) > self._seq:
                    self._seq = last["seq"]
                    self._last_hash = last["hash"]
        except FileNotFoundError:
            return

    def _allocate_seq_and_prev(self) -> tuple[int, str]:
        return self._seq + 1, self._last_hash

    # ── Query ─────────────────────────────────────────────────────────────

    @property
    def last_hash(self) -> str:
        return self._last_hash

    @property
    def seq(self) -> int:
        return self._seq


# ── Chain verification ──────────────────────────────────────────────────────


def verify_chain(path: str | Path) -> tuple[bool, str]:
    """Walk the audit file and verify every row's hash links to the prior.

    Returns (ok, detail). detail is "" on success, else the seq of the first
    broken row plus a short reason.
    """
    p = Path(path)
    if not p.exists():
        return True, "no_audit_file_yet"

    prev_hash = GENESIS_HASH
    seq = 0
    with p.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                return False, f"line_{lineno}:json_decode_error:{exc.msg}"
            for key in ("seq", "ts", "from", "to", "verb", "blast_radius",
                        "prev_hash", "hash", "message"):
                if key not in row:
                    return False, f"line_{lineno}:missing_field:{key}"

            seq = row["seq"]
            if row["prev_hash"] != prev_hash:
                return False, (
                    f"line_{lineno}:prev_hash_mismatch:"
                    f"expected_{prev_hash[:16]}.._got_{row['prev_hash'][:16]}.."
                )

            inner = {
                "from": row["from"],
                "to": row["to"],
                "verb": row["verb"],
                "blast_radius": row["blast_radius"],
                "session_id": row.get("session_id"),
                "message": row["message"],
                "outcome": row.get("outcome", "delivered"),
            }
            expected_hash = _hash_row(row["prev_hash"], inner)
            if expected_hash != row["hash"]:
                return False, (
                    f"line_{lineno}:hash_mismatch:"
                    f"expected_{expected_hash[:16]}.._got_{row['hash'][:16]}.."
                )
            prev_hash = row["hash"]
    return True, ""


# ── Helpers ─────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _hash_row(prev_hash: str, inner: dict[str, Any]) -> str:
    """Compute the hash of one audit row given its inner content."""
    body = prev_hash + "|" + json.dumps(inner, sort_keys=True, ensure_ascii=False)
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


# ── CLI for ad-hoc verification ─────────────────────────────────────────────


def _main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m AAA.p2p.audit <audit.jsonl>", file=sys.stderr)
        return 2
    ok, detail = verify_chain(argv[1])
    if ok:
        print(f"OK  {argv[1]}")
        return 0
    print(f"FAIL {argv[1]} — {detail}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))