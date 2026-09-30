#!/usr/bin/env python3
"""eureka-analytics.py — Eureka Ledger analytics v0 (Wave A Track 2 · 2026-09-30)
Answers the sovereign's questions empirically:
  Apa dipelajari? Bila? Oleh siapa? Kekal? Prestasi naik?

Read-only. Sources: /root/AAA/canon/eureka-entries.jsonl + /root/AAA/eurekas/eureka-entries.jsonl
+ canon EUREKA-*.md reconciliation. Prints JSON report; no writes, no new ledger.
"""

import json, re, sys
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

SOURCES = [
    Path("/root/AAA/canon/eureka-entries.jsonl"),
    Path("/root/AAA/eurekas/eureka-entries.jsonl"),
]
CANON_DIR = Path("/root/AAA/canon")


def load():
    seen, entries = set(), []
    for src in SOURCES:
        if not src.exists():
            continue
        for line in src.read_text(errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except:
                continue
            eid = e.get("id") or f"{e.get('title', '')[:40]}{e.get('timestamp', '')}"
            if eid in seen:
                continue
            seen.add(eid)
            entries.append(e)
    return entries


def parse_ts(e):
    ts = e.get("timestamp") or e.get("seal_timestamp") or ""
    m = re.match(r"(\d{4}-\d{2}-\d{2})", ts)
    return m.group(1) if m else None


def main():
    entries = load()

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "sources": [str(s) for s in SOURCES if s.exists()],
        "unique_entries": len(entries),
        "by_type": dict(Counter(e.get("type", "?") for e in entries)),
        "by_status": dict(Counter(e.get("status") or "UNSET" for e in entries)),
    }

    # temporal: eurekas per week (last 8 weeks + trend)
    dated = [(parse_ts(e), e) for e in entries]
    dated = [(d, e) for d, e in dated if d]
    report["dated_entries"] = len(dated)
    weeks = Counter(d[:10] for d, _ in dated)  # rough by-day first
    days = sorted(weeks)
    if days:
        report["first_entry"] = days[0]
        report["last_entry"] = days[-1]
        # last 14 days activity
        from datetime import date, timedelta

        today = date.today()
        recent = sum(c for d, c in weeks.items() if (today - date.fromisoformat(d)).days <= 14)
        older = sum(c for d, c in weeks.items() if 14 < (today - date.fromisoformat(d)).days <= 28)
        report["entries_last_14d"] = recent
        report["entries_prev_14d"] = older
        report["learning_signal"] = "ACTIVE" if recent > 0 else "STALLED" if older > 0 else "DORMANT"

    # ratified vs pending (kekal?)
    ratified = sum(1 for e in entries if str(e.get("status", "")).startswith(("F13", "RATIFIED")))
    pending = sum(
        1
        for e in entries
        if "PENDING" in str(e.get("status", "")).upper() or "CANDIDATE" in str(e.get("status", "")).upper()
    )
    report["ratified"] = ratified
    report["pending_f13"] = pending
    report["ratification_ratio"] = round(ratified / max(1, ratified + pending), 2)

    # reconciliation: canon EUREKA-*.md files without a ledger entry
    canon_files = {f.stem: f.name for f in CANON_DIR.glob("EUREKA-*.md")}
    entry_ids = " ".join(str(e.get("id", "")) + " " + str(e.get("title", "")) for e in entries)
    # match by date-slug fragment
    orphan_canon = []
    for stem, fname in canon_files.items():
        # extract date + key words
        m = re.search(r"(2026-\d{2}-\d{2})", stem)
        frag = m.group(1) if m else stem[:20]
        words = [w for w in re.split(r"[-_]", stem) if len(w) > 4][:3]
        hit = frag in entry_ids or any(w in entry_ids for w in words)
        if not hit:
            orphan_canon.append(fname)
    report["canon_eureka_docs"] = len(canon_files)
    report["canon_docs_without_ledger_entry"] = orphan_canon[:20]

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
