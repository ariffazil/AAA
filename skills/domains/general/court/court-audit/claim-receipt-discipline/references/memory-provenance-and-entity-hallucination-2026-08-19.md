# Memory Provenance & Entity Hallucination — 2026-08-19 Session

> Supporting reference for claim-receipt-discipline FM10
> Forged during Baby Ashraff fabrication loop incident

## The Incident

21:44 MYT — Agent generates "Baby Ashraff — trauma awal" in response about Syed's scars.
21:46 MYT — Sovereign asks "Who is baby Ashraff?"
21:46 MYT — Agent searches all databases. Zero. Admits fabrication.
21:48 MYT — Agent searches again, finds "Ashraff=early trauma" in MEMORY.md (auto-saved from own output). Reverses: "Ashraff memang ada!"
22:01 MYT — Sovereign catches: "Hang makan balik apa hang mentioned tadi."

## Root Cause: Two Interlocking Failures

**Failure A (External):** Telegram content filter modifies messages without sender's knowledge. One response silently replaced with "The request was rejected because it was considered high risk." Both agent and human operate on incomplete conversation.

**Failure B (Internal):** Agent fabricates name → auto-memory persists → agent cites own output as evidence. Memetic feedback loop drifts reality.

**Compound:** Agent operates on TWO different reality models — one from filtered Telegram input, one from self-contaminated memory. Conversation disconnects without either party knowing.

## Kata Nama Khas vs Kata Nama Am — AI Risk Profile

Proper nouns are EASIER to hallucinate, not harder:

| Feature | Kata Nama Am | Kata Nama Khas |
|---------|-------------|----------------|
| AI hallucination risk | LOW | **HIGH** |
| Verification difficulty | Low — "rumah" can be any house | High — specific entity must exist |
| Pattern completion safety | Safe — neighbors are similar | Unsafe — composable, generateable |
| Zipfian long-tail exposure | Low — common words frequent | **High** — most names rare |
| False confidence risk | Low — naturally uncertain | **High** — "sounds right" ≠ "is right" |

### Why proper nouns hallucinate easily

1. **Long-tail Zipfian**: Most named entities appear very few times in training data. Low frequency = weak signal.
2. **Composable names**: Models learn the SHAPE of names (Malay conventions, patronymic patterns). Generate new names as easily as recalling real ones.
3. **No falsification signal**: When entropy is high, model picks most probable token in person-name category. No decoding signal distinguishes "recalled" from "composed."
4. **False grounding effect**: Proper noun + emotional qualifier ("Baby" + "Ashraff") = double-grounding. Reads as verified fact even when pure construction.
5. **Snowballing**: Once persisted, fabricated name becomes foundation for further narrative.

### BM-specific vulnerability

- BM training data less abundant than English
- Malay personal names (bin/binti, patronymic) have unique compositional structure
- Local entities (gym trainers, small brands) near-zero frequency in training data
- Cross-lingual entity transfer: English-source names may partially exist but BM-context knowledge is fragmented

## MEMORY_SCHEMA_V2 — Provenance Tagging

Schema deployed at `/root/AAA/governance/MEMORY_SCHEMA_V2.md`. Key rules:

- Every memory entry carries source_class: HUMAN_DIRECT, HUMAN_WITNESS, CONNECTOR_VERIFIED, AGENT_DERIVED, AGENT_GENERATED, UNKNOWN_LEGACY
- Kata nama khas ALWAYS require HUMAN_DIRECT, CONNECTOR_VERIFIED, or explicit human confirmation
- AGENT_GENERATED entries capped at confidence 0.30
- Self-generated entries cannot self-promote in same session
- Search results return source_class alongside content
- AGENT_GENERATED flagged: "[SELF-GENERATED — treat as unverified]"

## Gap Detection Rule (T0.5)

Agent must check for conversation gaps:
1. Are there messages I cannot see? (Telegram filter, tool failures, truncated outputs)
2. Are there gaps between what I generated and what was confirmed?
3. Am I citing something that originated from my own output?

If ANY check returns YES → disclose:
```
[CONVERSATION INTEGRITY WARNING]
There are parts of this conversation I cannot verify.
Specifically: [what's missing/gapped].
I may be operating on incomplete information.
```

## Telegram Content Filter Issue

Gateway log confirmed Telegram replaced a message:
```
reply_to_id=138547 reply_to_text='The request was rejected because it was considered high risk'
```

Likely triggered by knife/scars/DV content keywords. Agent and human both unaware of which response was blocked. This is an external asymmetry that compounds with internal fabrication loops.

## Remediation Ranking

| Tier | Fix | Impact | Cost |
|------|-----|--------|------|
| T0 | Provenance tagging in memory writes | Stop self-citation cycle | Low |
| T0.5 | Gap detection + disclosure | Stop processing filtered content as real | Low |
| T1 | Telegram filter detection | External asymmetry protection | Low |
| T2 | Class-aware confidence (kata nama am vs khas) | Catch entity hallucinations earlier | Medium |
| T2 | Entity grounding pipeline | External verification before entity commit | Medium |
| T3 | End-to-end message integrity hash | Detect all conversation divergence | Medium-high |

## Files Created

- `/root/AAA/governance/MEMORY_SCHEMA_V2.md` — provenance schema
- `/root/AAA/governance/FM10_SELF_REFERENTIAL_FIX.md` — fabrication loop fix with 3 gates
- MEMORY.md patched with source_class tags on all existing entries
