#!/usr/bin/env python3
"""effect_guard.py — U12 external-effect idempotency guard + replay-in-observe.

Gate-2 item 5 (FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 U12, 2026-09-12).
Mechanizes the v1.1 ambiguous-commit protocol at the additive layer:
  durable intent before effect -> idempotency identity -> outcome entry ->
  UNKNOWN reconciliation, never blind retry.

Registry: append-only JSONL of effect attempts/outcomes at
  /root/.local/share/arifos/effect_registry.jsonl (same family as
  pending_receipts.jsonl / opencode_receipts.jsonl).

Semantics:
  check --key K     rc=0 = no committed prior (safe to fire)
                   rc=2 = committed prior exists (DO NOT re-fire; reconcile)
  register ...      appends {key, kind, target, status, ts, actor, refs}
                   status ∈ attempted|committed|denied|unknown
  replay            effect timeline merged with AAA commit history within a
                   window — REPLAY-IN-OBSERVE: read-only reconstruction,
                   no effect re-fired; commits annotate the policy state in
                   force at effect time (version pinning, not current-HEAD).

Enforcement is convention + tool tonight; Hermes send-path and kernel
first-class field are scoped to their lanes (UL-007 do-not-cascade).

DITEMPA BUKAN DIBERI.
"""

import argparse
import fcntl
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY = Path("/root/.local/share/arifos/effect_registry.jsonl")
STATUSES = {"attempted", "committed", "denied", "unknown"}


def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load():
    if not REGISTRY.exists():
        return []
    out = []
    for line in REGISTRY.read_text(errors="replace").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def parse_refs(raw):
    refs = []
    if raw:
        for pair in raw.split(","):
            if ":" not in pair:
                print(f"ERR refs entry '{pair.strip()}' must be kind:ref", file=sys.stderr)
                sys.exit(1)
            kind, ref = pair.split(":", 1)
            refs.append({"kind": kind.strip(), "ref": ref.strip()})
    return refs


def do_check(key):
    priors = [e for e in load() if e.get("key") == key]
    if not priors:
        print(f"SAFE — key '{key}' has no prior entry (register attempted BEFORE firing)")
        return 0
    for e in priors:
        print(f"  {e.get('ts')} {e.get('status','?'):9} {e.get('kind','?')} -> {e.get('target','?')}")
    if any(e.get("status") == "committed" for e in priors):
        print(f"BLOCKED — committed prior exists for '{key}': DO NOT re-fire; reconcile against external state (U12/U13)")
        return 2
    print(f"CAUTION — prior attempt(s) exist, none committed: verify external state before re-fire")
    return 0


def do_register(args):
    if args.status not in STATUSES:
        print(f"ERR status must be one of {sorted(STATUSES)}", file=sys.stderr)
        sys.exit(1)
    entry = {
        "key": args.key,
        "kind": args.kind,
        "target": args.target,
        "status": args.status,
        "ts": now_ts(),
        "actor": args.actor,
    }
    refs = parse_refs(args.refs)
    if refs:
        entry["refs"] = refs
    if args.note:
        entry["note"] = args.note
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)
    print(f"REGISTERED {args.status} key={args.key} kind={args.kind} target={args.target}")


def do_replay(window_h):
    cutoff = datetime.now(timezone.utc).timestamp() - window_h * 3600
    events = []
    for e in load():
        try:
            ts = datetime.strptime(e.get("ts", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if ts.timestamp() >= cutoff:
            events.append((ts, f"[effect] {e.get('status','?'):9} {e.get('kind','?')} -> {e.get('target','?')} key={e.get('key','?')}"))
    try:
        since = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        r = subprocess.run(
            ["git", "-C", "/root/AAA", "log", f"--since={window_h} hours", "--format=%cI|%h|%s"],
            capture_output=True, text=True, timeout=20,
        )
        for line in r.stdout.splitlines():
            iso, sha, subject = line.split("|", 2)
            try:
                ts = datetime.fromisoformat(iso)
            except ValueError:
                continue
            events.append((ts, f"[policy] {sha} {subject[:90]}"))
    except Exception:
        pass
    events.sort(key=lambda x: x[0])
    print(f"REPLAY-IN-OBSERVE (window {window_h}h) — read-only, no effects re-fired")
    print("NOTE: arifFlow receipt layer not indexed (unprobed) — timeline partial per Claim Layer = Evidence Layer")
    for ts, line in events:
        print(f"  {ts.astimezone(timezone.utc).strftime('%H:%M:%SZ')} {line}")
    return 0


def main():
    p = argparse.ArgumentParser(description="U12 effect idempotency guard + replay-in-observe")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--key", required=True)
    r = sub.add_parser("register")
    r.add_argument("--key", required=True)
    r.add_argument("--kind", required=True)
    r.add_argument("--target", required=True)
    r.add_argument("--status", required=True)
    r.add_argument("--actor", required=True)
    r.add_argument("--refs")
    r.add_argument("--note")
    w = sub.add_parser("replay")
    w.add_argument("--window-h", type=int, default=3, dest="window_h")
    args = p.parse_args()

    if args.cmd == "check":
        sys.exit(do_check(args.key))
    if args.cmd == "register":
        do_register(args)
    if args.cmd == "replay":
        sys.exit(do_replay(args.window_h))


if __name__ == "__main__":
    main()
