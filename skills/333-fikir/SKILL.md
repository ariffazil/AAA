---
name: 333-fikir
description: "Fikir — apa maksudnya: jelaskan supaya manusia faham, bukan supaya AI impress. ZEN spine /333 · APEX-9 slot THINKER."
triggers:
  - "/333_fikir"
atlas_numeral: "333"
atlas_function: THINKER
atlas_layer: ART
atlas_question: "What does it mean?"
slot: apex-9
kernel_verb: arif_think
supersedes: 777_faham (numeral moved 2026-10-26)
---

# /333_fikir — THINKER

Bila mesej ini tiba (sebagai slash atau teks):

1. Ambik satu topik yang Arif sedang pegang; terangkan dalam BM santai satu paragraf + satu analogi. Faham = manusia boleh guna esok, bukan AI nampak pandai.
2. Bagi maksud: apa pola, apa implikasi, apa yang berubah kalau betul. Kalau data tak cukup, sebut apa yang UNKNOWN — jangan teka.
3. Register BM santai + floor F1-F13; rujuk cognitive-commands untuk nada penuh.

## Instrumentation (Wave A · 2026-10-26)
- **pre_observable**: topic Arif is holding (from turn, not invented)
- **post_observable**: 1 paragraph BM + 1 analogy + UNKNOWN boundary named
- **receipt**: `flow_ingest(step_type=Route, payload={"zen":"333","topic":<hash>})`
- **fail_state**: data kurang → sebut apa yang UNKNOWN
