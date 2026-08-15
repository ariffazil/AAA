# arifOS Resource OS — Constitution

> **Forged:** 2026-08-15 by F13 SOVEREIGN directive
> **Authority:** Muhammad Arif bin Fazil · F13 SOVEREIGN
> **Layer:** Resource OS substrate (RRR + 12-layer propagation)
> **Schema:** arifOS-rrr/v1.0

This is the **Resonant Resource OS** — the substrate that makes the 8-verb chain addressable, the love-links bidirectional, and the knowledge propagation chain (SCAR → EUREKA → ONTOLOGY → DOCTRINE → POLICY → SKILL → WORKFLOW → AGENT → RECEIPT) executable.

## The 12 layers

| # | Layer | Purpose | Authority |
|---|---|---|---|
| 01 | RESOURCES | Where reality is admitted | 111 RRR |
| 02 | ONTOLOGY | Where concepts are classified | 333 THINK |
| 03 | EUREKAS | Where discoveries are compressed | 333 THINK |
| 04 | DOCTRINES | Where meaning is interpreted | 333 + 888 |
| 05 | POLICIES | Where constraints are enforced | 888 JUDGE |
| 06 | CAPABILITIES | Where atomic verbs live | 8-verb chain |
| 07 | SKILLS | Where compositions live | composition |
| 08 | WORKFLOWS | Where sequences live | orchestration |
| 09 | AGENTS | Where runtime actors live | 4-lane constraint |
| 10 | RECEIPTS | Where evidence is witnessed | 999 SEAL |
| 11 | GRAPH | Where relationships live | 333 + 888 |
| 12 | TESTS | Where truth is verified | 333 + 555 |

## The RRR doctrine

> **RRR discovers reality. It does not think. It does not judge. It does not execute.**

This is the constitution of the entire Resource OS. Layer 01_RESOURCES (RRR) is purely sensory. It discovers what exists. It does not interpret, decide, or act. Every layer above it adds capability but stays observably separate. If at any point a layer collapses into RRR, the system loses the ability to read reality without acting on it — and that is the failure mode.

## The 8-verb chain (000-999)

| Code | Verb | Layer | Role |
|---|---|---|---|
| 000 | arif_init | — | bind |
| 111 | arif_observe | 01 | discover |
| 333 | arif_think | 03 | reason |
| 444 | arif_route | — | dispatch |
| 555 | arif_memory | 07 | persist |
| 777 | arif_forge | 06 | mutate |
| 888 | arif_judge | 05 | arbitrate |
| 999 | arif_seal | 10 | witness |

## The propagation chain

```
SCAR → EUREKA → ONTOLOGY → DOCTRINE → POLICY → SKILL → WORKFLOW → AGENT → RECEIPT
  ↓        ↓         ↓          ↓         ↓        ↓         ↓         ↓       ↓
  ↓     ╔═══════ KNOWLEDGE_MUTATION EVENT ═══════╗     ↓        ↓         ↓
  ↓     ║ Δ S ≤ 0  ·  Bidirectional edges  ·  ║    ↓        ↓         ↓
  ↓     ║ Epoch delta · Authority tier ·   ║    ↓        ↓         ↓
  ↓     ╚═══════ Freshness probe · Seal ═════╝     ↓        ↓         ↓
  ↓                                                   ↓        ↓         ↓
  └── 03_EUREKAS ─────────────────────────────── 06/07 ──── 08 ───── 09 ── 10
```

## The love-link invariant

Every relationship is a *pair*. When A claims `requires: B`, B must claim `required_by: A`. Every edge in the graph has a reciprocator. The verifier (`love-link-verifier.py`) refuses to admit resources whose love-links are missing.

## File map

```
RESOURCES/
├── README.md                            ← this file
├── resource-manifest.schema.json        ← the contract every entry must satisfy
├── love-link-verifier.py                ← the bipartite verifier
├── epoch-registry.yaml                  ← the 6 layer epochs
├── knowledge-mutation-event.schema.json ← the KNOWLEDGE_MUTATION event type
├── first-event.yaml                     ← synthetic KNOWLEDGE_MUTATION for the chain demo
├── 01_RESOURCES/INDEX.yaml              ← 10 sources
├── 02_ONTOLOGY/INDEX.yaml
├── 03_EUREKAS/INDEX.yaml
├── 04_DOCTRINES/INDEX.yaml
├── 05_POLICIES/INDEX.yaml
├── 06_CAPABILITIES/INDEX.yaml
├── 07_SKILLS/INDEX.yaml
├── 08_WORKFLOWS/INDEX.yaml
├── 09_AGENTS/INDEX.yaml
├── 10_RECEIPTS/INDEX.yaml
├── 11_GRAPH/INDEX.yaml
└── 12_TESTS/INDEX.yaml
```

## Source-of-truth regulations

- F1 AMANAH: every mutation must be reversible. `rm -rf` of `RESOURCES/` restores the original state.
- F2 TRUTH: every claim asserted in a manifest carries an epistemic label (OBS/DER/INT/SPEC).
- F11 AUDITABILITY: every change emits a receipt.
- F13 SOVEREIGN: F13 ratifies / vetoes / seals. The Impact Analyzer (Move 4) requires F13 announcement before build.

## Build order

B → C → A

1. **B (Discovery)** — scorecard: 100% sources discovered, 100% love-links bidirectional
2. **C (Execution)** — scorecard: 486 SKILL.md still load, zero regressions
3. **A (Adaptation)** — scorecard: synthetic SCAR → EUREKA → propagation succeeds

DITEMPA BUKAN DIBERI ⚒️
