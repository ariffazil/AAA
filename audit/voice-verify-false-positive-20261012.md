# voice_render_verify — strict-mode false-positive class (evidence, 2026-10-12)

Run: SADO PERSONAL — MORNING FIRE, 2026-10-12 09:30 MYT
Artifact: /tmp/sado_morning_fire.wav (abang-sado-live-v1, 156.8s, md5 6bc603e66d2dc1b3b41daad684502f50)
Verdict: CONTAMINATED (exit 1, --strict), similarity 0.8879, expected 356 / heard 331 tokens.

## Classification: FALSE POSITIVE (numeral normalization + Malay ASR homophones)

All 22 `suspicious_extra_tokens` are digit-normalization or ASR spelling artifacts.
Zero foreign clauses; ASR transcript is content-faithful to the rendered script.

| suspicious token | source in script | class |
|---|---|---|
| 12, hari, bulan | "dua belas haribulan" | numeral→digit + word split |
| 201ml | "dua ratus satu emel" | numeral + homophone (emel→ml) |
| 13, 2, 2027, 3, 16, 5, 80, 42 | "tiga belas" / "dua ribu dua puluh tujuh" / ... | numeral→digit |
| rm32b, rm30b, rm380, rm71, 60, rm100 | "tiga puluh dua bilion ringgit" / "Brent tujuh puluh satu dolar enam puluh" / "atas seratus" | numeral→digit + RM normalization |
| brand | "Brent" | homophone |
| ada | "takde" | word split |
| okey | "Ok" | spelling |

## Baseline (same class, earlier accepted render)

/tmp/sado_night_truth.wav (2026-10-11) — same class: '9'(sembilan), 'tak'+'yah'(takyah),
'2'(dua), 'grup'(group), 'ejen'(agent), 'shelter'(shell), 'haribulan', 'kerilis'(release).
i.e. this class fires on any BM script containing numbers or English loanwords.

## Why it matters

- exit 1 is currently unconditional on this class → an otherwise clean render can never ship
  when the script contains numerals. This is a verifier calibration gap, not a voice defect.
- The strict gate MUST stay strict: on 2026-10-10 the same engine appended a real courtesy
  clause ("Terima kasih kerana menonton") in 1 of 6 renders — injection is a real failure mode.

## Proposed fix (verifier-side, one edit)

In `diff()`: canonically normalize both sides before tokenizing —
digit↔word for BM numerals (0-999 + ratus/ribu/bilion) and RM-prefix folding,
plus an explicit homophone tolerance list for the BM ASR set observed above.
Do NOT relax the threshold; normalize the comparator.

Owner: FI-008 (verifier is delivery-path infrastructure; not patched by the cron run).
