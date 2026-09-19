#!/usr/bin/env python3
"""
enforcement-coverage-monitor.py — ATTENTION-MODE enforcement-coverage ratchet.

WHY THIS EXISTS (2026-09-19 KITARAN audit)
------------------------------------------
Eight organ probes found 8 of 8 organs have at least one mutation path that
bypasses the gate. Each organ published its own reading under
/var/lib/arifos/asabiyyah/*.json with:

    evidence.ungated      -> the Kerkoporta list (named ungated paths)
    evidence.gated_paths  -> protected paths that DO pass a gate
    evidence.total_paths  -> every mutation path enumerated

That list was a SNAPSHOT. A snapshot cannot tell you whether the surface is
widening or closing. Doctrine (/root/AAA/instructions/authority-envelope.md)
requires COMPLETE MEDIATION:

    "If 99% of paths go through the gate but `bash \"echo x > file\"` bypasses
     it, there is no security property — only ethics suggestion."

Coverage is prior to prevention. A gate can block 100% of what it sees and
still leave the surface open. So the honest instrument is not "how many
attempts did we block" but "did the set of ungated paths change, and in which
direction".

WHAT THIS DOES
--------------
Reads the eight readings, flattens them into a REGISTER (one row per
(organ, ungated_path) plus per-organ gated/total/coverage), diffs the register
against the previous snapshot, and classifies every delta:

    NEW_UNGATED  a postern opened (or reopened)   -> HIGH
    CLOSED       a postern shut                   -> credit, ratcheted forever
    UNCHANGED    no movement

Then it writes the new snapshot and appends findings to the metrics log.

THE RATCHET
-----------
State may tighten but never silently loosen:

  * A CLOSED path is never forgotten. It moves to `closed` with `credited:
    true` and stays there. If it reappears it is reported as NEW_UNGATED with
    `reopened: true`, not as a neutral new row.
  * Per organ, `ratchet.min_enc_seen` (worst coverage ever witnessed) and
    `ratchet.max_ungated_seen` persist across runs, so a bad day cannot be
    averaged away by a good week.
  * `ratchet_hash` is a sha256 over the change-defining content only
    (organs, counts, path keys) — no timestamps. Two runs over unchanged
    readings produce the same hash, which is what makes idempotency checkable
    rather than asserted.

ATTENTION MODE — IT MUST NEVER BLOCK ANYTHING
---------------------------------------------
This is an OBSERVER. It does not enforce, deny, restart, mutate, signal, or
gate a live service. It:

  * is READ-ONLY against every organ repo, every reading, every live service;
  * writes only its own two state files under /var/lib/arifos/;
  * ALWAYS exits 0 in attention mode, even when it finds 30 new posterns —
    a monitor that fails closed on the day it first sees reality gets disabled
    within a week, and a disabled monitor has zero coverage.

Escalation is the reader's deliberate act, not this script's reflex.
`--strict-exit` exists so the escalation path can be tested; it is wired to no
cron, no hook, and no organ. Do not wire it.

MALFORMED INPUT IS NOT ZERO COVERAGE
------------------------------------
A reading that cannot be parsed is reported as malformed and its organ's
previous state is CARRIED FORWARD unclassified. A missing reading must never
be read as "those posterns closed" — that would let a broken probe earn a
credit it did not deserve.

USAGE
------
  enforcement-coverage-monitor.py                                  # attention run
  enforcement-coverage-monitor.py --json                           # machine-readable
  enforcement-coverage-monitor.py --dry-run                        # compute, write nothing
  enforcement-coverage-monitor.py --reset-baseline                 # re-bootstrap (explicit only)
  enforcement-coverage-monitor.py --strict-exit                    # exit 1 on NEW_UNGATED (UNWIRED)

Standard library only. Exit codes: 0 attention-mode OK, 1 only with
--strict-exit, 2 usage error, 3 refused unsafe write path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

REGISTER_VERSION = 1
MODE = "ATTENTION"

READINGS_DIR = Path("/var/lib/arifos/asabiyyah")
REGISTER_PATH = Path("/var/lib/arifos/enforcement-coverage-register.json")
FINDINGS_PATH = Path("/var/lib/arifos/metrics/enforcement-coverage-findings.jsonl")
STATE_ROOT = Path("/var/lib/arifos")

# Schema enum — /root/AAA/schemas/asabiyyah-reading.schema.json
ORGANS = ("arifOS", "AAA", "A-FORGE", "arifFlow", "WELL", "WEALTH", "GEOX", "HERMES")

SRC_STEM = 40  # chars used for advisory reword/reopen hints
LABEL_LEN = 80  # chars used for human-readable labels

# Exit code convention
EXIT_OK = 0
EXIT_STRICT = 1
EXIT_USAGE = 2
EXIT_UNSAFE_WRITE = 3


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z"


def _canon(text: str) -> str:
    """Canonicalise a path string for stable identity across runs.

    Whitespace is collapsed (readings wrap long sentences across lines) but
    punctuation and wording are preserved — two paths that differ in wording
    are two different paths and must not be silently merged.
    """
    return " ".join(str(text).split())


def _label(text: str) -> str:
    return text if len(text) <= LABEL_LEN else text[: LABEL_LEN - 1] + "\u2026"


def _stem(text: str) -> str:
    return _canon(text)[:SRC_STEM].lower()


def _row_key(organ: str, path_canon: str) -> str:
    return f"{organ}|{path_canon}"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except Exception:
            return None
    return None


def _write_allowed(path: Path) -> bool:
    """Guard: writes go to the state root, or to a system temp dir (tests).

    This script may not be repurposed into writing into an organ repo.
    """
    try:
        resolved = Path(path).expanduser().resolve()
    except Exception:
        return False
    for allowed in (STATE_ROOT, Path(tempfile.gettempdir())):
        try:
            resolved.relative_to(allowed.resolve())
            return True
        except Exception:
            continue
    return False


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def _append_jsonl(path: Path, records: list[dict[str, Any]]) -> int:
    """Append-only, one line per record, O_APPEND for atomic small writes."""
    if not records:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    blob = "".join(
        json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in records
    )
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, blob.encode("utf-8"))
    finally:
        os.close(fd)
    return len(records)


# --------------------------------------------------------------------------
# read + flatten the eight readings
# --------------------------------------------------------------------------
def read_readings(readings_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return (organs_by_name, malformed_list). Never raises on bad input."""
    organs: dict[str, Any] = {}
    malformed: list[dict[str, Any]] = []

    try:
        files = sorted(readings_dir.glob("*.json"))
    except Exception as exc:
        return {}, [{"file": str(readings_dir), "reason": f"unreadable_dir: {exc}"}]

    for f in files:
        fname = f.name
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
            digest = _sha256_file(f)
        except Exception as exc:
            malformed.append({"file": fname, "reason": f"unreadable: {exc}"})
            continue
        try:
            doc = json.loads(raw)
        except Exception as exc:
            malformed.append({"file": fname, "reason": f"bad_json: {exc}"})
            continue
        if not isinstance(doc, dict):
            malformed.append({"file": fname, "reason": "not_an_object"})
            continue

        organ = doc.get("organ")
        if not isinstance(organ, str) or not organ:
            malformed.append({"file": fname, "reason": "missing_organ"})
            continue
        if organ not in ORGANS:
            malformed.append({"file": fname, "reason": f"unknown_organ: {organ}"})
            continue

        ev = doc.get("evidence")
        if not isinstance(ev, dict):
            malformed.append({"file": fname, "reason": "missing_evidence_object"})
            continue

        gated = _as_int(ev.get("gated_paths"))
        total = _as_int(ev.get("total_paths"))

        raw_ungated = ev.get("ungated")
        if raw_ungated is None:
            ungated_paths: list[str] = []
            ungated_note = "ungated_field_absent"
        elif isinstance(raw_ungated, list):
            ungated_paths = [_canon(x) for x in raw_ungated if isinstance(x, str) and _canon(x)]
            dropped = len(raw_ungated) - len(ungated_paths)
            ungated_note = f"dropped_{dropped}_non_string" if dropped else ""
        else:
            ungated_paths = []
            ungated_note = f"ungated_not_a_list: {type(raw_ungated).__name__}"
            malformed.append({"file": fname, "reason": ungated_note})

        enc_metric = (doc.get("metrics") or {}).get("enc") if isinstance(doc.get("metrics"), dict) else None
        reading_enc = enc_metric.get("value") if isinstance(enc_metric, dict) else None
        if not isinstance(reading_enc, (int, float)):
            reading_enc = None

        # Re-derive coverage from raw counts. total_paths == 0 is
        # NOT_APPLICABLE per schema — never silently a perfect 1.0.
        if isinstance(gated, int) and isinstance(total, int) and total > 0:
            # Not rounded: a derived ratio is exact and rounding it only invites
            # spurious drift against a re-derivation elsewhere. Display rounds.
            enc = min(max(gated / total, 0.0), 1.0)
            enc_source = "derived"
        else:
            enc = None
            enc_source = "NOT_APPLICABLE" if total == 0 else "UNKNOWN"

        enc_mismatch = None
        if enc is not None and reading_enc is not None and abs(enc - float(reading_enc)) > 0.01:
            enc_mismatch = {"derived": enc, "reading": float(reading_enc)}

        record = {
            "organ": organ,
            "file": fname,
            "reading_sha256": digest,
            "observed_at": doc.get("observed_at"),
            "host": doc.get("host"),
            "gated_paths": gated,
            "total_paths": total,
            "enc": enc,
            "enc_source": enc_source,
            "reading_enc": float(reading_enc) if reading_enc is not None else None,
            "enc_mismatch": enc_mismatch,
            "ungated": ungated_paths,
            "ungated_note": ungated_note,
            "ungated_declared": len(ungated_paths),
        }
        if organ in organs:
            # Duplicate reading for one organ: keep the one with a later
            # observed_at when parseable, else the lexically later filename.
            prev = organs[organ]
            if str(record.get("observed_at") or "") >= str(prev.get("observed_at") or ""):
                record["superseded_file"] = prev["file"]
                organs[organ] = record
            else:
                malformed.append(
                    {"file": fname, "reason": f"duplicate_organ_reading_ignored (kept {prev['file']})"}
                )
        else:
            organs[organ] = record

    return organs, malformed


# --------------------------------------------------------------------------
# register build + diff
# --------------------------------------------------------------------------
def _ratchet_hash(organs: dict[str, Any], open_keys: list[str]) -> str:
    """Deterministic hash over change-defining content only (no timestamps)."""
    parts: list[str] = []
    for organ in sorted(organs):
        o = organs[organ]
        parts.append(f"E|{organ}|{o.get('gated_paths')}|{o.get('total_paths')}|{o.get('enc')}")
    for key in sorted(open_keys):
        parts.append(f"P|{key}")
    return "sha256:" + _sha256_text("\n".join(parts))


def _load_register(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.exists():
        return None, "absent"
    try:
        doc = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return None, f"unreadable: {exc}"
    if not isinstance(doc, dict):
        return None, "not_an_object"
    if _as_int(doc.get("register_version")) != REGISTER_VERSION:
        return None, f"version_mismatch: {doc.get('register_version')!r}"
    return doc, "ok"


def build_report(
    readings_dir: Path,
    register_path: Path,
    findings_path: Path,
    *,
    reset_baseline: bool = False,
) -> dict[str, Any]:
    """Pure computation. Returns the report dict; performs no writes."""
    now = _now_iso()
    now_epoch = time.time()

    organs, malformed = read_readings(readings_dir)

    prev, prev_reason = _load_register(register_path)
    if reset_baseline:
        prev, prev_reason = None, "reset_baseline_requested"
    bootstrap = prev is None

    prev_open: dict[str, Any] = (prev or {}).get("paths") or {}
    prev_closed: dict[str, Any] = (prev or {}).get("closed") or {}
    prev_organs: dict[str, Any] = (prev or {}).get("organs") or {}
    run_no = int((prev or {}).get("run_count") or 0) + 1

    # --- flatten current state -------------------------------------------
    cur_open: dict[str, Any] = {}
    organ_rows: dict[str, Any] = {}
    for organ in sorted(organs):
        rec = organs[organ]
        organ_rows[organ] = {
            "gated_paths": rec.get("gated_paths"),
            "total_paths": rec.get("total_paths"),
            "enc": rec.get("enc"),
            "enc_source": rec.get("enc_source"),
            "reading_enc": rec.get("reading_enc"),
            "enc_mismatch": rec.get("enc_mismatch"),
            "observed_at": rec.get("observed_at"),
            "host": rec.get("host"),
            "reading_file": rec.get("file"),
            "reading_sha256": rec.get("reading_sha256"),
            "ungated_declared": rec.get("ungated_declared"),
            "ungated_note": rec.get("ungated_note"),
            "stale_carried_forward": False,
        }
        for path_text in rec.get("ungated", []):
            cur_open[_row_key(organ, path_text)] = {
                "organ": organ,
                "path": path_text,
                "label": _label(path_text),
                "stem": _stem(path_text),
            }

    # --- organs with no readable reading this run: carry forward ----------
    stale_organs: list[str] = []
    for organ, prev_o in prev_organs.items():
        if organ in organ_rows:
            continue
        stale_organs.append(organ)
        organ_rows[organ] = dict(prev_o)
        organ_rows[organ]["stale_carried_forward"] = True
    for organ in stale_organs:
        prefix = f"{organ}|"
        for key, prev_row in prev_open.items():
            if key.startswith(prefix):
                cur_open[key] = prev_row

    stale_prefixes = tuple(f"{o}|" for o in stale_organs)

    # --- diff ------------------------------------------------------------
    new_rows: list[dict[str, Any]] = []
    closed_rows: list[dict[str, Any]] = []
    unchanged_count = 0
    for key in sorted(cur_open):
        row = cur_open[key]
        if key.startswith(stale_prefixes):
            unchanged_count += 1  # carried, never classified
            continue
        if bootstrap:
            continue
        if key in prev_closed:
            new_rows.append(
                {
                    "classification": "NEW_UNGATED",
                    "organ": row["organ"],
                    "path": row["path"],
                    "label": row["label"],
                    "reopened": True,
                    "reword_suspect": False,
                    "reword_of": None,
                    "severity": "HIGH",
                    "detail": "previously closed postern is open again",
                }
            )
        elif key not in prev_open:
            new_rows.append(
                {
                    "classification": "NEW_UNGATED",
                    "organ": row["organ"],
                    "path": row["path"],
                    "label": row["label"],
                    "reopened": False,
                    "reword_suspect": False,
                    "reword_of": None,
                    "severity": "HIGH",
                    "detail": "path absent from previous register",
                }
            )
        else:
            unchanged_count += 1

    if not bootstrap:
        for key in sorted(prev_open):
            if key.startswith(stale_prefixes):
                continue
            if key not in cur_open:
                row = prev_open[key]
                closed_rows.append(
                    {
                        "classification": "CLOSED",
                        "organ": row.get("organ"),
                        "path": row.get("path"),
                        "label": row.get("label") or _label(str(row.get("path") or "")),
                        "severity": "INFO",
                        "detail": "path present in previous register, absent now",
                    }
                )

    # Advisory: a brand-new path that looks like a paraphrase of a closed one.
    # The alarm still fires; this only tells the reader where to look first.
    known_stems: dict[str, str] = {}
    for src in (list(prev_closed.values()) + list(prev_open.values())):
        p = src.get("path")
        if isinstance(p, str) and p:
            known_stems.setdefault(_stem(p), p)
    for row in new_rows:
        if row["reopened"]:
            continue
        match = known_stems.get(_stem(row["path"]))
        if match and match != row["path"]:
            row["reword_suspect"] = True
            row["reword_of"] = _label(match)

    # --- ratchet + register assembly -------------------------------------
    ratchet_hash = _ratchet_hash(organs, list(cur_open))
    prev_hash = (prev or {}).get("ratchet_hash")

    for organ, row in organ_rows.items():
        prev_r = (prev_organs.get(organ) or {}).get("ratchet") or {}
        enc = row.get("enc")
        ungated_n = sum(1 for k in cur_open if k.startswith(f"{organ}|"))
        first_seen = prev_r.get("first_seen") or now
        ratchet = {
            "first_seen": first_seen,
            "min_enc_seen": prev_r.get("min_enc_seen"),
            "max_enc_seen": prev_r.get("max_enc_seen"),
            "max_ungated_seen": prev_r.get("max_ungated_seen") or 0,
            "changes": int(prev_r.get("changes") or 0),
            "last_change_at": prev_r.get("last_change_at"),
        }
        if isinstance(enc, (int, float)):
            lo = ratchet["min_enc_seen"]
            hi = ratchet["max_enc_seen"]
            ratchet["min_enc_seen"] = enc if lo is None else min(lo, enc)
            ratchet["max_enc_seen"] = enc if hi is None else max(hi, enc)
        ratchet["max_ungated_seen"] = max(int(ratchet["max_ungated_seen"] or 0), ungated_n)
        deltas_here = sum(1 for r in new_rows + closed_rows if r.get("organ") == organ)
        if deltas_here:
            ratchet["changes"] += deltas_here
            ratchet["last_change_at"] = now
        row["ratchet"] = ratchet
        row["ungated_open"] = ungated_n

    new_open: dict[str, Any] = {}
    new_closed: dict[str, Any] = dict(prev_closed)
    for key, row in cur_open.items():
        prev_row = prev_open.get(key) or {}
        new_open[key] = {
            "organ": row["organ"],
            "path": row["path"],
            "label": row["label"],
            "stem": row["stem"],
            "status": "OPEN",
            "first_seen": prev_row.get("first_seen") or now,
            "last_seen": now,
            "times_seen": int(prev_row.get("times_seen") or 0) + 1,
        }
    for row in closed_rows:
        key = _row_key(row["organ"], row["path"])
        prev_row = prev_open.get(key) or prev_closed.get(key) or {}
        new_closed[key] = {
            "organ": row["organ"],
            "path": row["path"],
            "label": row["label"],
            "stem": _stem(row["path"]),
            "status": "CLOSED",
            "first_seen": prev_row.get("first_seen") or now,
            "closed_at": now,
            "credited": True,
        }
    # Reopened paths leave the closed ledger (they are open again).
    for key in list(new_closed):
        if key in new_open:
            new_closed.pop(key)

    total_gated = sum(
        o.get("gated_paths") for o in organ_rows.values() if isinstance(o.get("gated_paths"), int)
    )
    total_paths = sum(
        o.get("total_paths") for o in organ_rows.values() if isinstance(o.get("total_paths"), int)
    )
    totals = {
        "organs": len(organ_rows),
        "ungated_paths": len([k for k in new_open if not k.startswith(stale_prefixes)]),
        "ungated_paths_carried": len([k for k in new_open if k.startswith(stale_prefixes)]),
        "gated_paths": total_gated,
        "total_paths": total_paths,
        "coverage": (total_gated / total_paths) if total_paths else None,
        "closed_ever": len(new_closed),
    }

    register = {
        "register_version": REGISTER_VERSION,
        "mode": MODE,
        "generated_at": now,
        "run_count": run_no,
        "prev_ratchet_hash": prev_hash,
        "ratchet_hash": ratchet_hash,
        "ratchet_changed": bool(prev_hash) and prev_hash != ratchet_hash,
        "readings_dir": str(readings_dir),
        "organs": organ_rows,
        "paths": new_open,
        "closed": new_closed,
        "totals": totals,
        "stale_organs": stale_organs,
    }

    # --- findings ---------------------------------------------------------
    findings: list[dict[str, Any]] = []
    for row in new_rows:
        findings.append(
            {
                "ts": now,
                "epoch": now_epoch,
                "kind": "DELTA",
                "class": "NEW_UNGATED",
                "severity": row["severity"],
                "organ": row["organ"],
                "path": row["path"],
                "reopened": row["reopened"],
                "reword_suspect": row["reword_suspect"],
                "reword_of": row["reword_of"],
                "ratchet_hash": ratchet_hash,
                "run": run_no,
            }
        )
    for row in closed_rows:
        findings.append(
            {
                "ts": now,
                "epoch": now_epoch,
                "kind": "DELTA",
                "class": "CLOSED",
                "severity": "INFO",
                "organ": row["organ"],
                "path": row["path"],
                "credited": True,
                "ratchet_hash": ratchet_hash,
                "run": run_no,
            }
        )

    if bootstrap:
        findings.append(
            {
                "ts": now,
                "epoch": now_epoch,
                "kind": "BASELINE",
                "class": "BASELINE_ESTABLISHED",
                "severity": "INFO",
                "reason": prev_reason,
                "baseline_organs": len(organ_rows),
                "baseline_ungated": totals["ungated_paths"],
                "baseline_closed": len(new_closed),
                "new_ungated": 0,
                "note": (
                    "first run: current ungated paths are the baseline, not alarms. "
                    "A baseline cannot distinguish a new postern from an old one."
                ),
                "ratchet_hash": ratchet_hash,
                "run": run_no,
            }
        )

    findings.append(
        {
            "ts": now,
            "epoch": now_epoch,
            "kind": "RUN",
            "class": "NO_CHANGE" if not (new_rows or closed_rows) else "CHANGED",
            "severity": "INFO",
            "organs": totals["organs"],
            "ungated_paths": totals["ungated_paths"],
            "coverage": totals["coverage"],
            "new_ungated": len(new_rows),
            "closed": len(closed_rows),
            "malformed_readings": len(malformed),
            "stale_organs": stale_organs,
            "ratchet_hash": ratchet_hash,
            "run": run_no,
        }
    )

    return {
        "mode": MODE,
        "generated_at": now,
        "readings_dir": str(readings_dir),
        "register_path": str(register_path),
        "findings_path": str(findings_path),
        "bootstrap": bootstrap,
        "bootstrap_reason": prev_reason if bootstrap else None,
        "run_count": run_no,
        "organs": organ_rows,
        "totals": totals,
        "new_ungated": new_rows,
        "closed": closed_rows,
        "new_ungated_count": len(new_rows),
        "closed_count": len(closed_rows),
        "unchanged_count": unchanged_count,
        "malformed_readings": malformed,
        "stale_organs": stale_organs,
        "ratchet_hash": ratchet_hash,
        "prev_ratchet_hash": prev_hash,
        "ratchet_changed": register["ratchet_changed"],
        "register": register,
        "findings": findings,
    }


# --------------------------------------------------------------------------
# summary printing
# --------------------------------------------------------------------------
def print_summary(rep: dict[str, Any]) -> None:
    t = rep["totals"]
    print(f"enforcement-coverage-monitor  [{rep['mode']}]  {rep['generated_at']}  run #{rep['run_count']}")
    print(f"readings: {rep['readings_dir']}   register: {rep['register_path']}")
    print()
    print(f"{'organ':10s} {'gated':>6s} {'total':>6s} {'coverage':>9s} {'ungated':>8s} {'worst':>8s}  state")
    print("-" * 74)
    for organ in sorted(rep["organs"]):
        o = rep["organs"][organ]
        enc = o.get("enc")
        enc_s = f"{enc:.4f}" if isinstance(enc, (int, float)) else str(o.get("enc_source"))
        worst = (o.get("ratchet") or {}).get("min_enc_seen")
        worst_s = f"{worst:.4f}" if isinstance(worst, (int, float)) else "-"
        state = "STALE_CARRIED_FORWARD" if o.get("stale_carried_forward") else (o.get("enc_source") or "")
        if o.get("enc_mismatch"):
            state += " ENC_MISMATCH"
        print(
            f"{organ:10s} {str(o.get('gated_paths')):>6s} {str(o.get('total_paths')):>6s} "
            f"{enc_s:>9s} {str(o.get('ungated_open')):>8s} {worst_s:>8s}  {state}"
        )
    print("-" * 74)
    cov = t["coverage"]
    cov_s = f"{cov:.4f}" if isinstance(cov, (int, float)) else "NOT_APPLICABLE"
    print(
        f"{'TOTAL':10s} {t['gated_paths']:>6d} {t['total_paths']:>6d} {cov_s:>9s} "
        f"{t['ungated_paths']:>8d}"
    )
    print(
        f"posterns closed (all time, ratcheted): {t['closed_ever']}"
        f"   carried-forward rows: {t['ungated_paths_carried']}"
    )
    print()

    if rep["bootstrap"]:
        print(f"BASELINE ESTABLISHED ({rep['bootstrap_reason']}) — no deltas computed on a first run.")
        print(f"  {t['organs']} organs, {t['ungated_paths']} ungated paths recorded as OPEN.")
        print("  These are the starting line, not alarms. Tomorrow's run can tell which are new.")
    else:
        print(f"NEW POSTERNS OPENED : {rep['new_ungated_count']}")
        for row in rep["new_ungated"]:
            extra = " [REOPENED]" if row["reopened"] else ""
            if row["reword_suspect"]:
                extra += f" [reword? of {row['reword_of']}]"
            print(f"  + [{row['organ']}] {row['label']}{extra}")
        print(f"POSTERNS CLOSED (credit): {rep['closed_count']}")
        for row in rep["closed"]:
            print(f"  - [{row['organ']}] {row['label']}")
        print(f"UNCHANGED          : {rep['unchanged_count']}")

    if rep["stale_organs"]:
        print()
        print(f"STALE (no readable reading this run, state carried forward): {', '.join(rep['stale_organs'])}")
        print("  A missing reading is NOT 'closed'. Those rows were excluded from the diff.")
    if rep["malformed_readings"]:
        print()
        print(f"MALFORMED READINGS ({len(rep['malformed_readings'])}) — reported, never fatal:")
        for m in rep["malformed_readings"]:
            print(f"  ! {m.get('file')}: {m.get('reason')}")

    print()
    if not rep["bootstrap"]:
        verb = "CHANGED" if rep["ratchet_changed"] else "unchanged"
        print(f"ratchet {verb}: {rep['ratchet_hash'][:23]}…")
    else:
        print(f"ratchet baseline: {rep['ratchet_hash'][:23]}…")
    print(f"ATTENTION MODE — nothing blocked, nothing enforced. {len(rep['findings'])} ledger line(s) appended.")
    print("Escalation is the reader's decision. --strict-exit is wired to nothing.")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="enforcement-coverage-monitor",
        description="ATTENTION-MODE enforcement-coverage ratchet (observe-only, never blocks).",
    )
    ap.add_argument("--readings-dir", default=str(READINGS_DIR))
    ap.add_argument("--register", default=str(REGISTER_PATH))
    ap.add_argument("--findings", default=str(FINDINGS_PATH))
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--quiet", action="store_true", help="suppress the human summary")
    ap.add_argument("--dry-run", action="store_true", help="compute only; write nothing at all")
    ap.add_argument(
        "--reset-baseline",
        action="store_true",
        help="discard the previous register and re-bootstrap (explicit; never automatic)",
    )
    ap.add_argument(
        "--strict-exit",
        action="store_true",
        help="exit 1 if a NEW_UNGATED path is found. UNWIRED: no cron/hook calls this.",
    )
    try:
        a = ap.parse_args(argv)
    except SystemExit as exc:  # argparse already printed
        return EXIT_USAGE if exc.code not in (0, None) else EXIT_OK

    register_path = Path(a.register)
    findings_path = Path(a.findings)

    if not a.dry_run:
        for p in (register_path, findings_path):
            if not _write_allowed(p):
                print(
                    f"[monitor] refused: write path {p} is outside /var/lib/arifos and not a temp dir.",
                    file=sys.stderr,
                )
                return EXIT_UNSAFE_WRITE

    try:
        rep = build_report(
            Path(a.readings_dir), register_path, findings_path, reset_baseline=a.reset_baseline
        )
    except Exception as exc:  # attention mode never hard-fails the caller
        print(f"[monitor] internal error (reported, not raised): {exc}", file=sys.stderr)
        return EXIT_OK

    written = 0
    if not a.dry_run:
        try:
            _atomic_write_json(register_path, rep["register"])
            written = _append_jsonl(findings_path, rep["findings"])
        except Exception as exc:
            print(f"[monitor] state write failed (reported, not raised): {exc}", file=sys.stderr)

    rep["findings_written"] = written
    rep["register_written"] = bool(written or not a.dry_run)
    rep["dry_run"] = bool(a.dry_run)
    rep.pop("register", None)  # keep JSON output readable; register is on disk

    if a.json:
        print(json.dumps(rep, indent=2, ensure_ascii=False, default=str))
    elif not a.quiet:
        print_summary(rep)

    if a.strict_exit and rep["new_ungated_count"]:
        return EXIT_STRICT
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
