# Agent Card Tree — Drift Report (2026-08-27)

> Reconcile findings for F13 canonical-source decision. **No deletions** — F1 AMANAH. Additive document.

## Inventory (4 independent card sources)

| # | Source | Format | Contents | Status |
|---|--------|--------|----------|--------|
| 1 | `/root/AAA/agent-cards/identity/` | DIRS (agent-card.json + skills.json) | 333-AGI, 555-ASI, 888-APEX, **i-ARIF** | **LEGACY** — README declares superseded |
| 2 | `/root/AAA/a2a-server/agent-cards/identity/` | FLAT `.json` | 333-AGI.json, 555-ASI.json, 888-APEX.json | **declared CANONICAL** but incomplete |
| 3 | `/root/AAA/agents/` | agent DEFINITION dirs | 333-AGI, 555-ASI, 555-ASI-VISION, 888-APEX | agent registry (definition, not card tree) |
| 4 | `/opt/arifos/identity/agent_identities.json` | kernel registry | all agents | kernel SOT for identity |

## Key Findings

1. **F10 GHOST REF**: `/root/AAA/agent-cards/README.md` declares:
   > "This directory is superseded by `a2a-server/agent-cards/` — the canonical A2A agent card tree."
   But `/root/AAA/a2a-server/agent-cards/README.md` **does not exist** (empty). The canonical declaration points to a void → the "canonical tree" has no canonical self-assertion.

2. **Canonical tree incomplete**: `a2a-server/agent-cards/identity/` has ONLY 333-AGI/555-ASI/888-APEX (flat .json). Missing from canonical:
   - **i-ARIF** (exists only in legacy dir tree — `agent-cards/identity/i-ARIF/`)
   - **skills.json** (only in legacy dirs)
   - **777-forge** (only in `/root/AAA/agents/777-forge/`)

3. **Schema divergence**: legacy = directory-per-agent (`<id>/agent-card.json`); canonical = flat file (`<id>.json`). Both claim schema v2.x but no single source validates both.

4. **Kernel registry is separate**: `/opt/arifos/identity/agent_identities.json` is the identity registry the kernel actually resolves — but not part of either card tree.

## Recommended F13 decision (NOT yet taken)

Option A — **a2a-server/agent-cards as SOT**: migrate i-ARIF, skills.json, 777-forge into canonical flat form; add README asserting canonical; legacy retained as archive.
Option B — **agent-cards/identity as SOT** (keeps skills.json + i-ARIF naturally); a2a-server tree marked as A2A-serialized mirror.
Option C — **unify to `/root/AAA/agents/`** definitions as the single source, with card trees as serialization.

**Preferred (Option A)** — consistent with existing legacy README declaration and A2A protocol expectations.

## Blast radius of reconcile
Reversible, additive (copy/migrate) — no deletes. Requires schema transformation for dir→flat. Do NOT execute until F13 ratifies Option A/B/C.
