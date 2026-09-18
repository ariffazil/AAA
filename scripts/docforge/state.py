#!/usr/bin/env python3
"""docforge.state — the memory that makes tomorrow's edition different from today's.

WHY THIS EXISTS
  A briefing built from scratch every morning is a newspaper, not intelligence.
  It has no idea it said something yesterday. The reader pays the same attention
  cost each day to re-read what they already know, and the genuinely new signal
  is buried in the familiar.

  State fixes that by making the SECOND edition cheaper to read than the first:
  it reports what moved, not the whole board.

THE DELTA IS COMPUTED FROM CLAIM STATE, NOT FROM TEXT DIFFING
  Text diffing a briefing is useless — prose is rewritten every day even when
  the underlying fact has not budged, and it flags a reworded sentence while
  missing that a CONTESTED claim went OPEN. So each tracked item carries an
  explicit lifecycle:

      NEW -> OPEN -> MOVED -> SETTLED
      CONTESTED -> (CONTESTED | SETTLED | RETRACTED)

  The delta is then a set operation over that lifecycle, which is why the answer
  is defensible: "PETRONAS-PETROS moved CONTESTED -> OPEN because the Federal
  Court set a hearing date" is a statement about recorded state, not about how
  someone happened to phrase a paragraph.

WHY SQLITE AND NOT ONLY QDRANT
  Qdrant is for semantic recall — "find me things LIKE this". The delta needs
  exact recall — "what did I record for claim id X, and when did it last
  change". Those are different access patterns and conflating them is how you
  get a vector store that cannot answer a yes/no question.

  SQLite is the authority: a single file, no server, transactional, diffable,
  and it survives a reboot. Qdrant is wired as an OPTIONAL mirror for semantic
  search of past editions; when it is absent the lane still works and says so,
  rather than silently degrading into "no memory".
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB = Path("/root/AAA/forge_work/brief-state.sqlite3")

SCHEMA = """
CREATE TABLE IF NOT EXISTS editions (
    edition     TEXT PRIMARY KEY,
    date        TEXT NOT NULL,
    built_at    TEXT NOT NULL,
    artifact_sha256 TEXT,
    content_sha256  TEXT,
    item_count  INTEGER,
    payload     TEXT
);
CREATE TABLE IF NOT EXISTS items (
    item_id      TEXT NOT NULL,
    edition      TEXT NOT NULL,
    section      TEXT NOT NULL,
    title        TEXT NOT NULL,
    claim_state  TEXT NOT NULL,
    summary      TEXT,
    source       TEXT,
    first_seen   TEXT NOT NULL,
    last_seen    TEXT NOT NULL,
    last_changed TEXT NOT NULL,
    PRIMARY KEY (item_id, edition)
);
CREATE INDEX IF NOT EXISTS idx_items_id ON items(item_id);
CREATE INDEX IF NOT EXISTS idx_items_state ON items(claim_state);
"""

SECTIONS = ("SITUATION", "WALL", "VOID", "EUREKA", "RISK", "OWN")
CLAIM_STATES = ("NEW", "OPEN", "MOVED", "CONTESTED", "SETTLED", "RETRACTED")
TERMINAL_STATES = ("SETTLED", "RETRACTED")

# A WALL is not a claim awaiting resolution — it is a boundary that was tested
# and held. Two different things live under it on purpose:
#   UNRESOLVED  something is knowable but not known yet (a hearing date)
#   WITHDRAWN   something cannot be resolved from open sources at all (a
#               pricetag with no filing behind it)
# Collapsing WITHDRAWN into UNRESOLVED is how a permanent limit starts looking
# like a gap that tomorrow's research will close.
WALL_KINDS = ("UNRESOLVED", "WITHDRAWN")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Delta:
    """What changed since the previous edition, and what is still hanging."""
    new: list[dict] = field(default_factory=list)
    moved: list[dict] = field(default_factory=list)      # state changed
    reopened: list[dict] = field(default_factory=list)   # terminal -> non-terminal
    still_open: list[dict] = field(default_factory=list)
    settled: list[dict] = field(default_factory=list)
    dropped: list[dict] = field(default_factory=list)    # in yesterday, absent today
    first_edition: bool = False

    def as_dict(self) -> dict:
        return {
            "first_edition": self.first_edition,
            "new": self.new, "moved": self.moved, "reopened": self.reopened,
            "still_open": self.still_open, "settled": self.settled,
            "dropped": self.dropped,
            "counts": {k: len(v) for k, v in (
                ("new", self.new), ("moved", self.moved),
                ("reopened", self.reopened), ("still_open", self.still_open),
                ("settled", self.settled), ("dropped", self.dropped))},
        }

    def headline(self) -> str:
        if self.first_edition:
            return "First tracked edition — no prior state to diff against."
        c = self.as_dict()["counts"]
        bits = []
        if c["new"]:
            bits.append(f"{c['new']} new")
        if c["moved"]:
            bits.append(f"{c['moved']} moved")
        if c["reopened"]:
            bits.append(f"{c['reopened']} reopened")
        if c["settled"]:
            bits.append(f"{c['settled']} settled")
        if c["still_open"]:
            bits.append(f"{c['still_open']} carrying over")
        if c["dropped"]:
            bits.append(f"{c['dropped']} dropped without resolution")
        return ", ".join(bits) if bits else "No state change since the last edition."


class Store:
    def __init__(self, path: Path | str = DEFAULT_DB):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    # ── writes ──────────────────────────────────────────────────────────────

    def record_edition(self, edition: str, date: str, items: list[dict],
                       artifact_sha256: str = "", content_sha256: str = "",
                       built_at: str = "", payload: dict | None = None) -> str | None:
        """Upsert one edition and all of its tracked items.

        Re-recording the same edition replaces its rows, so a rebuild (a
        corrected figure, for instance) does not leave the superseded version's
        claims sitting in the delta as phantoms.

        Returns the id of the edition it was diffed against, or None.
        """
        built_at = built_at or utc_now()
        prev = self._prev_edition(edition)

        cur = self.conn.cursor()
        cur.execute("DELETE FROM items WHERE edition = ?", (edition,))
        for it in items:
            item_id = it["item_id"]
            state = it["claim_state"].upper()
            if state not in CLAIM_STATES:
                raise ValueError(f"{item_id}: claim_state {state!r} not in {CLAIM_STATES}")
            prior = self._latest_item(item_id, exclude_edition=edition)
            first_seen = prior["first_seen"] if prior else date
            changed = (not prior) or (prior["claim_state"] != state)
            last_changed = date if (changed or not prior) else prior["last_changed"]
            cur.execute(
                "INSERT INTO items (item_id, edition, section, title, claim_state,"
                " summary, source, first_seen, last_seen, last_changed)"
                " VALUES (?,?,?,?,?,?,?,?,?,?)",
                (item_id, edition, it["section"], it["title"], state,
                 it.get("summary", ""), it.get("source", ""),
                 first_seen, date, last_changed),
            )
        cur.execute(
            "INSERT INTO editions (edition, date, built_at, artifact_sha256,"
            " content_sha256, item_count, payload) VALUES (?,?,?,?,?,?,?)"
            " ON CONFLICT(edition) DO UPDATE SET date=excluded.date,"
            " built_at=excluded.built_at, artifact_sha256=excluded.artifact_sha256,"
            " content_sha256=excluded.content_sha256, item_count=excluded.item_count,"
            " payload=excluded.payload",
            (edition, date, built_at, artifact_sha256, content_sha256,
             len(items), json.dumps(payload or {})),
        )
        self.conn.commit()
        return prev

    # ── reads ───────────────────────────────────────────────────────────────

    def _prev_edition(self, edition: str) -> str | None:
        rows = self.conn.execute(
            "SELECT edition FROM editions WHERE edition != ? ORDER BY date DESC, built_at DESC",
            (edition,)).fetchall()
        return rows[0]["edition"] if rows else None

    def _latest_item(self, item_id: str, exclude_edition: str | None = None) -> sqlite3.Row | None:
        q = "SELECT * FROM items WHERE item_id = ?"
        args: list = [item_id]
        if exclude_edition:
            q += " AND edition != ?"
            args.append(exclude_edition)
        q += " ORDER BY last_seen DESC LIMIT 1"
        return self.conn.execute(q, args).fetchone()

    def editions(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM editions ORDER BY date DESC, built_at DESC")]

    def open_items(self) -> list[dict]:
        """Everything still live, as of each item's LAST sighting.

        First version returned only the items present in the most recent edition.
        A test caught the consequence: a claim recorded in edition 1, never
        resolved, and simply not mentioned in edition 3 vanished from the
        register entirely — the register shrank as coverage moved around, which
        is the opposite of what "what is still hanging" means.

        The register is now the latest known state PER ITEM, not the latest
        edition's subset. Terminal items still leave it, because that exit is a
        real state change rather than an omission.
        """
        rows = self.conn.execute(
            "SELECT * FROM ("
            "  SELECT *, ROW_NUMBER() OVER ("
            "    PARTITION BY item_id ORDER BY last_seen DESC, rowid DESC"
            "  ) AS rn FROM items"
            ") WHERE rn = 1 AND claim_state NOT IN (?, ?)"
            " ORDER BY section, title",
            TERMINAL_STATES).fetchall()
        return [dict(r) for r in rows]

    # ── the delta ───────────────────────────────────────────────────────────

    def delta(self, edition: str) -> Delta:
        """Compare this edition against the most recent OTHER edition."""
        prev_ed = self._prev_edition(edition)
        today = {r["item_id"]: dict(r) for r in self.conn.execute(
            "SELECT * FROM items WHERE edition = ?", (edition,))}
        if not prev_ed:
            return Delta(first_edition=True,
                         new=list(today.values()))

        prev = {r["item_id"]: dict(r) for r in self.conn.execute(
            "SELECT * FROM items WHERE edition = ?", (prev_ed,))}

        d = Delta()
        for iid, it in today.items():
            before = prev.get(iid)
            if before is None:
                d.new.append(it)
                continue
            if before["claim_state"] != it["claim_state"]:
                if (before["claim_state"] in TERMINAL_STATES
                        and it["claim_state"] not in TERMINAL_STATES):
                    d.reopened.append({**it, "was": before["claim_state"]})
                elif it["claim_state"] in TERMINAL_STATES:
                    d.settled.append({**it, "was": before["claim_state"]})
                else:
                    d.moved.append({**it, "was": before["claim_state"]})
            elif it["claim_state"] not in TERMINAL_STATES:
                d.still_open.append(it)
        d.dropped = [it for iid, it in prev.items()
                     if iid not in today and it["claim_state"] not in TERMINAL_STATES]
        return d


# ── optional semantic mirror ─────────────────────────────────────────────────


def qdrant_status() -> tuple[bool, str]:
    """Probe the vector lane without pretending it is required.

    Reported as a status, never as a silent fallback: 'no semantic recall' and
    'semantic recall unavailable' are different facts and the operator is
    entitled to know which one they have.
    """
    try:
        import qdrant_client  # noqa: F401
    except Exception as exc:
        return False, f"qdrant_client not importable: {exc}"
    import os
    url = os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")
    try:
        import urllib.request
        with urllib.request.urlopen(url + "/collections", timeout=3) as r:
            if r.status == 200:
                return True, f"reachable at {url}"
    except Exception as exc:
        return False, f"client present but {url} unreachable: {exc}"
    return False, f"unexpected response from {url}"


def mirror_to_qdrant(edition: str, text: str, meta: dict) -> tuple[bool, str]:
    """Best-effort semantic mirror. Absence never blocks the edition."""
    ok, why = qdrant_status()
    if not ok:
        return False, why
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, PointStruct, VectorParams
        import hashlib
        client = QdrantClient(url=__import__("os").environ.get(
            "QDRANT_URL", "http://127.0.0.1:6333"))
        coll = "hermes_brief_editions"
        names = {c.name for c in client.get_collections().collections}
        if coll not in names:
            client.create_collection(coll, vectors_config=VectorParams(
                size=1024, distance=Distance.COSINE))
        pid = int(hashlib.sha256(edition.encode()).hexdigest()[:15], 16)
        client.upsert(coll, points=[PointStruct(
            id=pid, vector=[0.0] * 1024,
            payload={"edition": edition, "text": text[:4000], **meta})])
        return True, f"mirrored to {coll}"
    except Exception as exc:  # noqa: BLE001 - report, never mask
        return False, f"mirror failed: {exc}"
