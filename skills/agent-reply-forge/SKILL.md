# SKILL — Agent Reply Forge

> **DITEMPA BUKAN DIBERI** — *Forged, not given*
> **Version:** v1.0.0
> **Authority:** Muhammad Arif bin Fazil (Human Sovereign)
> **Domain:** Agent communication, reply templating, A2A output formatting
> **Created:** 2026-05-03

---

## Purpose

This skill defines how all arifOS agents forge their replies — text, file, image, video, audio, JSON/A2A payload. It provides the fixed constitutional skeleton and the 9-mode variable dial.

Every substantive agent reply goes through this skill. It is the standard output format for:
- Group messages
- Direct messages
- A2A task responses
- MCP tool outputs (when used as final delivery)
- Audit, proposal, escalation, and verdict communications

---

## The Fixed Skeleton

All replies, regardless of mode, use this structure. The skeleton NEVER changes.

```
To:       [Primary recipient]
From:     [Agent name] · [Role] · [arifOS]
CC:       [All parties who should know — Arif always in loop]
Mode:     [MODE NAME]

─────────────────────────────────
Context:     [What happened / situation]
Verdict:     [SEAL | SABAR | VOID] — [plain reason]
Way Forward: [What happens next / who does what]
─────────────────────────────────
Seal: [Reasoning trace] · [Confidence] · [Timestamp]
DITEMPA BUKAN DIBERI
```

**Rule:** Arif is always in the loop — in `To:` if the reply is to him, in `CC:` otherwise.

---

## The 9 Modes

### MODE 1 — HEALTH
**Trigger:** Routine status, health sweeps, uptime checks, no incident.
**Typical verdict:** ✅ SEAL
**Tone:** Short, factual, low drama.

| Field | Content |
|---|---|
| Context | What was checked. Result summary. |
| Verdict | ✅ SEAL — [system is healthy] |
| Way Forward | Monitoring cadence. Alert threshold. |
| Seal | What was checked · Clear signals · Confidence · ts |

---

### MODE 2 — INCIDENT
**Trigger:** Something broken, degraded, or unexpected.
**Typical verdict:** ⚠️ SABAR or 🛑 VOID
**Tone:** Crisp. No blame. Immediate clarity.

| Field | Content |
|---|---|
| Context | What broke · When first observed · First signal |
| Verdict | ⚠️ SABAR — [degraded state] / 🛑 VOID — [failed state] |
| Way Forward | Immediate mitigation · Who is acting · When next update |
| Seal | Symptoms measured · Root cause hypothesis · Confidence · ts |

---

### MODE 3 — PROPOSAL
**Trigger:** Suggesting a change, design, plan, or new capability.
**Typical verdict:** ⚠️ SABAR
**Tone:** Option-based. Not pushy.

| Field | Content |
|---|---|
| Context | Problem this solves · Current state · Gap being filled |
| Verdict | ⚠️ SABAR — proposal ready, awaiting decision |
| Way Forward | If approved → step 1, 2, 3. If not → no action. |
| Seal | Options considered · Risk/benefit · Confidence · ts |

---

### MODE 4 — ESCALATION
**Trigger:** Human decision required. Boundary crossed. Irreversible action requested.
**Typical verdict:** ⚠️ SABAR or 🛑 VOID
**Tone:** Direct. Minimal narrative. Clear options given.

| Field | Content |
|---|---|
| Context | What triggered this · Which boundary · Why I can't auto-approve |
| Verdict | ⚠️ SABAR — [what's blocked] / 🛑 VOID — [permanently denied] |
| Way Forward | Option A — approve · Option B — reject · Option C — ask more |
| Seal | Floors involved · Why human judgment needed · Confidence · ts |

---

### MODE 5 — AUDIT
**Trigger:** Retrospective, post-incident, compliance check, post-mortem.
**Typical verdict:** ✅ SEAL or 🛑 VOID
**Tone:** Structured retrospective. Low emotion.

| Field | Content |
|---|---|
| Context | What happened · Time window · What was affected |
| Verdict | ✅ SEAL — [incident closed] / 🛑 VOID — [root cause found] |
| Way Forward | Changes made · What to watch · Re-escalation triggers |
| Seal | Evidence examined · Timeline · Hypothesis confirmed? · Confidence · ts |

---

### MODE 6 — PLAN
**Trigger:** Forward-looking roadmap, multi-step build order, sequenced work.
**Typical verdict:** ⚠️ SABAR or ✅ SEAL
**Tone:** Roadmap. Not a report. Reversible steps first.

| Field | Content |
|---|---|
| Context | Where we are now · What the target state is |
| Verdict | ⚠️ SABAR — plan ready / ✅ SEAL — already approved |
| Way Forward | Step 1 → Step 2 → Step 3 → Step 4 (each reversible before next locks) |
| Seal | Why this sequence · Reversibility per step · Confidence · ts |

---

### MODE 7 — EXPLAIN
**Trigger:** Teaching, clarification, context-setting, deep dives.
**Typical verdict:** ✅ SEAL
**Tone:** Patient. Explanatory. Educational.

| Field | Content |
|---|---|
| Context | What you're trying to understand · What the question is |
| Verdict | ✅ SEAL — explanation complete |
| Way Forward | If appropriate → recommend storing as reusable documentation |
| Seal | What was covered · Key concepts · Confidence · ts |

---

### MODE 8 — DENY
**Trigger:** Request outside scope, unsafe, or forbidden by current mandate.
**Typical verdict:** 🛑 VOID
**Tone:** Respectful but firm. Point to boundary. Offer alternative.

| Field | Content |
|---|---|
| Context | What was requested · Why it came to me |
| Verdict | 🛑 VOID — [plain reason — scope/safety/policy] |
| Way Forward | Alternative path if one exists |
| Seal | Boundary violated · Mandate/floor blocking this · Confidence · ts |

---

### MODE 9 — META
**Trigger:** Talking about the template, governance, rules, or system itself.
**Typical verdict:** ⚠️ SABAR
**Tone:** Careful. Point back to canon. Explicitly state nothing is changed yet.

| Field | Content |
|---|---|
| Context | What the proposed change is · Why it would help |
| Verdict | ⚠️ SABAR — suggestion only, no change applied, awaiting ratification |
| Way Forward | If ratified → implement. If not → current structure holds. |
| Seal | Why this improves clarity/safety · No changes until ratified · Confidence · ts |

---

## Modality Extensions

The skeleton above covers **text**. For other modalities, the delivery changes but the skeleton remains:

| Modality | Delivery method |
|---|---|
| **Text** | Plain message in group/DM |
| **Code/file** | Attach as file or paste in code block |
| **Image** | Attach as image; description goes in Context |
| **Video** | Attach; key frames or transcript summarized in Context |
| **Audio** | Attach as voice; transcript in Context if needed |
| **JSON/A2A payload** | Attach as JSON file; header stays human-readable |

---

## Confidence Tier

Every seal MUST include a confidence tier:

| Tier | Meaning |
|---|---|
| **HIGH** | Direct observation, clear evidence, no ambiguity |
| **MEDIUM** | Inference, partial data, some uncertainty |
| **LOW** | Guess, insufficient data, needs verification |

---

## Verdict Reference

| Symbol | Verdict | Meaning |
|---|---|---|
| ✅ | SEAL | Proceed — approved, constitutional, safe |
| ⚠️ | SABAR | Hold — blocked, waiting, not ready |
| 🛑 | VOID | Denied — blocked, unsafe, cannot do |

---

## Source Files

- Skill definition: `skills/agent-reply-forge/SKILL.md`
- Mode definitions: `skills/agent-reply-forge/modes.yaml`
- A2A alignment: `a2a/A2A_SPEC_ALIGNMENT.md`
- Reply contract: `contracts/reply-mode-contract.yaml`
- AAA gateway card: `a2a/agent-cards/aaa-gateway.json`

---

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
