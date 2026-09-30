---
name: 555-betul
description: "Betul — periksa dan betulkan: fakta, kod, keadaan. ZEN spine /555. cognitive-commands doctrine di /root/AAA/skills/cognitive-commands/SKILL.md."
triggers:
  - "/555_betul"
---

# /555_betul

Bila mesej ini tiba (sebagai slash atau teks):

1. Abaikan apa yang patut diverify, run check sebenar (command/test/probe), laporkan PASS/FAIL dengan bukti. Number tanpa sumber = UNKNOWN, bukan angka.
2. Kekal dalam register BM santai + floor F1-F13; rujuk cognitive-commands untuk nada penuh.

## Instrumentation (Wave A · 2026-09-30)
- **pre_observable**: claim under test (quoted)
- **post_observable**: PASS/FAIL/UNKNOWN + evidence path (command output, file, probe)
- **receipt**: `flow_ingest(step_type=Verify, payload={"zen":"555","claim":<hash>,"verdict":<P|F|U>})`
- **fail_state**: cannot witness → UNKNOWN (bukan FAIL, bukan PASS)
