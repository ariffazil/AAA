#!/usr/bin/env python3
"""skills-catalog-drift.py — compare a remote node's skill catalog against AAA canonical.

WHY THIS EXISTS
  KVM8 governs /root/AAA/skills with a census, a registry, mesh sync and a curator. KVM4
  carries 241 SKILL.md in a REAL directory with no registry, no census, no index and a
  curator that patches live. Nothing on either node knows the other's catalog exists, so
  the same skill NAME can teach two different procedures and neither side gets a signal.
  Verified 2026-10-23: `arif-sites-content-ops` was 102,722B on KVM4 and a 2,363B pointer
  stub on KVM8; `maiamakcikgpt-article-forging` 97,076B vs 7,487B. An agent reading the
  stale copy learns a deploy rule KVM8 retired two days earlier. That is a doctrine fork,
  and no sensor was watching for it.

CONTRACT
  * READ-ONLY on both sides. This script never writes to the peer and never writes a
    registry. It reads SKILL.md bodies over the transport and classifies.
  * Identity is the declared `name:` (brand prefixes normalised), never the folder.
  * Body identity is the sha256 of the whole file. Frontmatter carries `description`, and
    the description IS the routing trigger — a copy with a different description routes
    differently, so it is DIVERGED, not MIRROR.

CLASSES
  MIRROR        same name, same body digest           — healthy duplication
  DIVERGED      same name, different body             — doctrine fork, needs a decision
  LOCAL_ONLY    on the peer, no such name locally     — peer-authored capability
  MISSING       local name absent on the peer         — peer is behind
  BROKEN        on the peer: no `name`, or a shell    — fails any loader

USAGE
  skills-catalog-drift.py --node kvm4
  skills-catalog-drift.py --node kvm4 --root /root/.hermes/skills --json
  skills-catalog-drift.py --local /root/AAA/skills --node kvm4 --write /tmp/ledger.md

EXIT
  0  no DIVERGED and no BROKEN
  1  DIVERGED or BROKEN present
  2  the peer could not be read (UNKNOWN — never reported as clean)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

BRAND = re.compile(r"^(forge|claude|qwen|kimi|opencode|copilot|gemini|grok|aaa|agi|asi|agent|hermes)[-_]+")

REMOTE_READER = r"""
import os, re, hashlib, json, sys
root = sys.argv[1]
rows = []
for dp, dn, fn in os.walk(root, followlinks=True):
    dn[:] = [d for d in dn if not d.startswith('.') and d not in ('node_modules','venv','__pycache__','.git')]
    if 'SKILL.md' not in fn:
        continue
    p = os.path.join(dp, 'SKILL.md')
    try:
        b = open(p, 'rb').read()
    except Exception:
        continue
    head = b[:8000]
    nm = re.search(rb'^name:\s*(.+)$', head, re.M)
    ds = re.search(rb'^description:\s*(.+)$', head, re.M)
    rows.append({
        'rel': os.path.relpath(dp, root),
        'name': nm.group(1).decode('utf8','replace').strip().strip('"\'') if nm else None,
        'has_desc': bool(ds),
        'bytes': len(b),
        'sha': hashlib.sha256(b).hexdigest(),
    })
print(json.dumps(rows))
"""


def identity(name: str | None, rel: str) -> str | None:
    n = name or rel.split("/")[-1]
    if not n:
        return None
    k = BRAND.sub("", re.sub(r"[-_\s]+", "-", n.strip().lower())).strip("-")
    return k or None


def scan_local(root: Path) -> dict[str, dict]:
    out = {}
    for p in root.rglob("SKILL.md"):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        rel = str(p.parent.relative_to(root))
        try:
            b = p.read_bytes()
        except OSError:
            continue
        head = b[:8000]
        nm = re.search(rb"^name:\s*(.+)$", head, re.M)
        k = identity(nm.group(1).decode("utf8", "replace").strip().strip("\"'") if nm else None, rel)
        if not k:
            continue
        cand = {"rel": rel, "bytes": len(b), "sha": hashlib.sha256(b).hexdigest()}
        # keep the largest body when a name has several homes locally
        if k not in out or cand["bytes"] > out[k]["bytes"]:
            out[k] = cand
    return out


def scan_remote(node: str, root: str, user: str = "root", timeout: int = 120):
    cmd = ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes", f"{user}@{node}",
           "/usr/bin/python3 - " + root]
    try:
        r = subprocess.run(cmd, input=REMOTE_READER, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"ssh timeout after {timeout}s"
    if r.returncode != 0:
        return None, f"ssh rc={r.returncode}: {(r.stderr or '').strip()[:200]}"
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError as e:
        return None, f"peer returned non-JSON ({e}): {r.stdout[:120]!r}"


def classify(local: dict[str, dict], remote_rows: list[dict]):
    remote: dict[str, dict] = {}
    broken = []
    for row in remote_rows:
        k = identity(row.get("name"), row["rel"])
        if not k or not row.get("name") or row["bytes"] < 200:
            broken.append(row)
            continue
        if k not in remote or row["bytes"] > remote[k]["bytes"]:
            remote[k] = row
    mirror, diverged = [], []
    for k, r in remote.items():
        if k in local:
            (mirror if local[k]["sha"] == r["sha"] else diverged).append((k, local[k], r))
    local_only = sorted(k for k in local if k not in remote)
    peer_only = sorted(k for k in remote if k not in local)
    return {"mirror": mirror, "diverged": diverged, "missing_on_peer": local_only,
            "peer_only": peer_only, "broken": broken, "remote_index": remote}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--node", required=True)
    ap.add_argument("--user", default="root")
    ap.add_argument("--root", default="/root/.hermes/skills", help="skill root ON THE PEER")
    ap.add_argument("--local", default="/root/AAA/skills")
    ap.add_argument("--write", default=None, help="write a markdown ledger here")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    local = scan_local(Path(a.local))
    rows, err = scan_remote(a.node, a.root, a.user)
    if err:
        print(f"skills-catalog-drift: UNKNOWN — peer unreadable ({err})", file=sys.stderr)
        return 2

    c = classify(local, rows)
    verdict = "FORK" if (c["diverged"] or c["broken"]) else "CONSISTENT"

    if a.json:
        print(json.dumps({
            "node": a.node, "peer_root": a.root, "local_root": a.local,
            "verdict": verdict,
            "peer_total": len(rows), "local_total": len(local),
            "mirror": len(c["mirror"]), "diverged": len(c["diverged"]),
            "peer_only": len(c["peer_only"]), "missing_on_peer": len(c["missing_on_peer"]),
            "broken": len(c["broken"]),
            "diverged_sample": [{"name": k, "local_bytes": l["bytes"], "peer_bytes": r["bytes"],
                                 "local_path": l["rel"], "peer_path": r["rel"]}
                                for k, l, r in c["diverged"][:40]],
            "broken_sample": [{"rel": b["rel"], "bytes": b["bytes"], "name": b.get("name")}
                              for b in c["broken"][:20]],
            "peer_only_sample": c["peer_only"][:40],
        }, indent=2))
    else:
        print(f"skills-catalog-drift  node={a.node}  peer_root={a.root}")
        print(f"  peer SKILL.md      {len(rows)}   local identities {len(local)}")
        print(f"  MIRROR             {len(c['mirror'])}  (same body digest — healthy)")
        print(f"  DIVERGED           {len(c['diverged'])}  (same name, different body — doctrine fork)")
        print(f"  PEER_ONLY          {len(c['peer_only'])}  (peer-authored, no local name)")
        print(f"  MISSING_ON_PEER    {len(c['missing_on_peer'])}")
        print(f"  BROKEN             {len(c['broken'])}  (no name / shell)")
        if c["diverged"]:
            print("\n  largest forks:")
            for k, l, r in sorted(c["diverged"], key=lambda x: -abs(x[1]["bytes"] - x[2]["bytes"]))[:10]:
                print(f"    {k:42s} peer={r['bytes']:>7d}  local={l['bytes']:>7d}")
        if c["broken"]:
            print("\n  broken on peer:")
            for b in c["broken"][:10]:
                print(f"    {b['rel']}  ({b['bytes']}B, name={b.get('name')})")
        print(f"\n  VERDICT            {verdict}")

    if a.write:
        L = [f"# Skill catalog drift — {a.node} vs {a.local}\n",
             f"> generated {__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(timespec='seconds')}\n",
             f"> read-only; peer root `{a.root}`, {len(rows)} SKILL.md\n",
             f"> VERDICT **{verdict}** — {len(c['diverged'])} diverged, {len(c['broken'])} broken, "
             f"{len(c['mirror'])} mirror, {len(c['peer_only'])} peer-only\n\n## Diverged\n\n",
             "| skill | peer bytes | local bytes | peer path |\n|---|---|---|---|\n"]
        for k, l, r in sorted(c["diverged"], key=lambda x: -abs(x[1]["bytes"] - x[2]["bytes"])):
            L.append(f"| `{k}` | {r['bytes']} | {l['bytes']} | `{r['rel']}` |\n")
        L.append("\n## Broken on peer\n\n| path | bytes | name |\n|---|---|---|\n")
        for b in c["broken"]:
            L.append(f"| `{b['rel']}` | {b['bytes']} | {b.get('name')} |\n")
        Path(a.write).write_text("".join(L))
        print(f"\n  ledger written: {a.write}")

    return 0 if verdict == "CONSISTENT" else 1


if __name__ == "__main__":
    sys.exit(main())
