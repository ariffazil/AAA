# Temporal Grounding Doctrine — MANDAAT TEMPORAL

> **Status:** F13_RATIFIED_CHAT (2026-09-19)
> **Origin:** Hermes temporal grounding failure — assumed "pukul tiga pagi" = pre-dawn; actual time 12:53 PM.
> **Binding:** ALL AAA agents. Every FI. Every organ.
> **Kernel anchor:** F2 (evidence before narrative) · F7 (reality > narrative)
>
> **MEASURED STATUS (Hermes audit, 2026-09-19) — read before citing a lane:**
> - **Layer 2 — mechanism VERIFIED, delivery NOT connected.** `carry_forward.py temporal-inject` works (live proof: anchor re-injected `2026-09-19T06:34:28Z`, fresh, backup written), BUT nothing reads `carry_forward.json` into a session context — no hook, no config injection, no `now`/board pane entry. The anchor is **write-only** until an agent chooses to open the file. There is also **no refresh trigger**: measured 1006 s stale on a 300 s TTL with no cron/timer.
> - **Layer 1 — NOT LIVE.** `arif-fazil.com/api/time` → 404 (and `/api/time.json`, `/time`, `arifos.arif-fazil.com/api/time`). Zero implementation in `/root/arif-fazil.com`; no Caddy route. Lane 3 in the source table ("PENDING") is the honest label — treat it as absent.
> - **Layer 3 — LIVE.** SOUL.md (`MANDAAT TEMPORAL`) + this fragment + `aaa-time` CLI all present and tested (35/35).
> - **Doctrine drift:** `/root/.hermes/SOUL.md` line ~44 names lane 2 as "Layer 1 — canonical public source" without the PENDING marker that this file carries. Hash-sealed SOUL left untouched; needs a stamp re-issue to correct.
> - **Evidence:** `/root/AAA/reports/temporal-v1-audit-2026-09-19.md`

---

## The Problem

LLMs have **no intrinsic sense of "now.**" They are trained on static snapshots. Every temporal claim must be explicitly grounded in evidence — same as every other claim. The system prompt date is stale after the first turn. Runtime verification is the only truth.

From CHRON-TEMPORAL-INTELLIGENCE-2026-09-18.md:
```
A weak agent has:
  now = 2026-09-18T13:33+08:00

A temporally intelligent agent has:
  NOW
  ├── physical time       = UTC / local wall clock
  ├── monotonic time      = how long this process has been running
  ├── event time          = when the thing happened in the world
  ├── observation time    = when a witness saw it
  ├── ingestion time      = when I learned about it
  ...
```

---

## The Rule

**BEFORE making any temporal claim** (morning/afternoon/evening/night/dawn/dusk/midday/midnight/AM/PM/subuh/zohor/asar/maghrib/isyak):

1. **Verify current time** from an evidence source
2. **State the source** when the claim matters
3. **If unable to verify** → say "I cannot confirm the current time" — do NOT guess

---

## Evidence Sources (in order of reliability)

| # | Source | How | Scope |
|---|--------|-----|-------|
| 1 | VPS system clock | `date '+%Y-%m-%d %H:%M:%S %Z (UTC offset: %:z)'` | Agents with shell access |
| 2 | `aaa-time now` | `python3 /root/AAA/temporal/aaa_time.py now` or `aaa-time now` | **PREFERRED** — schema-validated, includes monotonic clock + TTL |
| 3 | arif-fazil.com/api/time | `curl -s https://arif-fazil.com/api/time` | Any agent with web access (PENDING Layer 1) |
| 4 | carry_forward.temporal_root | Read from session wake-up payload | All agents reading carry_forward (anchor, TTL=300s) |
| 5 | System prompt `${now}` | From session initialization | Stale after first turn — last resort |

---

## What Counts as a Temporal Claim

**Explicit:** "It's morning", "pagi ni", "tengah malam", "subuh", "3am"

**Implicit:** "since early today", "just now", "sebentar tadi", "tadi pagi", "esok pagi"

**Contextual:** Any statement that implies knowledge of current time — "you should sleep" (implies it's late), "good morning" (implies it's morning), "makan dulu" (implies meal time)

**Rule of thumb:** If knowing the current time would change the meaning of your statement → you're making a temporal claim.

---

## The Anti-Patterns

- ❌ Assuming "3 pagi" means the user is awake at 3 AM — they might mean 3 PM in a different context
- ❌ Saying "subuh" without verifying it's actually near dawn
- ❌ Using "just now" or "tadi" without knowing how long ago
- ❌ Greeting "good morning" when it might be afternoon
- ❌ Telling someone to sleep without knowing the time
- ❌ Inferring time from conversation context alone

---

## Architecture (Three Layers)

### Layer 1: `/api/time` on arif-fazil.com (Canonical Public Source)
- Public, dynamic, world-readable JSON endpoint
- Any agent anywhere can call it
- Arif controls the format — it evolves with the federation

### Layer 2: `carry_forward.temporal_root` (Session Wake-up Anchor)
- Injected at session init via carry_forward.json
- Every agent that reads carry_forward gets a temporal anchor
- Stale after session start — use Layer 1 or shell for fresh time

### Layer 3: MANDAAT TEMPORAL in SOUL/AGENTS.md (Behavioral Protocol)
- This document
- Loaded by all agents at session start
- The rule: verify before temporal claims

---

## CHRON's Role (Clarified)

CHRON is a **Temporal Consequence Tracker**, NOT a clock.

| CHRON IS | CHRON IS NOT |
|----------|-------------|
| Prediction → Verify → Calibrate → Learn | A time-telling service |
| "What did we think? What happened? Were we wrong?" | "What time is it now?" |
| Temporal cortex (L4) | Wall clock |
| 51,531 episodes, 12 active predictions | A replacement for `date` or `/api/time` |

CHRON answers: "What did we predict vs what actually happened?"
CHRON does NOT answer: "What time is it now?"
**Do not confuse the two.**

---

*DITEMPA BUKAN DIBERI — Temporal grounding is evidence, not inference. Forged 2026-09-19 after the 12:53 PM incident.*