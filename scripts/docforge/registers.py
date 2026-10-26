#!/usr/bin/env python3
"""docforge.registers — the permanent layer under the daily edition.

WHY THIS EXISTS
  The edition is an evidence feed. It answers "what happened today". A briefing
  that only answers that is a newspaper with better sourcing: each morning's
  items are atomised, and nothing accumulates into knowledge.

  Five registers sit under the feed and survive it:

    SCARS          a failure that recurred is a survival rule, not an anecdote
    CONTRADICTIONS two claims that cannot both be true, held open until one dies
    STATES          a situation moving through phases, with a confidence
    REALITIES       the durable things the daily items are evidence ABOUT
    AGEING/ENTROPY  whether the register is metabolising or just accreting

  The edition stays the unit of evidence. These are the units of understanding.

ONE OWNER, ADDITIVE SCHEMA
  This module owns the register tables and nothing else. It never rewrites the
  delta engine (state.py) and never migrates a table destructively. New columns
  are added with ALTER TABLE ... ADD COLUMN; new tables are CREATE IF NOT EXISTS.
  `items.reality` is the only touch to an existing table, and it is nullable.

THE THREE LAWS THE REGISTERS ENFORCE
  1. ABSENT IS NOT RESOLVED. A contradiction or a scar that is not re-declared
     today keeps its last known state and its age — it does not vanish.
  2. A CLOSE REQUIRES A REASON. A contradiction cannot be marked RESOLVED with
     an empty resolution; a scar cannot be RETIRED with an empty fix.
  3. COUNT FROM EVIDENCE, NEVER FROM A COUNTER THE PRODUCER MAINTAINS.
     Scar recurrence is COUNT(scar_events), one row per witnessed edition, so
     re-running a build cannot inflate it (the EDITION-029 run-counter defect).

WHAT IS NOT MEASURED
  Confidence is DECLARED by the producer, not computed here. A register that
  invents a confidence number from source counts would look rigorous and be
  meaningless; the declared value is labelled as declared and the raw counts
  sit beside it so a reader can disagree.

CLI
  python3 -m docforge.registers --db <path> --edition EDITION-NNN [--json]
"""

from __future__ import annotations

import html
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

REGISTER_SCHEMA = """
CREATE TABLE IF NOT EXISTS scars (
    scar_id      TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    severity     TEXT NOT NULL DEFAULT 'medium',
    status       TEXT NOT NULL DEFAULT 'ACTIVE',
    symptom      TEXT,
    root_cause   TEXT,
    fix          TEXT,
    first_seen   TEXT NOT NULL,
    last_seen    TEXT NOT NULL,
    evidence     TEXT
);
CREATE TABLE IF NOT EXISTS scar_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    scar_id     TEXT NOT NULL,
    edition     TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    note        TEXT,
    UNIQUE(scar_id, edition)
);
CREATE TABLE IF NOT EXISTS contradictions (
    cid              TEXT PRIMARY KEY,
    topic            TEXT NOT NULL,
    claim_a          TEXT NOT NULL,
    source_a         TEXT,
    claim_b          TEXT NOT NULL,
    source_b         TEXT,
    opened_edition   TEXT NOT NULL,
    opened_at        TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'OPEN',
    resolution       TEXT,
    resolved_edition TEXT,
    resolved_at      TEXT
);
CREATE TABLE IF NOT EXISTS states (
    state_id      TEXT PRIMARY KEY,
    label         TEXT NOT NULL,
    phase         TEXT NOT NULL,
    confidence    REAL,
    first_seen    TEXT NOT NULL,
    last_seen     TEXT NOT NULL,
    last_observed TEXT NOT NULL,
    note          TEXT
);
CREATE TABLE IF NOT EXISTS state_obs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    state_id    TEXT NOT NULL,
    edition     TEXT NOT NULL,
    phase       TEXT NOT NULL,
    confidence  REAL,
    observed_at TEXT NOT NULL,
    note        TEXT,
    UNIQUE(state_id, edition)
);
CREATE TABLE IF NOT EXISTS realities (
    reality_id TEXT PRIMARY KEY,
    label      TEXT NOT NULL,
    domain     TEXT,
    status     TEXT NOT NULL DEFAULT 'ACTIVE',
    first_seen TEXT NOT NULL,
    last_seen  TEXT NOT NULL,
    note       TEXT
);
"""

PHASES = ("ESCALATING", "ELEVATED", "HOLDING", "DEESCALATING", "LATENT")
SEVERITIES = ("low", "medium", "high", "critical")
SCAR_STATUS = ("ACTIVE", "MITIGATED", "RETIRED")
CONTRADICTION_STATUS = ("OPEN", "RESOLVED", "DISSOLVED")
REALITY_STATUS = ("ACTIVE", "DORMANT", "CLOSED")

# EUREKA items are checkable one-line facts, already settled by publication.
# They are not claims awaiting resolution, so they must not age into a backlog
# or be counted as open contradictions. Excluding them here is a modelling
# decision stated once, in one place, rather than a filter smeared across SQL.
NON_CLAIM_SECTIONS = ("EUREKA",)

AGED_AFTER_EDITIONS = 7  # "aged" is a judgement; name the number, don't hide it
CONTRADICTION_AGED = 3


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Idempotent, additive. Safe to call on every read and write."""
    conn.executescript(REGISTER_SCHEMA)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(items)")}
    if "reality" not in cols:
        conn.execute("ALTER TABLE items ADD COLUMN reality TEXT")
    conn.commit()


# ── the edition axis ─────────────────────────────────────────────────────────


def _axis(
    conn: sqlite3.Connection,
) -> tuple[list[dict], dict[str, int], dict[str, int]]:
    eds = [
        dict(r)
        for r in conn.execute(
            "SELECT edition, date FROM editions ORDER BY date, built_at"
        )
    ]
    by_ed = {e["edition"]: i for i, e in enumerate(eds)}
    by_date: dict[str, int] = {}
    for i, e in enumerate(eds):
        by_date[e["date"]] = i
    return eds, by_ed, by_date


def _all_items(conn: sqlite3.Connection) -> list[dict]:
    ensure_schema(conn)
    return [
        dict(r)
        for r in conn.execute(
            "SELECT rowid AS rid, item_id, edition, section, title, claim_state,"
            " summary, source, first_seen, last_seen, last_changed, reality"
            " FROM items"
        )
    ]


def _latest_asof(
    rows: list[dict], allowed: set[str], by_ed: dict[str, int]
) -> dict[str, dict]:
    best: dict[str, dict] = {}
    best_key: dict[str, tuple] = {}
    for r in rows:
        if r["edition"] not in allowed:
            continue
        key = (by_ed.get(r["edition"], -1), r["rid"])
        iid = r["item_id"]
        if iid not in best or key > best_key[iid]:
            best[iid] = dict(r)
            best_key[iid] = key
    # A reality anchor is durable. Rewriting an item's row must not silently
    # drop the anchor just because the producer omitted the field on a later
    # day; it persists until it is explicitly changed.
    anchor: dict[str, str] = {}
    for r in sorted(rows, key=lambda x: (by_ed.get(x["edition"], -1), x["rid"])):
        if r["edition"] in allowed and r.get("reality"):
            anchor[r["item_id"]] = r["reality"]
    for iid, it in best.items():
        if not it.get("reality") and iid in anchor:
            it["reality"] = anchor[iid]
    return best


def _allowed_upto(eds: list[dict], edition: str) -> set[str]:
    out = set()
    for e in eds:
        out.add(e["edition"])
        if e["edition"] == edition:
            break
    return out


# ── writes ───────────────────────────────────────────────────────────────────


def _one(payload: dict, key: str) -> list[dict]:
    val = payload.get(key) or []
    if not isinstance(val, list):
        raise ValueError(f"{key!r} must be a list of objects")
    for v in val:
        if not isinstance(v, dict):
            raise ValueError(f"{key!r} contains a non-object entry")
    return val


def record_registers(store, payload: dict, edition: str, date: str) -> dict:
    """Persist the producer's declared inventory for one edition.

    The producer declares the CURRENT inventory, not a delta. Anything omitted
    keeps its last known state (absent != resolved). Every value that can be
    counted is counted from rows, never accepted as a producer-supplied total.
    """
    conn = store.conn
    ensure_schema(conn)
    now = utc_now()
    counts = {
        "scars": 0,
        "scar_events": 0,
        "contradictions": 0,
        "states": 0,
        "realities": 0,
        "items_bound": 0,
    }

    # items.reality — nullable anchor from the daily items[] itself
    for it in payload.get("_items", []):
        rid = it.get("item_id")
        anchor = it.get("reality")
        if rid and anchor:
            cur = conn.execute(
                "UPDATE items SET reality = ? WHERE item_id = ? AND edition = ?",
                (str(anchor).strip().upper(), rid, edition),
            )
            counts["items_bound"] += cur.rowcount

    # realities — durable anchors
    for r in _one(payload, "realities"):
        rid = str(r.get("reality_id") or "").strip().upper()
        if not rid:
            raise ValueError("realities[]: reality_id required")
        status = str(r.get("status") or "ACTIVE").upper()
        if status not in REALITY_STATUS:
            raise ValueError(f"{rid}: status {status!r} not in {REALITY_STATUS}")
        conn.execute(
            "INSERT INTO realities (reality_id, label, domain, status, first_seen, last_seen, note)"
            " VALUES (?,?,?,?,?,?,?) ON CONFLICT(reality_id) DO UPDATE SET"
            " label=excluded.label, domain=COALESCE(excluded.domain, realities.domain),"
            " status=excluded.status, last_seen=excluded.last_seen,"
            " note=COALESCE(excluded.note, realities.note)",
            (
                rid,
                r.get("label") or rid,
                r.get("domain"),
                status,
                r.get("first_seen") or edition,
                edition,
                r.get("note"),
            ),
        )
        counts["realities"] += 1

    # states — phase + declared confidence, one observation per edition
    for s in _one(payload, "states"):
        sid = str(s.get("state_id") or "").strip().upper()
        if not sid:
            raise ValueError("states[]: state_id required")
        phase = str(s.get("phase") or "").upper()
        if phase not in PHASES:
            raise ValueError(f"{sid}: phase {phase!r} not in {PHASES}")
        conf = s.get("confidence")
        if conf is not None:
            conf = float(conf)
            if not 0.0 <= conf <= 1.0:
                raise ValueError(f"{sid}: confidence {conf} outside [0,1]")
        conn.execute(
            "INSERT INTO states (state_id, label, phase, confidence, first_seen,"
            " last_seen, last_observed, note) VALUES (?,?,?,?,?,?,?,?)"
            " ON CONFLICT(state_id) DO UPDATE SET label=excluded.label,"
            " phase=excluded.phase, confidence=excluded.confidence,"
            " last_seen=excluded.last_seen, last_observed=excluded.last_observed,"
            " note=COALESCE(excluded.note, states.note)",
            (
                sid,
                s.get("label") or sid,
                phase,
                conf,
                s.get("first_seen") or edition,
                edition,
                edition,
                s.get("note"),
            ),
        )
        conn.execute(
            "INSERT INTO state_obs (state_id, edition, phase, confidence, observed_at, note)"
            " VALUES (?,?,?,?,?,?) ON CONFLICT(state_id, edition) DO UPDATE SET"
            " phase=excluded.phase, confidence=excluded.confidence,"
            " observed_at=excluded.observed_at, note=COALESCE(excluded.note, state_obs.note)",
            (sid, edition, phase, conf, now, s.get("note")),
        )
        counts["states"] += 1

    # contradictions — opened once, closed only with a reason
    for c in _one(payload, "contradictions"):
        cid = str(c.get("cid") or "").strip().upper()
        if not cid:
            raise ValueError("contradictions[]: cid required")
        row = conn.execute(
            "SELECT * FROM contradictions WHERE cid = ?", (cid,)
        ).fetchone()
        status = str(c.get("status") or "OPEN").upper()
        if status not in CONTRADICTION_STATUS:
            raise ValueError(f"{cid}: status {status!r} not in {CONTRADICTION_STATUS}")
        if row is None:
            if not c.get("claim_a") or not c.get("claim_b"):
                raise ValueError(
                    f"{cid}: claim_a and claim_b required on first declaration"
                )
            conn.execute(
                "INSERT INTO contradictions (cid, topic, claim_a, source_a, claim_b,"
                " source_b, opened_edition, opened_at, status, resolution,"
                " resolved_edition, resolved_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    cid,
                    c.get("topic") or cid,
                    c["claim_a"],
                    c.get("source_a"),
                    c["claim_b"],
                    c.get("source_b"),
                    c.get("opened_edition") or edition,
                    now,
                    status,
                    c.get("resolution"),
                    edition if status != "OPEN" else None,
                    now if status != "OPEN" else None,
                ),
            )
        else:
            if row["status"] != "OPEN" and status == "OPEN":
                raise ValueError(
                    f"{cid}: already {row['status']} — mint a new cid rather than reopening"
                )
            if status != "OPEN" and not (c.get("resolution") or "").strip():
                raise ValueError(f"{cid}: closing requires a non-empty resolution")
            conn.execute(
                "UPDATE contradictions SET topic=COALESCE(?, topic),"
                " claim_a=COALESCE(?, claim_a), source_a=COALESCE(?, source_a),"
                " claim_b=COALESCE(?, claim_b), source_b=COALESCE(?, source_b),"
                " status=?, resolution=COALESCE(?, resolution),"
                " resolved_edition=COALESCE(?, resolved_edition),"
                " resolved_at=COALESCE(?, resolved_at) WHERE cid=?",
                (
                    c.get("topic"),
                    c.get("claim_a"),
                    c.get("source_a"),
                    c.get("claim_b"),
                    c.get("source_b"),
                    status,
                    c.get("resolution"),
                    edition if status != "OPEN" else None,
                    now if status != "OPEN" else None,
                    cid,
                ),
            )
        counts["contradictions"] += 1

    # scars — recurrence counted from events, never from a supplied counter
    for sc in _one(payload, "scars"):
        sid = str(sc.get("scar_id") or "").strip().upper()
        if not sid:
            raise ValueError("scars[]: scar_id required")
        sev = str(sc.get("severity") or "medium").lower()
        if sev not in SEVERITIES:
            raise ValueError(f"{sid}: severity {sev!r} not in {SEVERITIES}")
        status = str(sc.get("status") or "ACTIVE").upper()
        if status not in SCAR_STATUS:
            raise ValueError(f"{sid}: status {status!r} not in {SCAR_STATUS}")
        if status == "RETIRED" and not (sc.get("fix") or "").strip():
            raise ValueError(f"{sid}: retiring a scar requires a non-empty fix")
        first = sc.get("first_seen") or edition
        conn.execute(
            "INSERT INTO scars (scar_id, name, severity, status, symptom, root_cause,"
            " fix, first_seen, last_seen, evidence) VALUES (?,?,?,?,?,?,?,?,?,?)"
            " ON CONFLICT(scar_id) DO UPDATE SET name=excluded.name,"
            " severity=excluded.severity, status=excluded.status,"
            " symptom=COALESCE(excluded.symptom, scars.symptom),"
            " root_cause=COALESCE(excluded.root_cause, scars.root_cause),"
            " fix=COALESCE(excluded.fix, scars.fix),"
            " last_seen=excluded.last_seen,"
            " evidence=COALESCE(excluded.evidence, scars.evidence)",
            (
                sid,
                sc.get("name") or sid,
                sev,
                status,
                sc.get("symptom"),
                sc.get("root_cause"),
                sc.get("fix"),
                first,
                edition,
                sc.get("evidence"),
            ),
        )
        # A standing inventory entry is NOT evidence of a fresh occurrence.
        # The producer must say `recurred_today: true` (with the symptom it saw
        # today) or the counter stays put. Default-false is the fail-safe
        # direction: under-count rather than inflate, the EDITION-029 lesson.
        if sc.get("recurred_today") is True:
            cur = conn.execute(
                "INSERT OR IGNORE INTO scar_events (scar_id, edition, observed_at, note)"
                " VALUES (?,?,?,?)",
                (sid, edition, now, sc.get("observed_note")),
            )
            counts["scar_events"] += cur.rowcount
        for occ in sc.get("occurrences") or []:
            if not isinstance(occ, dict) or not occ.get("edition"):
                raise ValueError(f"{sid}: occurrences[] needs {{edition, note}}")
            cur = conn.execute(
                "INSERT OR IGNORE INTO scar_events (scar_id, edition, observed_at, note)"
                " VALUES (?,?,?,?)",
                (sid, occ["edition"], now, occ.get("note")),
            )
            counts["scar_events"] += cur.rowcount
        counts["scars"] += 1

    conn.commit()
    return counts


# ── reads ────────────────────────────────────────────────────────────────────


def _open_latest(conn, edition: str, include_eureka: bool = False) -> list[dict]:
    eds, by_ed, _ = _axis(conn)
    rows = _all_items(conn)
    latest = _latest_asof(rows, _allowed_upto(eds, edition), by_ed)
    out = []
    for it in latest.values():
        if it["claim_state"] in ("SETTLED", "RETRACTED"):
            continue
        if not include_eureka and it["section"] in NON_CLAIM_SECTIONS:
            continue
        out.append(it)
    return out


def ageing(store, edition: str) -> list[dict]:
    """Age of every open claim, in editions, from recorded evidence only."""
    conn = store.conn
    ensure_schema(conn)
    eds, by_ed, by_date = _axis(conn)
    today = by_ed.get(edition, len(eds) - 1)
    seen: dict[str, int] = {}
    for r in conn.execute(
        "SELECT item_id, COUNT(DISTINCT edition) n FROM items GROUP BY item_id"
    ):
        seen[r["item_id"]] = r["n"]

    out = []
    for it in _open_latest(conn, edition):
        age = max(0, today - by_date.get(it["first_seen"], today))
        stalled = max(0, today - by_date.get(it["last_changed"], today))
        out.append(
            {
                "item_id": it["item_id"],
                "section": it["section"],
                "title": it["title"],
                "claim_state": it["claim_state"],
                "first_seen": it["first_seen"],
                "last_seen": it["last_seen"],
                "age_editions": age,
                "stalled_editions": stalled,
                "seen_editions": seen.get(it["item_id"], 1),
                "reality": it.get("reality"),
                "aged": age > AGED_AFTER_EDITIONS,
            }
        )
    out.sort(key=lambda x: (-x["age_editions"], x["section"], x["title"]))
    return out


def contradictions(store, edition: str, include_closed: bool = False) -> list[dict]:
    conn = store.conn
    ensure_schema(conn)
    _, by_ed, _ = _axis(conn)
    today = by_ed.get(edition, 0)
    q = "SELECT * FROM contradictions"
    if not include_closed:
        q += " WHERE status = 'OPEN'"
    q += " ORDER BY opened_edition"
    out = []
    for r in conn.execute(q):
        d = dict(r)
        d["age_editions"] = max(0, today - by_ed.get(d["opened_edition"], today))
        d["aged"] = d["age_editions"] > CONTRADICTION_AGED
        out.append(d)
    return out


def scar_ledger(store, edition: str, include_retired: bool = False) -> list[dict]:
    conn = store.conn
    ensure_schema(conn)
    q = "SELECT * FROM scars"
    if not include_retired:
        q += " WHERE status != 'RETIRED'"
    q += " ORDER BY scar_id"
    out = []
    for r in conn.execute(q):
        d = dict(r)
        d["recurrence"] = conn.execute(
            "SELECT COUNT(*) FROM scar_events WHERE scar_id = ?", (d["scar_id"],)
        ).fetchone()[0]
        d["recurred_this_edition"] = bool(
            conn.execute(
                "SELECT 1 FROM scar_events WHERE scar_id = ? AND edition = ?",
                (d["scar_id"], edition),
            ).fetchone()
        )
        out.append(d)
    return out


def states(store, edition: str) -> list[dict]:
    conn = store.conn
    ensure_schema(conn)
    _, by_ed, _ = _axis(conn)
    today = by_ed.get(edition, 0)
    out = []
    for r in conn.execute("SELECT * FROM states ORDER BY state_id"):
        d = dict(r)
        obs = [
            dict(o)
            for o in conn.execute(
                "SELECT edition, phase, confidence FROM state_obs"
                " WHERE state_id = ? AND edition != ?",
                (d["state_id"], edition),
            )
        ]
        prev = max(obs, key=lambda o: by_ed.get(o["edition"], -1)) if obs else None
        d["prev_phase"] = prev["phase"] if prev else None
        d["observed_this_edition"] = bool(
            conn.execute(
                "SELECT 1 FROM state_obs WHERE state_id = ? AND edition = ?",
                (d["state_id"], edition),
            ).fetchone()
        )
        d["unobserved_editions"] = (
            0
            if d["observed_this_edition"]
            else max(0, today - by_ed.get(d["last_observed"], today))
        )
        d["duration_editions"] = max(0, today - by_ed.get(d["first_seen"], today)) + 1
        d["evidence_count"] = conn.execute(
            "SELECT COUNT(*) FROM state_obs WHERE state_id = ?", (d["state_id"],)
        ).fetchone()[0]
        out.append(d)
    return out


def realities(store, edition: str) -> list[dict]:
    conn = store.conn
    ensure_schema(conn)
    _, by_ed, _ = _axis(conn)
    today = by_ed.get(edition, 0)
    rows = _all_items(conn)
    latest = _latest_asof(rows, _allowed_upto(_axis(conn)[0], edition), by_ed)
    out = []
    for r in conn.execute("SELECT * FROM realities ORDER BY reality_id"):
        d = dict(r)
        bound = [
            it for it in latest.values() if (it.get("reality") or "") == d["reality_id"]
        ]
        d["bound_total"] = len(bound)
        d["bound_open"] = sum(
            1 for it in bound if it["claim_state"] not in ("SETTLED", "RETRACTED")
        )
        d["bound_moved"] = sum(
            1 for it in bound if it["claim_state"] in ("MOVED", "NEW", "CONTESTED")
        )
        d["age_editions"] = max(0, today - by_ed.get(d["first_seen"], today))
        out.append(d)
    return out


def unbound_items(store, edition: str) -> list[dict]:
    return [it for it in _open_latest(store.conn, edition) if not it.get("reality")]


def entropy(store, edition: str, delta=None) -> dict:
    """The health read: is the register metabolising, or accreting?

    Every number is derived from rows. Where a number is a judgement (what
    counts as "aged"), the threshold is a named constant, not a hidden one.
    """
    conn = store.conn
    ensure_schema(conn)
    from .state import Store  # local import keeps this module importable alone

    eds, by_ed, _ = _axis(conn)
    today = by_ed.get(edition, len(eds) - 1)
    prev = eds[today - 1]["edition"] if today > 0 else None
    if delta is None:
        delta = Store(store.path).delta(edition)

    rows = _all_items(conn)
    to_today = _latest_asof(rows, _allowed_upto(eds, edition), by_ed)
    open_now = [
        r
        for r in to_today.values()
        if r["claim_state"] not in ("SETTLED", "RETRACTED")
        and r["section"] not in NON_CLAIM_SECTIONS
    ]
    open_prev = []
    if prev:
        p = _latest_asof(rows, _allowed_upto(eds, prev), by_ed)
        open_prev = [
            r
            for r in p.values()
            if r["claim_state"] not in ("SETTLED", "RETRACTED")
            and r["section"] not in NON_CLAIM_SECTIONS
        ]

    aged_rows = ageing(store, edition)
    aged = [r for r in aged_rows if r["aged"]]
    settled = len(delta.settled)
    dropped = len([d for d in delta.dropped if d["section"] not in NON_CLAIM_SECTIONS])
    exits = settled + dropped
    op = contradictions(store, edition)
    sc = scar_ledger(store, edition)
    st = states(store, edition)
    rl = realities(store, edition)
    unbound = [it for it in open_now if not it.get("reality")]
    unbound_today = [
        it
        for it in to_today.values()
        if it["edition"] == edition
        and it["section"] not in NON_CLAIM_SECTIONS
        and not it.get("reality")
    ]
    today_claims = [
        it
        for it in to_today.values()
        if it["edition"] == edition and it["section"] not in NON_CLAIM_SECTIONS
    ]

    moved_realities = [
        r
        for r in rl
        if any(
            s["state_id"] == r["reality_id"]
            and s["observed_this_edition"]
            and s["prev_phase"] is not None
            and s["phase"] != s["prev_phase"]
            for s in st
        )
    ]
    open_delta = len(open_now) - len(open_prev)
    if open_delta > 0:
        verdict = "ACCUMULATING"
    elif open_delta < 0:
        verdict = "METABOLIZING"
    else:
        verdict = "HOLDING"

    return {
        "edition": edition,
        "open_claims": len(open_now),
        "open_claims_prev": len(open_prev),
        "open_delta": open_delta,
        "new": len(delta.new),
        "moved": len(delta.moved),
        "settled": settled,
        "dropped": dropped,
        "exits": exits,
        "metabolism": round(settled / exits, 3) if exits else None,
        "aged_claims": len(aged),
        "aged_share": round(len(aged) / len(open_now), 3) if open_now else 0.0,
        "median_age_editions": sorted(a["age_editions"] for a in aged_rows)[
            len(aged_rows) // 2
        ]
        if aged_rows
        else 0,
        "contradictions_open": len(op),
        "contradictions_aged": sum(1 for c in op if c["aged"]),
        "scars_active": len(sc),
        "scar_recurrences": sum(1 for s in sc if s["recurred_this_edition"]),
        "states_active": len(st),
        "states_unobserved": sum(1 for s in st if not s["observed_this_edition"]),
        "realities_active": len(rl),
        "realities_moved": len(moved_realities),
        "unbound_open_claims": len(unbound),
        "unbound_today": len(unbound_today),
        "today_claims": len(today_claims),
        "wall_open": sum(1 for r in open_now if r["section"] == "WALL"),
        "verdict": verdict,
        "note": (
            "open_delta is a count of claims, not a thermodynamic quantity. "
            "Aged threshold: >%d editions. Contradiction aged: >%d."
            % (AGED_AFTER_EDITIONS, CONTRADICTION_AGED)
        ),
    }


# ── rendering ────────────────────────────────────────────────────────────────


def _e(v) -> str:
    return html.escape("" if v is None else str(v))


def _fmt_conf(v) -> str:
    return "declared" if v is None else f"{float(v):.2f}"


def render_registers_html(store, edition: str) -> str:
    st = states(store, edition)
    op = contradictions(store, edition)
    sc = scar_ledger(store, edition)
    rl = realities(store, edition)
    if not (st or op or sc or rl):
        return (
            "<h2>0.1 &middot; Registers</h2>"
            "<p class='small'>No register entries declared for this edition. "
            "Ageing and entropy below are derived from the item record, so they "
            "still apply.</p>"
        )

    out = [
        "<h2>0.1 &middot; Registers</h2>",
        "<p class='small'>The permanent layer under this edition. A state is a "
        "situation; an item is evidence about it. Absence is not resolution: a "
        "register entry omitted today keeps its last known state and keeps ageing.</p>",
    ]

    if st:
        out.append(
            "<h3>State register</h3><table><thead><tr><th>State</th><th>Phase</th>"
            "<th>Prev</th><th>Conf</th><th>Duration</th><th>Evidence</th>"
            "</tr></thead><tbody>"
        )
        for s in st:
            flag = (
                ""
                if s["observed_this_edition"]
                else (
                    f" <span class='small'>(not re-observed, {s['unobserved_editions']} ed)</span>"
                )
            )
            out.append(
                f"<tr><td><strong>{_e(s['label'])}</strong>{flag}</td>"
                f"<td><strong>{_e(s['phase'])}</strong></td>"
                f"<td>{_e(s['prev_phase'] or '—')}</td>"
                f"<td>{_e(_fmt_conf(s['confidence']))}</td>"
                f"<td>{s['duration_editions']} ed</td>"
                f"<td>{s['evidence_count']} obs</td></tr>"
            )
        out.append("</tbody></table>")

    if op:
        out.append(
            "<h3>Active contradictions</h3><table><thead><tr><th>ID</th>"
            "<th>Claim A</th><th>Claim B</th><th>Age</th><th>Status</th>"
            "</tr></thead><tbody>"
        )
        for c in op:
            out.append(
                f"<tr><td><strong>{_e(c['cid'])}</strong><br>"
                f"<span class='small'>{_e(c['topic'])}</span></td>"
                f"<td>{_e(c['claim_a'])}<br><span class='small'>{_e(c.get('source_a') or '')}</span></td>"
                f"<td>{_e(c['claim_b'])}<br><span class='small'>{_e(c.get('source_b') or '')}</span></td>"
                f"<td>{c['age_editions']} ed</td><td>{_e(c['status'])}</td></tr>"
            )
        out.append("</tbody></table>")

    if sc:
        out.append(
            "<h3>Scar ledger</h3><p class='small'>A recurrence is counted from "
            "witnessed editions, not from a number the producer maintains.</p>"
            "<table><thead><tr><th>ID</th><th>Failure</th><th>Severity</th>"
            "<th>Recurrence</th><th>Status</th></tr></thead><tbody>"
        )
        for s in sc:
            rec = f"{s['recurrence']}" + (
                " (this edition)" if s["recurred_this_edition"] else ""
            )
            out.append(
                f"<tr><td>{_e(s['scar_id'])}</td>"
                f"<td><strong>{_e(s['name'])}</strong><br>"
                f"<span class='small'>{_e(s.get('symptom') or '')}</span></td>"
                f"<td>{_e(s['severity'])}</td><td>{rec}</td>"
                f"<td>{_e(s['status'])}</td></tr>"
            )
        out.append("</tbody></table>")

    if rl:
        out.append(
            "<h3>Reality register</h3><table><thead><tr><th>Reality</th>"
            "<th>Status</th><th>Bound</th><th>Open</th><th>Moving</th>"
            "</tr></thead><tbody>"
        )
        for r in rl:
            out.append(
                f"<tr><td><strong>{_e(r['label'])}</strong></td>"
                f"<td>{_e(r['status'])}</td><td>{r['bound_total']}</td>"
                f"<td>{r['bound_open']}</td><td>{r['bound_moved']}</td></tr>"
            )
        out.append("</tbody></table>")
    return "".join(out)


def render_entropy_html(store, edition: str, delta=None) -> str:
    m = entropy(store, edition, delta)
    age = ageing(store, edition)
    oldest = age[:8]

    out = [
        "<h2>0.2 &middot; Ageing &amp; Entropy</h2>",
        "<p class='small'>Whether this register is metabolising or merely "
        "accreting. A claim that is open 30 editions is a different fact from "
        f"one open 2. Aged = older than {AGED_AFTER_EDITIONS} editions.</p>",
        "<table><thead><tr><th>Reading</th><th>Value</th></tr></thead><tbody>",
    ]

    def row(k, v):
        out.append(f"<tr><td>{k}</td><td><strong>{v}</strong></td></tr>")

    row(
        "Open claims (excl. EUREKA)",
        f"{m['open_claims']} ({m['open_delta']:+d} vs prev)",
    )
    row("Aged claims", f"{m['aged_claims']} ({int(m['aged_share'] * 100)}%)")
    row("Median age", f"{m['median_age_editions']} editions")
    row("Exits this edition", f"{m['settled']} settled, {m['dropped']} dropped")
    row(
        "Metabolism (settled / exits)",
        "&mdash;" if m["metabolism"] is None else f"{int(m['metabolism'] * 100)}%",
    )
    row(
        "Contradictions",
        f"{m['contradictions_open']} open, {m['contradictions_aged']} aged",
    )
    row("Scars", f"{m['scars_active']} active, {m['scar_recurrences']} recurred today")
    row(
        "States",
        f"{m['states_active']} tracked, {m['states_unobserved']} not re-observed",
    )
    row("Realities", f"{m['realities_active']} active, {m['realities_moved']} moved")
    row(
        "Unbound open claims",
        f"{m['unbound_open_claims']} backlog, {m['unbound_today']}/{m['today_claims']} today",
    )
    row("WALL open", f"{m['wall_open']}")
    row("Verdict", f"<strong>{m['verdict']}</strong>")
    out.append("</tbody></table>")

    if oldest:
        out.append(
            "<h3>Oldest open claims</h3><table><thead><tr><th>Age</th>"
            "<th>Item</th><th>State</th><th>Stalled</th><th>Seen</th>"
            "</tr></thead><tbody>"
        )
        for a in oldest:
            out.append(
                f"<tr><td>{a['age_editions']} ed</td>"
                f"<td><strong>{_e(a['title'])}</strong><br>"
                f"<span class='small'>{_e(a['section'])} &middot; {_e(a['item_id'])}</span></td>"
                f"<td>{_e(a['claim_state'])}</td>"
                f"<td>{a['stalled_editions']} ed</td><td>{a['seen_editions']}</td></tr>"
            )
        out.append("</tbody></table>")
        out.append(
            "<p class='small'>An item seen once and never re-mentioned is not "
            "resolved; it is an abandoned thread. The producer must either "
            "restate it, settle it, or retract it.</p>"
        )
    return "".join(out)


def summary(store, edition: str) -> dict:
    return {
        "ageing": ageing(store, edition)[:10],
        "contradictions": contradictions(store, edition),
        "scars": scar_ledger(store, edition),
        "states": states(store, edition),
        "realities": realities(store, edition),
        "entropy": entropy(store, edition),
    }


def main(argv=None) -> int:
    import argparse
    from .state import DEFAULT_DB, Store

    ap = argparse.ArgumentParser(prog="docforge.registers")
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--edition", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    s = Store(Path(a.db))
    if a.json:
        print(json.dumps(summary(s, a.edition), indent=2, default=str))
        return 0
    m = entropy(s, a.edition)
    print(json.dumps(m, indent=2))
    print("\nStates:")
    for st in states(s, a.edition):
        print(
            f"  {st['state_id']:<34} {st['phase']:<12} conf={_fmt_conf(st['confidence'])} "
            f"dur={st['duration_editions']}ed obs={st['evidence_count']}"
        )
    print("\nContradictions:")
    for c in contradictions(s, a.edition):
        print(f"  {c['cid']:<10} {c['age_editions']}ed  {c['topic']}")
    print("\nScars:")
    for sc in scar_ledger(s, a.edition):
        print(f"  {sc['scar_id']:<34} recurrence={sc['recurrence']:<3} {sc['status']}")
    print("\nOldest open claims:")
    for a_ in ageing(s, a.edition)[:10]:
        print(f"  {a_['age_editions']:>2}ed  {a_['section']:<9} {a_['title'][:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
