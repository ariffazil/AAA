---
name: agentic-genome-species
description: "9-function cognitive genome + species taxonomy for arifOS Federation. Use when operating on AAA registries, agent cards, GENESIS doctrine, EUREKA SIX PLANE, kernel verb surfaces, harness routing, or when a new runtime/coding tool arrives in the federation and needs a species binding. Triggers: 'species', 'genome', 'atlas', 'phenotype', '9-agent', '8≠9', 'openclaw-zen', 'opencode-zen', 'hermes-zen', 'blast radius'."
version: "2026-08-08-v1"
forged: "2026-08-08 by Hermes ASI under F13 SOVEREIGN directive"
canonical:
  doctrine: "/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md"
  genesis: "/root/arifOS/GENESIS/011_FEDERATION_AGI_SUBSTRATE.md"
  harness_routing: "/root/AAA/instructions/reality-first.md"
---

# Agentic Genome & Species Taxonomy

> **EUREKA (2026-08-08, F13 SOVEREIGN):** Runtimes are not separate agents with separate governance. They are phenotype instances of a universal cognitive genome.

## Core doctrine

AAA = Constitution (the authority layer, NOT cognition).
9-function Cognitive Atlas = universal genome (what ALL intelligence must contain).
Runtimes = species instances (phenotypes that express the genome with different weights).

## The 9-function genome (Cognitive Atlas)

```
REALITY          INTELLIGENCE       GOVERNANCE
000 Observer  →  333 Thinker   →   666 Auditor
111 Explorer  →  444 Orchestrator→  777 Executor
222 Architect →  555 Verifier  →   888 Judge
                                       ↓
                                   999 Witness
```

| # | Function | Kernel verb (today) | Status |
|---|---|---|---|
| 000 | Observer | `arif_observe` | ✅ exists |
| 111 | Explorer | — | ❌ organ-level capability |
| 222 | Architect | — | ❌ organ-level capability |
| 333 | Thinker | `arif_think` | ✅ exists |
| 444 | Orchestrator | `arif_route` | ✅ exists (semantic rename: route → orchestrate) |
| 555 | Verifier | `arif_memory` (partial) | ⚠️ memory ≠ verification (needs split) |
| 666 | Auditor | — | ❌ collapsed into 888 today |
| 777 | Executor | `arif_forge` | ✅ exists |
| 888 | Judge | `arif_judge` | ✅ exists |
| 999 | Witness | `arif_seal` | ✅ special authority layer, NOT a normal agent |

**8≠9 by design:** kernel has 8 verbs; atlas has 9 functions. Genome exceeds transcription machinery. Promotion to 11 verbs (adding 111/222/666) requires: compression causes constitutional harm. Current state: 111/222/666 are organ-level capabilities, not kernel verbs. See promotion criterion in `EUREKA_SIX_PLANE_EXECUTION_LOOP.md` §3.

## ART / ACT / AUTH gates

```
AAA
├── ART    (cognitive)    000 · 111 · 222 · 333 · 444
├── ACT    (operational)  555 · 666 · 777
└── AUTH   (authority)    888 · 999
```

Every level of abstraction (federation → species → task → session) contains the full ART+ACT+AUTH genome, but with different weights. This is the fractal kernel property.

## Species taxonomy (current instances)

| Species | Expression weights | Primary domain |
|---|---|---|
| **OpenCode-Zen** | 222=HIGH, 333=HIGH, 777=HIGH | Coding, structure, execution |
| **Hermes-Zen** | 111=HIGH, 444=HIGH, 555=HIGH, 666=HIGH | Sensing, orchestration, verification, governance |
| **OpenClaw-Zen** | 444=HIGH, 777=HIGH | Personal ops, execution, plugins |
| **GEOX-Zen** | 000=HIGH, 222=HIGH, 555=MED | Earth intelligence, structure, verification |
| **WEALTH-Zen** | 222=MED, 333=MED, 555=HIGH | Capital verification, evidence |
| **WELL-Zen** | 000=HIGH, 666=HIGH, 555=MED | Human observation, governance check |

**APEX is NOT a species.** 888/999 = authority layer, not cognition. Not an agent, not a phenotype. A chair, not a person.

**888 Judge in OpenCode-Zen = self-check** (not full constitutional judge — that stays at federation level only).

## What collapses under this doctrine

| Before (entropy) | After (genome) |
|---|---|
| 17+ agent cards, 10 FI slots | 6 species + organs + extensions |
| Separate governance per harness | One species constitution per species |
| "Is Kimi 333 or 777?" identity crisis | Kimi = OpenCode-Zen instance; weights say 222/333/777 |
| Per-agent A2A binding | Species-class A2A binding |

## Blast radius (when forging this upgrade)

**Canonical blast-radius inventory:** `references/genome-species-blast-radius-2026-08-08.md`

Summary categories (see reference for full file list):
1. **Kernel verbs** — 13 mega-tool files + tools_sot.yaml + surface governance scripts (HIGH)
2. **Federation contracts** — AAA_FEDERATION_CONTRACT_v0.1.2.yaml + PRINCIPAL_AGENT.md (HIGH)
3. **Registries** — AGENTS_UNIFIED.yaml + agents.yaml + bindings.yaml + forge_instruments.yaml (HIGH)
4. **A2A agent cards** — 14 harnesses + 5 lanes + 5 organs + 12 functions + 7 extensions (MEDIUM-HIGH)
5. **Prompts** — INIT.md + AAA-ZEN-ALIGNMENT.md + UNIVERSAL_BOOT.md (MEDIUM)
6. **GENESIS doctrine** — 011_FEDERATION_AGI_SUBSTRATE.md (MAJOR rewrite) + 030/040/041/045/046 (MEDIUM)
7. **Instructions fragments** — agentic-architecture.md + autonomy.md + topology.md + re-render via render-agents.sh (MEDIUM)
8. **Renderer** — opencode_render.py:155 BROKEN today — fix first (prerequisite)
9. **Skills** — ~10 of 150 require rewrite; rest transparent at species level (LOW)
10. **Model routes** — add `species_binding` field to AGENT_MODEL_MAP.json (LOW)
11. **A2A JS modules** — 12 files add species_id routing (LOW-MEDIUM)
12. **VAULT999/carry_forward/atlas333** — add species_id to receipt schema (LOW)
13. **Public surfaces** — llms.json, a2a/manifests, agent-taxonomy doc (LOW)

### Pre-forge baseline pattern (operational recipe)

Before a sibling agent forges this upgrade:

1. **CHAOS TRACE** — dirty repos, drift probe, seal-chain age, carry-forward state, organ health.
2. **Record** — commit the baseline so post-forge audit is a diff, not a memory.
3. **Post-forge:** diff against baseline → re-run drift → audit per §11.3 (F11 auditability + F12 injection defense) → SEAL or 888_HOLD.
4. **Delta S = 0** on trace-only; mutation only after SEAL verdict.

### Order of operations (canonical)

1. Fix `opencode_render.py:155` (audit cannot run without working drift detector).
2. **Load-bearing decision:** expand kernel to 9+ verbs OR keep 3 missing functions as organ-level.
3. Rewrite `AGENTS_UNIFIED.yaml` to species-first.
4. Update fragment `agentic-architecture.md` → re-render adapters via `render-agents.sh`.
5. Update GENESIS `011_FEDERATION_AGI_SUBSTRATE.md` (genome canon).
6. Re-emit A2A public manifest.
7. SEAL via `arif_seal`.
8. `make prove` — full federation validation.

## Agent-card registry — canonical tree (verified 2026-08-09)

**Canonical source is `/root/AAA/a2a-server/agent-cards/`** (schema `arifOS/agent-card/v2.2.0`). The older `/root/AAA/agent-cards/` (root-level) is **LEGACY** — its README says so explicitly; retained only for `extensions/`, `functions/openclaw.json`, and audit artifacts. Never edit/create cards in the legacy path.

## AAA 3-layer geometry (sealed FINAL 2026-08-09, F13)

Arif compressed proposed structures from 7→4→3 in one session. The sealed final:

| Layer | Contents | Mutability |
|---|---|---|
| **L1 IDENTITY** | 333-AGI · 555-ASI · 888-APEX (lane cards) | Sealed; 888 verdict only |
| **L2 HARNESS** | FI runtimes (opencode PRIMARY, kimi/claude/codex/grok…) | Swap freely |
| **L3 BINDING** | forge + functions + roles + organs + pillars + extensions | Attachment layer |

**Classification SOT:** `CIV33_LAYERS` map in `/root/AAA/a2a-server/agent-card-registry.js`. Physical dirs UNCHANGED — AAA is catalog only (DISPLAY_ONLY), classification only.

**WHO/WHERE vs WHICH:** provider/model changes (FED zen) are WHICH-engine — runtime layer only, never agent cards (WHO). Provider is a FIELD inside each harness card, not a separate axis. FED is plumbing — separate from AAA geometry entirely.

**Blueprint-first rule (Arif correction):** when Arif asks "what should X be" / "can we compress?" / "show me the geometry", present the DESIGN first and get his nod before touching any file. "Nope. Show me how X SHOULD BE" = design request, not execution order. Arif always compresses structure proposals — start at 3 orthogonal layers.

The 7 card classes (all under `a2a-server/agent-cards/`):

| Class | Dir | Contents (verified 2026-08-09) |
|---|---|---|
| identity | `identity/` | 333-AGI, 555-ASI, 888-APEX — lane bindings + role-binding skills (Δ MIND / Ω HEART / ΦΙ JUDGE) |
| harnesses | `harnesses/` | 13 runtime cards: opencode (PRIMARY), claude-code, codex, kimi-code, grok-build, copilot, copilot-cli, gemini-cli, qwen-code, antigravity, continue-cli, aider, openclaw |
| forge | `forge/` | fi-001-opencode, fi-008-kimi-code, forge-bot (execution tier bindings) |
| extensions | `extensions/` | hermes-asi, hermesarifos-bot, makcikgpt (peripheral cards) |
| functions | `functions/` | openclaw.json (gateway function card, model MiniMax-M3) |
| roles | `roles/` | aaa-architect, aaa-auditor, aaa-engineer, aaa-gateway, hermes-ops (AAA-side ops roles) |
| organs | `organs/` | arifos, aforge, geox, wealth, well |

Per-runtime card requirements (what a complete runtime needs: harness + identity binding + forge + extension/function + kernel skills) — full table with models: `references/agent-card-registry-2026-08-09.md`.

**Model-map SOT correction:** `AGENT_MODEL_MAP.json` (`/root/AAA/registries/models/`) is **deprecated 2026-07-24** — replaced by `/root/.config/federation-models.json` (has `agents[]` with per-agent `primary_model` + `fallback_chains`). Verified live 2026-08-09: opencode→`litellm-federation/opencode`, hermes→`minimax/MiniMax-M3`, openclaw→`deepseek/deepseek-v4-pro`, grok→`xai/grok-4.5`, kimi→`kimi-k3`, codex→`deepseek/deepseek-v4-pro`. Any audit or forge touching model routes must read the replacement file, not the deprecated one.

**Kernel skills every runtime must carry** (9 substrate-primitive, commit `2a64c37e`): `KERNEL-reality-skills` (F2), `KERNEL-sovereign-recognize` (F13), `KERNEL-session-inhabit` (INIT→OBSERVE→JUDGE→SEAL), `RSI-recursive-improvement` (ΔS<0), `KERNEL-trinity-33`, `SHADOW-diagnostic`, `CLAIM-verification-gate`. Plus lane role-binding skill: 333=role-binding-delta, 555=role-binding-omega, 888=role-binding-phi.

## Per-runtime agent-card requirements (audited 2026-08-09)

Canonical tree: **`/root/AAA/a2a-server/agent-cards/`** (schema v2.2.0). A runtime's card set = **identity lane + species binding + harness/forge-instrument card + extension/role cards**:

| Runtime | Species | Cards required |
|---|---|---|
| Hermes | hermes-zen | `identity/555-ASI.json` + `extensions/hermes-asi.json` (runtime_harness=hermes_cli, anchor SOUL.md, MCP creative+media) + `extensions/hermesarifos-bot.json` + `roles/hermes-ops.json` (+ `roles/aaa-{architect,auditor,engineer,gateway}.json` for A-ROLE switching) |
| OpenClaw | openclaw-zen | `functions/openclaw.json` (27 skills) + `harnesses/openclaw.json` (21 skills). No identity lane — correct, it's a function species |
| OpenCode | opencode-zen | `identity/333-AGI.json` + `forge/fi-001-opencode.json` (FI-001 PRIMARY, bound_to 333-AGI) + `harnesses/opencode.json` |
| Kimi Code | opencode-zen | `forge/fi-008-kimi-code.json` + `harnesses/kimi-code.json` |
| Claude Code · Codex · Grok · Qwen · Copilot · Gemini CLI · Antigravity · Aider · Continue | opencode-zen | `harnesses/<runtime>.json` only (FI-002..007 registered in AGENTS_UNIFIED.yaml but **no forge card artifact** — known gap) |

Shared substrate: `identity/888-APEX.json` (chair, not agent — HARAM-8≠9), `organs/*.json`, `forge/forge-bot.json`.

**Doctrine:** harnesses are NOT species — they are forged instruments (FI-001..008) with `species_proxy: opencode-zen`; they inherit the species W-vector and have no independent one. Never create a new species card for a coding tool (Pitfall 3).

**Known drift (2026-08-09):** `AGENTS_UNIFIED.yaml` canonical_card fields still point at legacy `agent-cards/identity/...` paths (0 refs to a2a-server); only fi-001 + fi-008 have forge cards; OpenClaw harness card has empty `species: {}` (half-migrated). Full matrix: `references/agent-cards-per-runtime-2026-08-09.md`.

## Key files for this class

| File | Role |
|---|---|
| `/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` | Phenotype Substrate doctrine (+106 lines, §3) |
| `/root/arifOS/GENESIS/011_FEDERATION_AGI_SUBSTRATE.md` | Federation AGI substrate canon (MAJOR rewrite target) |
| `/root/AAA/instructions/reality-first.md` | Harness Routing + ART/ACT/AUTH gates (+68 lines) |
| `/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` §3 | 8≠9 promotion criterion |
| `/root/AAA/agents/HEXAGON.yaml` | Current Trinity architecture (pre-genome) |
| `/root/AAA/contracts/PRINCIPAL_AGENT.md` | Principal taxonomy (rewrite target) |
| `/root/AAA/registries/AGENTS_UNIFIED.yaml` | SOT agent registry (rewrite target) |
| `/root/AAA/a2a-server/agent-cards/*.json` | **Canonical** agent-card tree (v2.2.0) — identity/, harnesses/, forge/, extensions/, functions/, roles/, organs/ |
| `/root/AAA/agent-cards/` | **LEGACY** card tree — do not edit (README declares supersession) |
| `/root/.config/federation-models.json` | **Current** per-agent model map (AGENT_MODEL_MAP.json is deprecated) |
| `/root/AAA/a2a-server/agent-cards/harnesses/*.json` | 13 harness cards → species instances |
| `/root/AAA/a2a-server/agent-cards/` | **CANONICAL agent-card tree** (schema v2.2.0) — identity/ functions/ extensions/ forge/ harnesses/ organs/ roles/ |
| `/root/AAA/agent-cards/identity/` | LEGACY lane identity (333/555/888) — README declares itself superseded by a2a-server tree |
| `/root/arifOS/arifosmcp/runtime/megaTools/` | Kernel verb surface (13 files) |
| `/root/arifOS/tools_sot.yaml` | Verb SOT (8 → possibly 11) |
| `/root/AAA/src/resolvers/opencode_render.py` | BROKEN drift detector (prerequisite fix) |

## Worked example — full forge cycle 2026-08-08

This session produced concrete artifacts against the doctrine. The full trail is at `/root/forge_work/_drafts/CHAOS_MAP_9ATLAS_UPGRADE.md` (57 paths, 8 hard lines).

### Atlas v1 — operational canonicals

```
000 OBSERVE    = arif_observe (kernel :8088)
111 EXPLORER   = organ-level capability (no kernel verb)
222 ARCHITECT  = organ-level capability (no kernel verb)
333 THINK      = arif_think
444 ORCHESTRATE = arif_route (semantic rename)
555 VERIFIER   = arif_memory (partial — needs split)
666 AUDITOR    = collapsed into 888 (HIGH risk: Gödel lock)
777 EXECUTE    = arif_forge
888 JUDGE      = arif_judge (federation-only; OpenCode self-check is light)
999 WITNESS    = arif_seal (authority layer, NOT normal agent)
```

### Per-runtime init prompts (loaded for `/init` to authenticate actor)

| Runtime | Init prompt | Atlas weights |
|---|---|---|
| Hermes ASI | `AAA/prompts/INIT_HERMES.md` | 000=HIGH, 444=HIGH, 555=PRIMARY, 666=MED, 999=MED |
| OpenClaw   | `AAA/prompts/INIT_OPENCLAW.md` | 333=HIGH, 444=HIGH (primary), 222=MED, 777=MED |
| Human      | `AAA/prompts/INIT_HUMAN.md` | SOVEREIGN (above registry) |

### Slash command map (OpenClaw, 32 commands T0–T3)

- Substrate: `/init`, `/request-seal` (NOT `/seal` — 888-APEX only)
- T0 OBSERVE: 14 commands (`/status`, `/agents`, `/skills`, `/tools`)
- T1 MUTATE: 11 commands (`/new`, `/goal`, `/reload-mcp`)
- T2 ANNOUNCE: 1 (`/yolo`)
- T3 HOLD: 5 (`/restart`, `/update`, `/stop`, `/approve`, `/deny`)

Reference: `AAA/registries/OPENCLAW_SLASH_COMMANDS.md`

### Deploy-guard catch-22 (the forge-blocking reality)

After committing all 3 init prompts and the slash-command map, `git push origin main` was blocked by `test_deployed_commit_matches_source` (local HEAD `c7c12ed4` ≠ deployed `265710480`). `make deploy-local` then blocked with `888_HOLD: local HEAD not origin/main`. Catch-22 by design — push needs deploy in sync, deploy needs push first.

Resolution paths:
1. **Force-push** (T3, needs `ACK_M10_PUSH_BRANCH` from Arif)
2. **Reset local** + re-apply fix after deploy (loses work)
3. **Skip push** + push at next forge cycle (accumulates drift)

Doctrine: per `arifos-federation-ops §4 ("never hand Arif digital work"), pushing force is sovereign-only — not a Hermes auto-act. Standard forge cycle assumes `make prove` locally first to surface deploy-guard errors before push.

### Cross-bot routing rule (Arif-mandated 2026-08-08)

Hermes DM cannot read group history (webhook blocks `getUpdates` on both `@ASI_arifos_bot` and `@AGI_ASI_bot`). To make OpenClaw act from a group context, tag `@AGI_ASI_bot` in the message — OpenClaw wakes on mention. AAA group chat_id is `-1003753855708` (requires `-100` supergroup prefix; bare `1003753855708` returns `400 chat not found`).

## Pitfalls

1. **Prerequisite blocker:** `opencode_render.py:155` is broken (`fb.get(...)` on str). Audit cannot run until fixed. Fix FIRST, before forge output validation.
2. **Promotion trap:** Do NOT add 111/222/666 as kernel verbs unless compression causes measurable constitutional harm. Genome exceeds transcription machinery by design.
3. **Identity trap:** Do NOT create new agent cards for every coding tool. They are OpenCode-Zen instances. One species card, many instance bindings.
4. **888 is not a person:** In OpenCode-Zen, 888 = self-check (lightweight). Full 888 constitutional judge lives ONLY at federation level. Don't put full judge authority in code sessions.
5. **Cross-profile guard:** HERMES has untracked skills dirs including `profiles/aaa-hermes/skills/` — verify profile boundary before forge touches these.
6. **Seal chain stale:** last seal is 5+ days old at baseline. New SEAL-worthy output requires renewing seal chain first.
7. **Baseline diff is mandatory:** never declare "upgrade complete" without diffing against a pre-forge CHAOS TRACE. Memory is unreliable for this — commit the baseline, diff the result.
8. **Two agent-card trees exist — use the right one.** `a2a-server/agent-cards/` is canonical; root `AAA/agent-cards/` is legacy. A sibling agent editing the legacy tree is editing a superseded map (2026-08-09: grok/codex had harness cards but NO full `agents/` folders — identity/key/binding files were never minted for them, which is a gap, not the norm).
9. **Model-map file drift:** quotes of `AGENT_MODEL_MAP.json` are stale — it self-declares `_deprecated: true`. Always read `/root/.config/federation-models.json` for live per-agent routes.
10. **Registry last-write-wins wipe (fixed 2026-08-09):** `register()` in `agent-card-registry.js` keys a Map by agentId — the warga scan (`agents/`) loads AFTER the canonical `a2a-server/agent-cards/` tree and overwrites duplicate agentIds with `civ_layer=null` (its sourcePath doesn't match the `/agent-cards/([^/]+)/` regex). Result: 20+ `unclassified` despite a correct CIV33_LAYERS map. Fix: guard in `register()` — "never downgrade a classified card to unclassified" (carry existing `civ_layer` forward when the new card's is null). Verified final distribution after fix: `identity:4 (incl 777-forge) · harness:14 · binding:20 · unclassified:0`.
11. **Consolidation sweep discipline (2026-08-09):** identity material lives in 6 locations (canonical `a2a-server/agent-cards/`, legacy root `agent-cards/`, warga `agents/`, `agents/_lanes/_archive/` v2.0.0 lane cards, `archive/2026-07-25/` 9.7MB snapshot, build outputs). 15 agentIds duplicate across 3 scan roots — canonical is always the newest superset (e.g. `_lanes/_archive` v2.0.0 has ZERO keys missing from canonical). One real distill surfaced: canonical `harnesses/codex.json` was stale (v2.0.0 + gpt-5.6-sol) vs live ledger (v2.3.0 + deepseek-v4-pro) — always diff canonical vs the `agents/_external/` mirror for version/model drift. Full map: `/root/forge_work/2026-08-09-aaa-consolidation/CONSOLIDATION_MAP.md`. Archive moves are reversible `mv` to `_retired`/`_archive` — never `rm`.

## Related skills

- `arifos-federation-ops` (kernel ops, session lifecycle, seal paths) — this skill extends it for the genome/species dimension
- `canon-integrity-check` (cross-reference live multi-repo state)
- `arifos-kernel-eurekas` (K1-K11 kernel honesty laws)
- `frontier-model-audit-verification` (audit sibling SEAL reports)

*DITEMPA BUKAN DIBERI — Forged 2026-08-08 under F13 SOVEREIGN directive. Genome is universal, not a feature.*
