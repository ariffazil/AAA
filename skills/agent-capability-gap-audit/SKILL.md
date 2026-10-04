---
name: agent-capability-gap-audit
description: "Use when auditing agent skill gaps or prune plans."
version: 1.0.0
author: Hermes (aaa-hermes)
license: MIT
category: autonomous-ai-agents
metadata:
  hermes:
    tags: [audit, skills, gap-analysis, telemetry, reality-adapters]
    related_skills: [federation-asset-probe, arifos-cron-ops, my-reality]
---

# Agent Capability Gap Audit

## When to Use

- User asks "what skills/capabilities is my agent missing?" (any harness: Hermes, OpenClaw, sibling CLIs)
- A prune plan, skill-count claim, or council proposal arrives and needs falsification before action
- Deciding build vs wire vs repair for a proposed capability

Class of work: determine what an agent is ACTUALLY missing, with evidence, before forging or pruning anything. Born from the 2026-08-15 Hermes reality-layer audit: a sibling "72→10 prune plan" audited the WRONG installation (ghost audit), and a council proposed 10 tiers of features with zero consumers. Both failed the same way — narrative before probe.

## Core doctrine

1. **Demand before inventory.** Count real user demand first (state.db telemetry). A skill bank can be thick where nobody lives and thin where users live daily.
2. **Falsify every "missing" claim.** Each candidate gap is one of four states — the fix differs radically:
   | State | Meaning | Fix |
   |---|---|---|
   | **COVERED** | Skill/organ already exists (grep bodies, not memory) | nothing |
   | **DORMANT** | Code exists, zero consumers (grep imports) | wire it — capital activation, not new build |
   | **BROKEN WIRE** | Pipeline exists + enabled, engine/dependency missing | repair > build |
   | **ABSENT** | No trace anywhere, but demand + live source verified | forge adapter |
3. **No abstract feature without concrete consumer** (F13 ruling 2026-08-15). Only forge where a real paying customer exists (live cron, measured traffic). Vision-tier proposals go to the graveyard ledger until reality picks them.
4. **Repair > wire > build.** Cheapest entropy path wins.

## Method (5 steps)

1. **Demand telemetry** — query the agent's state.db for user-message keyword counts:
   ```sql
   select lower(content) from messages where role='user'
   ```
   Aggregate keywords in Python (never dump raw content). High-count + no-native-surface = candidate gap.
2. **Live inventory** — count `SKILL.md` on the surface the agent ACTUALLY loads (`$HERMES_HOME`/profile path from running PID, not assumptions). Beware ghost audits: multiple installs coexist (bundled vs default ~/.hermes vs live profile — 289/442/476 observed).
3. **Per-gap falsification** — for each candidate:
   - API: `curl -sL` the source from the VPS itself, check HTTP code + parse shape (redirects need `-L`; e.g. Aladhan 302s).
   - Dormant code: `grep -rl <module>` for imports across organs — 0 imports = parked prototype.
   - Config/wiring: check config sections, venv deps (`pip show` / import in venv python), lazy-recheck behavior in source.
4. **Classify** into the four states; rank by leverage (existing demand + existing pipeline + single missing dependency = highest).
5. **Report RM-cost framing** where cost is relevant (user rejects token units — RM/month first, tokens footnote only).

## Verified endpoint bank + session evidence

- `references/malaysia-api-verified-bank-2026-08-15.md` — live-probed MY reality APIs (prayer/weather/AQI/FX/gold/holidays/fuel) with response shapes and quirks.

## Pitfalls

- **Ghost audits.** Verify the audited surface is the live one (PID → HERMES_HOME → inode check) before trusting any "skill count N" claim from a sibling or council.
- **Council vision = stub fabrication risk.** Multi-tier proposals violate the concrete-consumer rule by default; extract only the tier with existing consumers.
- **Inbound vs replied-to media differ.** Replied-to audio is cached + annotated as a file path note; only fresh inbound voice enters the STT pipeline. Don't claim "voice works" from a replied-to test.
- **Round-trip STT test leaks.** Generating test audio via a TTS tool that auto-delivers MEDIA: sends a voice bubble into the live user chat. Generate test audio via CLI to /tmp instead.
- **Provider-absence ≠ feature-off.** A missing transcription engine with an enabled pipeline is a BROKEN WIRE (install dependency), not a missing skill; upstream lazy-dep code re-checks per call, so an install can heal without service restart — verify in source before scheduling one.
- **API probes can fail on shape, not liveness.** 302 (follow redirects), nested objects (BNM `data[].rate.middle_rate`), empty-year datasets (holiday APIs return 204 until data exists). Read raw response before declaring a source dead.

## Related

- `federation-asset-probe` — breadth-first "does X exist" recon; this skill adds demand telemetry + four-state classification.
- `arifos-cron-ops` — consumers that justify adapters (cron jobs are the paying customers).
- `my-reality` — the adapters forged from this audit's Tier 0 (Malaysia daily reality).

*Forged 2026-08-15 from the Hermes reality-layer audit session. DITEMPA BUKAN DIBERI.*
