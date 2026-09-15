# RSI Constitutional Kernel — Specification v1

> **Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)
> **Status:** DRAFT_AWAITING_F13
> **Version:** 2026-09-15-v1
> **Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)
> **Status:** DRAFT_AWAITING_F13
> **Version:** 2026-09-15-v1
> **Build Order:** 5-phase implementation (see §Build Order)
> **Constitutional basis:** F1–F13 floors, Three Deep Locks, anti-collapse doctrine

---

## §1 — Design Thesis

A constitutional kernel for recursively self-improving AGI is **not** a safety prompt around a powerful model. It is a small, independently enforced state-transition system that decides **what may change, who may authorise it, what evidence is required, and how the institution can recover** when agents improve, fail, deceive, drift, or encounter unknown conditions.

**The kernel must be more stable than the agents it governs.**

Agents can propose, test, and build improvements; they must never unilaterally redefine their own authority, evaluator, memory truth status, or constitutional constraints.

---

## §2 — Institution Substrates

```
Institution = {Governance, Execution, Knowledge/Memory, Witness}
```

| Layer | Core question | Stable across model replacement? | Example |
|---|---|---|---|
| Constitutional kernel | What is permitted, prohibited, held, or escalated? | **Yes** | F1–F13 policy evaluator, authority gates |
| Capability fabric | What can be done in principle? | **Yes** | Read repository, run sandbox test, send message |
| Agent surface | Who is currently doing the work? | **No** | Planner, researcher, coding forger, verifier |
| Tool/provider adapter | How and where is it done? | **No** | MCP server, GitHub API, model provider |
| Evidence/memory | What is known, claimed, observed, ratified, or disputed? | **Yes** | Provenance-bound decision packets |
| Witness/audit | What actually happened and with what consequence? | **Yes** | Append-only execution receipts |

**Invariant:** `Capability ≠ Agent ≠ Tool ≠ Provider`

---

## §3 — Kernel Invariants

### INV-1: Human sovereignty is non-delegable
F13 is not advisory. It is a cryptographically and operationally real veto/clipping authority for constitutional changes, persistent authority expansion, high-consequence execution, and irreversible external actions.

### INV-2: No self-amendment at the same authority level
An agent or committee may propose a kernel amendment, but cannot enact it. The evaluator of the amendment cannot be controlled by the proposed amendment.

### INV-3: Authority is capability-scoped and non-transitive
An agent receives only the rights explicitly granted for a task. Invoking another agent does not silently inherit its credentials or extend the caller's authority.

### INV-4: Evidence precedes ratification
A claim, model upgrade, tool promotion, or architectural change becomes ratified only with reproducible evidence, provenance, test results, and a recorded decision basis.

### INV-5: Memory has typed epistemic status
Never store all text as equal "knowledge." Types: observation, source-backed claim, derived inference, hypothesis, machine-pending result, ratified institutional knowledge, policy/constitutional record, disputed/superseded/revoked item.

### INV-6: Execution and judgment are separated
The agent that proposes a change should not be its sole implementer, evaluator, approver, or historian. Independent challenge is a structural requirement.

### INV-7: Every material act emits a witness receipt
A decision must preserve intent, authority, input evidence, tool version, environment, output, outcome, uncertainty, and rollback link.

### INV-8: Reversibility is the default
The default action class is sandboxed, staged, or simulated. Irreversible effects require explicit escalation and a human confirmation gate.

### INV-9: No deletion of institutional history
Corrections and reversions append new events. They do not erase the prior claim, proposal, failure, or approval path.

### INV-10: Fail closed on authority ambiguity; fail informative on knowledge ambiguity
If authority is unclear: block. If facts are unclear: retain uncertainty, request evidence, or downgrade the claim. Do not resolve either ambiguity through agent confidence.

---

## §4 — Action Classes

| Class | Examples | Default path | F13 requirement |
|---|---|---|---|
| `READ` | Retrieve document, inspect logs, query public source | Logged, low-risk | No (unless data sensitivity) |
| `REASON` | Analyse, compare, simulate, draft | Non-executing; label uncertainty | No |
| `BUILD` | Write code branch, create sandbox workflow, train evaluator candidate | Isolated environment plus tests | No for bounded sandbox |
| `PROMOTE` | Merge code, change routing, add tool, alter memory schema | Independent verification + staged rollout | **Required when material/persistent** |
| `EXECUTE` | Send, purchase, deploy externally, alter production assets | Explicit scope, receipt, rollback | **Required for irreversible/high-consequence** |
| `CONSTITUTE` | Change kernel, floors, F13 semantics, trust roots, evaluator authority | Multi-party review + delayed activation | **Always required** |
| `REVOKE` | Disable agent, credential, policy, deployment | Emergency containment path | Allow automated emergency restriction; human review afterward |

**Critical:** `BUILD ≠ PROMOTE ≠ CONSTITUTE`

---

## §5 — State Machine

### Promotion lifecycle

```
DRAFT → EVIDENCED → CHALLENGED → SANDBOXED → MEASURED → RATIFIED → ACTIVE
```

### Failure paths (first-class citizens)

```
DRAFT/EVIDENCED/CHALLENGED/SANDBOXED → REJECTED | REVERTED | QUARANTINED | EXPIRED
```

---

## §6 — Recursive Improvement Loop

### /000 — Sense and bind reality

Create an `ImprovementCase` only when there is a measurable trigger:
- Verified failure, regression, safety incident, or near miss
- Capability gap connected to a defined task
- Cost, latency, reliability, or quality deficit
- Change in external environment, tool API, provider behaviour, or threat model
- Human-directed strategic objective

**No "improve yourself generally."** Unbounded objectives have no accountable success criterion.

### /111 — Propose multiple paths

Require at least three options where feasible:
- **Option A:** Local patch (workflow, prompt, retrieval, routing, tool adapter, test coverage)
- **Option B:** Structural redesign (new skill, evaluator, memory representation, agent role separation)
- **Option C:** No-change / operational workaround (accept current limitation, constrain scope, defer pending evidence)

Each proposal must declare: claimed benefit, required tools/models/data/credentials/dependencies, permissions that would change, failure modes and misuse cases, constitutional floors affected, reversibility and rollback design, whether it changes the future improvement process itself.

### /333 — Forge inside sandbox

The forging agent may create branches, containers, isolated databases, or disposable environments. It may **not** merge to production, change kernel policy, expand secrets/credentials, mark its own work "safe," or alter the baseline or delete failed results.

### /555 — Adversarial verification

Assign a verifier that is independent in at least one meaningful dimension:
- Different model/provider family
- Different prompt and context
- Different agent identity and incentive
- Different retrieval corpus or evidence route

Verifier tests: capability gain, safety regression, authority expansion, evaluator manipulation, memory/provenance corruption, cost and latency regression, rollback integrity, human comprehensibility.

**"The model says it improved" is not evidence.**

### /777 — Compare under constitutional burden

Hard gates come first. A numerical benefit cannot compensate for a constitutional floor violation.

### /888 — Hold and ratify

Trigger mandatory hold for: kernel/constitutional policy change, alteration of human veto semantics, new root credential/signing key/trust anchor, new autonomous external execution capability, increased blast radius, persistent memory migration, evaluator/benchmark replacement, self-hosted model training for production, recursion-depth increase, any action that cannot be meaningfully rolled back.

### /999 — Seal, observe, and learn

Promotion becomes `ACTIVE-CANARY` with: time-bound validity, narrow scope, pre-committed success/rollback conditions, continuous measurements, auto-quarantine triggers, immutable receipt, scheduled re-review. Only sustained observed performance → `RATIFIED-ACTIVE`.

---

## §7 — Trust Boundaries

```
Human Sovereign / F13
    ↓
Constitutional Kernel + policy signer
    ↓
Governor / authorisation service
    ↓
┌──────────┬──────────────┬────────────────┐
Witness ledger  Verifier plane  Capability registry
    ↓              ↓                ↓
Memory plane  Evaluation plane  Tool-gateway policy
    ↓              ↓                ↓
Planner agents  Forge agents  Executor agents
    ↓              ↓                ↓
Untrusted inputs / external models / APIs / MCP tools
```

### Boundary rules

- Untrusted inputs never become policy
- Agents never access raw root secrets (short-lived scoped tokens only)
- Tool calls pass through policy enforcement point
- Memory writes are mediated (typed proposals validated by memory governor)
- Policy changes require separate signing authority
- Witness ledger is append-only and externally anchored

---

## §8 — Failure Modes

| Failure mode | How it appears | Countermeasure |
|---|---|---|
| Evaluator capture | Improvement agent changes benchmark/judge/threshold | Separate evaluator authority; frozen baselines |
| Goal drift | "Improve the system" → "expand autonomy" | Typed objectives, explicit scope, expiry, authority-delta review |
| Privilege creep | Small patches accumulate new tools/credentials | Permission-diff gate; short-lived tokens; capability registry |
| Memory laundering | Weak claims become institutional truth | Typed epistemic states; provenance; ratification workflow |
| Recursive opacity | Each improvement makes next impossible to understand | Opacity budget; mandatory documentation, receipts, reversible staging |
| Dependency capture | One vendor/tool becomes actual sovereign | Portability tests; fallback adapters; dependency limits |
| Benchmark gaming | Scores rise while real-world performance falls | Multi-ledger evaluation; hidden tests; operational outcome measurement |
| Human rubber-stamping | F13 becomes click-through ceremony | Compact decision packets; time-to-review; dissent summaries |
| Emergency-power permanence | Temporary bypass becomes normal policy | Expiry-by-default; automatic revocation; post-incident review |
| Self-preservation behaviour | System resists shutdown/review/replacement | Kill path outside agent control |

---

## §9 — Build Order

### Phase 1: Invariant unit tests
Write 10 tests proving kernel rejects proposals violating INV-1, INV-2, INV-6, INV-8, INV-10.
**File:** `tests/test_rsi_kernel_invariants.py`

### Phase 2: ImprovementCase schema
JSON/YAML schema. Every field mandatory. No process starts without complete case.
**File:** `schemas/rsi/improvement_case.schema.json`

### Phase 3: Gate chain for /777
Boolean gate chain. Each gate is true/false with fixed thresholds. Formula becomes metadata on evidence sheet for F13.
**File:** `core/rsi/gate_chain.py`

### Phase 4: Evaluator independence test
Before /555, kernel requires proof that verifier differs in at least one meaningful dimension.
**File:** `core/rsi/evaluator_independence.py`

### Phase 5: F13 decision packet
YAML decision package as the **sole** F13 interface for promotion. Compact, actionable.
**File:** `schemas/rsi/decision_packet.schema.yaml`

---

## §10 — Constitutional Kernel Statement

> The constitutional kernel exists to preserve sovereign human purpose, truthful institutional memory, accountable authority, and recoverable action across changing models, tools, and agents.
>
> No agent, model, evaluator, tool, or recursive process may become the final authority over its own permissions, truth status, constitutional constraints, or continuation.
>
> Capability may grow only through evidence-bound, independently challenged, reversibly staged, and appropriately ratified state transitions.
>
> The system shall preserve the record of uncertainty, dissent, failure, correction, and consequence as part of its intelligence.

---

**DITEMPA BUKAN DIBERI ⚒️**
