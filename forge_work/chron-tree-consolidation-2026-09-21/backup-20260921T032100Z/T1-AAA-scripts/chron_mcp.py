#!/usr/bin/env python3
"""DEPRECATED LOCATION — CHRON organ module. Canonical source: /root/chron/chron_mcp.py

WHY THIS FILE EXISTS IN THIS SHAPE
----------------------------------
/root/AAA/scripts was the DOCUMENTED CHRON path (a cron card named it as the
organ's evidence path). It is NOT the executing path. The systemd units that run
CHRON execute from /root/chron (ExecStart lines in
/etc/systemd/system/chron-*.service), and PYTHONPATH=/root makes the `chron`
package resolve to /root/chron — measured: chron.__file__ == /root/chron/__init__.py.

This copy was a frozen snapshot of the same tree at commit 78a23416 (2026-09-18
14:18) and was never updated; /root/chron carries every later repair.
MEASURED PROOF of strict-subset status (difflib.unified_diff, old=this file,
new=/root/chron/chron_mcp.py): AAA-only lines = 5, chron-only = 5. The only
content unique to this copy was one superseded expression inside the
chron_store_stats() tool:

    [5 lines] verified = [
                  p
                  for p in preds
                  if p.get("status") in ("VERIFIED_CORRECT", "VERIFIED_INCORRECT")
              ]

The canonical module replaces it with a join against the verification log and a
canonical-verdict normaliser (`_canonical_verdict`, `_DECISIVE`). After the
2026-09-18 immutability repair, birth records keep status="ACTIVE" forever, so the
AAA-side expression returns an EMPTY list — it is not merely older, it is wrong on
the current data model. No symbol, branch or constant is lost by delegating.
Full AAA-only line dump: /root/chron/CANONICAL-TREE.md

Canonical record:      /root/chron/CANONICAL-TREE.md
Pre-change copy:       /root/AAA/scripts/.archived-20260921T032142Z-chron-canonical-dedup/chron_mcp.py

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import sys

if "/root" not in sys.path:
    sys.path.insert(0, "/root")

_CANONICAL = "chron.chron_mcp"

if __name__ == "__main__":
    import runpy

    runpy.run_module(_CANONICAL, run_name="__main__", alter_sys=True)
else:
    import importlib

    _mod = importlib.import_module(_CANONICAL)
    globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("__")})
