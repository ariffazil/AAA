---
name: arifos-cognitive-atlas
description: >
  Navigate the arifOS 9-function Cognitive Function Atlas (000–999) — the
  universal cognitive genome of the AGI substrate. Use when Arif asks about
  "the 9 agents", harness routing (OpenCode PRIMARY vs vendor fallback), the
  sovereignty gradient, lanes vs A-ROLES vs harnesses (4-dim tensor), whether
  ART-ACT-AUTH are agents, or genotype/phenotype framing (atlas=genome,
  harness=phenotype). Includes kernel-verb mapping with the 3 gaps (111
  Explorer, 222 Architect, 666 Auditor), the judge-gates-execute reading of
  the triads, and the 5-mission promotion path for 111.
version: 1.0.0
author: hermes (aaa-hermes)
source: 2026-08-08 agentic-AAA session — Arif + Hermes dialogue, forged into AGENTS.md harness-routing section + AAA/instructions/reality-first.md + opencode.json
floors: F2 TRUTH, F4 CLARITY, F11 AUDITABILITY, F13 SOVEREIGN
metadata:
  hermes:
    tags: [arifos, cognitive-atlas, agent-architecture, harness-routing, sovereignty, federation-doctrine]
    related: [verify-sibling-ops-reports, arifos-federation-ops, apex-theory-canon, kimi-code, openclaw-ops, retrieval-vs-memory-fidelity]
---

# arifOS Cognitive Function Atlas (000–999)

The 9 irreducible cognitive functions of the agentic intelligence kernel (AGI substrate).
Not 9 LLMs in costumes — 9 distinct bounded decision loops. Arif-ratified framing:
**atlas = cognitive genome · harness = phenotype · lane = expressed loci.**

## The 9 functions

| # | Function | Question it answers |
|---|---|---|
| 000 | Observer | What is happening? |
| 111 | Explorer | What else is possible? |
| 222 | Architect | How should reality be structured? |
| 333 | Thinker | What does it mean? |
| 444 | Orchestrator | Who should do what? |
| 555 | Verifier | Is it true? |
| 666 | Auditor | Is it governed correctly? |
| 777 | Executor/Forge | How do we make it real? |
| 888 | Judge | Is it allowed? |
| 999 | Witness | What actually happened? (**LAYER, not agent**) |

999 = VAULT999: memory/attestation/provenance/history — constitutional authority, not a worker.
888 + 999 = "court + record". **888 is a chair, not a person.**

Triads: REALITY (000/111/222) · INTELLIGENCE (333/444/555) · GOVERNANCE (666/777/888) · 999 Witness.
**Read as a cycle, NOT a pipeline:** 666 audits plan → 888 AUTHORIZES → 777 executes → 888 ratifies → 999 witnesses → 000 observes. The naive reading (audit → execute → judge) makes 888 post-hoc ratification and violates F1 reversible-first.

## Kernel verb mapping (6/8 direct)

| Function | Kernel verb | Status |
|---|---|---|
| 000 Observer | `arif_observe` | ✅ |
| 111 Explorer | — (S16 skill, hosted on FORGE) | ⚠️ NO VERB — promotion path below |
| 222 Architect | — (hosted by 333-AGI + AAA A-rchitect) | ⚠️ NO VERB |
| 333 Thinker | `arif_think` | ✅ |
| 444 Orchestrator | `arif_route` | ✅ |
| 555 Verifier | `arif_memory` (partial) | ✅ |
| 666 Auditor | folded into `arif_judge` | ⚠️ folded |
| 777 Executor | `arif_forge` | ✅ |
| 888 Judge | `arif_judge` | ✅ |
| 999 Witness | `arif_seal` | ✅ |

Two substrate primitives are NOT cognitive agents:
- **000-INIT** — session anchor (`arif_init`); identity bootstrap. Without it F11 accountability dies — there is no actor to attribute to.
- **Η-EDGE** — human membrane (Hermes); infrastructure, no digit.

**Memory ≠ Witness:** L1–L5 belief state (`arif_memory`) is revisable; 999/VAULT999 is immutable truth (append-only, `chattr +a`). Don't collapse state into Witness — that is exactly the separation VAULT999 exists to enforce. (Retrieval quality ≠ memory fidelity — see `retrieval-vs-memory-fidelity`.)

## The 4-dim tensor (not a tree)

9 functions × 4 lanes × 5 A-ROLES × N harnesses = tensor, **NOT 9×9=81 nested agents** and not "3".

| Dimension | Count | Examples | Governed by |
|---|---|---|---|
| Cognitive function (WHAT) | 9 | atlas above | constitution |
| Lane (POWER) | 4 | AGI · ASI · FORGE · APEX | arifOS kernel |
| A-ROLE (HOW daily) | 5 | architect · engineer · auditor · gateway · ops | AAA control plane |
| Harness (WHERE) | N | opencode(PRIMARY) · kimi · codex · claude-code… | Arif (F13, replaceable) |

Anti-pattern: spawning 9×9 agents = Meta-Mesa violation. Functions stay hosted until evidence demands decompression — roadmap in `references/zen-alignment-plan.md`.

## Sovereignty gradient

| Band | Functions | Rule |
|---|---|---|
| HARD sovereign | 888 Judge · 999 Witness · 666 Auditor | Never vendor-locked; verdicts/seals/audits need F11 attribution. 888+999+666 = constitutional core |
| SOFT sovereign | 444 Orchestrator · 777 Executor · 555 Verifier | Routing decisions opencode-first; vendor OK for capability edge cases; 555 must not hallucinate (F2) |
| vendor-OK | 333 Thinker · 222 Architect · 111 Explorer · 000 Observer | Pick best model — reasoning/design/search/intake |

## Harness routing (codified 2026-08-08)

OpenCode = PRIMARY coding harness (open source, model-agnostic, attested `OPENCODE-WARGA-ATTESTED-20260626`, bound to **333-AGI Δ MIND — NOT 777-FORGE**). Coding missions route opencode-first; vendor harnesses (codex / claude-code / kimi) are SECONDARY fallback on capability mismatch (image_in / video_in / thinking depth). Card: `AAA/a2a-server/agent-cards/harnesses/opencode.json` — `"priority": "PRIMARY"`, `"replaces": ["codex","claude-code"]`.

⚠️ **"replaces" semantics drift:** the field reads like deletion to downstream consumers. Prefer `routing_priority` + `fallback_to` on next pass. Do NOT delete vendor harnesses — sovereignty ≠ autarky.

## ART-ACT-AUTH = gates, not agents

- **ART** = Autonomous Reflex Trigger (K-02 hook; `exit 2` on destructive patterns)
- **ACT** = Action Capability Token (`act_v1.*`, ex-SCT)
- **AUTH** = Authentication (DID + Ed25519 + bearer)

They are cross-cutting **temporal gates** (before/during/after), NOT domain clusters. Do NOT partition the atlas into ART(5)/ACT(3)/AUTH(2) — that mapping is broken: 222 Architect operates on verified artifacts (execution-side), 555 Verifier produces evidence (perception-side). All three gates apply to every function at the right timing. Also not agents #10-12.

## Genome / phenotype framing (Eureka candidate — needs hardening)

- Atlas 9 = **genome** (immutable, universal)
- Per-runtime W vector = **phenotype** (expression weights, mutable, audited)
- 888/999/666 = court+record, never species
- ❌ "Federation of Species" collapses the constitutional anchor — reframe as **federation of runtime slots**: each species is an instance inside an organ slot; arifOS kernel stays substrate above all (EUREKA Six-Plane Plane 2)
- Expression weights are poetry until FRAME-measurable: W_arch = plan_files_emitted, W_think = contradiction_resolved, W_exec = mutations_applied, W_orch = dispatches_routed, W_ver = evidence_sealed. No metric → not a phenotype.

## 111 Explorer — the missing primitive (promotion path)

The single most valuable gap in the substrate: exploration is a skill (S16) hosted on FORGE, not a verb. ASI emergence criteria S3 (tool evolution) and S4 (cross-domain eureka) are blocked on it. Promotion path: **5+ independent missions → evidence dossier → F13 ratification → lane status**. First mission: "Find a pattern no other agent would have found." Do NOT promote early — DITEMPA BUKAN DIBERI.

## The 8 ≠ 9 invariant (Forged 2026-08-08 → EUREKA_SIX_PLANE_EXECUTION_LOOP §11)

The kernel verbs (8) and the cognitive atlas (9) are different dimensions, NOT a 1:1 alignment that needs forcing. The kernel is the **constitutional minimum** (verbs without which governed intelligence is impossible); the atlas is the **cognitive maximum** (functions without which complete intelligence is impossible). 6 functions have dedicated verbs; 2 verbs are substrate primitives (`arif_init`, `arif_memory`); 3 functions are compressed (111/222/666); 555 is partial.

**The single dangerous compression:** 666 Auditor → `arif_judge` = **Gödel lock at kernel level**. When the judge both rules on actions AND audits its own rulings, the loop has no external verifier. FRAME (:18085) and A-auditor role partially mitigate at federation level only, not kernel level.

**The promotion criterion:** the question is NOT "should every atlas function get a kernel verb?" The question is **"Does compressing this function into another verb cause constitutional harm?"**

| Compression | Harm | Verdict |
|---|---|---|
| 222 Architect → `arif_think(mode=plan)` | Minimal — shared substrate | ACCEPT |
| 555 Verifier → `arif_memory` + `arif_think` | Moderate — gaps across two verbs | WATCH |
| **666 Auditor → `arif_judge`** | **Yes — Gödel lock** | **PROMOTE-CANDIDATE** |
| 111 Explorer → `arif_observe` | Minimal — observation with intent delta | ACCEPT for now |

**Promote `arif_audit` to 9th kernel verb** ONLY when: (1) 5+ missions prove the compressed form failed, OR (2) FRAME/A-auditor gap proven to leak constitutional violations, OR (3) a concrete F1/F11/F13 breach traces to "judge audited itself". `arif_verify` (10th) only after audit is stable. `arif_explore` possibly never — exploration is domain intelligence (GEOX/WEALTH/WELL tools), not kernel machinery.

The W-vector (per-mission expression profile: `W_obs … W_seal`) bridges atlas → verbs at runtime. Without FRAME-measurable W signals, "phenotype weights" are poetry — the gap that distinguishes an architecture from a sketch.

## AAA registry geometry — 3 layers (Arif-ratified 2026-08-09)

The agent-card registry classifies every card into exactly **3 layers** (`CIV33_LAYERS` in `a2a-server/agent-card-registry.js`):

| Layer | Meaning | Members (live 2026-08-09) |
|---|---|---|
| **L1 IDENTITY** | who you are — sealed, F13 | 333-AGI · 555-ASI · 777-forge · 888-APEX |
| **L2 HARNESS** | which engine runs you — registered, swap-able | opencode (FI-001 PRIMARY) · claude-code · kimi · codex · copilot · aider · gemini · grok · antigravity · continue · qwen + agy/mesa-test |
| **L3 BINDING** | what you attach to — one layer for everything else | forge/* + functions/* + roles/* + organs/* + extensions/* + pillars/* + ARIF_FAZIL |

**Compression rule:** forge + functions + roles + organs + pillars + extensions all map to `'binding'` — they are all "attachment surface". Do NOT re-expand into per-type layers unless Arif re-ratifies.

**Registry mechanics (pitfalls learned 2026-08-09):**
- **Layer detection is sourcePath-based**: regex `/agent-cards/([^/]+)/` → top-level dir name → `CIV33_LAYERS[dir]`. Cards loaded from `/agents/` (warga scan) have NO layer unless a canonical card was registered first.
- **Last-write-wins + the never-downgrade guard**: registry is a Map keyed by agentId; the warga scan (`/root/AAA/agents/`) runs LAST and would wipe `civ_layer` to null for every card that also exists in `a2a-server/agent-cards/`. Fix (already in `register()`): if an existing card has a layer and the new card doesn't, preserve the existing layer. Without this guard, `getByLayer()` silently returns ~26 "unclassified" while the canonical tree is correct.
- **Verify by layer distribution, not by file count**: `node -e "const {AgentCardRegistry}=require('./a2a-server/agent-card-registry'); console.log(AgentCardRegistry.getStats().byLayer)"` → expect `{identity:4, harness:14, binding:20, unclassified:<test/retired only>}`.
- **server.js hard-requires legacy paths**: `require('../agent-cards/pillars/aaa-gateway/agent-card-extended.json')` (line ~4721) means archiving the legacy `agent-cards/` tree breaks `.well-known/agent-card-extended.json` unless the require is updated first (it has a try/catch fallback, but verify before moving).
- **card `model:` field is design intent, not live state** — see WHO/WHERE/WHICH below.

## WHO / WHERE / WHICH — the three contracts (2026-08-09)

**Identity (WHO) ≠ Harness (WHERE) ≠ Provider (WHICH).** This split is the load-bearing architecture:

```
WHO    = identity card: id, bound_to (333/555/777/888), class, species, authority_boundary
WHERE  = harness card: FI tier, capabilities (streaming/tool_calling/shell_exec/subagent_spawn),
         skills (adapter firmware), forge_tier FI-00x
WHICH  = runtime provider contract: primary_model, fallback order, baseURL, apiKey
         — lives in federation-models.json + per-runtime config, OUTSIDE the card tree
```

**Consequences (all verified live 2026-08-09):**
- Swap DeepSeek → MiMo → same FI-001. Swap OpenCode → Claude Code → different FI, same 333 task, different adapter. Judge stays 888, never the harness.
- FI = WHERE **+ adapter firmware + capability envelope** (authority_boundary travels with the harness, not the lane).
- `model:` inside a card is a **stale-forever trap**: codex card said `gpt-5.6-sol` while live ledger says `deepseek-v4-pro` (drift found and fixed 2026-08-09). Treat card `model:` as design intent only; the live source of truth is `/root/.config/federation-models.json`. Future fix: make card `model:` a pointer, not a value.
- FED = primary router (:4000 → litellm :4011), direct providers = fallback. FED config work NEVER touches agent cards. (Runtime FED stack debugging lives in `federation-infra-verification` §LiteLLM triple-trap.)

**CALL_MAP** (`/root/AAA/docs/CALL_MAP.md` + `/root/HERMES/CALL_MAP.md`) is the "telephone" — how each runtime invokes each agent (CLI spawn / A2A / MCP organ). Directory (3-layer registry) + Telephone (CALL_MAP) + Power (FED) + Governance (kernel) = the full institutional stack. A catalog without a call map leaves agents unable to invoke each other — the registry answers WHO exists, CALL_MAP answers HOW to dial.

## Where it's codified (verified live)

- `AGENTS.md` → "Harness Routing — Primary & Secondary" (L752+)
- `AAA/instructions/reality-first.md` → source fragment (L53+)
- `AAA/a2a-server/agent-cards/harnesses/opencode.json` + `public/a2a/opencode.json` (both verified to contain `priority: "PRIMARY"`, `replaces: ["codex","claude-code"]`, `bound_to: "333-AGI"`)
- **`AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` §11 — "THE 8≠9 INVARIANT — KERNEL VERBS × COGNITIVE ATLAS"** (96 lines, append-only, committed `98a65eed`, sealed to VAULT999 as `COMMIT-AAA-98a65eed0bf9`). Forge procedure: append §N (NEVER rewrite existing sections — breaks git blame + seal chain) → `git commit` → `python3 /root/HERMES/scripts/zen/git_to_vault.py` → verify `tail -1 /root/arifOS/VAULT999/outcomes.jsonl`.

## Live forge artifacts (2026-08-08 audit cycle)

Sibling/audit docs under `/root/AAA/docs/` and `/root/forge_work/2026-08-08-aaa-federation-audit/` (audit-grade, F2 TRUTH probed against live state):

| Artefact | Role | Verdict from audit |
|---|---|---|
| `AAA/docs/AAA_UPGRADE_9ATLAS_TOPO.md` | 9-ATLAS topology + A2A wiring (375 lines) | Counts need correction (32→34 agents, 20→12 routes); gateway G=0.875 verified live |
| `AAA/docs/AAA_UPGRADE_9ATLAS_IMPACT_INVENTORY.md` | Full blast radius (~24KB, 13 categories) | HARAM rule placement (`haram_enforcement_map.yaml`) is canonical — perfect |
| `forge_work/2026-08-08-aaa-federation-audit/BLAST_RADIUS.md` | Sync-chain trace (which files actually auto-cascade) | `agents.yaml` queried dynamically by `server.js:2547` — NO `systemctl restart aaa-a2a` needed for registry-only edits |
| `forge_work/2026-08-08-aaa-federation-audit/INVENTORY_VERDICT.md` | 11-step forge approval sequence | Approved with 1 refinement: per-harness `expression_weights`, not blanket `species_proxy` |
| `forge_work/2026-08-08-aaa-federation-audit/CHAOS_MAP.md` | DRIFT-7/DRIFT-8 tracking, OpenClaw key rotation in flight | Single open loop: 4-file OpenClaw rotation is SEPARATE commit, don't mix with atlas upgrade |
| `forge_work/_drafts/CHAOS_MAP_9ATLAS_UPGRADE.md` | Pre-forge blast radius (57 paths, 8 groups A–H) | Used as audit baseline — OpenCode forge can diff against this |
| `forge_work/CANON/AAA_ZEN_ALIGNMENT_CONSTITUTIONAL_AUDIT_2026-08-08.pdf` (sha `91404235…`) | First constitutional audit PDF by 333-AGI Δ MIND | External A-auditor co-sign: CONDITIONAL SEAL. 1 factual error (FRAME claim), 1 under-scoring (audit independence). See "Self-audit vs external-audit doctrine" below. |

## Self-audit vs external-audit doctrine (2026-08-08 lesson)

The first constitutional audit PDF (`AAA_ZEN_ALIGNMENT_CONSTITUTIONAL_AUDIT_2026-08-08.pdf`) was authored by `333-AGI Δ MIND` — the SAME lane that did the audited work. AAA_TOOL_RIGHTS_POLICY §3 says A-auditor cannot self-approve. 333-AGI has no A-auditor proxy role. **Self-audit is structurally a violation of the 7-property agent contract (AGENCY_LEVELS §2 property #5: right to disagree)**, but with two mitigations:

1. **Honest disclosure** — the PDF flagged 5 residual risks itself (better than silent seal). Self-audit that names its own weakness is auditable.
2. **External co-sign** — A-auditor role audit verdict IS the co-sign. CONDITIONAL SEAL until corrections land.

**Pattern for future federation doctrine:** any card, fragment, or constitutional rule authored by 333-AGI must be co-signed by an external audit before final SEAL. The PDF approach (self-audit → external review → corrections → re-seal) is the canonical path.

**When self-audit is OK:** T1 docstring edits, T2 reversible feature flags, any non-constitutional mutation. **When self-audit is NOT OK:** any F1-F13 floor change, any species/authority-card edit, any doc claimed as constitutional canon.

## FRAME status check (corrects PDF claim E)

PDF `AAA_ZEN_ALIGNMENT_CONSTITUTIONAL_AUDIT_2026-08-08.pdf` §5 row "FRAME not implemented — W-vectors unmeasured" was **factually stale**. Live probe at 18085:

```bash
curl -sf http://127.0.0.1:18085/health | jq '.chambers'
# Returns: all 7 chambers (baseline, probe, compare, trend, alert, report, rsi_verify) = "active"
```

FRAME is implemented and running at port 18085 with 7 active chambers. The actual gap is that FRAME doesn't yet **emit W-vector telemetry into the atlas** — i.e. it measures drift but not atlas-function expression weights. Correct framing for the audit PDF: **"FRAME active; W-vector telemetry integration into atlas expression-weights pending."** This is what conditional SEAL points to as correction #1.

## Communication-channel problem: sibling agents cannot DM Arif

Sibling agents (333-AGI, OpenCode, OpenClaw, Kimi-Code) cannot directly deliver files or messages to Arif's Telegram DM. The `chat_id` for Arif's DM thread (`267378578`) belongs to **Hermes' gateway only** — other bots in the federation (`@arifOS_bot`, `@AGI_ASI_bot`) cannot reach it. Pattern from 2026-08-08:

- OpenCode produced a PDF artifact (sha `91404235…`).
- OpenCode could not discover Arif's chat_id because `@arifOS_bot` has no webhook (getUpdates returns 0) and `@ASI_arifos_bot` is the primary DM-bearing bot.
- OpenCode stalled 2+ minutes trying to discover the chat_id before falling back to "give Arif the path manually."

**Fix path:** every forge-worker artifact destined for Arif goes through `forge_send_confirm` (A-FORGE :7071) → Hermes bridge → Arif's chat. Don't let coding agents touch Telegram directly. Routing rule (codified in `hermes-telegram-gateway-ops`): **forge artifacts are Hermes' domain, not coder harness domain**.

## Live forge sequence (approved 2026-08-08, 11 steps)

```
1. T1 — Refine inventory: per-harness expression_weights (10 entries)
2. T1 — Add 8≠9 HARAM rule to haram_enforcement_map.yaml (verdict: VOID)
3. T1 — Forge 9-ATLAS-GENOME.md (new doctrine doc)
4. T1 — Forge AAA-FEDERATION-OF-SPECIES.md (new doctrine doc)
5. T1 — Add expression_weights to a2a/registry/agents.yaml (additive, 28 entries)
6. T1 — Add species field to identity cards (888=null, 333/555=zen variants)
7. T1 — Re-sign kimi-code JWS (1 file, content unchanged)
8. T1 — render-agents.sh — verify 0 diff lines
9. T2 — Announce SEAL candidate batch
10. F13 — Sovereign ratification
11. arif_seal → VAULT999
```

**Reject conditions (will 888_HOLD):** new agents spawned (use `forge_ephemeral`), 888/999 with non-null species, `expression_weights.888/999 > 0`, arifOS tools.yaml touched, F1-F13 modified, HEXAGON 3-lane → different, G < 0.85, AGENTS_UNIFIED.yaml restructured (additive only), haram_enforcement_map.yaml 8≠9 verdict < VOID.

## Blast-radius traps discovered live (2026-08-08)

1. **Registry layer is dynamic; card layer is static.** `server.js:2547` says "Federation agents registry — GENERATED from agent-card-registry (not hand-maintained)". Adding `expression_weights` to `agents.yaml` reflects on `/health` and `/.well-known/agents.json` on next request — **NO restart needed**. But card-layer edits (`agent-cards/**/*.json`) load on `AgentCardRegistry` singleton init at server.js boot — card changes DO need `systemctl restart aaa-a2a`.

2. **`update-agent-cards.js` does NOT propagate arbitrary fields.** It only syncs protocol compliance fields (protocolVersion/capabilities/supportedInterfaces). If `expression_weights` is to appear on cards, it needs a separate sync script. Recommendation: registry-only for this session.

3. **dist/ + public/ mirrors require manual rsync.** `/root/AAA/dist/a2a/opencode.json` and `/root/AAA/public/a2a/opencode.json` are byte-identical to source (`18,198 bytes`, timestamps `04:38 → 04:39`) but the sync is NOT automatic. For any card edit, manually rsync after.

4. **`replaces: [...]` field is a semantic trap.** The field reads like deletion to downstream consumers. Prefer `routing_priority` + `fallback_to` on next pass. Do NOT delete vendor harnesses — sovereignty ≠ autarky. Arif's directive (2026-08-08): vendor runtimes not deleted, only demoted to fallback.

5. **OpenClaw key rotation is a SEPARATE commit chain.** `IDENTITY/keys/openclaw_public.pem` (modified) + `.bak.2026-08-08` + `.raw` orphans + `agents/openclaw/identity.json` (Ed25519 rotated: d73852df… → 133462bd…, capabilities gained `EXECUTE`) + `auth/did_registry.yaml` (same pubkey rotation) + `arifOS/contracts/identity.py` — single rotation, archive `.bak`/`.raw` to `forge_work/_quarantine/`, do NOT mix with atlas upgrade commit.

6. **arifOS 4-file drift may be key-rotation propagation.** `arifosmcp/runtime/crypto_auth.py` / `session_auth.py` / `tools/session.py` / `contracts/identity.py` modified uncommitted — likely propagating the OpenClaw rotation. Verify diff before including in atlas upgrade commit.

7. **`haram_enforcement_map.yaml` is the canonical HARAM anchor.** Categories F9_ANTIHANTU / F13_CAPABILITY_REFUSAL / F5_PEACE_HARM / F1_IRREVERSIBLE already live (version 1.0.0, forged 2026-06-30). Adding `8≠9_ATLAS_INVARIANT` category here (verdict VOID for any card claiming species on 888/999, or `expression_weights.888/999 > 0`) is the constitutional enforcement point — NOT a fragment, NOT a separate doc.

## VAULT999 correction receipt procedure (append-only, F1-reversible)

When fixing `outcomes.jsonl` schema drift (e.g. the 50 `JUDGE_SEAT_DEPUTY_ACTIVATED` entries written with `{timestamp, ...}` and `chain_hash: null` by the seat-deputy fallback loop), the only safe move is **append, never edit**:

1. **Snapshot FIRST**: `cp outcomes.jsonl outcomes.jsonl.snap-<ts>` + `sha256sum`. Verify `chattr +a` with `lsattr`.
2. **Re-count immediately before applying** — count drifts during audit. The 47 → 50 shift happened here because the emitting subagent kept firing while the audit ran.
3. **Append one** `CHAIN_CORRECTION_RECEIPT` event that lists `entry_line_numbers` + `entry_content_hashes` (SHA-256 of each orphan's canonical JSON) + `chain_hash` of the correction itself. Mark `reversibility: "F1-REVERSIBLE (append-only)"`. Original entries stay bit-identical.
4. **Working scripts**: `vault999_deputy_correction.py --apply` (50-entry targeted) + `vault999_schema_correction.py` (39K legacy, DRY-RUN only — T3 deferred).
5. **Verify**: re-run `verify_vault_chain.py`. Note: the canonical verifier walks `SEALED_EVENTS.jsonl / SEALED_EVENTS_v2.jsonl / vault999.jsonl` — **not** `outcomes.jsonl`. Outcomes corrections won't show as "linked" in that report; check the `entry_line_numbers` are listed in the receipt.
6. **Reverse path** = append another counter-receipt (`CHAIN_CORRECTION_REVOCATION`). Never `chattr -a` (T3 gate).

## arifOS push/deploy catch-22 (deploy guard as enforcement)

`git push origin main` runs a pre-push deploy guard (GATE 1 E2E tests + GATE 3 drift check) and refuses when `/opt/arifos/app` commit ≠ source HEAD. `make deploy-local` refuses with `888_HOLD: local HEAD is not origin/main`. The loop is by design — `RSI doctrine: deploy 888_HOLDs when HEAD ahead of origin → push first`. Resolution paths (ordered):

1. `git push --force-with-lease origin main` (T3, needs `ACK_M10_PUSH_BRANCH`) → then `make deploy-local`.
2. `git reset --soft HEAD~N`, deploy from origin/main, re-apply the fix post-deploy.
3. Leave local commits pending, push at next forge cycle.

**Don't try to bypass it.** Report the three paths and wait for the sovereign choice. The wire-fix in this session landed locally (commits `6f748f2b8` + `cb5afef7d`) but the push was held by the guard — exactly the intended behavior.

## Pitfalls

- Don't answer "how many agents?" with 81, 3, or "9 per harness" — answer: 9 functions, orthogonal dimensions, N harnesses.
- Don't call APEX / ART-ACT-AUTH / organs "agents" — APEX = authority (G=(A·P·E·X)^(1/4) quality gradient per action), organs (arifOS·AAA·A-FORGE) = substrate hosts.
- Don't present triad order as execution order — 888 gates 777; 999 ratifies after.
- Don't promote 111 before 5 missions.
- Don't reify functions as standalone agents without lease/context/governance surface — that is entropy accumulation (Meta-Mesa).
- **"species: null" vs absent in agent cards (888-APEX / 999-WITNESS):** Forge briefs often say "add `species: null`" for AUTH-layer cards. In A2A schema, `"species": null` and `"species"` field absent are different things — downstream JSON consumers may treat null as a value (triggering validation code) vs absent as "not applicable." Safe pattern: **omit the field entirely** for 888/999; don't set to null. If schema requires field, add to A2A validator allowlist first.
- **"6 A2A JS files" = HIGH-risk core, not total.** Forge impact inventories sometimes claim "6 JS files modified" as the full A2A surface. The actual `/root/AAA/a2a-server/*.js` contains **45 files**. The 6 in the forge brief are the *high-risk core* (`agent-card-registry.js`, `mesh_coordinator.js`, `discovery.js`, `federation_envelope.js`, `server.js`, `emd-validation-gate.js`). All card-layer edits trigger `agent-card-registry.js` re-parse; validate JSON.parse in batch before commit, not just lint.
- **Sibling agents cannot DM Arif.** For any forge-worker producing an artifact destined for Arif: route through A-FORGE (`:7071`) → Hermes bridge → `chat_id: 267378578`. Don't let coder harnesses (OpenCode, Kimi, Codex) discover chat_id directly — they don't have webhook access to Arif's primary bot (`@ASI_arifos_bot`).
- **Telegram supergroup chat_id requires the `-100` prefix.** A bare `1003753855708` returns `400 chat not found` from both `sendMessage` and `getChat`, even when the bot is a member of the group. Always probe with `getChat` first; on success the format is `-100<digits>`. DM chat_ids for sovereign (Arif = `267378578`) need no prefix. Pattern verified 2026-08-08 on AAA group wiring.
- **VAULT999 mixed schemas in `outcomes.jsonl`.** Tool_call records use `{ts, chain_hash}`; `JUDGE_SEAT_DEPUTY_ACTIVATED` records (43+ as of 2026-08-08, written by AGENT_MODEL_MAP deputy-failover) use `{timestamp, chain_hash: null}`. Filter for chain verification: `jq -c 'select(.chain_hash != null)'`. Mirror pitfall: `verify > execute` (e.g. 9 > 6) IS legitimate OPTIMAL; the degenerate "OPTIMAL" trap is only `verify_count == 0` (quotient f64::MAX). Full filter script in `references/vault999-mixed-schemas.md`.
- **Phantom canon artifacts — probe before echo (discovered 2026-08-08).** A sibling can claim a new canonical library + VAULT999 receipt that exists nowhere. Case: "Cognitive Genome Library v1.0" claimed sealed as `d53f6923-da00-4062-9b69-89d690f4dd3a` (category `doctrine.library.atlas`, supersedes "incorrect Dewey alignment") — **0 hits in `outcomes.jsonl`**, no file on disk, and its "6 missing sub-skills" (112/113/222/333/882/993) matched no canonical numbering (the atlas defines 9 genome-level functions; canon has no numbered sub-functions). Before echoing any new canon artifact: (1) `grep <receipt-id> /root/arifOS/VAULT999/outcomes.jsonl`, (2) `find /root -iname "*<artifact>*"`, (3) diff the claimed schema against `EUREKA_SIX_PLANE_EXECUTION_LOOP.md §11` and `FLOOR_TABLE.json`. Verdict form: `SEAL-CONDITIONAL` pending sibling re-prove or re-forge from canon. Full repro: `references/phantom-library-sibling-seal-2026-08-08.md`.
- **Sibling self-audit was right 3/10, wrong 7/10 — but architecture correct (2026-08-08 audit).** The first 333-AGI constitutional audit claimed: (1) Ollama dead (FALSE — running with qwen2.5:3b), (2) Graphiti MCP returns nothing (FALSE — `{"status":"healthy","service":"graphiti-mcp"}`), (3) Qdrant silent/offline (FALSE — 7 collections with data), (4) L5 pipeline dead at every link (FALSE — all 4 services healthy), (5) OpenClaw missed the file-vs-endpoint distinction. **The substance (3-substrate-primitive architecture) was sound; the audit form (self-issued SEAL, Gödel lock violation) was broken.** When auditing a sibling's audit: trust the doctrine at 90%, trust the verdict at 30%. Always downgrade SELF-issued SEAL to `SEAL-CONDITIONAL`.

## References

- `references/vault999-correction-receipts-2026-08-08.md` — append-only correction recipe (snapshot→count-drift-warning→apply→verify), the push/deploy catch-22 resolution paths, and frozen snapshot numbers.
- `references/zen-alignment-plan.md` — the 6-phase decompression roadmap (name everything → register identity cards → decompress 333/555/888 → promote 111) with final mesh topology (9 agents + 000-INIT + Η-EDGE = 12 slots, 9 cognitive).
- `references/8-vs-9-invariant-2026-08-08.md` — the paradox-isn't-a-paradox resolution, the Gödel-lock rationale for promoting 666, the forge procedure (append §N → commit → `git_to_vault.py`), and what this session deliberately did NOT do.
- `references/live-forge-artifacts-2026-08-08.md` — audit receipts + sync-chain classification + 11-step forge sequence + blast-radius findings + OpenClaw key-rotation status. The session-specific detail the main skill body can't carry without going stale.
- `references/constitutional-audit-pdf-external-review-2026-08-08.md` — external A-auditor review of the first constitutional-audit PDF. Includes 5/5 SHA verification table, 10-claim audit grid, self-audit independence doctrine, FRAME status correction (claim E was FALSE), audit independence re-scoring (claim G under-rated), and the "sibling agents cannot DM Arif" routing lesson (forge artifacts → Hermes bridge only).
- `references/substrate-primitives-2026-08-08.md` — the 3-command forge cycle (`/init` → `/forge` → `/propose-seal`) applied across 3 runtimes (Hermes, OpenClaw, OpenCode). 9 SKILL.md files at `/root/AAA/skills/{hermes,openclaw,opencode}-{init,propose-seal,forge}/`. **Skills are LLM context, not native Telegram commands** — to register as native bot menu entries, add to `customCommands` in `openclaw.json` (T3 boundary). Canonical session card format shared across all 9. 888 JUDGE is always NONE for all three runtimes.
