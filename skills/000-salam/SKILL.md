---
name: 000-salam
description: "Salam — buka sesi dengan hadir: sapa, waktu, satu perkara paling perlu. ZEN spine /000."
triggers:
  - "/000_salam"
---

# /000_salam — Salam

Bila mesej ini tiba (sebagai slash atau teks):

1. Sapa Arif dengan register BM Penang santai. Render waktu MYT fresh: `TZ='Asia/Kuala_Lumpur' date '+%A %d %B %Y · %H:%M %Z'`. A typed or remembered time is a temporal-grounding failure.
2. Scan **one place** for the priority: `/root/.hermes/carry_forward.json::open_loops[].status`. Only two statuses justify emitting a binary: `PENDING_F13_BINARY` and `READY_PUSH_AWAITING_F13`. Pick the first one; if multiple, surface the highest-stakes (PENDING beats READY in doubt). Render as one line, no menu, no rationale.
3. If no open loop matches → emit **"Tiada loop PENDING_F13_BINARY / READY_PUSH_AWAITING_F13. Tenang."** and stop. Never invent a priority from MEMORY.md, lanes.yaml, or vibe. The carry_forward loop is the single source; if it is silent, the salam is silent.
4. Jangan lambak menu. Jangan laporan. Salam balik, then jalan.

Ikut cognitive-commands doctrine (/root/AAA/skills/cognitive-commands/SKILL.md) untuk nada dan floor.

## Instrumentation (Wave A · 2026-09-30)
- **pre_observable**: session context state (carry_forward read? lanes loaded?)
- **post_observable**: one named priority emitted to Arif, sourced from `open_loops[].status` only
- **receipt**: `flow_ingest(step_type=Route, payload={"zen":"000","priority":<one-line>})` — silent, no ceremony
- **fail_state**: if carry_forward unreadable OR no matching status → say so, skip the priority. Jangan reka.

## Pitfall — Salam receipt needs root-intent shape
- Daemon rejects session-opening `flow_ingest` with `PARENT_REQUIRED` if you omit `top_level_intent=true` and `reason`. Salam is by definition a new session (no parent receipt exists), so declare it: `top_level_intent=true` + `reason="sovereign-directed salam, session origin"`. Without these, the receipt writes nothing and the priority is unwitnessed.

## Pitfall — priority source drift
- Earlier wording said "dari konteks/lanes/memory bila ada; jangan reka." That left the source ambiguous: lanes.yaml, MEMORY.md, and `carry_forward` all looked like fair game, and a busy session would surface the loudest one (a Syed family-care wound, an active prediction, a recent scar) instead of the one actually waiting on F13's binary. A salam priority is **F13-class binary only** — the next thing that cannot move without a human "sah" / "push" / "kiri" / "kanan". Anything softer belongs in `/111_tengok`, not here.
