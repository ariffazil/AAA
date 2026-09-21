#!/usr/bin/env python3
"""DEPRECATED LOCATION — CHRON organ module. Canonical source: /root/chron/chron_prediction.py

WHY THIS FILE EXISTS IN THIS SHAPE
----------------------------------
/root/AAA/scripts was the DOCUMENTED CHRON path (a cron card named it as the
organ's evidence path). It is NOT the executing path. The systemd units that run
CHRON execute from /root/chron (ExecStart lines in
/etc/systemd/system/chron-*.service), and PYTHONPATH=/root makes the `chron`
package resolve to /root/chron.

The copy that lived here was a frozen snapshot of the same tree at AAA commit
78a23416 (2026-09-18 14:18), 9787 B — sha256 c1598db5528e — and was never
updated. The canonical module is 41947 B (sha256 593eaccdfcb7) and is under
active development by its owner; it grew again during this consolidation session.
Every prediction-lifecycle operation the store depends on exists in the canonical
module: load_verifications, get_verified, verify_prediction, compute_calibration,
save_calibration, recalibrate_confidence, get_active, generate_from_chron_events,
_canonical_verdict, decided_ids. The snapshot here is a strict earlier generation.

MEASURED (this session): `import chron_prediction` from this directory failed
before any change was made —
  ModuleNotFoundError: No module named 'chron.chron_prediction'; 'chron' is not a package
because the sibling clock module /root/AAA/scripts/chron.py shadows the /root/chron
package as `chron` on this directory's sys.path. Delegating below repairs that
path; it does not regress a working one.

Pre-change copy:   /root/AAA/scripts/.archived-20260921T032142Z-chron-canonical-dedup/chron_prediction.py
Also preserved at: /root/AAA/forge_work/chron-tree-consolidation-2026-09-21/

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
# `import chron.chron_prediction` fails with "'chron' is not a package" while this directory is
# first on sys.path. Register the package by file path instead of mutating
# sys.path — verified to resolve with the shadow present.

_PKG_NAME = "chron"
_PKG_DIR = "/root/chron"
_CANONICAL = "chron.chron_prediction"

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
