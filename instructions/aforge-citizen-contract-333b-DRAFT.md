# A-FORGE CITIZEN CONTRACT — DRAFT 2026-10-01

> **Status:** DRAFT_INTERSECTION_REPORT (2026-10-01 · lane 333b) — observed path collision with FI-008's already-committed contract. This draft is NOT adopted; it documents the collision only. Production contract remains `/root/AAA/instructions/aforge-citizen-contract.md` (FI-008, commit 004b7e6b).
> **Author lane:** 333b
> **Supersedes:** nothing yet

> ## ⚠ PATH COLLISION — read first
>
> The mission assigned this draft to
> `/root/AAA/instructions/aforge-citizen-contract.md`. **That path is already occupied** by a
> different draft of the same contract, written by **FI-008 (kimi-code)** earlier on
> 2026-10-01, and already committed to git:
>
> - `004b7e6b` — forge: A-FORGE Citizen Contract (capability membrane, DRAFT_AWAITING_F13)
> - `b339b494` — forge: A-FORGE Competency Protocol v1 (projection + competency state + E1-E8 evals + 5-dim state)
>
> It is also already **bound in production config**: `ROOT_AGENT_CONFIG.yaml:20-24` sets
> `forge_citizenship_contract.path` to that exact file at `version: 0.1.0-draft`.
>
> Lane 333b is read-only on production code. Overwriting a committed, config-bound file
> owned by another agent would violate F1 AMANAH (rollback path) and the LAW-8
> revert-clobber scar (2026-09-28: `checkout HEAD` on a shared file forbidden — same class).
> **So this draft was written to a non-colliding sibling path instead, and the collision is
> handed to Arif as a binary.** Nothing was overwritten. See §12.

---

## 0. Core invariant

```
┌──────────────────────────────────────────────┐
│                                              │
│    AAA citizenship  ⇒  A-FORGE competency    │
│                                              │
│    (not merely: A-FORGE configured)          │
│                                              │
└──────────────────────────────────────────────┘
```

A citizen who has A-FORGE *configured* can call tools. A citizen who has A-FORGE
*competency* can find the right capability, stay inside authority, prove the result, and
learn from the outcome. Configuration is a fact about the machine. Competency is a fact
about the citizen. This contract governs the second.

---

## 1. Purpose

A-FORGE is the federation's governed execution and capability-forging plane.

A warga does not need to memorize A-FORGE's complete tool registry. The warga **MUST**
reason in capabilities:

```
INSPECT → PLAN → ACT → VERIFY → EXTEND → CONTROL → LEARN
```

For every executable task:

```
intent → capability → authority → implementation → evidence → verification → outcome
```

If any link in that chain is unknown, the task is **HOLD**, not a question to the human.

---

## 2. Routing

| Plane | Owns |
|---|---|
| **arifOS** | authority |
| **AAA** | attention, identity, coordination, routing |
| **A-FORGE** | physical execution, and acquisition of missing execution capability |

**Bypass rule.** An agent MUST NOT bypass A-FORGE with a direct external actuator when an
equivalent governed A-FORGE capability exists, unless the declared task explicitly requires
that direct surface. "The task required it" is a claim that needs evidence, not an
assertion that ends the question.

---

## 3. Boot

At session start:

1. `arif_init`
2. Confirm A-FORGE reachability
3. Read the current A-FORGE registry fingerprint / capability-map version
4. Reload the capability map **ONLY** when version/fingerprint changed
5. Do **NOT** inject the complete raw tool registry into working context unless required
   for diagnosis

Cold substrate by default. Hot only on demand.

---

## 4. Capability selection

Given a task, in this order:

1. Identify the required **semantic capability** first
2. Select the **narrowest** suitable A-FORGE implementation
3. Prefer **existing** capability over generating a new one
4. Prefer **reversible** over irreversible
5. Prefer **bounded execution** over unrestricted shell
6. Prefer **structured tools** over generic shell when both can complete the task

This is progressive disclosure, not tool deletion. The 122 schemas remain underneath.

---

## 5. Capability gap

If no existing capability matches:

```
inspect_gap → ephemeral forge → sandbox test → invoke → independently verify
```

An ephemeral capability **MUST NOT** become permanent merely because it worked once.
Promotion requires repeated verified utility. Unused or mission-specific capabilities
should expire or be retired.

Self-certification is inadmissible at the verify step. `forge_ephemeral` enforces this
directly: accepted verification methods are `known_answer | schema_invariant |
independent_recompute | domain_witness`, and `SELF_CERTIFIED` is rejected.

---

## 6. Completion

> **Tool success ≠ task success.**

Every consequential execution must produce evidence. Completion requires **independent**
comparison against task intent and acceptance criteria.

Record:

- selected capability
- alternatives considered
- execution result
- verification result
- cost
- repair loops
- final outcome

A green exit code is an observation about a process. It is not an observation about
whether the task was done.

---

## 7. Authority boundary

> **Capability ≠ authority.**

A-FORGE may execute only inside the authority granted by arifOS and the active
lease/session. A-FORGE never grants itself authority. An agent never treats its own
execution receipt as constitutional approval.

This is not a convention. It is observable in the registry: of the 122 A-FORGE tools, 11
delegate or transfer authority outward to arifOS or another organ (`forge_judge_proxy`,
`forge_check_governance`, `forge_heart_critique`, `forge_kernel`, `forge_session_init`,
`forge_lease`, `forge_tier_bind`, `forge_wealth`, `forge_well`, `forge_hf_import`,
`forge_predict`). `forge_lease` states it outright — *"A-FORGE does not self-issue leases
— arifOS mints them."* `forge_hf_import` states it outright — *"The gate validates — the
kernel seals."* `forge_tier_bind` can only set a trust tier **lower bound**; promotion is
arifOS's alone.

Evidence: `/root/AAA/federation/AFORGE_CAPABILITY_MAP_v1_DRAFT.md` §5.6.

---

## 8. Failure

If a required capability cannot be found, forged, authorized, or verified:

- **HOLD** the execution path
- Return **evidence** of the exact missing capability or authority boundary
- Do **not** convert implementation uncertainty into a human technical question when a
  reversible machine-resolution path remains available

HOLD is a completed action with a receipt, not a surrender of the task.

---

## 9. Core invariant (restated)

A competent warga must be able to:

1. identify the right capability
2. route through A-FORGE
3. stay within authority
4. verify reality
5. learn from the outcome

**Knowing tool names alone does not satisfy this contract.**

---

## 10. Hierarchy

```
AAA constitution / citizenship
  ↓
aforge-citizen-contract            ← always loaded (this file)
  ↓
capability map                     ← loaded on fingerprint change
  ↓
just-in-time exact tool discovery  ← loaded per task
  ↓
execution
  ↓
verification
  ↓
experience / scar                  ← persists
```

The contract is always loaded. The detailed A-FORGE knowledge is retrieved only when
necessary. **The 122 schemas remain cold substrate.**

Cold substrate, verified 2026-10-01: A-FORGE live `tools/list` on `:7072` returns exactly
**122** tools, matching `CAPABILITY_INDEX.json` with zero drift in either direction, and
`/health` reports `tool_count: 122`, `deployment_drift: false`. An agent that loaded all
122 schemas would be paying attention cost for tools it will never call this session.

---

## 11. Adoption gate (what this contract will require when Arif promotes it)

**This section is FORWARD-LOOKING and NOT YET ACTIVE.** When adopted, this contract will
require:

- [ ] `ROOT_AGENT_CONFIG.yaml` binding (path + version + hash) — **[F13 PENDING — held]**
- [ ] Adapter re-render across Claude/Kimi/OpenCode/Codex/Grok/Gemini — **[F13 PENDING — held]**
- [ ] A warga A-FORGE competency test — **[F13 PENDING — held]**
- [ ] Selection ledger schema with outcome + verification — **[F13 PENDING — held]**
- [ ] A-FORGE COMPETENCY block on every agent card — **[F13 PENDING — held]**
- [ ] Cleanup of duplicate FORGE-* skills per aforge skill audit — **[F13 PENDING — held]**

Note on the first item: `ROOT_AGENT_CONFIG.yaml:20-24` **already** binds
`forge_citizenship_contract.path` → `/root/AAA/instructions/aforge-citizen-contract.md` at
`version: 0.1.0-draft`, pointing at the FI-008 draft, not this one. That binding was made
without an F13 gate. See §12 Q1.

Note on the last item: the duplicate-skill condition it names is real and measured —
**25 case-duplicate skill directories** exist under `/root/.claude/skills/`, of which 22
are `FORGE-*`/`forge-*` pairs. Spot-checked pairs are byte-identical
(`forge-code-analysis`, `forge-infra-guardian`, `forge-onboarding` — matching sha256), so
these are duplicate registrations of one artifact, not divergent forks. Counted, not
fixed: cleanup is a mutation and outside this lane.

---

## 12. Collision with the FI-008 draft — F13 binaries for Arif

Two drafts of this contract now exist, written the same day by different lanes, and they
are **not interchangeable**. The substantive divergence:

| | FI-008 draft (committed, config-bound) | This 333b draft |
|---|---|---|
| Path | `/root/AAA/instructions/aforge-citizen-contract.md` | `/root/AAA/instructions/aforge-citizen-contract-333b-DRAFT.md` |
| Verb count | 7 | 7 |
| Verb names | `inspect, plan, change, run, verify, extend, control` | `INSPECT, PLAN, ACT, VERIFY, EXTEND, CONTROL, LEARN` |
| ACT | split into `change` + `run` | one class |
| **LEARN** | **absent** | present, 14 tools |
| Machine-readable schema | yes — `AFORGE_VERB_SCHEMA.json` + generator + projection + E1-E8 evals + competency state | no — prose only |

**Q1 — Which draft is canonical?** FI-008's is committed and already bound in
`ROOT_AGENT_CONFIG.yaml`, so it is the *de facto* contract today regardless of your intent.
Pick one, or direct a merge. Reversible either way; canonical-records class, so it is your
binary.

**Q2 — Does LEARN exist as a capability class?** This is the load-bearing question, and
FI-008's own artifacts contradict each other on it:

- `AFORGE_VERB_SCHEMA.json` has **7 verbs and none is LEARN** — its `L` dimension has no verb.
- `aforge-competency-schema.md` defines `K_AF = R × A × E × V × L` with
  `L = Learning competence (E7)`, and states *"If any dimension is zero → K_AF = 0."*
- `aforge-competency-evals.md` E7 tests `forge_experience_trace` explicitly.

So the eval suite scores a LEARN dimension that the verb schema never exposes. Worse, the
projection proves the consequence: in `/root/AAA/state/aforge/warga-capabilities.json`, of
the 10 LEARN-class tools, **9 are absent entirely** and `forge_wm_quality` was absorbed
into `forge_inspect`. Under FI-008's verb set, `L` can only ever be reached by accident.
`forge_plan`, `forge_change`, `forge_verify`, `forge_extend` all project **0 candidates**
while `forge_inspect` holds 26 — the LEARN tools fell through the gap and landed in the
catch-all.

My recommendation: **keep LEARN**, adopt the 333b class names, and have FI-008's machine
layer (which is good work and should be kept) re-project against them.

**Q3 — Was binding `ROOT_AGENT_CONFIG.yaml` to an unadopted draft correct?** The gate in
§11 says config binding happens *on adoption*. It already happened, at `0.1.0-draft`,
`status: DRAFT_AWAITING_F13`. A draft that is bound is a draft that adapters will render
into agent cards. Do you want the binding rolled back until adoption, or kept?

**Q4 — GOVERN class?** 19 of 122 tools are `aforge.governance.*` and neither 7-verb set has
a GOVERN class. This draft distributes them by function. See capability map §5.2 and §7 Q3.

---

*Neither draft is canonical. Both are DRAFT 2026-10-01. Arif's word is terminal.*

DITEMPA BUKAN DIBERI — Forged, not given.
