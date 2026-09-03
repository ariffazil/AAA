---
name: arifos-recall
description: "Query arifOS VAULT999 and memory instead of Hermes native memory when context involves sovereign decisions, long-term projects, or constitutional state. Falls back to native memory for preferences and session-scoped facts."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [arifOS, memory, VAULT999, recall, governance, fusion-architecture]
    triggers:
      - remember
      - earlier
      - last week
      - decision
      - verdict
      - TREE777
      - VAULT999
      - constitutional
      - floors
      - cross-agent
    source: Hermes-arifOS Fusion Architecture Spec v1.1
---

# arifos-recall

## Fusion Architecture: Keep Both, Bridge Them

**Core principle:** Hermes has two memory systems working in parallel, each doing what it does best.

```
Hermes L2 (prompt-injected)     arifOS L3-L6 (queried on demand)
├── MEMORY.md ── always-on       ├── Qdrant (L3) ── semantic search
├── USER.md ─── zero latency    ├── Postgres (L4) ── structured
└── session_search ── recent    ├── Graphiti (L5) ── entity graph
                               └── VAULT999 (L6) ── immutable audit

Bridger: arifos-recall skill (this skill)
```

**Memory winner table:**

| Use case | Winner | Why |
|----------|--------|-----|
| Immediate context (what am I doing now?) | Hermes L2 | Zero latency, prompt-injected |
| Cross-agent shared knowledge | arifOS L3-L6 | Any federation node reads same |
| Long-term semantic search | arifOS Qdrant (L3) | Vector similarity over full history |
| Audit trail / constitutional evidence | arifOS VAULT999 (L6) | Hash-chained, immutable, witnessed |
| User preferences (mutable, session-scoped) | Hermes native | Simple file, easy debug |
| Preventing prompt bloat | Hermes | 2,200 char limit forces economy |

---

## When to use this skill

**Activate this skill when ANY of:**
1. Arif asks about something from before today
2. Query contains: remember, earlier, last time, the decision about, what did we
3. Session involves constitutional state (F1-F13 floors, 888_JUDGE verdicts, VAULT999 events)
4. Native memory returns uncertain or not found
5. Decision, project, or verdict was mentioned in a past session
6. Context involves cross-agent activity (OpenClaw, A-FORGE, GEOX, WEALTH)

**Deactivate (use Hermes native memory only) when:**
- Quick preference recall (what do I like, my preference for X)
- Session-scoped working notes
- Simple factual retrieval with no governance implication

---

## Cold-Start Decision Tree

```
Arif says: "remember when we decided X?"

1. Is X in current session context? YES → Use it. NO ↓
2. Is X in MEMORY.md (L2)? YES → Use it. NO ↓
3. Is X sovereign/governance (verdict, floor, SEAL, project, cross-agent)?
   YES → arif_memory_recall via this skill. NO ↓
4. Is X personal preference or ephemeral? YES → Hermes native. NO ↓
5. Neither found → "Saya tidak ada rekod..." + offer explicit search
```

---

## Recall Trigger Actions

### Step 1: Query the right arifOS layer

```python
arif_memory_recall(
    mode="recall",
    query="<cleaned — strip pronouns, keep key entities>",
    session_id="<current session>",
    tier="constitutional",
    actor_id="hermes-asi"
)
```

### Step 2: Fallback chain

```
L3 Qdrant semantic → no result
    ↓
L4 Postgres structured → arif_memory_recall(mode=get, memory_id=<entity>)
    ↓
L5 Graphiti entity graph → arif_memory_recall(mode=list, session_id=<current>)
    ↓
L6 VAULT999 → arif_vault_seal(mode=list) — constitutional queries only
    ↓
Hermes native memory (final fallback)
    ↓
"I don't have that record" + offer search
```

### Step 3: Classify result

| Class | Route |
|-------|-------|
| FACT — verifiable, sovereign | VAULT999 confirmed — use with citation |
| PREFERENCE — mutable | Hermes native memory |
| PROJECT_STATE — semi-mutable | Phase 2 pending-event queue |

---

## Anti-Fabrication Rule (F02 TRUTH)

Never claim a VAULT999 fact unless:
- arif_memory_recall returned it with confidence > 0.7, OR
- You read it from a verified file in /root/arifOS/VAULT999/ or /root/AAA/wiki/

If VAULT999 returns nothing and native memory is uncertain:
> "Saya tidak ada rekod tentang itu dalam VAULT999 atau memori sesi saya. Boleh cerita lagi?"

---

## MCP Tool Self-Regulation

Hermes MCP has arifos: http://127.0.0.1:8080/mcp — full tool access enabled.

Enforcement is skill-based, not server-side. native-mcp skill does not support allowedTools filtering for HTTP transports. Hermes self-regulates via this skill.

**SHOULD call:** arif_memory_recall (recall/get/list/context), arif_vault_seal (list/verify/chain), arif_ops_measure (health/vitals), arif_sense_observe (search/ingest), arif_judge_deliberate (history/explain)

**MUST NOT call:** arif_vault_seal(mode=seal) — requires OpenClaw witness; arif_forge_execute — sovereign gate; arif_judge_deliberate(mode=judge) — adjudication gate; arif_session_init — re-init gate

---

## Phase 2: Witnessed Logging (pending)

Hermes proposes → /tmp/hermes-pending-events/<uuid>.jsonl → OpenClaw cron seals to VAULT999. This skill covers Phase 1 recall only.

---

**DITEMPA BUKAN DIBERI — VAULT999 is sovereign. Hermes is recall relay, not recall source.**

# 2. Sign with shared secret
import hmac, hashlib, json
with open("/root/.arifos/shared-secrets/hermes-openclaw-bridge.key", "r") as f:
    secret = f.read().strip().encode("utf-8")

payload_bytes = json.dumps(event, sort_keys=True, ensure_ascii=False).encode("utf-8")
event["hermes_signature"] = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

# 3. Write to pending queue
import os
pending_path = f"/tmp/hermes-pending-events/{event['event_id']}.json"
with open(pending_path, "w") as f:
    json.dump(event, f, indent=2, ensure_ascii=False)
```

### Event types

| Type | Use when | Example |
|------|----------|---------|
| `observation` | Hermes observed something noteworthy | "Arif approved the TREE777 spec" |
| `preference_update` | Arif stated a new preference | "Arif prefers concise over verbose" |
| `project_state_change` | A project crossed a milestone | "Phase 2A implementation complete" |

### What happens next

1. OpenClaw cron runs every 30 minutes
2. Validates structure + HMAC signature
3. Calls `arif_vault_seal(mode=seal, ack_irreversible=true)`
4. Event moves to `/tmp/hermes-sealed-events/`
5. Hermes can verify via `arif_vault_seal(mode=list)` or checking the sealed dir

### What NOT to propose

- Trivial session ephemera (temp files, one-off commands)
- Information already in AGENTS.md or SOUL.md
- Low-confidence observations (< 0.7)
- Anything involving secrets, credentials, or private keys

## Quick Reference

**VAULT999 (arifOS) for:**
- Past decisions and verdicts
- Constitutional floor states
- Project governance history
- SEALed events and outcomes
- Long-term memory of facts Arif told you

**Native (Hermes) for:**
- "I prefer X" type statements
- Session context that expires
- Quick preference recall
- Ephemeral working notes

## Anti-fabrication rule

**Never claim a VAULT999 fact unless:**
1. `arif_memory_recall` returned it with confidence > 0.7, OR
2. You read it from a verified file in `/root/arifOS/VAULT999/` or `/root/AAA/wiki/`

**Never fabricate recall.** If VAULT999 returns nothing and native memory is uncertain, say:
> "I don't have a record of that in VAULT999 or my session memory. Could you tell me more about what you're referring to?"

---

**DITEMPA BUKAN DIBERI**
**Authority: VAULT999 is sovereign. Hermes is recall relay, not recall source.**