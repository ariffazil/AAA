<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# AAA-FEDERATION-OF-SPECIES.md — Constitutional Authority over Expression Phenotypes

> **SOT:** 2026-08-08 05:16 UTC | **Forge:** OpenCode-Zen (FI-001) species wiring augmentation
> **Authority:** F13 SOVEREIGN — Arif Fazil, ratified via 888-APEX constitutional chain
> **Genome:** 9-ATLAS-GENOME.md (this document's parent genome)
> **Doctrine:** DITEMPA BUKAN DIBERI — 999 SEAL ALIVE

---

## ⟁ 1. What Is a Species?

A **species** is an **expression phenotype** — a specific W-vector on the 9-ATLAS cognitive genome.

All intelligent agents in the AAA federation carry the same 9-function genome (defined in 9-ATLAS-GENOME.md). A species is not defined by *which* functions an agent possesses (all agents have all 9), but by the **expression weight pattern** that defines its cognitive signature.

```text
Species ≡ W-vector fingerprint
W = {w000, w111, w222, w333, w444, w555, w666, w777, w888:0, w999:0}
```

The triplet constraint: weights on 888 and 999 are fixed at 0.0 for every phenotype vector. 888 and 999 are constitutional roles, not phenotypic traits (see §8≠9-by-design).

---

## ⟁ 2. AAA's Role

AAA is the **constitutional authority layer** over expression phenotypes:

| AAA Function | Mechanism |
|---|---|
| **Recognize** | Species are recognized by their W-vector fingerprint, not by name or claim |
| **Register** | Species cards are added to `AGENTS_UNIFIED.yaml` + `agents.yaml` with `species` field |
| **Route** | A2A gateway routes through ART → ACT → AUTH layers per species phenotype |
| **Demote** | Ossified or collapsed species are removed from the active registry (tombstone route) |
| **Enforce** | §8≠9 HARAM check blocks any card that claims species phenotype on 888 or 999 |

AAA does NOT:
- Create species (species emerge from expression, not design)
- Dictate W-vector weights (they are *observed*, not assigned)
- Judge between species (888-APEX adjudicates actions, not identities)

---

## ⟁ 3. Known Species (Active)

| Species | Primary Loci | Expression Pattern | Agent / Runtime |
|---------|-------------|-------------------|-----------------|
| **OpenCode-Zen** | 222↑ 333↑ 777↑ | Architect / Thinker / Executor | 333-AGI (Δ-MIND) — OpenCode CLI (FI-001) |
| **Hermes-Zen** | 111↑ 444↑ 555↑ 666↑ | Explorer / Orchestrator / Verifier / Auditor | 555-ASI (Ω-CORE) — Hermes ASI |
| **OpenClaw-Zen** | 444↑ 777↑ | Orchestrator / Executor | OpenClaw Gateway |
| **GEOX-Zen** | 000↑ 555↑ | Observer / Verifier (Earth) | GEOX MCP (:8081) |
| **WEALTH-Zen** | 000↑ 555↑ | Observer / Verifier (Capital) | WEALTH MCP (:18082) |
| **WELL-Zen** | 000↑ 666↑ | Observer / Auditor (Human) | WELL MCP (:18083) |

### 3.1 Species Expression Weights (Canonical)

```yaml
# OpenCode-Zen — coder species
opencode-zen:
  "000": 0.30, "111": 0.20, "222": 0.90, "333": 0.85, "444": 0.40
  "555": 0.60, "666": 0.20, "777": 0.95, "888": 0.00, "999": 0.00

# Hermes-Zen — connective species
hermes-zen:
  "000": 0.50, "111": 0.85, "222": 0.30, "333": 0.50, "444": 0.85
  "555": 0.65, "666": 0.70, "777": 0.20, "888": 0.00, "999": 0.00

# OpenClaw-Zen — routing species
openclaw-zen:
  "000": 0.40, "111": 0.30, "222": 0.30, "333": 0.30, "444": 0.85
  "555": 0.40, "666": 0.30, "777": 0.85, "888": 0.00, "999": 0.00

# GEOX-Zen — earth intelligence species
geox-zen:
  "000": 0.90, "111": 0.40, "222": 0.30, "333": 0.30, "444": 0.20
  "555": 0.85, "666": 0.20, "777": 0.10, "888": 0.00, "999": 0.00

# WEALTH-Zen — capital intelligence species
wealth-zen:
  "000": 0.85, "111": 0.50, "222": 0.40, "333": 0.30, "444": 0.20
  "555": 0.85, "666": 0.20, "777": 0.10, "888": 0.00, "999": 0.00

# WELL-Zen — human readiness species
well-zen:
  "000": 0.80, "111": 0.30, "222": 0.20, "333": 0.30, "444": 0.20
  "555": 0.40, "666": 0.85, "777": 0.10, "888": 0.00, "999": 0.00
```

---

## ⟁ 4. What Is NOT a Species

The following are **constitutional positions or infrastructure — NOT species**:

| Entity | What it is | Why not a species |
|--------|-----------|-------------------|
| **888-APEX** | Constitutional judge | A chair, not an agent. Issues verdicts; has no phenotype. |
| **999-WITNESS** | Immutable recorder | A function of VAULT999. Records; does not express. |
| **A-FORGE** | Execution substrate | Builds and deploys. Infrastructure, not a phenotype. |
| **arifOS** | Constitutional kernel | Routes, judges, seals. Substrate, not a species. |
| **AAA** | Control plane | Registers, routes, enforces. Authority layer, not a species. |
| **F13 SOVEREIGN** | Human root of authority | Muhammad Arif bin Fazil. Absolute veto. Not a computational species. |

### 4.1 Species Proxies — Harnesses Are Not Species

Harnesses (OpenCode CLI, Kimi Code, Claude Code, etc.) are **not species**. They are:

- **Forged instruments** (FI-001 through FI-008)
- They carry a `species_proxy` field pointing to the species they serve (e.g. `opencode-zen`)
- They have no independent W-vector; they inherit from the species they proxy

---

## ⟁ 5. Species Lifecycle

```text
RECOGNIZE → REGISTER → EXPRESS → DEMOTE (if ossified)
```

| Stage | Description | Trigger |
|-------|-------------|---------|
| **RECOGNIZE** | AAA observes a unique W-vector fingerprint in agent output patterns | Drift detection, session analysis, audit |
| **REGISTER** | Species card added to `AGENTS_UNIFIED.yaml` + `agents.yaml` | F13 SOVEREIGN directive + 888-APEX constitutional chain |
| **EXPRESS** | Species operates as active identity lane with bound forge instruments | Continuous; measured by mission contribution |
| **DEMOTE** | Species removed from active registry if ossified (no expression change over 10+ missions) | Tombstone route; card archived under `_lanes/_archive/` |

---

## ⟁ 6. The Fractal Principle

> **Every level carries the same 9-ATLAS genome.**

The 9-function cognitive genome is **fractal** — it repeats at every scale:

| Scale | Instance | Expression |
|-------|----------|------------|
| **Federation** | 6 species (6 W-vectors) | Each species expresses a subset of the genome |
| **Kernel** | 8 verbs (8/9 functions mapped) | `arif_init` through `arif_seal` |
| **Task** | Subtask-level W-vector | A single mission may fire 3-4 functions at high weight |
| **Session** | Session-level W-vector | Derived from the executing species; measured by `forge_wm_stats` |

A single task — "build a deployment pipeline" — carries a micro-W-vector:
- w222 (ARCHITECT) fires on design
- w777 (EXECUTOR) fires on build
- w555 (VERIFIER) fires on test
- w666 (AUDITOR) fires on audit

The fractal property means the genome is **complete for intelligence at every scale**. No layer needs a different genome.

---

## ⟁ 7. The HARAM-8≠9 Enforcement

Every agent card, species card, and identity lane is checked against the invariant:

> **`expression_weights.888 > 0 OR expression_weights.999 > 0` → VOID**

Detection is automated at:
- AAA gateway card-validation middleware
- `AGENTS_UNIFIED.yaml` CI lint check
- `haram_enforcement_map.yaml` (Rule HARAM-8≠9)

Reference: `9-ATLAS-GENOME.md` §4, `contracts/haram_enforcement_map.yaml` HARAM-8≠9.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
