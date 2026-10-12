#!/usr/bin/env python3
"""chron_morning — ONE morning pulse for the sovereign.

Converges the reality signals that hang (F13) and Abang Sado (Syed) need to know
into a single, deduplicated, human-language morning brief.

Replaces (does NOT duplicate):
  - alpha-zen morning pulse (07:15) — separately scheduled cron, lives in group
  - daily docforge brief (06:00) — same purpose, different audience
  - 10-step manual probe I was running each session
  - 4 CHRON systemd timer reports (each in its own .service file)

Reads (no new probes — all from existing local stores):
  1. chron_events.json       — ranked temporal events (chron.py render)
  2. chron_briefing          — 1-line operational pulse (T1+T2+T3+T4+T5 funnel)
  3. attention_debt          — overdue predictions / unresolved events
  4. gut_override            — Syed's gut-override ledger (what to do about it)
  5. attribution             — who generated last batch of episodes
  6. market cache            — Brent, USDMYR, VIX, DXY, US10Y, silver (from WEALTH)
  7. carry_forward.jsonl     — open_loops (sovereign/Abang-sado specific)
  8. lessons.jsonl           — last 3 lessons worth knowing
  9. cron health             — last_trigger of each chron-*.timer
 10. falkordb                — linkgraph group sizes (if graphiti is alive)

Output: one Markdown brief (~30 lines, BM Penang default) printed to stdout.
No new artifacts. No new cron. No new file unless explicitly asked.

If a section has no fresh signal, it is OMITTED, not padded.

Usage:
  python3 /root/AAA/scripts/chron_morning.py
  python3 /root/AAA/scripts/chron_morning.py --json    # for downstream
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- path setup: /root/chron is a package, needs PYTHONPATH=/root ---
os.environ.setdefault("PYTHONPATH", "/root")
sys.path.insert(0, "/root")

from chron.chron_briefing import (
    generate_briefing,
)
from chron.chron_attention_debt import get_ad_summary, collect_current_debt
from chron.chron_attribution import attribution_coverage

NOW = datetime.now(timezone(timedelta(hours=8)))
TODAY = NOW.date().isoformat()
NOW_ISO = NOW.isoformat()


# ---------- 1) chron_events.json ranked ----------
def ranked_events(limit: int = 5) -> list[dict]:
    """Invoke chron.py as a subprocess (it's a script, refuses module import).
    Parse its plain-text output: lines of the form
      "Title — N hari  [HIGH/PREPARE · truth=3.00 urg=7.00 → 21.00]"
    """
    try:
        r = subprocess.run(
            ["python3", "/root/AAA/scripts/chron.py"],
            capture_output=True, text=True, timeout=10,
        )
        out = []
        for line in r.stdout.splitlines():
            line = line.strip()
            if not line or line.startswith("2026 dah"):
                continue
            # parse "<title> — <when>  [<CONS>/<ACT> · truth=X urg=Y → Z>]"
            if " — " not in line or "[" not in line:
                continue
            try:
                title_part, rest = line.split(" — ", 1)
                when_part, bracket_part = rest.split("  [", 1)
                bracket = bracket_part.rstrip("]")
                # "HIGH  /PREPARE · truth=3.00 urg=7.00 → 21.00"
                if " · " in bracket:
                    cons_act, score_part = bracket.split(" · ", 1)
                else:
                    cons_act, score_part = bracket, ""
                # "HIGH  /PREPARE"
                cons, act = cons_act.split("/", 1)
                cons = cons.strip()
                act = act.strip()
                # parse when
                when = when_part.strip()
                if when == "HARI NI":
                    days = 0
                elif when == "esok":
                    days = 1
                elif "hari" in when:
                    try:
                        days = int(when.split()[0])
                    except Exception:
                        days = None
                elif "bulan" in when:
                    # "8 bulan (267 hari)"
                    try:
                        days = int(when.split("(")[1].split()[0])
                    except Exception:
                        days = None
                elif "tahun" in when:
                    try:
                        days = int(float(when.split("tahun")[0].strip().split()[-1]) * 365.25)
                    except Exception:
                        days = None
                else:
                    days = None
                # score
                score = None
                if "→" in score_part:
                    try:
                        score = float(score_part.split("→")[-1].strip())
                    except Exception:
                        pass
                out.append({
                    "title": title_part.strip(),
                    "days": days,
                    "when": when,
                    "consequence": cons,
                    "actionability": act,
                    "score": score,
                })
            except Exception:
                continue
        return out[:limit]
    except Exception as e:
        return [{"_err": str(e)[:200]}]


# ---------- 2) CHRON T1-T5 funnel summary ----------
def chron_funnel() -> dict:
    """generate_briefing() returns the full payload; pull the operational slice.
    Structure (verified 2026-10-06):
      predictions.{active_count, due_count, due:[]}
      calibration.{total, correct, accuracy, brier, effective_n}
      episodes_total
      recent_lessons_count, recent_lessons:[]

    verified/correct counts come from /root/chron/data/predictions.jsonl
    (status field), since the briefing doesn't carry them directly.
    """
    try:
        b = generate_briefing()
        preds = b.get("predictions", {})
        # count from the prediction store directly (authoritative)
        verified = correct = 0
        try:
            for ln in open("/root/chron/data/predictions.jsonl"):
                d = json.loads(ln)
                s = d.get("status")
                if s in ("VERIFIED", "CORRECT"):
                    verified += 1
                    if s == "CORRECT" or d.get("verdict") == "CORRECT":
                        correct += 1
        except Exception:
            pass
        # lessons: count real (non-placeholder) in lessons.jsonl
        lessons_total = lessons_active = 0
        try:
            for ln in open("/root/chron/data/lessons.jsonl"):
                d = json.loads(ln)
                t = (d.get("lesson") or d.get("statement") or "")
                if "Unknown error" not in t:
                    lessons_total += 1
                # 'active' = status field exists and not CANDIDATE-only
                if d.get("status") and d.get("status") != "DIAGNOSTIC":
                    lessons_active += 1
        except Exception:
            pass
        return {
            "active": preds.get("active_count", "?"),
            "due": preds.get("due_count", "?"),
            "verified": verified,
            "correct": correct,
            "calibration": b.get("calibration", {}),
            "episodes": b.get("episodes_total", "?"),
            "lessons": lessons_total,
            "lessons_active": lessons_active,
        }
    except Exception as e:
        return {"_err": str(e)[:200]}


# ---------- 3) attention_debt ----------
def ad_summary() -> dict:
    try:
        return get_ad_summary()
    except Exception as e:
        return {"_err": str(e)[:200]}


# ---------- 4) gut_override (only the recent ones that matter) ----------
def gut_override_recent(limit: int = 3) -> list[dict]:
    p = Path("/root/.local/share/arifos/gut_override_ledger.jsonl")
    if not p.exists():
        return []
    out = []
    for ln in p.read_text().splitlines()[-50:]:
        if not ln.strip():
            continue
        try:
            d = json.loads(ln)
        except Exception:
            continue
        out.append(d)
    return out[-limit:]


# ---------- 5) attribution ----------
def attribution_summary() -> dict:
    p = Path("/root/chron/data/episodes.jsonl")
    if not p.exists():
        return {"_err": "no episodes.jsonl"}
    try:
        # only feed the last 200 (cheap; full would be slow)
        eps = [json.loads(l) for l in p.read_text().splitlines()[-200:] if l.strip()]
        return attribution_coverage(eps)
    except Exception as e:
        return {"_err": str(e)[:200]}


# ---------- 6) market cache ----------
def market_snapshot() -> dict:
    p = Path("/root/AAA/scripts/.chron_market_cache.json")
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text())
        age_h = (NOW - datetime.fromisoformat(d.get("captured_at", NOW_ISO))).total_seconds() / 3600
        d["_age_h"] = round(age_h, 1)
        return d
    except Exception:
        return {}


# ---------- 7) carry_forward open loops ----------
def open_loops() -> list[dict]:
    p = Path("/root/.local/share/arifos/carry_forward.json")
    if not p.exists():
        return []
    try:
        d = json.loads(p.read_text())
        return d.get("open_loops", []) or []
    except Exception:
        return []


# ---------- 8) lessons (real ones, no UNKNOWN placeholders) ----------
def real_lessons(limit: int = 3) -> list[dict]:
    p = Path("/root/chron/data/lessons.jsonl")
    if not p.exists():
        return []
    out = []
    for ln in p.read_text().splitlines():
        if not ln.strip():
            continue
        try:
            d = json.loads(ln)
        except Exception:
            continue
        # skip placeholders
        if "Unknown error" in d.get("lesson", "") or "Unknown error" in d.get("statement", ""):
            continue
        out.append(d)
    return out[-limit:]


# ---------- 9) cron health (one-liner per active timer) ----------
def cron_health() -> list[dict]:
    out = []
    try:
        r = subprocess.run(
            ["systemctl", "list-timers", "--all", "--no-pager"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception as e:
        return [{"_err": str(e)[:200]}]
    for line in r.stdout.splitlines():
        # next | left | last | unit | activates
        if "chron-" not in line and "chron_" not in line:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        # crude parse — first 4 cols are time fields, then unit
        # column index for unit
        # actual format: "Tue 2026-10-06 09:45:00 +08         35min Mon 2026-10-05 09:45:01 +08       23h ago chron-reality-impact-attestor.timer chron-reality-impact-attestor.service"
        words = line.split()
        unit = next((w for w in words if w.startswith("chron-") and (w.endswith(".timer") or w.endswith(".service"))), None)
        if not unit:
            continue
        out.append({"unit": unit, "raw": line.strip()})
    return out


# ---------- 10) falkordb linkgraph group sizes (only if alive) ----------
def linkgraph_groups() -> list[dict]:
    try:
        r = subprocess.run(
            ["redis-cli", "-h", "127.0.0.1", "-p", "6380", "DBSIZE"],
            capture_output=True, text=True, timeout=3,
        )
        if r.returncode != 0:
            return []
        out = [{"_total_keys": r.stdout.strip()}]
        groups = ["arif_l5_knowledge", "sado_knowledge", "atlas333_graph",
                  "af_forge", "arifos", "arifos_federation", "searah_2026q3"]
        for g in groups:
            t = subprocess.run(
                ["redis-cli", "-h", "127.0.0.1", "-p", "6380", "TYPE", g],
                capture_output=True, text=True, timeout=3,
            ).stdout.strip()
            if t:
                out.append({"group": g, "type": t})
        return out
    except Exception as e:
        return [{"_err": str(e)[:200]}]


# ---------- render ----------
def render_md() -> str:
    out: list[str] = []
    out.append(f"# CHRON morning — {NOW.strftime('%A, %d %B %Y · %H:%M')} MYT")
    out.append("")

    # 1) ranked events
    try:
        evs = ranked_events(limit=5)
        if evs:
            out.append("## Tarikh depan (ranked)")
            for e in evs:
                days = e["days"]
                if days == 0:
                    when = "HARI NI"
                elif days == 1:
                    when = "esok"
                elif days < 31:
                    when = f"{days} hari"
                elif days < 550:
                    when = f"{days // 30} bulan ({days} hari)"
                else:
                    when = f"{days / 365.25:.1f} tahun"
                parts = f"{e['consequence']:6}/{e['actionability']:7}  score={e['score']:.2f}"
                aud = e.get("audience", "?")
                aud_marker = "ARIF" if aud == "arif" else "SYED" if aud == "syed" else "BOTH"
                out.append(f"- [{aud_marker}] **{e['title']}** — {when}  `[{parts}]`")
            out.append("")
    except Exception as e:
        out.append(f"## Tarikh: ERR {e}")
        out.append("")

    # 2) CHRON funnel
    try:
        f = chron_funnel()
        out.append("## CHRON funnel")
        out.append(
            f"- Predictions: **{f.get('active', '?')} active**, {f.get('due', '?')} due, "
            f"{f.get('verified', '?')} verified, {f.get('correct', '?')} correct"
        )
        cal = f.get("calibration", {})
        if cal:
            out.append(
                f"- Calibration: acc={cal.get('accuracy', '?')} brier={cal.get('brier', '?')} "
                f"(n={cal.get('total', '?')})"
            )
        out.append(f"- Episodes: **{f.get('episodes', '?')}** | "
                   f"Lessons: **{f.get('lessons', '?')}** | "
                   f"Lessons active: **{f.get('lessons_active', '?')}**")
        out.append("")
    except Exception as e:
        out.append(f"## Funnel: ERR {e}\n")

    # 3) attention debt
    try:
        ad = ad_summary()
        if ad and not ad.get("_err"):
            total = ad.get("total_ad", 0)
            n = ad.get("item_count", 0)
            gr = ad.get("growth_rate_per_day", 0)
            oldest = ad.get("oldest") or {}
            out.append("## Attention debt")
            out.append(
                f"- total_ad **{total:.1f}** across **{n} items**, growth {gr:+.2f}/hari"
            )
            if oldest:
                out.append(
                    f"- oldest: {oldest.get('description', '?')[:80]} "
                    f"({oldest.get('age_days', '?')} hari)"
                )
            out.append("")
    except Exception as e:
        out.append(f"## AD: ERR {e}\n")

    # 4) market (only if fresh and from WEALTH)
    m = market_snapshot()
    if m and not m.get("_err"):
        age = m.get("_age_h", 99)
        if age < 12:  # only show if fresh
            out.append("## Pasaran (live, WEALTH)")
            out.append(
                f"- Brent **{m.get('brent', '?')}** · USD/MYR **{m.get('usdmyr', '?')}** · "
                f"VIX **{m.get('vix', '?')}** · DXY **{m.get('dxy', '?')}** · "
                f"US10Y **{m.get('us10y', '?')}%** · silver **{m.get('silver', '?')}**"
            )
            out.append(f"  (snapshot {age}j lama, source: {m.get('source', '?')[:60]})")
            out.append("")

    # 5) real lessons (no placeholders)
    rl = real_lessons(limit=3)
    if rl:
        out.append("## Lessons baru (bukan placeholder)")
        for l in rl:
            txt = l.get("lesson", "")[:200]
            out.append(f"- {txt}")
        out.append("")

    # 6) gut_override recent (only if there are any)
    go = gut_override_recent(limit=3)
    if go:
        out.append("## Gut override (Syed)")
        for g in go:
            txt = g.get("description") or g.get("text") or json.dumps(g)[:200]
            out.append(f"- {str(txt)[:200]}")
        out.append("")

    # 7) cron health
    ch = cron_health()
    if ch:
        out.append("## CHRON cron health")
        for h in ch:
            unit = h.get("unit", "?")
            raw = h.get("raw", "")
            # extract last fire time
            last_marker = ""
            if "ago" in raw:
                # grab the time block right before "ago"
                parts = raw.split()
                for i, w in enumerate(parts):
                    if w == "ago" and i >= 2:
                        last_marker = f"  (last: {' '.join(parts[max(0,i-2):i])})"
                        break
            out.append(f"- {unit}{last_marker}")
        out.append("")

    # 8) linkgraph (only if alive)
    lg = linkgraph_groups()
    if lg and not any("_err" in x for x in lg):
        total_keys = next((x.get("_total_keys") for x in lg if "_total_keys" in x), "?")
        real_groups = [x for x in lg if "group" in x]
        if real_groups:
            out.append(f"## Link graph (FalkorDB) — {total_keys} keys")
            for g in real_groups:
                out.append(f"  - {g['group']:25} {g['type']}")
            out.append("")

    # 9) attribution (only if data available)
    try:
        attr = attribution_summary()
        if attr and not attr.get("_err") and attr.get("episodes_total", 0) > 0:
            out.append("## Attribution (last 200 episodes)")
            out.append(
                f"- {attr.get('attributed', 0)}/{attr.get('episodes_total', 0)} attributed "
                f"({attr.get('attributed_ratio', 0) * 100:.1f}%)"
            )
            per = attr.get("per_agent", {})
            if per:
                top = ", ".join(f"{k}={v}" for k, v in sorted(per.items(), key=lambda x: -x[1])[:5])
                out.append(f"- top: {top}")
            out.append("")
    except Exception:
        pass

    out.append("---")
    out.append("Source: chron.py · chron_briefing · attention_debt · gut_override · attribution · WEALTH · FalkorDB")
    out.append("If a section missing → no fresh signal, not omission.")

    return "\n".join(out)


def render_json() -> dict:
    """Programmatic version for downstream tools (alpha-zen, SADO)."""
    return {
        "as_of": NOW_ISO,
        "ranked_events": [
            {
                "id": e.get("id"),
                "title": e.get("title"),
                "days": e.get("days"),
                "audience": e.get("audience"),
                "consequence": e.get("consequence"),
                "actionability": e.get("actionability"),
                "score": e.get("score"),
            }
            for e in ranked_events(limit=10)
        ],
        "funnel": chron_funnel(),
        "attention_debt": ad_summary(),
        "market": market_snapshot(),
        "real_lessons": [
            {"id": l.get("lesson_id"), "text": l.get("lesson"), "audience": l.get("audience")}
            for l in real_lessons(limit=5)
        ],
        "open_loops": open_loops(),
        "cron_health": cron_health(),
        "linkgraph": linkgraph_groups(),
        "attribution": attribution_summary(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if args.json:
        print(json.dumps(render_json(), indent=2, ensure_ascii=False, default=str))
    else:
        print(render_md())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
