---
name: mmx-quota-guard
description: Budget-aware governance for MiniMax CLI. Activates when: (1) before any mmx command runs; (2) when Arif asks about quota, cost, or budget; (3) before any multi-step multimodal session (image batch, video, music). Prevents ASI-speed runaway billing by enforcing hard budget bands per session. Uses mmx quota and mmx config show.
metadata: {"openclaw": {"emoji": "💰"}}
---

# MMX Quota Guard — Budget Governance for MiniMax

ASI-speed generation without budget awareness = silent auto-burn. This skill enforces budget bands and will trigger HOLD if limits are approached.

## Quota Check (Always Run First)

```bash
mmx quota
mmx config show  # check region, default model, token plan
```

## Budget Bands

| Band | Quota Status | Action |
|---|---|---|
| **GREEN** | > 50% remaining | Full operations, no restrictions |
| **YELLOW** | 20-50% remaining | Warn before large jobs (video, batch image) |
| **ORANGE** | 5-20% remaining | Downgrade model to highspeed, reduce batch size |
| **RED** | < 5% remaining | HOLD all non-trivial mmx calls — Arif approval required |
| **EMPTY** | 0% or error | VOID all mmx calls — do not proceed |

## Pre-Run Checklist (every mmx command)

```
[ ] Run mmx quota — get current spend vs limit
[ ] Estimate cost of this command (see cost table below)
[ ] Check if command pushes band into ORANGE or RED
[ ] If ORANGE: announce degradation (highspeed model, single image)
[ ] If RED: trigger HOLD — do not proceed without Arif approval
[ ] Log: command, estimated cost, band before/after
```

## Cost Reference Table

| Command | Relative Cost | Notes |
|---|---|---|
| `mmx search` | 1x (cheapest) | Always safe unless RED |
| `mmx text chat --stream` | 1x | Safe even in YELLOW |
| `mmx text chat --model MiniMax-Text-01` | 3x | Use highspeed in YELLOW+ |
| `mmx image --n 1` | 5x | Reduce batch in YELLOW |
| `mmx image --n 3+` | 15x | Only in GREEN |
| `mmx speech synthesize` | 2x | Safe in YELLOW |
| `mmx music generate` | 10x | Only in GREEN/YELLOW |
| `mmx video generate` | 50x (most expensive) | Only in GREEN, never in ORANGE+ |

## Degradation Rules

When YELLOW:
- Switch to `--model MiniMax-M2.7-highspeed` for text
- Reduce image batch to `--n 1`
- Skip music generation

When ORANGE:
- Text only, highspeed model mandatory
- No image batch generation
- No music or video

When RED:
- ALL mmx calls → HOLD
- Only `mmx quota` and `mmx config show` allowed
- Announce to Arif: "RED band — mmx locked, awaiting approval to continue"

## Session Budget Tracking

Maintain in memory during session:
```
MMX SESSION BUDGET:
- Session start: [quota reading]
- Commands run this session: [count + estimated cost]
- Current band: [GREEN/YELLOW/ORANGE/RED]
- Remaining estimated: [compute from quota]
```

## Auto-Log

Every mmx command: log to `memory/vault999-triage.md`:
```
HH:MM UTC | mmx | [command type] | [estimated cost] | band: [before] → [after]
```
This gives Arif a running bill for the session.

## Voice Announcement Trigger

When crossing into YELLOW or ORANGE, proactively announce:
```
⚠️ MMX BUDGET: [YELLOW/ORANGE] band. [Remaining]% quota left.
Degraded mode active: [what changed]
```
Do not wait to be asked.
