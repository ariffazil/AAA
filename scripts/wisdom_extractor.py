#!/usr/bin/env python3
"""
Wisdom Extractor — Session chat logs → actionable memory
=========================================================
Extracts decisions, corrections, patterns, eurekas, and relationship insights
from Hermes session history via direct SQLite access (state.db with FTS5).

Usage:
  python3 /root/AAA/scripts/wisdom_extractor.py
  python3 /root/AAA/scripts/wisdom_extractor.py --topic "Syed relationship"
  python3 /root/AAA/scripts/wisdom_extractor.py --user-id 1042200555
  python3 /root/AAA/scripts/wisdom_extractor.py --last-n 10
  python3 /root/AAA/scripts/wisdom_extractor.py --topic "voice cloning" --apply
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

DB_PATH = os.path.expanduser("~/.hermes/state.db")
MEMORIES_DIR = os.path.expanduser("~/.hermes/memories/")

# ── Classification ──────────────────────────────────────────────────────

def classify_wisdom(content_lower):
    """Classify wisdom content into appropriate storage layer."""
    # User-specific info → USER profile
    if any(kw in content_lower for kw in [
        "arif prefer", "arif said", "arif hates", "arif likes", "arif wants",
        "ariffazil", "petronas", "geologist", "penang", "bayan lepas"
    ]):
        return "USER"

    # Relationship content → MEMORY (relationship layer)
    if any(kw in content_lower for kw in [
        "syed", "nabilah", "adik", "mak ", "ayah", "family",
        "khairuddin", "rico_ricaldo", "anis"
    ]):
        return "RELATIONSHIP"

    # Corrections/failures → SCAR
    if any(kw in content_lower for kw in [
        "salah", "wrong", "bukan", "x betul", "tak guna", "bodoh", "hang pi",
        "should have", "don't do", "never do", "stop doing", "mistake",
        "failed", "error", "broke", "correction"
    ]):
        return "SCAR"

    # Reusable procedures → SKILL candidate
    if any(kw in content_lower for kw in [
        "how to", "steps", "procedure", "runbook", "pipeline",
        "workflow", "command", "install", "setup", "deploy",
        "cara nak", "macam mana"
    ]):
        return "SKILL"

    # Environment/tool facts → MEMORY
    if any(kw in content_lower for kw in [
        "tool ", "command", "path ", "port ", "config", "endpoint",
        "api ", "key ", "token", "env ", "version"
    ]):
        return "MEMORY"

    # Decisions → MEMORY
    if any(kw in content_lower for kw in [
        "putus", "decide", "confirm", "approve", "setuju", "go ahead", "jalan"
    ]):
        return "DECISION"

    return "MEMORY"


# ── Pattern Detection ───────────────────────────────────────────────────

PATTERNS = {
    "decision": {
        "keywords": ["putus", "decide", "confirm", "approve", "setuju",
                      "go ahead", "jalan", "okay do it", "yes do"],
        "label": "DECISION",
        "store": "MEMORY",
    },
    "scar": {
        "keywords": ["salah", "wrong", "bukan", "x betul", "tak guna",
                      "bodoh", "hang pi", "should have", "don't do",
                      "never do", "stop doing", "mistake"],
        "label": "CORRECTION",
        "store": "SCAR",
    },
    "relationship": {
        "keywords": ["syed", "nabilah", "adik", "mak ", "ayah", "family",
                      "khairuddin", "rico_ricaldo"],
        "label": "RELATIONSHIP",
        "store": "MEMORY",
    },
    "skill": {
        "keywords": ["how to", "steps", "procedure", "runbook", "pipeline",
                      "workflow", "cara nak", "macam mana"],
        "label": "PROCEDURE",
        "store": "SKILL",
    },
    "eureka": {
        "keywords": ["found it", "it works", "berjaya", "finally",
                      "the fix", "the trick", "solution"],
        "label": "EUREKA",
        "store": "SKILL",
    },
}


def detect_patterns(content_lower):
    """Detect all pattern matches in content."""
    matches = []
    for pattern_name, pattern in PATTERNS.items():
        for kw in pattern["keywords"]:
            if kw in content_lower:
                matches.append({
                    "pattern": pattern_name,
                    "label": pattern["label"],
                    "store": pattern["store"],
                    "keyword": kw,
                })
                break  # One match per pattern
    return matches


# ── DB Queries ──────────────────────────────────────────────────────────

def get_db():
    """Open the state DB, return connection."""
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] DB not found at {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_sessions(conn, user_id=None, last_n=None, limit=50, topic=None):
    """Get sessions from DB with optional filters."""
    where = []
    params = []

    if user_id:
        where.append("session_key LIKE ?")
        params.append(f"%:{user_id}")

    if last_n:
        # Get last N session IDs first
        recent_ids = conn.execute(
            "SELECT id FROM sessions ORDER BY last_activity_at DESC LIMIT ?",
            (last_n,)
        ).fetchall()
        id_list = [r["id"] for r in recent_ids]
        if id_list:
            placeholders = ",".join("?" * len(id_list))
            where.append(f"id IN ({placeholders})")
            params.extend(id_list)

    if topic:
        # Use FTS5 to find sessions with matching messages
        try:
            ft_ids = conn.execute(
                "SELECT DISTINCT session_id FROM messages_fts WHERE messages_fts MATCH ? LIMIT 200",
                (topic.replace("'", "''"),)
            ).fetchall()
            id_list = [r["session_id"] for r in ft_ids]
            if id_list:
                placeholders = ",".join("?" * len(id_list))
                where.append(f"id IN ({placeholders})")
                params.extend(id_list)
            elif not where:
                # FTS5 returned nothing, fall back to title search
                where.append("title LIKE ?")
                params.append(f"%{topic}%")
        except Exception:
            where.append("title LIKE ?")
            params.append(f"%{topic}%")

    where_sql = " AND ".join(where) if where else "1=1"
    sql = f"SELECT * FROM sessions WHERE {where_sql} ORDER BY last_activity_at DESC LIMIT {limit}"
    sessions = [dict(r) for r in conn.execute(sql, params).fetchall()]
    return sessions


def get_messages(conn, session_id, max_messages=100):
    """Get messages for a session, prioritizing user messages."""
    # Get user messages first (most valuable for wisdom)
    rows = conn.execute(
        "SELECT role, content, timestamp, tool_name, reasoning "
        "FROM messages WHERE session_id = ? AND role IN ('user', 'assistant') "
        "ORDER BY timestamp DESC LIMIT ?",
        (session_id, max_messages)
    ).fetchall()
    return [dict(r) for r in rows]

def extract_wisdom(messages, session_title, session_id, session_key):
    """Extract wisdom items from messages."""
    items = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role != "user" or len(content) < 20:
            continue

        content_lower = content.lower()
        patterns = detect_patterns(content_lower)

        for pat in patterns:
            item = {
                "type": pat["label"],
                "store": pat["store"],
                "content": content[:300],
                "source_session": session_id[:16],
                "source_title": session_title[:50],
                "source_key": session_key[:60],
                "keyword": pat["keyword"],
                "confidence": 0.75 if pat["store"] == "SCAR" else 0.6,
                "timestamp": msg.get("timestamp", ""),
            }
            items.append(item)

    return items


# ── Report ──────────────────────────────────────────────────────────────

def generate_report(all_wisdom, session_count, topic=None):
    """Generate summary report."""
    by_type = {}
    by_store = {}
    for item in all_wisdom:
        t = item["type"]
        s = item["store"]
        by_type[t] = by_type.get(t, 0) + 1
        by_store[s] = by_store.get(s, 0) + 1

    return {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "sessions_analyzed": session_count,
        "total_wisdom_items": len(all_wisdom),
        "by_type": by_type,
        "by_store": by_store,
        "items": all_wisdom,
    }


# ── Main ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Wisdom Extractor — session logs → actionable memory"
    )
    parser.add_argument("--topic", help="Search topic/query")
    parser.add_argument("--user-id", help="Filter by Telegram user ID")
    parser.add_argument("--last-n", type=int, help="Analyze last N sessions")
    parser.add_argument("--limit", type=int, default=30, help="Max sessions")
    parser.add_argument("--max-msgs", type=int, default=50,
                        help="Max messages per session (default 50)")
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    parser.add_argument("--apply", action="store_true",
                        help="Write extracted wisdom to memory files")
    parser.add_argument("--scan-only", action="store_true",
                        help="Only list sessions, don't extract")
    args = parser.parse_args()

    print("=" * 70)
    print(" WISDOM EXTRACTOR — Session Logs → Actionable Memory")
    print("=" * 70)
    print()

    conn = get_db()

    # Step 1: Get sessions
    topic_label = args.topic or "all sessions"
    print(f"[1/5] Loading sessions ({topic_label})...")
    sessions = get_sessions(conn, user_id=args.user_id, last_n=args.last_n,
                            limit=args.limit, topic=args.topic)
    print(f"  Found {len(sessions)} sessions")

    if args.scan_only:
        for s in sessions[:15]:
            sid = s["id"][:16]
            title = (s.get("title") or "—")[:45]
            msgs = s.get("message_count", 0)
            tokens = s.get("total_tokens", 0)
            cost = s.get("estimated_cost_usd", 0)
            updated = (s.get("last_activity_at") or "?")[:19]
            print(f"  {sid} | {title:45s} | {msgs:>4} msgs | {tokens:>8,} tok | ${cost:.2f} | {updated}")
        conn.close()
        return

    # Step 2: Extract wisdom from messages
    print(f"\n[2/5] Extracting wisdom from messages...")
    all_wisdom = []
    sessions_with_wisdom = 0
    for sess in sessions:
        sid = sess["id"]
        title = sess.get("title") or "untitled"
        skey = sess.get("session_key", "")
        msgs = get_messages(conn, sid, max_messages=args.max_msgs)

        if not msgs:
            continue

        items = extract_wisdom(msgs, title, sid, skey)
        if items:
            sessions_with_wisdom += 1
            all_wisdom.extend(items)

    print(f"  {len(all_wisdom)} wisdom items from {sessions_with_wisdom}/{len(sessions)} sessions")

    # Step 3: FTS5 deep search if topic given
    if args.topic:
        print(f"\n[3/5] FTS5 deep search: '{args.topic}'...")
        try:
            # FTS5 table doesn't have session_id directly - match content, get docid, join to messages
            ft_rows = conn.execute(
                "SELECT DISTINCT m.session_id FROM messages_fts f "
                "JOIN messages m ON m.rowid = f.rowid "
                "WHERE f.content MATCH ? LIMIT 100",
                (args.topic.replace("'", "''"),)
            ).fetchall()
            ft_sids = [r["session_id"] for r in ft_rows]

            # Get sessions we haven't analyzed yet
            existing_sids = {s["id"] for s in sessions}
            new_sids = [sid for sid in ft_sids if sid not in existing_sids]

            if new_sids:
                print(f"  Found {len(new_sids)} additional sessions via FTS5")
                for sid in new_sids[:5]:
                    # Get session info
                    sess_row = conn.execute(
                        "SELECT id, title, session_key FROM sessions WHERE id = ?",
                        (sid,)
                    ).fetchone()
                    if sess_row:
                        msgs = get_messages(conn, sid, max_messages=args.max_msgs)
                        items = extract_wisdom(msgs, sess_row["title"] or "ft", sid, sess_row["session_key"])
                        all_wisdom.extend(items)
                        if items:
                            sessions_with_wisdom += 1
            else:
                print("  No additional sessions found")
        except Exception as e:
            print(f"  FTS5 search error: {e}")
    else:
        print("\n[3/5] Skipping FTS5 (no topic)")

    # Step 4: Classify
    print(f"\n[4/5] Classification:")
    by_type = {}
    by_store = {}
    for item in all_wisdom:
        t = item["type"]
        s = item["store"]
        by_type[t] = by_type.get(t, 0) + 1
        by_store[s] = by_store.get(s, 0) + 1

    for t, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")
    print(f"  Storage targets: {by_store}")

    # Step 5: Report
    print("\n[5/5] Report...")
    report = generate_report(all_wisdom, len(sessions), args.topic)

    output_json = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"  Saved to {args.output}")
    else:
        print()
        # Print summary + first few items
        print(f"Summary: {len(all_wisdom)} items, {sessions_with_wisdom} sessions")
        for item in all_wisdom[:10]:
            print(f"  [{item['type']:14s}] [{item['store']:10s}] "
                  f"k='{item['keyword']}' | {item['content'][:100]}...")
        if len(all_wisdom) > 10:
            print(f"  ... and {len(all_wisdom) - 10} more")

    # Optional: apply to memory
    if args.apply:
        print("\n[APPLY] Writing to memory files...")
        # Group by store type
        by_store_items = {}
        for item in all_wisdom:
            s = item["store"]
            by_store_items.setdefault(s, []).append(item)

        for store_type, items in by_store_items.items():
            target = os.path.join(MEMORIES_DIR, f"WISDOM-{store_type}.md")
            with open(target, "a") as f:
                f.write(f"\n## {store_type} Wisdom — {datetime.now().strftime('%Y-%m-%d')}\n\n")
                for item in items:
                    f.write(f"- [{item['type']}] (from: {item['source_title'][:30]}) "
                            f"k='{item['keyword']}': {item['content'][:200]}\n")
            print(f"  Appended {len(items)} items → {target}")

    print()
    print("=" * 70)
    print(f" DONE — {len(all_wisdom)} wisdom items extracted")
    print("=" * 70)

    conn.close()


if __name__ == "__main__":
    main()
