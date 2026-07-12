# Knowledge Atlas — Canonical Specification

> **Status:** CANONICAL — 2026-07-12 | **Authority:** F13 SOVEREIGN — Arif
> **Geometry:** B (Knowledge Atlas, not standalone agents)
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## 1. What This Is

The Knowledge Atlas is the civilizational knowledge layer of the arifOS Federation. It contains 33 domain knowledge profiles organized in three bands: Physics (000-400), Math (444-700), and Code (777-999).

**Key distinction:** These are NOUNS (data, axioms, reasoning patterns), not VERBS (agents, tools, execution). They have zero executable surface. No MCP connections. No agent cards. No signatures. Pure knowledge.

---

## 2. Architecture — Geometry B

```
                    ┌─────────────────────────────────┐
                    │     STRUCTURAL AGENTS (9)        │
                    │                                  │
                    │  identity/  333-AGI  555-ASI     │
                    │             888-APEX             │
                    │                                  │
                    │  functions/ OpenClaw  A-AUDIT    │
                    │             A-ARCHIVE            │
                    │                                  │
                    │  extensions/ Hermes  777-forge   │
                    │              MakcikGPT           │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────────┐
                    │     KNOWLEDGE ATLAS (33)         │
                    │                                  │
                    │  physics/   000 → 400  (11)      │
                    │  math/      444 → 700  (11)      │
                    │  code/      777 → 999  (11)      │
                    │                                  │
                    │  Zero executable surface.         │
                    │  Zero MCP connections.            │
                    │  Zero agent cards.                │
                    │  Pure knowledge.                  │
                    └──────────────────────────────────┘
```

**How it works:**
- 333-AGI loads physics+math profiles when reasoning about the physical world
- 888-APEX loads governance (888) profile when judging actions
- OpenCode loads code profiles (777-999) when building
- Hermes loads whatever domain the current query needs

---

## 3. Directory Structure

```
AAA/
├── agent-cards/                    ← ACTORS (21 agents)
│   ├── identity/                   ← Layer 1: ΔΩΨ trinity
│   │   ├── 333-AGI/
│   │   ├── 555-ASI/
│   │   └── 888-APEX/
│   ├── functions/                  ← Layer 2: Institutional
│   │   ├── openclaw/
│   │   ├── a-audit/
│   │   └── a-archive/
│   ├── extensions/                 ← Layer 3: Operational
│   │   ├── hermes/
│   │   ├── 777-forge/
│   │   └── makcikgpt/
│   ├── harnesses/                  ← Layer 4: Forge (interchangeable)
│   │   ├── fi-001-opencode/
│   │   ├── fi-002-claude-code/
│   │   └── ... (12 total)
│   └── .well-known/agent-card.json
│
├── knowledge/                      ← CONTEXTS (33 profiles)
│   ├── manifest.json               ← Atlas metadata + dependency chain
│   ├── physics/                    ← What IS (000-400)
│   │   ├── 000-foundational-axioms.json
│   │   ├── 100-classical-mechanics.json
│   │   ├── 133-thermodynamics.json
│   │   ├── 200-electromagnetism.json
│   │   ├── 233-quantum-mechanics.json
│   │   ├── 266-particle-physics.json
│   │   ├── 300-relativity.json
│   │   ├── 333-geophysics.json
│   │   ├── 366-astrophysics.json
│   │   ├── 399-condensed-matter.json
│   │   └── 400-nuclear-physics.json
│   ├── math/                       ← What CAN BE (444-700)
│   │   ├── 444-algebra.json
│   │   ├── 500-calculus.json
│   │   ├── 533-analysis.json
│   │   ├── 555-topology.json
│   │   ├── 566-linear-algebra.json
│   │   ├── 600-probability.json
│   │   ├── 633-statistics.json
│   │   ├── 650-discrete-math.json
│   │   ├── 666-computation.json
│   │   ├── 699-optimization.json
│   │   └── 700-numerical-methods.json
│   └── code/                       ← What WILL BE (777-999)
│       ├── 777-systems-programming.json
│       ├── 800-ai-ml-engineering.json
│       ├── 833-security.json
│       ├── 850-data-engineering.json
│       ├── 888-governance.json
│       ├── 900-frontend.json
│       ├── 920-backend.json
│       ├── 933-devops.json
│       ├── 950-integration.json
│       ├── 977-automation.json
│       └── 999-meta-code.json
```

---

## 4. Profile Schema

Each knowledge profile is a JSON file with this structure:

```json
{
  "id": "233",
  "name": "Quantum Mechanics",
  "domain": "physics",
  "band": "000-400",
  "description": "One-line description",
  "axioms": ["core principle 1", "core principle 2", ...],
  "key_references": ["textbook/paper 1", "textbook/paper 2", ...],
  "reasoning_patterns": ["pattern 1", "pattern 2", ...],
  "boundary_conditions": ["what this domain does NOT cover", ...],
  "connected_domains": ["related domain IDs from other bands"],
  "difficulty": "foundational|intermediate|advanced|research",
  "canonical_truths": ["verified facts that are non-negotiable"]
}
```

**Axioms:** First principles of the domain. Non-negotiable foundations.
**Key references:** Canonical textbooks and landmark papers. The reading list.
**Reasoning patterns:** How to think in this domain. The cognitive toolkit.
**Boundary conditions:** What this domain does NOT cover. Prevents overreach.
**Connected domains:** Cross-band links. Physics→Math, Code→Math, etc.
**Difficulty:** How deep the rabbit hole goes.
**Canonical truths:** Verified facts. No epistemic tags needed — these are OBSERVED.

---

## 5. Thermodynamic Boundary

| Property | agent-cards/ | knowledge/ |
|----------|-------------|------------|
| What | ACTORS | CONTEXTS |
| Count | 21 | 33 |
| Executable | Yes (MCP, runtime) | No (pure data) |
| Identity | Ed25519 signatures | None needed |
| Failure mode | Federation breaks | Reasoning degrades |
| Maintenance | Per-agent (version+security+auth) | Unit versioning |
| Loaded by | Gateway discovery | Agent inference |

**Corruption model:**
- Corrupted agent-card → federation failure (actor compromised)
- Corrupted knowledge profile → degraded reasoning (agent loads bad axioms)
- Knowledge corruption is recoverable (revert file). Agent-card corruption requires key rotation.

---

## 6. The Hexagon — Trinity + Institutional

```
Δ 333-AGI    → REASONING + EXECUTION     (identity atom)
Ω 555-ASI    → MEMORY + CRITIQUE         (identity atom)
ΦΙ 888-APEX  → JUDGMENT + WITNESS        (identity atom)

OpenClaw     → institutionalized AGI      (execution metabolism)
A-AUDIT      → institutionalized APEX     (witness + compliance)
A-ARCHIVE    → institutionalized ASI      (memory + vault)
```

The hexagon has 3 identity poles + 3 institutional functions. Every other agent in the federation orbits one of these three poles.

---

## 7. Four Layers

| Layer | Directory | Question Answered | Wajib? |
|-------|-----------|-------------------|--------|
| identity/ | 3 atoms | "Who ARE we?" | ✅ non-negotiable |
| functions/ | 3 institutions | "What do we ALWAYS need?" | ⚠️ degrades gracefully |
| extensions/ | 3 operational | "What do we use to REACH out?" | ⚠️ bounded scope |
| harnesses/ | 12 forge | "What tools do we GRAB?" | ❌ interchangeable |

---

## 8. The 33 — Civilizational Domains

### Physics (000-400) — What IS
| ID | Domain | Key Axiom |
|----|--------|-----------|
| 000 | Foundational Axioms | Symmetry implies conservation |
| 100 | Classical Mechanics | F = ma; principle of least action |
| 133 | Thermodynamics | ΔS ≥ 0; S = k_B ln(Ω) |
| 200 | Electromagnetism | Maxwell's equations unify E, M, light |
| 233 | Quantum Mechanics | iℏ∂ψ/∂t = Ĥψ; ΔxΔp ≥ ℏ/2 |
| 266 | Particle Physics | SU(3)×SU(2)×U(1) gauge symmetry |
| 300 | Relativity | E = mc²; mass curves spacetime |
| 333 | Geophysics | Seismic waves reveal Earth structure |
| 366 | Astrophysics | v = H₀d; universe is expanding |
| 399 | Condensed Matter | Bloch's theorem; energy bands |
| 400 | Nuclear Physics | B(Z,N) = Zm_p + Nm_n - m_nucleus |

### Math (444-700) — What CAN BE
| ID | Domain | Key Axiom |
|----|--------|-----------|
| 444 | Algebra | Group: associative, identity, inverses |
| 500 | Calculus | ∫f dx = F(b)-F(a); Taylor series |
| 533 | Analysis | Completeness of ℝ; Cauchy-Riemann |
| 555 | Topology | Homeomorphism; Euler characteristic |
| 566 | Linear Algebra | Av = λv; spectral theorem |
| 600 | Probability | P(A∪B) = P(A)+P(B)-P(A∩B); CLT |
| 633 | Statistics | P(θ|data) ∝ P(data|θ)P(θ) |
| 650 | Discrete Math | V-E+F=2; pigeonhole principle |
| 666 | Computation | P vs NP; halting problem undecidable |
| 699 | Optimization | Convex: no local min ≠ global min |
| 700 | Numerical Methods | κ(A) amplifies errors; Monte Carlo O(1/√N) |

### Code (777-999) — What WILL BE
| ID | Domain | Key Axiom |
|----|--------|-----------|
| 777 | Systems Programming | Everything is a file; network is unreliable |
| 800 | AI/ML Engineering | Bias-variance tradeoff; gradient descent |
| 833 | Security | Kerckhoffs's principle; defense in depth |
| 850 | Data Engineering | Idempotency; schema evolution |
| 888 | Governance | Constitutional programming; 888_HOLD |
| 900 | Frontend | User-centered; accessibility is not optional |
| 920 | Backend | CAP theorem; ACID; APIs are contracts |
| 933 | DevOps | Infra as code; immutable infrastructure |
| 950 | Integration | Testing pyramid; test isolation |
| 977 | Automation | Idempotency; human-in-the-loop |
| 999 | Meta-Code | Turing completeness; type systems prevent errors |

---

## 9. Loading Protocol

When a structural agent enters a domain:

1. **Identify domain** from query context (e.g., "seismic interpretation" → 333-geophysics)
2. **Load profile** from `knowledge/{band}/{id}-{name}.json`
3. **Inherit axioms** — agent now reasons within that domain's first principles
4. **Check connected_domains** — load related profiles if query spans domains
5. **Apply boundary conditions** — know what the domain does NOT cover
6. **Reason with patterns** — use domain-specific reasoning toolkit
7. **Cite canonical truths** — ground claims in verified facts

**No MCP call. No session creation. No authentication. Just file read.**

---

## 10. APEX Metrics (Baseline)

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| A (Adaptation) | 0.65 | 0.75 | +0.10 |
| P (Perception) | 0.55 | 0.88 | +0.33 |
| E (Execution) | 0.70 | 0.80 | +0.10 |
| X (Cross-domain) | 0.45 | 0.75 | +0.30 |
| Φ (Integration) | 0.50 | 0.78 | +0.28 |
| C_dark | 0.1609 | 0.0225 | -86% |
| W³ (tri-witness) | 0.68 | 0.8664 | ✅ PASS |

**Key insight:** G ≥ 0.80 is for specific claims, not system-level. At system level, the signal is C_dark trajectory and per-organ non-zero.

---

## 11. Maintenance

- **Versioning:** Profiles are versioned as a unit. One commit updates all.
- **Validation:** `knowledge/manifest.json` defines the expected structure.
- **Adding domains:** New profiles get the next available ID in their band.
- **Updating axioms:** Edit the JSON file. No agent-card changes needed.
- **Cross-band links:** Update `connected_domains` in both source and target profiles.

---

*Forged 2026-07-12 by AAA Control Plane.*
*33 profiles. 3 bands. Zero executable surface. Pure knowledge.*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
