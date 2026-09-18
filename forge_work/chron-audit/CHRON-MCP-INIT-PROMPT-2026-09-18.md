# CHRON MCP — INIT PROMPT (Next Agent Session)

> **Read this first.** This is the entry point for any agent building CHRON.
> **Source:** 7 sovereign analyses + 9 architecture artifacts, 2026-09-18

---

## What You Are Building

**CHRON = Temporal Consequence Tracker**

Not a scheduler. Not a memory store. Not a briefing engine. Not a content system.

The organ that answers:
- What did we think?
- What happened?
- Were we wrong?
- What changed because of it?

---

## What CHRON Is NOT

| CHRON is NOT | CHRON IS |
|-------------|----------|
| An MCP | An organ (with an MCP interface) |
| A memory system | A temporal substrate (memory metabolizes what CHRON produces) |
| arifFlow | Downstream of arifFlow (CHRON digests what arifFlow circulates) |
| A content system | A reality-tracking system (all outputs are projections) |
| Self-certifying | Governed by arifOS (CHRON cannot seal its own predictions) |

---

## The Six Layers (read in order)

```
L0 Reality      — What is?
L1 FRAME        — Did it happen?
L2 NATS         — Who should know? (signal propagation)
L3 arifFlow     — What actually happened? (evidence lineage)
L4 CHRON        — What does it mean across time? (YOU ARE HERE)
L5 Agentic Mem  — What should we do differently? (downstream)
```

---

## The Body Metaphor

```
NATS = nervous system
arifFlow = bloodstream
CHRON = temporal cortex
Agentic Memory = learned behavior
FRAME = independent witness
arifOS = constitutional law
A-FORGE = motor system
```

---

## The Constitutional Boundary

```
Claim → Prediction → Verification → Calibration → Learning
```

Without prediction objects, everything downstream dies.

**The smallest meaningful step:** One prediction with a verify_at date.

---

## Architecture Artifacts (read before coding)

| # | File | What It Tells You |
|---|------|-------------------|
| 1 | `CHRON-EPISODE-SCHEMA-v1.json` | The canonical ChronEpisode object (with PredictionNode) |
| 2 | `CHRON-TASK-GRAMMAR-v1.md` | Function-based naming: observe, prioritize, predict, verify, learn |
| 3 | `CHRON-MCP-ARCHITECTURE-2026-09-18.md` | CHRON MCP tools, FRAME integration, NATS subjects, authority |
| 4 | `CHRON-SIX-LAYER-ARCHITECTURE-2026-09-18.md` | The six layers and dependency chain |
| 5 | `CHRON-ORGAN-NOT-MCP-2026-09-18.md` | Why CHRON is an organ, not an MCP |
| 6 | `CHRON-ORGAN-BOUNDARY-DOCTRINE-2026-09-18.md` | Boundaries with every federation organ |
| 7 | `CHRON-AGENTIC-MEMORY-BOUNDARY-2026-09-18.md` | CHRON vs memory: temporal truth vs behavior change |
| 8 | `CHRON-FINAL-TASK-LEDGER-2026-09-18.md` | Compiled task ledger with all states |

---

## What Exists Today

| Component | Status |
|-----------|--------|
| `chron.py` — ranking engine | ALIVE (truth_score + urgency_score decomposition) |
| `chron_events.json` — event store | ALIVE (5 events, schema validated) |
| `chron_spine_gate.py` — 9-arrow check | ALIVE (6 PASS, 0 FAIL, 3 UNBUILT) |
| `alpha_zen_engine.py` — signal pools | ALIVE (9 domains, freshness gate) |
| NATS :4222 — event bus | LIVE |
| arifFlow :7073 — metabolic plane | LIVE |
| FRAME :18085 — independent observer | LIVE |

---

## What Does NOT Exist Yet

| Component | Why It Matters |
|-----------|---------------|
| ChronEpisode objects | No temporal identity for events |
| Prediction store with verify_at | No prediction → no verification → no learning |
| Verification cron | Predictions float forever without checking |
| Calibration (Brier scores) | No way to measure prediction accuracy |
| CHRON NATS subscription | CHRON doesn't consume organ events |
| CHRON MCP tools | No query API for other organs |
| Lesson extraction | No mechanism to convert errors to lessons |

---

## Your Mission

**Build CHRON as an organ, not as an MCP.**

1. Start with the ChronEpisode schema — derive from real payloads
2. Create the ChronStore (append-only, bitemporal)
3. Wire CHRON as NATS subscriber (observe material change)
4. Create first prediction from existing event
5. Build verification mechanism (check prediction at verify_at)
6. Expose CHRON MCP (query API for other organs)
7. Integrate FRAME as independent witness

---

## Naming Doctrine

**DO NOT** name tasks by artifacts:
```
❌ Generate Executive Briefing
❌ Create Morning Card
❌ Run News Feed
```

**DO** name tasks by function in the causal spine:
```
✅ Observe material change
✅ Prioritize what deserves attention
✅ Predict what we expect
✅ Verify predictions against outcomes
✅ Extract lessons from errors
```

---

## Authority Rules

| Action | Who |
|--------|-----|
| Create episode | CHRON (auto) |
| Create prediction | CHRON (must carry verify_at) |
| Verify prediction | CHRON (after verify_at) |
| Seal prediction | arifOS ONLY |
| Challenge claim | FRAME (independent) |
| Promote lesson to policy | Agentic Memory (requires authority) |

---

## Key Doctrines

- **"Seal the arrows, not the artwork."** — output format is dynamic; PNG/text/voice are renderers
- **"No control may certify itself."** — FRAME can say CHRON is wrong
- **"CHRON depends on arifFlow evidence. arifFlow must not depend on CHRON interpretation."**
- **"A Reality Graph can exist without CHRON. CHRON can exist without Agentic Memory. Agentic Memory can only emerge when CHRON closes Prediction → Verification → Calibration."**
- **"NATS = nervous system. arifFlow = bloodstream. CHRON = temporal cortex."**

---

## Compression

> You are building the temporal cortex of the arifOS federation. Not an MCP. Not a scheduler. Not a memory system. The organ that witnesses how reality changes attention, and how attention changes reality.

---

DITEMPA BUKAN DIBERI ⚒️
