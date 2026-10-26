# HUMAN-BRIEF.md — Ringkasan Realiti & Keputusan untuk Arif
**Tarikh:** 25 Oktober 2026 MYT · **Satu Ayat:** Membuang beban Arif menjadi 'router mesej' antara bot, dan membuktikan sistem hanya boleh buat perubahan jika ada kebenaran sah.

---

## 1. Apa Masalah Manusia Yang Diselesaikan?
Arif selama ini jadi "message bus" — setiap kali agent run, ia spam Telegram Arif atau tergantung minta kepastian. Sekarang sistem dibina supaya agent berhubung sesama agent dalam `inbox.jsonl`, dan **hanya ketuk pintu Arif jika ada sekatan sebenar atau keputusan bernilai tinggi**.

---

## 2. Apa Yang Telah Dibuktikan Secara Live? (BUKTI > STATUS)

1. **10 Ujian Loop Berjaya Bersih (10/10 PASS):**
   - [OBS] Kami bina dan jalankan test suite automatik (`test_verified_loop.py`).
   - Terbukti: Token palsu ditolak, token tamat tempoh ditolak, cubaan inject prompt ditolak, cubaan duplicate replay dihalang, dan crash sebelum receipt boleh dipulihkan tanpa re-run side effect.
2. **Audit 8 Tool Bahaya di A-FORGE (SELESAI):**
   - [OBS] 8 tool suspect (termasuk `forge_telegram`, `forge_drive_create`, `forge_seal_run`) telah diklasifikasikan dengan tepat.
   - [OBS] Tool baru yang tidak dikenali tidak lagi jadi "read-only" secara senyap — ia jatuh ke `MUTATE_FLOOR` (fail-closed). 343 ujian A-FORGE lulus.
3. **Misteri 79% CHRON Selesai Secara Matematik:**
   - [DER] 41 data sebenar: 30 betul, 7 salah, 4 mixed.
   - Ketepatan mutlak: **81.1%** (kes putus) atau **73.2%** (semua kes). Angka 79.5% datang dari kiraan markah separuh bagi 4 kes bercampur. Brier score = 0.1735. Tiada lagi nombor misteri.
4. **Keputusan Ujian Audit Yang Salah Fakta:**
   - [OBS] Tuduhan "prompts kernel rosak tiada messages" adalah SALAH (audit lama panggil tanpa parameter wajib). Bila parameter diberi, ia lulus 100%.
   - [OBS] Tuduhan "400 Bad Request" pada server HTTP adalah SALAH (protokol rasmi MCP memang wajibkan header session).

---

## 3. Apa Yang Masih Belum Selesai / Unknown?

1. [OBS] **Beban RAM & Swap:** Swap digunakan 94% (33 GiB) dan CPU load 16+ kerana banyak cron background berjalan serentak.
2. [OBS] **60 Link Mati di Gateway:** Federation gateway (:3003) masih mengiklankan resource `chron://state` yang beri 404 Not Found.
3. [OBS] **WEALTH outputSchema:** `capital_health` beri data betul tapi guna field `source_tool` bukan `tool_name`, jadi validator luar tolak.

---

## 4. Dua Keputusan Yang Arif Perlu Buat Sekarang

| # | Keputusan | Pilihan Tindakan Arif | Kesan Jika Setuju |
|---|---|---|---|
| **1** | **Buka freeze fail `.bak` lama di A-FORGE** | Bagi kelulusan `chattr -i` sebentar untuk fail `.bak` lama dan SOT registry. | Membolehkan A-FORGE kemaskini senarai 118 tools dan buang fail lapuk 15 hari lepas. |
| **2** | **Kebenaran Restart Kernel arifOS** | Bagi green light untuk `systemctl restart arifos.service` pada waktu senggang. | Mengaktifkan kod sekatan `arif_report` supaya mode tulis tidak lagi lepas sebagai read-only. |

---

*Fail lengkap, kod ujian dan arkib bukti tersedia di `/root/AAA/forge_work/next-horizon/`.*
