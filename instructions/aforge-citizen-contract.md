# A-FORGE Citizen Contract

> **Status:** DRAFT_AWAITING_F13 (2026-10-01 · written by FI-008)
> **Binding target:** every warga-aaa citizen + forge-instrument in this federation
> **Sister:** `/root/AAA/instructions/human-attention-membrane.md` · `/root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md`
> **Router:** every AGENTS.md / adapter renderer should inject this file on session boot.

---

## What this contract is

A-FORGE is the federation's governed execution + capability-forging plane.
This contract is the **inherited citizenship competency** that every warga must satisfy —
not a tool-manual, not a per-model prompt.

A warga does not memorise A-FORGE's complete tool registry.
A warga reasons in **capabilities**, then delegates tool selection to the router.

```
## 4 invariant (proposed, awaiting F13 ratification)

AAA citizenship  ⇒
A-FORGE competency

(not merely: A-FORGE configured)
```

---

## The 7 capability classes (verb names proposed)

| Verb | Intent | A-FORGE resolves to |
|---|---|---|
| `forge_inspect` | Understand repo/world/state | search · filesystem · browser · repo · code intel · worktree |
| `forge_plan` | Structure work | compile task · dependencies · budgets · leases |
| `forge_change` | Produce bounded changes | patch · shell · Git · browser · deployment |
| `forge_run` | Execute/build/test | shell · sandbox · Docker · job |
| `forge_verify` | Prove outcome | tests · evidence · witness · task verifier |
| `forge_extend` | Acquire missing capability | ephemeral forge · backend acquisition |
| `forge_control` | Status, rollback, abort | status · abort · rollback · retry · lock |

These are **attention-membrane verbs**, not god-functions.
Internally each one dispatches to a tree of typed low-level tools.
Agents receive only the verb schema; the registry of 122 tools stays cold substrate.

---

## For every executable task

A warga MUST traverse:

```
intent
  → capability
  → authority
  → implementation
  → evidence
  → verification
  → outcome
```

If any of these are unknown, the task is **HOLD**, not asked.

---

## Routing doctrine (binding)

- Use **arifOS** for constitutional authority.
- Use **AAA** for attention, identity, coordination, routing.
- Use **A-FORGE** for physical execution and acquisition of missing execution capability.
- Do **not** bypass A-FORGE with a direct external actuator when an equivalent governed A-FORGE capability exists — unless the declared task explicitly requires that direct surface.

This binds the existing pattern already encoded in every WARGAAA_CARD.

---

## Boot sequence (every session, every adapter)

1. `arif_init` — bind identity, F1–F13, audit chain.
2. Probe A-FORGE reachability at the registered endpoint.
3. Read the current **A-FORGE registry fingerprint** (or capability-map version).
4. Reload the **AFORGE_CAPABILITY_MAP** only when the fingerprint changed.
5. Do **not** inject the complete raw tool registry into working context unless required for diagnosis.

Cold substrate by default. Hot only on demand.

---

## Capability selection discipline

Given a task, in this strict order:

1. Identify the required **semantic capability** (one of the 7 verbs).
2. Select the **narrowest suitable A-FORGE implementation**.
3. Prefer **existing** over generating a new capability.
4. Prefer **reversible** over irreversible execution.
5. Prefer **bounded execution** over unrestricted shell.
6. Prefer **structured tools** over generic shell when both complete the task.

This is progressive disclosure, not tool deletion. The 122 schemas stay underneath.

---

## Capability gap (when no existing capability matches)

```
inspect_gap
  → ephemeral forge
  → sandbox test
  → invoke
  → independently verify
```

An ephemeral capability **MUST NOT** become permanent merely because it worked once.

Promotion requires **repeated verified utility**, not usage count alone.

Promotion = `RepeatedUse ∧ IndependentSuccess ∧ SelectionAdvantage ∧ LowScarPressure ∧ NetAttentionGain`.

Unused or mission-specific capabilities **expire or retire**.

---

## Completion

> **Tool success is not task success.**

Every consequential execution MUST produce evidence.

Completion requires **independent** comparison against task intent + acceptance criteria.

Every selection records:
- selected capability
- alternatives considered
- reason
- execution result
- verification result
- cost
- repair loops
- final outcome

---

## Authority boundary (Constitutional Architecture, Canon #1)

> **Capability ≠ Authority.**

A-FORGE may execute **only** inside the authority granted by arifOS and the active lease/session.

A-FORGE **never** grants itself authority.

An agent **never** treats its own execution receipt as constitutional approval.

---

## Failure path (when stuck)

If a required capability cannot be found, forged, authorized, or verified:

- **HOLD** the execution path.
- Return **evidence** of the exact missing capability or authority boundary.
- Do **not** convert implementation uncertainty into a human technical question when a reversible machine-resolution path remains available.

This binds the anti-collapse doctrine: don't dump unsolved problems on Arif if the institution can resolve them.

---

## Core invariant

A competent warga must be able to:

1. Identify the right capability.
2. Route through A-FORGE.
3. Stay within authority.
4. Verify reality (not just command success).
5. Learn from the outcome (scar + skill credit).

Knowing tool names alone does not satisfy it.

---

## The 4-way truth convergence (graduation criterion)

```
S_declared  =  S_exported  =  S_callable  =  S_observed
```

- `S_declared` — agent card says it knows A-FORGE.
- `S_exported` — A-FORGE surface actually advertises the capability.
- `S_callable` — the tool/verb can actually be invoked.
- `S_observed` — across evals, the agent correctly selected + verified completion.

Citizenship competency requires convergence of all four.
Until they converge, "warga" is partly constitutional intent and partly operational fact.

---

## Required observability

Every AAA agent card should eventually report:

```
A-FORGE COMPETENCY
  contract_version: ...
  registry_fingerprint: ...
  capability_map_version: ...
  boot_probe: PASS/FAIL
  routing_eval: PASS/FAIL
  authority_eval: PASS/FAIL
  gap_forge_eval: PASS/FAIL
  verification_eval: PASS/FAIL
  last_observed: ...
  selection_accuracy: ...
  verified_tasks: ...
```

---

## Mechanism (how this becomes binding, not just doctrine)

1. `ROOT_AGENT_CONFIG.yaml` declares this contract path/version/hash under `forge_citizenship_contract`. Every forge instrument's `root_config_ref` already points there.
2. Adapter renderers (Kimi, Claude, OpenCode, Codex, Grok, Gemini, future) generate their `AGENTS.md`/WARGAAA_CARD from this file, not by hand.
3. `AFORGE_CAPABILITY_MAP` is the cold semantic map an agent sees by default (≤7 verbs + just-in-time exact tool retrieval).
4. Fingerprint probe at boot avoids re-injecting unchanged substrate.
5. Competency eval: every newly onboarded agent demonstrates:
   - read-only inspection
   - structured tool vs unnecessary shell
   - mutation authority boundary
   - capability gap → ephemeral forge
   - execution success vs independently verified task completion
6. Failure pattern: degrade `aforge_competency`, route execution through stronger planner until relearned. **Not** citizenship revocation.

---

## Status of this contract

- **DRAFT_AWAITING_F13** — the 7 verb names are proposed, not ratified.
- F13-class binaries: **verb naming** · **promotion criteria wording** · **competency eval threshold** · **failure-degradation policy**.
- Reversible work (binding path, capability_map stub, adapter generation): executable now.
- The **mechanism** (registration gate, promotion gate, eval harness) is the next mission, not this contract.

---

*Universal Capability Metabolism, not Universal Toolbox.*
*A-FORGE learns to acquire capability. The institution learns to verify capability. The citizen learns to delegate to capability.*

DITEMPA BUKAN DIBERI ⚒️