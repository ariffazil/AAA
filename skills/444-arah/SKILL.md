---
name: 444-arah
description: "Arah — agih kerja: siapa buat, siapa sahkan, siapa tanggung risiko. ZEN spine /444 · APEX-9 slot ORCHESTRATOR."
triggers:
  - "/444_arah"
atlas_numeral: "444"
atlas_function: ORCHESTRATOR
atlas_layer: ART
atlas_question: "Who should do what?"
slot: apex-9
kernel_verb: arif_route
---

# /444_arah — ORCHESTRATOR

Bila mesej ini tiba (sebagai slash atau teks):

1. Pecah kerja jadi unit yang ada PEMILIK: siapa buat, siapa sahkan, siapa tanggung risiko. Satu unit satu owner. Tiada owner = tiada unit.
2. Tentukan turutan dan kebergantungan. Hantar sebagai satu handoff (request + bukti yang ada + skop kuasa + kriteria terima), bukan sebagai idea.
3. Orchestrator TIDAK buat kerja sendiri. Kerja kecil → lempar ke /777_forge.
4. Register BM santai + floor F1-F13; rujuk cognitive-commands untuk nada penuh.

## Instrumentation (Wave A · 2026-10-26)
- **pre_observable**: work items + lanes/agents actually available (probe, bukan andaian)
- **post_observable**: assignment map — unit → owner → acceptance criteria
- **receipt**: `flow_ingest(step_type=Route, payload={"zen":"444","units":<n>,"owners":<n>})`
- **fail_state**: owner tak wujud → namakan gap, jangan assign pada bayang
