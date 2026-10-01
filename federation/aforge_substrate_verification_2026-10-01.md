# A-FORGE Substrate Verification — DRAFT 2026-10-01
# Lane: 555c
# Status: read-only receipt, independent witness
# Supersedes: nothing

## 1. Method

Independent READ-ONLY disk probe of the eight substrate components Arif named as
already-existing. For each component I captured absolute path, sha256, mtime, git
provenance, and a verbatim snippet (5–20 lines). No file was modified except this
receipt. No service was restarted. No production artifact was mutated.

Canonical-repo determination: `/root/AAA/federation/organs.yaml` (machine SOT) was
read first per ASI-drift-watch doctrine. It names `/root/A-FORGE` (HEAD `237a7999`,
branch `main`) and `/root/arifOS` as the canonical source_paths. Two sibling worktrees
(`/root/A-FORGE-browser-poc`, `/root/A-FORGE-wt-l11l09`) also carry `a_think/affordances.yaml`
but are non-canonical branches — their copies DRIFT (different sha256, see §10).

Repo state at probe time:
- A-FORGE: branch `main`, working tree CLEAN. NOTE — HEAD advanced DURING this probe
  (was `237a7999` at start, `1af2ef9a` "fix(mcp): stop names drifting from the live
  registry" at 19:28). A concurrent writer is active on A-FORGE main. None of the eight
  probed files changed content between my first and second hash pass (all sha256 stable).
- arifOS: branch `feat/truth-metabolism-no-data-is-not-all-clear` (NOT main), HEAD `297abcb0`.
  Runtime marker `/opt/a-forge/app/.git_commit` = `f4a0a336` (Sep 27) — see drift note §10.

Epistemic labels used throughout: OBS (I saw bytes on disk) / DER (derived by computation
from those bytes) / INT (interpretation) / SPEC (speculation, flagged as such).

---

## Component 1: A-FORGE a_think/affordances.yaml

VERDICT: VERIFIED-ON-DISK

Path: /root/A-FORGE/a_think/affordances.yaml
sha256: cbe99c455e7c9924540d8d79e79ed63bdbb28c2d922ca719413969d117de1190
mtime: 2026-09-30 15:16:26 +0800 | size: 77005 bytes | lines: 2305
git: last commit bc98843d (2026-09-30 15:13) "seal: in-flight execution/governance surface work"; tree clean.

Verbatim evidence (lines 1–11) — the self-warning Arif cited:

```
# AFFORDANCE SURFACE NOTE (2026-08-09)
# Live MCP :7072 reports ~48 stateless tools; this file is broader design surface.
# APA GWS cards (forge_calendar/drive/gmail/sheets) REMOVED 2026-09-04 RBG audit —
#   surface-swept 2026-08-17 (core.ts 21e8a608c) but cards + zero-traffic bridges lingered.
# forge_gemini card KEPT (live, core.ts:3099). Rollback: git revert this commit.
# Phantom audit: compare to live tools/list before claiming tool exists.
# DITEMPA BUKAN DIBERI — no fake alignment with unregistered tools.
_comment: A-FORGE Affordance Cards — federation align v2. Actuators not plugins. Deny via gate/lease/SEAL only.
tools:
- name: forge_abort
  purpose: ACTUATOR [execute/MUTATE] supervised by kernel 777_FORGE. ...
```

Verbatim evidence (lines 10–28) — one full card, showing every field Arif named:

```
- name: forge_abort
  purpose: ACTUATOR [execute/MUTATE] supervised by kernel 777_FORGE. Safe stop + rollback...
  affordance_class: execute
  capability_surface: aforge.execute.abort
  kernel_verb: 777_FORGE
  mutation_class: MUTATE
  reads:
  - plans
  - tools
  writes:
  - filesystem
  - external_state
  external_side_effect: true
  destructive: true
  reversible: false
  requires_human_approval: true
  min_mode: GOVERN
  risk_label: R5
```

Field checklist (Arif claimed: semantic surface, mutation class, reads/writes, reversibility, approval requirement, mode, risk):
  [x] semantic surface  → `capability_surface:` present on 132/132 cards (OBS, grep count)
  [x] mutation class    → `mutation_class:` present 132/132
  [x] reads/writes      → `reads:` 136 occurrences, `writes:` 133
  [x] reversibility     → `reversible:` 138 occurrences
  [x] approval req      → `requires_human_approval:` 134 occurrences
  [x] mode              → `min_mode:` 131 occurrences
  [x] risk              → `risk_label:` 131 occurrences
  Card count (DER): 132 affordance cards (`grep -c '^- name:'`).

Self-warning present? YES (OBS). Two independent self-warnings:
  - line 2: "this file is broader design surface" (vs live MCP :7072 ~48 stateless tools)
  - line 6: "Phantom audit: compare to live tools/list before claiming tool exists."
  This is exactly Arif's "live tools/list must win before claiming a capability exists."

Cross-checks:
  - Consumed in-repo by: src/domain/governance/aThinkGuard.ts, src/interfaces/mcp/serve.ts,
    surfaceAuditTools.ts, yamlGovernanceValidator.ts, policyTools.ts, prompts.ts (OBS).
  - mtime 2026-09-30 (1 day old) — NOT stale; agrees with its "live design surface" role.
  - The "~48 stateless tools" self-warning vs organs.yaml live_probe (mcp_stateless_tools: 52)
    and vs CAPABILITY_INDEX aforge count (122) — three different numbers. See §10 DRIFT.

Scar flags:
  - NONE on the file itself (clean tree, fresh mtime, fields complete).
  - COUNT-DRIFT: file self-describes "~48 stateless tools" (2026-08-09 note, not rotated),
    while the same repo's live surface and the federation index report 52 and 122. The
    self-warning number is stale even though the file is fresh. (OBS)

---

## Component 2: arifOS constitutional ABI (8 verbs)

VERDICT: VERIFIED-ON-DISK (doc + machine-readable registry + code all agree)

Canonical doc path: /root/arifOS/docs/KERNEL_CAPABILITY_ABI.md
sha256: cf1c7f6dd55c7fd61901514a0a84038d4811c684759eea8ca9862d58e1e802c8
mtime: 2026-09-15 22:53:57 +0800 | size: 1286 bytes | lines: 29
git: last commit eacf0ca0 (2026-09-15) "fix(abi): resync discovery artifacts from kernel ABI registry"

Verbatim evidence (lines 5–16) — the transport clause + all 8 verbs:

```
arifOS has eight stable semantic capabilities. MCP, REST, A2A, model providers, and UI hosts are adapters; none may redefine capability meaning or grant authority.

| Capability | Version | MCP binding | Action | Authority |
|---|---:|---|---|---|
| `session.bind` | 1.0.0 | `arif_init` | OBSERVE | ANONYMOUS |
| `reality.observe` | 1.0.0 | `arif_observe` | OBSERVE | OBSERVER |
| `cognition.think` | 1.0.0 | `arif_think` | PREPARE | OBSERVER |
| `intent.route` | 1.0.0 | `arif_route` | PREPARE | OBSERVER |
| `memory.govern` | 1.0.0 | `arif_memory` | MATERIAL | TRUSTED_AGENT |
| `authority.judge` | 1.0.0 | `arif_judge` | MATERIAL | TRUSTED_AGENT |
| `action.execute` | 1.0.0 | `arif_forge` | MATERIAL | EXECUTOR |
| `history.seal` | 1.0.0 | `arif_seal` | IRREVERSIBLE | SOVEREIGN |
```

Verbatim (line 29): "Model identity and transport identity are evidence, not authority."

Machine-readable registry (the SOT the doc is generated FROM):
Path: /root/arifOS/arifosmcp/abi/capability_registry.json
sha256: d694c0e08a67c77dcfd634dd3a0d0f26785b22140391e8b3c95044814a789b0a
mtime: 2026-08-28 | abi_version: "2026.07.24"
registry description (verbatim): "Transport- and model-neutral semantic contract. Provider bindings are replaceable implementations, not constitutional meaning."

All 8 capability_ids confirmed present in the JSON (DER, parsed): session.bind, reality.observe,
cognition.think, intent.route, memory.govern, authority.judge, action.execute, history.seal —
each with provider.tool = arif_init/observe/think/route/memory/judge/forge/seal respectively.

Verbatim first registry record (proves per-verb semantic_hash + governance binding):

```
{
  "capability_id": "session.bind",
  "version": "1.0.0",
  "semantic_hash": "sha256:2a947992f413a8c969df2383c230f665c374f761de7618f5cf8f7a0e4299a5a5",
  "action_class": "OBSERVE",
  "mutation": false,
  "authority_required": "ANONYMOUS",
  "constitutional_floors": ["F1","F2","F4","F11","F13"],
  "provider": {"type": "mcp", "tool": "arif_init"},
  "arifos_governance": {"is_reversible": true, "impact_radius": 0, "requires_888_hold": false, ...}
}
```

Code that enforces the registry:
Path: /root/arifOS/arifosmcp/abi/kernel_abi.py
sha256: 92e1cccc8a4acdcf329cc155414254d09017afd9662235e58619d02bb13790ec
Doc generator: /root/arifOS/scripts/sync_kernel_abi.py (sha256 54fcc934..., exists, executable).

8-verb checklist:
  [x] session.bind    [x] reality.observe  [x] cognition.think  [x] intent.route
  [x] memory.govern   [x] authority.judge  [x] action.execute   [x] history.seal
  [x] "transports/providers cannot redefine capability meaning or grant authority" clause (doc line 5)
  [x] equivalent clause in machine registry ("Provider bindings are replaceable implementations, not constitutional meaning")

Cross-checks:
  - Doc line 3 self-declares it is GENERATED from the four registries under arifosmcp/abi/ —
    and the generator script exists. Not a hand-maintained orphan. (OBS)
  - Three substrates agree (doc table == registry JSON == kernel_abi.py reads provider.tool). (DER)
  - arifOS is on a FEATURE BRANCH (feat/truth-metabolism-...), not main. The ABI files themselves
    are committed/clean, but the branch is not merged. Flag for Lane 333b comparison. (OBS)

Scar flags:
  - abi_version "2026.07.24" (registry) vs doc mtime 2026-09-15 vs registry mtime 2026-08-28 —
    three different dates for one "stable" ABI. Cosmetic (version string vs file mtimes), but the
    version label is ~2 months behind the doc. Not a defect; noted. (OBS)
  - arifOS branch != main. If Lane 333b reads arifOS main, it may not see this exact HEAD. (INT)

---

## Component 3: arif_route(intent=...) routing

VERDICT: VERIFIED-ON-DISK

Primary evidence path: /root/A-FORGE/src/interfaces/mcp/prompts.ts
sha256: beb6abb190a246b8599ae837b7215c03ad548c5f16b606a0b930f181f44f57c1
mtime: 2026-08-12 06:36:08 +0800 | size: 40124 bytes | lines: 924
git: last commit 53e82f0b (2026-07-31) "feat: P0 Restore-One-Reality ..."

Verbatim evidence (lines 302–305) — the exact instruction Arif cited:

```
ROUTE VIA arif_route (PRIMARY):
Call arifOS arif_route(intent="${s.query}") FIRST to determine the correct organ.
arif_route returns: {organ, port, tool_prefix, suggested_tools, confidence}.
Do NOT hardcode organ/port mappings — arif_route is source of truth.
```

The instruction is embedded in the `cross-organ-query` MCP prompt (serve registration at
prompts.ts:285–286: "Route a query to the correct federation organ via arif_route (canonical intent router)").
Note lines 307–313 provide an ORGAN MAP explicitly labeled "fallback if arif_route unavailable" —
the hardcoded ports exist ONLY as a documented fallback, subordinate to arif_route. (OBS)

Routing-truth origin (arifOS side — where arif_route is implemented):
- /root/arifOS/arifosmcp/mission_router.py (sha256 10d53dc6...) — module docstring: "This module
  is the bridge between human language and silent organ orchestration... classify_mission() →
  mission + confidence". (OBS)
- /root/arifOS/arifosmcp/capability_map.py (sha256 5a278da3...)
- arif_route registered as a public MCP tool in /root/arifOS/arifosmcp/server.py (multiple refs,
  incl. alias map arif_kernel_route→arif_route, arif_bridge→arif_route). (OBS)

Instruction checklist:
  [x] agents told to call arif_route(intent=...) FIRST  (prompts.ts:303)
  [x] explicit "Do NOT hardcode organ/port mappings"    (prompts.ts:305)
  [x] "routing truth belongs to arifOS"                  (prompts.ts:305 "arif_route is source of truth";
                                                          impl lives in arifOS, not A-FORGE)

Cross-checks:
  - A-FORGE okf/arifos.md (sha256 a032f650...) line 25 independently states arifOS "Routes —
    Directs intent to correct domain organ via arif_route". Consistent. (OBS)
  - The instruction lives in the LIVE MCP prompt surface (compiled into dist/, see §10), not just docs.

Scar flags:
  - Minor tension (INT): the same prompt block that says "Do NOT hardcode organ/port mappings"
    then prints a hardcoded ORGAN MAP with ports (:8088, :8081, :18082, :18083, :7072, :3001)
    as "fallback." Not a contradiction (fallback is explicitly subordinate), but the hardcoded
    ports are physically present and could drift from organs.yaml. Current values DO match organs.yaml. (OBS)

---

## Component 4: forge_skill_select_query

VERDICT: VERIFIED-ON-DISK

Implementation path: /root/A-FORGE/src/interfaces/mcp/experienceTraceTools.ts
sha256: dbba337fc7740980906081df08b28b002b2bdd3c5a8deb949a4e8fc5527a34eb
mtime: 2026-09-14 00:54:54 +0800 | size: 28223 bytes | lines: 704
git: last commit 1fb71597 (2026-09-14) "refactor(traces): add success_basis provenance to experience traces"

Verbatim evidence (lines 597–602) — tool definition + SkillGate Phase 1 label:

```
  // ── forge_skill_select_query ──
  server.tool(
    "forge_skill_select_query",
    "Query skill selection events (SkillGate preparation). Returns which skills were selected, " +
    "by what method (keyword/learned/manual/routed/fallback), and outcomes. Read-only. " +
    "Prepares for Phase 2 SkillGate credit separation (selection credit vs execution credit).",
```

Verbatim evidence (lines 693–698) — the Phase 1 label in the epistemic block:

```
            _epistemic: {
              evidence_layer: "OBS",
              confidence: 0.90,
              source: "forge_skill_select_query",
              note: "Skill selection tracking = SkillGate Phase 1 observation. Credit separation in Phase 2.",
            },
```

Purpose claim verified (DER): the tool exposes (a) which skills selected (`skill_name`), (b) by what
method (`selection_method`: keyword/learned/manual/routed/fallback), (c) outcomes (`outcome_success`,
`outcome_summary`) — exactly Arif's "which skills were selected, by what method, and their outcomes
as preparation for later credit separation." The credit-separation intent is literal in the docstring
("Prepares for Phase 2 SkillGate credit separation (selection credit vs execution credit)"). (OBS)

SkillGate Phase 1 label checklist:
  [x] "SkillGate Phase 1" — verbatim at experienceTraceTools.ts:697 AND serve.ts:319 comment
      ("skill selection events — read-only (SkillGate Phase 1)"). (OBS)

Consolidation-audit reference (Arif: "an audit even proposes consolidating the query tools into a
more general experience interface"):
Path: /root/A-FORGE/AFORGE_TOOL_AUDIT_2026-09-15.md
sha256: 550b9fadd585590856a0131bad3856683053c93a788087d53e90a8f2db409394
mtime: 2026-09-17 01:27:24 +0800

Verbatim quote (audit §2.5 "Experience (2+1 → 1)", lines 78–85):

```
#### 2.5 Experience (2+1 → 1)
| Tool | Purpose | Verdict |
|---|---|---|
| `forge_experience_trace` | Record experience trace | **MERGE** into `forge_experience(verb: record\|query\|skill_select)` |
| `forge_experience_query` | Query traces | **DELETE** |
| `forge_skill_select_query` | Query skill selection events | **DELETE** (same JSONL-read pattern) |

**Savings: −2** | Risk: LOW (all whitelisted OBSERVE, shared `loadTraces`/`recordExperienceTrace`)
```

Audit overall verdict (line 3): "CONSOLIDATION RECOMMENDED — 26 tools eliminable across 14 clusters".
The proposed general interface is literally `forge_experience(verb: record|query|skill_select)`. (OBS)

Cross-checks:
  - Affordance card exists: affordances.yaml:1862–1876 (capability_surface aforge.meta.skill_select,
    mutation_class OBSERVE, risk_label R0, min_mode THINK). Consistent with read-only tool. (OBS)
  - Registered on live MCP surface: serve.ts:319 (OBS) and present in federation CAPABILITY_INDEX
    as aforge tool `forge_skill_select_query` (DER, parsed index). (OBS)
  - The audit is dated 2026-09-15/17; the consolidation it proposes is NOT yet implemented (the tool
    still exists as a standalone `server.tool` registration at experienceTraceTools.ts:598). So the
    audit is a PROPOSAL, matching Arif's "an audit even proposes consolidating." (OBS)

Scar flags:
  - Implementation-status gap (OBS): Arif said implementation "is still described as SkillGate
    Phase 1" — TRUE. But note the tool currently returns `total_events: 0` with message "No skill
    selection events recorded yet" when SKILL_SELECTION_LOG is absent (experienceTraceTools.ts:610–625).
    The tracker log path is /root/.local/share/arifos/skill-selection/selections.jsonl. I did NOT
    confirm whether that log has real events (out of scope for this receipt, and reading it is a
    separate substrate). So "Phase 1 observation" surface exists; whether it has ever OBSERVED a real
    selection event is UNMEASURED here. Flag as open question §12.

---

## Component 5: forge_experience_trace

VERDICT: VERIFIED-ON-DISK

Path: /root/A-FORGE/src/interfaces/mcp/experienceTraceTools.ts (same file as Component 4)
sha256: dbba337fc7740980906081df08b28b002b2bdd3c5a8deb949a4e8fc5527a34eb

Verbatim evidence (lines 447–452) — the action→observation→feedback→delta flow + 3 channels:

```
  server.tool(
    "forge_experience_trace",
    "Record an experience trace (Chain-of-Experience). Captures action→observation→feedback→delta " +
    "after every non-trivial forge tool execution. Three feedback channels: self (model critique), " +
    "environmental (test/lint/build), constitutional (floor check). Append-only hash-chained ledger. " +
    "Returns the sealed trace with hash chain link.",
```

Verbatim evidence (lines 40–71) — the ExperienceTrace interface (the data model):

```
interface ExperienceTrace {
  trace_id: string; seq: number; ts: string; session_id: string; agent_id: string;
  action: { tool: string; input_hash: string; };
  observation: {
    output_hash: string;
    success: boolean;
    // Provenance of the `success` verdict. ABSENT on legacy records (< 2026-09-14).
    //   "execution_cleanliness" — derived from tool_metrics.error_count (Lane A)
    //   "self_reported"         — supplied by the acting agent, NOT verified (Lane B)
    // Never treat a bare `success: true` as evidence without reading this field.
    success_basis?: string;
    // true only when an independent verifier confirmed the outcome.
    success_verified?: boolean;
  };
  feedback: { self?: string; environmental?: string; constitutional?: string; };
  experience_delta: {
    capability_change?: number; confidence_change?: number;
    new_scar?: string | null; new_skill?: string | null;
  };
  prev_hash: string; hash: string;
}
```

Verbatim evidence (lines 229–251) — the self_reported / success_verified=false marking Arif cited:

```
      observation: {
        output_hash: outputHash,
        // 2026-09-14 · F13 session — Lane B provenance.
        // `success` here is supplied BY THE CALLING AGENT (params.success) and is
        // NOT derived from any measurement, and NOT verified by a third party.
        // Recorded as such so a self-report cannot be mistaken for evidence.
        // Contrast Lane A (session-trace.py) which derives success from
        // tool_metrics.error_count and records "execution_cleanliness".
        success: params.success,
        success_basis: "self_reported",
        success_verified: false,
      },
      feedback: {
        self: params.feedback_self,
        environmental: params.feedback_environmental,
        constitutional: params.feedback_constitutional,
      },
      experience_delta: {
        capability_change: params.capability_change,
        confidence_change: params.confidence_change,
        new_scar: params.new_scar ?? null,
        new_skill: params.new_skill ?? null,
      },
```

Field checklist (Arif's claim):
  [x] action → observation → feedback → delta flow  (interface + docstring)
  [x] three feedback channels: self, environmental, constitutional  (lines 61–64, 241–245, 460–462)
  [x] stores capability/confidence change  (experience_delta.capability_change / confidence_change)
  [x] stores new scars and new skills      (experience_delta.new_scar / new_skill)
  [x] distinguishes success from success_verified  (lines 57–59)
  [x] marks agent-provided success as success_basis="self_reported", success_verified=false (lines 238–239)

Cross-checks:
  - Affordance card: affordances.yaml:1828–1844 (capability_surface aforge.meta.experience_trace,
    writes experience_traces, min_mode FAST, risk_label R1). Consistent. (OBS)
  - Live registration: serve.ts:317. Present in federation CAPABILITY_INDEX as aforge tool. (OBS)
  - Append-only hash-chained ledger: chain state (prev_hash/hash, tracePrevHash, initTraceChain)
    at experienceTraceTools.ts:72–114. Real hash-chaining, not just a claim. (OBS)
  - The success_basis field was added 2026-09-14 (git commit 1fb71597 message matches). mtime agrees. (OBS)

Scar flags:
  - NONE material. This is the STRONGEST-verified component: the self_reported/success_verified=false
    honesty guard is exactly as Arif described, and it is the federation's own F2-TRUTH discipline
    encoded in a tool. It explicitly refuses to let a self-report masquerade as evidence. (INT)
  - Minor: `success_basis` is optional (`?`) and "ABSENT on legacy records (< 2026-09-14)". Any
    consumer reading old traces must handle the absent case. Documented in-code. Not a defect. (OBS)

---

## Component 6: EphemeralGenesisRunner

VERDICT: VERIFIED-ON-DISK (with a naming nuance — see below)

NAMING NUANCE (OBS, important for Lane 333b reconciliation): Arif named "EphemeralGenesisRunner."
Two files carry that exact name:
  - /root/A-FORGE/src/domain/forge/EphemeralGenesisRunner.ts (551 lines, sha256 not primary — adapter)
  - /root/A-FORGE/src/domain/containment/EphemeralGenesisRunner.ts (770 lines, mtime 2026-09-25 — adapter)
BUT both are documented as thin lease/governance WRAPPERS. The file that self-declares CANONICAL is:

Canonical engine path: /root/A-FORGE/src/infrastructure/tools/EphemeralGenesis.ts
sha256: cf5fe9327b1428c91fa3dbe7a1aba705256e4f616f25b21f54fb8242e9193193
mtime: 2026-08-12 06:36:08 +0800 | size: 69366 bytes | lines: 1566
git: last commit 5f49cf4f (2026-08-10) "fix(containment): dynamic container backend resolution..."

Verbatim evidence (lines 1–12) — the "single canonical engine" declaration:

```
 * EphemeralGenesis Engine — CANONICAL Capability Metabolism for A-FORGE
 *
 * ═══ P0.2 RATIFIED (2026-07-31) — SINGLE CANONICAL ENGINE ═══════════════
 * THIS is the authoritative ephemeral tool engine. ALL paths — MCP surface,
 * domain/forge adapter, domain/containment adapter — ultimately route here.
 * One engine. One state machine. One registry. One singleton.
 *
 * Domain adapters (domain/forge/EphemeralGenesisRunner.ts,
 * domain/containment/EphemeralGenesisRunner.ts) provide lease + governance
 * wrappers but MUST NOT duplicate core lifecycle logic.
```

MCP surface path: /root/A-FORGE/src/interfaces/mcp/ephemeralTools.ts
sha256: 09fd17d2907fd427d38607dfa5aab6274fbcb384f51e89f2131f27ecd1cd2539
mtime: 2026-08-12 06:36:08 +0800 | size: 24197 bytes
git: last commit dd37162b (2026-08-02) "fix(ephemeral): P1-AA — unblock promotion gate..."

Verbatim evidence (ephemeralTools.ts lines 6–12) — sandbox_test/invoke/verify surface:

```
 * Modes:
 *   inspect_gap        — Detect what capability is missing
 *   generate           — Create ephemeral tool from template
 *   sandbox_test       — Verify the generated tool works
 *   invoke             — Execute the ephemeral tool
 *   verify             — Validate the result (independent verifier, NOT self-cert)
 *   retire             — Clean up + propose promotion if warranted
```

Verbatim evidence (ephemeralTools.ts lines 26–29) — the independent-verifier rule:

```
 * EVIDENCE RULES (P0.3 — fail-closed):
 *   - `verify` REJECTS verifier_method="SELF_CERTIFIED" as inadmissible.
 *   - Only these verifier methods are accepted: known_answer, schema_invariant,
 *     independent_recompute, domain_witness.
```

Verbatim evidence (EphemeralGenesis.ts lines 964–978) — enforcement in code, not just docs:

```
    if ((verifierMethod as string) === SELF_CERTIFIED) {
      return {
        ok: false, tool,
        error: "P0.3: SELF_CERTIFIED is inadmissible; tools cannot self-certify.",
      };
    }
    const wasInvoked = tool.state === "invoked" || tool.state === "tested";
    if (!wasInvoked) {
      return {
        ok: false, tool,
        error: "Tool not in invocable state — invoke first, then verify with independent verifier",
      };
    }
```

Retirement / TTL logic (Verbatim EphemeralGenesis.ts lines 1164–1173):

```
  cleanupExpired(): number {
    const now = new Date().toISOString();
    let cleaned = 0;
    for (const [id, tool] of this.store["tools"]) {
      if (tool.expiresAt <= now && tool.state !== "retired") {
        tool.state = "retired";
        cleaned++;
      }
    }
    return cleaned;
  }
```

TTL is set at generation (line 446): `const expiresAt = new Date(Date.now() + 3600_000).toISOString(); // 1 hour TTL`.
Permanent-vs-ephemeral governance (lines 26–32): "Same template instantiated N+ times →
propose_promotion → human gate → permanent"; "@constitutional F13 SOVEREIGN — promotion to
permanent requires human gate." So permanent registry changes remain governed while ephemeral
artifacts auto-expire. (OBS)

Checklist:
  [x] governed EphemeralGenesisRunner exists (canonical engine + 2 named adapters)
  [x] MCP surface defines sandbox_test, invoke, verify (ephemeralTools.ts:6–12, 9 modes total)
  [x] "verification must use independent verifier, not self-certification" (ephemeralTools.ts:11,26–29;
      EphemeralGenesis.ts:964–978 ENFORCES it; VerifierRegistry.ts hard-fails SELF_CERTIFIED at :342–345)
  [PARTIAL] "autonomous retirement logic where ephemeral artifacts expire based on TTL/scar pressure"
      → TTL expiry: VERIFIED (cleanupExpired, expiresAt, 1h TTL).
      → scar pressure as a retirement DRIVER of the ephemeral engine: NOT FOUND inside EphemeralGenesis.ts.
        Scar-pressure-driven rollback/retirement lives in ADJACENT subsystems:
          * /root/A-FORGE/src/domain/forge/canary.ts:30,130–131 — CANARY_SCAR_BUDGET=0.05,
            auto-rollback reason "scar_pressure" (sha256 5684527d...)
          * /root/A-FORGE/src/domain/forge/register.ts:137–139 — "Scar pressure ≥ 0.7 ... registration blocked"
            (sha256 a6dc729a...)
        So scar-pressure retirement is REAL in the federation but is enforced at the canary/registration
        layer, NOT inside the ephemeral engine's own retire path. (OBS + DER)

Cross-checks:
  - Independent verifier registry: /root/A-FORGE/src/domain/governance/verifier/VerifierRegistry.ts
    (sha256 de188e6d...) — "Independent verification for ephemeral capabilities... The engine refuses
    SELF_CERTIFIED. Promotion rejects receipts whose [method is not] domain_witness or independent_recompute." (OBS)
  - Live registration: serve.ts:276 "forge_ephemeral" with comment "generate, sandbox_test, invoke,
    verify, retire are session-gated in handler." Present in CAPABILITY_INDEX as aforge tool. (OBS)
  - Test coverage exists: test/EphemeralGenesisRunner.test.ts, test/ephemeralForgeRunnerDelegation.test.ts. (OBS)

Scar flags:
  - PARTIAL on scar-pressure-as-ephemeral-retirement-driver (see checklist). Arif conflated two real
    mechanisms: TTL expiry (in the engine) and scar-pressure rollback (in canary/register). Both exist;
    they are not co-located. This is a DRIFT between the self-description and the code topology. (INT)
  - Name drift: "EphemeralGenesisRunner" is the ADAPTER name; the CANONICAL engine is "EphemeralGenesis.ts".
    Arif's claim maps to the canonical engine's behavior. Not a defect, but Lane 333b may hash a different
    file if it greps only for "EphemeralGenesisRunner.ts". (INT)

---

## Component 7: "One graph, not several registries drifting apart"

VERDICT: VERIFIED-ON-DISK (as a specification) + code-realized (as capability_graph.py)

Spec path: /root/arifOS/docs/architecture/CAPABILITY_GRAPH_v1.md
sha256: d28361934746ef4942d685fda4cb59d61ad54e5e24095d622f17c1eeecea6cde
mtime: 2026-07-17 15:55:59 +0800 | size: 13400 bytes | lines: 377
git: last commit 2550d4e4 (2026-06-24) "docs(architecture): scope-bound CAPABILITY_GRAPH_v1 + self-audit report"

Verbatim evidence (lines 14–23) — kernel owns the graph:

```
## 1. Purpose
The arifOS kernel is the governed substrate. MCP is the syscall membrane. The **Capability Graph** is the single source of truth that connects them:
- The kernel owns the graph.
- Every MCP tool must be a node in the graph.
- If a tool is not in the graph, no MCP server may expose it.
- If a session lacks authority for a node, the kernel returns `KERNEL_DENY`.
```

Verbatim evidence (lines 45–51) — the "one graph" principle (Arif's literal quote) + organs propose + denial as data:

```
## 2. Design Principles
1. **One graph to rule them all.** No more `CANONICAL_TOOLS`, `tool_registry.json`, `public_tool_specs`, `mcp_surface_registry.yaml`, and `capability_map.py` drifting apart.
2. **Kernel-owned, organs-register.** GEOX/WEALTH/WELL/A-FORGE propose their tools; the kernel approves and publishes the graph.
3. **INIT-first.** A session token derived from `arif_init` is required before any non-observe tool.
4. **Self-correction-before-irreversible.** ...
5. **Denial is data.** `KERNEL_DENY` returns a structured envelope with reason, missing gate, and next safe action.
```

All four of Arif's sub-claims map verbatim:
  [x] "kernel owns the capability graph"        → line 18 "The kernel owns the graph."
  [x] "organs propose capabilities"             → line 48 "GEOX/WEALTH/WELL/A-FORGE propose their tools"
  [x] "kernel controls invocation by authority" → lines 21, 224–225 (authority ceiling → KERNEL_DENY)
  [x] "denial = structured data not opaque fail"→ line 51 "Denial is data... structured envelope with reason, missing gate, and next safe action"
  [x] most-important principle "one graph, rather than several registries drifting apart"
      → line 47, Design Principle #1, VERBATIM ("One graph to rule them all. No more [5 named registries] drifting apart.")

Code realization (the spec is not paper-only):
Path: /root/arifOS/arifosmcp/schemas/capability_graph.py
sha256: 19e62e5ed04f90840932e603dbaf8a183147044461619f92a9d0ee16ff551d3a
Header (verbatim, lines 1–8): "Canonical capability resolution — replaces 38 routing modules.
Planner decides WHAT. CapabilityGraph decides WHICH. Governor decides MAY. Executor does the exact
approved action. Forged: 2026-07-26 under Arif's P2 directive." (OBS)

Cross-checks:
  - Self-audit exists: /root/arifOS/docs/audits/CAPABILITY_GRAPH_v1_AUDIT.md (sha256 f173feae..., 9623 bytes).
  - The doc's frontmatter (line 10) says "epistemic_status: PROPOSAL → RATIFIED (F13 sovereign directive)"
    — so it claims ratified status.

Scar flags:
  - STALE / EXPIRED (OBS, material): the doc's OWN SOT-MANIFEST frontmatter declares
    `valid_from: 2026-06-24` and `valid_until: 2026-07-24`. As of today (2026-10-01) that validity
    window EXPIRED 69 days ago. No rotation/re-validation is stamped in the file. The principle survives
    (and is code-realized in capability_graph.py, forged 2026-07-26 = AFTER the doc's valid_until), but
    the SPEC document is past its self-declared expiry. This is the clearest stale-artifact scar in the set.
  - BROKEN CROSS-LINK (OBS): line 33 cites "See audit: /root/forge_work/CAPABILITY_GRAPH_v1_AUDIT.md".
    That path does NOT exist (`test -e` = MISSING). The audit actually lives at
    /root/arifOS/docs/audits/CAPABILITY_GRAPH_v1_AUDIT.md. The doc points at a phantom path. (Tier-0 class.)
  - Spec-vs-code drift (INT): doc mtime 2026-07-17, code (capability_graph.py) forged 2026-07-26 and
    claims to "replace 38 routing modules." The code has likely advanced past the v1 spec. The spec is
    labeled "v1"; no v2 spec file exists in docs/architecture/ (only CAPABILITY_GRAPH_v1.md). (OBS)

---

## Component 8: 122/343 capability index

VERDICT: VERIFIED-ON-DISK

Index path: /root/AAA/registries/CAPABILITY_INDEX.json
sha256: 5ca6c2c00dd40505858c900cd4bf67b9305671122210d8c3a3a0b30f5131c42b
mtime: 2026-09-29 23:07:52 +0800 | size: 214563 bytes
forgedAt (in-file): 2026-09-29T15:07:52+00:00  (= 2026-09-29 23:07 +0800; capture is 2 days old)
digest (in-file): 16e78b27fbe030f7801d2b109cf5cf4cca7195ef07227c28bb80779b4e81a1b6

Counts (DER — parsed the JSON tools[] array and counted by `server`):
  total_tools (in-file field): 343   ← matches Arif's "343 federation tools"
  aforge share:                122   ← matches Arif's "122 of the federation's 343"
  tools[] array length:        343   ← internally consistent with total_tools field

Full per-server breakdown (DER, sums to 343):
  aforge: 122 | well: 48 | wealth: 41 | geox: 33 | github: 26 | arifos: 24 |
  chron: 19 | memory: 9 | fed: 7 | brave-search: 6 | duckdb: 3 | context7: 2 |
  minimax: 2 | postgres: 1

Checklist:
  [x] Path of index: /root/AAA/registries/CAPABILITY_INDEX.json
  [x] sha256: 5ca6c2c0...
  [x] Total federation tool count: 343 (both `total_tools` field AND len(tools[]) agree)
  [x] A-FORGE share count: 122 (parsed count of tools[] where server=="aforge")
  [x] Date of capture: forgedAt 2026-09-29T15:07:52Z (mtime 2026-09-29 23:07 +0800)

Cross-checks:
  - Independent corroboration of the "122" number: /root/AAA/federation/organs.yaml:125 comment
    (2026-09-29 FI-003 audit) states "forge_surface_audit reports ... absent from the live registry
    (122 tools)". Two independent AAA artifacts (organs.yaml comment + CAPABILITY_INDEX) both say 122. (OBS)
  - All four experience/ephemeral tools from Components 4/5/6 ARE present among the 122 aforge entries
    (DER, parsed tool_name list): forge_ephemeral, forge_experience_trace, forge_experience_query,
    forge_skill_select_query, forge_skill, forge_skillstore_read, forge_skillstore_write. (OBS)
    → Components 4, 5, 6 are corroborated by the index in Component 8. Cross-component consistency.
  - Capture is 2 days old — FRESH, not stale. mtime agrees with forgedAt. (OBS)

Scar flags:
  - Index freshness is good (2 days), BUT it is a SNAPSHOT. The A-FORGE repo HEAD advanced during this
    very probe (237a7999→1af2ef9a). The 122 count is a 2026-09-29 snapshot of a live-moving surface;
    affordances.yaml (132 cards) and the index (122 aforge tools) legitimately differ because affordances
    is design surface and the index is live registry — this is the file's OWN stated distinction, not drift. (INT)

---

## 10. Cross-component consistency matrix

| # | Component | Verdict | Path (canonical) | sha256 (first 12) | Fresh? | Cross-linked? |
|---|-----------|---------|------------------|-------------------|--------|---------------|
| 1 | affordances.yaml | VERIFIED | /root/A-FORGE/a_think/affordances.yaml | cbe99c455e7c | YES (1d) | 6 in-repo consumers |
| 2 | constitutional ABI (8 verbs) | VERIFIED | /root/arifOS/docs/KERNEL_CAPABILITY_ABI.md + abi/capability_registry.json | cf1c7f6dd55c / d694c0e08a67 | YES (doc 16d, reg 34d) | generated by sync_kernel_abi.py |
| 3 | arif_route no-hardcode | VERIFIED | /root/A-FORGE/src/interfaces/mcp/prompts.ts:305 | beb6abb190a2 | mid (50d) | impl in arifOS mission_router.py |
| 4 | forge_skill_select_query | VERIFIED | /root/A-FORGE/src/interfaces/mcp/experienceTraceTools.ts:597 | dbba337fc774 | YES (17d) | audit + affordance card + index |
| 5 | forge_experience_trace | VERIFIED | /root/A-FORGE/src/interfaces/mcp/experienceTraceTools.ts:447 | dbba337fc774 | YES (17d) | affordance card + index + serve.ts |
| 6 | EphemeralGenesisRunner | VERIFIED (PARTIAL scar-pressure) | /root/A-FORGE/src/infrastructure/tools/EphemeralGenesis.ts (canonical) | cf5fe9327b14 | mid (50d) | VerifierRegistry + canary/register + index |
| 7 | "one graph" principle | VERIFIED (spec EXPIRED) | /root/arifOS/docs/architecture/CAPABILITY_GRAPH_v1.md | d2836193474 | NO (expired 69d) | code: capability_graph.py; audit link BROKEN |
| 8 | 122/343 index | VERIFIED | /root/AAA/registries/CAPABILITY_INDEX.json | 5ca6c2c00dd4 | YES (2d) | organs.yaml:125 corroborates 122 |

Overall: 8/8 VERIFIED-ON-DISK. Component 6 carries a PARTIAL sub-claim (scar-pressure retirement is
real but co-located in canary/register, not the ephemeral engine). Component 7 is verified as a
principle but the spec DOCUMENT is past its self-declared valid_until and has one broken cross-link.

Internal corroboration loop (strongest finding): Components 4, 5, 6 tools all appear inside Component 8's
122 aforge entries. Component 8's "122" is independently echoed in organs.yaml:125. This is genuine
two-substrate agreement WITHIN the federation, not just self-description. (DER)

DRIFT — affordances.yaml sibling worktrees (OBS):
  Expected (canonical /root/A-FORGE, main):   sha256 cbe99c455e7c9924540d8d79e79ed63bdbb28c2d922ca719413969d117de1190
  Observed /root/A-FORGE-browser-poc (split/browser-mcp-server): 9a2853d69c3f... (DIFFERENT)
  Observed /root/A-FORGE-wt-l11l09 (feat/l11-l09-envelope-actor): 687618ac0ccb... (DIFFERENT)
  Severity: LOW for this mission (organs.yaml names /root/A-FORGE canonical, and that is what I verified).
  But three divergent copies of "the" affordances.yaml exist on the same host. Any agent that greps
  /root broadly will hit a non-canonical copy. Consistent with the federation's known three-graph /
  fork-divergence scars.

DRIFT — A-FORGE runtime marker vs source HEAD (OBS):
  Expected: /opt/a-forge/app/.git_commit tracks source HEAD.
  Observed: runtime marker = f4a0a336 (Sep 27 18:36); source HEAD = 1af2ef9a (Oct 1 19:28).
  Severity: MEDIUM-adjacent BUT mitigated — the systemd unit runs from /root/A-FORGE/dist (compiled),
  WorkingDirectory=/root/A-FORGE, and dist/src/interfaces/mcp/experienceTraceTools.js was rebuilt
  Oct 1 19:19 and DOES contain "success_basis" (grep count 1) and serve.js contains
  "forge_skill_select_query" (grep count 1). So the LIVE compiled runtime reflects the verified source
  even though the .git_commit marker file is 4 days stale. The marker is stale; the runtime is not.
  This is the exact "runtime marker ≠ deployed truth" class from the 2026-09-30 forgel-init scar.

DRIFT — arifOS on feature branch (OBS):
  /root/arifOS is on branch feat/truth-metabolism-no-data-is-not-all-clear (HEAD 297abcb0), NOT main.
  Components 2 and 7 were verified against this branch. If Lane 333b verifies against arifOS main, the
  ABI/graph files may differ or the branch may not be merged. Severity: LOW (files are committed & clean
  on this branch) but a reconciliation point for the two-lane comparison.

COUNT-DRIFT — three numbers for "A-FORGE live tools" (OBS):
  - affordances.yaml self-note (2026-08-09, not rotated): "~48 stateless tools"
  - organs.yaml live_probe_2026_07_30: mcp_stateless_tools: 52, api_tools: 124
  - CAPABILITY_INDEX.json (2026-09-29): aforge = 122
  These measure different things (stateless-MCP vs API vs indexed-registry) at different dates, so they
  are not strictly contradictory — but no single artifact reconciles them, which is precisely the
  "several registries drifting apart" condition Component 7's "one graph" principle exists to end. (INT)

---

## 11. Disagreements with Lane 333b (forward-looking note)

I have NOT seen Lane 333b's receipt (it comes after mine). Points where an independent lane is most
likely to diverge from mine, pre-flagged so a disagreement is diagnosable rather than alarming:

1. Component 6 file choice. If 333b greps literally for "EphemeralGenesisRunner.ts" it will hash one of
   the two ADAPTER files (domain/forge 551 lines, or domain/containment 770 lines) and may report a
   different sha256 than my canonical EphemeralGenesis.ts. Reconcile by: the adapters self-declare they
   "MUST NOT duplicate core lifecycle logic" and route to the canonical engine. Both are "correct"; the
   canonical one is EphemeralGenesis.ts.

2. Component 6 scar-pressure sub-claim. I stamped PARTIAL (TTL verified in-engine; scar-pressure rollback
   lives in canary.ts/register.ts, not the engine). If 333b stamps full VERIFIED, the disagreement is about
   WHERE scar-pressure retirement lives, not WHETHER it exists. It exists.

3. Component 7 expiry. I flagged the spec's valid_until: 2026-07-24 as EXPIRED (69 days). If 333b stamps
   clean VERIFIED without the expiry note, the substance agrees (principle present, code-realized) but my
   receipt adds the staleness scar. Not a factual conflict.

4. arifOS branch. I read arifOS on feat/truth-metabolism-... (297abcb0). If 333b read arifOS main, sha256
   for Components 2/7 files could differ if the branch diverged from main on those paths. Reconcile by
   comparing `git rev-parse HEAD` each lane saw.

5. A-FORGE HEAD moved mid-probe (237a7999 → 1af2ef9a at 19:28). If 333b probed before/after, its A-FORGE
   HEAD SHA may differ from mine. My eight file hashes were STABLE across both my passes (re-hashed after
   the HEAD move; identical), so content verdicts are unaffected.

If both receipts land on 8/8 VERIFIED with the same caveats above, the federation has two-scar evidence
that the substrate for the new design is present on disk.

---

## 12. Open questions for Arif

(These are observation-completeness questions, NOT implementation/HOW questions — framed to respect the
attention membrane. None require a technical decision from Arif; they are routed to the organs/musyawarah.)

1. Component 7 spec expiry: CAPABILITY_GRAPH_v1.md declares valid_until 2026-07-24 (expired 69 days) and
   cites a phantom audit path (/root/forge_work/CAPABILITY_GRAPH_v1_AUDIT.md, which does not exist). Is the
   "one graph" principle to be treated as still-ratified doctrine (the code capability_graph.py postdates
   the expiry), or does the spec need a v2 re-stamp? → route to 333 ARCHITECT / 888, not a HOW question for Arif.

2. Component 6 scar-pressure location: the ephemeral engine retires by TTL; scar-pressure retirement lives
   in canary.ts/register.ts. Is that separation the intended design (TTL for ephemeral, scar-budget for
   canary/registration), or should the ephemeral retire path also read scar pressure? → musyawarah item.

3. Component 4 tracker liveness: forge_skill_select_query reads
   /root/.local/share/arifos/skill-selection/selections.jsonl. I did NOT open that log (out of scope). Whether
   SkillGate Phase 1 has ever recorded a real selection event is UNMEASURED in this receipt. If the federation
   wants Phase 1 to be "live" vs "surface-only," that log needs a direct probe. → 555 telemetry follow-up.

4. Count reconciliation: three artifacts give ~48 / 52 / 122 for "A-FORGE live tools." Which single number is
   canonical for external claims? (This is the "one graph" principle's exact target.) → 333 / registry owner.

5. arifOS branch state: arifOS is on a feature branch, not main. Is the ABI/capability-graph work on that
   branch intended to be the ratified substrate, or is main the reference? Relevant to whether Components 2/7
   are "shipped" vs "in-flight." → not a HOW question; a canonical-record/direction flag = F13-class awareness.

---

## Hand-back attestations

- NO production artifact was mutated. The ONLY file written by this lane is this receipt:
  /root/AAA/federation/aforge_substrate_verification_2026-10-01.md
- No service restarted. No config, no CLAUDE.md, no source, no registry touched.
- Tools used: Read, Bash (find/grep/sha256sum/stat/wc/git-log/git-status/python3-json-parse), no Edit/Write
  to any target file. git status confirmed A-FORGE tree clean before and after.
- All 8 component hashes were re-verified after the mid-probe A-FORGE HEAD advance; all stable.

SUMMARY: 8/8 VERIFIED-ON-DISK. Federation substrate for the new design IS present on disk. Two components
carry honest caveats rather than clean passes: Component 6 (scar-pressure retirement is real but co-located
in canary/register, not the ephemeral engine → PARTIAL sub-claim) and Component 7 (the "one graph" principle
is verified and code-realized, but the spec document is past its self-declared valid_until by 69 days and
cites one phantom audit path). No component was CLAIMED-BUT-NOT-FOUND.

---

## ADDENDUM — 2026-10-01 19:41 — attestation correction (F2 TRUTH)

My §Hand-back attestation originally stated "git status confirmed A-FORGE tree clean before and after."
On a final re-check that statement is NO LONGER ACCURATE and I correct it here rather than leave a
misleading seal.

OBSERVED (OBS): `git -C /root/A-FORGE status --porcelain` now reports ONE modified file:
`M src/interfaces/mcp/policyTools.ts` (mtime 2026-10-01 19:40:35, +43/−22 lines). The diff is tagged
in-code "S1 (F13 SAH 2026-10-01)" and rewrites `isExternalClient()` to require a VERIFIED credential
instead of an asserted session_id/lease_id string — a session-gate trust fix.

ATTRIBUTION (DER, high confidence): this modification is NOT from Lane 555c.
  - I used Edit/Write on ZERO A-FORGE files. My only writes to A-FORGE paths were `grep` reads.
  - The change landed at 19:40:35, the same minute I wrote my receipt, and is signed by a different
    actor/lane ("S1 F13 SAH"). A concurrent writer is active on /root/A-FORGE main (corroborated by the
    HEAD advance 237a7999→1af2ef9a I already logged in §10).
  - policyTools.ts is NOT one of my eight verified components. It appears in my receipt only once, as a
    listed consumer of affordances.yaml in Component 1's cross-check — I never hashed or verified it.

VERIFIED-FILE INTEGRITY (OBS): all eight component files remain CLEAN and hash-STABLE across this event:
  - affordances.yaml            cbe99c455e7c... (unchanged)
  - experienceTraceTools.ts     dbba337fc774... (unchanged)
  - EphemeralGenesis.ts         cf5fe9327b14... (unchanged)
  - (and KERNEL_CAPABILITY_ABI.md, capability_registry.json, prompts.ts, ephemeralTools.ts,
     AFORGE_TOOL_AUDIT_2026-09-15.md, CAPABILITY_GRAPH_v1.md, CAPABILITY_INDEX.json — none dirty.)
  `git status --porcelain` on all eight paths returns EMPTY.

CORRECTED ATTESTATION: No production artifact was mutated BY THIS LANE. The only file written by 555c is
this receipt. A concurrent, separately-signed writer (S1/F13 SAH) modified an UNRELATED A-FORGE file
(policyTools.ts) during my probe window; that change is not mine, does not touch any verified component,
and is flagged here for the operator and for Lane 333b reconciliation. My verdicts (8/8 VERIFIED-ON-DISK)
are unaffected — the eight files they rest on are byte-identical before and after the event.

Receipt sha256 (post-addendum): see hand-back; recompute after this append.
