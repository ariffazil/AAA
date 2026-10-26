---
name: 000-salam
description: "Salam — buka sesi dengan hadir: sapa, waktu, satu perkara paling perlu. ZEN spine /000."
triggers:
  - "/000_salam"
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
atlas_numeral: "000"
atlas_function: OBSERVER
atlas_layer: ART
atlas_question: "What is happening?"
slot: apex-9
kernel_verb: arif_observe
---

# /000_salam — Salam

> Slot: **000 OBSERVER** · APEX-9 spine (law: `cognitive-commands`).

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
