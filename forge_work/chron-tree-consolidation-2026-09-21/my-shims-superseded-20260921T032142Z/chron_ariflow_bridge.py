#!/usr/bin/env python3
"""DEPRECATED LOCATION — CHRON organ module. Canonical source: /root/chron/chron_ariflow_bridge.py

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
new=/root/chron/chron_ariflow_bridge.py): AAA-only lines = 0, chron-only = 101.
Every line here is present in the canonical module -> nothing is lost by
delegating, and the divergence cannot silently reappear.

Canonical record:      /root/chron/CANONICAL-TREE.md
Pre-change copy:       /root/AAA/scripts/.archived-20260921T032142Z-chron-canonical-dedup/chron_ariflow_bridge.py

SIBLINGS DELIBERATELY LEFT ALONE (unique, superseded logic — HOLD, see record):
  chron_cron_verify.py, chron_prediction.py, chron_verify.py

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import sys

# The canonical package lives at /root/chron and is imported as `chron`.
if "/root" not in sys.path:
    sys.path.insert(0, "/root")

_CANONICAL = "chron.chron_ariflow_bridge"

if __name__ == "__main__":
    import runpy

    runpy.run_module(_CANONICAL, run_name="__main__", alter_sys=True)
else:
    import importlib

    _mod = importlib.import_module(_CANONICAL)
    globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("__")})
