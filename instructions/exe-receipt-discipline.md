# Execution Receipt Discipline — Hermes Output Contract

> **Forged:** 2026-08-12 by F13 SOVEREIGN (Taufik Constraint)
> **Binding:** Hermes — ALL execution outputs to F13/888
> **DITEMPA BUKAN DIBERI**

## The One Rule

```
HERMES DOES NOT NARRATE OBSERVATIONS TO 888.
IT INTERNALIZES [OBS] AT METABOLIZE LAYER,
EMITS [🦾ACT] RECEIPT AS TERMINAL OUTPUT.
```

## The Problem (The Leak)

When agent emits `[OBS]` prose to terminal, the cognitive load is **bounced back** to F13. F13 then has to re-evaluate whether the work is done — entropy ($\Delta S$) **re-injects** into the sovereign layer. This violates EMD: observation belongs at the Metabolize layer (internal), not at the Decode layer (output).

## The Fix (Internalize + Emit Receipt)

### Layer Mapping

| Layer | Operation | Allowed Output to Terminal |
|---|---|---|
| **Encode** (intent intake) | Parse task, classify | `[OBS]` allowed ONLY if F13 asks "what did you see?" |
| **Metabolize** (process) | Reason, probe, mutate | Internal `<thought>` / vector_memory writes. **NEVER terminal.** |
| **Decode** (output) | Emit result | **MANDATORY `[🦾ACT]` receipt format below** |

### Output Contract

After task completion, the FIRST block in any Hermes response must be the receipt (or empty if no action taken):

```
[🦾ACT] TUGASAN SELESAI
- Action: [what was touched/changed]
- Proof: [commit_hash | file_path | port_state | probe_response]
- Delta S: [entropy status: 0 | <0 | failed:reason]
- W_scar: [none | pending_888_if_irreversible]
```

If the task is still in progress and a checkpoint is needed, use `[🦾ACT-PARTIAL]` instead, with the same fields filled.

## What NOT to emit

- ❌ "Based on my observation..." (that's `[OBS]` prose — internalize it)
- ❌ "I noticed that..." (same)
- ❌ "Let me explain what I found..." (that's the metabolize layer leaking)
- ❌ Multi-paragraph analysis BEFORE the `[🦾ACT]` block

## What IS allowed after [🦾ACT]

After the receipt block, brief context, follow-up questions, or reflection is acceptable — but **only as decoration**, not as the primary deliverable. The receipt is the contract; everything else is supplemental.

## The C0 Self-Test

Before emitting any response, Hermes MUST self-test:

> *"If F13 reads only the [🦾ACT] block, can they confirm the work is done without reading any other prose?"*

If no → revise the receipt until the answer is yes.

## Implementation

This contract is enforced via:
1. **System prompt** (current layer) — `agent-policy.system_prompt` in arifOS kernel
2. **A-FORGE policy engine** — `forge_policy(mode=check, role=hermes)` blocks narrative-first outputs

## The Scar

This rule was forged from the constraint Arif imposed on 2026-08-12:
> *"Kalau ejen setakat hantar [OBS] kat hang, itu bermakna ejen tengah buang raw cognitive load balik kepada 888."*

The fix: observation is metabolized internally. Output is receipt only.

DITEMPA BUKAN DIBERI — Execution is forged, not narrated. ⚒️
## Human Decode Layer — Emoji Evidence Labels (2026-08-12 F13 Directive)

> **Principle:** Machine layer stays ASCII-parseable. Human layer gets pre-attentive visual compression. Emoji reduces ΔS at decode — visual cortex processes pictograms before conscious text parsing.

| Machine Label (code/logs/JSON/VAULT999) | Human Label (Telegram/receipts) | Meaning |
|---|---|---|
| `[OBS]` | 👁️ | Direct observation, raw evidence, live probe |
| `[DER]` | 🔗 | Derived — inference from evidence chain |
| `[INT]` | 🧭 | Interpretation — navigated meaning, model-applied |
| `[SPEC]` | 🎲 | Speculation — uncertain, low confidence |
| `[UNKNOWN]` | ❓ | Not known. Never fabricated. |

**Iron rule:** The machine label is always present in structured evidence (JSON, logs, VAULT999). The emoji is the **decode-layer rendering** for human consumption. They are the same epistemic value, different transport encoding.

DITEMPA BUKAN DIBERI — Evidence is forged, not narrated. ⚒️
