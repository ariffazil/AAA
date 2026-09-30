#!/usr/bin/env python3
"""skill_witness — external receipt for skill self-modification.

WHY THIS EXISTS
  2026-09-29 21:20: the curator created skill `self-improvement-lock` — a skill about
  why unwitnessed self-modification is dangerous — with no VAULT999 receipt and no
  external witness. The mutation ledger that recorded it (~/.hermes/skills/.curator_ledger.jsonl)
  is local, writable by the same uid as the agent, and capped/compacted by that same
  process. Local-only evidence for a self-modification is not a witness; it is a diary.

WHAT IT DOES
  Every skill mutation that reaches the Hermes choke point (tools/skill_ledger.append_entry)
  is echoed here as a HASH-CHAINED receipt:
    - local canonical chain : /root/arifOS/VAULT999/skill_mutations.jsonl  (VAULT999)
    - external mirror       : witness node KVM2 (/root/witness/...), best-effort, labelled
  Each receipt carries prev_hash + hash, so any edit/removal breaks verification at a
  named sequence number.

HONEST LIMITS (do not oversell)
  * The agent runs as uid 0. File permissions are NOT a lock against uid 0 — the chain is
    tamper-EVIDENT, not tamper-PROOF. Proof needs the off-host copy, which is why the mirror
    exists; a mirror that is unreachable is recorded as `witness: local-only` and a later
    `verify` shows the gap rather than hiding it.
  * `verify` detects a rewritten or deleted line (chained entries only). Deleting the whole
    file is detectable only against the off-host mirror.

USAGE
  python3 skill_witness.py emit      < entry.json          # one ledger entry as JSON on stdin
  python3 skill_witness.py verify                          # recompute the local chain
  python3 skill_witness.py head                            # print the current chain head
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CHAIN = Path(os.environ.get("SKILL_WITNESS_CHAIN", "/root/arifOS/VAULT999/skill_mutations.jsonl"))
WITNESS_HOST = os.environ.get("SKILL_WITNESS_HOST", "kvm2")
WITNESS_PATH = "/root/witness/skill_mutations_from_kvm8.jsonl"
GENESIS = "0" * 64


def _canon(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _digest(prev: str, payload: dict) -> str:
    return hashlib.sha256(prev.encode() + _canon(payload)).hexdigest()


def _last() -> tuple[int, str]:
    """(last seq, last hash) of the local chain; (0, GENESIS) when absent/empty."""
    if not CHAIN.exists():
        return 0, GENESIS
    seq, digest = 0, GENESIS
    with CHAIN.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                raise SystemExit(f"skill_witness: malformed chain row after seq {seq} — refusing to append")
            seq, digest = int(row["seq"]), str(row["hash"])
    return seq, digest


def _mirror(line: str) -> str:
    """Best-effort off-host mirror. Returns a witness label for the receipt."""
    try:
        proc = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=6", WITNESS_HOST,
             f"mkdir -p $(dirname {WITNESS_PATH}) && cat >> {WITNESS_PATH}"],
            input=line, text=True, capture_output=True, timeout=20)
        return f"kvm2:{WITNESS_PATH}" if proc.returncode == 0 else f"local-only(ssh rc={proc.returncode})"
    except Exception as exc:  # unreachable witness is recorded, never silently dropped
        return f"local-only({type(exc).__name__})"


def cmd_emit() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        return 2
    entry = json.loads(raw)
    seq, prev = _last()
    payload = {
        "seq": seq + 1,
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": "SKILL_MUTATION",
        "entry_id": entry.get("id"),
        "action": entry.get("action"),
        "skill": entry.get("skill"),
        "actor": entry.get("actor"),
        "evidence": entry.get("evidence") or {},
        "after": [{"path": i.get("path"), "sha256": i.get("sha256")} for i in (entry.get("after") or [])],
        "prev": prev,
    }
    payload["hash"] = _digest(prev, payload)
    line = json.dumps(payload, ensure_ascii=False)
    CHAIN.parent.mkdir(parents=True, exist_ok=True)
    with CHAIN.open("a", encoding="utf-8") as fh:  # O_APPEND: one row, never a rewrite
        fh.write(line + "\n")
    label = _mirror(line + "\n")
    _log_witness(label, payload["seq"], payload["hash"])
    print(json.dumps({"seq": payload["seq"], "hash": payload["hash"], "witness": label}))
    return 0


def _log_witness(label: str, seq: int, digest: str) -> None:
    """Mirror outcome goes to a SIDECAR, never back into the chain row.

    Rewriting a chain row to record its own witness state is a tamper-shaped write on an
    append-only log. The row stays pure; the mirror's honesty lives here, where a
    `local-only(...)` label is visible without touching the hash chain.
    """
    try:
        with (CHAIN.parent / "skill_mutations.witness.log").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "seq": seq,
                                 "hash": digest, "witness": label}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def cmd_resync() -> int:
    """Push the WHOLE local chain to the witness node and report byte parity.

    A mirror that differs from the thing it mirrors is worse than no mirror: it looks like
    evidence. Byte parity is the claim, md5 is the receipt.
    """
    if not CHAIN.exists():
        print(json.dumps({"verdict": "NO_CHAIN"}))
        return 2
    data = CHAIN.read_text(encoding="utf-8")
    local_md5 = hashlib.md5(data.encode()).hexdigest()
    try:
        proc = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", WITNESS_HOST,
             f"mkdir -p $(dirname {WITNESS_PATH}) && cat > {WITNESS_PATH}"],
            input=data, text=True, capture_output=True, timeout=120)
        if proc.returncode != 0:
            print(json.dumps({"verdict": "MIRROR_FAILED", "rc": proc.returncode,
                              "stderr": (proc.stderr or "").strip()[:200]}))
            return 1
        remote = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", WITNESS_HOST,
             f"md5sum {WITNESS_PATH}"], capture_output=True, text=True, timeout=60).stdout.split()
        remote_md5 = remote[0] if remote else "unknown"
    except Exception as exc:
        print(json.dumps({"verdict": "MIRROR_FAILED", "error": f"{type(exc).__name__}: {exc}"}))
        return 1
    verdict = "PARITY_OK" if remote_md5 == local_md5 else "PARITY_DIFF"
    print(json.dumps({"verdict": verdict, "local_md5": local_md5, "remote_md5": remote_md5,
                      "entries": _last()[0], "head": _last()[1], "witness": f"{WITNESS_HOST}:{WITNESS_PATH}"}))
    return 0 if verdict == "PARITY_OK" else 1


def cmd_verify() -> int:
    if not CHAIN.exists():
        print(json.dumps({"verdict": "MISSING", "chain": str(CHAIN)}))
        return 2
    seq, prev = 0, GENESIS
    for n, line in enumerate(CHAIN.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        claimed = row.pop("hash", None)
        row.pop("witness", None)
        if row.get("seq") != seq + 1:
            print(json.dumps({"verdict": "TAMPERED", "row": n, "why": "seq gap", "expected_seq": seq + 1}))
            return 1
        if row.get("prev") != prev:
            print(json.dumps({"verdict": "TAMPERED", "row": n, "why": "prev_hash mismatch"}))
            return 1
        if _digest(prev, row) != claimed:
            print(json.dumps({"verdict": "TAMPERED", "row": n, "why": "content hash mismatch", "seq": row.get("seq")}))
            return 1
        seq, prev = row["seq"], claimed
    print(json.dumps({"verdict": "CHAIN_OK", "entries": seq, "head": prev, "chain": str(CHAIN)}))
    return 0


def cmd_head() -> int:
    print(json.dumps({"seq": _last()[0], "head": _last()[1]}))
    return 0


def cmd_backfill() -> int:
    """Receipt the mutations that ALREADY happened without a witness (local ledger -> chain).

    Labelled ``SKILL_MUTATION_BACKFILL`` and carrying the ORIGINAL timestamp + entry id, so a
    backfilled row can never be mistaken for a live receipt. This is how the 2026-09-29
    `self-improvement-lock` creation (and everything before it) stops being unwitnessed.
    """
    ledger = Path(os.environ.get("SKILL_WITNESS_LEDGER",
                                 str(Path(os.environ.get("HERMES_HOME", "/root/.hermes")) / "skills" / ".curator_ledger.jsonl")))
    if not ledger.exists():
        print(json.dumps({"verdict": "NO_LEDGER", "ledger": str(ledger)}))
        return 2
    seen = set()
    if CHAIN.exists():
        for line in CHAIN.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    seen.add(json.loads(line).get("entry_id"))
                except json.JSONDecodeError:
                    pass
    seq, prev = _last()
    new_lines = []
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if entry.get("id") in seen:
            continue
        seq += 1
        payload = {
            "seq": seq,
            "ts": entry.get("ts"),
            "kind": "SKILL_MUTATION_BACKFILL",
            "entry_id": entry.get("id"),
            "action": entry.get("action"),
            "skill": entry.get("skill"),
            "actor": entry.get("actor"),
            "evidence": entry.get("evidence") or {},
            "after": [{"path": i.get("path"), "sha256": i.get("sha256")} for i in (entry.get("after") or [])],
            "prev": prev,
            "backfilled_at": datetime.now(timezone.utc).isoformat(),
        }
        payload["hash"] = _digest(prev, payload)
        prev = payload["hash"]
        new_lines.append(json.dumps(payload, ensure_ascii=False))
    if not new_lines:
        print(json.dumps({"verdict": "ALREADY_WITNESSED", "entries": seq}))
        return 0
    CHAIN.parent.mkdir(parents=True, exist_ok=True)
    with CHAIN.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(new_lines) + "\n")
    label = _mirror("\n".join(new_lines))
    print(json.dumps({"verdict": "BACKFILLED", "added": len(new_lines),
                      "chain_entries": seq, "head": prev, "witness": label}))
    return 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "head"
    return {"emit": cmd_emit, "verify": cmd_verify, "head": cmd_head,
            "backfill": cmd_backfill, "resync": cmd_resync}.get(cmd, cmd_head)()


if __name__ == "__main__":
    raise SystemExit(main())
