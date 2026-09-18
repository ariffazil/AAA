#!/usr/bin/env python3
"""docforge.feedback — the loop that makes tomorrow's brief different because of today's comment.

THE PROBLEM
  A briefing that ignores what the reader said about yesterday's briefing is not
  stateful, it is just scheduled. The reader's correction is the highest-quality
  signal in the whole system — it is the one input that is unambiguously about
  what he actually wants — and without a place to put it, it evaporates into a
  chat message.

WHAT THIS IS NOT
  This is NOT an automatic prompt-rewriter. A comment in chat is RAW MATERIAL,
  not a rule: "buang naratif politik ni" said once after a bad week is an
  observation, and turning it into a permanent filter would be the machine
  obeying a mood. So:

      raw_text  what he actually said, preserved verbatim, never edited
      rule      the standing instruction DERIVED from it, reviewable
      active    whether it is in force

  The rule is derived, shown, and reversible. The raw text is the evidence the
  rule came from. Keeping both is what makes the loop auditable rather than
  mysterious.

WHY IT LIVES IN THE SAME SQLITE FILE
  The delta engine already answers "what did I record for claim X". Feedback is
  the same shape of question — "what standing instruction did he give me, and is
  it still in force" — so it belongs in the same authority store, not in a
  second database that can drift out of sync with it.

APPLICATION IS EXPLICIT
  `export_rules()` writes the active rules where the build reads them, and the
  count of editions each rule has influenced is incremented when it is exported
  for use. A rule that has been active for 40 editions and changed nothing is
  visible as such, which is how a dead rule gets noticed and retired.
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback (
    fb_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at    TEXT NOT NULL,
    source        TEXT NOT NULL,
    edition_ref   TEXT,
    raw_text      TEXT NOT NULL,
    rule          TEXT NOT NULL,
    scope         TEXT NOT NULL DEFAULT 'brief',
    active        INTEGER NOT NULL DEFAULT 1,
    applied_count INTEGER NOT NULL DEFAULT 0,
    retired_at    TEXT,
    retire_reason TEXT
);
CREATE INDEX IF NOT EXISTS idx_fb_active ON feedback(active, scope);
"""

# phrases that mean "stop doing X" — recognised so the derived rule carries the
# negation instead of silently inverting the reader's intent
NEGATIVE = ("buang", "jangan", "henti", "stop", "kurang", "tak payah", "remove",
            "drop", "no more", "don't")
# phrases that mean "do more of X"
POSITIVE = ("fokus", "focus", "tambah", "add", "lebih", "more", "prioritise",
            "prioritize", "utamakan")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalise(text: str) -> str:
    """Collapse whitespace and strip framing so two phrasings of one instruction
    are comparable. Deliberately conservative: it must never change the meaning."""
    t = (text or "").strip()
    t = re.sub(r"^\s*(hermes|arif|888|f13)\s*[:,.!-]\s*", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t)
    return t.strip(" .!,;:")


def derive_rule(raw: str) -> tuple[str, str]:
    """Turn a comment into a standing instruction. Returns (rule, direction).

    The direction is recorded because 'focus on X' and 'drop X' are opposite
    instructions and a system that stores only the keyword X will apply the
    wrong one.
    """
    t = normalise(raw)
    low = t.lower()
    if any(n in low for n in NEGATIVE):
        return f"SUPPRESS: {t}", "suppress"
    if any(p in low for p in POSITIVE):
        return f"EMPHASISE: {t}", "emphasise"
    return f"NOTE: {t}", "note"


class FeedbackStore:
    def __init__(self, db_path: Path | str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    # ── writes ──────────────────────────────────────────────────────────────

    def add(self, raw_text: str, *, source: str = "telegram_reply",
            edition_ref: str | None = None, scope: str = "brief",
            rule: str | None = None) -> dict:
        """Record one piece of feedback. Refuses an empty or duplicate rule.

        Duplicates are refused rather than silently stacked because the same
        instruction given twice is not twice as strong, and a list that can
        accumulate copies is a list nobody can read.
        """
        raw = (raw_text or "").strip()
        if not raw:
            raise ValueError("empty feedback — nothing to record")
        rule_text = rule or derive_rule(raw)[0]

        existing = self.conn.execute(
            "SELECT fb_id FROM feedback WHERE rule = ? AND active = 1 AND scope = ?",
            (rule_text, scope)).fetchone()
        if existing:
            return {"fb_id": existing["fb_id"], "duplicate": True,
                    "rule": rule_text,
                    "note": "already standing; not recorded twice"}

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO feedback (created_at, source, edition_ref, raw_text, rule,"
            " scope, active, applied_count) VALUES (?,?,?,?,?,?,1,0)",
            (utc_now(), source, edition_ref, raw, rule_text, scope))
        self.conn.commit()
        return {"fb_id": cur.lastrowid, "duplicate": False, "rule": rule_text,
                "direction": derive_rule(raw)[1], "raw_text": raw}

    def retire(self, fb_id: int, reason: str) -> bool:
        if not reason or not reason.strip():
            raise ValueError("a retirement needs a reason — an unexplained "
                             "retirement is indistinguishable from a bug")
        cur = self.conn.execute(
            "UPDATE feedback SET active = 0, retired_at = ?, retire_reason = ?"
            " WHERE fb_id = ? AND active = 1",
            (utc_now(), reason.strip(), fb_id))
        self.conn.commit()
        return cur.rowcount > 0

    def mark_applied(self, fb_ids: list[int]) -> int:
        if not fb_ids:
            return 0
        q = ("UPDATE feedback SET applied_count = applied_count + 1 WHERE fb_id IN ("
             + ",".join("?" * len(fb_ids)) + ")")
        cur = self.conn.execute(q, fb_ids)
        self.conn.commit()
        return cur.rowcount

    # ── reads ───────────────────────────────────────────────────────────────

    def active(self, scope: str = "brief") -> list[dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM feedback WHERE active = 1 AND scope = ?"
            " ORDER BY fb_id", (scope,))]

    def all_rows(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM feedback ORDER BY fb_id")]

    def export_rules(self, out: Path | None = None) -> Path:
        """Write the standing instructions where the build reads them, and count
        the application. The count is the point: a rule that never changes
        anything becomes visible and can be retired."""
        rows = self.active()
        lines = ["# Standing instructions for this brief",
                 "",
                 "Derived from Arif's own comments on previous editions.",
                 "Each carries the raw comment it came from and how long it has",
                 "been in force. A rule with a high count and no visible effect",
                 "is a candidate for retirement.",
                 ""]
        if not rows:
            lines.append("_None standing._")
        for r in rows:
            lines.append(f"- **{r['rule']}**")
            lines.append(f"  - standing since {r['created_at'][:10]}, scope `{r['scope']}`, "
                         f"applied in {r['applied_count']} edition(s)")
            lines.append(f"  - heard as: \"{r['raw_text']}\""
                         + (f" (re: {r['edition_ref']})" if r["edition_ref"] else ""))
        out = Path(out) if out else self.path.parent / "brief-rules.md"
        out.write_text("\n".join(lines) + "\n")
        self.mark_applied([r["fb_id"] for r in rows])
        return out


# ── best-effort capture ──────────────────────────────────────────────────────

REPLY_MARKERS = ("brief", "briefing", "edition", "pdf")


def capture_candidates(text: str) -> list[str]:
    """Pull instruction-shaped lines out of a message.

    Conservative on purpose: it returns candidates for a HUMAN-SHAPED decision,
    not rules. A message is a candidate only when it is short and contains a
    directive verb — a long paragraph about the news is not feedback about the
    format, and treating it as such is how a system starts obeying noise.
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
