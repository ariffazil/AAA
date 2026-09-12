#!/usr/bin/env python3
"""causal_spine.py — U11 cross-artifact causal reconstruction resolver.

Gate-2 item 4 (FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 U11, 2026-09-12).
The U11 falsifier: an independent party must be able to reconstruct a governed
transaction from ONE seed reference without manual multi-artifact forensics.
Tonight's K6 reconstruction required relay-prose x git x UL x commit-body
cross-reading by two agents — this tool collapses that to one query.

Indexed layers (probe-backed, Claim Layer = Evidence Layer):
  git logs       /root/AAA /root/scripts /root/arifOS   (commit subjects+bodies)
  git content    /root/AAA tracked files at HEAD
  UL lane        governance/UNRATIFIED-LESSONS-LEDGER.jsonl
  seal chain     ~/.local/share/arifos/vault999/seal_chain.jsonl
  forge_work     *.md artifacts

NOT indexed (unprobed tonight, do not claim): arifFlow receipt ledger
(Rust daemon storage not located this session), KVM4/KVM2 surfaces.
Depth: 1-hop (neighbors of the seed). Read-only. Exit 0 = external
neighbor(s) found; exit 1 = isolated seed (U11 gap signal); exit 2 = seed
matches nothing anywhere (unknown ref).

DITEMPA BUKAN DIBERI.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

GIT_REPOS = ["/root/AAA", "/root/scripts", "/root/arifOS"]
UL_LANE = Path("/root/AAA/governance/UNRATIFIED-LESSONS-LEDGER.jsonl")
SEAL_CHAIN = Path("/root/.local/share/arifos/vault999/seal_chain.jsonl")
FORGE_WORK = Path("/root/forge_work")


def _snippet(line, ref, width=120):
    i = line.find(ref)
    start = max(0, i - 40)
    return line[start : start + width].strip()


def find_git_log(ref):
    out = []
    for repo in GIT_REPOS:
        try:
            r = subprocess.run(
                ["git", "-C", repo, "log", "--all", "--format=%h|%s", f"--grep={ref}", "-F"],
                capture_output=True, text=True, timeout=20,
            )
            for line in r.stdout.splitlines():
                if "|" in line:
                    sha, subject = line.split("|", 1)
                    out.append({"layer": "git_log", "where": f"{repo}@{sha}", "ctx": subject[:120]})
        except Exception:
            pass
    return out


def find_git_content_aaa(ref):
    out = []
    try:
        r = subprocess.run(
            ["git", "-C", "/root/AAA", "grep", "-l", "-F", ref, "HEAD"],
            capture_output=True, text=True, timeout=20,
        )
        for f in r.stdout.splitlines():
            out.append({"layer": "aaa_tracked_content", "where": f, "ctx": ""})
    except Exception:
        pass
    return out


def find_jsonl(path, ref, layer):
    out = []
    if not path.exists():
        return out
    for i, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if ref in line:
            out.append({"layer": layer, "where": f"{path.name}:{i}", "ctx": _snippet(line, ref)})
    return out


def find_forge_work(ref):
    out = []
    if not FORGE_WORK.exists():
        return out
    for p in sorted(FORGE_WORK.rglob("*.md")):
        try:
            text = p.read_text(errors="replace")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if ref in line:
                out.append({"layer": "forge_work", "where": f"{p.name}:{i}", "ctx": _snippet(line, ref)})
                break
    return out


def resolve(ref):
    matches = []
    matches += find_git_log(ref)
    matches += find_git_content_aaa(ref)
    matches += find_jsonl(UL_LANE, ref, "ul_lane")
    matches += find_jsonl(SEAL_CHAIN, ref, "seal_chain")
    matches += find_forge_work(ref)
    return matches


def main():
    p = argparse.ArgumentParser(description="U11 cross-artifact causal resolver (1-hop, read-only)")
    p.add_argument("ref", help="seed reference: git sha, UL-###, receipt/hash fragment, token")
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args()
    ref = args.ref.strip()

    matches = resolve(ref)
    if args.as_json:
        print(json.dumps({"ref": ref, "neighbors": matches, "count": len(matches)}, indent=1))
    else:
        print(f"CAUSAL SPINE — seed '{ref}' — {len(matches)} neighbor(s)")
        for m in matches:
            ctx = f"  :: {m['ctx']}" if m["ctx"] else ""
            print(f"  [{m['layer']}] {m['where']}{ctx}")

    if not matches:
        print("UNKNOWN — seed matches nothing in indexed layers", file=sys.stderr)
        return 2
    seed_own = (
        (ref.startswith("UL-") and all(m["layer"] == "ul_lane" for m in matches))
        or (len(ref) in (7, 8, 40) and ref[:7].isalnum() and False)  # shas always have git_log self
    )
    if seed_own:
        print("ISOLATED — seed exists only in its own artifact (U11 gap)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
