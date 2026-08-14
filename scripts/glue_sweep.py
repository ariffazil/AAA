#!/usr/bin/env python3
"""
glue_sweep.py — Script-bytes registry (XZ glue-surface defence)
================================================================
EUREKA 2: eyeballs follow importance, not the dependency graph.
The kernel is audited; the 500 boring glue scripts are trusted by
inheritance. This module makes every executable byte in the glue
surface a KNOWN hash — unknown-hash-at-exec is drift, judge decides.

Modes:
  build   — hash all executable bytes -> registry JSONL
  verify  — compare live tree vs registry -> KNOWN / DRIFTED / UNKNOWN
            exit 0 = clean, exit 2 = drift/unknown (HOLD signal for gates)

Stdlib only. Registry path via env GLUE_REGISTRY (Banda Haram).
Default registry: /root/.arifos/registries/glue-bytes.jsonl
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_ROOTS = [
    "/root/AAA/scripts",
    "/root/AAA/federation/protocols",
    "/root/HERMES/scripts",
]
DEFAULT_REGISTRY = "/root/.arifos/registries/glue-bytes.jsonl"
EXTS = {".py", ".sh", ".js", ".ts", ".cjs", ".mjs"}
EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git", ".venv", "archive", "bak-archive", "backups"}


def roots():
    env = os.environ.get("GLUE_ROOTS")
    return env.split(":") if env else DEFAULT_ROOTS


def registry_path():
    return os.environ.get("GLUE_REGISTRY", DEFAULT_REGISTRY)


def iter_files(rs):
    for root in rs:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fn in sorted(filenames):
                if os.path.splitext(fn)[1] in EXTS:
                    yield os.path.join(dirpath, fn)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_build(a):
    rs = roots()
    entries, skipped = [], 0
    for p in iter_files(rs):
        try:
            digest = sha256_file(p)
        except OSError:
            skipped += 1
            continue
        st = os.stat(p)
        entries.append({
            "path": p, "sha256": digest, "bytes": st.st_size,
            "mtime": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
        })
    os.makedirs(os.path.dirname(registry_path()), exist_ok=True)
    with open(registry_path(), "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
    total_bytes = sum(e["bytes"] for e in entries)
    print(f"registry built: {len(entries)} files, {total_bytes:,} bytes, "
          f"{skipped} unreadable — {registry_path()}")
    return 0


def cmd_verify(a):
    if not os.path.exists(registry_path()):
        print(f"error: no registry at {registry_path()} — run build first", file=sys.stderr)
        return 2
    known = {}
    with open(registry_path()) as f:
        for line in f:
            e = json.loads(line)
            known[e["path"]] = e["sha256"]

    live = {}
    for p in iter_files(roots()):
        try:
            live[p] = sha256_file(p)
        except OSError:
            pass

    drifted = [p for p in live if p in known and live[p] != known[p]]
    unknown = [p for p in live if p not in known]
    vanished = [p for p in known if p not in live]

    print(f"glue surface: {len(live)} live files vs {len(known)} registered")
    print(f"  KNOWN    : {len(live) - len(drifted) - len(unknown)}")
    print(f"  DRIFTED  : {len(drifted)}")
    print(f"  UNKNOWN  : {len(unknown)}  <- new bytes, never audited")
    print(f"  VANISHED : {len(vanished)}")
    for p in drifted[:20]:
        print(f"  drift: {p}")
    for p in unknown[:20]:
        print(f"  unknown: {p}")
    for p in vanished[:20]:
        print(f"  vanished: {p}")

    if a.json:
        print(json.dumps({"known": len(live) - len(drifted) - len(unknown),
                          "drifted": drifted, "unknown": unknown,
                          "vanished": vanished}, indent=2))
    # HOLD signal: any drifted or unknown byte is judge material, not auto-trust
    return 2 if (drifted or unknown) else 0


def main():
    ap = argparse.ArgumentParser(description="Glue-surface byte registry")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="hash all glue bytes into registry")
    v = sub.add_parser("verify", help="verify live tree against registry")
    v.add_argument("--json", action="store_true")
    a = ap.parse_args()
    return cmd_build(a) if a.cmd == "build" else cmd_verify(a)


if __name__ == "__main__":
    sys.exit(main())
