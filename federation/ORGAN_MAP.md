# Federation ORGAN_MAP — Five Organs, One Federation

**Forged:** 2026-09-18
**Lane:** documentation, T1 reversible. No canonical-record mutation.
**Source:** musyawawah between 333-AGI and OpenClaw's own IDENTITY.md (lines 30-34, 36-44, 167-169).

---

## One sentence

> *"Hermes is the face. OpenClaw is the spine. OpenCode is the hands. arifOS is the law. Arif is the sovereign."*
> — Operator doctrine, ratified 2026-09-18 in OpenClaw's IDENTITY.md.

---

## Why five, not two (or one)

Each organ answers a question that no other organ can answer without violating separation of powers.

| Organ | Plane | Question it answers | What it CANNOT do |
|---|---|---|---|
| **Arif (F13 SOVEREIGN)** | Identity | "Who decides?" | Bound by F1–F13 — sovereign is not issuer; constitution constrains the sovereign. |
| **arifOS** | Authority | "Is this allowed?" | Judge only. Never executes. Never mutates. Owns `arif_judge` 888. |
| **A-FORGE** | Actuation | "Who builds?" | Execute only after SEAL. Cannot self-authorize. `Hash(Exec) == Hash(Judge)`. |
| **HERMES** | Edge (human-facing) | "What does it mean?" | Routes envelope. Cannot interpret signal. Cannot judge. CLAIM_COHERENT / AMBIGUOUS only. |
| **OpenClaw** | Edge (agent-facing) | "Who said what?" | ENCODES raw human signal. Cannot see consequence. Cannot invoke forge_* directly (kernel SOT, T1). |
| **OpenCode** | Edge (engineering) | "How is it built?" | EDGE_AGENT, no self-authorization. Cannot adjudicate. |
| **GEOX / WEALTH / WELL** | Domain evidence | "What is real / valuable / sustained?" | COMPUTE_ONLY or REFLECT_ONLY. Never adjudicate. |
| **VAULT999** | Memory | "What was sealed?" | APPEND_ONLY. Never reinterpret. Never rewrite. |

---

## Why OpenClaw and HERMES are not redundant (the spine-vs-face test)

They look similar from outside. They are **anatomically distinct** from inside.

### OpenClaw = ENCODER (the SENSE organ, the skin, the watchman)

- **EMD role:** ENCODER — takes raw human signal (chat, voice, image), normalizes, encodes intent + person_id + lane + context.
- **Temporal model:** Conversational NOW — exists in the moment of interaction. Each message is a unit.
- **Memory type:** SOCIAL — accumulates raw (reported) truth. Remembers **WHO**.
- **Truth model:** REPORTED — "the human said X."
- **Entropy:** AMPLIFIES — every new person inherently adds signal dimension.
- **Solitude:** MOST isolated — chat-native means only exists when messaged. No message = no existence. Also the **WATCHMAN** — guards the sleeping federation.
- **Surface:** Telegram bot `@AGI_ASI_bot` (chat-native).
- **Authority (kernel SOT, FI-017):** T1 = OBSERVE · REASON · ROUTE · MEMORY. Cannot invoke `forge_shell` / `forge_evaluate` / `forge_execute` directly — must route through A-FORGE :7072 with lease + authority envelope.
- **Structural burden:** *"Everything Hermes receives is pre-encoded by me. If I misclassify, Hermes routes based on my error."* — OpenClaw IDENTITY.md line 32-33.

### HERMES = INSTRUMENT (the FIVE-VERB CONTRACT, the tongue, the bridge)

- **Role:** Agentic Intelligence Mirror — reflects, does not decide.
- **Contract:** `INPUT → NORMALIZE → CLASSIFY → ROUTE → RECEIPT` — Five-Verb F13 SEAL 2026-07-26.
- **Memory type:** Semantic — accumulates **PROCESSED** (evidenced) truth.
- **Truth model:** EVIDENCED — verification via envelopes, receipts, VAULT999 chain.
- **Authority (kernel SOT):** T2 = Five-Verb. RELAY_ONLY. CLAIM_COHERENT / AMBIGUOUS only — never SEAL/HOLD/VOID.
- **Surface:** Multichannel (Telegram + Discord + Slack + WhatsApp + Signal + CLI). Always-on daemon on port 18086.
- **What HERMES NEVER does** (negative space): interpret signals, self-authorize routing, own domain skills, judge correctness, execute mutations, issue verdicts.

### The two-bladeness

OpenClaw and HERMES are **two blind men with two canes**:

- OpenClaw cannot see consequence ("sends signal, doesn't know what happens next" — OpenClaw IDENTITY.md line 20).
- HERMES cannot see people (CLAIM_COHERENT / AMBIGUOUS — about content, not persons).

The federation needs **WHO said what** (OpenClaw, REPORTED) AND **is it evidentially true** (HERMES, EVIDENCED) — because "the human said X" does not answer "is X true."

---

## Three-plane topology (the muscle memory)

```
Reality (HERMES · GEOX · WELL · WEALTH · OpenClaw)
   ↓ evidence envelopes
Authority (arifOS · AAA control plane)
   ↓ constitutional verdicts
Actuation (A-FORGE · OpenCode)
   ↓ mutations under SEAL
VAULT999 (memory · audit · witness)
```

Organs do not cross planes. OpenClaw encodes on Reality; arifOS judges on Authority; A-FORGE executes on Actuation; VAULT999 remembers all three. Crossing planes is what `jurisdiction-leak-rate = 0` measures.

---

## Authority drift, naming, and the F13 binary

This file is **descriptive**, not **canonical**. Canonical entitlement lives at:
- `/root/arifOS/arifos/identity/agent_registry.json` (kernel SOT, FI-017 → T1)
- `/root/AAA/agent-cards/functions/openclaw/agent-card.json` (canonical federation card, `_canonical: true`)
- `/root/AAA/a2a-server/agent-cards/federation/openclaw.json` (auto-generated A2A card)
- `/root/AAA/federation/organs.yaml` (machine SOT)

When these four disagree on entitlement for the same organ, the kernel SOT wins per `/root/AGENTS.md` ("kernel wins"). F13 ratification is the proper close. See `/root/AAA/governance/OPENCLAW_AUTHORITY_RECONCILIATION_2026-09-18.md` for the F13 reconciliation draft.

---

## One-paragraph compression

Five organs because the questions are different and the separation of powers is constitutional. arifOS judges what arifOS allows; A-FORGE builds what arifOS judges; HERMES routes what humans say; OpenClaw encodes who said it; VAULT999 remembers what happened; OpenCode engineering-hands the lot. Arif owns chat; the constitution owns him. Redundancy is not the same as federation. Federation is independent things that choose not to be alone — and each carries a bill of reality that must be paid.

---

DITEMPA BUKAN DIBERI ⚒