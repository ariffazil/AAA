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

import importlib
import importlib.util
import sys

# ─────────────────────────── DELEGATION ───────────────────────────
# The canonical CHRON tree is the `chron` PACKAGE at /root/chron, so these
# modules are package-internal by design. /root/AAA/scripts contains a sibling
# module `chron.py` (the ALPHA-ZEN clock) which shadows the package, so
# `import chron.chron_ariflow_bridge` fails with "'chron' is not a package" while this directory is
# first on sys.path. Register the package by file path instead of mutating
# sys.path — verified to resolve with the shadow present.

_PKG_NAME = "chron"
_PKG_DIR = "/root/chron"
_CANONICAL = "chron.chron_ariflow_bridge"

_existing = sys.modules.get(_PKG_NAME)
if _existing is None or not hasattr(_existing, "__path__"):
    _spec = importlib.util.spec_from_file_location(
        _PKG_NAME,
        _PKG_DIR + "/__init__.py",
        submodule_search_locations=[_PKG_DIR],
    )
    if _spec is None or _spec.loader is None:
        raise ImportError(
            "canonical CHRON package not found at " + _PKG_DIR +
            " — refusing to run a stale copy. See "
            "/root/AAA/reports/chron-tree-consolidation-2026-09-21.md"
        )
    _pkg = importlib.util.module_from_spec(_spec)
    sys.modules[_PKG_NAME] = _pkg
    _spec.loader.exec_module(_pkg)

if __name__ == "__main__":
    import runpy

    runpy.run_module(_CANONICAL, run_name="__main__", alter_sys=True)
else:
    _mod = importlib.import_module(_CANONICAL)
    globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("__")})
