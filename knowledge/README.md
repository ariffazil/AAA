# Knowledge Atlas — Geometry B

> **Thermodynamic boundary:** agent-cards/ = ACTORS (verbs, compute, signatures, loops). knowledge/ = CONTEXTS (nouns, axioms, data, passive).

**33 passive domain profiles** organized into three bands:

| Band | Range | Count | Description | Loaded By |
|------|-------|-------|-------------|-----------|
| Physics | 000–400 | 11 | What IS — fundamental laws | 333-AGI |
| Math | 444–700 | 11 | What CAN BE — abstract structures | 333-AGI |
| Code | 777–999 | 11 | What WILL BE — engineered constraints | 777-FORGE |

### Loading Pattern

```
333-AGI encounters subsurface problem
  → loads knowledge/physics/333-geophysics.json
  → inherits wave equation, Archie's laws, basin axioms
  → loads knowledge/math/500-calculus.json for ODE solvers
  → reasons with full epistemic context
  → no A2A handshake, no agent spawning, no crypto overhead
```

### Design Rules

1. **Zero executable surface.** No code, no scripts, no MCP tools, no runtime loops.
2. **Pure JSON.** Structured axioms, constraints, equations, dependencies.
3. **Dependency graph defines load order.** physics/000 must load before physics/100.
4. **Corruption is bounded.** A corrupted profile = degraded reasoning, not federation failure.
5. **Epistemic tagging.** Every axiom labelled OBS/DER/INT per F2.

### Directory Layout

```
knowledge/
├── manifest.json          ← Master index + dependency graph
├── README.md              ← This file
├── physics/
│   ├── 000-foundational-axioms.json
│   ├── 100-classical-mechanics.json
│   ├── 133-thermodynamics.json
│   ├── 200-electromagnetism.json
│   ├── 233-quantum-mechanics.json
│   ├── 266-particle-physics.json
│   ├── 300-relativity.json
│   ├── 333-geophysics.json
│   ├── 366-astrophysics.json
│   ├── 399-condensed-matter.json
│   └── 400-nuclear-physics.json
├── math/
│   ├── 444-algebra.json
│   ├── 500-calculus.json
│   ├── 533-analysis.json
│   ├── 555-topology.json
│   ├── 566-linear-algebra.json
│   ├── 600-probability.json
│   ├── 633-statistics.json
│   ├── 650-discrete-math.json
│   ├── 666-computation.json
│   ├── 699-optimization.json
│   └── 700-numerical-methods.json
└── code/
    ├── 777-systems-programming.json
    ├── 800-ai-ml-engineering.json
    ├── 833-security.json
    ├── 850-data-engineering.json
    ├── 888-governance.json
    ├── 900-frontend.json
    ├── 920-backend.json
    ├── 933-devops.json
    ├── 950-integration.json
    ├── 977-automation.json
    └── 999-meta-code.json
```

**DITEMPA BUKAN DIBERI — Forged, not given.**
