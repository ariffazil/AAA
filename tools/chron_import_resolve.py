#!/usr/bin/env python3
"""CHRON live-entrypoint import-resolution probe — REAL imports, no side effects.

For each live entrypoint it replicates the sys.path the live unit gives the
process, imports the entrypoint AS A MODULE (so module-level imports really
execute but no `if __name__ == "__main__"` block does), then prints the
`__file__` of every `chron*` module that landed in sys.modules.

That answers the only question that matters: which PHYSICAL FILE does this live
process actually import?

Run:  python3 /root/AAA/tools/chron_import_resolve.py
"""
from __future__ import annotations

import json
import subprocess
import sys

PROBE = r'''
import importlib, json, os, sys, traceback
entry_dir, modname, pythonpath = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, entry_dir)
if pythonpath:
    for p in pythonpath.split(":"):
        if p and p not in sys.path:
            sys.path.append(p)
os.chdir(sys.argv[4])
out = {"modules": [], "error": None}
try:
    importlib.import_module(modname)
except Exception as e:
    out["error"] = f"{type(e).__name__}: {e}"
for name, mod in sorted(sys.modules.items()):
    if name == "chron" or name.startswith("chron.") or name.startswith("chron_"):
        f = getattr(mod, "__file__", None)
        if f:
            out["modules"].append({"module": name, "file": f})
print(json.dumps(out))
'''

# label, entrypoint, module name, cwd, PYTHONPATH (as the unit sets it)
ENTRYPOINTS = [
    ("chron-loop-closer.service",
     "/root/chron/chron_loop_close.py", "chron_loop_close", "/", "/root"),
    ("chron-loop-closer.service ExecStartPost",
     "/root/chron/chron_briefing.py", "chron_briefing", "/", "/root"),
    ("chron-prediction-verifier.service",
     "/root/chron/chron_cron_verify.py", "chron_cron_verify", "/", "/root"),
    ("chron-task0-reconciliation.service",
     "/root/scripts/chron_personal/task0_reconciliation.py",
     "task0_reconciliation", "/", None),
    ("chron-mcp.service",
     "/root/chron/mcp_server.py", "mcp_server", "/root/chron", "/root"),
    ("crontab 30 15 * * *  /root/chron/verify_due.py",
     "/root/chron/verify_due.py", "verify_due", "/", None),
    ("ALPHA-ZEN card -> import chron (clock)",
     "/root/AAA/scripts/alpha_zen_chron.py", "alpha_zen_chron", "/", None),
]


def main() -> int:
    report = []
    for label, ep, mod, cwd, pypath in ENTRYPOINTS:
        entry_dir = ep.rsplit("/", 1)[0]
        r = subprocess.run(
            [sys.executable, "-c", PROBE, entry_dir, mod, pypath or "", cwd],
            capture_output=True, text=True, cwd="/", timeout=120,
        )
        try:
            data = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            data = {"modules": [], "error": f"probe failed: {r.stderr[-400:]}"}
        report.append({"entrypoint": label, "entrypoint_file": ep,
                       "cwd": cwd, "PYTHONPATH": pypath, **data})

    for e in report:
        print(f"\n=== {e['entrypoint']} ===")
        print(f"    entrypoint : {e['entrypoint_file']}")
        print(f"    cwd        : {e['cwd']}   PYTHONPATH={e['PYTHONPATH']}")
        if e.get("error"):
            print(f"    !! module import raised: {e['error']}")
        if not e["modules"]:
            print("    imports    : (no chron* module imported)")
        for m in e["modules"]:
            print(f"    {m['module']:28s} -> {m['file']}")

    with open("/root/AAA/forge_work/chron-tree-consolidation-2026-09-21"
              "/IMPORT-RESOLUTION.json", "w") as fh:
        json.dump(report, fh, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
