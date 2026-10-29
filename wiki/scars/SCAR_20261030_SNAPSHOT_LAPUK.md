---
title: "Scar — Snapshot lapuk: papan status 13 saat = sejarah, bukan kini"
created: 2026-10-30
type: scar
status: canonical
tags: [freshness, snapshot, attention-plane, runtime-state]
domain: observability
severity: medium
sources:
  - /root/AAA/state/federation_state.json
  - arifFlow /health per_actor held fi-008 (30 Okt)
---

# Scar — Snapshot lapuk

## Apa berlaku
Attention plane papar "1 HOLD aktif · fi-008" dari snapshot 13 saat lama. Probe langsung
ke enjin pada masa sama: hold telah lepas sendiri, 0 holds. Manusia hampir buat keputusan
atas angka mati.

## Hukum
State hidup diprobe dari sumber pada saat keputusan, bukan dibaca dari snapshot berumur.
Setiap paparan status mesti bawa `generated_at` + falsifier "re-probe sebelum bertindak".
Memory BUKAN realiti; snapshot BUKAN kini.

## Falsifier
Mana-mana eskalasi manusia yang dibina atas snapshot tanpa re-probe semasa = melanggar
parut ini. Kalau age > poll interval, label SEJARAH, bukan STATUS.
