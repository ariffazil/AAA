# AUDIO-INTELLIGENCE-CANON::v1 — Satu Kanun Audio Semua Lane

> **Tujuan:** Tamat kekacauan audio malam 2026-10-05 (katalog vs private library, double-push, "flaky", fail hilang antara vantage). Satu kanun, semua lane — KVM4 (irfanclaw) dan KVM8 (Hermes) benda yang sama.
> **Kuasa:** F13 (ARIF). **Forged:** 2026-10-05 20:49 UTC, irfanclaw FI-017.
> **Hierarki:** `voice/REGISTRY.md` (undang-undang) → playbook (play-by-play) → **kanun ni (blok kompak yang diedar ke semua lane)**. Isinya mesti kekal identik merentas lane.
> Status: F13_RATIFIED_DIRECTIVE 2026-10-05 — instrument: arahan F13 ARIF ("reduce the chaos for audio intelligence") · active all-lane canon · forged irfanclaw FI-017

```
ARAHERMES::AUDIO-INTELLIGENCE-CANON::v1
TARIKH: 2026-10-05 · KUASA: F13 (ARIF) · FORGE: irfanclaw FI-017 (KVM4)

═══ 1. ENJIN ═══
POST https://api.minimax.io/v1/t2a_v2 · model speech-2.8-hd
Header: "Authorization: Bearer <MINIMAX_API_KEY>"
data.audio = HEX (bytes.fromhex, BUKAN base64)
Gate: base_resp.status_code==0 + bytes>0, kalau tak = FAIL dilapor, bukan disenyap
MP3 32000Hz → ffmpeg libopus 48k 16k mono .ogg → ffprobe durasi → md5 resit

═══ 2. PETA SUARA (config-declared = AUTHORITATIVE) ═══
abang-sado-live-v1 — Syed (speed 0.90–0.93; 0.95 bila tender)
SSSiti20260926v1 — Siti (1.0; graceful, jangan muat kasar)
PMX20260930v1 — PMX (0.95; DISTRIBUTION_HOLD — lane peribadi Arif SAHAJA)
young_knight — Syakir arketip (1.05–1.08) · female-shaonv — GF arketip (1.05–1.08)
R1: semua id di atas duduk PRIVATE library akaun — katalog awam TAK senarai.
    Jangan hakim dari catalog list. Buktikan dengan push test (status 0 + bait>0).

═══ 3. DISIPLIN MULUT ═══
R2 stop-turn: tahan audio HANYA bila id tiada dalam config / capability tak tentu.
   Config ada + probe lulus → push. Over-defensive = defect, bukan keselamatan.
R3 capability truth = keputusan ujian terkini, bukan tanggapan senarai/gagal lampau.
R4 1 turn = 0 ATAU 1 audio. Penjelasan dah push → jangan push summary.
   Audio = nilai tambah, bukan compress teks. Telegram tak boleh recall.
R5 artifak: tulis disk lokal + md5 SEBELUM lapor. Tanpa disk: lapor
   Produced-tanpa-path. JANGAN dakwa "fail hilang" — vantage bukan kewujudan.

═══ 4. MULTI-VOICE ═══
Render per turn → gap 450–600ms (anullsrc) → concat.
Struktur proven: usik → disiplin → kejujuran → janji → "sayang hang bro".

═══ 5. FAILURE TABLE ═══
1004 = Bearer hilang · 2054 = id salah/tiada (push test dulu, jangan andaikan)
404 = lupa /v1 · 429 = hormat Retry-After · HEX kosong = decode salah
"files hilang" = vantage lane lain — tulis md5 dulu, jangan menuduh.

═══ 6. SEMPADAN ═══
Non-explicit · arketip tanpa nama · PMX hold · DM default kecuali F13 approve
group · clone = media register, bukan ganti manusia · resit PRODUCED ≠ DELIVERED
≠ OBSERVED dilapor berasingan, UNKNOWN ditaip, ayat sedap dilarang.
```

## Resit edaran
- KVM4: fail ni. KVM8: relai AAA group → @ASI_arifos_bot, arahan ingest + resit balik.
- Kunci MiniMax atas KVM8 = **UNKNOWN dari KVM4** — resit Hermes yang akan sahkan.
