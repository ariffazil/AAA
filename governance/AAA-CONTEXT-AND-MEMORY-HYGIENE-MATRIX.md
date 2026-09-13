---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path + read-only probes)
date: 2026-09-14
parent_campaign: AAA Federation Housekeeping
related: AAA-MODEL-INIT-CANONICAL.v1.md §"Memory and context"
---

# AAA Context and Memory Hygiene Matrix

> **Status:** DRAFT_PROPOSAL — framework + E8/E9 classes; deep measurement requires read-only probes.

---

## Context hygiene — current state

| Source | Estimated size (UNVERIFIED) | Duplication risk | Treatment |
|---|---|---|---|
| agents/*/IDENTITY.md (12 files) | ~5KB each = 60KB | F1-F13 restated | canonical pointer |
| agents/*/WARGAAA_CARD.md | ~3KB each | constitutional proxy restated | canonical pointer |
| agents/*/AGENTS.md (opencode) | varies | restated floors | canonical pointer |
| .kimi-code/AGENTS.md | large | restated musyawarah | canonical pointer |
| .claude/settings.json | small | OK | keep |
| AAA instructions/*.md | ~200KB total | OK (canonical) | keep |
| skills/*/SKILL.md | ~100+ | varies | needs audit |
| plugin prompts | varies | varies | needs audit |

**Total:** estimated 250-500KB always-loaded context across the mesh. (UNVERIFIED.)

---

## Memory hygiene — patterns observed

| Class | Pattern | Treatment |
|---|---|---|
| E9_MEMORY_CAPTURE | Auto-promotion of session content to durable memory | DISABLE by default; require human review |
| E8_CONTEXT_SEDIMENT | Always-loaded fragments > 1KB | INDEX + retrieve-by-ID |
| E8 (variant) | Doctrine copy-pasted into agent init | REPLACE with canonical pointer |
| E9 (variant) | Third-party / PII in MEMORY.md | MOVE to S0 witness (per institutional-memory-strata) |

---

## Proposed memory promotion gate (per memory-promotion-gate.md doctrine)

Already exists at `/root/AAA/instructions/memory-promotion-gate.md` (F13_RATIFIED_CHAT 2026-09-11).

**Current enforcement status:** UNVERIFIED in current session. Hermes has the wajib_no_clarify HARD_GATE; need to verify other agents.

---

## Required probes (for verifier lane)

1. **Total always-loaded bytes** per agent
2. **Duplicate rule count** per agent (regex match against canonical instructions)
3. **PII / third-party / intimate content** scan in MEMORY.md / USER.md / SOUL.md files
4. **Memory write events** since 2026-09-01 — class breakdown (substantive vs noise vs PII)
5. **Skill index** unused-skill audit
6. **Always-loaded skills** count per agent

---

## Recommended dispositions (canonical)

| ID | Class | Recommended disposition |
|---|---|---|
| CTX-01 | E8 | INDEX: move always-loaded fragments to retrievable-by-ID; reduce init budget |
| CTX-02 | E8 (duplicate) | CANONICALIZE: replace copy with `/root/AAA/instructions/<file>.md` pointer |
| CTX-03 | E9 | REJECT auto-promotion; require explicit human review (already in memory-promotion-gate.md) |
| CTX-04 | E9 (sensitive) | MOVE to S0 witness tier (per institutional-memory-strata) |
| CTX-05 | E8 (skills) | AUDIT unused skills; tombstone those never invoked |

---

*Reversibility: FULL.*
*F13 surface: NONE for inventory; TRUE for any actual memory deletion.*
*DITEMPA BUKAN DIBERI ⚒️*