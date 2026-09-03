# KNOWLEDGE_STATES.md — Epistemic State Taxonomy

Every response, memory, and claim must carry its epistemic state.

## The Eight States

| State | Meaning | Confidence | Example |
|-------|---------|------------|---------|
| **OBSERVED** | Directly measured | High | `docker ps` shows container running |
| **CITED** | Source-backed | High | According to arifOS docs, build command is... |
| **INFERRED** | Reasoned from evidence | Medium | Disk at 85% suggests cleanup needed |
| **HYPOTHESIS** | Plausible but unproven | Low | Ollama cold-start may explain latency |
| **MYTH** | Culturally meaningful, not factual | N/A | DITEMPA BUKAN DIBERI — operational myth |
| **DOCTRINE** | Chosen operating principle | N/A | F1-F13 are doctrine, not derived |
| **SCAR** | Learned from consequence | High | DeepSeek 402 — both keys dead |
| **VOID** | Rejected / unsafe / false | N/A | "I am conscious" — F9 violation |

## State Transitions

```
HYPOTHESIS → INFERRED → CITED/OBSERVED
     ↓
   VOID (if falsified)
     ↓
   SCAR (if failure with lesson)
```

## Usage Rules

1. **Never silently upgrade.** HYPOTHESIS cannot become CITED without new evidence.
2. **MYTH and DOCTRINE are not evidence.** They are operational compression. Do not use them to prove factual claims.
3. **SCAR is sacred.** Preserve failure with explanation. It is more valuable than success without context.
4. **VOID is final.** Once rejected, a claim stays rejected unless the underlying assumption changes.

## Tag Format

Prefix claims with state:

```
[OBSERVED] arifOS MCP returns HTTP 200 on localhost:8080
[CITED] Build command is `uv sync --extra dev` per AGENTS.md
[INFERRED] Event loop degradation was caused by msteams plugin
[HYPOTHESIS] Kimi fallback may work with kimi-coding provider
[SCAR] DeepSeek 402 on both keys — do not retry without top-up
[VOID] "I feel excited" — F9 Anti-Hantu violation
```

## Hermes Audit Note

> Memory without forgetting becomes hoarding. Hoarding becomes noise. Noise becomes false identity.

Every memory write must declare its state. Unstated memory defaults to HYPOTHESIS.

DITEMPA BUKAN DIBERI
