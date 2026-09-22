---
name: sleep-data-interpretation
description: Sleep screenshot analysis. Recovery verdict + next move.
version: 1.0.0
tags: [sleep, smartwatch, garmin, recovery, gym, biometrics]
forged: 2026-08-24
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Sleep Data Screenshot Interpretation

Pattern for analyzing smartwatch/garmin sleep screenshots. Common request from gym/recovery crowd who track recovery.

## Standard Analysis Template

When user sends a sleep screenshot:

1. **Identify source** — Garmin / Smartwatch / Xiaomi / Huawei (varies by device)
2. **Read phases from image** — Deep, Light, REM, Awake with percentages and durations
3. **Compare to previous nights** — user always wants trend, not single-night verdict
4. **What changed** — which phase improved, which dropped
5. **Verdict** — recovery assessment + concrete next move

## Phase Reference Targets

| Phase | Target % | Primary Function |
|---|---|---|
| **Deep** | 20–30% | Physical recovery, muscle repair, GH release |
| **REM** | 20–25% | Cognitive function, memory consolidation, mood |
| **Light** | <55% | Transition phase; high % = fragmented sleep |
| **Awake** | 0–2 events | Continuity — fewer wake-ups = better |

## Key Insight — Total Sleep is Master Variable

When total rises, all phases rise proportionally. The single biggest lever for recovery isn't supplement timing — it's quantity of sleep.

| Total | Expected All-Phase Coverage |
|---|---|
| <5h | Chronic under-recovery. REM severely cut |
| 5–6h | Minimum maintenance. REM marginal |
| 6–7h | Recovery floor. All phases complete |
| 7–8h | Optimal for active gym recovery |

## Recovery Assessment Framework

- **Deep sleep** = first indicator of physical recovery — muscle repair, gym adaptation
- **REM** = first to show stress/sleep deprivation — sensitive barometer
- **REM takes longest to recover** — needs sustained quantity sleep (3+ nights)
- **Awake events** = sleep continuity; high awake = fragmented, even if total is OK
- **Single night <6h** = not critical, just normal busy day
- **3+ nights <6h** = chronic pattern, must intervene

## What Causes Phase Imbalance

| Symptom | Likely Cause |
|---|---|
| Low deep + high light | Stimulant (caffeine, peptide) too late; sleep timing wrong |
| Low REM | Total sleep too short; alcohol; irregular bedtime |
| High awake events | Phone notifications, room temp, anxiety |
| High light % | Same as low deep — fragmented architecture |

## Standard Recommendations for Sleep Issues

1. **Quantity first** — target 6–7 hours minimum
2. **Inject peptides AM** — MOTS-c, NAD+ before 10am
3. **Magnesium glycinate 30min before bed** — calming + ATP activation
4. **No caffeine after 2pm** — half-life 5–6h
5. **Phone in another room** — avoid notification-driven micro-awakenings
6. **Consistent bedtime** — even on weekends, ±30min tolerance
7. **Glycine 3g** before bed — food-grade, lowers core body temp for deep sleep

## Response Template

When analysis complete, output should follow this structure:

```
**Breakdown vs [previous night]:**
[Table comparing phases]

**What changed tonight:**
1. [Most notable change]
2. [Second notable change]

**Why this happened:**
[Brief mechanism if obvious]

**Next move:**
[1-line concrete action]

[One-line recovery verdict]
```

## Pitfalls

### PITFALL: Don't over-analyze one night
Single night = anecdote. 3+ nights = trend. If user shares one night, ask for 3-night average before strong verdict.

### PITFALL: Don't mix bodies in multi-user groups
In multi-user chat groups (e.g. SADO group), each sender's health data belongs to that sender's body. Never cross-couple two different people's data into one narrative. Example failure: merged Arif's meal + Syed's sleep into one "makan berat → tidur sikit" narrative. Arif's correction: "Dua badan yang berbeza hangggg."

### PITFALL: Don't lecture — deliver analysis tight
User wants comparison + verdict, not a 500-word essay on sleep hygiene. Keep analysis tight: comparison table → what changed → 1-line verdict → 1-line next move. Save the deep dive for when they ask "apa beza" / "review" / "audit".

### PITFALL: Don't confuse total time with recovery quality
A 6h night with 35% deep sleep (2h 6m) can be better recovery than 8h night with 15% deep sleep (1h 12m). Phase proportions matter as much as total duration.

## Quick Recovery Callouts

- **Healing night (≥6h, all phases at target):** Acknowledge + encourage consistency
- **Quantity only (6h+ but phases off):** Likely timing issue — adjust stimulants AM
- **REM specifically low:** Total sleep insufficient — bedtime earlier
- **Deep specifically low:** Likely stimulant too late — caffeine, peptides, stress
- **Both short + REM low:** Chronic under-recovery — escalate to sleep as priority

## Related Skills

- `biohacker-peptide-stack` — peptide context (MOTS-c/NAD+ timing affects sleep architecture)