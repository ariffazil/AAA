#!/usr/bin/env python3
"""Deterministic measures for a relationship audit. Offline: no network, no credentials.

Usage:
    python3 relationship_measures.py CHAT.txt
    python3 relationship_measures.py CHAT.txt --a ARIFFAZIL --b "Syed Kudin" \\
        --count "worship:worship" --count "affection:sayang,rindu,love" \\
        --count "contact-check:busy ka,pi mana,senyap"

With --a/--b omitted, the two most frequent senders are used and reported.

Emits JSON on stdout: per-sender volume, active days and who opened each, the largest silences
in EACH party's own posting plus who broke them, per-sender media count, and a directional
token count per --count group (both sides, always).

Design notes that matter:
  * A message line is a timestamped line matching PREFIX; continuation lines are appended to the
    previous message so multi-line messages are not lost.
  * Invalid dates are skipped rather than raising, because exports contain malformed rows.
  * Word-boundary matching is used for tokens so a short token does not fire inside a longer word.
  * Directional counts are returned as a pair. Never report one side alone.
"""
import argparse
import collections
import datetime
import json
import re
import sys

PREFIX = re.compile(
    r"^(\d{1,2})/(\d{1,2})/(\d{2,4}),\s*(\d{1,2}):(\d{2})\s*([AP]M)?\s*-\s*([^:]{1,40}):\s?(.*)$",
    re.IGNORECASE,
)
OMITTED = ("<media omitted>", "<media", "image omitted", "video omitted", "audio omitted")


def parse(path):
    msgs = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m = PREFIX.match(line)
            if m:
                day, mon, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
                if not (1 <= day <= 31 and 1 <= mon <= 12):
                    continue
                if yr < 100:
                    yr += 2000
                hour = int(m.group(4)) % 12
                if (m.group(5) or "").upper() == "PM":
                    hour += 12
                try:
                    stamp = datetime.datetime(yr, mon, day, hour, int(m.group(6)))
                except ValueError:
                    continue
                msgs.append({"dt": stamp, "who": m.group(7).strip(), "txt": m.group(8)})
            elif msgs and line.strip():
                msgs[-1]["txt"] += " " + line.strip()
    msgs.sort(key=lambda x: x["dt"])
    return msgs


def top_senders(msgs, n=2):
    counts = collections.Counter(m["who"] for m in msgs)
    return [name for name, _ in counts.most_common(n)]


def side_of(who, a, b):
    if who == a:
        return "A"
    if who == b:
        return "B"
    return None


def active_days(msgs, a, b):
    days = collections.OrderedDict()
    for m in msgs:
        s = side_of(m["who"], a, b)
        if s:
            days.setdefault(m["dt"].date(), []).append(s)
    opened = collections.Counter()
    total = 0
    for _, sides in days.items():
        if len(sides) >= 2:
            total += 1
            opened[sides[0]] += 1
    return total, dict(opened)


def silences(msgs, side, a, b, top=5):
    """Largest gaps in ONE side's own posting, and who sent the next message after each."""
    mine = [m for m in msgs if side_of(m["who"], a, b) == side]
    gaps = []
    for prev, nxt in zip(mine, mine[1:]):
        hours = (nxt["dt"] - prev["dt"]).total_seconds() / 3600.0
        after = [m for m in msgs if m["dt"] > prev["dt"]]
        if after:
            head = after[0]
            breaker = side_of(head["who"], a, b) or "other"
            text = head["txt"][:80]
        else:
            breaker, text = None, None
        gaps.append({
            "days": round(hours / 24.0, 1),
            "from": prev["dt"].strftime("%Y-%m-%d"),
            "to": nxt["dt"].strftime("%Y-%m-%d"),
            "first_back": breaker,
            "first_back_text": text,
        })
    gaps.sort(key=lambda g: -g["days"])
    return gaps[:top]


def media_count(msgs, side, a, b):
    return sum(
        1 for m in msgs
        if side_of(m["who"], a, b) == side
        and any(tag in m["txt"].lower() for tag in OMITTED)
    )


def directional_tokens(msgs, groups, a, b):
    out = {}
    for label, words in groups.items():
        rx = re.compile(
            r"\b(" + "|".join(re.escape(w) for w in words) + r")\b", re.IGNORECASE
        )
        tally = collections.Counter()
        samples = {"A": [], "B": []}
        for m in msgs:
            s = side_of(m["who"], a, b)
            if s and rx.search(m["txt"]):
                tally[s] += 1
                if len(samples[s]) < 3:
                    samples[s].append(
                        {"date": m["dt"].strftime("%Y-%m-%d"), "text": m["txt"][:110]}
                    )
        out[label] = {"A": tally["A"], "B": tally["B"], "samples": samples}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("chat")
    ap.add_argument("--a", help="exact sender label for party A (default: most frequent)")
    ap.add_argument("--b", help="exact sender label for party B (default: second most frequent)")
    ap.add_argument(
        "--count", action="append", default=[], metavar="LABEL:tok1,tok2",
        help="token group; counted in BOTH directions",
    )
    args = ap.parse_args(argv)

    msgs = parse(args.chat)
    if not msgs:
        print(json.dumps({"error": "no messages parsed", "path": args.chat}), indent=1)
        return 1

    a, b = args.a, args.b
    if not (a and b):
        auto = top_senders(msgs, 2)
        a = a or auto[0]
        b = b or (auto[1] if len(auto) > 1 else None)
    if not b:
        print(json.dumps({"error": "need two senders", "senders": top_senders(msgs, 5)}), indent=1)
        return 1

    groups = {}
    for spec in args.count:
        if ":" not in spec:
            continue
        label, words = spec.split(":", 1)
        groups[label] = [w.strip() for w in words.split(",") if w.strip()]

    total_days, opened = active_days(msgs, a, b)
    result = {
        "path": args.chat,
        "party_A": a,
        "party_B": b,
        "span": [msgs[0]["dt"].strftime("%Y-%m-%d"), msgs[-1]["dt"].strftime("%Y-%m-%d")],
        "total_messages": len(msgs),
        "volume": dict(collections.Counter(
            side_of(m["who"], a, b) for m in msgs if side_of(m["who"], a, b)
        )),
        "active_days": total_days,
        "days_opened_by": opened,
        "media_by_side": {"A": media_count(msgs, "A", a, b), "B": media_count(msgs, "B", a, b)},
        "longest_silences_A": silences(msgs, "A", a, b),
        "longest_silences_B": silences(msgs, "B", a, b),
        "directional_tokens": directional_tokens(msgs, groups, a, b),
        "other_senders": [
            [name, n] for name, n in collections.Counter(
                m["who"] for m in msgs
            ).most_common()
            if name not in (a, b)
        ][:8],
    }
    print(json.dumps(result, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
