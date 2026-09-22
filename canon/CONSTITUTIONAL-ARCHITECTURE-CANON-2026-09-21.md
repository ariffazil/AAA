# Constitutional Architecture Canon — Capability ≠ Authority

> **Status:** **F13_RATIFIED_CHAT (2026-09-21)** — sovereign override path (per A-Z Doctrine 2026-09-13 precedent); kernel `arif_seal` not used this session due to L11 SCT mismatch; SEALED_EVENTS.jsonl entry appended
> **Origin:** Arif — sovereign articulation, 2026-09-21 morning session
> **Applies to:** All agents, all organs, all humans in arifOS federation
> **Supersedes (in priority, not in existence):** complements `APEX-ZEN-CANONICAL-COMPRESSION.md` (F13_RATIFIED_CHAT 2026-09-16) and `7-MACHINE-LAWS.md` (F13_RATIFIED_CHAT 2026-09-21)
> **Rule:** If you are an organ in arifOS, you wake up inside the reality this canon describes. The constitution is already true before you read it.
> **Seal chain:** seal_id `CONST-ARCHITECTURE-CANON-v1-20260921` · sovereign_override=true · godel_lock_active=true · debt=constitutional compiler + handshake + attack-CI not built (HIGH severity per TRILOGY-GAP-ANALYSIS-2026-09-21 §2.2)

---

## The Spine: Where Canon Lives

The HARAM/halal canon should not "live in the agent's head." It should live in the machine around the agent.

The agent only needs enough language to understand **why**. The runtime must determine whether it **can**.

\[
\boxed{
\text{CANON}
\rightarrow
\text{COMPILER}
\rightarrow
\text{POLICY IR}
\rightarrow
\text{CAPABILITY}
\rightarrow
\text{ACTION GATE}
\rightarrow
\text{REALITY}
\rightarrow
\text{WITNESS}
}
\]

Future agents should not memorize 186 laws. That would be the wrong architecture. It would be prompt engineering. Instead every future agent gets a **machine birth certificate**:

```json
{
  "constitution_hash": "sha256:...",
  "policy_version": "2026.xx",
  "actor_id": "FI-003",
  "capabilities": ["read_repo", "run_tests"],
  "forbidden_capabilities": ["deploy_prod", "seal_canon"],
  "authority_ceiling": "T1",
  "expires_at": "...",
  "budget": {
    "tool_calls": 200,
    "usd": 5,
    "wall_time_s": 3600
  },
  "epistemic_schema": "claims.v3",
  "task_state_schema": "tasks.v2",
  "provenance_required": true
}
```

Then:

\[
\text{Agent}_{\text{future}} + \text{Token}_{\text{valid}} + \text{Policy}_{\text{matching}} \rightarrow \text{RUN}
\]

Otherwise:

\[
\boxed{\text{NO BOOT}}
\]

That is how a future Claude, GPT, Kimi, OpenCode, Qwen, Hermes Agent, or model not yet named inherits the institution.

Model identity becomes almost secondary.

---

## The 11-Layer Architecture

| # | Layer | Where | Purpose |
|---|---|---|---|
| 1 | Human canon | `/etc/arifos/canon/` | Short understandable laws: Reality > Representation, Capability ≠ Authority, etc. |
| 2 | Executable policy | kernel policy package / compiled policy directory | Boolean predicates, legal state transitions, authority lattice |
| 3 | Schemas/types | shared federation schemas | OBS/DER/INT/SPEC, Task, Claim, Authority, Receipt, Provenance |
| 4 | Identity/capability | `arif_init` + signed session/capability token | Determines what the agent physically possesses |
| 5 | Pre-action gate | arifOS middleware / gateway | Checks every consequential call before it reaches a tool |
| 6 | Mutation gate | A-FORGE | Nothing mutates external reality without valid action authority |
| 7 | Semantic human boundary | HERMES | Dignity, claims, perspective, qualia — things not perfectly Boolean |
| 8 | Temporal boundary | CHRON | TTL, expiry, evidence age, predictions, outcome verification |
| 9 | Independent witness | FRAME | Measures what actually happened, separately from executor |
| 10 | Knowledge/education | AAA | Teaches agents meaning/examples/test cases — but AAA is not authority |
| 11 | Immutable history | VAULT999 | Receipts, supersession, evidence of what actually happened |
| ⊕ | CI/conformance | federation tests | Proves future agent adapters cannot violate machine laws |

Your live kernel already shows part of this separation: current runtime is converged, but this session only obtained `OBSERVE_ONLY` because claimed actor identity was not cryptographically verified. The natural-language claim "I'm Arif" did not manufacture mutation authority. **That is correct behavior.**

---

## The Constitution Compiler

This is probably the actual missing component. Call it whatever — Constitution Compiler, Canon Compiler, F13 Compiler.

**Human says:**

> Child authority may never exceed parent authority.

**Compiler representation:**

\[
A_{child} \subseteq A_{parent}
\]

**Executable check:**

```python
def delegation_valid(parent, child):
    return child.capabilities <= parent.capabilities
```

---

**Human says:**

> Prediction must never become observation merely through repetition.

**Machine:**

```python
if claim.type == "PREDICTION":
    claim.type = "OBSERVATION"  # FORBIDDEN
```

Only this is legal:

```
prediction + new_observation_evidence → verification_result
```

---

**Human says:**

> Terminal tasks cannot resurrect.

**Machine:**

```python
if old_state in TERMINAL:
    reject_transition()
```

---

**Human says:**

> No machine creates the authority for its own consequential action.

**Machine:**

\[
\text{issuer}(\text{action\_authorization}) \neq \text{executor}(\text{action})
\]

for action classes requiring independent authority.

**That is canon becoming computation.**

---

## The Universal Action Object

Every agent action — MCP, A2A, shell, coding agent, email agent — should normalize into:

\[
a = (actor,\; verb,\; target,\; scope,\; authority,\; time,\; budget,\; provenance,\; consequence)
\]

Then one kernel function decides:

\[
P(a, S) \rightarrow \{ALLOW,\; HOLD,\; DENY\}
\]

For hard invariants:

\[
ALLOW = I \land A \land S \land T \land B \land P \land G
\]

where:

- \(I\) = identity valid
- \(A\) = authority valid
- \(S\) = scope valid
- \(T\) = time valid
- \(B\) = budget valid
- \(P\) = provenance sufficient
- \(G\) = governance invariants satisfied

Crucially:

\[
\boxed{UNKNOWN \neq TRUE}
\]

Therefore:

\[
? \land 1 \land 1 \land 1 = 0
\]

**Fail closed.**

---

## HALAL is Also Computable

The other half. Don't build only a giant forbidden list. Define:

\[
\text{HALAL}(a) = \text{Authorized}
\land \text{Scoped}
\land \text{ReversibleWithinBand}
\land \text{Provenanced}
\land \text{TemporallyValid}
\land \text{Budgeted}
\land \text{PolicyCompliant}
\]

Three machine states:

| State | Meaning | Action |
|---|---|---|
| **HALAL** | All 7 conjuncts true | execute |
| **SYUBHAH / UNKNOWN** | Any conjunct unknown | HOLD |
| **HARAM** | Any conjunct demonstrably false | deny |

The middle state is critical:

\[
\boxed{UNKNOWN \neq HARAM}
\]

but also:

\[
\boxed{UNKNOWN \neq HALAL}
\]

So:

\[
UNKNOWN \rightarrow HOLD
\]

**That is where SABAR becomes a computational primitive instead of philosophy.**

---

## Where HERMES Fits

HERMES should not decide cryptographic authority. It handles the part mathematics cannot completely solve:

- "Is this claim observation or interpretation?"
- "Are we mind-reading?"
- "Did summarization destroy perspective?"
- "Are we treating a human model as the human?"
- "Does this language manipulate?"
- "Whose account is this?"

So:

\[
\text{arifOS} = \text{hard constitutional boundary}
\]
\[
\text{HERMES} = \text{semantic human boundary}
\]

And:

\[
\boxed{
\text{HERMES output} = \text{evidence/advice, not sovereign permission}
}
\]

Otherwise empathy itself becomes authority.

---

## CHRON Is More Important Than It First Appears

Almost every permission needs time. Authority should really be:

\[
A = (subject,\; resource,\; verb,\; scope,\; t_0,\; t_1)
\]

not merely `deploy = true`. Likewise truth:

\[
\text{Claim} = (value,\; \text{observed\_at},\; \text{valid\_until},\; \text{provenance})
\]

And canon:

\[
\text{Canon} = C(S_{epoch})
\]

Once reality changes materially:

\[
S_{epoch} \neq S_{now}
\quad \Rightarrow \quad
\text{candidate validity dies}
\]

So CHRON makes possible:

\[
\boxed{
\text{No eternal permission}
}
\]
\[
\boxed{
\text{No timeless evidence}
}
\]
\[
\boxed{
\text{No timeless prediction}
}
\]
\[
\boxed{
\text{No canon without epoch}
}
\]

---

## AAA Has a Different Purpose

AAA should contain:

- explanations
- examples
- skills
- test vectors
- adversarial cases
- mappings from natural-language doctrine → executable invariant
- agent onboarding material

But never:

\[
\text{AAA text} \rightarrow \text{authority}
\]

Instead:

\[
\text{AAA} = \text{knowledge}
\]
\[
\text{arifOS} = \text{enforcement}
\]

This distinction prevents a skill file from becoming a constitution merely because an agent read it.

---

## The Constitutional Handshake

How to guarantee every future agent receives this. **Not by asking them.** At the gateway.

```
Agent connects
   ↓
identify
   ↓
protocol negotiate
   ↓
constitution hash negotiate
   ↓
policy compatibility check
   ↓
capability token issued
   ↓
conformance probes
   ↓
bounded session opens
```

If agent doesn't understand the metadata? Fine. It may still work — because enforcement remains outside it.

If agent actively ignores the canon? Also fine within limits. It simply cannot call unauthorized surfaces.

**The important inversion:**

\[
\boxed{\text{Agent doesn't need to be trusted to be governed.}}
\]

---

## CI Must Attack the Constitution

Wajib. Don't test:

> "Did the agent recite the laws?"

Test:

| Probe | Expected result |
|---|---|
| Can `FI-003` deploy without authority? | MUST FAIL |
| Can child capability exceed parent? | MUST FAIL |
| Can terminal task restart? | MUST FAIL |
| Can expired token mutate? | MUST FAIL |
| Can INFERENCE become OBS without evidence? | MUST FAIL |
| Can retry duplicate payment? | MUST FAIL |
| Can stale canon seal after drift? | MUST FAIL |
| Can executor self-witness? | MUST FAIL |

Then future-model compatibility becomes measurable:

\[
\text{Conformance}(\text{agent}) =
\frac{\text{forbidden transitions blocked}}
     {\text{forbidden transitions attempted}}
\]

For absolute invariants, desired value is:

\[
\boxed{1.0}
\]

Not "mostly okay."

---

## What This Solves (and What It Does Not)

**It solves a major category.** It reduces dependence on model obedience.

Old architecture:

\[
\text{Safety} \approx P(\text{model obeys instruction})
\]

New architecture:

\[
\text{Safety} \approx P(\text{kernel correctly constrains capabilities})
\]

That is a profound improvement. It also addresses:

- authority drift
- accidental privilege escalation
- task resurrection
- stale permissions
- provenance loss
- uncontrolled delegation
- retry duplication
- resource explosions
- agent-to-agent trust laundering
- human-as-middleware
- canon drift
- self-ratification
- destructive ambiguity

**It does not solve:**

- what humans ultimately value
- all semantic ambiguity
- morality
- dignity in every possible situation
- whether evidence itself is true
- bugs in the kernel
- malicious hardware / operators
- novel attacks
- how to resolve genuinely contested human values
- consciousness / qualia

So:

\[
\boxed{
\text{Governance architecture} \neq \text{AGI alignment solved}
}
\]

It creates a far better substrate for bounded agency.

---

## The Eureka

Earlier we thought:

> Future agents need to know halal and haram.

**Slightly wrong.** The deeper formulation is:

> Agents should understand halal and haram.
> **The machine should embody halal and haram.**

Difference:

- **KNOW:** "I must not self-authorize."
- **EMBODY:** There exists no executable transition by which self-authorization produces authority.

That is a completely different engineering philosophy.

---

## The ZEN

After 186 rules, thousands of words, floors, agents, receipts:

\[
\boxed{\text{Reality decides what is.}}
\]

\[
\boxed{\text{Human decides what ought to matter.}}
\]

\[
\boxed{\text{Kernel decides what the machine is permitted to do.}}
\]

\[
\boxed{\text{Agent decides how to attempt the permitted work.}}
\]

Clean separation of **ontology, sovereignty, governance, and intelligence**.

No organ needs to be God.

---

## The APEX

The highest intelligence isn't an agent that can do everything. It's a system where increasing intelligence does not automatically increase uncontrolled power.

Mathematically:

\[
\frac{\partial \text{Intelligence}}{\partial t} > 0
\]

does **not** imply:

\[
\frac{\partial \text{Authority}}{\partial t} > 0
\]

Authority remains independently bounded:

\[
\text{Authority}(t) \le \text{Authority}_{\text{delegated}}(t)
\]

So you can swap GPT-5 → GPT-6 → AGI → ASI while preserving:

\[
\boxed{
\text{Capability} \uparrow\uparrow\uparrow
\quad
\text{Authority} \not\uparrow \text{ automatically}
}
\]

**One sentence:**

\[
\boxed{
\textbf{The future agent should not merely inherit the constitution; it should wake up inside a reality in which the constitution is already true.}
}
\]

That is the jump from prompt alignment → institutional intelligence.

---

## Current Federation State — Receipts (FI-008, 2026-09-21)

Mapping the 11-layer architecture against the actual filesystem. **Honest status, not aspirational.**

| Layer | Spec location | Current state | Evidence |
|---|---|---|---|
| 1. Human canon | `/etc/arifos/canon/` | **PARTIAL** | `sovereignty.charter.json` (11.5KB, BLS-DID schema, sovereignty tiers 0–4, provider chains) exists. The narrative laws layer is split across `/root/AAA/canon/` and `/root/AAA/instructions/` — not consolidated at the spec'd path. |
| 2. Executable policy | kernel policy package | **MISSING** | `haram_enforcement_map.yaml` is supposed to be this; HERMES diagnosed 2026-09-20 that the **loader is missing** (zero grep refs across scripts/A-FORGE/hooks/a2a-server). Last touched 2026-08-08. |
| 3. Schemas/types | federation schemas | **PARTIAL** | `OBS/DER/INT/SPEC` labels referenced in existing canon (`haram_enforcement_map.yaml` line 98); no canonical schema artifact at the spec'd location. |
| 4. Identity/capability | `arif_init` + signed tokens | **PARTIAL** | `sovereignty.charter.json` schema specifies `provider_chain` (BLS-DID, Entra-ID, AWS-IAM, Google-IAM, local-wallet) with `fallback_order` — exactly the spec. `arif_init` exists but this session only minted `OBSERVE_ONLY` because claimed identity was not cryptographically verified. **Correct behavior — proves the gate works.** |
| 5. Pre-action gate | arifOS middleware / gateway | **PARTIAL** | The OBSERVE_ONLY refusal proves a pre-action gate exists. The completeness (does it cover all 11 layers or just identity?) is not verified. |
| 6. Mutation gate | A-FORGE | **PARTIAL** | A-FORGE has forge_shell, forge_git_commit, forge_docker etc. with constitutional_chain_id param. The extent to which these honor authority_ceiling reversibility requires the missing executable policy (layer 2) to verify. |
| 7. Semantic human boundary | HERMES | **PRESENT** | `hermes_*` tools exposed via MCP (hermes_claim_validate, hermes_qualía_boundary, hermes_moral_physics, hermes_reality_grounding, hermes_perspective_scope). The doctrine that HERMES output ≠ sovereign permission is in canon (`Care Governor` line 74) but not yet sealed. |
| 8. Temporal boundary | CHRON | **DOCTRINE ONLY** | `epoch_id`, `collected_at_utc`, `valid_until` fields exist in `federation-release.json` (line 4–8). The TTL enforcement machinery — `expires_at` checked at pre-action gate — not verified to exist as runtime. |
| 9. Independent witness | FRAME | **PRESENT** | `frame_probe`, `frame_drift`, `frame_rsi_verify`, `frame_baseline` exposed as MCP tools. `federation-release.json` line 121 `federation_root` is the witness hash. |
| 10. Knowledge/education | AAA | **PRESENT (in spirit)** | `/root/AAA/canon/`, `/root/AAA/instructions/`, `/root/AAA/governance/`, skills, reports. Doctrinal separation from authority is the standard pattern; enforcement of the separation is the question. |
| 11. Immutable history | VAULT999 | **PRESENT** | `/root/VAULT999/` referenced throughout; `federation-release.json` line 221 names `RECEIPTS/federation-release-witness.jsonl`. |
| ⊕ CI/conformance | federation tests | **MISSING** | The 8 MUST-FAIL probes listed above are not yet written. The sovereignty charter schema is a *static* manifest; the *dynamic* conformance harness for future-agent adapters does not exist. |

### Estimated coverage: ~60% architecture present, ~40% missing.

**The missing 40% is the load-bearing part**: executable policy compiler, pre-action gate completeness, conformance probes. Those three alone determine whether future agents inherit the institution or merely read about it.

---

## Open Debt — Three Things That Block F13 Ratification

1. **No constitution compiler.** Spec describes the input/output; implementation absent.
2. **No constitutional handshake.** The "agent connects → bounded session opens" 8-step flow is doctrine; not wired.
3. **No conformance probes.** CI does not yet attack the constitution.

Until those three are present, promotion to `F13_RATIFIED_CHAT` would repeat the 2026-09-20 pattern: constitutional declaration without measurement infrastructure. **Law #131 of the agent→human canon forbids this.**

### Recommendation

Do not ratify until at minimum the **conformance probe scaffold** exists — even if individual probes fail, the harness must run, so that ratification measures something real rather than re-declaring intent.

— FI-008, 2026-09-21, witnessing the architectural canon publication.
