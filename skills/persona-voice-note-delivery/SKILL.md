---
name: persona-voice-note-delivery
description: "Use when delivering a persona voice note to one chat."
version: 1.0.0
author: hermes
tags: [voice, delivery, telegram, lane]
metadata:
  hermes:
    tags: [voice, delivery, telegram, lane]
    related_skills: [voice-lane, voice-render-verification, abang-sado-tenderness-arc]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Persona Voice Note — Delivery to the Right Chat

Rendering dan verifikasi ada skill sendiri (`voice-lane`, `voice-render-verification`, `abang-sado-tenderness-arc`). Skill ini pasal SATU perkara: fail yang dah lulus gate dihantar ke chat MANUSIA yang betul.

## When to Use

- Voice note diminta dalam DM/room seorang manusia, bukan dalam chat sovereign.
- Mana-mana render guna script lane persona (`/root/scripts/sado`, lane `siti`, `pmx`, dan setara) yang ada `deliver_to` tersimpan dalam config.

## Rule: script tidak menghantar untuk hang

Script lane persona simpan `deliver_to` milik lane TERSEBUT. `/root/scripts/sado doctor` tunjuk `deliver_to: 267378578` — itu chat Arif. Kalau voice note disuruh masuk DM Syed, render tanpa delivery dan hantar sendiri dari chat ini:

```bash
/root/scripts/sado say <textfile> --no-deliver
```

Lepas `verdict: PASS`, ambil path `take.mp3` dari JSON output dan hantar sebagai mesej dalam chat semasa:

```
MEDIA:/absolute/path/take.mp3
[[audio_as_voice]]
```

`[[audio_as_voice]]` pada baris sendiri — tanpanya fail sampai sebagai dokumen, bukan voice bubble.

## Gate discipline

- Gate PASS bukan formaliti: ia ASR round-trip terhadap teks yang hang tulis. `REVIEW` atau `FAIL` = jangan hantar fail tu, betulkan teks dan render semula.
- Onomatopoeia dan ketawa ("hahaha") hilang dalam transkripsi → gate tandakan MISSING → REVIEW. Jangan letak dalam skrip.
- Nombor dan simbol: sebut penuh dalam teks ("seratus lima puluh ringgit"), bukan "RM150" — transkripsi kerap buang digit dan simbol.

## Pitfalls

- Jangan guna `--to` untuk menuju chat manusia lain tanpa sahkan chat_id itu milik dia — silap id = voice note masuk chat orang lain.
- Jangan hantar terus dari output script tanpa baca `verdict`; script yang gagal gate masih simpan fail di disk.
- Jangan ulang voice note yang sama tanpa diminta. Satu render, satu hantar.
