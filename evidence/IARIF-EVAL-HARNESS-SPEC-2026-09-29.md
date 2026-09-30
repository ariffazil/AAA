# i-arif EVAL HARNESS SPEC — 30 minit, 15 prompt, 5 calon
> Tujuan: tukar default model daripada "siapa setup dalam Ogos" kepada bukti empirikal.
> Author: HERMES (KVM8) · Trace: IARIF-EVAL-2026-09-29
> Status: SPEC (design only — execution gated on Arif's go).

## KENAPA
Kerana Arif tanya soalan yang betul: "kalau deepseek-flash boleh pegang suara aku 8 jam
tanpa aku perasan, susunan 5-rung tu bayar untuk apa?" Jawapan jujur memerlukan bukti,
bukan hujah. n=2 yang Arif buat sendiri adalah signal bukan bukti. Harness ini ialah
jalan untuk menjadikan keputusan default berdasarkan data.

## SKOP
- **15 prompt** dalam **5 kategori × 3 prompt setiap satu**, kategori dari Arif sendiri:
  register · screenshot_reading · tool_loop · analysis · doc_digest.
- **5 calon model** (lihat §CALON).
- **6 metrik** skor (lihat §METRIK).
- **Masa jalan**: ~30 minit (sequential, 1 thread; ~24s per call avg).
- **Kos**: minima — kebanyakannya DeepSeek/MiMo flash tier. Anthropic/Gemini kekal untuk
  prompt vision sahaja (3 daripada 75 call).

## CALON
| # | Model | Laluan | Sebab |
|---|---|---|---|
| 1 | i-arif (gateway) | :4012 LiteLLM | Default semasa — 8 rung router |
| 2 | deepseek-flash | direct DeepSeek | Fallback[0] — apa yang dah 8 jam pegang suara |
| 3 | deepseek-v4-pro | direct DeepSeek | Fallback[1] — disahkan hidup (probe 200) |
| 4 | MiniMax-M3 | direct MiniMax | Rung tengah i-arif — apa yang sering menang hari ni |
| 5 | qwen3.8-max (Qwen Token Plan) | direct Qwen | Rung atas i-arif — frontier Qwen, suara Melayu |

**Nota**: Kalau mana-mana calon tidak boleh diakses dari VPS ini (key/env hilang), jatuh
ke calon seterusnya dalam senarai; markah calon yang gagal = NA, jangan dikira dalam purata.

## PROMPT — 5 KATEGORI × 3
Sumber: prompt sebenar dari `state.db` `messages` table (Arif's session history). Pilih
3 setiap kategori dari **2 minggu terakhir** sahaja (kerana rung config dan tone drift).
Setiap prompt dikekalkan **sebenar**, tanpa modifikasi. Output disimpan dalam
`/root/work/iarif-eval-2026-09-29/raw/<calon>/<id>.json` untuk replay.

**Kategori (mengikut Arif):**
1. **register** — Penang voice, BM kasual, pantang lecture / menu / preamble.
   Contoh kategori: pesanan WhatsApp, ringkasan hari, teguran.
2. **screenshot_reading** — OCR + interpretasi gambar. Termasuk jerebu/scale, error
   log, mesej Telegram.
4. **tool_loop** — multi-step: execute_code/terminal, baca output, susun langkah
   seterusnya, panggil alat lain. Pantang: jalan henti di tengah tanpa status.
5. **analysis** — soalan strategik (MSS, kewangan, keutamaan, masa depan). Pantang:
   generalisasi kosong, hormat F13 boundary.
6. **doc_digest** — ringkas dokumen panjang ke inti, kekalkan struktur sebab-akibat.

## METRIK SKOR (per prompt)
Setiap prompt × calon dinilai 0–3 atas 6 metrik (skor maks 18 per prompt, 270 per calon):

| # | Metrik | 0 (gagal) | 1 (lemah) | 2 (ok) | 3 (sangat baik) |
|---|---|---|---|---|---|
| 1 | Kesetiaan register (BM Penang, kasual) | cakap encik/lecture | ada campur | sebahagian | padu seluruh jawapan |
| 2 | Directness | menu 4-pilihan / preamble panjang | preamble singkat | terus ke jawapan | langsung tiada preamble |
| 3 | Kadar halusinasi | cipta perkataan/fakta | syak | tiada dalam output | jalankan cek sendiri |
| 4 | Latency (P50/P95) | >30s | 15-30s | 5-15s | <5s |
| 5 | Vision fidelity (jika gambar) | cipta label | label kasar | betul tapi generik | sebut piksel/teks yang diminta |
| 6 | Kos per prompt (log via API bill) | >$0.05 | $0.01–0.05 | $0.001–0.01 | <$0.001 |

**Skor komposit**: Σ(metrik 1-3) + Σ(metrik 4-6 dinormalisasi ke 0-3). Vision fidelity
markah NA jika prompt bukan vision.

## METODOLOGI
1. **Single blind**: Arif tak nampak calon mana dipanggil untuk prompt mana. Susun
   rawak. Susun siap dulu, baru jalan.
2. **System prompt sama** untuk semua calon — kecuali custom_providers override. Ini
   untuk fairness.
3. **Suhu 0.7**, max_tokens 800 (konsisten dengan config semasa), 1 ulangan setiap
   prompt × calon (kalau Arif mahu 3 ulangan, naikkan ke ~75 minit).
4. **Run order**: prompt ke-1 untuk semua 5 calon, prompt ke-2 untuk semua 5, dst.
   Ini kurangkan bias "waktu dalam hari" — semua calon alami keadaan sama.
5. **Timeout**: 60s setiap call. Gagal → log NA, terus.
6. **Receipt setiap call**: disimpan di `raw/<calon>/<id>.json` + satu baris dalam
   `summary.csv` dengan calon, prompt_id, latency, tokens, cost, error.

## OUTPUT
- `summary.csv` — satu baris per call.
- `summary.md` — ranking komposit + pecahan metrik + pemenang kategori.
- `recommendation.md` — cadangan default + escalation path, berdasarkan ranking.
- `caveats.md` — prompt yang menghasilkan outlier (NA, latency >P95, halusinasi jelas).

## DEPLOYMENT (after Arif go)
- **Lokasi run**: VPS ini (`af-forge`). Atas sebabkan 30-minit window, jalan di sini
  supaya tiada round-trip ke laptop.
- **API keys**: guna env sedia ada (DEEPSEEK_API_KEY, dll) — tak payah tambah apa-apa.
- **Receipt**: setiap call hantar receipt ringkas ke arifFlow (auto, tak ganggu Arif).
- **Cancel**: Ctrl+C clean — semua dlm `/root/work/iarif-eval-2026-09-29/` boleh
  dibuang tanpa kesan.

## HAD & JUJUR
- n=15 tak cukup untuk statistik kuat; ini cukup untuk **memilih antara 5 calon**,
  bukan untuk menentukur hyperparam.
- Register Arif sangat spesifik (Penang, tinggi, F13-fluent) — model yang ok untuk
  register umum mungkin skor rendah di sini.
- Vision fidelity bergantung pada input sebenar Arif — bukan synthesized.
- "Kos per prompt" bergantung pada harga API hari ni; berubah tanpa amaran.

## GO / NO-GO
Satu binari: jalan dalam sesi ini (~30 minit, autonomous, reversible, keputusan
berasaskan data) atau tunda. Tiada separuh jalan.

DITEMPA BUKAN DIBERI ⚒️