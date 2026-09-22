#!/usr/bin/env python3
"""DEPRECATED LOCATION — CHRON organ module. Canonical source: /root/chron/chron_learn.py

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
new=/root/chron/chron_learn.py): AAA-only lines = 5, chron-only = 29, and all 5
AAA-only lines are prose, not logic. The only content unique to this copy was:

    [line] the OLD extract_lessons() docstring (2 sentences)
    [line] a blank line
    [line] the comment "# Create learn episode"

The canonical module adds a fingerprint dedup (the L4/L5 loop-closure repair) and
skips lessons already held. No symbol, branch or constant exists here that is
absent canonically -> strict subset. Full AAA-only line dump:
/root/chron/CANONICAL-TREE.md

Canonical record:      /root/chron/CANONICAL-TREE.md
Pre-change copy:       /root/AAA/scripts/.archived-20260921T032142Z-chron-canonical-dedup/chron_learn.py

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import sys

if "/root" not in sys.path:
    sys.path.insert(0, "/root")

_CANONICAL = "chron.chron_learn"

if __name__ == "__main__":
    import runpy

    runpy.run_module(_CANONICAL, run_name="__main__", alter_sys=True)
else:
    import importlib

    _mod = importlib.import_module(_CANONICAL)
    globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("__")})
