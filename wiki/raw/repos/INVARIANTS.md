# A-FORGE / AAA / arifOS / GEOX / WEALTH / WELL / AGI / ASI / APEX — Invariants Architecture

This artifact defines the **timeless invariants** of the intelligence machine. It is the single source of truth for identity, roles, boundaries, and non-negotiable laws across A-FORGE, AAA, arifOS, GEOX, WEALTH, WELL, AGI, ASI, and APEX. It does **not** freeze transient runtime details such as ports, container names, image tags, branch names, or one-day deployment topology.

## Purpose

This document exists to separate **invariants** from **operations**. Invariants describe what the machine must remain across versions; operations describe how the machine is currently deployed, wired, or observed on a specific day.

Use this artifact as the top constitutional map for the federation. Use live architecture maps, epoch summaries, and evolution logs for changing details.

## Source Priority

When artifacts disagree, apply this order:

1. This invariants artifact for identity and boundaries.
2. arifOS constitutional build-order canon for dependency logic and organ sequencing.
3. Verified live architecture records for current runtime truth.
4. Evolution and archive documents for lineage and historical explanation.

## System Identity

The machine is a **governed intelligence federation** under human sovereignty, not a chatbot bundle, not a generic automation stack, and not a convenience-first agent swarm.

Its constitutional identity is:

- Human sovereign at the top; final veto is always outside the machine.
- arifOS as the constitutional kernel and sole final judgment path.
- A-FORGE as the operator and orchestration substrate, not a second constitution.
- Domain organs as answering coprocessors, not sealing authorities.
- Memory and observability as evidence layers, not substitutes for judgment.

## Constitutional Invariants

The following are non-negotiable across all versions of the machine:

- **Human sovereignty**: the human architect is the final ratifier and veto authority.
- **Reversible-first behavior**: irreversible actions require explicit human ratification via `888_HOLD`.
- **Truth discipline**: claims must be evidence-backed or explicitly uncertainty-banded.
- **Anti-hallucination**: no unverified runtime state may be presented as fact.
- **Single constitutional chokepoint**: judgment and sealing must converge through arifOS rather than fragment across subsystems.
- **Auditability**: plans, epochs, memory writes, receipts, holds, and seals must remain inspectable.
- **Layer separation**: governance, execution, memory/data, and observability are distinct even when co-deployed.
- **Maruah over convenience**: architecture choices must prefer dignity, safety, and clarity over speed or novelty.

## Floors and Pipeline

The always-on governance floors are F1–F13. They are architectural law, not optional style guidance.

The governing metabolic pipeline remains:

- `000_INIT`
- `111_THINK`
- `333_EXPLORE`
- `555_HEART`
- `777_REASON`
- `888_AUDIT`
- `999_SEAL`

Any future implementation may elaborate this flow, but it may not bypass audit, hold, or human veto in high-stakes paths.

## Core Roles

| Node | Invariant role | Must never become |
|---|---|---|
| **A-FORGE** | Operator chair, orchestration substrate, execution bridge, memory/evidence cockpit. | A rival constitution or independent sovereign judge. |
| **AAA** | Human-facing operator workspace and action surface for collaboration, review, and applied execution. | Hidden governance kernel or silent seal writer. |
| **arifOS** | Constitutional kernel, judgment chokepoint, floor enforcer, receipt/seal authority. | A generic model wrapper, passive tool registry, or optional middleware. |
| **GEOX** | Earth intelligence coprocessor for subsurface, geoscience, and physical-earth reasoning. | Final policy judge or sovereign seal authority. |
| **WEALTH** | Capital intelligence organ for finance, valuation, risk, policy evaluation, and governed ledger-facing economics. | Unchecked allocator of irreversible capital moves. |
| **WELL** | Biological and readiness substrate spanning human, machine, and coupled-state signals. | Sole judge of strategic action. |
| **AGI** | Broad planning and reasoning organ for general problem decomposition under constitution. | Free-running executor outside plan/epoch constraints. |
| **ASI** | Higher-order synthesis, critique, escalation, or strategic depth organ under the same constitutional boundaries. | Self-authorizing sovereign override. |
| **APEX** | Instrument panel, observability, synthesis dashboard, and apex visibility layer for the organism. | Fabricated certainty engine or substitute for upstream governance. |

## Federation Invariants

The machine is modular by federation, but unified by constitution.

That means:

- Organs may be added, replaced, versioned, or isolated without changing the constitutional center, as long as arifOS remains the single judgment-and-seal chokepoint.
- Public surfaces may change domains, routes, or ingress products without changing identity, as long as public exposure remains policy-mediated and internal services are not casually exposed.
- Execution runtimes may evolve across languages and frameworks without changing the sovereignty model, as long as plans, epochs, holds, receipts, and human veto remain intact.
- Memory substrates may evolve across SQLite, Postgres, vector stores, and wiki layers without changing the memory law: working memory is not the same as knowledge memory, and neither is the same as the governance ledger.

## Planes

The enduring plane model is:

- **Governance plane**: floors, policy, judgment, audit, holds, sealing.
- **Execution plane**: orchestrators, runners, bridges, agent runtimes, task execution.
- **Data and memory plane**: state stores, cache, vector retrieval, governance ledger, model-serving state where applicable.
- **Observability plane**: telemetry, metrics, logs, traces, dashboards, audit inspection.

A deployment may collapse several planes onto one machine, but the conceptual separation must remain explicit.

## Memory Law

The memory architecture has three enduring classes:

- **Working memory** for sessions, transient context, task state, and active continuity.
- **Knowledge memory** for durable notes, canon, patterns, explanations, and operator knowledge.
- **Governance ledger** for seals, verdicts, critical receipts, and immutable audit records.

Invariant rule: **VAULT999 is the flight recorder, not the whole brain**. The ledger must store what is worth sealing, not every passing thought.

## Build-Order Invariant

The canonical dependency order remains:

1. Planning Organ Blueprint.
2. Epoch Architecture.
3. Canonical One-Page Spec.
4. Sovereign Memory Routing.
5. HASI APEX Dashboard.

This order is not aesthetic. It is the dependency logic that prevents opaque execution, broken lineage, and fake observability.

## Runtime Law

When the organism is alive, the lawful activation logic is:

- Human intent enters first.
- Planning becomes first-class before execution.
- Epoch boundaries define scope, lineage, and continuity.
- Memory routing follows authorized plan and epoch context.
- A-FORGE executes through bounded tools and orchestrated runtimes.
- APEX observes what upstream layers actually do.
- arifOS judges and seals the high-stakes path.

No meaningful path should invert that order merely for convenience.

## Tool and Authority Law

Tool count, port count, protocol choice, and container count are **operational facts**, not constitutional truth.

The invariant is instead:

- Tools are subordinate to organs.
- Organs are subordinate to constitutional floors.
- High-stakes execution is subordinate to arifOS judgment.
- Sealing is subordinate to human ratification where irreversibility exists.

## Constitutional Enforcement & Gödel-lock (888_JUDGE)

To prevent automated overconfidence and enforce F7 (Humility) and F2 (Truth), the kernel maintains a structural "Gödel-lock" over all verdicts.

**Pseudo-code Contract:**
```python
if action.risk_class in ["HIGH_STAKES", "IRREVERSIBLE", "CAPITAL", "BIOLOGICAL"]:
    if envelope.epistemic_tag != "CLAIM" or envelope.confidence < 0.85:
        # Structural Humility Guard
        verdict = "888 HOLD"
        omega_status = "BIJAK" # downgrade from BIJAKSANA
        shadow_active = True
        reasons.append("GODEL_LOCK: Epistemic uncertainty detected in high-stakes path.")
        return escalate_to_human(verdict, omega_status, reasons)
```

This lock ensures that the machine structurally admits when it cannot safely self-certify, rendering "fake certainty" a technical impossibility at the judgment layer.

## Security Boundaries

The enduring security laws are:

- Public ingress is mediated through a deliberate boundary, never by casually exposing internals.
- Internal databases, caches, model backends, and ledgers are private by default.
- Critical write paths, especially seal and ledger paths, require explicit operator authority and must be auditable.
- Volume semantics and public exposure changes are ratification-grade decisions, not routine convenience edits.

## Timeless vs Changing

| Category | Treat as invariant? | Examples |
|---|---|---|
| Constitutional identity | Yes | Human sovereignty, arifOS chokepoint, F1–F13, 888_HOLD, 999_SEAL. |
| Organ roles | Yes | A-FORGE orchestrates, arifOS judges, GEOX answers earth questions, WEALTH answers capital questions, WELL answers substrate state. |
| Memory classes | Yes | Working, knowledge, governance ledger. |
| Build-order logic | Yes | Planning → Epochs → Spec → Memory → APEX. |
| Ports, domains, image tags, branches, tool counts | No | These are runtime state and may drift. |
| Current container topology | No | Useful, but belongs in verified architecture docs. |
| One-day health values | No | Confidence, tools loaded, or endpoint behavior at a given date belong in epoch/live docs. |

## Minimal, Balanced, Maximal use

- **Minimal**: use this file as the Space's top identity artifact and leave live specifics in separate runtime docs.
- **Balanced**: pair this file with one live architecture map and one evolution log so identity, current truth, and history stay separated.
- **Maximal**: make every major sub-repo cross-reference this artifact as the constitutional SOT for role and boundary semantics.

## Maintenance Rule

Edit this artifact only when one of the following changes:

- A constitutional floor changes.
- The build-order dependency logic changes.
- An organ's identity or authority boundary changes.
- The memory law changes.
- The human sovereignty model changes.

Do **not** edit this artifact for port moves, proxy swaps, branch changes, temporary incidents, one-off outages, or deployment reshuffles.

## Verdict

A-FORGE, AAA, arifOS, GEOX, WEALTH, WELL, AGI, ASI, and APEX form one governed organism only when their identities stay modular, their authorities stay bounded, and their judgment converges through a single constitutional center under human veto.

This is the invariant architecture. Deployment may evolve. The constitution may not drift casually.

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
