#!/usr/bin/env python3
"""DEPRECATED LOCATION — CHRON organ module. Canonical source: /root/chron/chron_cron_verify.py

WHY THIS FILE EXISTS IN THIS SHAPE
----------------------------------
/root/AAA/scripts was the DOCUMENTED CHRON path (a cron card named it as the
organ's evidence path). It is NOT the executing path:

  chron-prediction-verifier.service  ExecStart=/usr/bin/python3 /root/chron/chron_cron_verify.py

The copy that lived here was a frozen snapshot of the same tree at AAA commit
78a23416 (2026-09-18 14:18), 13927 B, and was never updated. It was not merely
stale — the canonical module's own docstring (lines 4-21) names this exact
snapshot as the SECOND, divergent verification implementation REMOVED by the
F13-authorised repair of 2026-09-18, with three measured defects:

  * V1  it rewrote `predictions.jsonl`, overwriting birth records, so the belief
        snapshot that produced a prediction did not survive verification;
  * V2  it wrote a third row schema into verification_log.jsonl, making the join
        ambiguous;
  * V3  it decided outcomes by asserting that a passed calendar date meant the
        claim held, minting CORRECT verdicts with no evidence at all.

MEASURED (this session): the snapshot here was byte-identical — sha256
54b0b0e05c6b — to the pre-repair rollback
/root/chron/.backup-chron-repair-20260918T152417Z/chron_cron_verify.py, i.e. it is
provably the pre-repair file and not a later fork. The canonical module (3011 B,
sha256 cd1f7c69892d) gathers no evidence, decides no verdict and writes no
prediction record; it delegates to the single verification implementation
`chron.chron_verify`.

MEASURED (this session): running the snapshot from this directory failed before
any change was made —
  ModuleNotFoundError: No module named 'chron.chron_prediction'; 'chron' is not a package
because the sibling clock module /root/AAA/scripts/chron.py shadows the /root/chron
package as `chron` on this directory's sys.path. Delegating below repairs that
path; it does not regress a working one.

Pre-change copy:   /root/AAA/scripts/.archived-20260921T032142Z-chron-canonical-dedup/chron_cron_verify.py
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
# `import chron.chron_cron_verify` fails with "'chron' is not a package" while this directory is
# first on sys.path. Register the package by file path instead of mutating
# sys.path — verified to resolve with the shadow present.

_PKG_NAME = "chron"
_PKG_DIR = "/root/chron"
_CANONICAL = "chron.chron_cron_verify"

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
