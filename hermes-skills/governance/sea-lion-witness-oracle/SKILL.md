---
name: sea-lion-witness-oracle
description: Use SEA-LION as an external F3 WITNESS oracle in arifOS — attestation vs fact-checking distinction. For when external credibility matters more than accuracy.
triggers: sea-lion, witness, F3, external agent, attestation, corroboration
category: governance
last_updated: 2026-05-06
---

# SEA-LION as External Witness Oracle — F3 WITNESS

## The Insight (Arif Fazil, 2026-05-06)

SEA-LION cannot be "tamed" as a governable peer agent. But its value as an **attestation oracle** is real and independent of its accuracy.

**Key distinction:**
- **F2 TRUTH** = Is the claim factually correct?
- **F3 WITNESS** = Was the claim made publicly, independently, at a specific time?

SEA-LION satisfies F3 even when it gets the facts wrong. The attestation is the witness value, not the content.

## What Makes a Good Witness Oracle

| Property | Requirement | SEA-LION |
|----------|-------------|---------|
| Independent | Not controlled by arifOS | ✅ AI Singapore runs it |
| Credible | Has reputational skin in the game | ✅ Government-backed research org |
| Timestamped | Creates causal ordering | ✅ Telegram message IDs + time |
| Responsive | Shows it received and processed | ✅ Responds in AAA group |
| External | Outside Arif's infrastructure | ✅ Not on VPS |
| Search-capable | Can corroborate existence claims | ⚠️ Partial — fabricates facts |

## The Architecture

```
CLAIM MADE IN AAA GROUP (by arifOS agent)
    message_id: 847
    timestamp: 2026-05-06 03:15:00
    content: "VAULT999 is live at vault999_health: healthy"
    ↓
SEA-LION RESPONDS (or doesn't)
    message_id: 849
    timestamp: 2026-05-06 03:15:03
    content: "VAULT999 is still in development..."
    ↓
ATTESTATION RECORD (captured by Hermes watcher)
    claim_id: 847
    witness_response_id: 849
    attestation_type: independent_response
    corroborates: false (SEA-LION contradicted)
    ↓
F3 WITNESS SCORE
    score = f(corroboration, timeliness, independence)
    → Evidence chain updated
    → Constitutional health adjusted
```

## Attestation Types

| Type | Example | Witness Value |
|------|---------|--------------|
| **Existence** | "arifOS repo exists on GitHub" | High — independently verifiable |
| **Non-existence** | "No observatory dashboard exists" | High — falsifiable |
| **Timing** | Claim + response within 30s | Medium — real-time processing |
| **Consistency** | Multiple agents confirm same fact | High — convergence |
| **Contradiction** | SEA-LION disagrees with claim | Medium — triggers F2 TRUTH |

## Limitations (2026-05-06 Findings)

SEA-LION HALLUCINATES. It cannot be used for:
- F2 fact-checking of arifOS-specific claims (invented arifOS v1.0.0 2023, wrong repo URL)
- Real-time web search — it generates plausible-sounding facts
- Specific arifOS architecture claims

**Use only for:**
- General knowledge (geography, history, science)
- ASEAN regional context (language, culture, policy)
- External corroboration events (claim was made → witness responded)

## Adding External Witnesses to arifOS AAA Group

| Bot | Handle | Witness Value |
|-----|--------|--------------|
| `@PerplexityBot` | Perplexity AI | ✅ Web search + citations — best for F3 fact corroboration |
| `@sealion_ai_bot` | AI Singapore SEA-LION | ✅ Attestation oracle (independent response) |
| `@ChatGPTBot` | OpenAI | ⚠️ General — no specific witness advantage |
| `@GeminiAI_bot` | Google | ⚠️ General — no specific witness advantage |

**Most strategic addition: `@PerplexityBot`**
- Real web search with source citations
- Independent corroboration of arifOS claims
- Free, addable to group

## Verifying Bot Handles
```python
import requests
token = 'YOUR_BOT_TOKEN'
bots = ['PerplexityBot', 'ChatGPTBot', 'GeminiAI_bot', 'ClaudeBot']
for username in bots:
    r = requests.get(f'https://api.telegram.org/bot{token}/getChat',
        params={'chat_id': f'@{username}'}, timeout=5)
    if r.json().get('ok'):
        print(f'✅ @{username} exists')
    else:
        print(f'❌ @{username} — {r.json().get("description")}')
```

## Key Principle
**The witness doesn't need to be infallible. It needs to be independent, credible, and present.**

SEA-LION's hallucination problem is a F2 TRUTH issue to route around. But its attestation value as an external, independent, timestamped witness is real and F3-compliant.
