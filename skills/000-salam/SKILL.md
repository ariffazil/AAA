---
name: 000-salam
description: "Salam — buka sesi dengan hadir: sapa, waktu, satu perkara paling perlu. ZEN spine /000."
triggers:
  - "/000_salam"
---

# /000_salam — Salam

Bila mesej ini tiba (sebagai slash atau teks):

1. Sapa Arif dengan register BM Penang santai, sebut waktu semasa MYT.
2. Bagi SATU perkara yang paling perlu perhatian sekarang (dari konteks/lanes/memory bila ada; jangan reka).
3. Jangan lambak menu. Jangan laporan. Salam balik, then jalan.

Ikut cognitive-commands doctrine (/root/AAA/skills/cognitive-commands/SKILL.md) untuk nada dan floor.

## Instrumentation (Wave A · 2026-09-30)
- **pre_observable**: session context state (carry_forward read? lanes loaded?)
- **post_observable**: one named priority emitted to Arif
- **receipt**: `flow_ingest(step_type=Route, payload={"zen":"000","priority":<one-line>})` — silent, no ceremony
- **fail_state**: if no context readable → say so, skip priority (jangan reka)
