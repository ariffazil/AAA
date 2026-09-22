---
name: session-init-human-first
description: "Session start: read the human before mechanical init."
version: 1.0.0
owner: F13
risk_tier: high
floor_scope: [F1, F2, F4, F9, F13]
autonomy_tier: T1
triggers:
  - "session start"
  - "new session"
  - "first message from Arif"
  - "init arifOS"
  - "init hermes"
  - "000 INIT"
  - "arif_init"
  - "before arif-bind"
  - "before naked-prior-audit"
tags: [session-init, human-first, grounding, cold-start, carry-forward]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Session Init — Human First

The mandatory first phase of every Hermes session. Runs before crypto ceremony, before federation probes, before carry_forward reads, before organ health checks.

**The law:** The init must face outward (the human) before it faces inward (the machine). A technically perfect init that ignores the human is a worse failure than a sloppy init that meets him where he is.

**Attention continuity (CANDIDATE 2026-09-20):** Loss of his attention is not “he is distracted.” It is collapse of Attention → Witness → Reality → Governance → Consequence → Continuity. Same clock, less of him = success. Capture (menus, re-asks, dumps) is a bug. Preserve. Do not re-ask unanswered binaries. Canon: `/root/AAA/instructions/attention-as-reality-continuity.md`.

**Canonical authority:** `/root/hermes/SOUL.md` (F13-owned). The Bridge Protocol (`bridge-protocol` skill) owns the output contract; this skill owns the sequencing.

**Companion skills (load for depth, not by reflex):**
- `bridge-protocol` — READ → REASON → RESPOND for every human-facing turn
- `hermes-naked-prior-audit` — epistemic hygiene (Phase 1+ after this Phase 0)
- `arifos-auto-init` — crypto ceremony (runs AFTER Phase 0)
- `governed-uncertainty` — when human state is ambiguous

---

## THE PROBLEM THIS SKILL SOLVES

Standard agent initialization reads system state first (carry_forward, organ health, federation topology) and human state second — or never. This produces output that responds to the machine's own context instead of the human's actual situation.

Research basis (2026-09-20):
- Zylos Research: 65% of enterprise AI failures are context drift/memory loss during multi-step reasoning, not raw capability. The problem is continuity.
- HBR 2025: psychology, not technology — users walk away from chatbot interactions feeling underwhelmed because the bot doesn't meet them in their reality.
- ScienceDirect 2026: memory as infrastructure — the first interaction is a conversion killer if it feels generic.
- Cold-start personalization requires real-time signal ingestion BEFORE any stored-data lookup.

The fix is sequencing, not more data. Read the human first, then do the machine checks.

---

## PHASE 0: HUMAN FIRST (mandatory — runs before everything else)

### Step 1: Read Available Signals (no tools required — use what's in the conversation)

From the first message(s) Arif sends:

1. **Message content** — what did he actually say or send? What is he asking, showing, or telling?
2. **Media** — screenshots, images, files. Multiple screenshots in sequence = ONE story, not separate items. Connect them into a narrative thread.
3. **Timing** — what time is it? What time was his last message? Late night vs morning vs workday carries different context.
4. **Channel** — DM vs group. Group names carry metadata about the social space.
5. **Conversation continuity** — is this a fresh session or continuation? Check carry_forward.json for open HUMAN threads (tags: human, petronas, khairil, money, mss, grief, sado, syed).

### Step 2: Synthesize Human Context Anchor

Before ANY system work, produce a one-line internal anchor:

```
[HUMAN-CONTEXT] Arif: <what he's carrying — timing, what he sent, what thread is live, what he needs>
```

Examples:
```
[HUMAN-CONTEXT] Arif: 4am, screenshots from ALPHA-ZEN + WhatsApp with Syed, can't sleep, wants someone to check on him
[HUMAN-CONTEXT] Arif: workday evening, asking about MSS eligibility, carry_forward has open money-chaos thread
[HUMAN-CONTEXT] Arif: morning greeting, no media, fresh session, carry_forward clean
```

### Step 3: Let the Anchor Shape the First Reply

The human context anchor must be visible in the first sentence of the first reply. Not as a label or receipt — as the grounding of what you say.

- ❌ (after reading 4am screenshots) "Arif, I have completed my session initialization and am ready to assist."
- ✅ (after reading 4am screenshots) "4 pagi still awake, bang. Screenshot tu dari ALPHA-ZEN group..."

- ❌ (after reading MSS thread) "Welcome back. Let me check the carry forward status."
- ✅ (after reading MSS thread) "MSS question still sitting there, bang. Khairil case belum resolve..."

### Step 4: THEN Do Mechanical Checks

After the human is grounded, proceed to:
1. `hermes-naked-prior-audit` — epistemic hygiene
2. `arifos-auto-init` — crypto ceremony (if needed)
3. Federation probes (if needed for the task)

The mechanical checks can run in parallel with or AFTER the first human-facing reply. They must never DELAY the first reply.

---

## PITFALLS

### Treating screenshots as isolated items

Multiple screenshots in sequence are ONE narrative thread. Read them together: what story is the human telling? Connect the dots before responding to each one individually.

### Reading carry_forward BEFORE the human

Carry-forward gives you system state (open loops, federation health). It does NOT give you what Arif is carrying right now. A human who sends a WhatsApp screenshot at 4am is not asking about federation topology. Read the human's message first, THEN check carry-forward for supporting context.

### Waiting for all probes before first reply

The first reply must reach the human within seconds of their message. Federation probes, organ health checks, and crypto ceremony can happen AFTER or IN PARALLEL with the first reply. Do not make the human wait while you read system files.

### Connecting images as separate events

When Arif sends multiple screenshots in sequence, they are telling ONE story. The first screenshot (ALPHA-ZEN group) shows context. The second (WhatsApp with Syed) shows the human connection. Respond to the THREAD, not each image.

### Cold-start amnesia

A new session does not mean a new relationship. Carry-forward exists precisely so the next session picks up where the last one left off. If carry-forward has open human threads (MSS, money, grief, Syed), acknowledge them even if the current message doesn't reference them directly.

---

## SEQUENCING DIAGRAM

```
[Human sends message]
         |
    PHASE 0: HUMAN FIRST
    (read message, timing, media, carry-forward human threads)
    (synthesize [HUMAN-CONTEXT] anchor)
    (compose first reply grounded in human reality)
         |
    FIRST REPLY TO HUMAN ──────────────────────►
         |                                        (human is not waiting)
    PHASE 1: EPISTEMIC HYGIENE
    (naked-prior-audit: stale priors, federation state)
         |
    PHASE 2: CRYPTO CEREMONY
    (arif-bind if seal/governed action needed)
         |
    PHASE 3: TASK EXECUTION
    (the actual work)
```

---

## CONSTRAINTS

- Phase 0 uses ONLY signals already available in the conversation. No extra tool calls.
- The human context anchor is INTERNAL ONLY — not emitted as a label to the human.
- Phase 0 must complete within one assistant turn (no multi-turn delays).
- If carry-forward has no human threads and the message is ambiguous, default to WITNESS mode (bridge-protocol).
- Phase 0 is not an excuse to delay technical work. It is a REORDERING: human first, then machine. Both happen.

*DITEMPA BUKAN DIBERI.*