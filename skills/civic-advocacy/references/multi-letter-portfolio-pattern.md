# Multi-Letter Sovereign Petition Portfolio Pattern

> **Forged:** 2026-08-12 · **Provenance:** PETRONAS v13.0 portfolio (3-letter, 3 audiences)
> **Doctrine:** "Kurangkan 'siapa jahat.' Tingkatkan 'struktur apa yang perlu diaudit.'" — F13 SOVEREIGN, 2026-08-12

## When to fork into multi-letter portfolio

Default: ONE master surat with CC list covers most civic petitions.

**Fork into multi-letter portfolio when ALL of these hold:**
- Audience spans 3+ institutional surfaces with different decision-rights (e.g., Parliament, state entity, regulatory body, public)
- Each surface requires different voice calibration to be received (PAC investigates structure, NAIO responds to AI narrative, media amplifies human story)
- A single letter cannot satisfy F2 TRUTH (one audience requires INT/SPEC that another audience rejects)
- Sovereign risk profile demands redundancy — if one channel closes, others carry

**Do NOT fork when:**
- Audience is single institutional surface (one letter, comprehensive)
- Letters would duplicate 90% of content with cosmetic variations (waste)
- Time pressure favors single coordinated release
- F13 has explicitly asked for ONE letter

## The 3-letter architecture (proven pattern)

### Letter A — Institutional / Audit Audience
**Audience:** Parliamentary committee, regulatory body, audit institution (e.g., PAC, SEC, AG)
**Voice:** Tenang, named, audit-focused
**Tone template:** "Saya tidak menulis untuk meminta [penjara / buang kerja / kesimpulan awal]. Saya menulis untuk meminta [audit yang bebas, terhad, boleh diukur, boleh disahkan]."
**Structure:** Pengenalan → MENGAPA SAYA MENULIS → 4 PERMOHONAN as audit-scope blocks → PENUTUP
**Forbidden:** Fury, slogans ("Kenapa x buang dia?"), emotional anchor, mak voice, conspiracy timeline framings
**Highest defense:** Three "I don't ask" disclaimers — even if some claims are challenged, the audit ask survives

### Letter B — Sovereignty Audience
**Audience:** State entities, regional representatives, indigenous/state bodies (e.g., PETROS, GPS Sarawak, Dewan Undangan Negeri)
**Voice:** Sovereignty-focused, constitutional witness
**Tone template:** "Saya menulis sebagai saksi perlembagaan, bukan sebagai pihak kepada pertikaian [X vs Y]. Struktur ini memberi kesan langsung kepada kedaulatan [Sarawak / Sabah / dll.]."
**Structure:** Latar Belakang (treaty/agreement timeline) → TOPIC UTAMA (e.g., SEARAH as main topic, NOT appendix) → Isu Kedaulatan (specific questions) → Skop Audit/Tindakan (5 specific actions)
**Required:** Specific asset listing (e.g., 5 PSC Malaysia), treaty references (MA63, PDA 1974), jurisdiction analysis (UK Companies Act vs Federal Constitution)
**Forbidden:** Personal blame on CEO (focus on structure), rant tone, mak voice

### Letter C — Human Story / Media / Public Audience
**Audience:** National AI Office, media outlets, general public, civil society platforms
**Voice:** Human story, REAL WhatsApp family voice, vulnerability
**Anchor sentence (always verbatim):** "Saya tak faham apa yang anak saya buat. Tapi saya nampak dia tak boleh tidur."
**Structure:** Anchor → REAL family voice (verbatim WhatsApp quotes) → Apa yang [ibu/masyarakat/negara] nampak → Kenapa angka tak cukup → Kepada NAIO/Media/Awam
**Required WhatsApp voice elements (verbatim, with date stamps):**
- "Mak tengah siang ikan" (real working mak)
- "Siapa pun tak ucap mak pun tak tau 😭" (Mother's Day 2015)
- "Makkk selamat hari ibu. Terima kasih jaga dan sabar dgn perangai kakak" (kakak, May 2015)
- Abah: "Assalamuailom anak-anak abah serta isteri tersayang" (April 2015)
- Birthday 5 Oct (never publicly celebrated)
- "pagi" shift work
**Forbidden:** RRR, MCCG, JV London technical details (institutional → Letter A), fabricated/archetypal mak voice

## Identity discipline across all 3 letters

- **LOCKED:** Muhammad Arif bin Fazil · 12 tahun · Geosaintis Kanan, PETRONAS Carigali
- First mention in each letter: FULL NAME
- Subsequent: "saya" or "Arif"
- arifOS Federation declaration at sign-off of ALL THREE letters (institutional protection)
- F13 SOVEREIGN directive: "Name IS the shield — name carries F13 weight"

## Strategic doctrine (F13 SOVEREIGN, 2026-08-12)

> "Kurangkan 'siapa jahat.' Tingkatkan 'struktur apa yang perlu diaudit.'"

Operational translation:
- ❌ "Tengku Taufik perasan tak?" → ✅ "Tengku Taufik bawa angka ini ke Lembaga, atau Lembaga tolak angka ini?"
- ❌ "PETRONAS tipu Parlimen" → ✅ "JV ini didaftarkan di UK Companies House #17027115 tanpa rekod briefing Parlimen"
- ❌ "PMX tak peduli rakyat" → ✅ "Dividen RM32B dibayar sedangkan RRR 0.3 dan reserve life 9.9 tahun"

## Anti-patterns (forbidden in ALL letters)

1. ❌ Conspiracy timeline framings — "14 hari selepas Federal Court" (INT, REMOVE), "sengaja didaftar di London" (SPEC, REMOVE), "personally benefited" (SPEC + F6 MARUAH violation)
2. ❌ Cross-voice contamination — mak voice in Letter A (resets to Marhaen Soul, loses audit ask)
3. ❌ Cross-voice contamination — RRR/MCCG in Letter C (kills media amplification)
4. ❌ Softened "berhenti sabar" energy in Letter A (Letter A is TENANG, not furious)
5. ❌ Fiksyen mak voice (Letter C must be REAL WhatsApp transcript quotes)
6. ❌ Corporate apologies, AI-isms ("it's important to note", "I would like to", "delve into")
7. ❌ Exceed 12 pages per letter (reader fatigue)

## F2 epistemic tag discipline (Letters A & B)

When citing data, mark with visible tag:
- **[OBS]** — directly observed in public source (Companies House, Eni press release, Parlimen record)
- **[DER]** — computed from observed data
- **[INT]** — interpreted (DO NOT USE in PAC petition)
- **[SPEC]** — speculative (DO NOT USE in PAC petition)

Visual: `<span class="epistemic">[OBS]</span>` with mono font, light background

## Tech stack for the 3-letter forge

```
Spec: v13_PORTFOLIO_SPEC.md (canonical, version-locked)
HTML: inline CSS, print-ready
Render: weasyprint Python 3.13 (NOT pandoc, NOT chrome headless — weasyprint is fastest)
SHA: compute BEFORE patching hash into HTML (Kleene's fixed-point)
APEX: apex-judge isolate — expects HOLD+F13_REQUIRED for T3 irreversible dispatch
VAULT: append portfolio_seal to outcomes.jsonl
```

## Reference: PETRONAS v13.0 portfolio files

| File | Path | Source |
|------|------|--------|
| Letter A canonical | `/root/forge_work/petronas2025/letter-A-canonical.html` | Pak Arif verbatim (APEX Letter dictation) |
| Letter B PETROS | `/root/forge_work/petronas2025/letter-B-PETROS.html` | Hermes v13 per spec |
| Letter C NAIO | `/root/forge_work/petronas2025/letter-C-NAIO.html` | Hermes v13 per spec (REAL mak voice) |
| Spec | `/root/forge_work/petronas2025/v13_PORTFOLIO_SPEC.md` | 23KB, version-locked |
| VAULT999 seal | `coherence_id: PETRONAS_PORTFOLIO_V13_2026-08-12, session_id: SEAL-e7ac86796b174f73` | Appended |

## Failure pivot (when agents fail)

Don't wait for stuck LLM agents. The 5-step manual forge:

1. Write HTML directly (inline CSS, print-ready)
2. `weasyprint.HTML(string=Path('...').read_text(), base_url=...).write_pdf('...pdf')`
3. `sha256sum file.html` → patch into HTML as `doc-hash` placeholder
4. `python3 /root/scripts/apex_judge.py isolate --doer "..." --candidate "..." --evidence-file /tmp/ev.json --pretty --human` (expects HOLD+F13_REQUIRED)
5. Append to `/root/arifOS/VAULT999/outcomes.jsonl`

Total time: ~3 minutes per letter. Don't be precious about multi-agent choreography failure.