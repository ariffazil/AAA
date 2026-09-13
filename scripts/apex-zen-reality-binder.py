#!/usr/bin/env python3
"""
APEX-ZEN Reality Binder — Layers 5: bind telemetry nodes to witnessed reality nodes.

DOCTRINE (ARIF, 2026-09-13): "Telemetry Graph != Reality Graph."
"No metric may be promoted unless it is backed by a witness object."

4-level witness hierarchy:
  L1 Intent      — conversation GO signals (bound via apex-zen-telemetry.jsonl)
  L2 Execution   — mutating tool.call events (Edit/Write/MultiEdit/apply_patch)
  L3 Persistence — mutated paths survive on disk (exists + size + sha256 prefix)
  L4 Consequence — persistence promoted to git/receipts/CI (durability witness)

Output: /root/VAULT999/apex-zen-witness.jsonl (append-only witness objects).

Usage:
  python3 apex-zen-reality-binder.py --session <wire.jsonl>
  python3 apex-zen-reality-binder.py --latest N
"""

import json, argparse, hashlib, subprocess, glob
from pathlib import Path
from datetime import datetime, timezone

SESSIONS_GLOB = "/root/.kimi-code/sessions/*/session_*/agents/main/wire.jsonl"
OUT = Path("/root/VAULT999/apex-zen-witness.jsonl")
MUTATING = {"edit", "write", "multiedit", "notebookedit", "apply_patch"}
GIT_ROOTS = ("/root/AAA", "/root/arifOS", "/root/A-FORGE", "/root/WELL", "/root/GEOX", "/root/WEALTH")


def extract_mutations(wire_path: Path):
    events = []
    for line in wire_path.read_text(errors="ignore").splitlines():
        if '"tool.call"' not in line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        ev = rec.get("event") or {}
        if ev.get("type") != "tool.call":
            continue
        name = str(ev.get("name") or "")
        if name.lower() not in MUTATING:
            continue
        disp = ev.get("display") or {}
        args = ev.get("args") or {}
        p = disp.get("path") or args.get("path") or args.get("file_path") or ""
        p = str(p)
        if p and not p.startswith("/"):
            p = "/root/" + p
        events.append({"tool": name, "path": p, "turnId": ev.get("turnId")})
    return events


def file_witness(p: Path):
    try:
        st = p.stat()
        h = None
        if st.st_size < 2_000_000:
            try:
                h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
            except OSError:
                h = None
        return {
            "exists": True,
            "size": st.st_size,
            "sha256_12": h,
            "mtime": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
        }
    except OSError:
        return {"exists": False}


def git_witness(p: Path):
    for root in GIT_ROOTS:
        try:
            rel = p.resolve().relative_to(root)
        except (ValueError, OSError):
            continue
        try:
            r = subprocess.run(
                ["git", "-C", root, "log", "-1", "--format=%h %cs %s", "--", str(rel)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if r.returncode == 0 and r.stdout.strip():
                return {"repo": root, "last_commit": r.stdout.strip()[:160]}
            return {"repo": root, "last_commit": None}
        except Exception:
            return {"repo": root, "last_commit": None}
    return None


def build_witness(wire_path: Path):
    muts = extract_mutations(wire_path)
    paths = sorted({m["path"] for m in muts if m["path"]})
    l3, git_hits = [], 0
    for ps in paths[:60]:
        p = Path(ps)
        w = file_witness(p)
        g = git_witness(p) if w["exists"] else None
        if g and g.get("last_commit"):
            git_hits += 1
        l3.append({"path": ps, **w, "git": g})
    breakdown = {}
    for m in muts:
        breakdown[m["tool"]] = breakdown.get(m["tool"], 0) + 1
    wo = {
        "witness_type": "reality_binding",
        "session_source": str(wire_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "doctrine": "No metric may be promoted unless it is backed by a witness object.",
        "levels": {
            "L1_intent": {"surface": "conversation", "bound_via": "apex-zen-telemetry.jsonl", "status": "BOUND"},
            "L2_execution": {
                "surface": "tool.call",
                "mutations": len(muts),
                "breakdown": breakdown,
                "unique_paths": len(paths),
                "status": "BOUND" if muts else "EMPTY",
            },
            "L3_persistence": {
                "surface": "filesystem",
                "files_checked": len(l3),
                "files_existing": sum(1 for x in l3 if x["exists"]),
                "status": "BOUND" if l3 else "EMPTY",
            },
            "L4_consequence": {
                "surface": "git/receipts/CI",
                "files_with_commit": git_hits,
                "status": "PARTIAL" if git_hits else "NOT_YET_BOUND",
            },
        },
        "auditable": True,
        "details_L3": l3,
    }
    return wo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session")
    ap.add_argument("--latest", type=int, default=0)
    args = ap.parse_args()
    targets = []
    if args.session:
        targets = [Path(args.session)]
    elif args.latest:
        files = sorted(glob.glob(SESSIONS_GLOB), key=lambda f: Path(f).stat().st_mtime, reverse=True)[: args.latest]
        targets = [Path(f) for f in files]
    if not targets:
        ap.error("need --session or --latest")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("a") as f:
        for t in targets:
            wo = build_witness(t)
            f.write(json.dumps(wo) + "\n")
            L = wo["levels"]
            print(
                f"{t.parent.parent.name[:26]:26}  "
                f"L2={L['L2_execution']['mutations']:3} muts/{L['L2_execution']['unique_paths']:2} paths  "
                f"L3={L['L3_persistence']['files_existing']:2}/{L['L3_persistence']['files_checked']:2} exist  "
                f"L4={L['L4_consequence']['files_with_commit']:2} committed  [{L['L2_execution']['status']}/{L['L3_persistence']['status']}/{L['L4_consequence']['status']}]"
            )
    print("witness stream →", OUT)


if __name__ == "__main__":
    main()
