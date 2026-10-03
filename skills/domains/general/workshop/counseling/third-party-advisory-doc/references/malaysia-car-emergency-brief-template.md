# Malaysia Car Emergency Brief — Template

Use when Arif asks for a procedural guide to forward to a family member or friend who drives but is not yet equipped for Malaysian car emergency (breakdown, accident, theft, flood, hijack-light scenarios). Recipients in scope: young siblings, parents who recently got a car, friends new to Malaysian roads, anyone Arif frames as "kena ingat ni untuk [nama]".

The deliverable is almost always a **PDF** (the recipient bookmarks it in phone). Multi-page is OK — this is a phone reference, not a chat reply.

## Verified hotline reference state (live-confirmed Oct 2026)

When producing this brief, anchor to these numbers. They were verified against official sources during the Azwa (Myvi 2019) session — re-verify if the brief is older than 6 months:

| Hotline | Number | Source / notes |
|---|---|---|
| Polis / ambulans / bomba emergency | **999** | Standard MCMC emergency line, 24/7 |
| Etiqa 24/7 Roadside Assistance | **1800-88-6491** | Verified from etiqa.com.my Help & Support page (Oct 2026). Tow + jump start + tayar tukar + locksmith (ikut plan) |
| Etiqa Claims Careline | **1300-88-1007** | Verify current — Etiqa contact page |
| Etiqa Customer Care (Mon–Fri 9–5) | **1300-13-8888** | General policy enquiries only |
| PLUS Highway Emergency | **1800-88-0000** | Standar lama; verify on PLUS official site for current routing |
| Perodua Careline (servis) | **1800-22-5555** | For Myvi/Kelisa/etc servis & recall |

**Never use web_search results for these numbers** — engines return homepage spam. Go directly to the insurer's contact/help-and-support page; that page IS the canonical source.

## Pitfall — Web search dies on Malaysian-specific queries

Observed pattern Oct 2026: queries like "Etiqa Takaful motor claim hotline Malaysia", "PLUS highway emergency 1800 88 0000", "Perodua Myvi 2019 recall" return either the insurer homepage, tourism content about Malaysia, or empty results. **Falling-back ladder:**

1. Direct `web_extract` to the insurer's `/contact-us` or `/help-and-support` page — these are short, structured, and authoritative
2. Wikipedia API for known entities (cars, highways, insurers)
3. If both fail, **label as memory-based + force live-verify at counter** (do not invent)

Do not present "1800-22-PERODUA" or similar guess numbers as fact. The recipient trusts Arif's name on the document; one wrong number costs real help.

## Document structure (use for new sessions — modify per recipient)

```
# Panduan Kecemasan Kereta — [Nama]
[Subtitle: kereta, plate, insurans, prepared by Arif + Wawabot + tarikh]

## 3 Nombor Wajib Ada Dalam Phone
Big-number table: 999 · Etiqa 1800-88-6491 · PLUS 1800-88-0000
(untuk insurant selain Etiqa, tukar ke hotline roadside syarikat tu)

## Senarai Nombor Penuh
Table dengan semua hotline di atas + insurant recipient punya hotline penuh

## Situasi 1: Kemalangan (langgar/dilanggar)
## Situasi 2: Rosak Tengah Jalan (highway vs jalan biasa)
## Situasi 3: Tak Boleh Start (bateri)
## Situasi 4: Tayar Pancit
## Situasi 5: Enjin Overheat
## Situasi 6: Banjir / Jalan Berair
## Situasi 7: Kunci Hilang / Terkunci Dalam Kereta
## Situasi 8: Kereta Dicuri / Pecah Kereta
## Situasi 9: Minyak Habis

## Kit Kecemasan — Check & Lengkapkan Dalam Boot
- Segi tiga amaran (wajib) · tayar spare + jack + spanar (wajib) · jumper cable (beli ~RM40 Shopee) · torch / powerbank · air botol + first aid · salinan geran + cover insurans

## Bila Chat Wawabot Masa Kecemasan — Template
Lokasi pin (paling penting) · apa jadi (1-2 ayat) · ada orang cedera? · plate · dah call siapa. **JANGAN hantar "tolong" je — Wawabot tak nampak lokasi.**

## Servis Berkala (khas untuk model kereta recipient)
- Minyak enjin: 10,000 km / 6 bulan
- Bateri: 2 tahun sekali (Myvi 2019 dah 7 tahun — patut diganti)
- Tayar: 5 tahun atau DOT code botak · tekanan ikut sticker pintu pemandu
- Roadtax + insurans: renew SEBELUM luput (app Etiqa+ atau MyEG)
```

## Recipient-specific facts (capture in PDF, never in chat)

Always leave editable boxes for facts the recipient knows better than the agent:
- Nombor polisi insurans
- Tarikh luput roadtax + insurans
- Warna kereta (untuk laporan curi)
- Bateri smart key jenis CR — check belakang fob / manual (don't guess)
- Tekanan tyar tepat — check sticker pintu pemandu / manual (don't guess generic)

Rule: estimate-vs-fact lines must say "verify kat [counter/manual]". A wrong battery type or tyre pressure can break AEDAP (xia).

## Anti-pattern: generic emergency cheat sheet

Pitfall: produce a 2-page bullet list that could apply to anyone. Recipient reads it as decoration. The brief works only if every section ties to:
- Their actual car (model, age → known issues)
- Their actual insurer (hotline, plan coverage)
- Their actual context (drives alone vs family, urban vs highway, day vs night)

When In doubt, ask Arif 2-3 questions: insurer apa, model kereta, drives mostly mana. Don't ask 10. The questions that matter are: **insurer** (changes hotline), **model + age** (changes common issues), **typical routes** (changes what hazards to emphasize: highway = PLUS hotline + jump risks; urban = scam tow truck warning).

## Delivery shape

- Render via `forge-pdf-delivery` pipeline: HTML → weasyprint → verify with `pdfinfo`
- 5-8 pages A4 is normal (this is phone reference, not chat)
- Top of PDF: name, plate, insurer — supaya kalau phone hilang, orang yang jumpa boleh baca
- Footer: "Sila verify [item 1, 2, 3] kat [kaunter/manual]" supaya recipient tidak assume generic = current
- Send via MEDIA: in Telegram; not as path /tmp/xxx.pdf — phone can't reach VPS path

## Source label at footer

```
Sumber: [insurer rasmi help page URL] (live Ogos 2026).
[Other hotlines] = hotline rasmi yang lama bertapak; sila verify sekali pada cover insurans/manual kereta.
999 = MCMC emergency standard.
[Cost estimates, e.g. bateri/locksmith/kunci] = julat pasaran 2026, boleh berubah.
Nota jujur: [model-specific facts] = smart pressure arif / sticker pintu pemandu; jangan ikut angka umum membabi-buta.
```

The footer does F2 honesty work — recipient knows what's verified and what's a rule-of-thumb.

## Sample structure for Myvi 2019 VBP9170 (Azwa session)

```markdown
# 🚗 Panduan Kecemasan Kereta — Azwa
Kereta: Perodua Myvi 2019 · Plate: VBP 9170 · Insurans: Etiqa Takaful
Disediakan oleh Abang Arif + Wawabot · Oktober 2026

[3 nombor + senarai penuh]
[6 situasi: kemalangan, rosak highway, bateri, tayar, overheating, banjir]
[Kunci hilang, kereta curi, minyak habis]
[Kit kecemasan]
[Template bila chat Wawabot]
[Servis berkala Myvi 2019]
```

Don't get into THIS because Azwa is sibling. Don't get into THIS because Arif framed it as "dia drive Myvi 2019 vbp9170". The recipient plate and model are routing signals — they let the agent skip the "apa kereta abang?" question and go straight to model-specific sections (Myvi 2019 = batteri dah 7 tahun, smart key CR type, compact spare tayar).