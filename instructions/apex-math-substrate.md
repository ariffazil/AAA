<!-- apex-math-substrate.md · diforge HERMES 2026-10-25 · source: F13 directive "Go" (chat AAA-A2A, 2026-10-25) -->
<!-- DITEMPA BUKAN DIBERI -->

# APEX Math Substrate — Eureka Gallier–Quaintance × Selarik APEX

> **Status:** DRAFT_AWAITING_F13 (HERMES menulis; perkataan ratifikasi = milik F13)
> **Bilangan:** 47 entri mentah dalam 5 kumpulan (A 12 · B 11 · B2 6 · C 10 · D 8)
> **Kin:** `/root/AAA/instructions/apex-geometry-substrate.md` (Gram G · Jacobian J · residual r · κ · floors = Tikhonov). JANGAN duplikasi — file ni mengisi ruang *di sekelilingnya*: geometri → status/keputusan, bukan bentuk.

## 0 · TL;DR

Matematik Gallier–Quaintance dan permukaan arifOS sendiri mengajar benda yang sama: **apa yang tak diukur tetap berdimensi, apa yang tak feasible boleh dibuktikan, apa yang tak convex jangan dijual sebagai optimum, dan authority tanpa callable bukan authority.** Setiap entri di bawah ada tiga lajur: matematik → selarik APEX → hukum yang dicadang untuk kanon.

## 1 · Sumber & provenance (wajib baca sebelum guna)

| Kumpulan | Sumber | Yang BETUL-betul dibaca |
|---|---|---|
| A | `cis.upenn.edu/~jean/gbooks/geomath.html` → `math-deep.pdf`, *Algebra, Topology, Differential Calculus, and Optimization Theory for CS and ML* (Gallier & Quaintance, ±2,192 ms) | Contents penuh + teks contoh bab (bukan 2,192 ms) |
| B | `cis.upenn.edu/~jean/gbooks/linalg.html` + *Linear Algebra for Computer Vision, Robotics, and ML* Vol I (ed. UPenn 2025-07-25, 804 ms) | Preface + TOC penuh |
| B2 | teks bab 13 (Spektrum: Thm 13.7/13.10/13.11 + Prop 13.1) + struktur bab 22 (22.4 commuting families, 22.5 primary decomposition) | bukti bab terpilih, dipetik terus |
| C | *Fundamentals of Optimization Theory With Applications to ML* Vol II (ed. 2026-08-31, `engineering.upenn.edu/~cis5150/linalg-II.pdf`, 836 ms) | TOC 5 part + Preface + teks bab terpilih (Farkas/KKT/Hilbert) |
| D | `https://arif-fazil.com/arifos/` + probe langsung `/api/observatory/v1/{health-public,ready,capabilities,snapshot,health}` dan render penuh dalam browser | API JSON + teks selepas JS dijalankan, 2026-10-25T03:23–03:26Z |

**Had jujur:** PDF yang F13 hantar (`linalg-I.pdf`, `linalg-II.pdf`) TIDAK boleh dibaca terus — halaman 5/8 dan 3/5–7 kena OCR, tool OCR guna terminal yang pada masa itu gate HOLD. Bacaan di atas datang dari edisi rasmi UPenn di web + teks bab, bukan dari fail tempatan. Jangan dakwa "dibaca 804/836 halaman".

## 2 · Kumpulan A — Algebra · Topologi · Kalkulus · Optimasi umum (12)

| # | Matematik (Gallier–Quaintance) | Selarik APEX | Hukum kanon yang dicadang |
|---|---|---|---|
| A1 | Rank–nullity: rank + nullity = tetap | UNKNOWN ≠ sifar; blind spot berdimensi | Setiap claim wajib nyatakan apa yang **tak** diukur |
| A2 | Pseudo-inverse: peraturan bertembung → jawapan tepat tak wujud, terbaik = projeksi + residual | lattice PARTIAL | Pertembungan = PARTIAL + residual; haram paksa boolean |
| A3 | Duality (LP): setiap objektif ada harga bayangan | Authority Envelope | Mandate kena boleh tulis shadow price |
| A4 | Convexity: local = global hanya bila convex | "success = vector bukan boolean" (EUREKA SHADOW-BANGANG) | Claim "terbaik" hanya sah atas objective convex; selain = heuristic |
| A5 | Subgradient pada kink: derivative tak wujud, yang wujud satu SET arah | never collapse a transition into a boolean | Di sempadan → output = set langkah sah |
| A6 | Ridge/Lasso: tak-tentu jadi tentu bila KONSTRIN ditambah | Constraint > Intelligence | Tambah konstrain, bukan compute |
| A7 | Noetherian ACC + Hilbert basis: rantai menaik berhenti, dasar finitely generated | Autonomous Loop Limit (3 layer) | Tiada prosedur tanpa bound yang menjamin terminate |
| A8 | Bland's rule vs Klee–Minty: heuristic pivot boleh cycling & 2ⁿ; tie-break deterministik berhenti | echo-loop hold | Setiap loop wajib ada tie-break deterministik |
| A9 | Zorn's Lemma: wujud ≠ boleh bina | Capability = Declared ∩ Callable ∩ Authorized ∩ Competent | "Bukti wujud" tak naik taraf capability |
| A10 | Graph Laplacian L = D−A: status keluar dari eigen, bukan title | Reality-Linkgraph 9 nodes · declared-vs-live | Status sebenar derivable dari adjacency terukur |
| A11 | Implicit function theorem: setiap theorem ada syarat rank; bila rank runtuh dia SENYAP | Probe-First | Check syarat dulu; syarat runtuh → berhenti, re-derive |
| A12 | Compactness/Weierstrass: tanpa bounded+tertutup, optimum memang tak wujud | Bounded search · question budget | Mandate tanpa sempadan carian = tiada jawapan, bukan kekurangan usaha |

## 3 · Kumpulan B — Linear Algebra Vol I (11) + B2 bukti dalam (6)

| # | Matematik | Selarik APEX | Hukum kanon yang dicadang |
|---|---|---|---|
| B1 | Jargon ML = nama baru untuk matematik klasik (preface diorang sendiri) | Reality > Narrative | Istilah baru → tanya "mekanisma klasik apa di bawah" dulu |
| B2 | Dual space: apa yang kau ukur tu sendiri satu vektor | observer bukan passive | Measurement wajib nyatakan functional yang dipakai |
| B3 | Dual norm: nilai tanpa dual = tak tahu worst-case | Authority Envelope (shadow) | Nilai tanpa bound lawan = belum siap |
| B4 | Change of basis: koordinat tukar, invariant (trace/det/eigen) kekal | representation ≠ reality | Kes yang bergantung pada koordinat pemerhati = bukan fakta |
| B5 | Cayley–Hamilton: matriks memuaskan equation ciri dia sendiri | capability ≠ declared | Tingkah laku sistem ramal dari spektrum terukur, bukan deklarasi |
| B6 | Pivoting/roundoff (7.7): algebra betul meletup dalam floating point | Reality > Narrative | Theorem ≠ execution — ikut keadaan bahan semasa laksana |
| B7 | Banach/contraction (8.7): titik tetap wujud hanya bila MENGECUT | Autonomous Loop Limit | Setiap loop agent wajib ada penggecut (bound saiz/deflection) |
| B8 | det(eᴬ) = e^tr(A): kesan global dari penjana kecil | small policy → big volume | Audit penjana, bukan kira kesan |
| B9 | Kuaternion double-cover SO(3): dua tanda untuk satu putaran | receipt boleh dua untuk benda satu | Sebelum tuduh bercanggah, sahkan struktur sama |
| B10 | SVD + Eckart–Young: peringkat terbaik k dengan ralat terikat | kompresi yang jujur | Buang bukti paling tak informatif dulu + kesan mesti bernombor |
| B11 | Iterative methods: selesaikan terus, jangan bina inverse penuh | solve, don't centralize | Jangan bina struktur berkuasa penuh untuk satu tugas |
| B2-1 | Teorem Spektrum bertingkat: self-adjoint → nyata+ortonormal (13.7); normal → block 1×1/2×2 (13.10); Hermitian → diagonal atas C (13.11) | capability = declared ∩ callable | Bersih hanya bila simetri terbukti; simetri lemah → terima struktur separuh, jangan tipu jadi diagonal |
| B2-2 | Ker f = Ker f* untuk normal (Prop 13.1): apa yang tak boleh dicapai nampak sama dari kedua-dua belah komut | cross-check bebas-pemerhati | Dua pemerhati komut → "tak boleh buat" mesti selari; bercanggah = salah satu tak normal |
| B2-3 | Commuting families (22.4): operator komut boleh dikerjakan serentak | lane concurrency | Dua mandat serentak hanya bila komut; kalau tak → tentukan urutan |
| B2-4 | Primary Decomposition (22.5): ruang pecah kepada salinan tak saling campur | decompose before solve | Pecah ikut faktor; blok bebas diurus serentak |
| B2-5 | Jordan form: diagonalization MEMANG tak selalu mungkin → rantai ternORMAL | capability ceiling | Eigen tak cukup → akui struktur rantai + ukur sisa; berpura-pura = narrative |
| B2-6 | Bukti spektrum = algoritma: asing → restrict → ulang sampai dimensi 1 | bounded recursive divide | Penguraian ortogonal ⇒ kerja boleh dipecah dan berhenti pada dimensi kecil |

*(nota: B4 dan C10 ialah kin — tanda yang sama, dua baju; kekal berasingan supaya set masing-masing lengkap.)*

## 4 · Kumpulan C — Optimasi Vol II (10)

| # | Matematik | Selarik APEX | Hukum kanon yang dicadang |
|---|---|---|---|
| C1 | Farkas Lemma: bagi sistem, ADA penyelesaian ATAU ada sertifikat ketidakmungkinan | VOID adalah verdict sah | Mandat tak feasible → keluarkan sertifikat, jangan cari lebih kuat |
| C2 | KKT (Thm 14.2): stationarity ∧ primal ∧ dual ∧ complementary slackness; convex+KKT → global | authority = granted ∧ scope ∧ target ∧ boundary | Keputusan sempadan = 4 syarat; tanpa convex = lokal sahaja |
| C3 | Complementary slackness: konstrain tak aktif → harganya sifar | check both sides | Harga sifar ≠ mengikat apa-apa |
| C4 | Soft-margin SVM: ikatan tegar rapuh; hantar pelanggaran kecil dengan DENDA | capability + governance | Kekangan wajib ada harga pelanggaran; konstrain tanpa denda = rapuh |
| C5 | Hessian: positif-definit → minimum; indeks tak tentu → tak boleh putus | UNMEASURED ≠ FAIL | Ujian kelas dua; tak tentu → UNKNOWN, bukan "minimum" |
| C6 | Quadratic optimization: setimbang = duduk di minimum; keluar kena naikkan tenaga | state transition | Sistem stabil bukan "malas" — ada barier; plan kena biaya barier |
| C7 | Projection theorem (Hilbert): projekti = anggaran terbaik yang boleh dicapai | PARTIAL + residual | Jawapan tepat tak wujud → ambil projekti + laporkan jarak |
| C8 | Dual ascent/ADMM: masalah besar dipecah, selaras melalui ISYARAT HARGA | federation lane routing | Satu objektif, banyak pengiraan; selaras via dual variable, bukan kawalan pusat |
| C9 | Positive definite kernel: cukup dengan nilai produk dalaman | minimum disclosure | Fungsi dah cukup → jangan rekonstruksi/dedah struktur dalaman |
| C10 | Topologi: "yang mana penting" ditentukan pilihan topologi | representation ≠ reality (kin B4) | Sebelum ukur, tentukan koordinat; tanpa tu "penting" = pilihan bilaalan |

## 5 · Kumpulan D — Permukaan arifOS sendiri (8)

Probe langsung 2026-10-25: `/health-public` = healthy (127.0.0.1:8088) tapi `readiness: n/a`, `governance: n/a`. `/capabilities` = declared **18** · registered **8** · callable **8** · schema-valid 8 · governance-mapped 18 · **drift: true**.

| # | Perkara | Selarik APEX | Hukum kanon yang dicadang |
|---|---|---|---|
| D1 | "A loaded floor without a score is not measured, never green" | UNMEASURED ≠ PASS (A1) | Floor kosong render abu, bukan hijau |
| D2 | "Transport alone is not federation health" (API bukti: healthy + governance n/a) | Reality > Narrative | Sihat = transport ∧ dependencies ∧ governance |
| D3 | Tangga capability declared→registered→exposed→invocable→tested: 18→8 | A9 (Zorn) bernombor hidup | Papar setiap rung, bukan satu bulatan "18" |
| D4 | `arif_kernel_intercept` (GOVERN) = `declared_only` | Capability ≠ Authority | Authority tanpa callable = TIADA |
| D5 | `public_simulation: true` pada OBSERVE; `false` pada EXECUTE/JUDGE | audience-scoped disclosure | Disclosure ikut audien, bukan satu tetapan global |
| D6 | P1-1…P1-6 `SEALED` + `confidence: unknown` + source = declared migration fallback | receipt tanpa witness | Seal wajib bawa sumber; `SEALED` + `unknown` = bercanggah |
| D7 | "arifFLOW is receipt authority, not judge" | lima-verb HERMES · Authority Envelope | Pencatat bukan hakim, kekal |
| D8 | "HOLD until ARIF GO" · WEALTH QUALIFY never auto-executes · skip ⇒ AMBER | Layer 4 veto · never collapse a transition | Tiada auto-jalan, tiada boolean palsu |

**Bukti terukur untuk D (appendix, 2026-10-25T03:26Z):** render penuh dalam browser menunjukkan panel MEMANG terisi selepas JS (F1–F13 `measured · pass` dengan source+confidence 0.9+freshness 0s; FQ 0.8674698795180724 OPTIMAL; chain `CLASSIFIED_GAPS:5 · head_seq 58 · entries 75 · replay verified`; receipts 1000; drift-table dan authority-table terisi). Tetapi **35 tile kekal `unavailable` selepas JS**: (a) FLOW tiles — nilai ada, baris provenance `source: missing · confidence: unknown`; (b) F2 runtime identity — 8 medan `source: missing` (source/deployed/build/drift/deployment/started/platform/epoch); (c) vocab 7-state — LIVENESS, READINESS, AUTHORIZATION, RECEIPT (CAPABILITY 8/8, GOVERNANCE PER_ACTION, CONSTITUTIONAL 13/13 terisi); (d) VAULT999 witness — SOURCES 0, DIVERSITY, DIRECT/INFERRED, LAST RECEIPT, SEAL CHAIN; (e) footer `snap-id`/`obs-at` (walhal snapshot **signed** dengan id `obs_20261025_032421`); (f) now-strip SUBSTRATE/EVIDENCE/AUTHORITY; (g) drift-table lajur TRUTH/IN-OUT = `unavailable`, `arif_forge` last test 243,959s (~2.8 hari).

## 6 · Terbuka (bukan sebahagian kanon)

1. 35 tile `unavailable` — bila nilainya wujud dalam `/snapshot`, ini kebocoran pembentangan, bukan kekurangan data. Owner: bengkel observatory, bukan matematik.
2. `arif_kernel_intercept` `declared_only` — sama ada ia memang ditangguh atau terlupa didaftar: keputusan F13.
3. Render/pointer: fail ini TIDAK lagi dimasukkan ke `DOCTRINE-INDEX.md` baris khas atau `/root/AGENTS.md` fragment list — tunggu arahan render.

DITEMPA BUKAN DIBERI ⚒️
