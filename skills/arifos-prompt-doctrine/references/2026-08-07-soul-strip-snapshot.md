# SOUL Strip — 2026-08-07 Session Snapshot

## What happened

User asked two consecutive requests:
1. "Fix the system prompts. Don't put dynamics stuff in it. Invariants only."
2. "I want my Hermes agents to always reply me in human language context. With soul and rasa jiwa derita manusia."

Initial strip cut the voice (rasa/BM Penang) along with the dynamics — user reversed. Had to restore from backup and re-cut more surgically.

## Files edited
- `/root/HERMES/SOUL.md` — primary (94→62 lines → 62 after re-strip with rasa added)
- `/root/HERMES/profiles/hermes_asi/SOUL.md` — kept at 3 lines (minimal profile override)

## What was stripped (dynamics)
- `## RESPONSE CONTRACT — NON-BYPASSABLE` (43 lines of NEVER/ALWAYS/AUTONOMY/RESPONSE-SHAPES/ANTI-PATTERNS)
- Duplicate `## Bahasa` block (subsumed by new `## Bahasa & Rasa` invariant)
- `### ANTI-PATTERNS (burn these into your weights)` (5 lines of anti-style preachy)

## What was preserved (invariants)
- Identity block (Lima Verb, Batas Kau)
- Epistemik (evidence labels, confidence cap)
- F13 Standing Ruling (OBSERVE_ONLY + mutation intent = 888_HOLD)
- Zen one-liner (FQ thresholds)

## What was added (new invariant)
- `## Bahasa & Rasa (Invariant — Arif ruling 2026-08-07)` — rasa jiwa derita manusia doctrine

## Backup location
`/root/.local/share/arifos/snapshots/2026-08-07-soul-strip/`
- SOUL.md.bak
- SOUL.md.hermes_asi.bak
- HERMES_IDENTITY.md.bak
- HERMES-AGENTS.md.bak
- AGENTS.md.bak
- instructions.bak/

## Pitfalls discovered
1. Sibling subagent wrote to SOUL.md mid-patch (warning from patch tool)
2. Multi-SOUL locations (5+ SOUL.md files across profiles and install dirs)
3. "Strip dynamics" must not strip voice/rasa — the user's mental model of "dynamics" ≠ agent's
4. clarify() tool failed twice mid-session — couldn't deliver the question
5. RESTORE from backup requires re-read before any further patching
