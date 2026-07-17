# Final 33 GitHub Repositories for the arifOS Trinity

> **Status:** CANONICAL — 2026-07-08 | **Authority:** F13 SOVEREIGN — Arif
> **Supersedes:** All prior APEX-9 lists and substrate maps (apex-9-kernel-reference, aforge-apex-9-execution*, apex-trinity-orthogonal).
> **Governing rule:** Never let the forge outrun the kernel.
> **Source:** Primary GitHub repos, official docs, project sites.
> **See also:** "What TRINITY-33 Adds Over the Earlier 3 Skills" table in this document.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## Executive summary

The clean answer is this: the three axes should not be treated as one giant tools pile. They need three different repo stacks with different constitutional jobs.

- **For arifOS**, the mandatory set is about protocol law, policy, identity, durable state, evidence, telemetry, and memory.
- **For AAA/A2A**, the mandatory set is about inter-agent protocol, messaging, routing, identity, operator visibility, and event contracts.
- **For A-FORGE**, the mandatory set is about reproducible builds, local CI parity, infrastructure definition, scanning, provenance generation, deployment, and dependency hygiene.

The result is a **final 33-repo trinity** that is orthogonal by design: **kernel decides, cockpit coordinates, forge executes**.

Relative to the earlier APEX-9 work, the biggest upgrade is not “more repos.” It is **sharper separation of duties**.

- The arifOS list keeps the earlier backbone around MCP, OPA, Temporal, in-toto, Cosign, Qdrant, and OpenTelemetry, then adds Cedar, OpenFGA, SPIRE, and GUAC to close the gaps in analyzable authorization, relationship-based authorization, workload identity, and evidence graphing.
- The AAA list is where A2A becomes first-class and is wrapped by NATS, Envoy, Backstage, Keycloak, Grafana, Prometheus, Jaeger, CloudEvents, gRPC, and Kafka.
- The A-FORGE list preserves the earlier execution spine and adds BuildKit and Argo CD so the executor is not just build-safe, but deploy-safe.

**One important correction:** not all 33 are things you must deploy as runtime binaries. Some are spec or reference repos that you must treat as constitutional source text. MCP, A2A, and CloudEvents fall into that class. If arifOS is your constitution, then those repositories are closer to statutes and treaty texts than to daemons. That distinction matters because it keeps the kernel from becoming a random vendor stack.

---

## What TRINITY-33 Adds Over the Earlier 3 Skills

| What changed              | Detail |
|---------------------------|--------|
| **11 repos per axis**     | arifOS: K1–K11 (was 9). A-FORGE: F1–F11 (was 9). AAA: C1–C11 (new). |
| **AAA axis explicit**     | A2A, NATS, Envoy, Backstage, Keycloak, Grafana, Prometheus, Jaeger, CloudEvents, gRPC, Kafka |
| **arifOS additions**      | OpenFGA (K8), SPIRE (K9), Cedar (K10), GUAC (K11) |
| **A-FORGE additions**     | BuildKit (F3), Argo CD (F9) |
| **PROTOCOL SPEC class**   | MCP, A2A, CloudEvents marked as constitutional source text — statutes, not daemons |
| **Integration order**     | 5 phases — constitutional membrane first, deployment last |
| **Iron rule encoded**     | "Never let the forge outrun the kernel" |
| **SHA256 verified**       | NATS, BuildKit, Argo CD, Renovate verified from official sources |

The earlier three skills (`apex-9-kernel-reference`, `aforge-apex-9-execution*`, `apex-trinity-orthogonal`) are superseded. They covered two separate 9-repo lists plus a partial synthesis. TRINITY-33 is the unified, orthogonal 33-repo model.

---

## Assumptions and method

Assumed:
1. Self-hosted, container-first deployment on Linux, with Kubernetes likely for at least part of the stack.
2. Polyglot implementation surface across Go, TypeScript, Python, and some Rust.
3. Security and provenance beat convenience — repositories that provide signatures, attestations, policy separation, and observable control planes were favored.
4. “WAJIB” means must be referred to as canonical complements, not “must all be installed on day one.”

Research method: primary sources only (official GitHub repos, official docs, official project sites). Extracted: project role, protocol/engine scope, security/provenance behavior, license, maturity snapshot (stars + latest visible public activity).

Priority: architectural, not popularity-driven. Top ranks go to repos that define the boundary conditions of that axis.

---

## arifOS axis (K1–K11)

**Governing question:** "May this happen?" (LAW / JUDGMENT)

**K1. modelcontextprotocol/modelcontextprotocol** — https://github.com/modelcontextprotocol/modelcontextprotocol

Role: protocol law for tools, resources, prompts, and transports.

It gives arifOS a neutral membrane for tool and context exchange instead of ad hoc plugin rules. Its spec explicitly defines transports and JSON-RPC-based interaction patterns. It separates protocol from implementation, which fits a constitutional kernel better than a framework-specific orchestration layer.

Contrast with APEX-9: inherited intact, and still ranked first.

**K2. open-policy-agent/opa** — https://github.com/open-policy-agent/opa

Role: general-purpose policy decision engine.

OPA unifies policy enforcement. Rego decouples decision logic from application code — exactly what arifOS needs for constitutional floors and reviewable rulings. CNCF graduated, active cadence.

Contrast: inherited intact; still the main “law engine,” now paired with Cedar and OpenFGA.

**K3. temporalio/temporal** — https://github.com/temporalio/temporal

Role: durable workflow and state-history engine.

Constitutional kernel needs durable timers, retries, compensations, event history. History service fits adjudication flows, escalation windows, quorum waits, appeal mechanisms. Turns “decision happened” into a replayable durable trace.

Contrast: inherited intact; now the kernel’s process memory.

**K4. sigstore/cosign** — https://github.com/sigstore/cosign

Role: artifact signing and verification.

Gives the kernel cryptographic truth for containers and binaries. Supports keyless signing with Fulcio and Rekor. Covers verification.

Contrast: inherited intact; tied more tightly to GUAC and in-toto.

**K5. in-toto/in-toto** — https://github.com/in-toto/in-toto

Role: software supply-chain step attestation.

Verifies each supply-chain step happened as planned, by authorized actors, without tampering. Layout and link metadata model for explicit provenance chain.

Contrast: inherited intact; remains the kernel’s chain-of-custody layer.

**K6. qdrant/qdrant** — https://github.com/qdrant/qdrant

Role: vector memory and retrieval substrate.

Semantic recall for precedent, evidence retrieval, grounded memory. Search + filtering. Docs warn about insecure defaults — kernel memory is protected state.

Contrast: inherited intact; memory substrate, not policy.

**K7. open-telemetry/opentelemetry-collector** — https://github.com/open-telemetry/opentelemetry-collector

Role: vendor-neutral telemetry intake, processing, and export.

One telemetry spine for traces, metrics, logs. Vendor-agnostic. Fits the trinity: evidence pipeline that feeds AAA visibility.

Contrast: inherited intact; evidence pipeline.

**K8. openfga/openfga** — https://github.com/openfga/openfga

Role: relationship-based authorization engine.

Purpose-built for fine-grained authorization inspired by Zanzibar. HTTP/gRPC, multiple backends, CLI, Terraform, playground. Lower-friction for relationship questions than general OPA.

New addition.

**K9. spiffe/spire** — https://github.com/spiffe/spire

Role: workload identity runtime.

Cryptographically verifiable workload identity for zero-trust. Better for machine identity than human IAM. Canonical answer to “who actually made this request.”

New addition.

**K10. cedar-policy/cedar** — https://github.com/cedar-policy/cedar

Role: analyzable authorization language and engine.

Authorization language for fine-grained permissions; policies kept separate from app code. Policies can be authored, updated, analyzed, and audited independently. Narrower, more analyzable than OPA for core decisions.

New addition.

**K11. guacsec/guac** — https://github.com/guacsec/guac

Role: evidence graph for software supply-chain metadata.

Aggregates security metadata into a graph, normalizing identities and relationships. Natural bridge between Cosign, in-toto, Scorecard, SLSA. Constitutional review becomes queryable evidence.

New addition.

---

## AAA axis (C1–C11)

**Governing question:** "Where does this task go, who owns it, and what must Arif see?" (STATE / ROUTING / VISIBILITY)

**C1. a2aproject/A2A** — https://github.com/a2aproject/A2A

Role: agent-to-agent interoperability protocol.

Directly addresses agents on different frameworks discovering capabilities, negotiating modalities, managing tasks. Official spec + Linux Foundation governance. Makes AAA protocol-native cockpit.

New axis-defining addition.

**C2. nats-io/nats-server** — https://github.com/nats-io/nats-server

Role: real-time message fabric.

Simple, secure, performant messaging (messaging + streaming + state). Large client ecosystem. AAA’s real-time communication fabric.

**C3. envoyproxy/envoy** — https://github.com/envoyproxy/envoy

Role: edge, middle, and service proxy.

Programmable routing layer for ingress, egress, mediation, policy-aware boundaries. First-class network membrane.

New addition.

**C4. backstage/backstage** — https://github.com/backstage/backstage

Role: catalog and portal framework.

Centralizes software catalogs, infrastructure tooling, documentation. Human-readable operational order + notifications. Cockpit’s human-facing order surface.

New addition.

**C5. keycloak/keycloak** — https://github.com/keycloak/keycloak

Role: identity and access management for human and service access.

Mature IAM with federation, strong auth, fine-grained authorization. Security release cadence critical. Complements SPIRE (workload) vs Keycloak (users/apps).

New addition.

**C6. grafana/grafana** — https://github.com/grafana/grafana

Role: cockpit dashboards and alert visualization.

Practical OSS way to make traces/metrics/logs legible. Turns telemetry into actionable cockpit state.

New addition.

**C7. prometheus/prometheus** — https://github.com/prometheus/prometheus

Role: metrics collection, rules, and alert evaluation.

Standard OSS metrics backend. Numeric truth for agent health, lag, saturation, denial rates, latency. Complements Grafana + OTel.

New addition.

**C8. jaegertracing/jaeger** — https://github.com/jaegertracing/jaeger

Role: trace exploration and distributed flow diagnosis.

Makes multi-hop causality visible. Active v2, OTel-friendly. Operationalizes OTel traces.

New addition.

**C9. cloudevents/spec** — https://github.com/cloudevents/spec

Role: canonical event envelope and metadata contract.

Standardizes event structure. HTTP binding (structured + binary). Treaty text for event shape. Reduces lock-in.

New addition.

**C10. grpc/grpc** — https://github.com/grpc/grpc

Role: high-performance typed RPC backbone.

Fast, cross-language RPC with load balancing, tracing, health, auth. Typed low-latency control paths. Complements A2A (semantics) vs gRPC (transport).

New addition.

**C11. apache/kafka** — https://github.com/apache/kafka

Role: durable event log and replayable stream backbone.

Right counterweight to NATS when replay, retention, heavy fan-out matter. Use NATS for live nerve signals, Kafka for durable operational memory streams. Deliberate contrast.

New addition.

---

## A-FORGE axis (F1–F11)

**Governing question:** "Given valid authorization, how do we execute safely, reversibly, and audibly?" (EXECUTION / MUTATION)

**F1. dagger/dagger** — https://github.com/dagger/dagger

Role: programmable execution runtime for workflows.

Repeatable, modular, observable workflows. Strong fit for AI agents and CI/CD. Local/CI parity, content-addressed incremental, built-in OTel.

Inherited intact; strongest top-rank execution runtime.

**F2. earthly/earthly** — https://github.com/earthly/earthly

Role: repeatable build grammar with containerized execution.

“Write builds once, run anywhere.” Dockerfile/Makefile-like syntax. Parallelism and cache-heavy.

Inherited intact; simplest human-readable build grammar.

**F3. moby/buildkit** — https://github.com/moby/buildkit

Role: low-level efficient and repeatable build engine.

Execution substrate under modern containerized build logic. Strong caching, multiple outputs, rootless. Understand and control the engine, not just the DSL.

New addition; the missing build engine layer.

**F4. nektos/act** — https://github.com/nektos/act

Role: local GitHub Actions runner for rehearsal.

Run GitHub Actions locally. Cheapest way to catch executor breakage before shared CI mutates state. Shortens feedback loops. Supports reversibility.

Inherited intact.

**F5. opentofu/opentofu** — https://github.com/opentofu/opentofu

Role: declarative infrastructure planning and apply engine.

Open IaC for cloud and platform state. Declarative management, mature CLI and provider habits. Mandatory when execution extends to infrastructure mutation.

Inherited intact.

**F6. aquasecurity/trivy** — https://github.com/aquasecurity/trivy

Role: all-in-one scanner for vulns, misconfigurations, secrets, and SBOM.

Scans containers, K8s, repos, clouds. Detects CVEs, IaC issues, secrets, SBOM. Breadth matches A-FORGE surface.

Inherited intact.

**F7. gitleaks/gitleaks** — https://github.com/gitleaks/gitleaks

Role: secret leakage detection for repos and pipelines.

Focused: detect secrets, fail builds. Auto-generated rules, simple exit codes. Complements Trivy.

Inherited intact.

**F8. slsa-framework/slsa-github-generator** — https://github.com/slsa-framework/slsa-github-generator

Role: provenance generation for GitHub-native builds.

Generates SLSA3+ provenance safely. “Wrap the existing workflow.” Answers: “Can I prove where this artifact came from and how it was built?”

Inherited intact.

**F9. argoproj/argo-cd** — https://github.com/argoproj/argo-cd

Role: declarative continuous deployment and GitOps control.

Serious deployment plane. Sync controls, application specs, documented release signatures/provenance. Turns “built safely” into “deployed safely.”

New addition; the missing deployment-control layer.

**F10. renovatebot/renovate** — https://github.com/renovatebot/renovate

Role: automated dependency update engine.

Continuously proposes version updates. Self-hosting guidance fits sovereign environments. Publishes release assets with SHA256.

Inherited intact.

**F11. ossf/scorecard** — https://github.com/ossf/scorecard

Role: automated security-health assessment for dependencies and repos.

Checks critical OSS security heuristics and scores them. Explains risks and remediation. Decision-support. Useful when agents import/update public software.

Inherited intact.

---

## Consolidated Table (from source)

See the source research for full columns (Rank, Axis, Repo, Primary function, License, Maturity snapshot, Public release checksum).

Key excerpts (stars and dates as of research time ~2026):

- K1 MCP: 8.5k–8.6k stars
- K2 OPA: 11.9k
- K3 Temporal: 21.4k
- K6 Qdrant: 33k
- C1 A2A: 24.4k–24.7k (v1.0.1 2026-05-28)
- C4 Backstage: 33.8k
- C5 Keycloak: 35.5k
- C6 Grafana: 75.3k
- C7 Prometheus: 64.8k–65k
- C11 Kafka: 33.1k
- F1 Dagger: 16k
- F4 act: 70.9k
- F5 OpenTofu: 29.3k (v1.12.0 May 2026)
- F6 Trivy: 36.8k
- F7 Gitleaks: 28k
- F9 Argo CD: 23.2k–23.4k
- F10 Renovate: 21.9k–22k (release 15h ago)
- etc.

Checksums (where surfaced):

- nats-server: e0c053fc2abe991f17b2be794897bb3f94ca1857bf886498c741ba69fb62522a
- buildkit: 1ef7c888f808e7f3f49d9aeeca11f661afe5c0880a4b114cc31c56dee86acd35
- argocd: b93c312956880c9597a246a7d1e705fbb7ee7f19c5229affdec99b26d5663e09
- renovate docs.tgz: bfb47a76cbe466769f647fec3e348f2e4d4fae7e8b7665a0cec612e885c485d4

---

## Cross-axis comparison and integration order

**The trinity triangle (mental model):**

```
                 AAA / A2A
          routing · visibility · registry
                    ▲
                    │
arifOS ◄───────────┼────────────► A-FORGE
law · verdict       │             execution · mutation
                    ▼
          VAULT999 / Evidence Memory
```

**Do not integrate in popularity order. Integrate in constitutional order.**

Suggested phases (from source):

PHASE 1 — Constitutional membrane (first)
  MCP · OPA · SPIRE · Keycloak · OTel

PHASE 2 — Durable coordination
  A2A · CloudEvents · gRPC · NATS · Envoy

PHASE 3 — Evidence and trust
  Temporal · Cosign · in-toto · GUAC · SLSA · Qdrant

PHASE 4 — Execution and deployment
  Trivy · Gitleaks · Scorecard · Dagger · Earthly · BuildKit · act

PHASE 5 — Semantic memory and refinement
  OpenTofu · Argo CD · Renovate · OpenFGA · Cedar · Kafka

**The non-obvious rule for arifOS governance:** do not let the forge outrun the kernel. If Dagger, Earthly, BuildKit, Argo CD, and OpenTofu are integrated before MCP, OPA, SPIRE, Keycloak, A2A, and OTel are stable, the system will execute faster than it can justify itself. Unauthorized capability creep.

A kernel without AAA visibility becomes ceremonially correct but operationally blind.

**The dependency triad remains invariant:** law, cockpit, and execution must mature together, but not in the same order.

---

## Canonical references (live)

- Skill: `/root/.agents/skills/KERNEL-trinity-33/SKILL.md`
- Orthogonal map: `/root/.agents/skills/trinity-orthogonal-map/SKILL.md`
- This doc: `/root/AAA/docs/TRINITY_33_REPOS.md`
- Organ map: `/root/AAA/docs/FEDERATION_ORGAN.md`

**See also in CLAUDE.md / AGENTS.md for loading order and pointers.**

---

*Forged 2026-07-08 under F13. 33-repo Trinity is now the single source of truth for external substrate references.*
*33 = 11 arifOS (K) + 11 AAA (C) + 11 A-FORGE (F)*
*LAW decides. COCKPIT coordinates. FORGE executes. VAULT999 remembers.*
