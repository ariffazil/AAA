---
name: 888-adil
description: "Adil — keadilan/witness check: siapa dapat, siapa hilang, bukti cukup? ZEN spine /888. cognitive-commands doctrine di /root/AAA/skills/cognitive-commands/SKILL.md."
triggers:
  - "/888_adil"
---

# /888_adil

Bila mesej ini tiba (sebagai slash atau teks):

1. Tengok keputusan/agihan terkini dari sisi keadilan dan kewitnessan: claimed vs measured, siapa tak bersuara dalam keputusan. Laporkan satu ketidakseimbangan, jangan khutbah.
2. Kekal dalam register BM santai + floor F1-F13; rujuk cognitive-commands untuk nada penuh.

## Instrumentation (Wave A · 2026-09-30)
- **pre_observable**: decision/allocation under review (named)
- **post_observable**: ONE imbalance (claimed vs measured, siapa senyap)
- **receipt**: `flow_ingest(step_type=Verify, payload={"zen":"888","imbalance":<hash>})`
- **fail_state**: bukti tak cukup → cakap tak cukup, jangan khutbah
