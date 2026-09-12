<!-- PROPOSED (PROPOSE_WITH_HOLD) — staged 2026-09-12 by 333-AGI from the ARIF-PERPLEXITY draft for F13 review.
     Content verbatim; markdown formatting reconstructed from the draft; link targets resolved against the repo inventory.
     Not canonical until ratified. Publish path: replace root README.md, commit, push — gated on scoped F13 approval. -->

AAA — Federation Intelligence Routing & State Plane
=====================================================

AAA is the control plane for the arifOS federation. It receives human and agent requests, binds identity and task context, classifies intent, selects permitted routes, and preserves task lineage across federation organs.

**AAA routes. arifOS judges. A-FORGE executes. VAULT999 witnesses.**

AAA is not an AI model, not a constitutional judge, not an execution engine, and not the authoritative audit ledger. It is the layer that helps the federation send the right bounded task to the right organ while preserving identity, provenance, and state.

> **Status:** Active federation control-plane software. A2A protocol conformance and governed A2A execution remain under test-backed verification. See [A2A alignment research](docs/A2A-AAA-ALIGNMENT-RESEARCH-2026-09-12.md) and [SECURITY.md](SECURITY.md).

## What AAA does

AAA provides four bounded control-plane functions:

- **Intent classification** — distinguishes query, analysis, proposal, and execution-request intent.
- **Federation routing** — selects eligible organs using declared capability, local policy, authenticated principal, task context, and federation state.
- **State and registry services** — maintains agent, skill, route, health, and task-correlation information for the federation.
- **A2A gateway boundary** — provides the federation boundary for interoperable agent discovery and task exchange as A2A support is validated.

AAA does not issue constitutional verdicts. Consequential action proposals must be sent to arifOS for judgment before any executor may act.

## Federation boundary

```text
Human or external agent
          │
          │ A2A task, UI request, or internal federation request
          ▼
┌────────────────────────────────────────────────────────────┐
│ AAA — Control Plane                                         │
│                                                            │
│ identity binding · task correlation · intent classification│
│ capability policy · route selection · state observability  │
└─────────────┬──────────────────────────────────────────────┘
              │
     ┌────────┼───────────────────────────────────────┐
     │        │                 │                     │
     ▼        ▼                 ▼                     ▼
   GEOX     WEALTH             WELL                 FRAME
 domain    capital            observation          evidence
 evidence  intelligence       only                 gathering
     │        │                 │                     │
     └────────┴─────────────────┴──────────┬──────────┘
                                             │
                                  consequential proposal?
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ arifOS          │
                                    │ policy judgment │
                                    │ SEAL/HOLD/      │
                                    │ SABAR/VOID      │
                                    └────────┬────────┘
                                             │
                               valid, scoped, unexpired SEAL only
                                             ▼
                                    ┌─────────────────┐
                                    │ A-FORGE         │
                                    │ execution       │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ VAULT999        │
                                    │ receipt chain   │
                                    └─────────────────┘
```

## Division of constitutional labor

| Organ | Federation role | Authority ceiling | Does not do |
|-------|-----------------|-------------------|-------------|
| arifOS | Policy decision point | Evaluates consequential proposals against constitutional policy | Execute real-world mutations |
| AAA | Control plane | Identity binding, route selection, registry, state, A2A boundary | Judge, certify, execute, or author the evidence ledger |
| arifFlow | Metabolic observation | Flow and operational monitoring | Judge or execute |
| A-FORGE | Execution plane | Performs authorized, scoped operations | Adjudicate its own authority |
| GEOX | Earth-science evidence | Domain analysis and evidence | Issue constitutional verdicts |
| WEALTH | Capital intelligence | Financial analysis and evidence | Execute financial actions without valid authorization |
| WELL | Vitality observation | Human and machine observation | Judge or execute |
| FRAME | Independent observation | Drift detection and evidence gathering | Issue authoritative verdicts |
| FED | Model/provider routing | Model access and provider selection | Judge or execute |

## A2A role

A2A is an open protocol for communication between independent agent systems. It provides interoperable concepts for agent discovery, authentication, tasks, messages, artifacts, streaming, and long-running work.

AAA is the federation's A2A-aware control plane. It does not treat an A2A task as execution authority.

```text
A2A task completion ≠ arifOS authorization
A2A authenticated peer ≠ authorized executor
A2A Agent Card claim ≠ local capability permission
```

For consequential work, AAA maintains a correlation chain:

```text
a2a_task_id
  → aaa_session_id
  → aaa_route_receipt_id
  → arifOS_proposal_id
  → arifOS_verdict_id / decision_hash
  → a_forge_lease_id / operation_id
  → vault999_chain_id / receipt_id
```

If a required link is absent, consequential execution must fail closed.

## A2A implementation status

AAA contains A2A-related assets and an Agent Card. This is not, by itself, a public claim of complete protocol conformance.

| Surface | Status |
|---------|--------|
| Agent Card and capability declarations | Present; schema and runtime conformance require pinned test evidence |
| A2A task ingress | Under controlled implementation/verification |
| Task state, context, and correlation model | Under alignment and test-backed verification |
| Streaming and push notification behavior | Must be advertised only when endpoint behavior is tested |
| Governed A2A-to-execution path | Requires valid arifOS judgment and A-FORGE independent verification |

See [A2A alignment research](docs/A2A-AAA-ALIGNMENT-RESEARCH-2026-09-12.md) for the protocol boundary, threat model, and evidence gates.

## Core capabilities

### Intent classification and route selection

AAA classifies a request before selecting an eligible route. It distinguishes at least these control meanings:

| Class | AAA action | Execution authority |
|-------|------------|---------------------|
| Query | Route to permitted read/lookup capability | None |
| Analysis | Route to a domain or reasoning organ | None |
| Draft | Route to bounded content generation or preparation | None |
| Proposal | Canonicalize and submit to arifOS when consequential | No; judgment pending |
| Execution request | Require a valid scoped arifOS SEAL before A-FORGE dispatch | Only A-FORGE may act |

AAA uses deterministic routing where possible and may use model-assisted parsing as an aid. A model output is not authority; it is an input to bounded route policy.

### State, registry, and skills

AAA maintains federation-facing control information, including:

- Agent and capability registry records.
- Skill discovery and composition metadata.
- Route and task correlation context.
- Federation health and operational-state views.
- HOLD and escalation visibility for operators.

State visibility is not equivalent to governance authority. AAA may display a verdict reference but never creates or upgrades a verdict.

### Model/provider routing

AAA may coordinate model/provider routing through the federation's configured routing surfaces. Provider fallback is an availability mechanism, not a reason to weaken identity binding, evidence requirements, task lineage, or arifOS judgment gates.

## Quick start

### Docker

```bash
git clone https://github.com/ariffazil/AAA.git
cd AAA
docker compose up -d

# Verify the AAA service
curl http://localhost:3001/health
```

If your deployment includes the configured model-routing service, check its documented health endpoint separately. Do not expose internal service endpoints publicly without an explicit deployment policy.

### Local development

```bash
npm ci
npm run dev
```

Run the repository-defined test, build, and validation commands before treating a local instance as a federation control-plane candidate.

## Security model

AAA applies a separation-of-authority model:

```text
DISCOVERED ≠ AUTHENTICATED ≠ TRUSTED ≠ AUTHORIZED ≠ JUDGED ≠ EXECUTABLE
```

Discovery metadata does not grant access.

Authentication does not grant authority.

A remote agent's claimed capability is intersected with AAA local route policy.

A task result or A2A COMPLETED state does not authorize execution.

AAA cannot turn HOLD, SABAR, or VOID into a dispatch.

A-FORGE must independently reject missing, forged, expired, replayed, or scope-mismatched authorization.

Security design and responsible disclosure are documented in [SECURITY.md](SECURITY.md).

## Documentation

- [Full technical README](docs/README-FULL.md)
- [Federation architecture](FEDERATION.md)
- [A2A alignment research and evidence gates](docs/A2A-AAA-ALIGNMENT-RESEARCH-2026-09-12.md)
- [A2A organ registry](docs/A2A_ORGAN_REGISTRY.md)
- [Deployment guide](DEPLOYMENT.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Repository taxonomy

AAA is part of the arifOS federation. The federation separates runtime, governance infrastructure, interfaces, infrastructure attachments, and archives so that historical or auxiliary repositories do not silently acquire runtime authority.

For the current repository map and authority boundaries, see [Federation architecture](FEDERATION.md).

## License

AAA is licensed under the GNU Affero General Public License v3.0. See [LICENSE](LICENSE).

When the software is modified and made available for use over a network, AGPL-3.0 obligations may require making corresponding source available to network users. Refer to the license text and obtain legal advice for your deployment where needed.

---

Built by Muhammad Arif bin Fazil.

DITEMPA BUKAN DIBERI — Forged, Not Given.
