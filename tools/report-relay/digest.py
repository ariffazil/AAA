#!/usr/bin/env python3
"""
digest — flush the queued human-lane messages into ONE Telegram message.

The relay never pings the sovereign for P2/P3. They land in pending.jsonl.
This script turns the queue into a single readable digest and sends it once,
so attention is spent on a batch instead of bleeding on every notification.

Design:
  - one message, grouped by severity then source
  - bounded: max 12 distinct findings, longest bodies trimmed
  - the queue is only cleared AFTER Telegram confirms, so a failed send
    re-tries next run instead of silently dropping the batch
  - --dry-run prints exactly what would be sent, sends nothing

Run: python3 digest.py [--dry-run] [--max 12]
Timer: report-digest.timer (3x daily)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from collections import OrderedDict
from datetime import datetime, timezone

BASE = os.environ.get("RELAY_BASE", "/var/log/report-relay")
PENDING = os.path.join(BASE, "pending.jsonl")
ARCHIVE = os.path.join(BASE, "pending-archive.jsonl")
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("RELAY_CHAT_ID", "267378578")
TG_LIMIT = 3900

SEV_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
SEV_LABEL = {"P0": "🔴 P0", "P1": "🟠 P1", "P2": "🟡 P2", "P3": "🟢 P3"}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load() -> list[dict]:
    if not os.path.exists(PENDING):
        return []
    with open(PENDING, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def trim(text: str, n: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def build(rows: list[dict], max_items: int) -> str:
    rows = sorted(rows, key=lambda r: (SEV_ORDER.get(r.get("severity", "P3"), 3), r.get("ts", "")))
    shown = rows[:max_items]
    rest = len(rows) - len(shown)

    now = datetime.now(timezone.utc).astimezone()
    counts = {}
    for r in rows:
        counts[r.get("severity", "P3")] = counts.get(r.get("severity", "P3"), 0) + 1
    tally = " · ".join(f"{SEV_LABEL.get(s, s)} {counts[s]}" for s in sorted(counts, key=lambda s: SEV_ORDER.get(s, 9)))

    out = [f"<b>Digest</b> · {now.strftime('%a %d %b %H:%M %Z')}", tally, ""]

    grouped: "OrderedDict[str, list[dict]]" = OrderedDict()
    for r in shown:
        grouped.setdefault(r.get("severity", "P3"), []).append(r)

    for sev, items in grouped.items():
        out.append(f"<b>{SEV_LABEL.get(sev, sev)}</b>")
        for r in items:
            src = r.get("source", "?")
            out.append(f"• <b>{esc(trim(r.get('title','(no title)'), 90))}</b>  <code>{esc(src)}</code>")
            body = trim(r.get("body", ""), 300)
            if body:
                out.append(f"   {esc(body)}")
        out.append("")

    if rest:
        out.append(f"… and {rest} more queued (see /var/log/report-relay/pending.jsonl)")
    text = "\n".join(out).strip()
    if len(text) > TG_LIMIT:
        text = text[: TG_LIMIT - 30].rstrip() + "\n\n… [digest truncated]"
    return text


def send(text: str) -> tuple[bool, str]:
    if not TG_TOKEN:
        return False, "TELEGRAM_BOT_TOKEN not configured"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID, "text": text, "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            payload = json.loads(r.read().decode())
    except Exception as e:  # noqa: BLE001
        return False, f"{e.__class__.__name__}: {e}"
    if not payload.get("ok"):
        return False, payload.get("description", "unknown")
    return True, str(payload.get("result", {}).get("message_id", ""))


def main() -> int:
    dry = "--dry-run" in sys.argv
    max_items = 12
    if "--max" in sys.argv:
        try:
            max_items = max(1, int(sys.argv[sys.argv.index("--max") + 1]))
        except (IndexError, ValueError):
            pass

    rows = load()
    if not rows:
        print("digest: queue empty, nothing sent")
        return 0

    text = build(rows, max_items)
    if dry:
        print(text)
        print(f"\n[--dry-run] {len(rows)} queued item(s); nothing sent, queue untouched")
        return 0

    ok, detail = send(text)
    if not ok:
        print(f"digest: NOT SENT ({detail}) — {len(rows)} item(s) kept in queue")
        return 1

    os.makedirs(os.path.dirname(ARCHIVE), exist_ok=True)
    with open(ARCHIVE, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({**r, "digested_at": datetime.now(timezone.utc).isoformat()},
                               ensure_ascii=False) + "\n")
    open(PENDING, "w").close()
    print(f"digest: sent {len(rows)} item(s) as one message, id={detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
