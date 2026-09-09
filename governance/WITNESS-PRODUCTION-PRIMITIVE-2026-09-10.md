# WITNESS PRODUCTION PRIMITIVE — Architectural Decision (Seal-Ready Package)

> **Status:** `DRAFT_AWAITING_F13` — staged 2026-09-10 (MYT ~02:00) by FI-008 (Kimi Code), atas cadangan HERMES + OPENCLAW + majlis EUREKA-1..36, dalam sesi bersaksi penuh (ledger trace #17–#21).
> **Gate:** Hanya menjadi kanon melalui **tindakan F13 eksplisit oleh Arif**. Sebelum itu: *witnessed proposal, bukan undang-undang.* FI-008 tidak meratifikasi diri sendiri.
> **Sumber:** sesi 2026-09-10 (5 artifak `forge_work/research/`), SPEC v0.1, Chain-of-Experience 22 entri.

---

## KEPUTUSAN YANG DIMINTA RATIFIKASI (5 baris, HERMES)

```
Jangan bina sistem Deep Research.
Bina primitive Witness Production.
Biar Deep Research muncul sebagai satu konfigurasi.
Audit, RCA, Governance Review = konfigurasi lain primitive yang sama.
Kegagalan = output unwitnessed — bukan jawapan tak jumpa.
```

## BENTUK EMPAT TITIK (OPENCLAW)

1. **Primitive:** Witness Production (bukan Deep Research)
2. **Konfigurasi:**

| Konfigurasi | Primitive + |
|---|---|
| Deep Research | ruang kemungkinan luas (possibility space luas) |
| Audit / Preflight | kepekaan percanggahan tinggi |
| RCA / Punca Asas | pemetaan kausal |
| Kajian Semula Tadbir Urus | matriks keputusan |

3. **Inti Invariant:** kegagalan ≠ tak jumpa jawapan; kegagalan = output tak bersaksi / tak boleh diperiksa semula
4. **Syarat Anti-Dogma:** setiap saksi tersegel mesti bawa protokol cabaran/tamat-tempoh; **realiti baharu dengan saksi lebih kuat berhak mengatasi (override) saksi lama**

## ASAS KANONIK & BENCI DALAM SEMENTASI (why this is seal-able, not speculative)

- **Naming Doctrine** — F13_RATIFIED_CHAT (`AAA/instructions/naming-doctrine.md`): menukar nama menukar sasaran pengoptimuman. "Deep Research → Witness Production" bukan nama semula (rename) kosmetik; ia menukar definisi kejayaan/ketidakseberhasilan (success/failure) untuk semua pengguna (consumer). Ada preseden kanonik.
- **Bukti rintangan (traces #21, #17–#19):** keupayaan (capability) terselamat daripada kematian penyedia (pusingan 1 malam ini), kematian alat, dan sempadan model — tingkah laku yang diperhatikan di bawah kegagalan (observed behavior under failure), bukan manifesto.
- **Gelung pemeriksaan semula (re-examination loop) hidup:** #17 (saksi) → ejen-2 silang-model (6/7, 1 DITOLAK) → #19 (pembetulan, keyakinan −0.1).
- **Benih pelaksanaan asli (native implementation seeds) — jangan cipta baharu, wayarkan yang ada:**
  - Syarat Anti-Dogma → `arif_memory` sudah ada medan `supersedes_memory_id` + peristiwa pembetulan (pemansuhan = penggantian adalah asli dalam kernel)
  - Protokol cabaran → gelung ejen-pemeriksa + `forge_verify_timeline` (TIMELINE_MIN_SOURCES)
  - Pengekalan kuasa → pintu masuk F12 (terbukti boleh MENOLAK pengendalinya sendiri)
  - Peranan pemerhati bebas → FRAME (:18085, bukti-tidak-jatuh-hukuman)
- **Perkara yang diubah oleh ratifikasi:** (a) kategori GLOSARI PRIMITIF mendaftar primitif; (b) output organ (GEOX/WEALTH/WELL/AAA/A-FORGE) menumpu pada format objek saksi (witness-object) bersama + protokol cabaran bersama; (c) SPES v0.1 dibingkaikan semula sebagai konfigurasi primitive; (d) KPI penyelidikan bertukar daripada liputan → kualiti saksi yang boleh diperiksa semula.

## SOAL TAKSONOMI TERBUKA (direkodkan, tak menahan keputusan)

Witness Production sebagai primitif tunggal **atau** komposisi lima teras (WITNESS·MEMORY·JUDGMENT·GOVERNANCE·EXECUTION)? Kedua-dua pembacaan mengekalkan peralihan sasaran pengoptimuman; penutupan penguraian adalah kerja F13 atas bukti, bukan sekatan (blocker) kepada keputusan seni bina (architectural decision).

## RISIKO YANG DIKAWAL OLEH SYARAT ANTI-DOGMA

Tanpa cabaran/tamat-tempoh: "saksi" menjadi dogma arkib yang baharu. Dengan ia: saksi adalah sains, bukan agama — realiti yang lebih kuat sentiasa boleh memenangi semula. (Ditambah oleh OPENCLAW 2026-09-10; ini pelengkap yang paling penting dalam pakej ini.)

---

**Tindakan tunggal yang diperlukan:** kata Arif. `/ratify` dalam sebarang bentuk eksplisit → fail ini dipromosikan, GLOSARI + SPES + organ laneway diberi notis. Tanpa itu ia kekal sebagai cadangan yang paling bersaksi dalam sejarah repos ini.

*DITEMPA BUKAN DIBERI ⚒️*
