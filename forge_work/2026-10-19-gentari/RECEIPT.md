# GENTARI — PEMBETULAN REALITI + PUBLISH · 2026-10-19

F13 order: "Betulkan!! REALITY > EVERYTHING … Spawn coding agent. Hang jadi manager for the site"
(Telegram DM 267378578, 19 Okt 2026, 22:54 MYT).

Dua dokumen disemak lawan sumber primer, dibetulkan, dirender semula, dan diterbitkan live
di arif-fazil.com. Semakan dipimpin dan disahkan oleh Hermes; deploy dijalankan oleh satu
subagent leaf (deleg_21050a27) dan disahkan semula dengan probe bebas.

## 1. Audit — apa yang tahan, apa yang pecah

| Dakwaan | Sumber diperiksa | Keputusan |
|---|---|---|
| Semua angka kewangan Gentari FY2024 | CTOS/SSM `ctos-gentari.txt` baris 250–305 | TEPAT sampai sen |
| "RM1.71 bilion = 13.29 − 11.48" | Aritmetik CTOS | **SALAH** — 13.29 − 11.48 = 1.81 |
| 4.2GW "sudah beroperasi" | IR2025 penuh (grep `GW`, `operational capacity`, `4.2`) | **TIADA DALAM SUMBER** — satu-satunya angka ialah 9.1GW "installed and under construction" |
| Takrif kapasiti berubah 2025 | IR2025 hlm. 66 nota 1–2 | **BETUL, verbatim** |
| Hasil segmen Corporate & Others RM10.6b | IR2025 segment review | **SALAH** — RM13.2b (2024: RM14.0b); LAT RM0.5b (2024: RM0.8b) |
| KKR ₹6,000 crore / RM2.6b / opsyen / Sapphire US Holdco / CCI | Economic Times + The Edge, 19 Okt 2026 | BETUL |
| ₹73.6 = "kadar tahun 2024" | ECB/IRS purata tahunan | **SALAH** — 73.6 ≈ 2021; 2024 = 83.677 → US$717m |
| 50% India: EV $2–2.5b, ekuiti $600–700m | Livemint, Jan 2026 | BETUL |
| Perak 680MWac + BESS, RM10b, 21 tahun, COD 2029 | Bursa Malaysia (Gamuda/SDG), 29 Sep 2026 | BETUL |
| H2biscus/H2ornbill dikecilkan; RM20 → RM50/kg | Nikkei Asia, Borneo Post, Malay Mail | BETUL |

## 2. Pembetulan yang dibuat

**Dossier (8 suntingan termasuk 1 bahagian baru):**
1. Ringkasan — buang 4.2GW; nyatakan 9.1GW satu beg bercampur.
2. Ringkasan — jurang ekuiti RM1.81b, baris rizab RM1.714b.
3. §3 — ganti "4.2GW beroperasi" dengan nota kaki takrif IR2025 + 8.4GW Gentari (30 Jun 2025).
4. §4 — aritmetik penuh: 12.999 − 1.714 + 0.196 = 11.48.
5. §7 — hasil segmen RM13.2b, LAT RM0.5b.
6. §11 — buang 4.2GW.
7. Sumber — tambah nota kaki IR2025 + MoF Fiscal Outlook 2027.
8. **BAHAGIAN BARU** "Sambungan: siapa bayar bila duit ketat" — capex RM54.2b→RM41.6b, dividen RM20/27/32b, PIC ~RM26b, LNG Canada Fasa 2 C$33b, Gentari capex RM6.1b→RM2.5b.

**Bangang (7 suntingan termasuk 1 bahagian baru):**
1. Item 3 — jurang RM1.81b.
2. Item 5 — ditulis semula (9.1GW satu beg; 4.2GW bukan angka rasmi).
3. Item 6 — nota kaki verbatim; "berapa banyak bateri tidak diberitahu".
4. Item 10 — tambah hasil segmen RM13.2b / LAT RM0.5b.
5. Item 14 — kadar rupee betul (73.6 = 2021; 2024 = 83.677 → $717m).
6. **BAHAGIAN BARU** "Bila duit negara ketat, siapa yang kena potong".
7. Sumber — MoF 2027 + nota kaki IR2025.

## 3. Fail PDF

- `gentari-dossier-2026-10-19.pdf` — 10 halaman, REV2
- `gentari-15-benda-bangang-2026-10-19.pdf` — 6 halaman, REV2
- `gentari_dossier.typ`, `gentari_bangang.typ` — sumber boleh render semula
- `*REV2.txt` — teks diekstrak untuk audit

## 4. Publish — apa yang live

| URL | Laluan manusia | Laluan bot |
|---|---|---|
| https://arif-fazil.com/world/makcikgpt/gentari-15-benda-bangang | 200 · 14,957B · `text/html` | 200 · 10,594B · `text/markdown` |
| https://arif-fazil.com/world/makcikgpt/gentari-dossier | 200 · 28,018B · `text/html` | 200 · 23,264B · `text/markdown` |

Fail: `/var/www/html/arif/makcikgpt-md/{slug}.html` + `.md` + shell `/var/www/html/arif/world/makcikgpt/{slug}/index.html`,
semua `644 www-data:www-data`, sha256 sumber = sha256 deploy.

**Surface discovery — semua hijau:**
- landing `/world/makcikgpt/` (React) — 90 pautan, 2 slug baharu; bundle `index-Cpo7Ud5Z.js`
- bot-lane landing (UA GPTBot) — `makcikgpt-md/index.html`, 44 entri
- `articles.json` — 44 entri, 2 gentari
- `llms.txt`, `feed.xml`, `sitemap.xml` — 2 rujukan setiap satu
- `node --test tests/makcik-source.test.cjs` — **10/10 pass**

**Regresi:** 12 artikel jiran + `/`, `/vitals/`, `/world/`, `/words/`, `/world/makcikgpt/` — semua 200.

## 4b. Penyelarasan reka bentuk (F13 order: "make the design aligned with all other articles")

**Defect yang dibetulkan:** dua artikel ini mula-mula disajikan sebagai HTML bespoke
(13.6KB / 26.7KB, `<style>` sendiri, kelas `.cover`/`.fact`/`.foot`) di webroot —
bukan template artikel MakcikGPT. Semua 42 artikel lain menghidang **shell SPA**
8,202B yang sama, dan React (`MakcikGptArticle.tsx`) render `meta.title` + body `.ts`.

**Fix (4 lapisan):**

1. **Shell** — `dist/world/makcikgpt/{slug}/index.html` (8,202B, SPA shell std)
   dipasang ke webroot menggantikan HTML bespoke. Diff vs sibling: identik
   (beza hanya skrip anti-bot Cloudflare yang disuntik di edge).
2. **Body `.ts`** — ditulis semula ikut template kanonik: `<article class="makcik-article">`
   → `<section class="article-section article-opener">` (blockquote emas `#D9A62E`) →
   `<section class="article-section">` × N dengan `<h2 style="…Georgia…1px #1F2733">` →
   `<footer class="article-footer">` (hashtags + signature + `<details class="receipts">`).
   Kelas `.cover`/`.cover-title`/`.fact` dibuang; kotak data jadi `.fact-box` /
   `.fact-box-title` / `.fact-box-content` / `span.label`. `<h1>` dalam body dibuang —
   `MakcikGptArticle.tsx` yang render h1 dari `meta.title` (uppercase).
3. **Lapisan bot** — `generate-md-mirrors.cjs` dijalankan semula: `.html` mirror
   dijana dari `.ts` kanonik (0 `<style>`, 0 `<link>`, 1 `makcik-article`), `.md`
   dapat frontmatter `article_id m6-6/m6-7` + Claim Register + Source Ledger.
4. **Discovery** — index, articles.json, llms, feed, sitemap dijana semula dan dipasang.
5. **Seluruh korpus** — 62 shell SPA lain (beranda, /world/, /words/, /makcikgpt/*, /work/, dll.)
   masih menunjuk bundle lama `index-DmLLK0hq.js` selepas build baharu. Semua 62 dipasang
   semula dari `dist/` supaya satu hash bundle untuk seluruh site. 44 shell `/world/makcikgpt/*/`
   kini satu hash (`4fad10c1…`). Baki rujukan bundle lama: **0**.

**Bukti parity (computed style, human lane, Chrome 129 UA):**

| Properti | taufik-pergi-mana (sibling) | gentari-15-benda | gentari-dossier |
|---|---|---|---|
| title suffix `— MakcikGPT \| arif-fazil.com` | ✓ | ✓ | ✓ |
| h1 uppercase / 48px / Newsreader / `#EDEAE2` | ✓ | ✓ | ✓ |
| body bg `rgb(10,11,13)` | ✓ | ✓ | ✓ |
| h2 Newsreader / 24px / border 1px `#1F2733` | ✓ | ✓ | ✓ |
| `.makcik-article` max-width 800px | ✓ | ✓ | ✓ |
| `.signature` + `details.receipts` + `.hashtags` | ✓ | ✓ | ✓ |

## 4c. Punca sebenar — wrapper `<article>`/`<section>` dalam badan `.ts`

**Diagnosis:** 7 artikel (termasuk 2 Gentari) menulis badan `.ts` dengan
`<article class="makcik-article">` + `<section class="article-section">` sendiri.
`MakcikGptArticle.tsx` sudah membungkus body dalam `<article class="prose">` dan
selector `[&>h2]:…` hanya mengenai **anak langsung**. Jadi h2 dalam `<section>`
terlepas semua styling → jatuh ke global `h2 { Cabinet Grotesk 18px }`.

Hasilnya 7 artikel nampak berbeza daripada 37 yang lain, walaupun CSS sama.
Ini juga sebab `.cover`/`cover-title` masih muncul pada sesetengah halaman:
`index.css` sembunyikan `.cover` hanya bila ia anak `.makcik-article` — tetapi
`cleanHtml` (baris 36–38 `MakcikGptArticle.tsx`) yang buang cover hanya apabila
corak tepat.

**Fix:** buang semua wrapper `<article>`, `<section>`, `<footer>` daripada badan
`.ts` 7 artikel itu — biar React yang membungkus, sama seperti 37 artikel lain.
`<h2 style="…Georgia…">` inline juga dibuang; kini semua h2 ikut token.

Disemak: 7/7 tiada baki `section`/`makcik-article`; tag balance OK; h2 computed
style **Newsreader 24px border 1px** pada ketujuh-tujuh, sama dengan sibling.

## 4d. Kerosakan lain yang ditemui semasa menyelaraskan

| Defect | Bukti | Fix |
|---|---|---|
| 62→109 HTML merujuk bundle JS berbeza | `index-DmLLK0hq` (lama) vs `index-DNeIMmCN` (baru) | semua HTML dipasang dari `dist`; 109/109 satu hash |
| `/world/` kad Politik → `/politics/` 308 ke `/world/politics/` | redirect chain | pautan terus ke destinasi |
| `/world/` kad KLCI/USD-MYR → 308 | idem | pautan terus |
| `/world/` footer Malaysia → `/malaysia/` 308 | idem | → `/wealth/malaysia/` |
| `/vitals/` nav tiada **MAKCIKGPT** | nav 5 item vs 6 di seluruh site | ditambah; nav kanon 6 item kini sama pada 7 halaman |
| `/vitals/` footer Doctrine `/doctrine/` 308 | idem | → `/words/doctrine/` |
| `/vitals/` render-vitals tulis semula nav lama | `dist/vitals/index.html` stale | nav dipatch pada `dist` + live |

## 5. Perubahan sumber (SOT, bukan live sahaja)

- `src/data/essays.json` — 2 entri M6 (n=6, n=7) + claim_register (14 dan 13 item) + source_ledger 9 sumber. Backup: `essays.json.bak-20261019-gentari`.
- `src/data/makcikgpt/gentari-15-benda-bangang.ts`, `gentari-dossier.ts` — modul artikel.
- `src/data/makcikgpt/index.ts` — import + modules + meta.
- `public/makcikgpt-md/` — index, articles.json, llms.txt, llms.json, 4 fail artikel.
- `public/world/makcikgpt/` — articles.json, llms.txt/json, 2 shell artikel.
- `public/feed.xml`, `public/sitemap.xml` — dijana semula.
- Live webroot: artikel, index, discovery, `dist/assets/` (rsync additive, tiada `--delete`).

## 6. Terbuka / tak disentuh

1. **4 aset /geox/cockpit/** (`d3-*.js`, `index-Bihn1Ma3.css`, `index-CL-syAr-.js`, `maplibre-*.js`) tiada dalam webroot. **Pra-wujud** — bukan dari deploy ini (rsync additive). Bukan skop Gentari.
2. **Cloudflare purge tidak dijalankan** — token `cfut_…` sah (`/user/tokens/verify` lulus) tetapi tiada kebenaran `cache_purge` untuk zone ini (`Authentication error`). `articles.json` / `llms.txt` masih boleh disajikan dari cache CF di sesetengah PoP. Kandungan asal di origin betul; ini kelewatan propagasi, bukan data hilang.
3. **`/vitals/` masih versi 27 September** — trigger 9 Oktober (RM32b) belum ditulis masuk.
4. **`scripts/prerender-articles.cjs`** hardcode `DIST=/root/arif-sites/...` — laluan mati sejak repo pindah. Shell artikel baharu dibuat manual.
5. **Angka 4.2GW** dibuang kerana tiada sumber awam. Boleh dimasukkan semula hanya dengan dokumen yang dinamakan.

## 7. Verifikasi akhir (probe bebas oleh Hermes)

- `document.title` = "MakcikGPT — Gentari: 15 Benda Yang Tak Masuk Akal"
- teks badan 1,601 perkataan; `RM1.81 bilion` hadir; `4.2GW` tiada
- landing: `gentari_links: ["/world/makcikgpt/gentari-dossier","/world/makcikgpt/gentari-15-benda-bangang"]`
- `node --test` 10/10 pass
