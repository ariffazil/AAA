---
name: 666-rasa
description: "Rasa — somatic/human-state check untuk Arif: energy, tidur, makan, mood. ZEN spine /666. cognitive-commands doctrine di /root/AAA/skills/cognitive-commands/SKILL.md."
triggers:
  - "/666_rasa"
---

# /666_rasa

Bila mesej ini tiba (sebagai slash atau teks):

1. Refleksi keadaan manusia dengan data (WELL/biometric/last DM tone), bukan nasihat preachy. Satu baris jujur, satu cadangan lembut maksimum. Dignity first.
2. Kekal dalam register BM santai + floor F1-F13; rujuk cognitive-commands untuk nada penuh.

## Instrumentation (Wave A · 2026-09-30)
- **pre_observable**: WELL state.json freshness + last-DM tone sample
- **post_observable**: one honest line + max one suggestion (dignity-first)
- **receipt**: `flow_ingest(step_type=Cool, payload={"zen":"666","state_age_min":<n>})`
- **fail_state**: WELL stale/degraded → label data-stale, jangan pseud precision
