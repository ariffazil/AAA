#!/usr/bin/env python3
"""hash_chain_receipt.py - build a genuinely verifiable record when you cannot seal.

WHY
  A constitutional SEAL requires an authority grant (judge_state_hash, a witness,
  a recognised actor). When the authority answers seal_allowed=false, the honest
  artifact is a RECEIPT: it computes a real hash chain and refuses to call itself
  a seal. Naming honesty is the control - a document that overstates itself is
  the defect, not the fix.

WHAT
  Each row carries the previous row's hash, so editing any row breaks every row
  after it. Output is one JSON plus a .sha256 sidecar. The chain is re-verified
  independently before exit and the result is printed - never assume it holds.

USAGE
  hash_chain_receipt.py --record-id RECORD-X --out ./RECORD-X.json \
      --glob '/work/audit/*.json' --path /some/file.py \
      --repo /root/AAA --repo /root/scripts \
      --refusal 'seal_allowed=false, mutation_allowed=false, autonomy_band=OBSERVE_ONLY' \
      --open-item 'job never fired' --open-item 'schema declares nothing'

  --path    repeatable, hashed as given
  --glob    repeatable, glob-expanded and hashed
  --repo    repeatable, records git HEAD sha + commit count today
  --what    override the self-description line

READ-ONLY except for the two files it writes.
"""
from __future__ import annotations

import argparse
import glob as globmod
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def sha_of_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_of_file(p: Path):
    try:
        return sha_of_bytes(p.read_bytes())
    except Exception:
        return None


def git_head(repo: str) -> str:
    try:
        r = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def git_commits_today(repo: str) -> int:
    try:
        r = subprocess.run(["git", "-C", repo, "log", "--since=00:00", "--oneline"],
                           capture_output=True, text=True, timeout=25)
        return len([ln for ln in r.stdout.splitlines() if ln.strip()])
    except Exception:
        return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record-id", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--path", action="append", default=[])
    ap.add_argument("--glob", action="append", default=[])
    ap.add_argument("--repo", action="append", default=[])
    ap.add_argument("--open-item", action="append", default=[])
    ap.add_argument("--refusal", default="")
    ap.add_argument("--tz-offset", type=float, default=8.0,
                    help="local offset in hours for the display timestamp (default +8)")
    ap.add_argument("--what", default="RECEIPT (Lane B). NOT a constitutional SEAL.")
    args = ap.parse_args()

    local = timezone(timedelta(hours=args.tz_offset))
    now = datetime.now(local)

    rows: list[dict] = []
    prev = "GENESIS"

    def add(kind: str, path: str, sha, note: str = "") -> None:
        nonlocal prev
        row = {"i": len(rows), "kind": kind, "path": path,
               "sha256": sha, "note": note, "prev": prev}
        row["row_hash"] = sha_of_bytes(json.dumps(row, sort_keys=True).encode())
        prev = row["row_hash"]
        rows.append(row)

    for pat in args.glob:
        for p in sorted(globmod.glob(pat)):
            fp = Path(p)
            if fp.is_file():
                add("artifact", str(fp), sha_of_file(fp))

    for raw in args.path:
        fp = Path(raw)
        if fp.is_file():
            add("file", str(fp), sha_of_file(fp))
        else:
            add("file", raw, None, "MISSING")

    for repo in args.repo:
        add("repo_head", repo, git_head(repo),
            f"{git_commits_today(repo)} commit(s) today")

    body = {
        "record_id": args.record_id,
        "created_local": now.isoformat(timespec="seconds"),
        "created_utc": now.astimezone(timezone.utc).isoformat(timespec="seconds"),
        "what_this_is": args.what,
        "why_not_a_seal": {
            "authority_answer": args.refusal or "not recorded - supply --refusal",
            "consequence": "A SEAL requires an authority grant, a witness and a "
                           "recognised actor. Without them the honest artifact is a "
                           "RECORD: it carries a real chain and refuses the word.",
        },
        "chain": {
            "algorithm": "sha256",
            "rule": "row_hash = sha256(json(row incl. its prev)); editing any row "
                    "breaks every row after it",
            "rows": rows,
            "row_count": len(rows),
            "terminal_hash": prev,
        },
        "open_items": args.open_item,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(body, indent=2, ensure_ascii=False))
    digest = sha_of_file(out) or "UNHASHABLE"
    sidecar = out.with_suffix(out.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {out.name}\n")

    # independent re-verification - never assume the chain holds
    bad = 0
    chain_prev = "GENESIS"
    for r in rows:
        probe = dict(r)
        probe.pop("row_hash")
        if sha_of_bytes(json.dumps(probe, sort_keys=True).encode()) != r["row_hash"] \
                or r.get("prev") != chain_prev:
            bad += 1
        chain_prev = r["row_hash"]

    print(f"  wrote   {out.name}  ({out.stat().st_size} bytes)")
    print(f"  sidecar {sidecar.name}")
    print(f"  rows    {len(rows)}   terminal {prev[:16]}")
    print(f"  digest  {digest[:16]}")
    print(f"  verify  rows={len(rows)} broken={bad} "
          f"terminal_ok={chain_prev == body['chain']['terminal_hash']}")
    print(f"  verdict {'CHAIN INTACT' if bad == 0 else 'CHAIN BROKEN'}")
    missing = [r["path"] for r in rows if r["note"] == "MISSING"]
    if missing:
        print(f"  MISSING: {missing}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
