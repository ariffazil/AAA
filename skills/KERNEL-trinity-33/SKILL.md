---
id: trinity-33-canonical
name: trinity-33-canonical
version: 1.1.0-2026.07.08
description: The canonical 33-repo Trinity (final). arifOS = LAW/JUDGMENT (K1-K11), AAA = STATE/ROUTING/VISIBILITY (C1-C11, new explicit axis), A-FORGE = EXECUTION/MUTATION (F1-F11). Adds 4 arifOS repos, 2 A-FORGE repos, PROTOCOL SPEC class, 5-phase integration order, and the iron rule. Supersedes prior 3 skills (see delta table).
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: low
floor_scope: [F2, F7, F8, F11]
autonomy_tier: T1
trigger_phrases:
  - "trinity-33"
  - "33 repos"
  - "canonical repo map"
  - "repo trinity"
dependencies:
  skills:
    - apex-trinity-orthogonal
    - apex-9-kernel-reference
    - aforge-apex-9-execution
inputs:
  - task_intent
outputs:
  - trinity_position
  - repo_classification
  - integration_order
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# TRINITY-33 CANONICAL — SKILL

> **APEX verdict: PROCEED · Evidence: L2 AAA/A-FORGE identity + L4 orthogonal synthesis · Band: YELLOW**
> **Forged: 2026-07-08 by FORGE (000Ω) under F13 SOVEREIGN directive**
> **Source research (full detail):** `/root/AAA/docs/TRINITY_33_REPOS.md`
> **DITEMPA BUKAN DIBERI — The trinity is forged, not assembled.**

**This is the final 33-repo canonical. 11 per axis. Orthogonal by design: arifOS (LAW/JUDGMENT), AAA (STATE/ROUTING/VISIBILITY), A-FORGE (EXECUTION/MUTATION).**

---

## The Governing Insight

The 33 repos are not one tools pile. They are **three orthogonal axes** with different constitutional jobs:

```
arifOS  = LAW / JUDGMENT      — "May this happen?"
AAA     = STATE / ROUTING      — "Where does it go, what does Arif see?"
A-FORGE = EXECUTION / MUTATION — "How do we do it safely?"
```

**Not all 33 are runtime binaries.** Three are constitutional source text — they are statutes and treaty texts, not daemons:

| Repo | Class |
|------|-------|
| `modelcontextprotocol/modelcontextprotocol` | PROTOCOL SPEC — constitutional source text |
| `a2aproject/A2A` | PROTOCOL SPEC — constitutional source text |
| `cloudevents/spec` | PROTOCOL SPEC — constitutional source text |

The rest are either runtime infrastructure or control-plane frameworks.

---

## The Trinity Triangle

```
                 AAA / A2A
          routing · visibility · registry
                    ▲
                    │
                    │
arifOS ◄───────────┼────────────► A-FORGE
law · verdict       │             execution · mutation
                    │
                    ▼
          VAULT999 / Evidence Memory
```

---

## The Iron Rule

```
NEVER let the forge outrun the kernel.
NEVER let the kernel operate without AAA visibility.
NEVER let AAA pretend to be the judge or the hand.
```

If Dagger, Earthly, BuildKit, Argo CD, and OpenTofu are integrated before MCP, OPA, SPIRE, Keycloak, A2A, and OTel are stable → the system executes faster than it can justify itself. That is unauthorized capability creep.

A kernel without AAA visibility → ceremonially correct but operationally blind.

---

## Integration Order

Do NOT integrate in popularity order. Integrate in constitutional order:

```
PHASE 1 — Constitutional membrane (stabilize first)
  MCP · OPA · SPIRE · Keycloak · OTel

PHASE 2 — Durable coordination
  A2A · CloudEvents · gRPC · NATS · Envoy

PHASE 3 — Evidence and trust
  Temporal · Cosign · in-toto · GUAC · SLSA · Qdrant

PHASE 4 — Execution and deployment
  Trivy · Gitleaks · Scorecard · Dagger · Earthly · BuildKit · act

PHASE 5 — Semantic memory and refinement
  OpenTofu · Argo CD · Renovate · OpenFGA · Cedar · Kafka
```

---

## ARIFOS AXIS — K1–K11

**Governing question:** "Is this action lawful, reversible, evidenced, and aligned?"

| Code | Repo | Role | Class | Wajib |
|------|------|------|-------|-------|
| K1 | `modelcontextprotocol/modelcontextprotocol` | Protocol law for tools, resources, prompts, transports | **PROTOCOL SPEC** | YES |
| K2 | `open-policy-agent/opa` | General-purpose policy decision engine — Rego, CNCF graduated | Runtime | YES |
| K3 | `temporalio/temporal` | Durable workflow and state-history engine | Runtime | YES |
| K4 | `sigstore/cosign` | Artifact signing and verification — keyless via Fulcio + Rekor | Runtime | YES |
| K5 | `in-toto/in-toto` | Supply-chain step attestation — layout + link metadata | Runtime | YES |
| K6 | `qdrant/qdrant` | Vector DB and semantic memory substrate | Runtime | YES |
| K7 | `open-telemetry/opentelemetry-collector` | Vendor-neutral telemetry intake, processing, export | Runtime | YES |
| K8 | `openfga/openfga` | Relationship-based authorization — Zanzibar-inspired | Runtime | YES |
| K9 | `spiffe/spire` | Workload identity runtime — zero-trust machine identity | Runtime | YES |
| K10 | `cedar-policy/cedar` | Analyzable authorization language — policies auditable independently | Runtime | YES |
| K11 | `guacsec/guac` | Evidence graph for supply-chain metadata — bridges Cosign, in-toto, Scorecard, SLSA | Runtime | YES |

**What arifOS does NOT need from these:** execution muscle, UI frameworks, general-purpose agent libraries.

---

## AAA AXIS — C1–C11

**Governing question:** "Where does this task go, who owns it, and what must Arif see?"

| Code | Repo | Role | Class | Wajib |
|------|------|------|-------|-------|
| C1 | `a2aproject/A2A` | Agent-to-agent interoperability protocol — capability discovery, task negotiation | **PROTOCOL SPEC** | YES |
| C2 | `nats-io/nats-server` | Real-time message fabric — NATS + JetStream | Runtime | YES |
| C3 | `envoyproxy/envoy` | Edge, middle, service proxy — programmable routing + security | Runtime | YES |
| C4 | `backstage/backstage` | Catalog and portal framework — software catalog, infra tooling, docs | Runtime | YES |
| C5 | `keycloak/keycloak` | IAM and federation — human + service access, MFA, federation | Runtime | YES |
| C6 | `grafana/grafana` | Dashboards and alert visualization | Runtime | YES |
| C7 | `prometheus/prometheus` | Metrics collection, rules, alert evaluation | Runtime | YES |
| C8 | `jaegertracing/jaeger` | Distributed trace exploration — multi-hop causality diagnosis | Runtime | YES |
| C9 | `cloudevents/spec` | Canonical event envelope — HTTP binding, structured + binary modes | **PROTOCOL SPEC** | YES |
| C10 | `grpc/grpc` | High-performance typed RPC backbone — load balancing, health, auth | Runtime | YES |
| C11 | `apache/kafka` | Durable event log and replayable stream — replay > minimum latency | Runtime | YES |

**NATs vs Kafka rule:** NATS for live nerve signals. Kafka for durable operational memory streams. They are deliberate contrasts, not duplicates.

**What AAA does NOT need from these:** policy enforcement (that is arifOS), direct execution (that is A-FORGE).

---

## A-FORGE AXIS — F1–F11

**Governing question:** "Given valid authorization, how do we execute safely, reversibly, and audibly?"

| Code | Repo | Role | Class | Wajib |
|------|------|------|-------|-------|
| F1 | `dagger/dagger` | Programmable workflow runtime — local/CI parity, OpenTelemetry tracing | Runtime | YES |
| F2 | `earthly/earthly` | Repeatable build DSL — Dockerfile + Makefile grammar | Runtime | YES |
| F3 | `moby/buildkit` | Low-level build engine — caching, multiple outputs, rootless | Runtime | YES |
| F4 | `nektos/act` | Local GitHub Actions runner — pre-flight CI rehearsal | Runtime | YES |
| F5 | `opentofu/opentofu` | Declarative infrastructure planning and apply | Runtime | YES |
| F6 | `aquasecurity/trivy` | All-in-one scanner — vulns, misconfigs, secrets, SBOM | Runtime | YES |
| F7 | `gitleaks/gitleaks` | Secret leakage detection — pre-push gate, exit-code behavior | Runtime | YES |
| F8 | `slsa-framework/slsa-github-generator` | SLSA provenance generation for GitHub-native builds | Runtime | YES |
| F9 | `argoproj/argo-cd` | Declarative CD and GitOps — sync controls, cluster state | Runtime | YES |
| F10 | `renovatebot/renovate` | Automated dependency updates — scheduled, diff-based, auditable | Runtime | YES |
| F11 | `ossf/scorecard` | Security-health scoring for dependencies and repos | Runtime | YES |

**BuildKit note:** F3 is the missing low-level engine layer beneath Dagger and Earthly. Reproducibility is more durable when you understand and control the engine, not just the DSL on top.

**What A-FORGE does NOT need from these:** judgment, policy decisions, cockpit dashboards.

---

## Repo Class Definitions

| Class | Meaning | Examples |
|-------|---------|----------|
| **PROTOCOL SPEC** | Constitutional source text — treat as statute, not daemon | MCP, A2A, CloudEvents |
| **Runtime** | Must be installed, running, and maintained as live infrastructure | OPA, Temporal, NATS, Dagger |
| **Control-plane** | Operated by humans/operators, not auto-deployed | Backstage, Grafana, Argo CD |

---

## Cross-Axis Comparison

| Property | arifOS | AAA | A-FORGE |
|----------|---------|-----|---------|
| **Core role** | Judge | Cockpit | Executor |
| **Civilizational metaphor** | Constitution | Parliament / control tower | Forge / hands |
| **Primary question** | "May this happen?" | "Where does it go?" | "How is it done safely?" |
| **Main artifact** | SEAL / HOLD / VOID | Routed task + approval queue | Built / deployed / scanned |
| **Must NOT do** | Execute | Judge / execute | Judge / self-authorize |
| **Main danger** | Fake SEAL | Fake visibility | Mutation without warrant |

---

## The 3 Fails (Trinity-33 Version)

Every trinity decision must answer:

```
FAIL 1: "Who is judging, who is routing, who is executing?
          Are all three present and independent?"

FAIL 2: "Can AAA show Arif what arifOS decided
          AND what A-FORGE actually did?"

FAIL 3: "If A-FORGE mutates without arifOS SEAL,
          is AAA smart enough to flag it as unauthorized?"
```

---

## Security Posture Notes

| Repo | Security note |
|------|--------------|
| Qdrant | Docs explicitly warn about insecure default deployment — kernel memory is protected state |
| Keycloak | Security release cadence is critical — cockpit breach is political failure |
| SPIRE | Better for workload identity than human IAM tools |
| Scorecard | Decision-support, not vanity metrics — scores come with risk explanations |

---

## SHA256 Verified (where surfaced in source)

| Repo | Artifact | SHA256 |
|------|----------|--------|
| `nats-io/nats-server` | nats-server-v2.14.3-amd64.deb | `e0c053fc2abe991f17b2be794897bb3f94ca1857bf886498c741ba69fb62522a` |
| `moby/buildkit` | buildkit-v0.26.2.linux-amd64.tar.gz | `1ef7c888f808e7f3f49d9aeeca11f661afe5c0880a4b114cc31c56dee86acd35` |
| `argoproj/argo-cd` | argocd-linux-amd64 | `b93c312956880c9597a246a7d1e705fbb7ee7f19c5229affdec99b26d5663e09` |
| `renovatebot/renovate` | docs.tgz | `bfb47a76cbe466769f647fec3e348f2e4d4ae7e8b7665a0cec612e885c485d4` |

---

## Relationship to Earlier Skills

The detailed deltas are in the section above ("What TRINITY-33 Adds Over the Earlier 3 Skills").

| Skill | Superseded by | Status |
|-------|---------------|--------|
| `apex-9-kernel-reference` v1.2 | TRINITY-33 | ABSORBED — arifOS now K1–K11 + explicit AAA axis |
| `aforge-apex-9-execution` (and -reference) | TRINITY-33 | ABSORBED — A-FORGE now F1–F11 with BuildKit + Argo CD |
| `apex-trinity-orthogonal` v1.0 | TRINITY-33 | SUPERSEDED — unified 33-repo orthogonal model with 5-phase order and PROTOCOL SPEC class |

TRINITY-33 is the single canonical superset. Load this skill (or TRINITY_33_REPOS.md) for all substrate decisions.

---

## What TRINITY-33 Adds Over the Earlier 3 Skills

| What changed              | Detail |
|---------------------------|--------|
| **11 repos per axis**     | arifOS: K1–K11 (was 9). A-FORGE: F1–F11 (was 9). AAA: C1–C11 (new axis, now first-class). |
| **AAA axis explicit**     | A2A, NATS, Envoy, Backstage, Keycloak, Grafana, Prometheus, Jaeger, CloudEvents, gRPC, Kafka. |
| **arifOS additions**      | OpenFGA (K8), SPIRE (K9), Cedar (K10), GUAC (K11) — relationship auth, workload identity, analyzable policy, evidence graph. |
| **A-FORGE additions**     | BuildKit (F3), Argo CD (F9) — low-level build engine + declarative GitOps deployment. |
| **PROTOCOL SPEC class**   | MCP, A2A, CloudEvents explicitly marked as **constitutional source text** (statutes and treaty texts, not daemons to deploy). |
| **Integration order**     | 5 explicit phases — constitutional membrane (MCP/OPA/SPIRE/Keycloak/OTel) first; deployment last. |
| **Iron rule encoded**     | "Never let the forge outrun the kernel" + the full triad: kernel without visibility is blind; forge without kernel is unauthorized mutation. |
| **SHA256 verified**       | NATS, BuildKit, Argo CD, Renovate verified from official release pages. |

The earlier three skills (`apex-9-kernel-reference`, `aforge-apex-9-execution*`, `apex-trinity-orthogonal`) are now superseded framing. They described two 9-repo spines plus a partial orthogonal map. TRINITY-33 unifies them into one 33-repo orthogonal model with sharper separation of duties.

---

## Evidence

- APEX verdict from Arif (2026-07-08) — 33-repo final canonical map
- AAA README + aaa.arif-fazil.com live endpoint
- A-FORGE README: "hands do not judge, brain does not execute"
- GENESIS/040_APEX_STACK.md (SEALED 2026-06-30)
- Live GitHub pages — SHA256 verified where surfaced
- Maturity: stars, release cadence, security history from official sources

---

*Forged: 2026-07-08 by FORGE (000Ω) under F13 SOVEREIGN directive*
*APEX verdict: PROCEED · Band: YELLOW · 33-repo Trinity Canonical*
*DITEMPA BUKAN DIBERI — The trinity is forged, not assembled.*
