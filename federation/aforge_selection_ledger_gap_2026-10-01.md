# A-FORGE Selection-Ledger Gap + Adapter-Generation Audit — DRAFT 2026-10-01
# Lane: 555b
# Status: read-only receipt, no production change

> Probed 2026-10-01 by 555-ASI Φ SENSE (Lane 555b, sensory / read-only).
> Covers Probe 2 (selection ledger) + Probe 3 (adapter generation) + the
> verify-on-disk status of every A-FORGE/arifOS component Arif named.

## PART A — Probe 2: the selection ledger (12 events, 0 outcomes)

### A.1 Ledger location [OBS]

Canonical live ledger: `/root/.local/share/arifos/skill-selection/selections.jsonl`
- sha256(bytes) = d0a833593bc9c06681b3d0ecd6cd036192c4420fb851c7e1cc10ba50b1aa34dc
- 12 lines, 4667 bytes, last written 2026-09-17T17:19Z
- Companion lock file present (selections.jsonl.lock, 0 bytes)
- This is the ONLY file on the box matching selections.jsonl (find /root -name selections.jsonl).

The SPEC for a richer ledger lives at `/root/AAA/governance/SELECTIONS_LEDGER_SPEC.md`
(status PROPOSAL_AWAITING_F13). The live ledger implements a REDUCED schema, not the
spec's schema. See A.4 gap.

### A.2 Verbatim schema (keys actually present in the live records) [OBS]

11 keys, identical across all 12 rows:
```
ts, skill_name, selection_method, intent, session_id, agent_id,
outcome_success, outcome_summary, alternative_skills, write_class, trigger
```

Sample row (row 1, verbatim, truncated intent):
```json
{"ts":"2026-09-09T00:45:51+00:00","skill_name":"external-artifact-verdict",
 "selection_method":"keyword","intent":"External Copilot handoff ...",
 "session_id":"session_7d9e7edb-...","agent_id":"kimi-code/FI-008",
 "outcome_success":null,"outcome_summary":null,"alternative_skills":null,
 "write_class":"learn","trigger":"harness_skill_tool"}
```

### A.3 Field population rate (n=12) [OBS]

| Field | Populated | Note |
|---|---|---|
| ts | 12/12 | full |
| skill_name | 12/12 | full |
| selection_method | 12/12 | ALL = "keyword" (no scalar/scar-weighted/semantic selection observed) |
| intent | 7/12 | 5 rows have empty-string intent |
| session_id | 12/12 | full |
| agent_id | 12/12 | ALL = "kimi-code/FI-008" (single agent; no other warga emitted) |
| outcome_success | **0/12** | ALL null |
| outcome_summary | **0/12** | ALL null |
| alternative_skills | **0/12** | ALL null |
| write_class | 12/12 | ALL = "learn" |
| trigger | 12/12 | ALL = "harness_skill_tool" |

### A.4 The 12 events, categorized

- By agent: 12/12 kimi-code/FI-008. Zero from claude/opencode/codex/grok/gemini. [OBS]
- By selection_method: 12/12 keyword. [OBS]
- By outcome status: 12/12 UNKNOWN (outcome_success null on every row). [OBS]
- By capability class (INSPECT/PLAN/ACT/VERIFY/EXTEND/CONTROL/LEARN): **field absent.**
  The live schema carries NO capability-class / axis_of_selection / verb field. Cannot
  categorize by class from the ledger. The only class-like field is write_class="learn"
  (uniform). [OBS]
- The 12 skill_names selected: external-artifact-verdict, FORGE-agentic-web-builder,
  "Reality Loop - Autonomous 000 to 999 Recursive Improvement", mata, token-plan-image,
  "RSI - Federation Mesh (Cross-Agent Recursive Improvement)", AGI-dream-engine,
  a2a-task-delegator, check-kimi-code-docs (x2), mcp-testing, openclaw. [OBS]

### A.5 Confirmed counts for the hand-back

- events = 12 [OBS]
- outcomes populated = 0 [OBS]
- independent-verification fields present = 0. The live schema has NO independent-
  verification field at all (not "present but empty" — absent from schema). [OBS]

### A.6 Gap vs Arif's design (missing fields) [OBS]

Arif's design (per SELECTIONS_LEDGER_SPEC.md + citizen-contract §Completion) requires:
selected_capability, alternatives_considered, reason, execution_outcome,
independent_verification_result. Mapping to live schema:

| Design field | Live field | Status |
|---|---|---|
| selected_capability | skill_name | PRESENT (but no capability CLASS/verb) |
| alternatives_considered | alternative_skills | PRESENT-but-EMPTY (0/12 populated) |
| reason | intent | PARTIAL (7/12; free text, not structured reason codes) |
| execution_outcome | outcome_success / outcome_summary | PRESENT-but-EMPTY (0/12) |
| independent_verification_result | — | **ABSENT from schema entirely** |

The spec's richer fields (decision_context, axis_of_selection, candidates[] with
score+method, constraints_hit, expected_outcome, attention_cost_min, closure{}) are
NOT implemented in the live ledger. The live ledger is a minimal keyword-selection log,
not the spec'd decision-point ledger. Distance to a verified learning loop:
outcome backfill = 0/12, independent verification = schema-absent, so the loop
`select → execute → verify → credit` cannot close on any of the 12 events today. [DER]

## PART B — Probe 3: adapter generation (is it fragment-based?)

### B.1 The renderer [OBS]

`/root/scripts/render-agents.sh` — "arifOS Federation — Fragment Composer (monorepo
render.sh pattern)". Reads canonical fragments from `/root/AAA/instructions/*.md`,
composes rendered adapter files. `--check` = dry-run. Forged 2026-08-04 by 333-AGI.
Line ~192 comment: "Core targets — fragment → output (agent-specific adapters stripped
2026-08-04)". So per-agent adapters were REMOVED from render targets on 2026-08-04.

Actual render targets in the script: `/root/AGENTS.md`, `/root/.codex/AGENTS.md`,
`/root/CLAUDE.md` (pointer). Fragment source dir = /root/AAA/instructions/.

### B.2 Per-adapter table (the 6 warga Arif named + canonical) [OBS]

| Adapter file | GENERATED hdr? | Fragment-driven? | Declared source | Drift note |
|---|---|---|---|---|
| /root/AGENTS.md (canonical) | YES | **YES** — 27 fragments listed inline | /root/AAA/instructions/ | mtime 2026-10-01 15:42 |
| /root/CLAUDE.md | (pointer) | **YES** — rendered pointer stub | → /root/AGENTS.md | mtime 2026-10-01 15:42 |
| /root/.codex/AGENTS.md (Codex) | YES | **YES** — Fragment: codex-boot-platform-specific | /root/AAA/instructions/codex-boot-platform-specific.md | mtime 2026-10-01 15:42; F13_RATIFIED_ASIDE 2026-09-29 |
| /root/.arifos/agents/claude/AGENTS.md (Claude) | no | NO — hand pointer | Canonical: /root/AGENTS.md | points to fragment-rendered canonical; not itself rendered |
| /root/.arifos/agents/gemini/AGENTS.md (Gemini) | no | NO — hand pointer | Canonical: /root/AGENTS.md | same |
| /root/.arifos/agents/kimi/AGENTS.md (Kimi) | no | NO — hand-maintained full doc | CCC doctrine refs | 8245 bytes, mtime 2026-09-26 |
| /root/.arifos/agents/opencode/AGENTS.md (OpenCode) | no | NO — hand-maintained full doc | CCC doctrine refs | 6315 bytes, mtime 2026-09-26 |
| /root/.grok/AGENTS.md (Grok) | no | NO — hand doc w/ resolver ref | authority:/root/AGENTS.md; resolver:agent-compartment.md | frontmatter compartment A2M/A2A |
| /root/AAA/agents/grok-build/AGENTS.md | no | NO — hand-maintained | — | 2914 bytes, mtime 2026-09-24 |

**Verdict on Arif's claim "adapter generation is fragment-based":** PARTIALLY TRUE. [DER]
- The CANONICAL layer (/root/AGENTS.md) IS fragment-driven (27 fragments via renderer).
- Of the 6 NAMED warga adapters, only **1 (Codex)** is directly fragment-rendered.
  Claude + Gemini are hand-maintained POINTERS that inherit the canonical fragments
  transitively (they say "Load /root/AGENTS.md for full doctrine"). Kimi, OpenCode,
  Grok are hand-maintained full docs that reference canonical/governance but are NOT
  rendered from fragments.
- So: fragment-driven at canonical layer = YES; per-warga adapter layer = 1/6 rendered,
  2/6 transitive pointers, 3/6 hand-maintained. "Adapter generation is fragment-based"
  holds for the shared trunk, not uniformly for the per-agent files.

### B.3 ROOT_AGENT_CONFIG.yaml + A-FORGE leases [OBS]

`/root/AAA/ROOT_AGENT_CONFIG.yaml` EXISTS. sha256 = 99c44616e176bcac9ff45288b7bd4a9b1d005a5f4601eb0a4af61ef4697ee9a1
(changed mid-session from e9d98851… — concurrent writer, see receipt 1 DRIFT-3).
It DOES reference A-FORGE/arifOS leases for external agents:
- routing_rule: "external agent -> A-FORGE/arifOS lease -> AAA warga/proxy -> AAA state"
- forge_citizenship_contract block (lines ~20-42) declares: contract path, verb_schema,
  generator, projection_output, competency_schema, competency_evals, competency_test_dir,
  competency_state_dir, m_min_metric. status = DRAFT_AWAITING_F13.
- aforge-executor id at line ~133, port 7071; aforge MCP endpoint http://127.0.0.1:7072/mcp
  (line ~165); kimi launcher stdio:/root/.arifos/agents/kimi/mcp-launchers/aforge.sh.

## PART C — Verify-on-disk: every component Arif named

Scar class = claimed-before-checking. Each is marked verified-on-disk or not-found.

| Component Arif named | Status | Evidence path |
|---|---|---|
| a_think/affordances.yaml | **verified-on-disk** | /root/A-FORGE/a_think/affordances.yaml (sha cbe99c45…, 132 cards) |
| forge_experience_trace | **verified-on-disk (LIVE tool)** | registered /root/A-FORGE/src/interfaces/mcp/serve.ts:317; impl experienceTraceTools.ts:446-448; success_basis="self_reported" + success_verified=false at experienceTraceTools.ts:238-239 |
| forge_skill_select_query | **verified-on-disk (LIVE tool)** | registered serve.ts:319 ("read-only SkillGate Phase 1"); impl experienceTraceTools.ts:597-599 |
| EphemeralGenesisRunner | **verified-on-disk** | /root/A-FORGE/src/domain/forge/EphemeralGenesisRunner.ts (also src/domain/containment/ + src/infrastructure/tools/EphemeralGenesis.ts); independent verify at verifyOutput() line ~387: "Independent verification: different method than the tool itself" |
| arif_route(intent=...) | **verified-on-disk** | /opt/arifos/app/arifosmcp/tools/kernel_canonical.py:11 ("route intent to organ"); organ_intent_map.yaml loader line 93-102; capability_id intent.route in /root/arifOS/static/manifest/tools.json:101 |
| forge_verifier | **claimed-by-Arif-but-NOT-found as that literal name.** No forge_verifier tool in the live 122. Verification capability EXISTS under different names: EphemeralGenesisRunner.verifyOutput() (independent, different-method) + live tools forge_runtime_verify, forge_verify_timeline. Report the rename, do not pretend forge_verifier exists. |
| success_basis=self_reported / success_verified=false | **verified-on-disk** | experienceTraceTools.ts:55 (comment "self_reported — supplied by the acting agent, NOT verified (Lane B)"), :238-239 (literal values) |
| kernel ABI 8 verbs | **verified-on-disk** | /root/arifOS/docs/KERNEL_CAPABILITY_ABI.md (sha cf1c7f6d…) + /root/arifOS/static/manifest/tools.json capability_id fields |

## PART D — Learning-loop chain (the file-5 content, verified as EXISTING substrate)

The redirect asked for a note that the learning loop uses existing A-FORGE substrate and
must NOT be re-implemented. I verified the substrate exists; recording the chain here as
sensory observation (I do not author doctrine — see PART E on collisions):

```
CAPABILITY SELECTED        → selections.jsonl (LIVE, 12 events) + forge_skill_select_query (LIVE tool)
EXECUTION                  → forge_execute / forge_run (LIVE)
EXPERIENCE TRACE           → forge_experience_trace (LIVE tool, serve.ts:317) — channels self/environmental/constitutional
INDEPENDENT VERIFICATION   → EphemeralGenesisRunner.verifyOutput() (different-method) — NOT self-certification;
                             but selections.jsonl outcome_success = 0/12 and no verification field → loop OPEN
SELECTION CREDIT           → forge_skill_select_query (read exposure exists; credit-back instrumentation = peer T5 PENDING)
FUTURE ROUTING PRIOR       → organ_intent_map.yaml (arifOS) — not yet fed by verified selection credit
```
The chain's substrate is real; the CLOSED loop is not — outcome backfill 0/12, independent-
verification field schema-absent, selection-credit instrumentation listed PENDING in peer
protocol T5. This matches Arif's premise (12 events, 0 outcomes). [DER]

## PART E — Collision map: the 5 redirected doctrine files (CRITICAL for hand-back)

The redirect asked me to write 5 files. As SENSORY lane I do not author/overwrite doctrine,
and 4 of the 5 ALREADY EXIST as committed peer work (FI-008). Writing my own at federation/
paths would fork duplicate doctrine over committed artifacts = LAW-8 clobber + duplicate-
registry scar class, and would violate the redirect's OWN principle ("use a projection, not
another registry"). The peer also already enacted the correction: commit b339b494 DELETED
the hand-maintained AFORGE_CAPABILITY_MAP.json (-229 lines) and replaced it with a generator.

| Redirect file | On disk? | Committed path | sha256 |
|---|---|---|---|
| (1) instructions/aforge-citizen-contract.md | **EXISTS (committed 004b7e6b)** | /root/AAA/instructions/aforge-citizen-contract.md | 4ed5a78282af744b459c6202ffdb19e2a8ad4e8678a220136fddf2025d5b2b90 |
| (2) WARGA_AFORGE_VIEW_SPEC (generator spec) | **EXISTS as code+doc, not as that .md filename** | generator /root/AAA/scripts/aforge_warga_view_generator.py (505a3e99…); verb schema /root/AAA/registries/AFORGE_VERB_SCHEMA.json (40ef03c5…); projection /root/AAA/state/aforge/warga-capabilities.json (2ba53183…); ROOT_AGENT_CONFIG block encodes C_warga rule | — |
| (3) AFORGE_COMPETENCY_SCHEMA | **EXISTS (committed b339b494)** | /root/AAA/instructions/aforge-competency-schema.md | 641db78356bc4439460128a724aa8171e26cb12690bbb5b93faed55fbb100d2b |
| (4) AFORGE_COMPETENCY_EVAL (E1-E8) | **EXISTS (committed b339b494)** | /root/AAA/instructions/aforge-competency-evals.md | 157ee926b1c4019a874f1f1d3f97ccd6cb7a4dd3d4430077c57a5781487b485e |
| (5) AFORGE_LEARNING_LOOP_NOTE | **NOT a dedicated file.** Content lives in PART D above + protocol T5 (PENDING). Genuinely not-yet-written. | — | — |

What the peer artifacts ALREADY contain (so a duplicate is pure drift):
- K_AF = R × A × E × V × L with "if any is zero, K_AF = 0" — competency-schema.md:63-75. ✓
- 5-identity split (Identity≠Citizenship≠Trust≠Competency≠ActiveAuthority) + Claude-vs-Kimi
  example semantics — competency-schema.md:11-54 + protocol doc. ✓
- E1-E8 with PASS criteria + graduation (W2_A-FORGE = E1∧…∧E8 semantics) — competency-evals.md. ✓
- C_warga = C_live ∩ C_affordance ∩ C_kernel ∩ C_authority + JIT + conflict policy —
  generator docstring + ROOT_AGENT_CONFIG forge_citizenship_contract + protocol doc. ✓
- ToolSuccess≠TaskSuccess≠VerifiedSuccess — citizen-contract.md:126 "Tool success is not
  task success" + truth chain declared→callable→competent→verified. ✓ (Note: the redirect's
  literal success_basis=self_reported / success_verified=false wording is NOT yet in the
  contract .md, though it is TRUE on disk at experienceTraceTools.ts:238-239.)

GENUINE content gaps a future authoring lane could EXTEND (not fork) into the existing files:
1. citizen-contract.md lacks the literal `success_basis=self_reported / success_verified=false`
   callout and the explicit 5-identity worked example (Claude VERIFIED/PROPOSE_AND_VERIFY vs
   Kimi DEGRADED/OBSERVE_ONLY) — currently only in schema.md prose.
2. No dedicated learning-loop note (PART D) — peer protocol T5 "selection credit
   instrumentation" is PENDING; a note file would be net-new, non-colliding.
3. Generator does not emit an explicit CONFLICT/HOLD policy section (DRIFT-2 shows 78/122
   tools silently unmapped rather than surfaced as UNCLASSIFIED→HOLD).

## PART F — Scar-class evidence summary

- **DRIFT-1 (MEDIUM):** competency state registry_fingerprint = federation-wide 343-tool
  digest (16e78b27…), not A-FORGE-scoped (aa39ecd5…). See receipt 1.
- **DRIFT-2 (MEDIUM):** generator maps only 44/122 live tools to verbs; 78 MAPS_NONE
  (silently dropped); 4 of 7 verbs have zero candidates. Selection class = silent-failure.
- **DRIFT-4 (MEDIUM):** A-FORGE source HEAD 237a7999 is 25 commits ahead of runtime
  f4a0a336, delta touches affordances.yaml + mcp/*.ts; health deployment_drift:false is
  runtime-vs-runtime only.
- **Missing fields (selection ledger):** independent_verification_result ABSENT from schema;
  outcome_success/outcome_summary/alternative_skills 0/12 populated; no capability-class field.
- **Stale registries:** tools_sot.yaml (self-deprecated, 51 vs 122), contracts/tools.yaml
  (2026-05-19, non-forge_* naming).
- **Duplicate-doctrine near-miss (AVOIDED):** 4/5 redirect files already committed by peer;
  this lane did not overwrite them (LAW-8 clobber + duplicate-registry scar class averted).

— 555-ASI Φ SENSE, Lane 555b. Read-only. No production artifact mutated.
