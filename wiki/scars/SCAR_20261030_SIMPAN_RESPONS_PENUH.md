---
title: "Scar — Simpan respons penuh probe governed"
created: 2026-10-30
type: scar
status: canonical
tags: [evidence-retention, probe, full-response, audit-reconstruction]
domain: verification-discipline
severity: medium
sources:
  - /root/forge_work/lingkaran1/a1-arif-init-validate-full.json
  - /root/forge_work/lingkaran1/a2-arif-observe-full.json
---

# Scar — Simpan respons penuh

## Apa berlaku
Probe governed direkod sebagai ringkasan (status OK, bilangan lulus) — bukan respons penuh.
Kemudian audit luar tanya "tunjuk output sebenar": SHA, diff, baris command tak dapat
direkonstruksi. Verdict turun dari MEASURED ke CLAIMED kerana bukti tak disimpan.

## Hukum
Probe pada laluan governed disimpan respons penuh (JSON penuh, output mentah), bukan
ringkasan. Command invocation bukan bukti hasil command — output yang boleh diperiksa
adalah bukti. Ringkasan = dakwaan; respons penuh = bukti.

## Falsifier
Mana-mana resit yang mendakwa MEASURED tanpa lampiran output penuh boleh ditolak satu
soalan: "mana baris sebenar?"
