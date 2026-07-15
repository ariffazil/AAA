# 888 HOLD Resolution Memo — HOLD-01 + HOLD-02

> **Epoch:** 2026-07-15  
> **Auditor:** Grok Build Agent  
> **Authority needed:** ARIF F13 (confirmation only — evidence already OBS)  
> **DITEMPA BUKAN DIBERI**

---

## HOLD-01 · WELL license AGPL-3.0 vs BSL-1.1

### Evidence (OBS)

| Source | Value |
|--------|--------|
| `/root/WELL/LICENSE` | **GNU AGPL v3** full text |
| `/root/WELL/README.md` (zen identity) | AGPL-3.0 |
| `/root/WELL/pyproject.toml` / package | AGPL pattern with LICENSE |
| Architecture draft (prose) | claimed BSL-1.1 — **wrong** |
| `Dockerfile` OCI label | **was BSL-1.1** — residual drift |

GEOX alone is BSL-1.1 (LICENSE + pyproject). WEALTH + WELL are AGPL-3.0.

### Legal / federation meaning

| License | Typical intent |
|---------|----------------|
| **BSL-1.1** (GEOX) | Source available; commercial use terms for Earth product |
| **AGPL-3.0** (WEALTH, WELL) | Strong copyleft; network use must share source — fits compute/mirror organs that must not be closed SaaS forks of capital/human mirrors |

### Recommendation (best)

| Path | Verdict |
|------|---------|
| **A. Keep AGPL-3.0 for WELL** | **RECOMMENDED** — matches LICENSE file on disk; aligned with WEALTH; zen README already correct |
| B. Relicense WELL → BSL-1.1 | Only if Arif wants product/commercial symmetry with GEOX — requires deliberate LICENSE rewrite + GitHub license change (constitutional/product choice, not a bugfix) |

**Do not “fix” LICENSE to BSL to match a wrong architecture slide.** That would be narrative > physics.

### Actions if Path A (recommended)

1. Confirm F13: “WELL stays AGPL-3.0.”  
2. Fix residual BSL labels (Dockerfile OCI — **done 2026-07-15**).  
3. Grep federation docs for “WELL … BSL” and correct to AGPL.  
4. Commit with license truth in message.

---

## HOLD-02 · WEALTH tools 12 vs 50

### Evidence (OBS)

| Source | Count / content |
|--------|-----------------|
| Live mcporter / `tools/list` | **12** |
| `wealth_mcp/server.py` | Comment: *Canonical tool surface (7 tools, mode-dispatched)* + institutional register |
| `_OBSERVE_SURFACE` frozenset | **exactly 12 names** |
| `wealth_mcp/tools/canonical.py` | 8 tools: `capital_primitive`, `capital_health`, `capital_diagnose`, `capital_wisdom`, `capital_market`, `capital_ledger`, `capital_registry`, `capital_entropy` |
| `wealth_mcp/tools/institutional.py` | 4 tools: stress, cascade, governance_capacity, exploitation |
| `capital_primitive` modes | npv \| irr \| emv \| evoi \| mc \| kelly \| markowitz \| robust \| chance_constrained \| two_stage (**10 modes on 1 tool**) |
| `capital_health` / `capital_diagnose` | multi-mode (runway, conservation, collapse, bid_surface, …) |
| `internal/monolith.py` | ~24 named `wealth_*` (legacy) |
| `contracts/tools.yaml` | **~64** historical names — **stale catalog**, pre-ZEN |

### Interpretation

```
OLD surface (prose “50”):  many named wealth_* tools + aliases + modes counted as tools
NEW surface (ZEN 2026-07): 12 MCP tools × modes  = capability preserved, surface simplified
```

This is **intentional consolidation**, not a silent registration outage.  
Proof: modes still execute (EMV, EVOI, Kelly live-tested earlier this epoch); institutional tools present; federated architecture layers ALIVE.

### Recommendation (best)

| Path | Verdict |
|------|---------|
| **A. Accept 12 as public MCP SOT** | **RECOMMENDED** — matches code + runtime + ZEN design |
| B. Re-expand to 50 tool names | Only if product wants one-tool-per-verb UX; increases entropy; reverse of zen |
| C. Hybrid: 12 tools + public “capability map” | **RECOMMENDED companion** — document modes as capabilities, not tool counts |

**Capability claim (honest):**

| Capability class | How exposed |
|------------------|-------------|
| Capital math (NPV/IRR/EMV/EVOI/Kelly/Markowitz/MC/…) | `capital_primitive(mode=…)` |
| Health / runway / conservation | `capital_health(mode=…)` |
| Institutional / collapse / bid surface | `capital_diagnose` + 4 institutional tools |
| Market / wisdom / ledger / entropy / registry | dedicated capital_* tools |

“27 stock modes” if still true live under `capital_market` / stock payload — verify per schema; do **not** add to tool count.

### Actions if Path A

1. Confirm F13: “12 tools is intentional; modes hold the old surface.”  
2. Update `contracts/tools.yaml` header → “LEGACY monolith catalog; public SOT = 12 mode-dispatched tools” or regenerate from live list.  
3. Ban “50 public tools” in README / architecture seals (already fixed in zen).  
4. Optional: `docs/TOOL_SURFACE.md` with table tools × modes.

---

## Decision table for ARIF (one line each)

| HOLD | Question | Agent recommendation | Risk if wrong |
|------|----------|----------------------|---------------|
| **01** | WELL AGPL or BSL? | **AGPL-3.0** (file truth) | BSL claim = F2 lie; relicense needs deliberate product intent |
| **02** | WEALTH 12 or 50? | **12 tools intentional** (mode ZEN) | Re-counting modes as tools confuses agents; 50 prose breaks SOT |

### Suggested F13 replies (copy-paste)

```
HOLD-01: AGPL-3.0 intentional. Keep. Fix residual BSL labels only.
HOLD-02: 12 tools intentional (mode-dispatched ZEN). Capability ≠ tool count. Update tools.yaml to legacy.
Release commits WELL → WEALTH → GEOX after gate scoped.
```

---

## Commit gate

| Gate | State |
|------|--------|
| HOLD-01 | **Await F13** — evidence favors AGPL; Dockerfile label fixed preemptively to match LICENSE |
| HOLD-02 | **Await F13** — evidence favors 12 as design |
| governance-gate secrets | Pre-existing noise; scope out before push |
| Push | **No** until HOLDs released + gate scoped |

---

*Physics > narrative. LICENSE file > architecture slide. tools/list > marketing count.*
