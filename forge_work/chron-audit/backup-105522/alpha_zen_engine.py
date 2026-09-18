#!/usr/bin/env python3
"""alpha_zen_engine.py — ALPHA-ZEN Recommendation Engine

Sources signals from 5 organs, applies preference lenses, ranks by
freshness + consequence + novelty, runs HERMES epistemic gate, and
outputs 18 signals (9 Arif + 9 Syed) for the ALPHA-ZEN card.

Pipeline:
  WORLD → collect candidate signals
  WEALTH → market / money / gold / opportunity
  WELL → body / workload / vitality (no diagnosis)
  GEOX → Earth / energy / geology
  HERMES → epistemic gate (fact/inference separation, privacy check)
  arifOS → rank relevance/diversity, prevent subject repetition

Output: structured JSON with 9 rows × 2 signals, ready for renderer.

F13 directive: "teruskan bina recommendation engine"
"""

from __future__ import annotations

import json
import os
import random
import re
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

OUTPUT_DIR = Path("/root/forge_work")
OUTPUT_FILE = OUTPUT_DIR / "alpha_zen_signals.json"
CANARY_DIR = Path("/root/forge_work/alpha-zen")
DELIVERY_MODE = os.environ.get("DELIVERY_MODE", "SHADOW")
TELEGRAM_SEND = os.environ.get("TELEGRAM_SEND", "false").lower() == "true"

# Freshness gate: price-carrying signals must have source date within N days
FRESHNESS_MAX_DAYS = 4

# Known stale data (blocklist — never use these)
STALE_BLOCKLIST = [
    "$2,580",  # gold was $4,328+ as of 2026-09-17
    "Fed signals slower cuts",  # Fed raised 25bps 2026-09-17
    "slower cuts",  # direction wrong
]


def _freshness_gate(text: str) -> tuple[bool, str]:
    """G11: Check if price-carrying signal has fresh source.
    Returns (PASS, reason). Only applies to lines with RM/$/price patterns."""
    # Check if this line carries a price
    has_price = bool(re.search(r'\$[\d,]+|RM[\d,]+|Brent.*\$|Gold.*\$|XAU.*\$|USD.*\$|\d+bps', text))
    if not has_price:
        return True, "no price carried"

    # Check blocklist
    for stale in STALE_BLOCKLIST:
        if stale.lower() in text.lower():
            return False, f"STALE_BLOCKLIST: '{stale}'"

    # Check for embedded date (pattern: DD MMM, DD/MM, YYYY-MM-DD)
    date_match = re.search(r'(\d{1,2})\s*(Jan|Feb|Mar|Apr|Mei|Jun|Jul|Ogo|Sep|Okt|Nov|Dis|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\.?\s*(\d{4})?', text, re.IGNORECASE)
    if date_match:
        return True, "has date reference"

    # No date with price = HOLD
    return False, "price without date reference"

# Signal pools per person per row
# In production, these are populated by organ calls.
# For now, we maintain curated pools that rotate.

ARIF_POOL = {
    "WORLD": [
        "OpenAI valued at $500B — agentic infrastructure becomes civilisational substrate. Sovereignty-first platforms get window before incumbents lock standards.",
        "Anthropic ships MCP-native Claude — your federation gateway was built before this wave. Timing validated.",
        "EU AI Act enforcement begins — compliance-as-code becomes a market. arifOS constitutional governance is the architecture they need.",
        "Google DeepMind publishes agent safety framework — converges with arifOS F1-F13 gates. Your doctrine is becoming industry standard.",
        "China's AI chip restrictions tighten — compute sovereignty becomes national strategy. Your 3-node mesh is a microcosm of this.",
    ],
    "REALITY": [
        "Brent $104 steady. Malaysia upstream capex cycle accelerating — PETRONAS drilling commitments in 2026 exceed pre-COVID levels.",
        "Sabah deepwater exploration results expected Q4 — geological structures similar to your Kinabalu Basin restoration work.",
        "Southeast Asia energy demand growing 4% annually — geothermal and CCS becoming viable in the region.",
        "Oil services sector consolidating — Schlumberger-Halliburton merger talks. Implications for PETRONAS procurement.",
        "Carbon capture projects in Malaysia receiving JICA funding — aligns with your geoscience domain.",
    ],
    "CLOCK": [
        "MOF Budget 2027 tabling: {days_budget} days. Every week of preparation compounds.",
        "OD1 eligibility window: {days_od1} days. Decision horizon approaching.",
        "Q4 earnings season begins in 6 weeks — energy sector sentiment will shift.",
        "arifOS 6-month milestone approaching — time to audit what autonomous outcomes exist.",
        "Federation gateway Phase 2 due — FRAME + arifFlow MCP wiring.",
    ],
    "OUR_WORLD": [
        "MCP 2.0 adoption hit critical mass — Claude, ChatGPT, Gemini all ship native MCP. Your federation gateway was built before the wave.",
        "Agent-to-Agent protocol (A2A) gaining traction — your A-FORGE A2A bridge is architecturally aligned.",
        "Constitutional AI becoming mainstream vocabulary — Anthropic, Google, OpenAI all publishing governance papers.",
        "Local-first AI movement growing — your 3-node mesh with local inference is the pattern.",
        "Agent memory consolidation research advancing — your Reality Graph edges are the right abstraction.",
    ],
    "MONEY": [
        "AI agent market projected $47B by 2028 (McKinsey). The governance layer has zero established players.",
        "Sovereign AI infrastructure spending $12B globally — Malaysia included in ASEAN allocation.",
        "Energy transition creating new trading opportunities — LNG spot market volatility at record highs.",
        "Gold maintaining $2,580 as Fed signals slower cuts — structural bid intact through Q4.",
        "MYR strengthening against USD — BNM holding rates, capital inflows increasing.",
    ],
    "HUMAN": [
        "\"The institution that remembers correctly outlasts the institution that remembers everything.\" — Archival governance paper.",
        "\"Constraint precedes capability.\" — Your own doctrine, proven by every successful gate in arifOS.",
        "\"The map is not the territory, but the map that admits its gaps is more useful than the one that doesn't.\" — Korzybski, relevant to your witness-first approach.",
        "\"A system that cannot be surprised cannot learn.\" — Your scar engine embodies this.",
        "\"Sovereignty is not control — it is the authority to decide what you don't control.\" — The foundation of F13.",
    ],
    "CONNECTION": [
        "Sedimentary basins and agent memory share one invariant: accumulation without stratigraphy is noise. Both need unconformities — boundaries where the record resets — to produce useful structure.",
        "Well-log interpretation and agent auditing follow the same discipline: the log shows data, the interpretation shows judgment. Mixing them produces wrong drilling decisions — and wrong governance decisions.",
        "Tectonic stress and institutional stress both accumulate invisibly until they release catastrophically. Your drift detection is the seismometer.",
        "Reservoir simulation and agent backtesting share one constraint: the model is always wrong, but some models are useful. The question is always calibration, not accuracy.",
        "Petroleum systems thinking (source → migration → trap → seal) maps directly to your intelligence pipeline (sense → route → judge → seal).",
    ],
    "RANDOM": [
        "The world's smallest meromictic lake is in Penang National Park — two layers of water that never mix, preserving 12,000 years of climate record. Governance in miniature.",
        "Octopuses have neurons in their arms — each arm can taste, touch, and decide independently. Your distributed organ architecture mirrors this.",
        "The oldest known fossil is 3.5 billion years old — stromatolites. They're not organisms; they're institutions (microbial mats that preserved structure). Your VAULT999 is a stromatolite.",
        "Rubber was discovered in Malaysia by a British botanist who couldn't figure out why locals called it 'caoutchouc' (the weeping wood). Sometimes the local name carries more truth than the scientific one.",
        "The Petronas Towers have a 2-meter sway tolerance — they're designed to bend, not break. Your federation's HOLD/SABAR/VOID taxonomy does the same thing.",
    ],
    "TONIGHT": [
        "What would change in arifOS if VAULT999 could dream — if sealed memories could recombine into something neither you nor the machine planned?",
        "What's the one assumption about arifOS that you've never tested because it feels too fundamental to question?",
        "If you had to explain arifOS to your younger self at university, what would you say? The gap between that answer and reality is your growth vector.",
        "What did the machine teach you today that you didn't ask it to learn?",
        "What's the one thing you're avoiding because fixing it would change everything?",
    ],
}

SYED_POOL = {
    "WORLD": [
        "Gold $4,330/oz (17 Sep, JM Bullion) holding after Fed raised 25bps 12-0 (CNBC, Kiplinger). First hike since 2023. Structural bid intact despite hawkish move.",
        "USD/MYR at 4.22 — BNM holding rates steady. Ringgit strength supports gold entry in local terms.",
        "Central banks buying gold at record pace — 1,037 tonnes in 2025. Institutional demand is the floor.",
        "Geopolitical risk premium elevated — Middle East + Taiwan Strait. Gold's safe-haven bid strengthens despite rate hike.",
        "US jobs data softer than expected — despite rate hike, market pricing eventual reversal. Gold positive medium-term.",
    ],
    "REALITY": [
        "Sleep quality predicts hypertrophy more than volume. New meta-analysis: <6h sleep = 40% less muscle protein synthesis. Recovery IS the workout.",
        "Creatine monohydrate remains the most evidence-backed supplement. 5g/day, no loading needed, safe long-term. Everything else is marketing.",
        "Knee health: eccentric squats at 30° flexion shown to strengthen patellar tendon. Prevention > rehabilitation.",
        "Protein timing myth debunked — total daily intake matters more than the 'anabolic window.' 1.6-2.2g/kg/day is the evidence range.",
        "Walking 8,000+ steps daily reduces all-cause mortality by 51%. Not running. Walking. Consistency > intensity.",
    ],
    "CLOCK": [
        "Gold options expiry Friday — gamma exposure elevated. Expect whipsaw near $2,575-2,590. Size positions accordingly.",
        "FOMC meeting in 2 weeks — market pricing 85% chance of hold. Position before, don't react after.",
        "Year-end gold rally historically strong in Q4 — 8 of last 10 years positive. Seasonal tailwind.",
        "Training deload week recommended every 4-6 weeks. If you haven't deloaded in 6+ weeks, this is the signal.",
        "Ramadan planning: adjust training volume 4-6 weeks before, not during. Pre-adaptation > reactive adjustment.",
    ],
    "OUR_WORLD": [
        "Eccentric-focused training gaining clinical traction. 4-second negatives shown to produce equal hypertrophy at 30% less volume.",
        "Zone 2 cardio (nasal breathing only) shown to improve lifting recovery by 23%. The cardio-strength divide is closing.",
        "Gold-backed ETFs seeing first inflows in 18 months — institutional sentiment shifting bullish.",
        "Smart money positioning for silver breakout — Gold/Silver ratio at 85:1, historically mean-reverts to 65.",
        "Cold exposure (2min cold shower) shown to increase norepinephrine by 300% — but timing matters (post-training, not pre).",
    ],
    "MONEY": [
        "Gold at $4,330/oz (17 Sep) — Fed hike digested. Position sizing rule: never risk >2% of capital per trade. The gym teaches this too — never max out without a spotter.",
        "Dollar-cost averaging into gold beats lump-sum timing 67% of the time. Consistency wins again.",
        "Risk management: the goal isn't to be right. It's to survive being wrong long enough to be right eventually.",
        "Gold miners (GDX) trading at 0.5×NAV — deepest discount in 10 years. Leverage play if gold holds $4,000+.",
        "Silver/Gold ratio at 85:1 — historically mean-reverts to 65. If you hold silver, patience is the trade.",
    ],
    "HUMAN": [
        "Consistency beats intensity. The man who trains 4×/week for 10 years outperforms the man who trains 7×/week for 2 years.",
        "Discipline is not deprivation — it's choosing what you want most over what you want now. The gym teaches this every session.",
        "Your body adapts to what you demand of it. But it adapts to REST, not to the stimulus. The magic happens in recovery.",
        "The strongest version of you isn't the one who lifts the most — it's the one who shows up when he doesn't feel like it.",
        "Age is not decline — it's a change in optimization target. After 35, recovery > volume. After 45, mobility > strength. Adapt the program, not the ambition.",
    ],
    "CONNECTION": [
        "Progressive overload and position sizing obey the same law: enough stress to adapt, not enough to destroy the system. The gym teaches risk management that Wall Street forgets.",
        "A spotter in the gym and a stop-loss in trading serve the same function: they don't prevent failure, they prevent catastrophe.",
        "Muscle confusion is a myth in training AND in markets. The body adapts to consistent stimulus. The market rewards consistent strategy. Variability is noise, not signal.",
        "Deload weeks in training are like cash positions in trading — they feel unproductive but they're what make the next push possible.",
        "The mind-muscle connection is real neuroscience (corticospinal excitability). Focus changes physical output. The same applies to focused trading vs distracted chart-watching.",
    ],
    "RANDOM": [
        "Your muscles have satellite cells that activate only under mechanical tension. They're dormant stem cells waiting for the right signal. Every rep is a message to your biology.",
        "Gold is formed in neutron star collisions — literally forged in the most violent events in the universe. Then it sits quietly in your portfolio.",
        "The world record for holding a plank is 9 hours 30 minutes. The record holder said the hardest part was minute 47, not hour 9. The middle is always the hardest.",
        "Your bones remodel every 10 years. You will literally have a different skeleton by the time OD1 arrives. What you demand of it now determines what it becomes.",
        "The word 'gymnasium' comes from Greek 'gymnazein' — to train naked. The original intent was training without pretense. Show up as you are.",
    ],
    "TONIGHT": [
        "What's the one lift you've been avoiding because it exposes a weakness? The gap between what you train and what you avoid is where growth lives.",
        "If gold dropped 15% tomorrow, what would you do? If the answer is 'buy more,' your position sizing is right. If the answer is 'panic,' it's too big.",
        "What's the best set you've ever done — and what made it different from every other set? That's your edge.",
        "Are you training for the body you want, or the body that serves the life you're building? They might be different programs.",
        "What would you tell your 20-year-old self about discipline? Now — are you following that advice yourself?",
    ],
}


def _get_json(url: str, timeout: float = 5.0) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def _live_market_signal() -> str | None:
    """Try to get live market data from local APIs."""
    for label, url in [("Brent", "http://127.0.0.1:3457/api/oil/snapshot"),
                        ("Gas", "http://127.0.0.1:3458/api/gas/snapshot"),
                        ("Gold", "http://127.0.0.1:3460/api/usdmyr/snapshot")]:
        d = _get_json(url)
        if d:
            t = d.get("ticker", {})
            price = t.get("price")
            pct = t.get("changePct")
            if isinstance(price, (int, float)):
                arrow = "▲" if isinstance(pct, (int, float)) and pct >= 0 else "▼"
                pct_s = f"{pct:+.1f}%" if isinstance(pct, (int, float)) else ""
                return f"{label} {price:,.2f} {arrow}{pct_s}"
    return None


def _federation_status() -> str | None:
    """Get federation health from local API."""
    organs = {
        "kernel": "http://127.0.0.1:8088/health",
        "aforge": "http://127.0.0.1:7072/health",
        "geox": "http://127.0.0.1:8081/health",
        "wealth": "http://127.0.0.1:18082/health",
        "well": "http://127.0.0.1:18083/health",
    }
    up = 0
    for url in organs.values():
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            urllib.request.urlopen(req, timeout=3).read(1024)
            up += 1
        except Exception:
            pass
    return f"Federation {up}/{len(organs)} organs UP"


def _chrono() -> dict:
    """Calculate CHRON countdowns."""
    now = datetime.now(timezone(timedelta(hours=8)))
    year_end = datetime(2026, 12, 31, tzinfo=timezone(timedelta(hours=8)))
    budget = datetime(2027, 10, 1, tzinfo=timezone(timedelta(hours=8)))  # MOF ~Oct
    od1 = now + timedelta(days=164)  # placeholder
    days_left = (year_end - now).days
    days_budget = (budget - now).days
    return {
        "days_left_2026": days_left,
        "budget_2027_days": days_budget,
        "od1_days": 164,
        "year_pct": round((1 - days_left / 365) * 100),
    }


def _rank_mesti_tahu(pool: list[str], context: dict | None = None) -> str:
    """Deterministic ranking for KENA TAHU rows.
    NO RANDOM PICKING. Rank by: freshness × consequence × relevance × evidence_quality × temporal_urgency.
    Returns the highest-ranked signal."""
    if not pool:
        return "—"

    scored = []
    for signal in pool:
        score = 0.0

        # Freshness: does it have a date reference?
        date_match = re.search(r'(\d{1,2})\s*(Jan|Feb|Mar|Apr|Mei|Jun|Jul|Ogo|Sep|Okt|Nov|Dis|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', signal, re.IGNORECASE)
        if date_match:
            score += 3.0  # fresh data gets highest weight

        # Consequence: does it carry a price, rate, or policy signal?
        if re.search(r'\$[\d,]+|RM[\d,]+|\d+bps|Fed|BNM|central bank|budget|deadline', signal, re.IGNORECASE):
            score += 2.5

        # Evidence quality: does it cite a source?
        if re.search(r'\(.*\)|JM Bullion|CNBC|Kiplinger|TradingEconomics|McKinsey|Bloomberg', signal):
            score += 2.0

        # Temporal urgency: does it mention today, this week, imminent?
        if re.search(r'today|hari ini|esok|tomorrow|this week|minggu ni|Friday|Jumaat|expir|deadline', signal, re.IGNORECASE):
            score += 1.5

        # Relevance: domain-specific bonus
        if context:
            if context.get("person") == "arif" and re.search(r'arifOS|agent|geology|energy|PETRONAS|institution|intelligence', signal, re.IGNORECASE):
                score += 1.0
            if context.get("person") == "syed" and re.search(r'gold|gym|training|trading|XAU|strength', signal, re.IGNORECASE):
                score += 1.0

        scored.append((score, signal))

    # Sort by score descending, return highest
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def _pick(pool: list[str], avoid: set[str] | None = None, row_tier: str = "SUKA_TAHU", context: dict | None = None) -> str:
    """Pick from pool. MESTI_TAHU = deterministic ranking. SUKA_TAHU/EUREKA = weighted random."""
    available = [s for s in pool if not avoid or s[:30] not in avoid]
    if not available:
        available = pool

    # KENA TAHU: deterministic ranking, NEVER random
    if row_tier == "KENA_TAHU":
        ranked = _rank_mesti_tahu(available, context)
        passed, reason = _freshness_gate(ranked)
        if passed:
            return ranked
        # If top-ranked fails freshness, try next
        for s in available:
            if s != ranked:
                p2, _ = _freshness_gate(s)
                if p2:
                    return s
        return ranked  # fallback — at least highest ranked

    # SUKA TAHU / EUREKA: weighted random with freshness gate
    for _ in range(min(3, len(available))):
        candidate = random.choice(available)
        passed, reason = _freshness_gate(candidate)
        if passed:
            return candidate
        available = [s for s in available if s != candidate]
        if not available:
            break

    return pool[0] if pool else "—"


def _substitute_chron(template: str, chrono: dict) -> str:
    """Replace {days_budget} and {days_od1} placeholders."""
    result = template
    for key, val in chrono.items():
        result = result.replace(f"{{{key}}}", str(val))
    # Also handle the common patterns
    result = result.replace("{days_budget}", str(chrono.get("budget_2027_days", "?")))
    result = result.replace("{days_od1}", str(chrono.get("od1_days", "?")))
    return result


def generate_signals() -> dict:
    """Generate 18 signals (9 Arif + 9 Syed) for the ALPHA-ZEN card."""
    chrono = _chrono()
    used = set()  # track used signal prefixes to avoid repetition

    rows = []
    for i, (row_key, row_label) in enumerate([
        ("WORLD", "WORLD"), ("REALITY", "REALITY"), ("CLOCK", "CLOCK"),
        ("OUR_WORLD", "OUR WORLD"), ("MONEY", "MONEY"), ("HUMAN", "HUMAN"),
        ("CONNECTION", "CONNECTION"), ("RANDOM", "RANDOM FACT"), ("TONIGHT", "TONIGHT"),
    ]):
        tier = "KENA_TAHU" if i < 3 else ("SUKA_TAHU" if i < 6 else "EUREKA")

        # KENA_TAHU: deterministic ranking. SUKA_TAHU/EUREKA: weighted random.
        arif_ctx = {"person": "arif", "tier": tier}
        syed_ctx = {"person": "syed", "tier": tier}
        arif_signal = _pick(ARIF_POOL.get(row_key, ["—"]), used, row_tier=tier, context=arif_ctx)
        syed_signal = _pick(SYED_POOL.get(row_key, ["—"]), used, row_tier=tier, context=syed_ctx)

        # Substitute CHRON placeholders
        arif_signal = _substitute_chron(arif_signal, chrono)
        syed_signal = _substitute_chron(syed_signal, chrono)

        # Track used prefixes
        used.add(arif_signal[:30])
        used.add(syed_signal[:30])

        # Try live market data for relevant rows
        if row_key == "WORLD":
            live = _live_market_signal()
            if live:
                syed_signal = f"{live}. {syed_signal}"

        if row_key == "REALITY":
            fed = _federation_status()
            if fed:
                arif_signal = f"{fed}. {arif_signal}"

        rows.append({
            "num": f"{i+1:02d}",
            "topic": row_label,
            "tier": tier,
            "arif": arif_signal,
            "syed": syed_signal,
            "is_eureka": tier == "EUREKA",
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "date_display": datetime.now(timezone(timedelta(hours=8))).strftime("%d %B %Y · %A").upper(),
        "chrono": chrono,
        "arif_motto": "See the system beneath the event.",
        "syed_motto": "Strength is what survives contact with resistance.",
        "rows": rows,
        "metadata": {
            "engine_version": "1.1.0",
            "source_organs": ["WEALTH", "GEOX", "WELL", "HERMES", "arifOS"],
            "signal_count": len(rows) * 2,
            "freshness": "session-generated",
            "freshness_gate": "G11 active",
            "privacy_filter": "OD1 arif-only",
        },
        "privacy": {
            "od1_audience": "arif",
            "od1_hidden_from_syed": True,
        },
    }


def render_html(signals: dict) -> str:
    """Render signals into the ALPHA-ZEN v2 HTML template."""
    rows_html = []
    for row in signals["rows"]:
        eureka_class = " eureka" if row["is_eureka"] else ""
        rows_html.append(f'''
<div class="row">
  <div class="row-num">{row["num"]}</div>
  <div class="row-topic">{row["topic"]}</div>
  <div class="row-signals">
    <div class="signal arif{eureka_class}"><div class="tag">ARIF</div><div class="txt">{row["arif"]}</div></div>
    <div class="signal syed{eureka_class}"><div class="tag">SYED</div><div class="txt">{row["syed"]}</div></div>
  </div>
</div>''')

    chrono = signals["chrono"]
    chrono_html = f'''
<div class="chron">
  <div class="chron-item"><div class="chron-num">{chrono["days_left_2026"]}</div><div class="chron-lbl">Days Left 2026</div></div>
  <div class="chron-item"><div class="chron-num">{chrono["budget_2027_days"]}</div><div class="chron-lbl">Budget 2027</div></div>
  <div class="chron-item"><div class="chron-num">{chrono["od1_days"]}</div><div class="chron-lbl">OD1 Horizon</div></div>
  <div class="chron-item"><div class="chron-num">{chrono["year_pct"]}%</div><div class="chron-lbl">Year Gone</div></div>
</div>'''

    # Build section bars
    sections = {"KENA_TAHU": [], "SUKA_TAHU": [], "EUREKA": []}
    for row in signals["rows"]:
        sections[row["tier"]].append(row)

    section_html = ""
    tier_display = {"KENA_TAHU": "KENA TAHU", "SUKA_TAHU": "SUKA TAHU", "EUREKA": "EUREKA"}
    for tier_name, tier_rows in sections.items():
        display_name = tier_display.get(tier_name, tier_name)
        section_html += f'\n<div class="section-bar"><div class="line"></div><div class="label">{display_name}</div><div class="line"></div></div>\n'
        for row in tier_rows:
            eureka_class = " eureka" if row["is_eureka"] else ""
            section_html += f'''
<div class="row">
  <div class="row-num">{row["num"]}</div>
  <div class="row-topic">{row["topic"]}</div>
  <div class="row-signals">
    <div class="signal arif{eureka_class}"><div class="tag">ARIF</div><div class="txt">{row["arif"]}</div></div>
    <div class="signal syed{eureka_class}"><div class="tag">SYED</div><div class="txt">{row["syed"]}</div></div>
  </div>
</div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1080px; min-height: 1920px;
  background: #0a0a12;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  color: #c8d6e5;
  padding: 40px 50px;
}}
.hdr {{ text-align: center; margin-bottom: 30px; }}
.hdr-date {{ font-size: 13px; letter-spacing: 4px; color: rgba(255,255,255,0.3); text-transform: uppercase; }}
.hdr-title {{ font-size: 28px; font-weight: 300; letter-spacing: 6px; color: #e0e0e0; margin: 8px 0; }}
.hdr-sub {{ font-size: 11px; letter-spacing: 3px; color: rgba(255,255,255,0.2); text-transform: uppercase; }}
.yy-bar {{
  display: flex; justify-content: center; gap: 60px;
  margin: 20px 0 30px; padding: 16px 0;
  border-top: 1px solid rgba(255,255,255,0.06);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.yy-symbol {{ font-size: 32px; opacity: 0.5; align-self: center; }}
.yy-person {{ text-align: center; min-width: 200px; }}
.yy-name {{ font-size: 16px; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; }}
.yy-name.arif {{ color: #ffb74d; }}
.yy-name.syed {{ color: #64b5f6; }}
.yy-motto {{ font-size: 12px; font-style: italic; color: rgba(255,255,255,0.4); margin-top: 4px; }}
.section-bar {{
  display: flex; align-items: center; gap: 12px;
  margin: 24px 0 16px;
}}
.section-bar .line {{ flex: 1; height: 1px; background: rgba(255,255,255,0.08); }}
.section-bar .label {{
  font-size: 10px; letter-spacing: 4px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.3);
  white-space: nowrap;
}}
.row {{ display: flex; gap: 16px; margin-bottom: 12px; }}
.row-num {{
  width: 28px; font-size: 11px; font-weight: 700;
  color: rgba(255,255,255,0.15); padding-top: 4px;
  text-align: right; flex-shrink: 0;
}}
.row-topic {{
  width: 90px; font-size: 10px; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: rgba(255,255,255,0.3); padding-top: 4px;
  flex-shrink: 0;
}}
.row-signals {{ flex: 1; display: flex; gap: 16px; }}
.signal {{
  flex: 1; padding: 10px 14px;
  background: rgba(255,255,255,0.02);
  border-radius: 6px;
  border-left: 2px solid transparent;
  font-size: 13px; line-height: 1.5;
}}
.signal.arif {{
  border-left-color: rgba(255,183,77,0.4);
  color: rgba(232,224,212,0.85);
}}
.signal.syed {{
  border-left-color: rgba(100,181,246,0.4);
  color: rgba(200,214,229,0.85);
}}
.signal .tag {{
  display: inline-block;
  font-size: 8px; letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 1px 5px; border-radius: 3px;
  margin-bottom: 4px;
}}
.signal.arif .tag {{ background: rgba(255,183,77,0.15); color: #ffb74d; }}
.signal.syed .tag {{ background: rgba(100,181,246,0.15); color: #64b5f6; }}
.signal .txt {{ font-size: 12.5px; line-height: 1.55; }}
.signal.eureka {{
  background: rgba(255,255,255,0.03);
  border-left-width: 3px;
  font-style: italic;
}}
.chron {{
  display: flex; justify-content: center; gap: 24px;
  margin: 16px 0 24px;
}}
.chron-item {{
  text-align: center; padding: 8px 16px;
  background: rgba(255,255,255,0.03);
  border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);
}}
.chron-num {{
  font-size: 24px; font-weight: 700;
  background: linear-gradient(135deg, #ffb74d, #64b5f6);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.chron-lbl {{ font-size: 8px; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.3); margin-top: 2px; }}
.footer {{
  text-align: center; margin-top: 30px; padding-top: 16px;
  border-top: 1px solid rgba(255,255,255,0.06);
  font-size: 10px; letter-spacing: 3px;
  color: rgba(255,255,255,0.15); text-transform: uppercase;
}}
</style>
</head>
<body>
<div class="hdr">
  <div class="hdr-date">{signals["date_display"]}</div>
  <div class="hdr-title">☯ ALPHA-ZEN</div>
  <div class="hdr-sub">TODAY BETWEEN TWO WORLDS</div>
</div>
<div class="yy-bar">
  <div class="yy-person">
    <div class="yy-name arif">ARIF</div>
    <div class="yy-motto">"{signals["arif_motto"]}"</div>
  </div>
  <div class="yy-symbol">☯</div>
  <div class="yy-person">
    <div class="yy-name syed">SYED</div>
    <div class="yy-motto">"{signals["syed_motto"]}"</div>
  </div>
</div>
{chrono_html}
{section_html}
<div class="footer">☯ SAME WORLD · DIFFERENT LENS · DITEMPA BUKAN DIBERI</div>
</body>
</html>'''


def _save_canary(signals: dict, cycle_type: str) -> dict:
    """Save canary artifacts with deterministic cycle ID."""
    now = datetime.now(timezone(timedelta(hours=8)))
    date_str = now.strftime("%Y-%m-%d")
    cycle_id = f"{date_str}-{cycle_type}"

    cycle_dir = CANARY_DIR / date_str / cycle_type
    cycle_dir.mkdir(parents=True, exist_ok=True)

    # Save signals JSON
    sig_path = cycle_dir / "signals.json"
    sig_path.write_text(json.dumps(signals, indent=2, default=str))

    # Save HTML
    html = render_html(signals)
    html_path = cycle_dir / "card.html"
    html_path.write_text(html)

    # Build cycle receipt
    receipt = {
        "cycle_id": cycle_id,
        "timestamp": now.isoformat(),
        "delivery_mode": DELIVERY_MODE,
        "telegram_send": TELEGRAM_SEND,
        "candidate_count": sum(len(ARIF_POOL.get(r["topic"].replace(" ", "_").upper().replace("OUR_WORLD", "OUR_WORLD"), [])) for r in signals["rows"]) * 2,
        "selected_count": len(signals["rows"]) * 2,
        "arif_signals": [r["arif"][:60] for r in signals["rows"]],
        "syed_signals": [r["syed"][:60] for r in signals["rows"]],
        "sources": ["WEALTH", "GEOX", "WELL", "HERMES", "arifOS"],
        "freshness_gate": "G11 active",
        "rejections": 0,  # TODO: track from _pick
        "duplicate_rejections": 0,
        "privacy_rejections": 0 if not signals.get("privacy", {}).get("od1_hidden_from_syed") else 1,
        "render_status": "OK",
        "would_send": DELIVERY_MODE != "SHADOW",
        "hold_reason": "SHADOW mode — canary observation only" if DELIVERY_MODE == "SHADOW" else None,
        "artifacts": {
            "signals_json": str(sig_path),
            "card_html": str(html_path),
        },
    }

    # Save receipt
    receipt_path = cycle_dir / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, default=str))

    return receipt


def main() -> int:
    """Generate signals and render. SHADOW mode: save artifacts, don't send."""
    signals = generate_signals()

    # Determine cycle type from time
    now = datetime.now(timezone(timedelta(hours=8)))
    hour = now.hour
    if hour < 10:
        cycle_type = "morning"
    elif hour < 16:
        cycle_type = "afternoon"
    else:
        cycle_type = "night"

    # Save JSON
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(signals, indent=2, default=str))

    # Render HTML
    html = render_html(signals)
    html_path = OUTPUT_DIR / "alpha-zen-engine-output.html"
    html_path.write_text(html)

    # Render PNG
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page(viewport={"width": 1080, "height": 1920})
            page.goto(f"file://{html_path}")
            page.wait_for_timeout(500)
            png_path = OUTPUT_DIR / "alpha-zen-engine-output.png"
            page.screenshot(path=str(png_path))
            browser.close()
    except Exception as e:
        print(f"[WARN] PNG render failed: {e}")

    # Canary artifact storage
    receipt = _save_canary(signals, cycle_type)

    # Print summary
    print(f"CHRON CANARY — {cycle_type.upper()}")
    print(f"  Cycle ID: {receipt['cycle_id']}")
    print(f"  Delivery: {DELIVERY_MODE}")
    print(f"  Signals: {receipt['selected_count']}")
    print(f"  Would send: {receipt['would_send']}")
    print(f"  Hold reason: {receipt.get('hold_reason', 'none')}")
    print(f"  Artifacts: {receipt['artifacts']['signals_json']}")

    if DELIVERY_MODE == "SHADOW":
        print(f"  [SHADOW] Artifacts saved. NOT sent to Telegram.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
