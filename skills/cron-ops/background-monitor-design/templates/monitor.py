#!/usr/bin/env python3
"""Standing monitor skeleton — implements the silence contract.

Four modes:
    <script>              silent unless a NEW matching item appears, or a source dies
    <script> --baseline   seed the seen-set silently (run once before scheduling)
    <script> --health     print monitor status (for the unconditional heartbeat job)
    <script> --verbose    print every fetched item, ignore dedupe (debug only)

Design law:
  * Empty stdout on a normal tick => the scheduler delivers nothing.
  * VOID GUARD: when every source fails, SHOUT. Never render "cannot check" as an
    empty, all-clear tick.
  * Deterministic gated output: no timestamps on this path.

Edit CONFIG below, then:
    python3 monitor.py --baseline
    python3 monitor.py --health
    python3 monitor.py
"""

import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ---------------------------------------------------------------- CONFIG
STATE_PATH = "/root/.hermes/cron/<monitor-name>/state.json"
SEEN_CAP = 4000  # per watcher; bounds state growth
USER_AGENT = "Mozilla/5.0 (compatible; arifOS-monitor/1.0)"

# One entry per thing being watched. A hit needs a term from `require` AND one
# from `confirm` in the same headline — co-occurrence is what buys precision.
WATCHERS = [
    {
        "id": "example-topic",
        "label": "Example topic",
        "why": "One sentence: why this is worth waking a human for.",
        "queries": ["primary query phrase", "fallback query phrase"],
        "require": ["subject-term", "alias"],
        "confirm": ["action-term", "status-term"],
    },
]
# Source: Google News RSS — deterministic, keyless.
FEED = "https://news.google.com/rss/search?q={q}&hl=en-MY&gl=MY&ceid=MY:en"
# -----------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state() -> dict:
    try:
        with open(STATE_PATH) as f:
            s = json.load(f)
        s.setdefault("watchers", {})
        return s
    except (OSError, json.JSONDecodeError):
        return {"watchers": {}, "created": now_iso()}


def save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    os.replace(tmp, STATE_PATH)  # atomic: never leave a half-written state file


def fetch(query: str, timeout: int = 20):
    """Return (items, error). items=[] with error=None means genuinely empty."""
    url = FEED.format(q=urllib.parse.quote(query))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as e:
        return [], f"{type(e).__name__}: {e}"
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return [], f"ParseError: {e}"

    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        if not title:
            continue
        out.append({"title": title, "link": link})
    return out, None


def matches(w: dict, title: str) -> bool:
    t = title.lower()
    return any(r in t for r in w["require"]) and any(c in t for c in w["confirm"])


def key_of(item: dict) -> str:
    basis = item["link"] or item["title"].lower()
    return hashlib.sha256(basis.encode()).hexdigest()[:16]


def run(verbose: bool = False, baseline: bool = False) -> int:
    state = load_state()
    hits, failures = [], []

    for w in WATCHERS:
        st = state["watchers"].setdefault(
            w["id"], {"seen": {}, "last_success": None, "fails": 0, "hits": 0}
        )
        seen, errs, fetched = st["seen"], [], 0

        for q in w["queries"]:
            items, err = fetch(q)
            if err:
                errs.append(f"{q!r} -> {err}")
                continue
            fetched += len(items)
            for item in items:
                if verbose:
                    print(f"[{w['id']}] {item['title'][:110]}")
                k = key_of(item)
                if k in seen:
                    continue
                if matches(w, item["title"]):
                    seen[k] = now_iso()
                    st["hits"] += 1
                    if not baseline:
                        hits.append(
                            f"MONITOR {w['id']} — {w['label']}\n"
                            f"  {item['title']}\n  {item['link']}"
                        )

        # Bound state: evict oldest-first so it cannot grow without limit.
        if len(seen) > SEEN_CAP:
            for k, _ in sorted(seen.items(), key=lambda kv: kv[1])[: len(seen) - SEEN_CAP]:
                seen.pop(k, None)

        # VOID GUARD: total failure must shout, never look like a quiet tick.
        if errs and fetched == 0:
            st["fails"] += 1
            failures.append(
                f"TRIPWIRE {w['id']} ({w['label']}): CANNOT WITNESS — every source "
                f"failed this tick ({len(errs)} errors). This is NOT an all-clear.\n"
                + "\n".join(f"    {e}" for e in errs[:4])
            )
        else:
            st["last_success"] = now_iso()
            st["fails"] = 0  # partial loss records, but does not alert

    state["last_run"] = now_iso()
    save_state(state)

    if verbose:
        return 0
    out = []
    if hits:
        out.append(f"\U0001f514 MONITOR — {len(hits)} new match(es)\n")
        out.append("\n\n".join(hits))
    if failures:
        out.append("\u26a0\ufe0f " + "\n".join(failures))
    if out:
        print("\n\n".join(out))  # empty stdout => scheduler delivers nothing
    return 0


def health() -> int:
    state = load_state()
    print(f"MONITOR HEALTH   last_run: {state.get('last_run') or 'NEVER'}")
    dead = []
    for w in WATCHERS:
        st = state["watchers"].get(w["id"])
        if not st:
            dead.append(w["id"])
            print(f"  {w['id']:14} NEVER RAN")
            continue
        age = "?"
        if st.get("last_success"):
            dt = datetime.strptime(st["last_success"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
            age = f"{(datetime.now(timezone.utc) - dt).total_seconds() / 3600:.1f}h ago"
        flag = "DEAD" if st.get("fails", 0) >= 3 else "ok"
        if flag == "DEAD":
            dead.append(w["id"])
        print(
            f"  {w['id']:14} last_ok={age:12} fails={st.get('fails', 0):<3} "
            f"seek={len(st.get('seen', {})):<5} hits={st.get('hits', 0):<4} {flag}"
        )
    if dead:
        print("  \u26a0\ufe0f DEAD/NEVER-RAN: " + ", ".join(dead))
    return 0


if __name__ == "__main__":
    if "--health" in sys.argv:
        sys.exit(health())
    sys.exit(
        run(verbose="--verbose" in sys.argv, baseline="--baseline" in sys.argv)
    )
