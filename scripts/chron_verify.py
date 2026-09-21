#!/usr/bin/env python3
"""DEPRECATED LOCATION — CHRON organ module. Canonical source: /root/chron/chron_verify.py

WHY THIS FILE EXISTS IN THIS SHAPE
----------------------------------
/root/AAA/scripts was the DOCUMENTED CHRON path (a cron card named it as the
organ's evidence path). It is NOT the executing path. Every systemd unit that runs
CHRON verification executes from /root/chron:

  chron-prediction-verifier.service  ExecStart=/usr/bin/python3 /root/chron/chron_cron_verify.py
  chron-loop-closer.service          ExecStart=/usr/bin/python3 /root/chron/chron_loop_close.py

The copy that lived here was a frozen snapshot of the same tree at AAA commit
78a23416 (2026-09-18 14:18), 8194 B — sha256 37ea925c3056 — and was never updated.
The canonical module is the single verification implementation named by the
2026-09-18 repair ("There is now exactly ONE verification implementation:
`chron.chron_verify`"); it was 19755 B (sha256 607a1d1badfb) at the start of this
session and has since grown further under its owner's development. It carries
_evidence_for, _search, _title_tokens, _is_already_verified,
_append_verification_record, _emit_ariflow_verify — none of which exist in the
snapshot here.

MEASURED (this session): `import chron_verify` from this directory failed before
any change was made —
  ModuleNotFoundError: No module named 'chron.chron_prediction'; 'chron' is not a package
(reproduced directly: /root/AAA/scripts/__main__.py verify -> exit 1, traceback at
chron_verify.py line 21) because the sibling clock module /root/AAA/scripts/chron.py
shadows the /root/chron package as `chron` on this directory's sys.path.
Delegating below repairs that path; it does not regress a working one.

Pre-change copy:   /root/AAA/scripts/.archived-20260921T032142Z-chron-canonical-dedup/chron_verify.py
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
# `import chron.chron_verify` fails with "'chron' is not a package" while this directory is
# first on sys.path. Register the package by file path instead of mutating
# sys.path — verified to resolve with the shadow present.

_PKG_NAME = "chron"
_PKG_DIR = "/root/chron"
_CANONICAL = "chron.chron_verify"

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
