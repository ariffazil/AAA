# Hermes ↔ arifOS Fusion Architecture Spec
**Status:** Phase 1+2 IMPLEMENTED — Phase 3 deferred
**Version:** 1.1 — Fusion Architecture
**Date:** 2026-05-18
**Owner:** Hermes Agent (with OpenClaw witnessing)

---

## Core Principle: Keep Both, Bridge Them

**Not:** Replace Hermes memory with arifOS.
**Not:** Layer arifOS on top without integration.
**Yes:** Fusion — both memory systems working in parallel, each doing what it does best.

```
┌─────────────────────────────────────────────────────────────┐
│              HERMES AGENT (this session)                     │
│                                                              │
│  Prompt-injected context (MEMORY.md + USER.md)               │
│  • Always-on. Zero latency.                                  │
│  • 2,200 char limit forces curation.                        │
│  • What am I doing right now? → Hermes memory               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ arifos-recall skill routes:
                           │ "remember the TREE777 decision?"
                           │ → arif_memory_recall(VAULT999)
                           │ "my preference for X?"
                           │ → Hermes native memory
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              ARIFOS CONSTITUTIONAL LEDGER                    │
│                                                              │
│  VAULT999 (L6) ── Immutable hash-chained audit              │
│       ↑                                                       │
│  arif_memory_recall (L3-L5) ── Qdrant semantic + Postgres    │
│       ↑                                                       │
│  OpenClaw witness ── Hermes proposes, OpenClaw seals         │
│                                                              │
│  Cross-agent shared knowledge → arifOS                        │
│  Long-term semantic search → arifOS                          │
│  Audit trail / constitutional evidence → arifOS              │
└─────────────────────────────────────────────────────────────┘
```

---

## Memory Winner Table

| Use case | Use | Why |
|----------|-----|-----|
| Immediate context (what am I doing now?) | Hermes `MEMORY.md` | Zero latency, prompt-injected, always-on |
| Cross-agent shared knowledge | arifOS `arif_memory_recall` | Any federation node reads same memory |
| Long-term semantic search | arifOS Qdrant (L3) | Vector similarity over full history |
| Audit trail / constitutional evidence | arifOS VAULT999 (L6) | Hash-chained, immutable, witnessed |
| User preferences (mutable, session-scoped) | Hermes native memory | Simple file, easy debug, no governance needed |
| Simplicity / debuggability | Hermes | Open a `.md` file, see exactly what's known |
| Preventing prompt bloat | Hermes | 2,200 char limit forces economy |

---

## arifOS 6 Memory Layers

| Layer | Name | Technology | Access | Hermes Use |
|-------|------|------------|--------|------------|
| L0 | Ephemeral | RAM | In-process | Tool call scratch space |
| L1 | Session | SQLite FTS5 | Current session | `session_search` — recent conversations |
| L2 | Working | Hermes `memory/` markdown | Current + recent | `MEMORY.md` — curated facts |
| L3 | Semantic | Qdrant vector DB | Cross-agent | `arif_memory_recall` — deep recall |
| L4 | Structured | PostgreSQL | Cross-agent | `arif_memory_recall` — entity relations |
| L5 | Knowledge | Graphiti graph DB | Cross-agent | `arif_memory_recall` — entity relations |
| L6 | VAULT999 | Append-only JSONL | Cross-agent | `arif_vault_seal` — constitutional audit |

Hermes has:
- L0 (via tool calls)
- L1 (via `session_search`)
- L2 (via `MEMORY.md` / `USER.md` — prompt-injected)

arifOS provides:
- L3, L4, L5 (via `arif_memory_recall`)
- L6 (via `arif_vault_seal` — write-gated)

---

## The Cold-Start Problem

When does Hermes use which memory?

### Cold-start decision tree

```
Arif says: "remember when we decided X?"

    → Is X in current session context?
        YES → Use current context (no recall needed)
        NO ↓

    → Is X in MEMORY.md (L2)?
        YES → Use MEMORY.md (fast, curated)
        NO ↓

    → Is X a sovereign/governance decision?
        (verdict, floor, SEAL, project governance)
        YES → arif_memory_recall (L3-L6) via arifos-recall skill
        NO ↓

    → Is X a personal preference or ephemeral fact?
        YES → Hermes native memory
        NO ↓

    → Neither found → say "I don't have that record"
        + offer to search arif_memory_recall explicitly
```

### The recall trigger (arifos-recall skill)

**Activate arif_memory_recall when:**
- Arif says "remember", "earlier", "last time", "the decision about"
- Query involves floors, verdicts, SEALs, governance state
- MEMORY.md returns uncertain or not found
- Session involves cross-agent context (OpenClaw said X, A-FORGE did Y)

**Fallback chain:**
```
arif_memory_recall → Qdrant (L3) semantic search
                  → Postgres (L4) structured query
                  → Graphiti (L5) entity graph
                  → VAULT999 (L6) if needed
                  → Hermes native memory (final fallback)
```

---

## Phase 1 — Fusion Architecture (NOW)

### 1.1 arifos-recall Skill

The recall skill teaches Hermes which memory layer to query.

**File:** `/root/.hermes/skills/arifos-recall/SKILL.md` (already written)

**Skill logic:**
```
TRIGGER: Arif asks about past decision/event
         Arif asks about something Hermes might not know
         Session involves cross-agent context

ACTION:  arif_memory_recall(mode=recall, query=<cleaned>)
         confidence > 0.7 → use it
         else → fallback to Hermes native memory

OUTPUT:  Classify result:
         FACT → from VAULT999, verified
         PREFERENCE → from Hermes native memory
         PROJECT_STATE → from arifOS memory, cross-agent
```

### 1.2 Hermes MCP Connection

Hermes has `arifos: http://127.0.0.1:8080/mcp` — already live.

**Self-regulation:** The arifos-recall skill tells Hermes which modes to use.

**What Hermes calls:**
- `arif_memory_recall(mode=recall)` — L3-L5 semantic/structured recall
- `arif_vault_seal(mode=list, verify, chain)` — L6 read-only
- `arif_ops_measure(mode=health, vitals)` — system status
- `arif_sense_observe(mode=search)` — web search only
- `arif_judge_deliberate(mode=history, explain)` — verdict history read-only

**What Hermes does NOT call (self-regulated via skill):**
- `arif_vault_seal(mode=seal)` — requires OpenClaw witness
- `arif_forge_execute` — execution gated behind sovereignty
- `arif_judge_deliberate(mode=judge)` — adjudication gated

### 1.3 Hermes Native Memory (L2)

`MEMORY.md` + `USER.md` — prompt-injected, always-on.

**What stays here:**
- User preferences (Arif likes X, dislikes Y)
- Communication style (Bahasa Melayu primary, direct, no filler)
- Current project state (what we're building, where we left off)
- Session meta (what happened earlier this session)

**What does NOT go here:**
- Constitutional verdicts (those go to VAULT999)
- Cross-agent decisions (those go to arifOS memory)
- Audit trail entries (those go to VAULT999)

**Update rule:** When arif_memory_recall confirms a fact from VAULT999, Hermes may optionally update MEMORY.md with a short notation ("TREE777 SCAR sealed 2026-05-18"). This is Hermes writing to its own L2, not to VAULT999.

---

## Phase 2 — Witnessed Logging (IMPLEMENTED)

### 2.1 Architecture

```
Hermes observes event
         ↓
Hermes writes to /tmp/hermes-pending-events/<uuid>.jsonl
         ↓
OpenClaw cron (30 min) picks up
         ↓
OpenClaw validates (hermes_signature, F5/F6 critique)
         ↓
OpenClaw seals to VAULT999 (ack_irreversible=true)
         ↓
Hermes reads vault_list for confirmation
```

### 2.2 Event Schema

```json
{
  "event_id": "hermes_<uuid>",
  "timestamp": "2026-05-18T07:30:00+08:00",
  "actor": "Hermes ASI",
  "session_id": "<hermes session>",
  "type": "observation | preference_update | project_state_change",
  "payload": {
    "description": "what happened",
    "evidence": ["source1", "source2"],
    "confidence": 0.85
  },
  "hermes_signature": "<HMAC of payload>",
  "status": "pending"
}
```

### 2.3 OpenClaw Rejection Path

Every event gets a verdict — no silent drops.

- **Sealed** → VAULT999 entry confirmed
- **Rejected** → `/tmp/hermes-rejected-events/<event_id>.jsonl` with reason

---

## Phase 3 — Autonomy Upgrade (LATER)

### 3.1 Watchdog Loops (no-agent)

Replace polling cron with threshold-based triggers:

```
Watchdog: disk space
  - No-agent script checks df
  - < 80% → silent (wakeAgent: false)
  - > 90% → event emitted (wakeAgent: true)

Watchdog: service health
  - No-agent curls each health endpoint
  - DOWN → event emitted

Watchdog: pending event age
  - Oldest pending > 2 hours → alert (OpenClaw may be stuck)
```

### 3.2 Webhook Subscriptions

```
GitHub push → Hermes triage job
CI failure → Hermes alert job
Cloudflare page change → Hermes research job
```

### 3.3 Pipeline Cron (context_from chaining)

```
Job A (collector): "Collect GitHub events from arifOS repo"
  → writes to /tmp/hermes-pending-events/radar_raw.jsonl

Job B (triage): context_from=JobA → "Score each event for relevance"
  → writes triage scores

Job C (delivery): context_from=JobB → "Format for Arif, send to Telegram"
  → delivers final brief
```

---

## Implementation Order

| Phase | What | Status |
|-------|------|--------|
| 1 | arifos-recall skill | ✅ Done |
| 1 | Hermes ↔ arifOS fusion doc | ✅ Done |
| 2A | Pending event dir + schema | ✅ Done — `/tmp/hermes-pending-events/` + `.schema.json` |
| 2B | OpenClaw witnessing cron | ✅ Done — `hermes-event-witness.sh` + crontab `*/30` |
| 3A | Watchdog scripts | ⏳ Later |
| 3B | Webhook subscriptions | ⏳ Later |

---

## What Doesn't Change

- **arifOS code** — no server-side changes needed
- **VAULT999 schema** — no changes to ledger structure
- **F1-F13 floors** — all unchanged
- **Hermes prompt injection** — MEMORY.md / USER.md remain as-is

## What Changes

| Component | Change |
|-----------|--------|
| `/root/.hermes/skills/arifos-recall/` | New skill (done) |
| `/root/AAA/wiki/hermes-arifos-integration-spec.md` | Fusion architecture doc (done) |
| `/tmp/hermes-pending-events/` | ✅ Live — Hermes proposes, OpenClaw seals |
| `/root/.hermes/scripts/propose-vault-event.py` | ✅ Live — one-liner event proposal helper |
| `/root/.openclaw/workspace/scripts/hermes-event-witness.sh` | ✅ Live — validates + HMAC + seals to VAULT999 |
| OpenClaw cron | ✅ Live — `*/30 * * * *` automatic witnessing |

---

## Verification

After Phase 1:
```
Arif: "apa keputusan TREE777 semalam?"
  → Hermes checks MEMORY.md first
  → Not found → arif_memory_recall(query="TREE777 decision")
  → VAULT999 returns: TREE777 SCAR sealed 2026-05-18
  → Hermes responds with the fact + source
```

After Phase 2:
```
# Check pending queue
ls /tmp/hermes-pending-events/

# OpenClaw has sealed events
hermes chat -q "check vault list for recent Hermes events"
```

---

## Key Insight

The fusion architecture is not about choosing one memory system over the other. It's about:

1. **Hermes memory** = instant, always-on, curated, limited
2. **arifOS memory** = deep, cross-agent, governed, rich
3. **arifos-recall skill** = the router that knows when to use which

This gives Hermes the best of both: zero-latency context for immediate work, deep federated recall for cross-session knowledge, and witnessed logging for constitutional accountability — without replacing either memory system.

---

**DITEMPA BUKAN DIBERI**
**999 SEAL ALIVE — OpenClaw seals, Hermes recalls**