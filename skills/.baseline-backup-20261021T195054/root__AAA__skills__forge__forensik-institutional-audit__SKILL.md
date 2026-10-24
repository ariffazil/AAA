---
name: forensik-institutional-audit
description: Forge BM kampung institutional-audit PDF. HOLD verdict.
tags: [pdf, audit, institutional, bmhakikat, federasi]
metadata:
  hermes:
    tags: [pdf, audit, institutional, bmhakikat, federasi]
---

# Forensik Institutional Audit — BM Penang Kampung Edition

Guna skill ni bila user bagi nama manusia + institusi mereka dan minta "realiti hidup", "witness artifact", atau "institutional audit" — bukan biography bunga, bukan prosecution, bukan fanboy. Kelas task ini berulang: Demis Hassabis, Elon Musk, Sam Altman, Amodei siblings. Format: PDF Typst 14-25 muka dengan constitutional doctrine binding, watched execution, provisional verdict HOLD pending F13 review.

## Procedure

1. **Pilih pola framing INSTITUSI, bukan manusia tunggal.** Subjek ialah *institution* dengan manusia sebagai node. Bio hilang keutamaannya — audit ialah siapa pegang autoriti, siapa tanggung akibat, apa yang dipunyai oleh struktur, apa yang hanya di design saja.
2. **Cross-audit prior artifact.** Jika artifact sebelumnya menyebut subjek semasa (sam_altman.pdf menyebut OpenAI capability dispersion), setiap dakwaan demi dakwaan dikelaskan FACT/QUOTE/INTERPRETATION/CONTESTED/UNKNOWN dan ditentusukan lagi. Jangan inherit conclusion dari prior artifact — verify atau annotate.
3. **Pre-forge hypothesis sebelum research.** Untuk persona duo-founding (Amodei bersaudara, Hassabis+Suleyman+Legg), hypothesis awal = "duo equals founder." Cross-audit cepat dari web mengesahkan atau refutes — kalau refuted, identity naratif menjadi complementarity map, bukan dichotomy "mind/hands."
4. **Bina artifact dengan 21-25 seksyen typst dwi-komponen:**
   - **Front matter**: Cover, Executive Judgment (PROVEN/CONTESTED/UNKNOWN × 3), Epistemic Limits, Founder taxonomy.
   - **Subjek-as-vektor**: latar belakang, sumbangan disahkan, autoriti hari ini, founder decomposition (lain-lain), lineage ke OpenAI kalau relevan.
   - **Struktur analisis**: Scar Ledger, Shadow Register, Paradox Tests (6-8), Consequence Ledger, Authority Graph, Capital+Compute dependencies.
   - **Cross-audit prior PDF**, kontradiksi dikekalkan, falsification queue, Constitutional Findings (10 CF).
   - **Back matter**: Open Questions, Source manifest, ONE reusable lesson.
5. **Voice Penang kampung BM**: pendek, terus, dipendekkan, tak ada jargón falsafah, tak ada lecture. Petikan verbatim dari dokumen primer dibiarkan dalam bahasa Inggeris asal. Penutup = soalan terbuka, bukan verdict menang/kalah.
6. **Constitutional doctrine binding — SELALU**: `Reality > Narrative`, `Capability != Authority`, `Founder != Sole Creator`, `Investment != Invention`, `Product Success != Governance Legitimacy`, `Safety Claim != Safety Enforcement`. Pakai sebagai CF (Constitutional Findings) di akhir artifact.
7. **Verdict HOLD — bukan SEAL.** Setiap artifact berverdict HOLD pending F13 review. Jangan self-issue SEAL.

## Pitfalls

- **Dua beradik/orang duo = founder totals** — hypothesis "duo equals founder" mesti diuji dengan field-level verification. Anthropic alah dari "Amodei bersaudara saja" kepada tujuh pengasas (TIME, Wikipedia, Anthropic company page). Rule: kalau nama domain menunjukkan *founding team*, verify the count dulu, then map complementarity — bukan assume "two-person story" naratif.
- **Genderized "mind/hands" dichotomy** — Dario=intellectual+Daniela=operational framing ialah restating stereotype. Daniela di Stanford (Feb 2024) berkata "much more practical, the business oriented side" *bukan* "less intellectual." Rule: complementarity map, bukan binary intellectual/operational split. Frame organ-organisasi, bukan genotype manusia.
- **Cross-inherit conclusion dari prior artifact** — sam_altman.pdf mengata "Anthropic safety capability exited" tapi itu interpretation. Anthropic audit kena cross-audit dakwaan itu, bukan terus ulang. Rule: setiap cross-audit clause begins with its evidence class (FACT/QUOTE/INTERPRETATION), not a restatement.
- **Memoir-mode untuk orang sebenar** — jangan inventif childhood trauma, motif dalaman, atau motif kekeluargaan. Dokumen primer kalau ada tentang kerjaya/kehidupan profesional — guna. Reconstruction keluarga tanpa source = contamination. Rule: documented institutional authority only. Representation(Person) != Person.
- **Verdict SEAL** — user instructed HOLD pending F13 review. Self-issue SEAL adalah defect prioriti tinggi. Rule: HOLD dengan explicit gap disebut dalam text.
- **Source-class drift** — bila artifact mix Wikipedia, Reddit, dan 9to5AI dengan satu anggapan authority sama, constitutional doctrine collapses. Rule: Tier 1 = dokumen primer (charter, AG filing, IPO prospectus, arXiv paper). Tier 2 = laporan berkualiti (Reuters, TIME, MIT Tech Review). Tier 3 = wiki, blog, secondary. Restate hujah dengan source class explicit; kalau takde Tier 1, label UNKNOWN.

## Critical Typst escapes for this class

- **`*text*` bullet list at line start** — Typst interpret `*` sebagai emphasis, breaks with "unclosed delimiter." Guna `- text` untuk bullets. Kalau nak bold dalam bullet: `- #text(weight: "bold")[text]`.
- **`***` (3 asterisks) onomatopoeia / starred expletive** — Typst treat tiga asterisk sebagai emphasis delimiter. Tukar kepada dash atau punctuation (e.g. "fool" bukan "f---").
- **`$X` (USD atau nama)** sebagai math — escape dengan `\$`. kalau semua $ adalah math, perlukan global `\`-escape in execute_code pass.
- **`#align(left)[#sm[content]]` typos** — bila tiga escape levels nested, Typst quietly miss-parsing. Repair dengan replacing `#align[left)#sm[` ke `#align(left)[#sm[` dan tambah closing `]` pada akhir content block.

## Why this class beats plain biography

- Constitutional doctrine forcing artifacts mengasingkan *assertion* dari *evidence*. Bio naratif biasa mensyaratkan narrator to be likeable; audit documents narrator disappears to let evidence speak.
- BM Penang kampung voice menghalang over-claim. "Aku rasa", "aku claim", "aku tahu" semua disabled. "Dokumen mengatakan", "sumber primer X", "tier Y" semua required.
- HOLD verdict memaksa human-sovereign review — artifact bukan closure, tetapi disclosure.

## Relationship to adjacent artifacts

- Audit kelas ini duduk di downstream `sam_altman.pdf` (OpenAI) dan `elon.pdf` (Musk). Cross-audit obligation applies untuk any subsequent named-person artifact yang berada dalam lintasan capability OpenAI/AI/AGI. *Tidak* obligasi untuk persona di luar domain.
- Downstream consumers: human-sovereign F13 ratifies dengan examining HOLD queues di `/tmp/demis-pdf/` atau similar scratch path.
