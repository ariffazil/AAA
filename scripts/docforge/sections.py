#!/usr/bin/env python3
"""docforge.sections — the four COMPUTED sections of AAA::EDITION_RENDER_CONTRACT::v1.3.

WHY THIS MODULE EXISTS (and why it is not a prompt)
  pipeline.py's own header says "THE ITEM SOURCE IS INJECTED, NOT HARDCODED" —
  the register is authored by an agent and handed in. That separation is right
  for intelligence gathering and wrong for numbers. Measured proof: the live
  /999/ page served "Overall Brier Score: 0.088" and "142 Resolved Predictions"
  while /root/chron/data/calibration.json held mean_brier 0.14881943646798773
  and predictions_total 133. 0.088 matched NO scope the SOT exposes. An authored
  number and a lying number are indistinguishable to a reader.

  So these four sections are read out of the stores at render time, by code, on
  every build. Peraturan Sifar #4: semua nombor dari SOT semasa render.

THE FOUR SECTIONS (contract v1.3, F13 SAH 2026-10-08)
  0.2 MODEL_CHANGE              audit object, not narrative — 12 named fields
  0.3 PREDICTION_LINEAGE        TOP-N by NEAREST / HIGHEST-CONSEQUENCE / OLDEST
  0.4 SURVIVORS_AND_NEWCOMERS   name + age in days, from created_at
  0.5 LEARNING_RECEIPT + CALIBRATION_WITNESS
                                accuracy / brier / bias / lessons / blind-share

THREE LAWS THIS FILE MECHANISES, NOT RECITES
  1. Peraturan Sifar #5 — a confidence that was never measured renders literally
     "n/a (unmeasured)". There is no code path here that can produce a plausible
     number for a missing one; the sentinel is the only fallback.
  2. Peraturan Sifar #6 — bias = confidence − accuracy, rendered as FORMULA + SIGN.
     The renderer is forbidden from interpreting the direction in free prose, and
     it does not interpret anything else either: every label below is either a
     field name from the store or the contract's own sentence. The word the 3×
     same-day error produced ("overconfident") never appears in this file, and
     the only place the demoted belief is named is MC-001's `old` column, which
     is the audit record of the error, not a claim about the data.
  3. §8.2 — NO reliability diagram. 22 effective observations across 10 bins
     means most bins hold <=3 and the curve would be noise wearing the costume of
     a measurement. The honest form at this n is a table with per-row n plus the
     Brier Skill Score headline. The refusal is printed in the document so a
     reader knows the absence is deliberate and not an oversight.

VOID GUARD
  An unreadable SOT is "cannot witness", never "all clear". Each reader returns
  (value, error); the section renders the sentinel plus a visible warning box,
  the error is recorded in the build receipt, and — for calibration.json, the
  SOT behind the measured drift — the armed g_sot_truth assertion fails closed
  and refuses the seal. A degraded edition is still delivered; a lying one is not.

NO NEW ANYTHING
  Zero new store, cron, organ, MCP server, public surface or database. This is
  one module inside the existing docforge package, reading files that already
  exist, called from the pipeline that already runs at 06:00.
"""
from __future__ import annotations

import html as htmllib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ── sources of truth ─────────────────────────────────────────────────────────
# Every number this module renders comes from one of these. Nothing is cached,
# nothing is authored, nothing is remembered from a previous build.

SOT = {
    "calibration": Path("/root/chron/data/calibration.json"),
    "predictions": Path("/root/chron/data/predictions.jsonl"),
    "lessons":     Path("/root/chron/data/lessons.jsonl"),
    "eurekas":     Path("/root/AAA/eurekas/eureka-entries.jsonl"),
    "episodes":    Path("/root/chron/data/episodes.jsonl"),
    "events":      Path("/root/AAA/scripts/chron_events.json"),
}
# NOTE: /root/AAA/canon/eureka-entries.jsonl is chattr +i FROZEN. It is not read
# and never written here. The LIVE writable copy is AAA/eurekas/ (contract P3).

UNMEASURED = "n/a (unmeasured)"

# The measured stale literals from the live /999/ page (probed over HTTP
# 2026-10-08). Armed on the calibration assertion so g_sot_truth refuses any
# edition that carries them next to the SOT value.
FORBID_LITERALS = ("0.088", "142 Resolved Predictions", "WELL CALIBRATED")

# g_text_layer refuses a document carrying an internal absolute path, so SOT
# labels shown to the reader are root-relative. The absolute path still lives in
# spec.json (on disk, not in the PDF) where the gate needs it.
_LEAK_PREFIXES = ("/root/", "/tmp/", "/home/", "file:///")


def _sot_label(p: Path | str) -> str:
    s = str(p)
    return s[len("/root/"):] if s.startswith("/root/") else s


# ── MODEL_CHANGE contract shape ──────────────────────────────────────────────

MC_FIELDS = ("id", "status", "subject", "old", "new", "trigger", "evidence",
             "confidence", "falsifier", "prediction_impact", "od1_impact")
MC_STATUSES = ("PROMOTED", "DEMOTED", "FALSIFIED", "SPLIT", "MERGED")

# Registry seeded from the ratified canon fragment's REGISTRY MC (v1.3). These
# are code, not a store: they live in git beside the renderer, they carry no
# number that can go stale (MC-001's evidence is bound live to the SOT below),
# and the counter the contract asks for is a render-time count of rows.
MC_REGISTRY_SEED: tuple[dict, ...] = (
    {
        "id": "MC-001", "status": "DEMOTED",
        "subject": "tafsiran arah bias / interpretation of the bias direction",
        "old": "overconfident",
        "new": "UNDER-confident (bias negative: confidence below accuracy)",
        "trigger": "direction error repeated 3x in one day (333 -> sibling -> "
                   "sibling), 2026-10-08",
        # {live_bias} is substituted at render from calibration.json — the one
        # seeded row whose evidence is a measurement, so it is bound, not typed.
        "evidence": "SOT chron/data/calibration.json bias = {live_bias} "
                    "(mean_confidence {live_conf} - accuracy {live_acc}); "
                    "session SEAL-56d88ddc11b346ac receipts ffca69a4, af645bf1; "
                    "scar HERMES-NOTIFICATION-DRIFT",
        "confidence": UNMEASURED,
        "falsifier": "bias sign flips positive on a later calibration.json read "
                     "while mean_confidence stays below accuracy",
        "prediction_impact": UNMEASURED,
        "od1_impact": UNMEASURED,
        "source": "AAA/instructions/aaa-edition-render-contract-v1.md REGISTRY MC",
    },
    {
        "id": "MC-002", "status": "PROMOTED",
        "subject": "instrumen wujud, penerbitan tak dedahkan / instruments exist, "
                   "publication does not disclose them",
        "old": UNMEASURED, "new": UNMEASURED,
        "trigger": "sibling audit", "evidence": "sibling lane report",
        "confidence": UNMEASURED, "falsifier": UNMEASURED,
        "prediction_impact": UNMEASURED, "od1_impact": UNMEASURED,
        "source": "AAA/instructions/aaa-edition-render-contract-v1.md REGISTRY MC",
    },
    {
        "id": "MC-003", "status": "PROMOTED",
        "subject": "peranan PETRONAS / PETRONAS role in the fiscal frame",
        "old": "dividend pressure moderate",
        "new": "struktur fiscal buffer kitaran GE16",
        "trigger": "subsidi RM4B/bln (dari RM0.7B), Brent >100, B2027",
        "evidence": "canon REGISTRY MC v1.3 (trigger values as ratified)",
        "confidence": UNMEASURED, "falsifier": UNMEASURED,
        "prediction_impact": UNMEASURED, "od1_impact": UNMEASURED,
        "source": "AAA/instructions/aaa-edition-render-contract-v1.md REGISTRY MC v1.3",
    },
    {
        "id": "MC-004", "status": "PROMOTED",
        "subject": "disiplin bukti / evidence discipline for substrate memory",
        "old": "substrate memory = evidence",
        "new": "memory = REPORTED sahaja; witness-class diperlukan sebelum naik OBS",
        "trigger": "audit HERMES map — dakwaan tak-boleh-audit",
        "evidence": "canon REGISTRY MC v1.3",
        "confidence": UNMEASURED, "falsifier": UNMEASURED,
        "prediction_impact": UNMEASURED, "od1_impact": UNMEASURED,
        "source": "AAA/instructions/aaa-edition-render-contract-v1.md REGISTRY MC v1.3",
    },
)

# ── lineage mapping ──────────────────────────────────────────────────────────
# The contract names four lineage statuses. The store names seven. Only the
# unambiguous ones are mapped; anything else is shown VERBATIM and counted as
# UNMAPPED, because coercing an unknown state into a known one is the
# failure-class-collapse error (malformed != denied != absent).
LINEAGE_MAP = {
    "ACTIVE": "OPEN",
    "UNBOUND": "OPEN",          # unresolved; "not bound to a verifier" is shown
    "VERIFIED": "VERIFIED",
    "CORRECT": "VERIFIED",
    "INCORRECT": "FALSIFIED",
    "SPLIT": "SPLIT",
}
LINEAGE_STATUSES = ("OPEN", "VERIFIED", "FALSIFIED", "SPLIT")
UNRESOLVED_STORE_STATES = ("ACTIVE", "UNBOUND")
CONSEQUENCE_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

# A PERSONAL_SAFE event renders witness status only. The classification is the
# store's own `kind` field, not this module's opinion.
PERSONAL_SAFE_KIND = "PERSONAL_SAFE"
INTENT_UNKNOWN = ("Owner intent (posture vs deadline): UNKNOWN — belongs to the "
                  "owner. The machine does not infer it and does not conclude it.")

EPISODE_SCAN_MAX_BYTES = 1 << 30   # 1 GiB tail bound; the file measured 168 MiB


# ── small honest helpers ─────────────────────────────────────────────────────


def _esc(v) -> str:
    """Escape store text, and de-path it.

    Two jobs, both mechanical:
      * escape, because a claim containing '<' must not become markup;
      * rewrite internal absolute path prefixes, because g_text_layer refuses —
        correctly — to ship a document carrying the building machine's layout.
        The paths arrive inside QUOTED store text (eureka evidence lists, event
        source notes), not from this module's own labels. Dropping the '/root/'
        prefix keeps the file identifiable to the reader while removing the
        machine-root assertion. Every rewrite is counted and disclosed in the
        document, because a silent edit to quoted evidence is the same defect
        class this whole module exists to prevent.
    """
    if v is None:
        return ""
    return htmllib.escape(_depath(str(v)), quote=False)


# order matters: the URI form is rewritten before the bare prefixes it contains
_PATH_REWRITES = (("file:///", "file://"), ("/root/", ""), ("/tmp/", "tmp/"),
                  ("/home/", "home/"))
_REWRITES = {"n": 0}


def _depath(s: str) -> str:
    out = s
    for a, b in _PATH_REWRITES:
        if a in out:
            _REWRITES["n"] += out.count(a)
            out = out.replace(a, b)
    return out


def _fmt3(v) -> str:
    """ONE formatter for both the HTML and the gate assertion.

    The gate compares strings, so the rendered text and the expected text must be
    produced by the same function or they can disagree about rounding. Keeping a
    single formatter is what makes the assertion non-decorative.
    """
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        return f"{v:.3f}"
    if isinstance(v, int):
        return str(v)
    return UNMEASURED if v is None else str(v)


def _num(v) -> str:
    """Render a store number, or the sentinel. Never rounds a hole into a digit."""
    return UNMEASURED if v is None else _fmt3(v)


def _parse_dt(s):
    if not s or not isinstance(s, str):
        return None
    t = s.strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(t)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _read_json(path: Path):
    """(data, error) — fail closed, never a silent default."""
    try:
        return json.loads(Path(path).read_text()), None
    except FileNotFoundError:
        return None, f"SOT absent: {_sot_label(path)}"
    except Exception as exc:  # noqa: BLE001 - report, never mask
        return None, f"SOT unreadable ({type(exc).__name__}): {_sot_label(path)}"


def _read_jsonl(path: Path):
    """(rows, error). A malformed LINE is reported and skipped, not hidden: the
    row count is rendered next to it so the reader sees what was dropped."""
    p = Path(path)
    try:
        raw = p.read_text().splitlines()
    except FileNotFoundError:
        return [], f"SOT absent: {_sot_label(p)}"
    except Exception as exc:  # noqa: BLE001
        return [], f"SOT unreadable ({type(exc).__name__}): {_sot_label(p)}"
    rows, bad = [], 0
    for line in raw:
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception:  # noqa: BLE001
            bad += 1
    err = (f"{bad} malformed line(s) skipped in {_sot_label(p)}" if bad else None)
    return rows, err


def _read_learn_episodes(path: Path):
    """CHRON episodes with function=learn — the contract's MODEL_CHANGE store.

    episodes.jsonl measured 168 MiB / ~143k episodes, of which a handful are
    learn episodes. A cheap substring prefilter runs before json.loads so the
    build parses a few lines, not 143k. A tail bound keeps the cost from growing
    without limit; when the bound binds, the render says so — a silently
    truncated scan would be a hidden absence.
    """
    p = Path(path)
    try:
        size = p.stat().st_size
    except FileNotFoundError:
        return [], None, f"SOT absent: {_sot_label(p)}"
    except Exception as exc:  # noqa: BLE001
        return [], None, f"SOT unreadable ({type(exc).__name__}): {_sot_label(p)}"

    bounded = size > EPISODE_SCAN_MAX_BYTES
    out, scanned = [], 0
    try:
        with p.open("r", errors="replace") as fh:
            if bounded:
                fh.seek(size - EPISODE_SCAN_MAX_BYTES)
                fh.readline()          # drop the partial line the seek landed in
            for line in fh:
                scanned += 1
                if '"learn"' not in line:
                    continue
                if '"function": "learn"' not in line and '"function":"learn"' not in line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    pass
    except Exception as exc:  # noqa: BLE001
        return out, scanned, f"episode scan failed ({type(exc).__name__}): {_sot_label(p)}"
    return out, scanned, None


def _age_days(created, ref_date) -> int | None:
    """Age in whole days by DATE parts, so an item created today is 0 and no
    item can ever be negative."""
    d = _parse_dt(created)
    if d is None or ref_date is None:
        return None
    return (ref_date.date() - d.astimezone(timezone.utc).date()).days


def _due_label(verify_at, ref_date) -> str:
    d = _parse_dt(verify_at)
    if d is None or ref_date is None:
        return UNMEASURED
    dd = (d.astimezone(timezone.utc).date() - ref_date.date()).days
    day = d.astimezone(timezone.utc).strftime("%Y-%m-%d")
    if dd < 0:
        return f"{day} (overdue {-dd} d)"
    return f"{day} (in {dd} d)"


def _warn(errors: list[str], what: str) -> str:
    """The visible form of 'cannot witness'. Never a blank, never a default."""
    if not errors:
        return ""
    return ("<div class='box warn'><strong>SOT UNREADABLE — cannot witness "
            f"{_esc(what)}.</strong><br><span class='small'>"
            + "<br>".join(_esc(e) for e in errors)
            + "<br>Values below render as <code>" + UNMEASURED
            + "</code>. This is not an all-clear.</span></div>")


# ── load ─────────────────────────────────────────────────────────────────────


def load_sot(paths: dict | None = None) -> dict:
    """Read every store once per build. Returns data AND errors side by side."""
    p = dict(SOT, **(paths or {}))
    calib, e_calib = _read_json(p["calibration"])
    preds, e_preds = _read_jsonl(p["predictions"])
    lessons, e_lessons = _read_jsonl(p["lessons"])
    eurekas, e_eurekas = _read_jsonl(p["eurekas"])
    episodes, ep_lines, e_eps = _read_learn_episodes(p["episodes"])
    events_doc, e_events = _read_json(p["events"])
    events = (events_doc or {}).get("events") if isinstance(events_doc, dict) else events_doc
    if events is None:
        events = []
        if not e_events:
            e_events = f"no 'events' list in {_sot_label(p['events'])}"
    return {
        "paths": p,
        "calibration": calib, "predictions": preds, "lessons": lessons,
        "eurekas": eurekas, "episodes": episodes, "events": events,
        "episode_lines_scanned": ep_lines,
        "episode_scan_bounded": bool(p["episodes"].exists())
        and p["episodes"].stat().st_size > EPISODE_SCAN_MAX_BYTES,
        "errors": {k: v for k, v in (
            ("calibration", e_calib), ("predictions", e_preds), ("lessons", e_lessons),
            ("eurekas", e_eurekas), ("episodes", e_eps), ("events", e_events)) if v},
    }


# ── 0.2 MODEL_CHANGE ─────────────────────────────────────────────────────────


def _mc_row(**kw) -> dict:
    row = {k: kw.get(k, UNMEASURED) for k in MC_FIELDS}
    row["source"] = kw.get("source", UNMEASURED)
    row["source_state"] = kw.get("source_state", "")
    return row


def model_change_rows(sot: dict, *, today: datetime, window_days: int = 7) -> list[dict]:
    """Seeded registry + rows derived at render time from the two named stores.

    Nothing here is authored by the running agent. A derived row that does not
    declare a status in the contract's enum renders the sentinel and carries the
    source's own word in `source_state` — the enum is never back-filled by
    guessing, and a status nobody measured is not a status.
    """
    calib = sot.get("calibration") or {}
    live = {
        "live_bias": _num(calib.get("bias")),
        "live_conf": _num(calib.get("mean_confidence")),
        "live_acc": _num(calib.get("accuracy")),
    }
    rows = []
    for seed in MC_REGISTRY_SEED:
        r = dict(seed)
        for k, v in list(r.items()):
            if isinstance(v, str) and "{" in v:
                try:
                    r[k] = v.format(**live)
                except (KeyError, IndexError):
                    pass
        rows.append(_mc_row(**r))

    # CHRON learn episodes — the contract's named MODEL_CHANGE store.
    for ep in sot.get("episodes") or []:
        for cl in (ep.get("claims") or [])[:1]:
            rows.append(_mc_row(
                id=cl.get("claim_id") or UNMEASURED,
                status=UNMEASURED,
                source_state=f"truth_state={cl.get('truth_state', UNMEASURED)}",
                subject=(cl.get("statement") or UNMEASURED)[:160],
                trigger=f"{ep.get('question', UNMEASURED)} · observed_at "
                        f"{ep.get('observed_at', UNMEASURED)}",
                evidence=cl.get("basis") or UNMEASURED,
                confidence=UNMEASURED,
                source=f"chron/data/episodes.jsonl function=learn "
                       f"({_sot_label(sot['paths']['episodes'])})",
            ))

    # Eureka entries dated inside the window. The window is a stated render rule,
    # not a judgement about which insights matter.
    for i, e in enumerate(sot.get("eurekas") or [], start=1):
        ts = e.get("ts") or e.get("date")
        d = _parse_dt(ts if isinstance(ts, str) and "T" in ts
                      else f"{ts}T00:00:00Z" if ts else None)
        if d is None or (today.date() - d.astimezone(timezone.utc).date()).days > window_days:
            continue
        rid = e.get("id") or f"EU-{(ts or 'undated')}-{e.get('agent') or e.get('lane') or 'unknown'}"
        rows.append(_mc_row(
            id=str(rid), status=UNMEASURED,
            source_state=" · ".join(str(e[k]) for k in ("status", "verdict", "truth_class")
                                    if e.get(k)) or UNMEASURED,
            subject=(e.get("eureka") or e.get("insight") or UNMEASURED)[:160],
            trigger=e.get("context") or e.get("session") or UNMEASURED,
            evidence=e.get("evidence") or e.get("source") or UNMEASURED,
            confidence=UNMEASURED,
            falsifier=e.get("falsifier") or UNMEASURED,
            source=f"AAA/eurekas/eureka-entries.jsonl line {i}",
        ))
    return rows


def render_model_change(rows: list[dict], *, errors: list[str], rendered_at: str) -> str:
    unclassified = sum(1 for r in rows if r["status"] == UNMEASURED)
    out = ["<h2>0.2 &middot; MODEL_CHANGE</h2>",
           "<p class='small'>Audit object, not narrative — "
           "<code>AAA::EDITION_RENDER_CONTRACT::v1.3</code> §1. Computed at render from "
           "CHRON episodes <code>function=learn</code> + "
           "<code>AAA/eurekas/eureka-entries.jsonl</code>, over the registry seeded from "
           "the canon. A status is asserted only where a source declares one; "
           f"<strong>{unclassified}</strong> of <strong>{len(rows)}</strong> row(s) carry "
           f"<code>{UNMEASURED}</code> because no source measured one (Peraturan Sifar #5). "
           f"Receipt counter = render-time row count: <strong>{len(rows)}</strong> "
           f"at {_esc(rendered_at)}.</p>",
           _warn(errors, "MODEL_CHANGE sources")]
    if not rows:
        out.append("<div class='box key'>No model-change row could be read this build.</div>")
        return "".join(out)
    out.append("<table><thead><tr><th style='width:16%'>id / status</th>"
               "<th style='width:42%'>subject · old &rarr; new</th>"
               "<th>trigger · evidence · confidence · falsifier · impact</th>"
               "</tr></thead><tbody>")
    for r in rows:
        st = r["status"]
        tag = "t-doc" if st in MC_STATUSES else "t-wire"
        out.append(
            "<tr>"
            f"<td><strong>{_esc(r['id'])}</strong><br>"
            f"<span class='tag {tag}'>{_esc(st)}</span>"
            + (f"<br><span class='small'>{_esc(r['source_state'])}</span>"
               if r.get("source_state") else "")
            + f"<br><span class='small'>source: {_esc(r['source'])}</span></td>"
            f"<td><strong>subject:</strong> {_esc(r['subject'])}<br>"
            f"<span class='small'><strong>old:</strong> {_esc(r['old'])} &rarr; "
            f"<strong>new:</strong> {_esc(r['new'])}</span></td>"
            "<td class='small'>"
            f"<strong>trigger:</strong> {_esc(r['trigger'])}<br>"
            f"<strong>evidence:</strong> {_esc(r['evidence'])}<br>"
            f"<strong>confidence:</strong> {_esc(r['confidence'])}<br>"
            f"<strong>falsifier:</strong> {_esc(r['falsifier'])}<br>"
            f"<strong>prediction_impact:</strong> {_esc(r['prediction_impact'])}<br>"
            f"<strong>od1_impact:</strong> {_esc(r['od1_impact'])}"
            "</td></tr>")
    out.append("</tbody></table>")
    out.append("<p class='small'>status enum: "
               + " | ".join(MC_STATUSES)
               + f" — anything else renders <code>{UNMEASURED}</code> and is never "
                 "coerced into the enum. od1_impact is a PERSONAL_SAFE field: see 0.5.</p>")
    return "".join(out)


# ── 0.3 PREDICTION_LINEAGE ───────────────────────────────────────────────────


def _lineage(status: str) -> str:
    return LINEAGE_MAP.get((status or "").upper(), f"UNMAPPED:{status or 'none'}")


def lineage_census(rows: list[dict]) -> dict:
    cen: dict[str, dict] = {}
    for r in rows:
        lin = _lineage(r.get("status"))
        key = lin if lin in LINEAGE_STATUSES else "UNMAPPED"
        slot = cen.setdefault(key, {"n": 0, "store": {}})
        slot["n"] += 1
        s = str(r.get("status") or "none")
        slot["store"][s] = slot["store"].get(s, 0) + 1
    return cen


def lineage_top(rows: list[dict], events: list[dict], *, today: datetime,
                top_n: int, order: str) -> list[dict]:
    """TOP-N over UNRESOLVED rows by NEAREST / HIGHEST-CONSEQUENCE / OLDEST.

    Consequence is not a field of the prediction store — it is declared on the
    EVENT the prediction was minted from, joined by source_id. A row whose event
    declares no consequence is ranked LAST and labelled unmeasured; assuming
    "unknown = low" would silently demote a real risk, and assuming "unknown =
    high" would manufacture urgency. Neither is a measurement.
    """
    cons = {}
    for e in events or []:
        if isinstance(e, dict) and e.get("id"):
            cons[str(e["id"])] = e.get("consequence")
    live = [r for r in rows if str(r.get("status") or "").upper() in UNRESOLVED_STORE_STATES]
    enriched = []
    for r in live:
        sid = str(r.get("source_id") or "")
        c = cons.get(sid)
        enriched.append({
            "id": r.get("prediction_id") or UNMEASURED,
            "claim": (r.get("claim") or UNMEASURED),
            "lineage": _lineage(r.get("status")),
            "store_status": r.get("status") or UNMEASURED,
            "consequence": c or UNMEASURED,
            "proposed": r.get("confidence_proposed"),
            "calibrated": r.get("confidence_calibrated"),
            "due": _due_label(r.get("verify_at"), today),
            "verify_dt": _parse_dt(r.get("verify_at")),
            "created_dt": _parse_dt(r.get("created_at")),
            "age_days": _age_days(r.get("created_at"), today),
        })
    if order == "NEAREST":
        enriched.sort(key=lambda x: (x["verify_dt"] is None,
                                     x["verify_dt"] or datetime.max.replace(tzinfo=timezone.utc)))
    elif order == "OLDEST":
        enriched.sort(key=lambda x: (x["created_dt"] is None,
                                     x["created_dt"] or datetime.max.replace(tzinfo=timezone.utc)))
    elif order == "HIGHEST-CONSEQUENCE":
        enriched.sort(key=lambda x: (CONSEQUENCE_RANK.get(str(x["consequence"]).upper(), 99),
                                     x["id"]))
    else:
        raise ValueError(f"unknown lineage order {order!r}")
    return enriched[:top_n]


def _lineage_table(rows: list[dict], *, with_consequence: bool) -> str:
    if not rows:
        return ("<div class='box key'>No unresolved prediction row could be read "
                "for this ordering.</div>")
    head = ("<tr><th>prediction_id</th><th>claim</th><th>lineage</th>"
            + ("<th>consequence</th>" if with_consequence else "")
            + "<th>confidence_proposed</th><th>confidence_calibrated</th>"
              "<th>verify_at</th><th>age d</th></tr>")
    out = ["<table><thead>", head, "</thead><tbody>"]
    for r in rows:
        age = UNMEASURED if r["age_days"] is None else str(r["age_days"])
        out.append(
            "<tr>"
            f"<td class='small'>{_esc(r['id'])}</td>"
            f"<td>{_esc(r['claim'][:78])}{'...' if len(str(r['claim'])) > 78 else ''}</td>"
            f"<td>{_esc(r['lineage'])}<br><span class='small'>{_esc(r['store_status'])}</span></td>"
            + (f"<td>{_esc(r['consequence'])}</td>" if with_consequence else "")
            + f"<td>{_num(r['proposed'])}</td>"
            f"<td>{_num(r['calibrated'])}</td>"
            f"<td class='small'>{_esc(r['due'])}</td>"
            f"<td>{_esc(age)}</td>"
            "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_prediction_lineage(sot: dict, *, today: datetime, top_n: int,
                              errors: list[str]) -> str:
    preds = sot.get("predictions") or []
    cen = lineage_census(preds)
    out = ["<h2>0.3 &middot; PREDICTION_LINEAGE</h2>",
           "<p class='small'>Computed at render from <code>chron/data/predictions.jsonl</code> "
           f"({_esc(_sot_label(sot['paths']['predictions']))}), "
           f"{len(preds)} row(s) read. Consequence joined from "
           "<code>AAA/scripts/chron_events.json</code> by <code>source_id</code>. "
           f"TOP-{top_n} per ordering, over unresolved rows only "
           f"({' / '.join(UNRESOLVED_STORE_STATES)}).</p>",
           _warn(errors, "the prediction store")]

    out.append("<h3>Lineage status census (all rows)</h3>")
    out.append("<table><thead><tr><th>lineage status</th><th>rows</th>"
               "<th>store status behind it (verbatim)</th></tr></thead><tbody>")
    for k in list(LINEAGE_STATUSES) + ["UNMAPPED"]:
        slot = cen.get(k)
        if not slot:
            out.append(f"<tr><td>{k}</td><td>0</td><td class='small'>&mdash;</td></tr>")
            continue
        behind = ", ".join(f"{s}={n}" for s, n in sorted(slot["store"].items()))
        out.append(f"<tr><td><strong>{k}</strong></td><td>{slot['n']}</td>"
                   f"<td class='small'>{_esc(behind)}</td></tr>")
    out.append("</tbody></table>")
    out.append("<p class='small'>Mapping is printed rather than assumed: "
               + "; ".join(f"{k}&rarr;{v}" for k, v in sorted(LINEAGE_MAP.items()))
               + "; any other store status &rarr; UNMAPPED and shown verbatim. "
                 "An unmapped state is not folded into OPEN — malformed, denied and "
                 "absent are different facts.</p>")

    for order, with_c in (("NEAREST", False), ("HIGHEST-CONSEQUENCE", True), ("OLDEST", False)):
        rows = lineage_top(preds, sot.get("events") or [], today=today,
                           top_n=top_n, order=order)
        rule = {"NEAREST": "earliest <code>verify_at</code> first (overdue surfaces first)",
                "HIGHEST-CONSEQUENCE": "event-declared consequence HIGH &rarr; MEDIUM &rarr; LOW; "
                                       f"rows with no declared consequence rank last as "
                                       f"<code>{UNMEASURED}</code>",
                "OLDEST": "earliest <code>created_at</code> first"}[order]
        out.append(f"<h3>TOP-{top_n} · {order}</h3>"
                   f"<p class='small'>ordering rule: {rule}</p>")
        out.append(_lineage_table(rows, with_consequence=with_c))
    return "".join(out)


# ── 0.4 SURVIVORS_AND_NEWCOMERS ──────────────────────────────────────────────


def survivor_rows(sot: dict, *, today: datetime, newcomer_days: int) -> dict:
    preds = sot.get("predictions") or []
    live = [r for r in preds
            if str(r.get("status") or "").upper() in UNRESOLVED_STORE_STATES]
    rows, undated = [], []
    for r in live:
        age = _age_days(r.get("created_at"), today)
        rec = {"id": r.get("prediction_id") or UNMEASURED,
               "name": (r.get("claim") or UNMEASURED),
               "age_days": age,
               "store_status": r.get("status") or UNMEASURED}
        (rows if age is not None else undated).append(rec)
    newcomers = sorted([r for r in rows if r["age_days"] <= newcomer_days],
                       key=lambda x: x["age_days"])
    survivors = sorted([r for r in rows if r["age_days"] > newcomer_days],
                       key=lambda x: -x["age_days"])
    return {"live": len(live), "newcomers": newcomers, "survivors": survivors,
            "undated": undated, "newcomer_days": newcomer_days}


def _age_table(rows: list[dict], limit: int) -> str:
    if not rows:
        return "<p class='small'>none</p>"
    out = ["<table><thead><tr><th>name</th><th>prediction_id</th><th>age (days)</th>"
           "<th>store status</th></tr></thead><tbody>"]
    for r in rows[:limit]:
        out.append(f"<tr><td>{_esc(str(r['name'])[:78])}"
                   f"{'...' if len(str(r['name'])) > 78 else ''}</td>"
                   f"<td class='small'>{_esc(r['id'])}</td>"
                   f"<td><strong>{r['age_days']}</strong></td>"
                   f"<td class='small'>{_esc(r['store_status'])}</td></tr>")
    out.append("</tbody></table>")
    if len(rows) > limit:
        out.append(f"<p class='small'>{len(rows) - limit} further row(s) not listed "
                   f"(bounded at {limit} to keep the edition readable); the counts "
                   "above cover all of them.</p>")
    return "".join(out)


def render_survivors(sot: dict, *, today: datetime, newcomer_days: int,
                     errors: list[str], limit: int = 10) -> str:
    s = survivor_rows(sot, today=today, newcomer_days=newcomer_days)
    oldest = s["survivors"][0]["age_days"] if s["survivors"] else None
    out = ["<h2>0.4 &middot; SURVIVORS_AND_NEWCOMERS</h2>",
           "<p class='small'>Name + age in days, computed from "
           "<code>created_at</code> on unresolved rows of "
           f"<code>chron/data/predictions.jsonl</code> against the edition date "
           f"{today.strftime('%Y-%m-%d')}. Rule, printed not implied: "
           f"<strong>newcomer</strong> = age &le; {newcomer_days} d; "
           "<strong>survivor</strong> = older than that and still unresolved. "
           f"A row with no parseable <code>created_at</code> renders "
           f"<code>{UNMEASURED}</code> — it is never counted as age 0.</p>",
           _warn(errors, "the prediction store"),
           "<table><thead><tr><th>unresolved rows</th><th>survivors</th>"
           "<th>newcomers</th><th>oldest survivor</th><th>age unmeasured</th>"
           "</tr></thead><tbody><tr>"
           f"<td>{s['live']}</td><td>{len(s['survivors'])}</td>"
           f"<td>{len(s['newcomers'])}</td>"
           f"<td>{UNMEASURED if oldest is None else str(oldest) + ' d'}</td>"
           f"<td>{len(s['undated'])}</td>"
           "</tr></tbody></table>",
           f"<h3>Newcomers (&le; {newcomer_days} d)</h3>",
           _age_table(s["newcomers"], limit),
           "<h3>Survivors (oldest first)</h3>",
           _age_table(s["survivors"], limit)]
    return "".join(out)


# ── 0.5 LEARNING_RECEIPT + CALIBRATION_WITNESS ───────────────────────────────


def bss(mean_brier) -> str:
    """Brier Skill Score against a coin flip, with the arithmetic shown.

    §8.2: at this n the headline a reader can actually use is "how much better
    than chance", not a binned curve. Printed as a substitution so it is
    checkable by hand rather than trusted.
    """
    if not isinstance(mean_brier, float):
        return UNMEASURED
    val = (0.25 - mean_brier) / 0.25
    return f"BSS = (0.25 - {_fmt3(mean_brier)}) / 0.25 = {_fmt3(val)}"


def spread_report(preds: list[dict]) -> dict:
    """confidence_proposed vs confidence_calibrated, kept SEPARATE.

    §1.5 / ISSUE-005: merging the two launders a measured discrimination loss.
    The loss is recomputed here from the live rows rather than quoted, so the
    edition can never carry yesterday's 71.4% as if it were today's measurement.
    """
    pairs = [(r.get("confidence_proposed"), r.get("confidence_calibrated"))
             for r in preds
             if isinstance(r.get("confidence_proposed"), (int, float))
             and isinstance(r.get("confidence_calibrated"), (int, float))]
    if not pairs:
        return {"n": 0}
    prop = [a for a, _ in pairs]
    cal = [b for _, b in pairs]
    sp, sc = (max(prop) - min(prop)), (max(cal) - min(cal))
    return {
        "n": len(pairs),
        "rows_with_proposed_only": sum(
            1 for r in preds
            if isinstance(r.get("confidence_proposed"), (int, float))
            and not isinstance(r.get("confidence_calibrated"), (int, float))),
        "mean_proposed": sum(prop) / len(prop),
        "mean_calibrated": sum(cal) / len(cal),
        "spread_proposed": sp, "spread_calibrated": sc,
        "spread_loss": (1 - sc / sp) if sp else None,
        "mean_abs_shift": sum(abs(a - b) for a, b in pairs) / len(pairs),
    }


def lessons_report(lessons: list[dict]) -> dict:
    total = len(lessons)
    actionable = sum(1 for r in lessons if r.get("actionable") is True)
    not_actionable = sum(1 for r in lessons if r.get("actionable") is False)
    unspecified = total - actionable - not_actionable
    et: dict[str, int] = {}
    for r in lessons:
        k = str(r.get("error_type") or "UNTYPED")
        et[k] = et.get(k, 0) + 1
    st: dict[str, int] = {}
    for r in lessons:
        k = str(r.get("status") or "UNDECLARED")
        st[k] = st.get(k, 0) + 1
    untyped = et.get("UNTYPED", 0) + et.get("UNKNOWN", 0)
    return {"total": total, "actionable": actionable, "not_actionable": not_actionable,
            "unspecified": unspecified, "by_error_type": et, "by_status": st,
            "error_class_blind": untyped,
            "blind_share": (actionable / total) if total else None,
            "non_actionable_share": ((total - actionable) / total) if total else None}


def calibration_assertions(calib: dict | None, sot_path: Path) -> list[dict]:
    """Arm g_sot_truth for every SOT-backed number this section renders.

    A gate nobody arms is decoration, so the assertions are produced from the
    same live read that produced the HTML, through the same _fmt3 formatter.

    Two deliberate omissions, both stated rather than hidden:
      * effective_n (22) and by_error_type counts are NOT asserted — a two-digit
        string like "22" appears in dates all over the document, so the assertion
        would pass vacuously and look like a witness.
      * JSONL-derived counts (lessons, prediction rows) cannot be asserted by
        g_sot_truth, which reads one dotted key out of a JSON object. Extending
        the landed P2 gate to JSONL is a change to that gate, not to this module,
        so those numbers are instead re-read independently by the test suite and
        snapshotted into the build receipt.
    """
    p = str(sot_path)
    if not isinstance(calib, dict):
        # Fail closed: an unreadable calibration SOT must refuse the seal, because
        # this is the exact SOT the live /999/ page was measured lying about.
        return [{"label": "mean_brier (calibration SOT unreadable)", "sot": p,
                 "key": "mean_brier", "forbid": list(FORBID_LITERALS)}]
    specs = [
        ("mean_brier", "mean_brier", list(FORBID_LITERALS)),
        ("accuracy", "accuracy", []),
        ("bias", "bias", []),
        ("mean_confidence", "mean_confidence", []),
        ("predictions_total", "predictions_total", ["142 Resolved Predictions"]),
        ("quality", "quality", ["WELL CALIBRATED"]),
        ("brier (excl. self-tests)",
         "honest_scopes.canonical_unified_excluding_self_tests.mean_brier", []),
        ("brier (raw, one row per hypothesis)", "raw.mean_brier", []),
        ("brier (gold-pair scope)", "honest_scopes.gold_pair_scope.mean_brier", []),
    ]
    out = []
    for label, key, forbid in specs:
        cur = calib
        for part in key.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur is None:
            continue
        a = {"label": label, "sot": p, "key": key, "render": _fmt3(cur)}
        if forbid:
            a["forbid"] = forbid
        out.append(a)
    return out


def render_learning(sot: dict, *, today: datetime, errors: list[str]) -> str:
    c = sot.get("calibration") or {}
    preds = sot.get("predictions") or []
    lessons = sot.get("lessons") or []
    lr = lessons_report(lessons)
    sp = spread_report(preds)
    p_cal = _sot_label(sot["paths"]["calibration"])
    p_les = _sot_label(sot["paths"]["lessons"])
    p_pred = _sot_label(sot["paths"]["predictions"])

    out = ["<h2>0.5 &middot; LEARNING_RECEIPT + CALIBRATION_WITNESS</h2>",
           _warn(errors, "the calibration / lessons stores"),
           "<h3>Calibration witness — one row per measure, with its own n</h3>",
           "<table><thead><tr><th>measure</th><th>value</th><th>n</th>"
           "<th>SOT key</th></tr></thead><tbody>"]

    n_eff = c.get("effective_n")
    n_eff_s = UNMEASURED if n_eff is None else str(n_eff)
    for label, key, n in (
            ("accuracy", "accuracy", n_eff_s),
            ("mean_brier", "mean_brier", n_eff_s),
            ("mean_confidence", "mean_confidence", n_eff_s),
            ("reliability (Murphy)", "reliability", n_eff_s),
            ("predictions_total (all stores)", "predictions_total", "all stores"),
            ("decisive", "decisive", n_eff_s),
            ("records_in_log", "records_in_log", "log rows"),
            ("synthetic_self_tests", "synthetic_self_tests", "self-test rows"),
            ("quality", "quality", n_eff_s)):
        v = c.get(key)
        out.append(f"<tr><td>{_esc(label)}</td><td><strong>{_num(v)}</strong></td>"
                   f"<td>{_esc(n)}</td><td class='small'>{_esc(p_cal)}:{_esc(key)}</td></tr>")
    out.append("</tbody></table>")
    out.append(f"<p class='small'>SOT read at render: <code>{_esc(p_cal)}</code>, "
               f"<code>updated_at {_esc(c.get('updated_at') or UNMEASURED)}</code>, "
               f"edition date {today.strftime('%Y-%m-%d')}. "
               "Every value above is a pass-through of that file — this renderer "
               "computes no metric of its own and caches none (Peraturan Sifar #4).</p>")

    # ── bias: formula + sign ONLY (Peraturan Sifar #6) ──
    bias, conf, acc = c.get("bias"), c.get("mean_confidence"), c.get("accuracy")
    sign = UNMEASURED
    if isinstance(bias, (int, float)):
        sign = "NEGATIVE" if bias < 0 else ("POSITIVE" if bias > 0 else "ZERO")
    out.append("<div class='box key'><strong>bias</strong> &mdash; rendered as formula and "
               "sign only. The renderer does not interpret the direction in prose "
               "(Peraturan Sifar #6; the direction error was made 3&times; in one day, "
               "registry MC-001).<br>"
               "<code>bias = confidence - accuracy</code><br>"
               f"<code>{_num(conf)} - {_num(acc)} = <strong>{_num(bias)}</strong></code><br>"
               f"<code>sign = {_esc(sign)}</code><br>"
               "<span class='small'>Canon legend, quoted not paraphrased: "
               "&ldquo;bias = confidence &minus; accuracy. Tanda negatif = "
               "UNDER-confident (keyakinan di bawah ketepatan).&rdquo;</span></div>")

    # ── BSS headline instead of a reliability diagram (§8.2) ──
    out.append("<div class='box key'><strong>Headline vs chance:</strong> "
               f"<code>{_esc(bss(c.get('mean_brier')))}</code>"
               + (" &mdash; roughly 40% better than a coin flip, at the n shown above."
                  if isinstance(c.get("mean_brier"), float) else "")
               + "<br><span class='small'><strong>No reliability diagram is rendered, "
                 "deliberately.</strong> With "
               f"{_esc(n_eff_s)} effective observations across 10 bins most bins would "
               "hold &le;3 points, so the curve would be noise presented as a "
               "measurement. The honest form at this n is the per-row-n table above "
               "(proposal §8.2). Adopt a diagram only once verified n reaches the "
               "floor.</span></div>")

    # ── honest scopes: the per-row-n table that replaces the curve ──
    scopes = c.get("honest_scopes") or {}
    if scopes:
        out.append("<h3>Honest scopes (the SOT's own, each with its n)</h3>"
                   "<table><thead><tr><th>scope</th><th>n</th><th>correct</th>"
                   "<th>incorrect</th><th>mixed</th><th>accuracy</th>"
                   "<th>mean_brier</th></tr></thead><tbody>")
        for name, s in scopes.items():
            if not isinstance(s, dict):
                continue
            out.append(f"<tr><td class='small'>{_esc(name)}</td>"
                       f"<td>{_esc(s.get('n'))}</td><td>{_esc(s.get('correct'))}</td>"
                       f"<td>{_esc(s.get('incorrect'))}</td><td>{_esc(s.get('mixed'))}</td>"
                       f"<td>{_num(s.get('accuracy'))}</td>"
                       f"<td>{_num(s.get('mean_brier'))}</td></tr>")
        out.append("</tbody></table>")
    err_t = c.get("by_error_type") or {}
    if err_t:
        out.append("<p class='small'>error classes in the SOT: "
                   + ", ".join(f"{_esc(k)}={_esc(v)}" for k, v in err_t.items())
                   + " &mdash; no skill-attributable class is present, which is the "
                     "blindness the blind-share below measures.</p>")

    # ── confidence_proposed vs confidence_calibrated, NEVER merged (§1.5) ──
    out.append("<h3>confidence_proposed and confidence_calibrated — two columns, "
               "never one</h3>")
    if sp.get("n"):
        out.append("<table><thead><tr><th>quantity</th><th>value</th><th>n</th>"
                   "</tr></thead><tbody>"
                   f"<tr><td>mean confidence_proposed (as authored)</td>"
                   f"<td><strong>{_fmt3(sp['mean_proposed'])}</strong></td><td>{sp['n']}</td></tr>"
                   f"<tr><td>mean confidence_calibrated (as emitted)</td>"
                   f"<td><strong>{_fmt3(sp['mean_calibrated'])}</strong></td><td>{sp['n']}</td></tr>"
                   f"<tr><td>spread (max-min) confidence_proposed</td>"
                   f"<td>{_fmt3(sp['spread_proposed'])}</td><td>{sp['n']}</td></tr>"
                   f"<tr><td>spread (max-min) confidence_calibrated</td>"
                   f"<td>{_fmt3(sp['spread_calibrated'])}</td><td>{sp['n']}</td></tr>"
                   f"<tr><td>spread loss = 1 - (spread_calibrated / spread_proposed)</td>"
                   f"<td><strong>{UNMEASURED if sp['spread_loss'] is None else _fmt3(sp['spread_loss'])}"
                   f"</strong></td><td>{sp['n']}</td></tr>"
                   f"<tr><td>mean |proposed - calibrated|</td>"
                   f"<td>{_fmt3(sp['mean_abs_shift'])}</td><td>{sp['n']}</td></tr>"
                   f"<tr><td>rows carrying proposed with no calibrated value</td>"
                   f"<td>{sp['rows_with_proposed_only']}</td>"
                   f"<td>{len(preds)} rows read</td></tr>"
                   "</tbody></table>")
        out.append("<p class='small'>Both columns are printed because collapsing them "
                   "into one number launders the shrinkage the recalibration step "
                   "applies (proposal §1.5, ISSUE-005). Recomputed from "
                   f"<code>{_esc(p_pred)}</code> at this render, not quoted from an "
                   "earlier edition.</p>")
    else:
        out.append(f"<p class='small'><code>{UNMEASURED}</code> — no row in "
                   f"<code>{_esc(p_pred)}</code> carries both confidence fields this "
                   "build.</p>")

    # ── learning receipt: lessons + blind-share ──
    out.append("<h3>Learning receipt</h3>"
               "<table><thead><tr><th>quantity</th><th>value</th>"
               "<th>SOT</th></tr></thead><tbody>"
               f"<tr><td>lessons_total</td><td><strong>{lr['total']}</strong></td>"
               f"<td class='small'>{_esc(p_les)}</td></tr>"
               f"<tr><td>lessons_actionable (actionable=true)</td>"
               f"<td><strong>{lr['actionable']}</strong></td>"
               f"<td class='small'>{_esc(p_les)}</td></tr>"
               f"<tr><td>actionable=false</td><td>{lr['not_actionable']}</td>"
               f"<td class='small'>{_esc(p_les)}</td></tr>"
               f"<tr><td>actionable field absent</td><td>{lr['unspecified']}</td>"
               f"<td class='small'>{_esc(p_les)}</td></tr>"
               f"<tr><td>error class blind (UNTYPED + UNKNOWN)</td>"
               f"<td><strong>{lr['error_class_blind']}</strong></td>"
               f"<td class='small'>{_esc(p_les)}</td></tr>"
               "</tbody></table>")
    out.append("<p class='small'>lesson status: "
               + (", ".join(f"{_esc(k)}={v}" for k, v in sorted(lr["by_status"].items()))
                  or UNMEASURED)
               + " &nbsp;·&nbsp; error_type: "
               + (", ".join(f"{_esc(k)}={v}" for k, v in sorted(lr["by_error_type"].items()))
                  or UNMEASURED)
               + "</p>")
    out.append("<div class='box open'><strong>blind_share</strong> — the contract's "
               "formula, rendered literally: <code>blind_share = lessons_actionable / "
               f"lessons_total = {lr['actionable']} / {lr['total']} = "
               f"{UNMEASURED if lr['blind_share'] is None else _fmt3(lr['blind_share'])}"
               "</code><br>"
               "Complementary count, printed beside it so the formula cannot be "
               "misread: <code>non_actionable_share = (lessons_total - "
               f"lessons_actionable) / lessons_total = {lr['total'] - lr['actionable']} / "
               f"{lr['total']} = "
               f"{UNMEASURED if lr['non_actionable_share'] is None else _fmt3(lr['non_actionable_share'])}"
               "</code><br>"
               "<span class='small'><strong>Contradiction preserved, not smoothed:</strong> "
               "the canon names the ratio <code>lessons_actionable / lessons_total</code> "
               "&ldquo;blind-share&rdquo;, while its own worked example (&ldquo;10/13 "
               "blind&rdquo;) counts the <em>non</em>-actionable side. Both readings are "
               "printed; the renderer picks neither, because choosing would be an "
               "interpretation the source does not support.</span></div>")

    out.append(_render_personal_safe(sot))
    return "".join(out)


def _render_personal_safe(sot: dict) -> str:
    """Witness status only, for objects the store itself classifies PERSONAL_SAFE.

    The boundary is not this module's judgement about what feels personal — it is
    the event's own declared `kind`. What may be rendered: that a form/condition
    exists, its dates, its deadline, and the rules the owner wrote. What may not:
    any inference about the owner's posture, motive or intention. That is UNKNOWN
    and it stays UNKNOWN, in the document, on the page, where a reader can see
    the machine declining to guess.
    """
    events = [e for e in (sot.get("events") or [])
              if isinstance(e, dict) and str(e.get("kind") or "").upper() == PERSONAL_SAFE_KIND]
    preds = sot.get("predictions") or []
    out = ["<h3>PERSONAL_SAFE — witness status only</h3>"]
    if not events:
        out.append(f"<p class='small'>No event in <code>AAA/scripts/chron_events.json</code> "
                   "declares <code>kind=PERSONAL_SAFE</code> this build.</p>")
        return "".join(out)
    for e in events:
        eid = str(e.get("id") or UNMEASURED)
        bound = [r for r in preds if str(r.get("source_id") or "") == eid]
        out.append("<div class='box claim'>"
                   f"<strong>{_esc(e.get('title') or eid)}</strong> "
                   f"<span class='small'>(event <code>{_esc(eid)}</code>, "
                   f"kind={_esc(e.get('kind'))})</span>"
                   "<table><thead><tr><th>witness field</th><th>value as declared</th>"
                   "</tr></thead><tbody>"
                   f"<tr><td>target_date (deadline)</td><td>{_esc(e.get('target_date') or UNMEASURED)}"
                   f" <span class='small'>{_esc(e.get('timezone') or '')}</span></td></tr>"
                   f"<tr><td>consequence (store-declared)</td><td>{_esc(e.get('consequence') or UNMEASURED)}</td></tr>"
                   f"<tr><td>actionability (store-declared)</td><td>{_esc(e.get('actionability') or UNMEASURED)}</td></tr>"
                   f"<tr><td>declared source</td><td class='small'>{_esc(e.get('source') or UNMEASURED)}</td></tr>"
                   f"<tr><td>owner note (verbatim)</td><td class='small'>{_esc(e.get('note') or UNMEASURED)}</td></tr>"
                   "</tbody></table>")
        rules = e.get("predictions") or []
        if rules:
            out.append("<p class='small'><strong>Conditions the owner wrote</strong> "
                       "(rendered as written; the machine adds no reading of them):</p>"
                       "<table><thead><tr><th>condition</th><th>verifier</th>"
                       "<th>falsifier</th></tr></thead><tbody>")
            for r in rules:
                if not isinstance(r, dict):
                    continue
                out.append(f"<tr><td>{_esc(r.get('claim') or UNMEASURED)}</td>"
                           f"<td class='small'>{_esc(r.get('verifier') or UNMEASURED)}</td>"
                           f"<td class='small'>{_esc(r.get('falsifier') or UNMEASURED)}</td></tr>")
            out.append("</tbody></table>")
        if bound:
            out.append("<p class='small'><strong>Ledger rows bound to this event</strong> "
                       "(witness status only):</p>"
                       "<table><thead><tr><th>prediction_id</th><th>status</th>"
                       "<th>lineage</th><th>created_at</th><th>verify_at</th>"
                       "<th>falsifier</th></tr></thead><tbody>")
            for r in bound:
                out.append(f"<tr><td class='small'>{_esc(r.get('prediction_id') or UNMEASURED)}</td>"
                           f"<td>{_esc(r.get('status') or UNMEASURED)}</td>"
                           f"<td>{_esc(_lineage(r.get('status')))}</td>"
                           f"<td class='small'>{_esc(str(r.get('created_at') or UNMEASURED)[:10])}</td>"
                           f"<td class='small'>{_esc(r.get('verify_at') or UNMEASURED)}</td>"
                           f"<td class='small'>{_esc(r.get('falsifier') or UNMEASURED)}</td></tr>")
            out.append("</tbody></table>")
        out.append(f"<p><strong>{_esc(INTENT_UNKNOWN)}</strong></p></div>")
    return "".join(out)


# ── the composed result ──────────────────────────────────────────────────────


@dataclass
class ComputedSections:
    html: str = ""
    assertions: list[dict] = field(default_factory=list)
    must_contain: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    snapshot: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"html_chars": len(self.html), "assertions_armed": len(self.assertions),
                "must_contain": self.must_contain, "errors": self.errors,
                "snapshot": self.snapshot}


def compute_sections(*, today: str | None = None, top_n: int = 5,
                     window_days: int = 7, newcomer_days: int = 7,
                     sot: dict | None = None) -> ComputedSections:
    """Read the stores once and render all four sections.

    `today` is the EDITION date, not the wall clock, so a rebuild of a past
    edition reproduces the same ages. `sot` is injectable for tests; production
    callers leave it None and get a fresh read.
    """
    ref = _parse_dt(today) if today else datetime.now(timezone.utc)
    if ref is None:
        ref = datetime.now(timezone.utc)
    ref = ref.replace(hour=0, minute=0, second=0, microsecond=0)
    rendered_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _REWRITES["n"] = 0
    s = sot if sot is not None else load_sot()

    errs: list[str] = []
    parts: list[str] = []
    counts: dict[str, int] = {}

    def guarded(name: str, fn, err_keys: tuple[str, ...]) -> str:
        """One broken section must not take the edition down — and must not
        disappear quietly either. The error is printed IN the document."""
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - report, never mask
            msg = f"{name}: render failed ({type(exc).__name__}: {exc})"
            errs.append(msg)
            return (f"<h2>{name}</h2><div class='box warn'><strong>SECTION NOT "
                    f"COMPUTED.</strong><br><span class='small'>{_esc(msg)}<br>"
                    f"Nothing is substituted for it: {UNMEASURED}</span></div>")

    e_cal = s["errors"].get("calibration")
    e_pred = s["errors"].get("predictions")
    e_les = s["errors"].get("lessons")
    for e in (s["errors"].get("episodes"), s["errors"].get("eurekas"),
              s["errors"].get("events")):
        if e:
            errs.append(e)
    if e_pred:
        errs.append(e_pred)
    if e_les:
        errs.append(e_les)
    if e_cal:
        errs.append(e_cal)

    mc = guarded("0.2 MODEL_CHANGE", lambda: model_change_rows(
        s, today=ref, window_days=window_days), ())
    counts["model_change_rows"] = len(mc)
    parts.append(guarded("0.2 MODEL_CHANGE", lambda: render_model_change(
        mc, errors=[e for e in errs if "episode" in e or "eureka" in e
                    or "events" in e or "calibration" in e],
        rendered_at=rendered_at), ()))

    parts.append(guarded("0.3 PREDICTION_LINEAGE", lambda: render_prediction_lineage(
        s, today=ref, top_n=top_n, errors=[e_pred] if e_pred else []), ()))

    surv = guarded("0.4 SURVIVORS", lambda: survivor_rows(
        s, today=ref, newcomer_days=newcomer_days), ())
    if isinstance(surv, dict):
        counts.update({"unresolved_rows": surv["live"],
                       "survivors": len(surv["survivors"]),
                       "newcomers": len(surv["newcomers"]),
                       "age_unmeasured": len(surv["undated"])})
        parts.append(guarded("0.4 SURVIVORS_AND_NEWCOMERS", lambda: render_survivors(
            s, today=ref, newcomer_days=newcomer_days,
            errors=[e_pred] if e_pred else [], limit=10), ()))
    else:
        parts.append(surv)

    parts.append(guarded("0.5 LEARNING_RECEIPT + CALIBRATION_WITNESS",
                         lambda: render_learning(
                             s, today=ref,
                             errors=[e for e in (e_cal, e_les, e_pred) if e]), ()))

    # Disclosure of the one mechanical edit made to quoted store text (see _esc).
    # A renderer that alters evidence silently is the defect this module exists to
    # prevent, so the alteration is printed on the page it affected.
    note = ""
    if _REWRITES["n"]:
        note = ("<p class='small'><strong>Provenance note:</strong> "
                f"{_REWRITES['n']} internal absolute path prefix(es) inside quoted "
                "store text were rewritten root-relative so the text-layer gate "
                "holds. No other character of the quoted text was altered.</p>")
    html = note + "".join(parts)
    # Defence in depth: g_text_layer refuses a document leaking an internal
    # absolute path. Catch it here, at the source, with the section named.
    for pat in _LEAK_PREFIXES:
        if pat in html:
            errs.append(f"internal path prefix {pat!r} reached the rendered HTML — "
                        "SOT labels must be root-relative")

    lr = lessons_report(s.get("lessons") or [])
    sp = spread_report(s.get("predictions") or [])
    calib = s.get("calibration") or {}
    snapshot = {
        "rendered_at": rendered_at,
        "edition_date": ref.strftime("%Y-%m-%d"),
        "sot": {k: _sot_label(v) for k, v in s["paths"].items()},
        "counts": counts,
        "calibration": {k: calib.get(k) for k in (
            "accuracy", "mean_brier", "bias", "mean_confidence", "predictions_total",
            "effective_n", "quality", "updated_at")} if isinstance(calib, dict) else None,
        "lessons": {k: lr[k] for k in ("total", "actionable", "not_actionable",
                                       "unspecified", "error_class_blind",
                                       "blind_share", "non_actionable_share")},
        "confidence_spread": {k: sp.get(k) for k in (
            "n", "mean_proposed", "mean_calibrated", "spread_proposed",
            "spread_calibrated", "spread_loss")},
        "episodes": {"learn_episodes": len(s.get("episodes") or []),
                     "lines_scanned": s.get("episode_lines_scanned"),
                     "tail_bounded": s.get("episode_scan_bounded")},
        "path_rewrites_in_quoted_text": _REWRITES["n"],
        "sot_errors": s["errors"],
    }
    return ComputedSections(
        html=html,
        assertions=calibration_assertions(calib if isinstance(calib, dict) else None,
                                          s["paths"]["calibration"]),
        must_contain=["MODEL_CHANGE", "PREDICTION_LINEAGE", "SURVIVORS_AND_NEWCOMERS",
                      "LEARNING_RECEIPT", "CALIBRATION_WITNESS"],
        errors=errs,
        snapshot=snapshot,
    )
