#!/usr/bin/env python3
"""docforge.feedback — the loop that makes tomorrow's brief different because of today's comment.

THE PROBLEM
  A briefing that ignores what the reader said about yesterday's briefing is not
  stateful, it is just scheduled. His correction is the highest-quality signal in
  the system — the one input unambiguously about what he actually wants — and
  without a place to put it, it evaporates into a chat message.

WHAT THIS IS NOT
  NOT an automatic prompt-rewriter. A chat remark is RAW MATERIAL, not a rule:
  "buang naratif politik ni" said once after a bad week is an observation, and
  turning it into a permanent filter is the machine obeying a mood. So:
      raw_text   what he actually said, VERBATIM, never rewritten
      rule       the standing instruction DERIVED from it, reviewable
      status     ACTIVE or RETIRED — nothing is deleted, ever

  Direction is stored with the rule (SUPPRESS vs EMPHASISE) because a store that
  keeps only the keyword applies the opposite instruction: "buang X" and "fokus
  X" reduce to the same token and mean opposite things.

SCHEMA PROVENANCE — READ THIS BEFORE CHANGING A COLUMN
  The live table was created by a parallel session that reached the same design
  independently, and its provenance columns are BETTER than the first version of
  this module: it carries chat_id and platform_message_id (which is what makes
  reply-capture possible at all), plus superseded_by and last_applied_at.

  So this module ADAPTS to that table rather than migrating it. Rewriting
  another agent's schema to match mine would destroy evidence for no gain. The
  differences are bridged in one place, `_row()`, which returns BOTH names for
  each field so older callers keep working:

      their column        alias used here
      id                  fb_id
      status              active   (1 when ACTIVE, 0 otherwise)
      editions_applied    applied_count
      edition             edition_ref

  One column is added additively when missing: `scope` (default 'brief'), so a
  rule can belong to something other than the daily brief later.

REFUSALS ARE RECORDED TOO
  A refused instruction is information: it says the system was asked for
  something and declined. `feedback_refusals` already exists in the live store
  and is written to here, so a refusal is visible rather than vanishing into a
  stderr line.
"""
from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# phrases meaning "stop doing X" — recognised so the derived rule carries the
# negation instead of silently inverting the reader's intent
NEGATIVE = ("buang", "jangan", "henti", "stop", "kurang", "tak payah", "remove",
            "drop", "no more", "don't", "hate", "benci", "tak suka", "dislike",
            "avoid", "elak")
POSITIVE = ("fokus", "focus", "tambah", "add", "lebih", "more", "prioritise",
            "prioritize", "utamakan", "prefer")

CREATE_FEEDBACK = """
CREATE TABLE IF NOT EXISTS feedback (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at          TEXT NOT NULL,
    source              TEXT NOT NULL,
    chat_id             TEXT,
    platform_message_id TEXT,
    edition             TEXT,
    raw_text            TEXT NOT NULL,
    rule                TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'ACTIVE',
    editions_applied    INTEGER NOT NULL DEFAULT 0,
    last_applied_at     TEXT,
    retired_at          TEXT,
    retire_reason       TEXT,
    superseded_by       INTEGER
);
"""
CREATE_REFUSALS = """
CREATE TABLE IF NOT EXISTS feedback_refusals (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    at        TEXT NOT NULL,
    chat_id   TEXT,
    reason    TEXT NOT NULL,
    raw_text  TEXT
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalise(text: str) -> str:
    """Collapse whitespace and strip framing so two phrasings of one instruction
    are comparable. Deliberately conservative: it must never change meaning."""
    t = (text or "").strip()
    t = re.sub(r"^\s*(hermes|arif|888|f13)\s*[:,.!-]\s*", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t)
    return t.strip(" .!,;:")


def derive_rule(raw: str) -> tuple[str, str]:
    """Turn a comment into a standing instruction. Returns (rule, direction)."""
    t = normalise(raw)
    low = t.lower()
    if any(n in low for n in NEGATIVE):
        return f"SUPPRESS: {t}", "suppress"
    if any(p in low for p in POSITIVE):
        return f"EMPHASISE: {t}", "emphasise"
    return f"NOTE: {t}", "note"


def _row(r: sqlite3.Row) -> dict:
    """One compatibility view: both the live column names and the aliases."""
    d = dict(r)
    d.setdefault("fb_id", d.get("id"))
    d["active"] = 1 if str(d.get("status", "")).upper() == "ACTIVE" else 0
    d["applied_count"] = d.get("editions_applied", 0)
    d["edition_ref"] = d.get("edition")
    d.setdefault("scope", "brief")
    return d


class FeedbackStore:
    def __init__(self, db_path: Path | str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(CREATE_FEEDBACK)
        self.conn.executescript(CREATE_REFUSALS)
        self._ensure_scope_column()
        self.conn.commit()

    def _ensure_scope_column(self) -> None:
        cols = {r["name"] for r in self.conn.execute("PRAGMA table_info(feedback)")}
        if "scope" not in cols:
            self.conn.execute(
                "ALTER TABLE feedback ADD COLUMN scope TEXT NOT NULL DEFAULT 'brief'")
            self.conn.commit()

    # ── refusals ────────────────────────────────────────────────────────────

    def _refuse(self, reason: str, raw_text: str = "", chat_id: str | None = None) -> None:
        self.conn.execute(
            "INSERT INTO feedback_refusals (at, chat_id, reason, raw_text) VALUES (?,?,?,?)",
            (utc_now(), chat_id, reason, (raw_text or "")[:2000]))
        self.conn.commit()

    def refusals(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM feedback_refusals ORDER BY id")]

    # ── writes ──────────────────────────────────────────────────────────────

    def add(self, raw_text: str, *, source: str = "telegram_reply",
            edition_ref: str | None = None, scope: str = "brief",
            rule: str | None = None, chat_id: str | None = None,
            message_id: str | None = None) -> dict:
        """Record one piece of feedback. Refuses empty or duplicate input.

        Duplicates are refused rather than stacked: the same instruction given
        twice is not twice as strong, and a list that accumulates copies is a
        list nobody reads.
        """
        raw = (raw_text or "").strip()
        if not raw:
            reason = "empty feedback — nothing to record"
            self._refuse(reason, raw_text, chat_id)
            raise ValueError(reason)
        rule_text = rule or derive_rule(raw)[0]

        existing = self.conn.execute(
            "SELECT id FROM feedback WHERE rule = ? AND status = 'ACTIVE' AND scope = ?",
            (rule_text, scope)).fetchone()
        if existing:
            return {"fb_id": existing["id"], "duplicate": True, "rule": rule_text,
                    "note": "already standing; not recorded twice"}

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO feedback (created_at, source, chat_id, platform_message_id,"
            " edition, raw_text, rule, status, editions_applied)"
            " VALUES (?,?,?,?,?,?,?,'ACTIVE',0)",
            (utc_now(), source, chat_id, message_id, edition_ref, raw, rule_text))
        self.conn.commit()
        return {"fb_id": cur.lastrowid, "duplicate": False, "rule": rule_text,
                "direction": derive_rule(raw)[1], "raw_text": raw}

    def retire(self, fb_id: int, reason: str) -> bool:
        if not reason or not reason.strip():
            msg = ("a retirement needs a reason — an unexplained retirement is "
                   "indistinguishable from a bug")
            self._refuse(msg, f"fb_id={fb_id}")
            raise ValueError(msg)
        cur = self.conn.execute(
            "UPDATE feedback SET status='RETIRED', retired_at=?, retire_reason=?"
            " WHERE id=? AND status='ACTIVE'",
            (utc_now(), reason.strip(), fb_id))
        self.conn.commit()
        return cur.rowcount > 0

    def mark_applied(self, fb_ids: list[int]) -> int:
        if not fb_ids:
            return 0
        q = ("UPDATE feedback SET editions_applied = editions_applied + 1,"
             " last_applied_at = ? WHERE id IN ("
             + ",".join("?" * len(fb_ids)) + ")")
        cur = self.conn.execute(q, [utc_now(), *fb_ids])
        self.conn.commit()
        return cur.rowcount

    # ── reads ───────────────────────────────────────────────────────────────

    def active(self, scope: str | None = "brief") -> list[dict]:
        if scope is None:
            rows = self.conn.execute(
                "SELECT * FROM feedback WHERE status='ACTIVE' ORDER BY id")
        else:
            rows = self.conn.execute(
                "SELECT * FROM feedback WHERE status='ACTIVE' AND scope=? ORDER BY id",
                (scope,))
        return [_row(r) for r in rows]

    def all_rows(self) -> list[dict]:
        return [_row(r) for r in self.conn.execute("SELECT * FROM feedback ORDER BY id")]

    def export_rules(self, out: Path | None = None) -> Path:
        """Write the standing instructions where the build reads them, and count
        the application. The count is the point: a rule that never changes
        anything becomes visible and can be retired."""
        rows = self.active()
        lines = ["# Standing instructions for this brief",
                 "",
                 "Derived from Arif's own comments on previous editions. Each carries",
                 "the raw comment it came from and how long it has been in force.",
                 "A rule with a high count and no visible effect is a candidate for",
                 "retirement.",
                 ""]
        if not rows:
            lines.append("_None standing._")
        for r in rows:
            lines.append(f"- **{r['rule']}**")
            lines.append(f"  - standing since {str(r['created_at'])[:10]}, "
                         f"scope `{r['scope']}`, applied in {r['applied_count']} edition(s)")
            lines.append(f"  - heard as: \"{r['raw_text']}\""
                         + (f" (re: {r['edition_ref']})" if r["edition_ref"] else ""))
        out = Path(out) if out else self.path.parent / "brief-rules.md"
        out.write_text("\n".join(lines) + "\n")
        self.mark_applied([r["fb_id"] for r in rows])
        return out


# ── best-effort capture ──────────────────────────────────────────────────────

def capture_candidates(text: str) -> list[str]:
    """Pull instruction-shaped lines out of a message.

    Conservative on purpose: it returns candidates for a decision, not rules. A
    line qualifies only when it is short and contains a directive verb — a long
    paragraph about the news is not feedback about the format, and treating it
    as such is how a system starts obeying noise.
    """
    out: list[str] = []
    for line in (text or "").splitlines():
        s = normalise(line)
        if not s or len(s) > 200:
            continue
        low = s.lower()
        if any(d in low for d in NEGATIVE + POSITIVE):
            out.append(s)
    return out
