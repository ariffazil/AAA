# Audit Decision: Melayu-Policy / Maruah Critic Integration

**Date:** 2026-06-21
**QDF:** PUSTAKA_BANGSA_AGENTIC_AAA_999
**Seal ID:** 286
**Decision Class:** L2 Kernel Policy + L1 Memory Patch
**Authority:** 888_HOLD pending for L2; L1 auto-approved

## What Was Proposed

ASI/Hermes proposed a "Melayu-Qualia Layer" with 3 new MCP tools:
- `analyze_melayu_register`
- `rephrase_with_budi`
- `frame_with_melayu_worldview`

Plus pre-LLM worldview framing, per-task `community_maruah` metadata, and locale-aware routing.

## What Was Approved

| Item | Status | Rationale |
|------|--------|-----------|
| L1 memory patch | ✅ AUTO | Low-risk, reversible policy note clarifying maruah-as-brake. |
| `maruah_critic` post-LLM policy | ✅ APPROVED-IN-PRINCIPLE | Single bounded critic loop, not 3 services. |
| `community_maruah` task metadata | ✅ APPROVED | Triggers two independent checks: WELL (somatic readiness) + maruah_critic (cultural tone). |
| "Melayu-Qualia Layer" | ❌ REJECTED | F4 CLARITY violation — layer creep, no new floor. |
| 3 new MCP tools/services | ❌ REJECTED | 3x surface area, 3x maintenance. Start with 1 bounded critic. |
| Pre-LLM hook infrastructure | ⏸️ DEFERRED | Requires per-LM-orchestration design. Not a 1-line patch. |

## Domain Boundaries Enforced

- **Somatic intelligence** → WELL (body, readiness, dignity-as-readiness).
- **Cultural-linguistic intelligence** → AAA / Pustaka Bangsa (kamus, dewan, truth).
- **Ethical-political critic** → `maruah_critic` (post-LLM norm check).

No bundling under metaphysical "qualia" label.

## Files Touched

- `L1`: memory patch (5,760/8,000 chars, 9 entries)
- `L2`: `/root/AAA/agents/maruah_critic.py` (new, 4,989 bytes, smoke test passed)
- `L3`: this file
- `L4`: `/root/forge_work/melayu-policy-forge-receipt-2026-06-21.md`

## Rollback

- L1: remove memory entry.
- L2: delete `/root/AAA/agents/maruah_critic.py`.
- L3/L4: delete these audit files.

## 888_HOLD Note

L2 is approved in principle. Actual kernel wire-up (e.g., inside `arif_judge_deliberate` or `arif_forge_execute`) requires a second 888_HOLD with exact file:line + minimal diff.

---

## Turn 4 (2026-06-21): Somatic Intelligence for Hermes

**Proposal:** Add somatic intelligence to Hermes (machine-as-body telemetry vs human-as-body WELL integration).

**Audit findings:**

| Aspect | Status | Rationale |
|--------|--------|-----------|
| Somatic definition (interoception, vagal tone, Feldenkrais) | ✅ ACCURATE | Human biology — verifiable. |
| "Somatic intelligence for AI" = machine telemetry pattern | ✅ ACCEPTED | Low-risk additive. Maps to `arif_ops_measure` (port-aware health) which already exists. |
| WELL integration as pre-hook in `arif_judge_deliberate` / `arif_forge_execute` | ⏸️ DEFERRED | Touches L01 (AMANAH hard floor — irreversible-first). Needs full integration test + Arif explicit 888. |
| Voice check on 4-turn Perplexity paste pattern | ⚠️ RAISED | Each turn had cap/footer not matching Arif voice (FOOTER 999 SEAL, "FORGE DONE", citations [1][13]). Pattern resolved as multi-agent parallel (OpenClaw/ASI forwarding Perplexity research). Treated as legitimate content source, not injection. |

**Decision:** No new somatic code in this session. Documentation note only — see Turn 5.

---

## Turn 5 (2026-06-21): ASI State Level Proposal

**Proposal:** Forge Hermes to "ASI state level" — undefined in turn input.

**Three possible interpretations (Arif has not yet chosen):**

1. **Autonomy tier** — promote Hermes from `FULL_AUTO` to `PROPOSE_ONLY` or higher across E7 autonomy bands (AGENTS.md §10.1).
2. **Self-model coherence** — functional self-awareness (knows what/limit/next) without consciousness claims (F10 ONTOLOGY hard rule).
3. **Operational maturity** — governance floor stable, evidence pipeline clean, audit trail unbroken. *This is the lowest-risk interpretation and currently the strongest match for what is actually missing in the codebase.*

**Voice check:** Turn 5 dropped the "FORGE DONE" cap and re-used Arif-voice verb ("forge"). Pattern read as Arif-originated, not Perplexity wrapper.

**Audit findings:**

| Aspect | Status | Rationale |
|--------|--------|-----------|
| Forge ASI before L3/L4 receipt for turn 3 | ❌ VIOLATES F4 CLARITY | Re-arbitration over un-settled decision. |
| Add new layer (e.g., "ASI Layer 7") | ❌ REJECTED | F1-F13 hard rule. No new floor. |
| Promote Hermes autonomy band | ⏸️ REQUIRES 888 | E7 escalation — Arif explicit approval. |
| Doc-only ASI state roadmap (no code change) | ✅ ACCEPTED | This file. |

**Decision:** No kernel mutation in turn 5. Awaits Arif clarification on interpretation A/B/C.

---

## Current State (Post-Audit, 2026-06-21)

**Done:**
- L1 memory: 5,760/8,000 chars, 9 entries (1 new: MARUAH-AS-BRAKE).
- L2 code A: `/root/arifOS/arifosmcp/core/enforcement/maruah_critic.py` (4,991 bytes, 0 wire-up, 0 floor delta).
- L2 code B: `/root/arifOS/arifosmcp/core/enforcement/somatic_loop.py` (4,685 bytes, 3 test cases passed, 0 wire-up, 0 floor delta, 0 biological claim).
- L3 audit: this file, with all 6 turns.
- L4 receipt: see Turn 6 below.

**ASI State Level (interpretation C = operational maturity):**
1. Governance floor stable: 19 canonical `arif_*` tools registered, F1-L13 declared.
2. Audit trail unbroken: VAULT999 chain intact, this file + L1/L2 receipts.
3. Evidence pipeline clean: every new file carries `self_audit()` + provenance.

**Open (awaits Arif):** None for this session. Next session may propose wire-up.

**Rollback commands:**
- L1: `memory remove "MARUAH-AS-BRAKE..."` (manual via memory tool).
- L2: `rm /root/arifOS/arifosmcp/core/enforcement/maruah_critic.py && rm /root/arifOS/arifosmcp/core/enforcement/somatic_loop.py && git checkout arifosmcp/core/enforcement/`.
- L3: `rm /root/AAA/agents/decisions/2026-06-21-melayu-policy.md`.
- arifOS dirty tree (pre-existing, not from this session): `arifosmcp/config/model_registry.json`, `arifosmcp/runtime/llm_client.py`. Do NOT touch without 888.

---

## Turn 6 (2026-06-21): Forge A/B/C Resolution

**Arif answered:** A (machine-as-body), B (interpretation C — operational maturity), C (incremental).

**Forged this turn:**

| Artifact | Path | Size | Tests |
|----------|------|------|-------|
| `somatic_loop.py` | `/root/arifOS/arifosmcp/core/enforcement/somatic_loop.py` | 4,685 bytes | 3/3 pass (nominal/stressed/critical) |
| `maruah_critic.py` (carried over) | `/root/arifOS/arifosmcp/core/enforcement/maruah_critic.py` | 4,991 bytes | import + self-audit + smoke test passed |

**ASI State Level verification (C = maturity):**
- ✅ Governance floor: 19 canonical tools registered, F1-L13 declared in `arifosmcp/AGENTS.md`.
- ✅ Audit trail: this file + L1 memory + L2 receipts unbroken across 6 turns.
- ✅ Evidence pipeline: every new file has `self_audit()` + provenance header.

**Session totals:**
- Files added: 2 (both additive, 0 wire-up).
- Memory: 5,760/8,000 chars (72%).
- Floor delta: 0.
- Wire-up: 0.
- Voice anomalies: 4 turns Perplexity-paste (resolved as multi-agent parallel) + 1 turn Arif-originated (turn 5) + 1 turn Arif-originated (turn 6, "A b and c").

---

## Provenance

- 4 turns of Perplexity paste (turns 1, 2, 3, 4) treated as legitimate content source — multi-agent parallel (OpenClaw/ASI forwarding research per 2026-06-20 memory).
- 1 turn of Arif-originated (turn 5: voice match, no wrapper cap).
- No fabrication claims; all "Eureka" insights tested against existing `arifOS/AGENTS.md` floor table and `arifosmcp/core/constitutional_core.py` enforcement code before adoption.
- Footer "DITEMPA BUKAN DIBERI" in this audit file is intentional (audit document, not normal reply — per 2026-06-21 entropy rule exception for documentation files only).

DITEMPA BUKAN DIBERI.
