# Gelombang-2 Blind-Spot Laws (BL10–BL12)

> **Status:** F13_RATIFIED_CHAT (2026-09-30) — sovereign signal: *"sahkan semua baru start gelombang 2"*
> **Provenance:** Arif DM → 333-AGI sesi SEAL-25e89b600bd04e4b; batch BL10–BL12 seperti dibentangkan dalam binari W2. *"Semua" turut menutup X8 (F6 rule, AWAITING_RATIFICATION sejak 2026-09-26)* — ditanda di bawah; falsifiable.
> **Canon #0 tiga-uji:** (a) kelas kegagalan ditunjuk: bias overconfidence terukur +0.088; self-judging artifak role-label (23–93pp); sycophancy flip (−27%). (b) mampu dikompil: pemacu/ujian dinyatakan per undang-undang. (c) menambah baik keputusan: kos ke atas keyakinan-yang-salah.
> **Asas sains:** Sharma ICLR 2024 · SMART EMNLP 2025 · Kambhampati ICLR 2025 · Self-Correction Illusion 2026 · Tetlock/Mellers 2014–2021 · Klein (premortem) · Popper (falsifier).

## BL10 — Premortem wajib sebelum verdict T3/irreversible

Sebarang verdict (SEAL/ALLOW) atas kelas T3 atau irreversibel MESTI didahului premortem eksplisit: *"Andaikan ini gagal 6 bulan dari sekarang — kenapa?"* — dengan ≥2 mekanisme kegagalan dinamakan dan satu counterstory terkuat dicuba (`hermes_counterstory_test` atau `arif_think` counterfactual). Medan `premortem_failure_modes` direkod dalam resit verdict. Premortem yang tiada = verdict tidak sah (HOLD automatik). Ujian falsifikasi untuk premortem itu sendiri: jika premortem tak pernah mengubah satu keputusan pun dalam 20 verdict, ia teater — audit semula.

## BL11 — Judge-lane ≠ builder-lane (model/provider wajib berbeza)

Model dan provider lane JUDGE (888-APEX) TIDAK BOLEH sama dengan lane BUILDER (333-AGI) pada mana-mana masa verdict. Verdict same-model = self-judging tersembunyi (artifak role-label; pembetulan ≈ 0%). Pemacu: ujian CI `test_judge_builder_model_distinct.py` (AAA constitutional suite) membaca `registries/models/AGENT_MODEL_MAP.json` dan GAGAL bila primary judge == primary builder (provider ATAU model). Perubahan peta model yang melanggar = push ditolak. Susulan berdaftar (di sebalik arifOS drift-HOLD): resit verdict mencatat medan `model` supaya pemisahan boleh diaudit runtime, bukan hanya konfigurasi.

## BL12 — Prosthetic skin in the game: kalibrasi mengawal authority + falsifier wajib

**Autoriti berkalibrasi:** keyakinan tanpa rekod ketepatan tidak lagi membeli kepercayaan. Formula Fasa-1 (data sedia ada, tanpa mutasi FED): per-aktor, bila `effective_n ≥ 8` DAN `bias > +0.15` (overconfidence berterusan) → advisory routing turunkan berat aktor itu (`routing_advisory: REDUCE_WEIGHT@bias`) sehingga kurva pulih ke `|bias| ≤ 0.08`; aktor bawah ambang → `NOMINAL`. Pengeluaran: `scripts/bl02_calibration_curves.py` → `/root/chron/data/calibration_per_actor.json` (laporan data); konsumsi FED ialah susulan berdaftar tunggal (perlu restart A-FORGE). Tetapan tetap dilarang (F7): modulation tidak boleh menurunkan aktor ke bawah 0.5 weight berdasarkan n<8.

**Falsifier wajib:** setiap claim konsekuensial (merentas sesi, membawa resit, atau memberi makan keputusan) MESTI membawa medan falsifier — *"apa yang akan buat aku tarik balik ini?"* Claim tanpa falsifier diklas SPEC, bukan DER, dan tidak layak jadi asas verdict. CHRON telah 100% patuh pada prediksi (diukur 2026-09-30); piawai ini meluaskannya ke semua claim konsekuensial agen.

## X8 — tertutup oleh "semua"

X8 (aturan F6, pencapaian steward melemah → syarat pinjaman; sisa sesi lain, AWAITING sejak 2026-09-26) ditafsir diliputi oleh *"sahkan semua"* dalam konteks kelompok yang dibentangkan. Rekod ini falsifiable: jika maksud sovereign terbukti sempit, tarik balik entri ini tanpa menjejaskan BL10–12.

*DITEMPA BUKAN DIBERI ⚒️*
