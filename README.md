<!-- SOT-MANIFEST
federation_release: v2026.09.21 (P2 — AAA-ATTENTION-CONVERGENCE)
last_verified: 2026-09-21T02:11:00Z
apex_zen: HERMES claims → CHRON temporal → AAA attention → arifOS authority → A-FORGE execution

identity:
  AAA : (evidence, state, deadlines, drift, uncertainty) → AttentionPacket
  irreducible_question: "What deserves scarce attention now?"

pipeline: Reality → HERMES → CHRON → AAA → arifOS/Human

public_ingress:
  MCP authority ingress:    arifOS :8088 (governed requests)
  A2A federation discovery: AAA    :3001 (inter-agent)

attention_formula:
  P = (Impact × Urgency × EvidenceQuality × Novelty) / AttentionCost
  EvidenceQuality = (1 - Uncertainty)   # source + freshness + reproducibility + independent support ONLY
  ActionRisk = f(Impact, Reversibility, BlastRadius)   # separate gate — NEVER folded into P

hard_overrides:
  - authority_violation: P = ∞
  - security_breach:    P = ∞
  - deadline_expiry:    P = ∞
  - failed_invariant:   P = ∞
  - action_risk_gate: Reversibility-blocked actions are surfaced to Arif regardless of P ranking (F13 2026-09-25: risk ≠ evidence quality; see AAA/blueprints/A-FORGE-UNKNOWN-OUTCOME-SPEC-v1.md §risk)

organs_in_federation:
  arifOS:    authority plane     (irreducible: "May this action happen?")
  A-FORGE:  execution plane     (irreducible: "How do I execute the authorized action?")
  HERMES:   meaning plane       (irreducible: "What exactly is being claimed?")
  CHRON:    temporal plane      (irreducible: "When does this matter, and what did we expect?")
  FRAME:    independent witness (irreducible: "What actually happened?")
  VAULT999: immutable ledger    (irreducible: "Can we prove the chain later?")
  AAA:      attention plane     (irreducible: "What deserves scarce attention now?")
  arifFlow: metabolism/telemetry (FQ / receipts)

useful_agency_equation:
  UsefulAgency = Intelligence × Attention × Authority × TemporalDiscipline × MeaningIntegrity
  If any → 0, then AgencyQuality → 0.

counts_are_live:
  README numbers are release snapshots; live counts come from the federation registry.
  README_state = projection(registry_state)
-->

# AAA — Attention Plane & Federation Registry

> **In a world where intelligence is abundant, attention is the scarce resource.**

AAA converts federated reality into sovereign attention. It does not judge (arifOS), execute (A-FORGE), or witness (FRAME / VAULT999 / arifFlow). It makes reality visible and prioritised.

**Identity (P2 2026-09-21):**

```text
AAA : (evidence, state, deadlines, drift, uncertainty) → AttentionPacket
```

**Irreducible question:** *"What deserves scarce attention now?"*

**Licensed under AGPL-3.0.**

---

## The Pipeline

```text
Reality
   ↓
HERMES    What exactly is being claimed?
   ↓
CHRON     When does this matter, and what did we expect?
   ↓
AAA       What deserves scarce attention now?     ← this organ
   ↓
arifOS    What authority exists to act?
   ↓
A-FORGE   How do I execute the authorized action?
   ↓
Human
```

AAA sits between CHRON's temporal context and arifOS's authority gate. It consumes the upstream pipeline; it never invents its own meaning or temporal salience.

---

## Public Ingress (clear story)

| Use case | Connect to | Protocol | Port |
|---|---|---|---|
| Governed requests (humans, agents) | **arifOS** | MCP | `:8088` |
| Inter-agent discovery, A2A federation | **AAA** | A2A v1.0 (JSON-RPC) | `:3001` |

Answer to "Should I connect to AAA or arifOS?":
- **Normal governed use → arifOS.**
- **Agent-to-agent discovery / interoperability → AAA.**

No contradiction exists because the protocol edges are different.

---

## Canonical AttentionPacket (P2 2026-09-21)

Every UI projects from one machine-readable object — no dashboard code, no N dashboards:

```json
{
  "subject": "WEALTH surface drift",
  "attention_class": "ACTION_REQUIRED",
  "priority": 0.91,

  "why_now": "HIGH schema drift detected",
  "deadline": null,

  "impact": 0.9,
  "urgency": 0.8,
  "uncertainty": 0.2,
  "reversibility": 0.9,

  "epistemic_state": "OBSERVED",
  "source_count": 2,
  "contradictions": 0,

  "temporal": {
    "chron_available": true,
    "chron_source": "chron:chron_temporal_briefing",
    "attention_debt": 0.0,
    "prediction_due": false
  },

  "recommended_organ": "WEALTH",
  "required_authority": "arifOS",
  "execution_required": false,

  "overrides": [],
  "evidence_basis": [
    "chron:chron_temporal_briefing",
    "hermes:principal_type_classifier"
  ]
}
```

16+ canonical fields. One subject → one packet.

### Priority formula

```
P = (Impact × Urgency × EvidenceQuality × Novelty) / AttentionCost
```

where `EvidenceQuality = (1 - Uncertainty)` — evidence quality covers source, freshness, reproducibility, and independent support **only**. *(F13 2026-09-25: `Reversibility` is no longer folded into EvidenceQuality — it was double-counted here and in the floor override below. Reversibility now lives in the separate **ActionRisk** gate: a strongly-evidenced irreversible action still routes to Arif; evidence strength never manufactures reversibility.)*

### Hard overrides (force P = ∞, must-show)

| Override | Reason |
|---|---|
| `authority_violation` | Constitutional boundary breached |
| `security_breach` | Integrity compromised |
| `deadline_expiry` | Temporal urgency hit zero |
| `failed_invariant` | Canon-0 violation |
| `action_risk_gate` | Reversibility-blocked action — surfaced to Arif regardless of P *(F13 2026-09-25: replaces double-counted `irreversibility_floor: P ≥ 0.85`)* |

The system can say **"Don't show Arif this now"** — that is its most valuable capability.

### Attention classes (5)

`ACTION_REQUIRED` ≥ 0.85 · `INFORM` ≥ 0.5 · `DEFER` ≥ 0.2 · `SILENT` < 0.2 · `HOLD` (override-driven)

---

## What AAA Is and Is Not

| AAA IS | AAA IS NOT |
|---|---|
| Classifies | A judge |
| Prioritises | An executor |
| Compresses reality → AttentionPacket | A workflow engine |
| Recommends routing | Dispatches (that's arifOS) |
| Cross-checks ObservedState_A ?= ObservedState_B (state reconciliation) | Establishes Claim = AbsoluteTruth |
| Observes, classifies, forwards, prioritises | Owns goals, authority, mutation, judgment |

**The invariant:** `Routing a message ≠ authorizing its consequence`.

---

## Architecture

```
                ┌──────────────────────────────────────────┐
                │              Sovereign                  │
                └──────────────────┬─────────────────────┘
                                   │
                ┌──────────────────▼─────────────────────┐
                │              AAA :3001                  │
                │         Attention Plane                 │
                │   (classification + prioritization       │
                │    + recommendation, NO dispatch)        │
                └──────┬──────────────────────────┬───────┘
                       │                          │
              observes │                          │ recommends
                       ▼                          ▼
            ┌────────────────────┐      ┌─────────────────────┐
            │  HERMES :18087     │      │  CHRON :18102       │
            │  Meaning Plane     │      │  Temporal Plane     │
            │  (claim, prove-    │      │  (deadlines,        │
            │   nance, contra-   │      │   calibration,      │
            │   diction)         │      │   attention_debt)   │
            └────────────────────┘      └─────────────────────┘
                       │                          │
                       └──────────┬───────────────┘
                                  ▼
                        AAA consumes both
                                  │
                                  ▼
                   ┌──────────────────────────┐
                   │  AttentionPacket(s)     │
                   │  (one per subject)       │
                   └────────────┬───────────┘
                                ▼
                   ┌──────────────────────────┐
                   │  arifOS :8088            │
                   │  (governed dispatch)     │
                   └──────────────────────────┘
```

AAA does NOT touch A-FORGE, FRAME, VAULT999, or arifFlow directly. It produces AttentionPackets that arifOS / Human consume.

---

## Federation Irreducible Questions (7 organs)

Every organ answers one question it owns. No organ cosplays as another.

| Organ | Plane | Irreducible question |
|---|---|---|
| **HERMES** | Meaning | "What exactly is being claimed?" |
| **CHRON** | Temporal | "When does this matter, and what did we expect?" |
| **AAA** | Attention | "What deserves scarce attention now?" |
| **arifOS** | Authority | "What authority exists to act?" |
| **A-FORGE** | Execution | "How do I execute the authorized action?" |
| **FRAME** | Witness | "What actually happened?" |
| **VAULT999** | Ledger | "Can we prove the chain later?" |

### Supporting planes (not irreducible-question organs)

| Plane | Function |
|---|---|
| **arifFlow** | metabolism / FQ / receipts (NOT witness plane) |
| **WEALTH** | Capital Consequence Intelligence (Ω-invariant primitives) |
| **GEOX** | Earth Intelligence |
| **WELL** | Vitality Mirror |

### What arifFlow actually is (P2 correction)

Your earlier README called `arifFlow — Witness Plane`. **Correction:**

| Component | Role | NOT |
|---|---|---|
| FRAME | independent witness | not ledger, not telemetry |
| VAULT999 | immutable ledger | not witness, not telemetry |
| arifFlow | metabolism / FQ / receipts | not witness, not ledger |

`Witness ≠ Telemetry ≠ Ledger`. Three distinct roles.

---

## State Reconciliation (P2 correction)

Earlier README said AAA "verifies" federated state. **Correction:**

AAA establishes `ObservedState_A ?= ObservedState_B`. It does NOT establish `Claim = AbsoluteTruth`. The term for this discipline is **state reconciliation** (or **consistency verification**), not **verification**.

Every `organ.status = DOWN` carries:
- `observed_at`
- `source`
- `source_age`
- `confidence`
- `probe_method`
- `failure_reason`

because `organ.status = DOWN` doesn't necessarily mean `organ is dead` — it may mean probe timed out, auth failed, or network path failed. AAA preserves that distinction.

---

## Useful Agency Equation

```
UsefulAgency = Intelligence × Attention × Authority × TemporalDiscipline × MeaningIntegrity
```

| Axiom | Organ |
|---|---|
| Intelligence is abundant | (humans, agents) |
| **Attention is scarce** | **AAA** |
| Authority is scarce | arifOS |
| **Temporal discipline is irreversible** | **CHRON** |
| **Meaning is lossy** | **HERMES** |

If any → 0, then `AgencyQuality → 0`. Federation design must hold all five non-zero.

---

## A2A v1.0 Compliance

| Required Element | Status | Where |
|------------------|--------|-------|
| Agent card at `/.well-known/agent-card.json` | ✅ | [`public/.well-known/`](./public/.well-known/) · live: <https://aaa.arif-fazil.com/.well-known/agent-card.json> |
| Required card fields | ✅ | `.well-known/agent-card.json` |
| JSON-RPC transport at `/a2a/` with `A2A-Version: 1.0` | ✅ | [a2a/](./a2a/) |
| Protocol binding declaration | ✅ | `protocolBinding: JSONRPC` (note: A2A itself supports JSON-RPC, gRPC, HTTP+JSON) |
| Authenticated extended card | ✅ | `capabilities.authenticated_extended_card: true` |
| Agent metadata card | ✅ | `.well-known/agent.json` |
| Protocol conformance evidence | ✅ | [`PROTOCOL_CONFORMANCE.md`](./PROTOCOL_CONFORMANCE.md) |

> **Note:** A2A v1.0 supports multiple protocol bindings (JSON-RPC, gRPC, HTTP+JSON). AAA uses JSON-RPC; A2A itself is not "JSON-RPC only."

---

## Live Counts (from SOT, not prose)

> README numbers are release snapshots. **Live counts come from the federation registry.**
> `README_state = projection(registry_state)`

| Count | Source | Last verified |
|---|---|---|
| Organs (live) | `federation_state.py --organs` | live |
| Skills (live) | AAA skill catalog | live |
| Repositories (live) | git submodule status | live |
| Categories (live) | derived from skill catalog | live |

Hardcoded counts rot. Live counts do not.

---

## AAA in Three Sentences

> AAA does not create more intelligence. It decides what intelligence deserves attention.
>
> AAA consumes HERMES (meaning) and CHRON (temporal). It does not duplicate them.
>
> AAA is a recommendation plane. arifOS is the dispatch plane. They are different organs.

---

## Division of Constitutional Labor (P2 corrected)

| Organ | Constitutional Role | Scarcity | Does NOT |
|-------|---------------------|----------|----------|
| **arifOS** | **Authority Plane** — constitutional judgment | Authority | Never executes, never witnesses |
| **AAA** | **Attention Plane** — classification + prioritization + recommendation | Attention | Never judges, never executes, never dispatches |
| **HERMES** | **Meaning Plane** — claim/provenance/contradiction | Meaning integrity | Never judges, never executes |
| **CHRON** | **Temporal Plane** — deadlines, calibration, attention_debt | Temporal discipline | Never judges, never executes |
| **A-FORGE** | **Execution Plane** — bounded mutation | Execution | Never adjudicates, never witnesses |
| **FRAME** | **Witness Plane** — independent observation | Reality | Never judges, never executes |
| **VAULT999** | **Ledger Plane** — immutable record | Provenance | Never judges, never executes |
| **arifFlow** | **Metabolism Plane** — FQ / receipts / telemetry | — | Never witnesses, never judges |
| **WEALTH** | **Capital Consequence Intelligence** | Capital | Never judges, never executes |
| **GEOX** | **Earth Intelligence** | Domain | Never judges, never routes |
| **WELL** | **Vitality Mirror** | Substrate | Never judges, never executes |

---

## What AAA Recommends vs. What arifOS Dispatches

| | AAA | arifOS |
|---|---|---|
| Function | Classification + prioritization + recommendation | Governed dispatch + authority |
| Authority | NONE (DISPLAY_ONLY) | FULL (LIMITED_MUTATE / FULL) |
| Output | AttentionPacket | Tool call / mutation |
| Decision | "This deserves attention" | "This action may proceed" |
| Failure mode | Wrong priority (recoverable) | Constitutional breach (888_HOLD) |

> `AAA_route = recommendation` ≠ `arifOS_route = governed dispatch`

---

## Quick Start

```bash
git clone https://github.com/arif-fazil/AAA.git
cd AAA
docker compose up -d

# Verify
curl http://localhost:3001/health
curl http://localhost:4000/health/liveliness

# Generate a sample AttentionPacket
python3 /root/AAA/scripts/attention_plane.py
```

---

## Documentation

- [Full Technical README](docs/README-FULL.md)
- [Federation Architecture](docs/FEDERATION.md)
- [A2A Protocol Spec](docs/A2A_ORGAN_REGISTRY.md)
- [Protocol Conformance](PROTOCOL_CONFORMANCE.md)
- [Agent Card (live)](https://aaa.arif-fazil.com/.well-known/agent-card.json)
- [Deployment Guide](DEPLOYMENT.md)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.

Built by Muhammad Arif bin Fazil.
