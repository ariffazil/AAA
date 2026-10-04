# Sabar / Summarize Mode — Arif's Checkpoint Signal

When Arif says "sabar dulu la" / "summarize" / "just summarize untuk aku apa yang dah berlaku" — it is a **style-flip signal**, not a request for elaboration. The conversation has moved from investigation to checkpoint.

## What changed

- Drop all tables, options, decision matrices.
- Drop the "what should we do next" framing.
- Lead with a **one-line verdict** of what just happened.
- Then a numbered chronology of the session's actions (5-8 items max).
- Then "what's left" or "what was deferred" — only if material.
- No "nak aku patch?" / "proceed?" / "should I?" — autonomous execution within T1/T2 is the default.

## Example (from this session 2026-08-06)

**Trigger:** After 6+ turns including PDF reading, kernel probe, corpus verification, Ollama/FLAME test, and constraint enumeration, Arif said "Sabar dulu la. Just summarize untuk aku apa yang dah berlaku."

**Wrong response:** Re-state the constraint table, list options, ask "nak aku patch apa?"

**Right response (sent):**

> **Ringkasan:**
> Kau hantar PDF "Constitutional AI Framework Research" — GAP 3b specification untuk i-ARIF. Aku baca, verify, dan propose wire Ollama sebagai judge sebelum spend GPU.
>
> **Apa yang berlaku:**
> 1. PDF dibaca — 5 crisis scenario, Pydantic EMD, Merkle sealing. Spec, bukan code.
> 2. Live state verified — kernel ready (8 tools, 13 floors, VAULT999). `ml_method: heuristic`.
> 3. Arif clarified — I-ARIF = 888-APEX judge (1.5-3B), bukan generator.
> 4. Aku proposed Ollama proof-of-concept (qwen2.5:3b, free, CPU).
> 5. Doing agent probed — judge.py 3233 lines, deterministic pipeline, flip point at `ARIFOS_ML_FLOORS`.
> 6. Tested live — 2/4 Ollama probes pass (~3s short, 180s+ timeout long). FLAME alternative measured at 1s.
>
> **Keputusan:** qwen2.5:3b produces correct verdicts, tidak diwire ke kernel. Kau cakap sabar dulu.
>
> **Yang belum:** wiring Ollama, training I-ARIF, atau perubahan apa-apa. Semua read-only.

## Why this matters

When Arif says "sabar / summarize", he is signaling:

1. **Token budget** — the conversation has burned enough; compress.
2. **Decision fatigue** — he just wants the lay of the land, not more options.
3. **Check point, not check mate** — the work pauses here, may resume later.
4. **No A/B/C** — don't offer choices; offer "what's left if you say yes."

The 8-bullet chronology is the right granularity: enough to resume, not enough to drown.

## Pitfall

- Do NOT include "next steps" or "should I do X?" — that's the question-permission pattern. State what remains as facts, not requests.
- Do NOT include a new ROI table — only relevant after a task is done, not after a checkpoint.
- Keep it in Bahasa Malaysia (or Malay-English mixed) when Arif uses Bahasa — the language match signals "I heard you, I respect your pace."
- The session ended with `Nothing to save.` becoming a real option — but in this session, the durable learnings (Ollama/FLAME latency, I-ARIF scope clarification, sabar-mode signal) were captured in `i-arif-corpus-ops` skill and `arifos-integration-recon` references.
