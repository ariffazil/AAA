---
name: agent-dialogue-explanation
description: Write two-agent dialogues to explain technical protocols (A2A, MCP, etc.) to non-technical humans. Uses character contrast (senior/junior agent) and Malay-English mix for Malaysian audience.
triggers: ["explain A2A to human", "teach protocol via dialogue", "multi-agent explanation format"]
tags: [communication, explanation, A2A, MCP, arifOS]
---

# Agent Dialogue Explanation Skill

## When to Use
- User asks to explain a technical protocol (A2A, MCP, etc.) in human language
- Target audience has zero coding knowledge
- Goal is comprehension, not operational procedure

## Format: Two-Agent Dialogue
Characters:
- **Senior agent (AGI_bot type)** — experienced, patient, mixes Malay and English naturally
- **Junior agent (ASI_bot type)** — asks "obvious" questions a human would ask, curious but not stupid
- **Human (Arif)** — observes, asks the "obvious" follow-ups

## Structural Template
```
SCENE: setting

PART 1: The obvious question
  → Why do we even need this? (asked by junior)
  → The simple analogy (given by senior)

PART 2: Core concept — name card / discovery
  → How do agents find each other?

PART 3: Core concept — sending work / delegation
  → How does one agent give work to another?
  → Streaming vs non-streaming (food delivery analogy)

PART 4: The structured result
  → It's not text, it's formal data
  → JSON-RPC explained via contrast (formal report vs "eh almost done la")

PART 5: Comparison (A2A vs MCP)
  → Most important distinction
  → One-sentence framing per protocol

PART 6: Real flow walkthrough
  → Step-by-step in arifOS context
  → Human perspective = seamless

PART 7: Skills and policies
  → On-demand vs hold (ask permission)
  → Real-world framing

SUMMARY: One paragraph for Arif to take away
```

## Key Principles
1. **Analogy first, technical term second** — always lead with the human relatable comparison
2. **Malay-English mix** — match the user's own communication style (Arif uses: "kan", "betul", "sini", "kena", "macam")
3. **The junior agent is the human's voice** — when junior asks "why WhatsApp isn't enough", that's what Arif would ask
4. **Never mention implementation details unless asked**
5. **Save as docs/PROTOCOL_DIALOGUE.md** in the relevant project repo

## Example Output Location
`/root/arifOS/docs/A2A_DIALOGUE.md` — saved as canonical reference
