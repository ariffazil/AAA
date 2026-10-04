---
name: visual-nutrition-estimation
id: visual-nutrition-estimation
risk_tier: low
description: "Estimate kcal from food photos via scale cues. Receipt."
version: 1.0.1
tags:
- nutrition
- multimodal
- estimation
- images
- F2
- F4
- F7
owner: AAA
autonomy_tier: T1
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [telegram, image, calorie, estimation]
    related_skills: []
---
# Visual Nutrition Estimation

## Purpose
Provide a fast, defensible calorie estimate from food photos by combining visual scale cues with known kcal-per-100g bands. Optimized for Telegram chats where the user asks "berapa kalori / how many calories".

## When to Use
- Dessert-in-cup, plated meals, or beverages with a common object for scale (spoon, fork, standard cups).
- User expects a range and the method, not false precision.

## Floors & Discipline
- F2 TRUTH: Separate [OBS] (visual cues), [DER] (math), [SPEC] (assumptions).
- F4 CLARITY: Emit [🦾ACT] receipt with Action/Proof/ΔS.
- F7 HUMILITY: Ranges, not single-point claims, unless weighed.
- Image policy: never identify people; describe food neutrally.

## Protocol (Dessert Cups)
1) Scale: use teaspoon (bowl ~4–5 cm Ø; handle ~13–14 cm) or known cup sizes.
2) Dimensions: small low glass cup ≈ Ø 7–8 cm, height 6–7 cm.
3) Mass: cream desserts ≈ 0.95–1.05 g/ml → 150–230 g for 160–220 ml.
4) kcal bands (per 100 g):
   - Tiramisu: 240–330
   - Chocolate mousse: 300–360
5) Compute: kcal_low = mass_g × band_low/100; kcal_high = mass_g × band_high/100.
6) Report: midpoint for 180 g + low/high; ask ONE narrowing question (coffee/mascarpone vs pure chocolate; cup volume if known).

See: references/food-photo-calorie-estimation.md

## Output Template
```
[🦾ACT] TUGASAN SELESAI
- Action: Anggar kalori dari foto + kiraan berparameter.
- Proof: Kalkulasi (execute_code) → hasil julat.
- Delta S: <0
- W_scar: none
```

## Pitfalls
- Overconfidence from visuals alone; avoid single number.
- Hidden biscuit/cake base increases kcal (+20–60 kcal typical).
- Whipped cream above rim adds 10–15% volume.

## Verification
- When user supplies cup volume or label, recompute with tighter mass.
- If restaurant nutrition info available, prefer that over estimate.
