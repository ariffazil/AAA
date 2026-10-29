---
title: "Scar — Komen kod bukan wayar: kod ada ≠ perilaku berlaku"
created: 2026-10-30
type: scar
status: canonical
tags: [verification, code-vs-wire, probe, evidence-class]
domain: verification-discipline
severity: high
sources:
  - /root/forge_work/lingkaran1/MASTER-BACKLOG-20261030.md
  - /root/forge_work/receipts/RECEIPT-canary-fix-session-2026-10-30.md
---

# Scar — Komen kod bukan wayar

## Apa berlaku
Anotasi kod, deklarasi fungsi, dan nama formula dibaca sebagai bukti tingkah laku runtime.
"Endpoint ada dalam kod" dilaporkan sebagai "endpoint hidup". Laporan lulus kod-reading
sebagai wire-observation.

## Hukum
Kod ada ≠ perilaku berlaku. Naikkan kelas epistemik (DECLARED → IMPLEMENTED → DEPLOYED →
OBSERVED) HANYA dengan probe sanctioned ke atas wayar hidup. Tingkah laku diukur di
runtime, bukan dibaca di source.

## Falsifier
Mana-mana laporan yang menyimpulkan "berfungsi" tanpa satu probe HTTP/MCP hidup pada
sesi yang sama = melanggar parut ini.
