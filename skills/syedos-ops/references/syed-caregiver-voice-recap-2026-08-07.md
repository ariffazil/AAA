# Syed Caregiver Reality Recap — Voice Note (2026-08-07)

> Proven delivery pattern for Syed's medical situation context. Captures: who the patient is, what happened, current state, watch signs, follow-up question.

## When to use

When Arif (or anyone in the SADO orbit) asks for a "full reality" or "recap" of Mak Khairuddin / Rosnani's situation, OR when Syed himself requests a voice briefing about his mom's medical journey. Syed **prefers voice** over text (proven: "Dia malas nak Baca. Malas nak type.").

## Voice note script (proven 2026-08-07)

**Voice:** `edge-tts --voice ms-MY-OsmanNeural --rate "+5%"`
**Format:** OGG (libopus, 32k bitrate, mono, 48kHz) for Telegram voice bubble
**Duration:** **5:47 actual** for the 1,050-word full reality script. This OVERRUNS the 90s SyedOS spec — only do full-length when Arif/Syed explicitly requests comprehensive recap.

```text
Assalamualaikum abang sado. Aku tau kau orang yang sibuk — nasi lemak, gym, trading, jaga mak. Tapi kali ni aku nak kau dengar sampai habis, sebab ni pasal mak kau. Aku nak bagi kau gambaran penuh, supaya bila kau pi check balik doktor nanti, kau tak keliru, dan kau tau apa nak tanya.

[... full transcript at /tmp/sado-mak-full-analysis.txt ...]
```

### Why this script structure works

The 5-block structure maps to Syed's information needs in check-back visits:

1. **Apa yang jadi (chronology)** — gives him the timeline so he can answer doctor's questions accurately
2. **Bukan salah sesiapa (framing)** — pre-empts his "salah siapa?" anger, gives him the statistical context (ERCP perforation 0.5-1.5%) so he doesn't waste energy on misplaced blame
3. **Sekarang (current state)** — bibik, dressing, surgeon-himself-dressing = good sign, validates his decisions
4. **Watch signs (actionable)** — 3 red flags (luka berair, berbau, merah meluas) gives him concrete monitoring instead of anxiety
5. **Jaga diri sendiri (caregiver support)** — acknowledges the burden is on him alone, validates, reminds him to not collapse

### Key sentences Syed needs to hear (high-impact phrases)

| Phrase | Why it lands |
|---|---|
| "Mak hang survive. Tu kira menang besar." | Reframes open laparotomy as victory, not setback |
| "Doktor baik. Surgeon sendiri dress luka mak hang. Itu rare. Simpan relationship tu." | Validates that the surgeon is an asset, not a threat |
| "Satu soalan je: bila schedule operation kedua untuk CBD tu." | Gives him ONE question to remember, not a checklist |
| "Kalau hang tumbang, mak hang siapa nak jaga?" | Cuts through caregiver martyrdom without lecturing |
| "Kau dah buat semua benda yang betul." | Closes with affirmation, not instructions |

## Pattern variations for shorter versions

When the full 5:47 is too long, scale to:
- **90-second version** (SyedOS spec): keep only blocks 1 + 2 + 4
- **30-second version** (status check): just "mak ok, dressing 2-minggu, no fever, line dah potong"
- **Question prep version** (before clinic visit): blocks 1 + 3 + 5, drop 2 (already accepted)

## Pitfalls

- ❌ **Don't generate voice >90s without sign-off** — default SyedOS spec is hard ceiling. Use the full 5:47 only when explicitly requested for caregiver reality recap.
- ❌ **Don't say "salah hospital"** — ERCP perforation is statistical, not negligence. Reframe as "nasib tak elok, bukan kecuaian."
- ❌ **Don't lecture about caregiving burden** — Syed already knows. Acknowledge + give one actionable, don't pile on.
- ❌ **Don't list all watch signs as a checklist** — Syed will tune out. Three signs max, in his language: "luka berair ke, berbau ke, merah meluas ke?"
- ❌ **Don't say "saya doakan" formally** — Syed is BM casual. "Mak hang akan ok" lands better than "Semoga cepat sembuh."

## Verification

After voice note generation, check:
1. Duration via `ffprobe` — should match requested length
2. Bitrate via `ffprobe` — 32k for ogg is fine for voice
3. File size — 5:47 at 32k ≈ 1.3 MB ogg (matches actual: 1.3M)
4. Token check BEFORE attempting programmatic send — see `voice-note-delivery-syed-2026-08-07.md`

## Related files

- `/tmp/sado-mak-full-analysis.txt` — full transcript (1,050 words)
- `/tmp/sado-mak-full-analysis.mp3` — TTS output (mp3)
- `/tmp/sado-mak-full-analysis.ogg` — Telegram-ready (1.3MB ogg)
- `references/voice-note-delivery-syed-2026-08-07.md` — delivery pitfalls, token masking
- `references/syed-person-identity.md` — full family tree, identity corrections