# AFORGE_CAPABILITY_MAP_v1_DRAFT — DRAFT 2026-10-01
# Status: DRAFT — cold-substrate inventory into 7 capability classes
# Author lane: 333b
# Source registry: /root/AAA/registries/CAPABILITY_INDEX.json (sha256 5ca6c2c00dd40505858c900cd4bf67b9305671122210d8c3a3a0b30f5131c42b)
# Supersedes: nothing yet

---

## 0. Purpose

Map each A-FORGE tool into one of 7 classes so an agent reasons in **capabilities**, not
tool names. This is the cold substrate beneath
`/root/AAA/instructions/aforge-citizen-contract*.md`: the contract is always loaded, this
map is retrieved only when an agent must resolve a capability to an exact tool.

Tools not currently in the registry are **NOT** included. Capability classes are stable;
tool membership is not. When the registry fingerprint changes, this map is re-derived —
never hand-edited.

Class counts: INSPECT 38 · PLAN 9 · ACT 20 · VERIFY 20 · EXTEND 5 · CONTROL 15 · LEARN 14 · UNCLASSIFIED 1 — **122 total**.

---

## 1. Source and method

### 1.1 Primary source

| Field | Value |
|---|---|
| File | `/root/AAA/registries/CAPABILITY_INDEX.json` |
| sha256 | `5ca6c2c00dd40505858c900cd4bf67b9305671122210d8c3a3a0b30f5131c42b` |
| Internal `digest` field | `16e78b27fbe030f7801d2b109cf5cf4cca7195ef07227c28bb80779b4e81a1b6` |
| `forgedAt` | `2026-09-29T15:07:52+00:00` |
| Schema | `arifOS/AAA-capability-index/v2.0.0` |
| Line range of A-FORGE entries | **69–1931** (122 `"server": "aforge"` records) |
| Federation total | 343 tools across all organs; A-FORGE = 122 (35.6%) |
| Captured | **2026-10-01** |
| A-FORGE tool count observed | **122** |
| sha256 of sorted 122-name list | `0a9b4339af4fca51b99d4977bce5a976f969a7b0a38bf7929524d2c9f173db17` |

### 1.2 Cross-checks performed (live probe before any claim)

Per the audit-methodology scar (2026-09-28: mandatory live probe before any gap claim),
the cold index was **not** trusted alone. Three independent sources were compared:

| Source | Count | Result |
|---|---|---|
| `CAPABILITY_INDEX.json` (cold, 2026-09-29) | 122 | baseline |
| **Live** `POST :7072/mcp` `tools/list` (2026-10-01) | 122 | **EXACT MATCH** — zero live-only, zero index-only |
| **Live** `GET :7071/health` | `tool_count: 122`, `tools_loaded: 122` | agrees |
| `/root/A-FORGE/a_think/affordances.yaml` | **132** | **DISAGREES** — see §1.3 |

Live `/health` also reported `deployed_commit: f4a0a33`, `source_commit: f4a0a33`,
`deployment_drift: false`, `status: healthy`, `version: v2026.07.24`.

### 1.3 Semantic surface source and its disagreement

`/root/A-FORGE/a_think/affordances.yaml`
(sha256 `cbe99c455e7c9924540d8d79e79ed63bdbb28c2d922ca719413969d117de1190`)
declares **132** tools — 10 more than exist. All 122 live tools *are* covered; the extra 10
are **phantom entries** (declared, not callable):

`forge_calendar`, `forge_cool_pattern`, `forge_docs_lookup`, `forge_drive`, `forge_gmail`,
`forge_minimax_search`, `forge_proxy_call`, `forge_research`, `forge_sheets`, `forge_whoami`

`forge_research` is already tombstoned in `organs.yaml` (CONVERGED 2026-09-17 FI-003
referential-integrity audit) but was never removed from `affordances.yaml`. This is exactly
the phantom class `forge_surface_audit` exists to detect — and the detector's own input file
is stale. Recorded as receipt, not fixed (read-only lane).

### 1.4 Method

1. Extract the 122 `server == "aforge"` records from `CAPABILITY_INDEX.json` (lines 69–1931).
2. Confirm the set against live `tools/list` on `:7072` — exact match required before classifying.
3. Join each tool to its `affordances.yaml` entry for `risk_label`, `mutation_class`,
   `destructive`, `reversible`, `external_side_effect`, `requires_human_approval`,
   `capability_surface`.
4. Derive **risk band** from evidence (precedence: destructive ∨ ¬reversible → `irreversible`;
   else requires_human_approval → `irreversible`; else external_side_effect → `external`;
   else mutation_class ∈ {MUTATE, EXECUTE_REVERSIBLE} → `mutate`; else `read`).
5. Assign **primary class** from the tool's own stated purpose + `capability_surface`,
   and a **secondary class** where the tool genuinely serves two capabilities.
6. Where affordance flags contradict the tool's own description, correct **upward** and
   mark `(dispute)` in Notes. Never silently trust the lower-risk source.
7. Flag `⚖` where the tool delegates or transfers authority to arifOS.

No tool was classified by name-pattern alone. Every row is backed by description text plus
affordance flags.

---

## 2. The 7 classes

| Class | One-line |
|---|---|
| **INSPECT** | Understand — read state from filesystem, repo, browser, web, registry, infra. |
| **PLAN** | Structure — compile intent into a bounded, dependency-aware, budgeted task. |
| **ACT** | Change — mutate filesystem, shell, git, browser, deployment, money. |
| **VERIFY** | Prove — independent comparison of result against intent and acceptance criteria. |
| **EXTEND** | Acquire a missing capability — ephemeral forge, backend/model acquisition, registration. |
| **CONTROL** | Recover and bound — status, abort, rollback, lease, lock, retry, pause/resume. |
| **LEARN** | Improve — outcome traces, experience, scar, selection credit, world-model quality. |

Routing chain these serve:
`intent → capability → authority → implementation → evidence → verification → outcome`

---

## 3. The mapping table

122 rows. `⚖` = delegates/transfers authority to arifOS (§5.6).
Risk bands: `read` (71) · `mutate` (21) · `external` (19) · `irreversible` (11).

| Tool | Class | Secondary | Risk band | Notes |
|---|---|---|---|---|
| `forge_agent` | INSPECT | CONTROL | read | Modes register/status/list/kill span inspect+control. Index action_class=OBSERVE though kill mutates. |
| `forge_apex_goal_status` | INSPECT | PLAN | read | Reads goal state: tasks, G, C_dark, Jacobian, metabolic history. |
| `forge_browser_extract_text` | INSPECT | — | external | Read-only page text extraction. |
| `forge_browser_navigate` | INSPECT | — | external | Index action_class=MUTATE but affordance R0/read and description says OBSERVE-class (dispute). |
| `forge_browser_screenshot` | INSPECT | — | external | Index action_class=MUTATE but description says OBSERVE-class (dispute). |
| `forge_canon_recall` | INSPECT | LEARN | read | Semantic recall over canon incl. scar corpus. Only tool with risk_label=None in affordances. |
| `forge_chart` | INSPECT | LEARN | read | Charting + eureka margin-pattern candidates. |
| `forge_docsgpt` | INSPECT | — | read | Governed DocsGPT knowledge query behind F2/F7 membrane. |
| `forge_document_ingest` | INSPECT | — | read | Layout-first parsing w/ bbox provenance. Index action_class=MUTATE but parsing is read (dispute). |
| `forge_entropy_sweep` | INSPECT | LEARN | read | Measures workspace dS: file count, uncommitted changes, temp files, hotspots. |
| `forge_fetch` | INSPECT | — | external | Governed URL evidence intake + SearxNG search. Affordance external_side_effect=False UNDER-REPORTS network egress (dispute). |
| `forge_filesystem` | INSPECT | ACT | mutate | read/write/patch/delete/search in one primitive. Affordance R0/read understates write+delete (dispute). |
| `forge_github` | INSPECT | — | read | search + pr modes. |
| `forge_github_get_file` | INSPECT | — | read | Reads a file from GitHub. |
| `forge_health_check` | INSPECT | CONTROL | read | A-FORGE server health + constitutional genome v2.0 status. |
| `forge_journalctl` | INSPECT | — | read | systemd journal query, read-only + PII-redacted. |
| `forge_memory` | INSPECT | LEARN | read | L3 semantic recall (Qdrant + capability registry) w/ Supabase vault fallback + SRO admissibility gate. |
| `forge_netdata_alarms` | INSPECT | — | read | Read Netdata alarms. |
| `forge_netdata_metrics` | INSPECT | — | read | Read Netdata chart data. |
| `forge_probe` | INSPECT | CONTROL | read | Federation organ liveness: all 5 organs + latency. |
| `forge_probe_site` | INSPECT | — | read | Probes a web/cockpit surface for resilience + compliance. |
| `forge_registry` | INSPECT | LEARN | read | status/list/get/scars/fingerprint/scan - the JIT discovery surface. |
| `forge_registry_status` | INSPECT | CONTROL | read | callable/blocked/degraded/drift for all tools + fingerprinting. |
| `forge_search` | INSPECT | — | external | Unified governed search: Brave web + Context7 docs + deep research w/ provenance. |
| `forge_shell_alert_history` | INSPECT | LEARN | read | Recent ArifJudge DENY/GATE/self-modification alerts. Read-only. |
| `forge_shell_dryrun` | INSPECT | VERIFY | read | Previews a command WITHOUT executing. F1 AMANAH: pure dry-run. |
| `forge_shell_ledger` | INSPECT | VERIFY | read | Queries ArifSeal hash-chain ledger + chain integrity status. |
| `forge_shell_status` | INSPECT | CONTROL | read | forge_shell subsystem health: ledger state, judge pattern count, defaults. |
| `forge_skillstore_read` | INSPECT | — | read | Artifact store semantic search w/ tag filtering. |
| `forge_vault` | INSPECT | LEARN | mutate | VAULT999 cache layer: read/list/write/receipt. Seal itself routes to arifOS. Affordance R0/read understates write (dispute). |
| `forge_vps_cron` | INSPECT | — | read | Cron registry from root crontab, /etc/crontab, /etc/cron.d. Does not mutate. |
| `forge_vps_ports` | INSPECT | — | read | Listening ports classified public/internal/unknown. Does not trust UFW alone (Docker bypass). |
| `forge_vps_services` | INSPECT | — | read | Running systemd services + Docker containers. |
| `forge_wealth` ⚖ | INSPECT | — | read | Organ bridge to WEALTH: emv/conservation/flow/runway/wisdom. |
| `forge_web_extract` | INSPECT | — | external | Agentic web extraction: SPA rendering, browser actions, authenticated sessions, downloads. |
| `forge_web_zen` | INSPECT | VERIFY | read | web_zen CLI wrapper: sense/verify/orphan(dry-run only)/ephemeral/doctor. |
| `forge_well` ⚖ | INSPECT | — | read | Organ bridge to WELL (:18083): state/readiness/floors/anchor/machine_intelligence. |
| `forge_worktree` | INSPECT | — | read | Local git physics sensor: branch, dirty state, stash, conflicts, in-progress ops, blast radius. |
| `auth_pipeline` | PLAN | INSPECT | read | Declares the OBSERVE->MUTATE->DEPLOY gate pipeline. Protocol surface, not an executor - see Gaps. |
| `forge_apex_encode` | PLAN | — | read | Encodes goal -> task vector T with Jacobian. Returns G_local (is_canonical_g=false). |
| `forge_apex_recompute` | PLAN | — | read | Recomputes task plan when a governance field changes; only sensitivity>0.6 recalculated. |
| `forge_compile_task` | PLAN | — | mutate | Compiles intent -> immutable TaskIR over arif_route.444. Frozen at creation. |
| `forge_compose` | PLAN | ACT | external | Composition Bus: sequential/parallel/conditional/loop DAG with cycle detection. Index action_class=OBSERVE but description says MUTATE (dispute). |
| `forge_dispatch_lane` | PLAN | ACT | irreversible | Dispatches frozen TaskIR to one bounded lane; one-dispatch-per-TaskIR. reversible=False. |
| `forge_parallel` | PLAN | ACT | mutate | Fan-out N concurrent A2A tasks w/ bounded concurrency + failure policies. Affordance R0/read understates spawn (dispute). |
| `forge_predict` ⚖ | PLAN | VERIFY | read | Pre-action simulation; GEOX/WEALTH forward models run BEFORE forge_execute, result attached as evidence to arif_judge. |
| `forge_reality_loop` | PLAN | CONTROL | read | Intent compiler: 7-stage ledger MEANING->OBSERVE->ENCODE->IMPROVE->VERIFY->SEAL->RETURN. Modes incl. seal + destroy. |
| `forge_browser_click` | ACT | — | external | Browser actuation on a live page. |
| `forge_browser_evaluate_js` | ACT | INSPECT | external | Arbitrary JS in browser context. Index action_class=GOVERN - odd for a browser actuator. |
| `forge_browser_type` | ACT | — | external | Types into a page field; can submit forms. |
| `forge_canonize` | ACT | LEARN | mutate | Promotes draft -> CANON, computes sha256, writes receipt. Affordance R0/read understates (dispute). |
| `forge_docker` | ACT | — | irreversible | ps/logs/exec/images. Destructive ops excluded from this route by design. |
| `forge_execute` | ACT | — | irreversible | Execution/motor cortex (stage 777 FORGE). Requires cc_id for mutations (INV-4). |
| `forge_execute_sealed` | ACT | VERIFY | irreversible | Executes only with VAULT999 seal or stage_id+human_seal_token. FAILS HARD without authorization. |
| `forge_git` | ACT | INSPECT | external | status/diff/log/commit. Mutating modes floor-gated. ext=True reflects remote ops. |
| `forge_git_commit` | ACT | — | mutate | Governed commit w/ pre-commit checks; EXECUTE_HIGH_IMPACT in actionClassifier.ts. Affordance R0/read is WRONG (dispute). |
| `forge_github_create_issue` | ACT | — | external | Creates a GitHub issue. Lease required. |
| `forge_github_create_or_update_file` | ACT | — | external | Writes a file to GitHub. |
| `forge_pipeline_run` | ACT | PLAN | irreversible | Autonomous pipeline: routes organs, evidence->compute->(judge+seal). Index action_class=OBSERVE but description says MUTATE (dispute). |
| `forge_postgres` | ACT | INSPECT | external | query + schema. Writes require mutate=true and stay floor-gated. Index action_class=OBSERVE but description says MUTATE (dispute). |
| `forge_sandbox_run` | ACT | VERIFY | mutate | Executes staged artifact in isolated sandbox w/ ABSOLUTE non-overridable timeout. ext=True reflects sandbox backend, not external world. |
| `forge_send_confirm` | ACT | — | irreversible | Sends data with human confirmation via elicitation (form + URL modes). F13 consent gate. |
| `forge_shell` | ACT | — | irreversible | Canonical governed shell via ArifJudge gate + ArifSeal hash chain. DENY patterns hard-blocked, GATE patterns need human approval. |
| `forge_skillstore_write` | ACT | LEARN | external | Stores artifact w/ provenance. WRITE mode only; two-layer retention + SCAR immunization. |
| `forge_stage` | ACT | CONTROL | external | Stages an artifact or governance preview; governance mode returns ui://aforge/preview/<stage_id>. |
| `forge_synthesize` | ACT | EXTEND | external | Creates artifact from intent. Code goes to a temporary buffer ONLY - never touches filesystem. |
| `forge_transfer_confirm` | ACT | — | irreversible | MONEY movement with human confirmation. F13 consent gate; blocks until accept/decline/cancel. |
| `forge_apex_emd` | VERIFY | PLAN | read | EMD validation gate; detects drift + scope creep. Returns ToAC verdict. |
| `forge_check_governance` ⚖ | VERIFY | — | read | Constitutional check DELEGATED to arifOS. A-FORGE never adjudicates floors. |
| `forge_collect_evidence` | VERIFY | ACT | mutate | Builds typed evidence packet (diffs+tests+cost). ext flag reflects federation routing, not external world. |
| `forge_docket_prep` | VERIFY | CONTROL | read | Packages evidence and RELINQUISHES CONTROL to arifOS; docket is read-only. |
| `forge_evaluate` | VERIFY | — | read | APEX v36-Omega G-space gate; G=(A.P.E.X)^(1/4), is_canonical_g=true. Returns SEAL/REVIEW/VOID. |
| `forge_fingerprint_check` | VERIFY | INSPECT | read | Computes/verifies tool fingerprints; detects duplicate tools + schema drift. |
| `forge_heart_critique` ⚖ | VERIFY | — | read | Risk/ethical review DELEGATED to arifOS 666 HEART. No local floor adjudication. |
| `forge_isomorphism_check` | VERIFY | INSPECT | read | J-space manifold stability; verifies GEOX<->arifOS isomorphism pairs via runtime witness. |
| `forge_judge_proxy` ⚖ | VERIFY | — | read | Pure forwarder to canonical arifOS constitutional judge. |
| `forge_receipt_draft` | VERIFY | — | read | Drafts a compliance receipt formatted for arifOS VAULT999 verification. |
| `forge_runtime_verify` | VERIFY | INSPECT | read | git source commit vs installed wheel vs import path -> MATCH|DRIFT|UNKNOWN. Fail-closed on DRIFT. |
| `forge_scan` | VERIFY | INSPECT | read | Security scan of file/dir BEFORE code execution; detects dangerous patterns. |
| `forge_seal_run` | VERIFY | LEARN | mutate | Submits TaskIR+evidence to constitutional judgment; returns AWAITING_VERIFICATION. Only arif_judge.666 may upgrade to SEAL. |
| `forge_security_drift_scan` | VERIFY | INSPECT | read | Live ports/services/cron vs Machine Constitution registry; flags unknown public ports, rogue containers. |
| `forge_surface_audit` | VERIFY | INSPECT | read | Live registry vs affordances.yaml: phantom entries, missing tools, description drift, alias conflicts. |
| `forge_surface_guard` | VERIFY | INSPECT | read | Schema fingerprinting + drift detection: check/status/pin/config. |
| `forge_verify_timeline` | VERIFY | — | read | TIMELINE_MIN_SOURCES invariant: no timeline claim passes with <2 independent sources. |
| `forge_visual_qa` | VERIFY | — | read | W3 tri-witness (vision+linter+sovereign) + scar consult + entropy gate. PASS does not exist - only PASS_CANDIDATE. |
| `forge_visual_seal` | VERIFY | LEARN | irreversible | VAULT999 composite seal; validates W3 hash, I1-I5 invariants. Index action_class=SEAL but affordance R0/read/hr=False (dispute). |
| `forge_witness` | VERIFY | — | read | Tri-witness consensus W3=cbrt(Human*AI*External) (Nash 1950). Zero in any channel voids consensus. |
| `forge_ephemeral` | EXTEND | VERIFY | mutate | THE extend tool: inspect_gap->generate->sandbox_test->invoke->verify->retire. Affordance R0/read understates generation+invocation (dispute). |
| `forge_gemini` | EXTEND | INSPECT | external | External model backend bridge (Google AI Studio, 127.0.0.1:18092). Backend acquisition - see Gaps. |
| `forge_hf_import` ⚖ | EXTEND | VERIFY | read | Hugging Face model/dataset import gate through F1-F13. "The gate validates - the kernel seals." |
| `forge_register` | EXTEND | CONTROL | read | Gated tool registration: requires SEAL verdict + tri-witness CONSENSUS + HARAM pass + scar consult. Non-compensable. |
| `forge_skill` | EXTEND | ACT | external | Dynamic tool forge: generates a new MCP tool via LLM, HARAM-gated, sealed to VAULT999. 24h expiry, max depth 1. Index action_class=OBSERVE but description says MUTATE (dispute). |
| `forge_abort` | CONTROL | — | irreversible | Safe stop + rollback. Index description says MUTATE but action_class=OBSERVE (registry inconsistency). |
| `forge_job` | CONTROL | ACT | mutate | Background job system: submit + status. Affordance R0/read understates submit (dispute). |
| `forge_lease` ⚖ | CONTROL | — | mutate | Lease request/status/revoke. "A-FORGE does not self-issue leases - arifOS mints them." Affordance R0/read understates (dispute). |
| `forge_lock` | CONTROL | ACT | mutate | Amanah/F1 lock: acquire (reversible gate before mutation) / release. Affordance R0/read understates (dispute). |
| `forge_parallel_cancel` | CONTROL | — | mutate | Propagates tasks/cancel to non-terminal members. Affordance R0/read understates (dispute). |
| `forge_parallel_list` | CONTROL | INSPECT | read | Lists task groups + status. |
| `forge_parallel_status` | CONTROL | INSPECT | read | Group status: member states, outputs, delta anchors. |
| `forge_policy` | CONTROL | EXTEND | mutate | MCP Policy Engine check/set/remove/list/save. set+remove+save are SOVEREIGN-ONLY. Affordance R0/read understates (dispute). |
| `forge_sandbox_auto_evict` | CONTROL | ACT | mutate | Purges snapshots >24h from cold storage. Index MUTATE; affordance R0/read (dispute). |
| `forge_sandbox_list_paused` | CONTROL | INSPECT | read | Lists paused sandboxes w/ snapshot age. |
| `forge_sandbox_pause` | CONTROL | ACT | mutate | tar upperdir + sha256 + unmount overlay -> cold storage. Index MUTATE; affordance R0/read (dispute). |
| `forge_sandbox_resume` | CONTROL | ACT | mutate | Extract tarball + re-mount overlay + lease re-verify. Index MUTATE; affordance R0/read (dispute). |
| `forge_session_init` ⚖ | CONTROL | — | read | Session ignition PROXIED to arifOS - A-FORGE no longer mints independent sessions. 7 classes have no BOOT verb; see Gaps. |
| `forge_status` | CONTROL | INSPECT | read | Active execution state: jobs, leases, agents. |
| `forge_tier_bind` ⚖ | CONTROL | EXTEND | mutate | Sets trust tier LOWER BOUND only - A-FORGE cannot promote, only arifOS sets actual tier. Affordance R0/read understates (dispute). |
| `forge_apex_metabolize` | LEARN | PLAN | mutate | Adjusts risk/constraint weights FROM TASK OUTCOMES = outcome learning. Index MUTATE; affordance says R0/read (dispute). |
| `forge_cool` | LEARN | VERIFY | read | Emits COOLING_RECEIPT (verb=drift|pattern) -> VAULT999 append. INV-C1 OBSERVE-only, INV-C2 no forge caller. |
| `forge_experience_query` | LEARN | — | read | Read-only query over experience traces by agent/tool/feedback type. |
| `forge_experience_trace` | LEARN | — | read | Records Chain-of-Experience: action->observation->feedback->delta. 3 feedback channels. |
| `forge_rsi_dual_rate_fq` | LEARN | INSPECT | read | Daily FQ (observational) vs 7-day rolling FQ (constitutional). Daily is ALIASED for weekly governance cycles. |
| `forge_rsi_impulse_response` | LEARN | INSPECT | read | Impulse response h(t): causal half-life of 888_HOLD / scar seal / tool failure in later routing. |
| `forge_rsi_state_vector` | LEARN | INSPECT | read | s_t=(identity,plant,memory,controller) computed from live traces, not stored. |
| `forge_scar` | LEARN | CONTROL | mutate | Seals failures as PERMANENT constitutional constraints (seal/list/consult). Index action_class=OBSERVE+risk low CONTRADICTS "permanent" (dispute). |
| `forge_seal` | LEARN | VERIFY | irreversible | Seals a Tri-Witness-validated skill into permanent VAULT999. IRREVERSIBLE: cannot be deleted, demoted, or expired. Needs REVIEWED tier + F13. |
| `forge_skill_select_query` | LEARN | — | read | Which skills were selected, by what method (keyword/learned/manual/routed/fallback) + outcomes. This IS selection credit. |
| `forge_trust_score` | LEARN | VERIFY | read | Scores external MCP servers on 5 dims -> ALLOW/LIMITED/HOLD/DENY bands; keeps history. |
| `forge_wm_gaps` | LEARN | INSPECT | read | High-confidence WRONG predictions, cross-referenced against experience feedback. |
| `forge_wm_quality` | LEARN | INSPECT | read | Grades tools A-D on training-data quality; assesses ECHO/PaW RL readiness. |
| `forge_wm_stats` | LEARN | INSPECT | read | Record counts, per-tool surprise scores, WM eligibility, prediction trending. |
| `forge_kernel` ⚖ | UNCLASSIFIED | — | read | Proxy exposing ALL 8 arifOS verbs (init/observe/think/route/memory/judge/forge/seal). Spans every class; it is an authority bridge, not a capability. See Gaps. |

---

## 4. Per-class summary

### INSPECT — 38 tools

> Understand — read state from filesystem, repo, browser, web, registry, infra.

- **Highest risk band present:** `external`
- **Band spread:** read:30 · mutate:2 · external:6
- **Tools carrying a secondary class:** 17/38
- **Representative:** `forge_filesystem`, `forge_search`, `forge_registry`, `forge_worktree`, `forge_probe`
- **Hot path (JIT-discovered most often):** `forge_filesystem`, `forge_search`, `forge_fetch`, `forge_registry`, `forge_worktree`, `forge_probe`
- **Cold substrate (rarely needed, stays unloaded):** `forge_netdata_alarms`, `forge_netdata_metrics`, `forge_vps_cron`, `forge_journalctl`, `forge_docsgpt`, `forge_web_zen`, `forge_shell_alert_history`

### PLAN — 9 tools

> Structure — compile intent into a bounded, dependency-aware, budgeted task.

- **Highest risk band present:** `irreversible`
- **Band spread:** read:5 · mutate:2 · external:1 · irreversible:1
- **Tools carrying a secondary class:** 6/9
- **Representative:** `forge_compile_task`, `forge_dispatch_lane`, `forge_compose`, `forge_predict`, `auth_pipeline`
- **Hot path (JIT-discovered most often):** `forge_compile_task`, `forge_dispatch_lane`, `forge_compose`
- **Cold substrate (rarely needed, stays unloaded):** `forge_apex_encode`, `forge_apex_recompute`, `forge_reality_loop`, `auth_pipeline`

### ACT — 20 tools

> Change — mutate filesystem, shell, git, browser, deployment, money.

- **Highest risk band present:** `irreversible`
- **Band spread:** mutate:3 · external:10 · irreversible:7
- **Tools carrying a secondary class:** 10/20
- **Representative:** `forge_shell`, `forge_git`, `forge_execute`, `forge_sandbox_run`, `forge_docker`
- **Hot path (JIT-discovered most often):** `forge_shell`, `forge_git`, `forge_execute`, `forge_sandbox_run`, `forge_docker`
- **Cold substrate (rarely needed, stays unloaded):** `forge_transfer_confirm`, `forge_send_confirm`, `forge_canonize`, `forge_synthesize`, `forge_github_create_issue`, `forge_github_create_or_update_file`

### VERIFY — 20 tools

> Prove — independent comparison of result against intent and acceptance criteria.

- **Highest risk band present:** `irreversible`
- **Band spread:** read:17 · mutate:2 · irreversible:1
- **Tools carrying a secondary class:** 12/20
- **Representative:** `forge_collect_evidence`, `forge_runtime_verify`, `forge_witness`, `forge_evaluate`, `forge_visual_qa`
- **Hot path (JIT-discovered most often):** `forge_collect_evidence`, `forge_runtime_verify`, `forge_witness`, `forge_evaluate`, `forge_visual_qa`
- **Cold substrate (rarely needed, stays unloaded):** `forge_isomorphism_check`, `forge_verify_timeline`, `forge_docket_prep`, `forge_heart_critique`, `forge_fingerprint_check`, `forge_security_drift_scan`

### EXTEND — 5 tools

> Acquire a missing capability — ephemeral forge, backend/model acquisition, tool registration.

- **Highest risk band present:** `external`
- **Band spread:** read:2 · mutate:1 · external:2
- **Tools carrying a secondary class:** 5/5
- **Representative:** `forge_ephemeral`, `forge_skill`, `forge_register`, `forge_hf_import`, `forge_gemini`
- **Hot path (JIT-discovered most often):** `forge_ephemeral`, `forge_skill`
- **Cold substrate (rarely needed, stays unloaded):** `forge_hf_import`, `forge_gemini`, `forge_register`

### CONTROL — 15 tools

> Recover and bound — status, abort, rollback, lease, lock, retry, pause/resume.

- **Highest risk band present:** `irreversible`
- **Band spread:** read:5 · mutate:9 · irreversible:1
- **Tools carrying a secondary class:** 11/15
- **Representative:** `forge_status`, `forge_abort`, `forge_lease`, `forge_lock`, `forge_sandbox_pause`
- **Hot path (JIT-discovered most often):** `forge_status`, `forge_abort`, `forge_lease`, `forge_lock`
- **Cold substrate (rarely needed, stays unloaded):** `forge_parallel_cancel`, `forge_parallel_list`, `forge_parallel_status`, `forge_sandbox_auto_evict`, `forge_sandbox_list_paused`, `forge_policy`, `forge_tier_bind`, `forge_job`

### LEARN — 14 tools

> Improve — outcome traces, experience, scar, selection credit, world-model quality.

- **Highest risk band present:** `irreversible`
- **Band spread:** read:11 · mutate:2 · irreversible:1
- **Tools carrying a secondary class:** 11/14
- **Representative:** `forge_scar`, `forge_experience_trace`, `forge_experience_query`, `forge_skill_select_query`, `forge_seal`
- **Hot path (JIT-discovered most often):** `forge_scar`, `forge_experience_query`
- **Cold substrate (rarely needed, stays unloaded):** `forge_rsi_dual_rate_fq`, `forge_rsi_impulse_response`, `forge_rsi_state_vector`, `forge_wm_gaps`, `forge_wm_quality`, `forge_wm_stats`, `forge_cool`, `forge_apex_metabolize`, `forge_trust_score`

### UNCLASSIFIED — 1 tools

> Does not map to one capability — spans classes or is an authority bridge rather than a capability.

- **Highest risk band present:** `read`
- **Band spread:** read:1
- **Tools carrying a secondary class:** 0/1
- **Representative:** `forge_kernel`
- **Hot path (JIT-discovered most often):** —
- **Cold substrate (rarely needed, stays unloaded):** —

---

## 5. Gaps

**5.1 `forge_kernel` — UNCLASSIFIED (1 tool).**
`capability_surface: aforge.governance.kernel`. It proxies all 8 arifOS verbs
(`init | observe | think | route | memory | judge | forge | seal`) through one A-FORGE
entry point. It is therefore *not* one capability — it is a multiplexer over every
capability plus the authority plane. Forcing it into a class would mislead an agent
into thinking a single tool answers to one verb. Classified `UNCLASSIFIED` deliberately.

**5.2 No GOVERN class exists in the 7, but 19 tools are governance-surfaced.**
`capability_surface: aforge.governance.*` covers 19 tools:
`auth_pipeline`, `forge_apex_emd`, `forge_apex_encode`, `forge_apex_goal_status`, `forge_apex_metabolize`, `forge_apex_recompute`, `forge_check_governance`, `forge_evaluate`, `forge_heart_critique`, `forge_judge_proxy`, `forge_kernel`, `forge_predict`, `forge_reality_loop`, `forge_seal_run`, `forge_session_init`, `forge_trust_score`, `forge_visual_qa`, `forge_visual_seal`, `forge_witness`.
The 7 classes have no GOVERN verb, so these were distributed by *function*, not surface:
verdict-producing ones to VERIFY (`forge_evaluate`, `forge_witness`, `forge_check_governance`),
goal-structuring ones to PLAN (`forge_predict`, `forge_reality_loop`, `auth_pipeline`),
outcome-weighting ones to LEARN (`forge_trust_score`, `forge_seal`, `forge_apex_metabolize`),
boundary-setting ones to CONTROL (`forge_session_init`, `forge_tier_bind`).
This is the largest structural strain in the mapping. An 8th class (GOVERN) would absorb
them cleanly — but that is Arif's binary, not the mapper's call. See §7.

**5.3 No BOOT class exists.**
`forge_session_init` (stage 000 INIT) is the entry point of the routing chain but the 7
classes begin at INSPECT. It was placed in CONTROL because it establishes and bounds the
session, yet semantically it is a *precondition* of all 7. Contract §3 handles boot
procedurally instead; note the class model does not represent it.

**5.4 `auth_pipeline` is a protocol declaration, not an executor.**
Its description is the OBSERVE→MUTATE→DEPLOY three-law pipeline itself
(`DECLARE → FQ_GATE → LEASE → LOCK → EXECUTE → EVIDENCE → VERIFY → JUDGE → MERGE → SEAL → INGEST`).
Mapped to PLAN as the pipeline *shape*, but an agent that "calls auth_pipeline to plan"
will get a doctrine recital, not a plan. Candidate for deprecation as a callable tool.

**5.5 INSPECT∩VERIFY dual-class tools (10).**
These are genuinely both — they read *in order to prove*:
`forge_fingerprint_check`, `forge_isomorphism_check`, `forge_runtime_verify`, `forge_scan`, `forge_security_drift_scan`, `forge_shell_dryrun`, `forge_shell_ledger`, `forge_surface_audit`, `forge_surface_guard`, `forge_web_zen`.
Recorded as primary + secondary rather than forced into one.

**5.6 Tools bridging to arifOS authority — ⚖ flag (11).**
Each of these **transfers or delegates authority**; A-FORGE holds no verdict power in them:
- `forge_check_governance`
- `forge_heart_critique`
- `forge_hf_import`
- `forge_judge_proxy`
- `forge_kernel`
- `forge_lease`
- `forge_predict`
- `forge_session_init`
- `forge_tier_bind`
- `forge_wealth`
- `forge_well`

Two sub-kinds, and the difference matters at call time:
- **Verdict-delegating** (`forge_judge_proxy`, `forge_check_governance`, `forge_heart_critique`,
  `forge_kernel`, `forge_session_init`, `forge_lease`, `forge_tier_bind`) — A-FORGE forwards
  and the answer comes from arifOS. A success return here is *not* a verdict.
- **Organ/evidence bridges** (`forge_wealth`, `forge_well`, `forge_hf_import`, `forge_predict`) —
  A-FORGE supplies evidence *toward* a judgment made elsewhere. `forge_hf_import` states it
  plainly: "The gate validates — the kernel seals."

Per Organ Domain Boundary Law (2026-09-17) only arifOS emits AUTHORIZED/HOLD/VOID.
The ⚖ flag marks where an agent must not read an A-FORGE return as a verdict.
`forge_web_zen` and `forge_git_commit` were considered and **excluded**: the first wraps a
CLI, the second delegates internally to `forge_git` — neither crosses into arifOS authority.

**5.7 Registry self-contradiction — 26 tools carry conflicting class metadata.**
Three sources disagree per-tool. Examples:
- `forge_scar` — index `action_class: OBSERVE`, `risk_tier: low`, `authority_ceiling: UNBOUNDED`,
  yet its own description says it "Seals failures as **permanent** constitutional constraints."
  A permanent, non-deletable mutation is not OBSERVE/low.
- `forge_git_commit` — affordance `R0`/`OBSERVE`, but index description names it
  `EXECUTE_HIGH_IMPACT in actionClassifier.ts`. R0 is wrong.
- `forge_fetch` — affordance `external_side_effect: false`, yet it fetches URLs and queries
  SearxNG. Network egress is under-reported.
- `forge_visual_seal` — index `action_class: SEAL`, affordance `R0`/`requires_human_approval: false`.
- 6 tools have descriptions declaring MUTATE while `action_class` says OBSERVE:
  `forge_abort`, `forge_compose`, `forge_pipeline_run`, `forge_postgres`,
  `forge_sandbox_run`, `forge_skill`.

Risk bands in §3 were derived from the **affordances.yaml** flags
(`destructive`/`reversible`/`requires_human_approval`/`external_side_effect`), then
hand-corrected upward where the tool's own description contradicts them. Every correction
is flagged `(dispute)` in the Notes column. `authority_ceiling: UNBOUNDED` on all 122
index entries was **ignored** — see §7, it is false.

---

## 6. JIT strategy

An agent should never load this file's table into context. Resolve capability → tool at
call time:

1. **Class first.** Name the capability (INSPECT/PLAN/ACT/VERIFY/EXTEND/CONTROL/LEARN) from
   task intent — before looking at any tool name.
2. **Fingerprint check.** `GET :7071/health` → read `tool_count` + `deployed_commit`.
   Compare against the fingerprint recorded in this file's frontmatter. If unchanged, the
   cached class membership is still valid; skip re-discovery.
3. **Narrow query.** Call `forge_registry(mode="list")` or `forge_registry_status` and
   filter by `capability_surface` prefix (`aforge.<class-ish domain>.*`), not by loading all
   122 schemas. Surface prefixes are the stable join key: `probe`→INSPECT, `execute`→ACT,
   `governance`→VERIFY, `registry`→CONTROL, `meta`→LEARN/PLAN, `skill`→EXTEND, `vault`→LEARN.
4. **One manifest.** `forge_registry(mode="get", tool=<name>)` to pull a single schema only
   when the exact parameter shape is needed.
5. **Least power.** Among candidates in the class, take the narrowest risk band that
   completes the task. Never escalate to `forge_shell` because it is general.
6. **Extremely cold path.** Only if the class query returns nothing useful: read §3 of this
   file directly. That is a diagnosis path, not a routing path.
7. **Never re-inject.** After resolution, the 122 schemas stay cold substrate.

---

## 7. Open questions for Arif

**Q1 — F13 binary: is `authority_ceiling: UNBOUNDED` on all 122 index entries a bug or a claim?**
`CAPABILITY_INDEX.json` stamps `authority_ceiling: UNBOUNDED` for **every one** of the 122
A-FORGE tools. Three sources contradict it:
- Live `/health` reports `authority_ceiling: "777_FORGE"`.
- `organs.yaml` declares A-FORGE `authority_ceiling: EXECUTE_AFTER_SEAL`.
- `organs.yaml` lists `forbidden_domains: [constitutional_judgment, self_authorization,
  earth_evidence, capital_allocation]`.

An index that tells every agent its ceiling is UNBOUNDED is the inverse of the federation
thesis (AGI = Capability↑ ⇒ Authority∅). I ignored the field. **Needs your binary:
is the index field wrong, or is it a deliberate statement about tool-level reachability
distinct from actor-level authority?** This is canonical-records class, so it is yours.

**Q2 — F13 binary: does LEARN exist as a class, or is it 7 verbs without it?**
FI-008's already-committed draft at
`/root/AAA/registries/AFORGE_VERB_SCHEMA.json` proposes 7 verbs:
`forge_inspect, forge_plan, forge_change, forge_run, forge_verify, forge_extend, forge_control`.
Your spec proposes a different 7: `INSPECT, PLAN, ACT, VERIFY, EXTEND, CONTROL, LEARN`.
The deltas: FI-008 splits ACT into `change`+`run` and **has no LEARN**; your spec has one
ACT and **has LEARN**. 14 tools in my mapping are LEARN-primary
(`forge_scar`, `forge_experience_*`, `forge_skill_select_query`, `forge_wm_*`, `forge_rsi_*`,
`forge_cool`, `forge_seal`, `forge_trust_score`, `forge_apex_metabolize`). Under FI-008's
verb set these 14 have **no home** — they would fall into `forge_inspect` by default, which
is how 9 of 10 already landed there in the live projection
(`/root/AAA/state/aforge/warga-capabilities.json`: `forge_wm_quality`→`forge_inspect`,
the other 9 absent entirely). Naming is your binary per F13 Intent-not-Syntax.

**Q3 — Is an 8th class GOVERN wanted?** §5.2: 19 tools are `aforge.governance.*`
and I distributed them across VERIFY/PLAN/LEARN/CONTROL by function. That distribution is
defensible but lossy. An 8th class would absorb them. Alternatively the governance surface
stays *outside* the capability model entirely, since A-FORGE never adjudicates — it only
forwards. Which framing do you want?

**Q4 — Boot has no class.** `forge_session_init` sits in CONTROL by my mapping (§5.3) but is
really a precondition of all 7. Accept CONTROL, or treat boot as contract §3 prose only and
leave it unmapped?

**Q5 — 10 phantom tools in `affordances.yaml`.** §1.3. `forge_surface_audit` should have
caught these; its own input is stale. Cleanup is a mutation, outside this lane. Do you want
a separate FI task to reconcile `affordances.yaml` to the live 122?

**Q6 — `forge_kernel` stays UNCLASSIFIED?** §5.1. My recommendation: yes, keep it
UNCLASSIFIED and treat it as an authority bridge (⚖), not a capability. Confirm or
override.

**Q7 — 26 tools with self-contradictory risk metadata.** §5.7. My bands are
corrected upward from the tool's own description where sources disagreed. That is a
judgment call in a read-only lane — it should be ratified or recomputed from a fixed
authority. Which source wins when description and affordance disagree?

---

## 8. Adoption gate

This section is FORWARD-LOOKING and NOT YET ACTIVE. When adopted, this map will require:

- [ ] `ROOT_AGENT_CONFIG.yaml` binding (path + version + hash) — **[F13 PENDING — held]**
- [ ] Adapter re-render across Claude/Kimi/OpenCode/Codex/Grok/Gemini — **[F13 PENDING — held]**
- [ ] A warga A-FORGE competency test — **[F13 PENDING — held]**
- [ ] Selection ledger schema with outcome + verification — **[F13 PENDING — held]**
- [ ] A-FORGE COMPETENCY block on every agent card — **[F13 PENDING — held]**
- [ ] Cleanup of duplicate FORGE-* skills per aforge skill audit — **[F13 PENDING — held]**

Additionally, before adoption this map needs its own regeneration hook: it is derived
substrate, so it must be re-derived from a fingerprinted source, never hand-edited. That
hook does not exist yet.

---

*Derived 2026-10-01 by lane 333b. 122/122 tools classified from evidence; 1 held
UNCLASSIFIED by design. Nothing here is canonical until Arif adopts it.*

DITEMPA BUKAN DIBERI — Forged, not given.
