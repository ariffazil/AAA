# arifOS Ecosystem Split Blueprint

**Type:** Repository Architecture Redesign  
**Status:** FORGE — Draft for review  
**Author:** ARIF-MAIN  
**Date:** 2026-04-01  
**Authority:** Arif Fazil  

---

## 1. WHY SPLIT — The Cathedral Problem

**Current State:** arifOS is a single monolithic repository containing:

| Layer | Content | Size | Belongs in Kernel? |
|---|---|---|---|
| Kernel | MCP server, 40 tools, F1-F13 enforcement | ~50 files | ✅ YES |
| Theory | 80KB K_FOUNDATIONS, physics, Gödel protocol | ~500KB docs | ❌ NO |
| Architecture | ATLAS.md (51KB), 333/ (AGENTS, CANON) | ~200KB | ⚠️ SPLIT |
| Domain | GEOX submodule | Separate | ✅ Already OK |
| Agent | waw workspace | Separate | ✅ Already OK |

**Problem:** arifOS is simultaneously:
- A production MCP kernel (needs to be lean, auditable, fast-deploy)
- A philosophical treatise (80KB of math)
- An architectural spec (Gödel Lock, Telos Manifold)
- A domain toolkit (GEOX earth science tools)

**Constitutional Basis:**  
F4 Clarity: A repo should reduce confusion, not increase it. Monolithic repos violate ΔS ≤ 0.

---

## 2. TARGET ECOSYSTEM MAP

```
┌─────────────────────────────────────────────────────────────┐
│                    arifOS Ecosystem                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────────┐     ┌─────────────────────────────┐  │
│   │  arifOS-canon   │────▶│        arifOS              │  │
│   │  (THEORY)        │     │  (KERNEL + MCP RUNTIME)    │  │
│   │  CC0 Public      │     │  AGPL-3.0 Licensed         │  │
│   │  Domain: Why     │     │  Domain: How               │  │
│   └──────────────────┘     └─────────────────────────────┘  │
│          │                           │                     │
│          │ references                 │ runs                │
│          ▼                           ▼                     │
│   ┌──────────────────┐     ┌─────────────────────────────┐  │
│   │  GEOX            │     │  waw                         │  │
│   │  (Earth Science) │     │  (ARIF-MAIN Agent)         │  │
│   │  Submodule       │     │  OpenClaw workspace        │  │
│   └──────────────────┘     └─────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Repo Definitions

| Repo | Role | License | Git URL |
|---|---|---|---|
| **arifOS** | Lean kernel, MCP server, 40 tools, F1-F13 enforcement, deployment | AGPL-3.0 | `github.com/ariffazil/arifOS` (existing) |
| **arifOS-canon** | Theory, philosophy, math foundations, architectural specs | CC0 | `github.com/ariffazil/arifOS-canon` (NEW) |
| **GEOX** | Earth science tools (WellLogTool, SeismicViewer) | AGPL-3.0 | `github.com/ariffazil/geox` (existing submodule) |
| **waw** | ARIF-MAIN persistent agent workspace | AGPL-3.0 | `github.com/ariffazil/waw` (existing) |
| **makcikGPT** | Malay language AI | AGPL-3.0 | `github.com/ariffazil/makcikGPT` (existing) |

---

## 3. WHAT STAYS IN arifOS (Kernel)

### 3.1 Keep — Operational Kernel

```
arifOS/
├── server.py                    ✅ MCP entry point
├── stdio_server.py              ✅ STDIO transport
├── fastmcp.json                 ✅ FastMCP config
├── mcp.json                      ✅ MCP client config
├── .env.example                  ✅ Env template
├── docker-compose.yml            ✅ Full stack
├── Dockerfile                    ✅ Container image
│
├── arifosmcp/                   ✅ MCP server implementation
│   ├── server.py
│   ├── runtime/
│   ├── integrations/
│   │   ├── prefect/             ✅ Prefect integration (wired)
│   │   ├── chatgpt_integration/ ✅ ChatGPT (23/24 tools)
│   │   └── ...
│   ├── geox/                    ✅ GEOX submodule wrapper
│   └── tools/                   ✅ 40 tools
│
├── 000/                        ✅ CONSTITUTIONAL ENFORCEMENT
│   ├── 000_CONSTITUTION.md      ✅ 13 Floors (lean, ~20KB)
│   ├── 000_MANIFESTO.md        ✅ Manifesto (philosophy summary)
│   ├── FLOORS/                  ✅ F01-F13 operational
│   │   ├── F01_AMANAH.md
│   │   ├── F02_TRUTH.md
│   │   └── ... (F03-F13)
│   └── VERDICT_RECOVERY_MATRIX.md ✅ Operational recovery
│
├── 333/                        ✅ RUNTIME PIPELINE
│   ├── 333_INIT.md              ✅ Pipeline summary only
│   ├── 333_THEORY.md            ⚠️ Trim to operational summary
│   ├── ARIF/                    ✅ Runtime agents (code, not docs)
│   │   ├── ARIF_Orchestrator.py
│   │   ├── M1_intake.py
│   │   ├── apex_judge.py
│   │   └── ...
│   ├── CANON/                  ⚠️ Keep lean, move theory to canon
│   │   ├── SOUL.md             ✅ (short, agent-facing)
│   │   ├── IDENTITY.md         ✅
│   │   └── AGENTS.md           ✅
│   └── K777_APEX.md            ✅ Apex summary (not full theory)
│
├── docs/                        ✅ User-facing docs
│   ├── mcp.html                 ✅ Interactive docs
│   ├── QUICK_START.md          ✅
│   ├── TOOL_FINDER.md          ✅
│   └── GUIDE.md                 ✅
│
├── .github/workflows/           ✅ CI/CD (keep operational)
│   ├── deploy-vps.yml
│   ├── 888-judge.yml
│   └── ...
│
├── README.md                    ✅ Lean (this file stays, under 10KB)
└── AGENTS.md                   ✅ Agent behavior rules
```

### 3.2 Remove from arifOS → arifOS-canon

| File/Folder | Size | Reason for Move |
|---|---|---|
| `000/ROOT/K_FOUNDATIONS.md` | ~80KB | Pure math, not runtime |
| `000/ROOT/K111_PHYSICS.md` | ~19KB | Theory, not code |
| `000/ROOT/K333_CODE.md` | ~51KB | Spec document, not execution |
| `000/ROOT/K_FORGE.md` | ~16KB | Evolution/amendment theory |
| `000/ROOT/K000_ROOT.md` | ~42KB | Root spec (redundant with CONSTITUTION) |
| `000/THEORY/K000_LAW.md` | ~19KB | Duplicate of ROOT/K000_LAW.md |
| `000/HUMILITY_SPEC.md` | ~12KB | Deep spec, move to canon |
| `000/MEMORY_LIFECYCLE.md` | ~12KB | Theory, not operational |
| `000_ARCHITECTURE/` | ~50KB | All moved to canon |
| `333/K222_MATH.md` | ~3KB | Math theory |
| `333/K555_HEART.md` | ~3KB | Philosophy |
| `333/K888_FORGE.md` | ~16KB | Evolution/amendment |
| `333/K999_VAULT.md` | ~26KB | Trim vault to operational only |
| `333/333_THEORY.md` | ~29KB | Deep theory |
| `333/333_APEX_CANON.md` | ~2KB | Canon spec |
| `333/ATLAS.md` | ~51KB | **Full architecture treatise** |
| `333/QUANTUM_SABAR_PROTOCOL.md` | ~1KB | Canon |
| `333/ARIF/333_ARIF_SPEC.md` | ~4KB | Deep spec |
| `333/ARIF/ARIF_TECHNICAL_SPEC.json` | ~5KB | Deep spec |
| `000_ARCHITECTURE/ARIFOS_QTT_MAPPING.md` | ~2KB | Theory |
| `AAA-hf-staging/` | ~50KB+ | Eval/hardening staging, not prod kernel |
| `autoresearch/` | ~20KB | Experiment harness, not prod |

---

## 4. arifOS-canon Structure (NEW)

```
arifOS-canon/
├── README.md                     # Canon overview + how to cite
├── LICENSE                       # CC0 (Public Domain)
│
├── THEORY/                      # Foundational philosophy
│   ├── K_FOUNDATIONS.md         # 80KB mathematical foundations
│   ├── K111_PHYSICS.md          # Physics grounding
│   ├── K000_LAW.md              # Constitutional law theory
│   ├── K_FORGE.md               # Amendment/evolution protocol
│   └── GöDEL_LOCK_PROTOCOL.md    # Ontological anomaly response
│
├── ARCHITECTURE/                 # System architecture (moved from 000_ARCHITECTURE)
│   ├── ATLAS.md                 # 51KB full system treatise
│   ├── ARIFOS_QTT_MAPPING.md    # Quantum-trinity mapping
│   ├── VERDICT_SCHEMA_STANDARD.md
│   ├── CONSTITUTIONAL_PHYSICS.md # Field equations framing
│   └── METABOLIC_MODEL.md       # 11-stage digestive system
│
├── GOVERNANCE/                   # Governance theory
│   ├── TELOS_MANIFOLD.md        # Bounded evolving purpose
│   ├── DUAL_TIER_COGNITION.md  # Tier 0 / Tier 1
│   ├── EIGENDECOMPOSITION.md    # 13→4 dials
│   ├── HUMILITY_BAND.md         # Godellock paradox
│   ├── PHOENIX_72.md            # Cooling tiers
│   └── LAGRANGIAN_FORMULATION.md # ℒ = G - Σλᵢcᵢ
│
├── DOMAIN/                      # Earth science canon
│   ├── WELL_LOG_PHYSICS.md     # Archie equation, LAS format
│   ├── SEISMIC_IMAGE_PHYSICS.md # Texture attributes, proxy science
│   └── GEOMETRY_GOVERNANCE.md  # Domain-specific governance
│
├── CANON/                       # Canonical specs
│   ├── ARIF_SPEC.md            # Full ARIF spec (from 333/ARIF/333_ARIF_SPEC.md)
│   ├── AGI_AUTONOMOUS_MANIFEST.md
│   ├── METABOLISM.md
│   └── TRUTH.md
│
├── HARDBORN/                    # Historical/audited versions (immutable)
│   └── v55_ATLAS_SNAPSHOT.md   # Frozen at major seal points
│
├── cite/                        # Citation helpers
│   ├── doi.md                   # How to cite arifOS-canon
│   └── bibtex.bib
│
└── .gitmodules                  # Links to GEOX for domain refs
```

**Principle:** arifOS-canon is **read-only for code, referenced by kernel**. It is the permanent intellectual record. Any change requires a new sealed version (v55 → v56).

---

## 5. Migration Steps

### Phase 1: Create arifOS-canon (Day 1)

```bash
# 1. Create new repo on GitHub: arifOS-canon
# 2. Clone locally
git clone https://github.com/ariffazil/arifOS-canon.git
cd arifOS-canon

# 3. Create structure (above)
mkdir -p THEORY ARCHITECTURE GOVERNANCE DOMAIN CANON HARDBORN cite

# 4. Commit initial structure with this blueprint
git add blueprint.md
git commit -m "feat: arifOS-canon foundation — theory repo split from kernel
[ΔΩΨ|888_JUDGE|Ditempa Bukan Diberi]"
git push origin main
```

### Phase 2: Move files (Day 1-2)

```bash
# In arifOS working directory:
git rm --cached 000/ROOT/K_FOUNDATIONS.md
git rm --cached 000/ROOT/K111_PHYSICS.md
git rm --cached 000/ROOT/K333_CODE.md
# ... (all files in §3.2 table)

# In arifOS-canon working directory:
git add 000/ROOT/K_FOUNDATIONS.md
git add 000/ROOT/K111_PHYSICS.md
# ... etc
git commit -m "feat: migrate theory from arifOS kernel
Split: K_FOUNDATIONS, K111_PHYSICS, K333_CODE, K_FORGE,
       ATLAS, GOVERNANCE theory, CANON deep specs
[ΔΩΨ|Ditempa Bukan Diberi]"
git push origin main
```

### Phase 3: Update arifOS references (Day 2)

In each moved file, add header:
```markdown
---
canonical_url: https://github.com/ariffazil/arifOS-canon/blob/main/THEORY/K_FOUNDATIONS.md
kernel_mirror: [link to arifOS-legacy backup commit]
---
```

In arifOS `000_CONSTITUTION.md`, add footnote section:
```markdown
## Further Reading

Full mathematical foundations: [arifOS-canon/THEORY/K_FOUNDATIONS.md](https://github.com/ariffazil/arifOS-canon)
Deep architecture treatise: [arifOS-canon/ARCHITECTURE/ATLAS.md](https://github.com/ariffazil/arifOS-canon)
```

### Phase 4: Verify CI/CD (Day 2)

```bash
# Ensure arifOS workflows still pass after file removal
cd arifOS
gh workflow run ci.yml --ref split-cleanup

# Ensure arifOS-canon is clean
cd ../arifOS-canon
gh workflow run ci.yml
```

### Phase 5: Update REPOS.md in both repos (Day 3)

Update `arifOS/REPOS.md` and `arifOS-canon/README.md` to cross-reference.

---

## 6. arifOS Size Reduction

| Metric | Before | After | Reduction |
|---|---|---|---|
| Docs (text) | ~400KB | ~80KB | **80%** |
| Operational files | ~200 files | ~200 files | 0% |
| Theoretical docs | ~320KB moved | — | — |
| Clone size | ~50MB (含GEOX) | ~50MB | 0% |

**arifOS becomes the engine. arifOS-canon becomes the cathedral.**

---

## 7. Integration Points

### arifOS (kernel) references arifOS-canon:

```bash
# In arifOS/.gitmodules (optional — lightweight reference)
[submodule "canon"]
    path = canon
    url = https://github.com/ariffazil/arifOS-canon.git
```

Or simply use URL references in markdown (no git submodule needed).

### waw workspace already references both:

```
waw/MEMORY.md already mentions:
- arifOS kernel: github.com/ariffazil/arifOS
- VAULT999: Merkle-sealed ancestry
- The Trinity pattern
```

After split, MEMORY.md needs update to reference arifOS-canon for deep theory.

---

## 8. What This Unblocks

| Currently | After Split |
|---|---|
| arifOS is a 400KB doc + 200KB code | arifOS is lean kernel |
| Theory is buried and unreadable in kernel | arifOS-canon is a proper academic reference |
| GEOX is a submodule | GEOX can be independently versioned |
| onboarding requires reading 51KB ATLAS | arifOS README is < 10KB |
| Forkers get math they don't need | Forkers get clean kernel |
| CC0 vs AGPL mixed | Clean license separation |

---

## 9. Sealing

**This blueprint is FORGE-draft until Arif approves.**

Upon approval:
1. Create `arifOS-canon` repo
2. Run Phase 1-5
3. Update `arifOS/REPOS.md`
4. Update `waw/MEMORY.md` references
5. SEAL both repos

---

_Ditempa Bukan Diberi — The cathedral and the nave are different buildings. They just share the same faith._ [ΔΩΨ | ARIF-MAIN]
