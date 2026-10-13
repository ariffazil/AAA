#!/usr/bin/env python3
"""attention_debt_daily.py — count [C:*]-tagged human correction turns (convention v1,
/root/AAA/instructions/correction-ledger-convention.md). Read-only over state.db.
Usage: python3 attention_debt_daily.py [--date YYYY-MM-DD]  (default: today UTC)
Output: JSON {date, total, by_cause, turns:[{ts, cause, excerpt}]}
NOTE: counts ONLY tagged turns. Undercount is honest; heuristic guessing is HARAM (F2).
"""

import json, re, sqlite3, sys, datetime

CAUSES = {"c": "confabulation", "p": "phantom_work", "a": "permission_ask", "i": "intent_drift", "o": "other"}
TAG = re.compile(r"^\s*\[C:([cpaio])\]", re.I)


def main():
    date = (
        sys.argv[sys.argv.index("--date") + 1]
        if "--date" in sys.argv
        else datetime.datetime.utcnow().strftime("%Y-%m-%d")
    )
    db = sqlite3.connect("/root/.hermes/state.db")
    rows = db.execute(
        "SELECT timestamp, content FROM messages WHERE role IN ('human','user') AND content LIKE '[C:%' "
        "AND substr(timestamp,1,10)=? ORDER BY timestamp",
        (date,),
    ).fetchall()
    turns, by = [], {v: 0 for v in CAUSES.values()}
    for ts, content in rows:
        m = TAG.match(content or "")
        if not m:
            continue
        cause = CAUSES.get(m.group(1).lower(), "other")
        by[cause] += 1
        turns.append({"ts": ts, "cause": cause, "excerpt": re.sub(r"\s+", " ", content[:90])})
    out = {
        "date": date,
        "total": len(turns),
        "by_cause": by,
        "note": "tagged-only count (convention v1); F13-class turns excluded by definition",
        "turns": turns[:50],
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
