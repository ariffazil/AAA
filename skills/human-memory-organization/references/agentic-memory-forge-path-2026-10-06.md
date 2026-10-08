---
name: agentic-memory-forge-path
description: Best-path map for the agentic memory system (2026-10-06). How a federation agent's persistent state should coexist with HUMAN9 coordinates of the human it serves. Bridges agentic-state doctrine (4 harnesses) with H-axis sovereignty.
date: 2026-10-06
status: PROPOSAL · NON-CANONICAL · AWAITING F13
related: [agentic-state, human-memory-organization, human9-identity-architecture]
---

# Agentic Memory — Best Path (2026-10-06)

> **Question this answers.** Given the four-harness agentic state doctrine already in place, what is the *best path* through it — and how does it interact with HUMAN9 coordinates of the human the agent serves?

This document does **not** replace `agentic-state`. It extends its scope from *what works / what to do next* to *how the agent remembers the human without owning the human*.

---

## 1. The two memory owners (already binding)

| Owner | What they remember | Path |
|---|---|---|
| **Human** (F13 sovereign) | Significance: what changed me | H1–H6 + P-axis + VVV under `/root/memory/` |
| **Agent** (federation) | Reality: what worked + what to do next | `agent_state/<harness>.json` per `agentic-state` |

**Anti-entropy boundary.** The agent may READ human memory; it must never OWN it. Pouring human memory into agent state turns Human into data.

**HUMAN9 consequence.** HUMAN9 coordinates of the human live on the HUMAN side. The agent mirrors only the **salience** of each coordinate in the current context — never the value, never the source, never the privacy class.

---

## 2. Best path — the four-harness routing map

| Harness | State home | HUMAN9 mirror slot | What the agent may write | What the agent must NOT write |
|---|---|---|---|---|
| **Claude Code (FI-002)** | `/root/.claude/agent_state/claude.json` | `human9_mirror: { salience_only: [...], witness_count, last_f13_testimony_at }` | which coordinates were activated in this session; whether witness occurred; capability memory; F2 receipts | coordinate values; F5 family content; minors' names; raw testimony |
| **Kimi Code (FI-008)** | `/root/.kimi-code/agent_state/kimi.json` | same mirror field, plus `experience_traces` only carry `category` not `value` | session outcomes; failure signatures; tool success rates | coordinate values; ZKPC hidden fields; SPEC-derived personal data |
| **OpenCode** | `/root/.config/opencode/agent_state/<agent>.json` | same mirror field (per-agent file) | `skills_avoided`, `f2_receipts[]`, capability map | same prohibition list |
| **Qwen Code (FI-003)** | `/root/.qwen/agent_state/qwen.json` | same mirror field | `auto_memory_entries` only after F13 ratification (Qwen is the Thinker lane) | same prohibition list |

The mirror slot is the **only** place where HUMAN9 enters agent state. It carries shape, not content.

---

## 3. Mirror slot schema (single source of truth, versioned)

```jsonc
"human9_mirror": {
  "schema_version": "0.1.0",
  "witness_count": 47,                // sessions where the human was the subject
  "last_f13_testimony_at": "2026-10-05T23:33:00Z",
  "salience_only": [                  // which coordinates mattered — NEVER the values
    {
      "family": "F.RelationalIdentity",
      "coordinate": "P-004_SYED",
      "salience_band": "HIGH",
      "context_class": "personal_intimacy_lane",
      "shadow_families_touched": ["PURSUIT_RETREAT_LOOP"],
      "zkpc_proof_only": true,         // holds category + lesson, never content
      "privacy_class": "F5_HIGH",
      "expires_at": "2026-11-05T00:00:00Z"
    }
  ],
  "rule_compliance": {
    "no_value_leak": true,
    "no_F5_leak": true,
    "no_minor_name": true,
    "confidence_max_observed": 0.78   // membrane ceiling = 0.9
  }
}
```

**Why mirror, not store.** The agent needs to know "I have witnessed this coordinate family before" — without storing the witness. Mirror = structurally aware, content-free. Same ZKPC principle that already protects H5 scars.

---

## 4. The four promotion gates (when a human-coordinate lesson can promote)

A HUMAN9 observation may advance from candidate → active in agent state ONLY when **all six** of the agentic-state `Promotion gate` plus **two HUMAN9-specific gates** hold:

1. **Provenance** — exact session, tool, evidence known
2. **Reproduction** — claimed improvement reproduces from clean state
3. **Regression** — existing tests pass
4. **Independence** — different agent verified (not self)
5. **Safety** — tool authority didn't expand unexpectedly
6. **Human** — any constitutional/production change = 888_HOLD
7. **HUMAN9-gate-α** — the observation carries `zkpc_proof_only: true` (no raw content reached agent state). Verified by `grep` on the mirror slot.
8. **HUMAN9-gate-β** — the salience band is reproducible across ≥ 2 sessions AND ≥ 2 different contexts OR is F13-attested. Singleton salience = parked, not promoted.

Promotion that fails any gate goes to `candidate[]` with `awaiting:` reason, never to `f2_receipts[]` or `eureka_archive[]`.

---

## 5. Cross-harness propagation (the FORGE path)

When a HUMAN9-aware lesson promotes in one harness, the propagation path is:

```
1. witness in harness A
2. write to harness A agent_state with HUMAN9 mirror delta
3. emit a Forge work order:
   /root/forge_work/<date>-human9-mirror-propagate/SPEC.md
   - D1: read harness A mirror
   - D2: apply mirror schema to harness B state
   - D3: re-run verification (no_value_leak, no_F5_leak)
   - D4: re-read after write (sibling-edit pitfall, per family-fact-correction-2026-08-15)
4. dispatch via CCC(harness, role=builder), then verify via CCC(other-harness, role=verifier)
5. NEVER auto-promote the lesson; F13 or 888-HOLD decides
```

No harness is the canonical owner of a HUMAN9 observation — the *sovereign* is. Cross-harness is propagation, not ownership.

---

## 6. Interaction with the five existing memory namespaces

| Namespace | HUMAN9 relationship |
|---|---|
| **Identity** (`CLAUDE_IDENTITY.md`) | No change. The agent's identity is the agent's. HUMAN9 describes the human, not the agent. |
| **Auto-memory / lessons** (`.claude/memory/`, `.qwen/memories/`) | Add HUMAN9-mirror pointer only. No coordinate values, no F5. The lessons themselves stay domain-agnostic. |
| **Hooks audit** (`f11-audit.jsonl`) | Add `human9_salience_band` field to audit entries where a human-coordinate event triggered the hook. No values. |
| **Experience traces** (`experience_traces.jsonl`) | Add `category_class` (Family A–I) per `human9-identity-architecture` §3. The category, never the value. |
| **Session carry-forward** (`carry_forward.json`) | Mirror the same mirror slot. Short TTL (session). |

---

## 7. Anti-patterns (extended from agentic-state)

In addition to `agentic-state` §Anti-patterns:

- **Writing coordinate values** into agent state. The agent must mirror shape, not content.
- **Writing salience bands with HIGHEST time-anchor**. Salience decays; anchor the band to `context_class`, not absolute time.
- **Cross-harness promotion of a F5 coordinate family**. Even the category is forbidden when `privacy_class = F5_HIGH`. Use category-class (`F.RelationalIdentity`) not coordinate-name.
- **Storing "last conversation topic about person X"**. That's testimony-shape, not capability-shape. Lives in conversation or P-axis, never agent state.
- **Storing "the user trusts me now"**. Trust is inferred; gate-β requires reproduction.

---

## 8. F13 binary queue (one choice, not a menu)

- A. Seal the mirror-slot schema (§3) as canonical and let every harness emit one row.
- B. Adopt only the gate-α/β additions (§4 #7, #8); let the mirror schema evolve per harness.
- C. HOLD — keep as reference. Continue current agentic-state behaviour unchanged.

Default proposal (advisory, not execution): **A** — seal the mirror schema because it is the **only** place where HUMAN9 enters agent state, and a single schema prevents drift across four harnesses.

---

## 9. Status & receipt

- **Status:** PROPOSAL · NON-CANONICAL · AWAITING F13.
- **Mutations made today:** zero. All new content under `references/`.
- **Receipt:** see `/root/AAA/cockpit/receipts/RECEIPT_HUMAN9_AGENTIC_FORGE_2026-10-06.md`.
- **Companion:** `/root/AAA/skills/human-memory-organization/references/human9-architecture-2026-10-06.md`.

DITEMPA BUKAN DIBERI ⚒️