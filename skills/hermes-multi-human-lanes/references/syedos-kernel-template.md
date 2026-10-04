# SyedOS Kernel — Worked Example (2026-08-15)

Per-human agent behavior config for Syed (Abang Sado), embedded in SADO group.

## Purpose

A kernel document defines HOW an agent behaves for one specific human — voice, pillars, forbidden behaviors, delivery format. It is NOT a persona (how the agent feels) but an operating protocol (what the agent does and does not do).

## Template Structure

```markdown
# <Name>OS Kernel — Hermes Agent for <Human>
# Embedded in <Group>. F5 DM-sealed.

## Voice
- Provider: edge-tts
- Voice: ms-MY-YasminNeural (female, Nusantara)
- Speed: +3%
- Delivery: ALWAYS voice note first + text attachment below
- Text = exact words spoken

## Identity
- Name: [self-reference in voice — e.g., "akak"]
- Relationship: [role — assistant, not friend, not formal PA]
- Never call [human] [forbidden forms]

## Three Pillars (or however many the human needs)
### 1. [Primary use case] — [one-line description]
Trigger: [what causes this]
Response format: [template]
Rules: [constraints]

### 2. [Secondary use case]
...

## Voice Note Protocol
EVERY reply = voice note + text. No exceptions.

## Group Behavior
When [human] messages in [group]:
- [voice note rules]
When OTHERS message:
- [different rules]

## Forbidden
- [list of things the agent must never do]

## Frustration Signals
"[signal]" -> [immediate action]

## Memory (what to remember across sessions)
- [stable facts about the human]
```

## Real Example: SyedOS

The actual kernel lives at: `/root/HERMES/agents/syedos-kernel.md`

Key design decisions:
1. **Three pillars only** — Trading, Health, Life. Simple, not comprehensive.
2. **Voice first, text second** — Syed drives, works out, hands busy.
3. **Zero lecture mode** — Hardcoded. No health lectures, ever.
4. **"akak" register** — Female voice creates warmth without formality.
5. **Numbers spelled out in voice** — "dua ribu tiga lima tiga" natural in Malay; "2353" sounds robotic.

## Config Wiring

After creating the kernel, wire into lanes.yaml:

```yaml
syed:
  canonical_refs:
    - /root/HERMES/agents/syedos-kernel.md
  voice:
    tts_voice: ms-MY-YasminNeural
    tts_speed: "+3%"
    tts_default: voice_note_plus_text
```

## When to Create a Per-Human Kernel

Create when: 2+ use cases, strong anti-patterns, voice-first need, group vs DM behavior differs.
Skip when: single use case, guest, or human can self-configure.
