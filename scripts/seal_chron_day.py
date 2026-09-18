#!/usr/bin/env python3
"""seal_chron_day.py — consolidate everything from 2026-09-18 into one hash-chained record.

WHY THIS IS A RECEIPT AND NOT A SEAL
  The kernel was asked. It answered: seal_allowed=false, mutation_allowed=false,
  actor_cryptographically_verified=false, autonomy_band=OBSERVE_ONLY. A Lane A
  constitutional SEAL requires a judge_state_hash, a witness, and an actor the
  substrate recognises. This seat has none of those.

  The seal-discipline doctrine is explicit: "I will not call RECEIPT a SEAL. I
  will not write the word SEAL without the hash chain." So this artifact computes
  a real hash chain and refuses to call itself a seal. Naming honesty is the
  control; a document that overstates itself is the defect this whole day was
  spent finding.

WHAT IT DOES
  1. Walks every artifact named in the day's work: audit records, distillates,
     seals, the claim ledger, and every code file the ledger references.
  2. Computes sha256 for each.
  3. Builds a chain: each row carries the previous row's hash, so the record
     cannot be edited in the middle without breaking every row after it.
  4. Records the kernel's refusal verbatim as the reason this is Lane B.
  5. Emits one file plus a sidecar .sha256.

READ-ONLY on everything except its two outputs.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

RUN = Path("/root/AAA/forge_work/chron-audit")
LEDGER = Path("/root/AAA/claim_ledger/claims.db")
MYT = timezone(timedelta(hours=8))

OUT = RUN / "RECORD-CHRON-2026-09-18.json"
SIDECAR = RUN / "RECORD-CHRON-2026-09-18.sha256"

# Code files the claim ledger or the seals reference. Each is hashed as it
# exists now; a later edit will break the chain, which is the point.
CODE = [
    "/root/AAA/scripts/alpha_zen_card.py",
    "/root/AAA/scripts/alpha_zen_gate.py",
    "/root/AAA/scripts/alpha_zen_infographic.py",
    "/root/AAA/scripts/alpha_zen_card.schema.json",
    "/root/AAA/scripts/chron.py",
    "/root/AAA/scripts/chron_events.json",
    "/root/AAA/scripts/chron_events.schema.json",
    "/root/AAA/scripts/chron_spine_gate.py",
    "/root/AAA/scripts/semantic_authority_gate.py",
    "/root/AAA/scripts/musyawarah_gate.py",
    "/root/AAA/scripts/test_alpha_zen_gate.py",
    "/root/AAA/scripts/cron_failure_autopause.py",
    "/root/AAA/scripts/apex-zen-compact.py",
    "/root/AAA/registries/federated-recurrence.yaml",
    "/root/scripts/alpha_zen_engine.py",
    "/root/A-FORGE/hooks/pre-commit-lsp-gate.sh",
]


def h_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def h_file(p: Path) -> str | None:
    try:
        return h_bytes(p.read_bytes())
    except Exception:
        return None


def git_head(repo: str) -> str:
    try:
        r = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except Exception:
        return "unknown"


def git_commits_today(repo: str) -> int:
    try:
        r = subprocess.run(["git", "-C", repo, "log", "--since=2026-09-18 00:00",
                            "--oneline"], capture_output=True, text=True, timeout=20)
        return len([l for l in r.stdout.splitlines() if l.strip()])
    except Exception:
        return 0


def main() -> int:
    now = datetime.now(MYT)
    rows: list[dict] = []
    prev = "GENESIS"

    def add(kind: str, path: str | None, sha: str | None, note: str = "") -> None:
        nonlocal prev
        row = {"i": len(rows), "kind": kind, "path": path,
               "sha256": sha, "note": note, "prev": prev}
        row["row_hash"] = h_bytes(json.dumps(row, sort_keys=True).encode())
        prev = row["row_hash"]
        rows.append(row)

    # 1. the day's audit artifacts
    for p in sorted(RUN.glob("*.json")):
        add("artifact", str(p), h_file(p))

    # 2. the code under record
    for c in CODE:
        p = Path(c)
        add("code", c, h_file(p), "" if p.exists() else "MISSING")

    # 3. the claim ledger (the durable record)
    add("ledger", str(LEDGER), h_file(LEDGER))

    # 4. repo heads
    for repo in ("/root/AAA", "/root/scripts", "/root/A-FORGE", "/root/arifOS"):
        add("repo_head", repo, git_head(repo),
            f"{git_commits_today(repo)} commit(s) today")

    body = {
        "record_id": "RECORD-CHRON-2026-09-18",
        "created": now.isoformat(timespec="seconds"),
        "created_utc": now.astimezone(timezone.utc).isoformat(timespec="seconds"),

        "what_this_is": "RECEIPT (Lane B). NOT a constitutional SEAL.",
        "why_not_a_seal": {
            "asked": "kernel arif_init at :8088, 2026-09-18T11:47 MYT",
            "kernel_answer": {
                "seal_allowed": False,
                "mutation_allowed": False,
                "actor_cryptographically_verified": False,
                "autonomy_band": "OBSERVE_ONLY",
                "effective_verdict": "HOLD",
                "reason_code": "NEEDS_REVIEW",
            },
            "consequence": "A Lane A SEAL requires judge_state_hash + witness + a "
                           "recognised actor. This seat has none. Per seal-discipline: "
                           "'I will not call RECEIPT a SEAL. I will not write the word "
                           "SEAL without the hash chain.'",
            "so": "this file carries a real hash chain and refuses the word SEAL.",
        },

        "chain": {
            "algorithm": "sha256",
            "rule": "row_hash = sha256(json(previous row incl. its prev)). "
                    "Editing any row breaks every row after it.",
            "rows": rows,
            "terminal_hash": prev,
            "row_count": len(rows),
        },

        "what_it_covers": {
            "audit_artifacts": len([r for r in rows if r["kind"] == "artifact"]),
            "code_files": len([r for r in rows if r["kind"] == "code"]),
            "missing_code": [r["path"] for r in rows
                             if r["kind"] == "code" and r["note"] == "MISSING"],
            "claim_ledger": str(LEDGER),
            "repo_heads": {r["path"]: r["sha256"] for r in rows
                           if r["kind"] == "repo_head"},
        },

        "open_items": [
            "14:00 ALPHA-ZEN Body Check has NOT fired. Recorded as VOID in the claim "
            "ledger (clm-01c59438b9d22cda). Must be superseded by an OBS after the run.",
            "The 06:00 docforge job's first scheduled fire is tomorrow 06:00. Its "
            "dispatch path is a dry run today; delivery is unproven.",
            "alpha_zen_engine.py carries uncommitted working-tree changes. Two writers "
            "touched it; a classifier agent is judging whether they are deliberate.",
            "A-FORGE world-model-lite.jsonl stopped writing 2026-08-27 (22 days). "
            "Root cause unknown.",
            "kernel tools.py lines 140 and 153 accept a LABEL and a SUBSTRING as "
            "deployment-drift proof. Latent; no current false label observed.",
            "identity.py:87 returns a bare 'status' constant while holding both commits "
            "needed to compute drift. Staged fix written, NOT applied.",
            "One subagent (artifact manifest) still running at record time.",
        ],

        "chron_state": "EXPERIMENTAL",
        "state_reason": "0 of 3 ALPHA-ZEN jobs have fired; the arrow chain is unproven",

        "next_single_action": "14:00 MYT — witness the nine arrows. Supersede the VOID "
                              "claim with an OBS. Nothing else.",
    }

    OUT.write_text(json.dumps(body, indent=2, ensure_ascii=False))
    digest = h_file(OUT) or "UNHASHABLE"
    SIDECAR.write_text(f"{digest}  {OUT.name}\n")

    print(f"  wrote   {OUT.name}  ({OUT.stat().st_size} bytes)")
    print(f"  rows    {len(rows)}   terminal {prev[:16]}")
    print(f"  digest  {digest[:16]}")
    missing = [r["path"] for r in rows if r["note"] == "MISSING"]
    if missing:
        print(f"  MISSING code files: {missing}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
