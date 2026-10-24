# Voice sample set — 2026-10-20

Satu baris sama, lima register. Label ikut asal-usul, bukan ikut nama dalam registry.

| # | Fail | voice_id | Asal-usul | f0 ukur | Gate |
|---|---|---|---|---|---|
| 01 | `01-siti__clone-of-sitinurhaliza.ogg` | `siti` | Clone of the real singer's voice, built on F13 instruction 2026-09-26. Not the principal's voice. | 198.6 Hz | PASS 100.0% |
| 02 | `02-pmx__clone-of-pmx.ogg` | `pmx-live-v1` | Clone of a 12.0s reference, F13-canon 2026-10-14. Derivative of a real public figure's voice, not an official recording. | 112.7 Hz | PASS 100.0% |
| 03 | `03-abang-sado-mad__clone-of-SYED.ogg` | `abang-sado-mad-v1` | Built from Syed's own 19.97s group voice note (2026-10-20). The only register in the set sourced from Syed. | 160.2 Hz | PASS 100.0% |
| 04 | `04-abang-sado-edge-deep__SYNTHETIC.ogg` | `abang-sado-edge-deep` | Vendor synthetic voice. NOT derived from any real person's audio. | 84.1 Hz | PASS 88.9% |
| 05 | `05-abang-sado-live-v1__clone-of-ARIF.ogg` | `abang-sado-live-v1` | Clone of F13's OWN 46.9s Telegram voice notes. Registry displays it as 'Abang Sado Syed'. Measured 97.5 vs principal's own note 97.6 Hz; Syed's notes measure 148-186 Hz. LABEL CORRECTED HERE. | 93.0 Hz | PASS 100.0% |

## Teks yang dibaca

> Selamat malam. Ini satu baris yang sama, dibaca oleh empat suara. Dengar beza dia.

## Cara ukur
parselmouth 0.4.7, praat autocorrelation 60–400 Hz, 10 ms step. F0 median voiced frames sahaja.

## Nota alat
`ffprobe` dalam build ffmpeg 9.0.1 di host ni **tidak memaparkan** Vorbis comment Opus. Tag ditulis dan disahkan dengan `mutagen.oggopus`, bukan dengan ffprobe. Jangan anggap tag tiada hanya sebab ffprobe senyap.

## Percanggahan yang belum diselesaikan
Registry masih melabel `abang-sado-live-v1` sebagai "Abang Sado Syed" dan mendakwa ia padan dengan register Syed 101.6 Hz. Ukuran sendiri: sumber klon 103.2 Hz, nota principal 97.6 Hz, nota Syed 148–186 Hz. Label registry itu salah dan belum dibetulkan — menunggu keputusan F13.