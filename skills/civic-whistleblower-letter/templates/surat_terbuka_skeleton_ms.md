># SURAT TERBUKA SKELETON (Bahasa Malaysia)

Skeleton untuk civic whistleblower letter dalam Bahasa Malaysia. Adapt voice mengikut user.

## Header

```
SURAT TERBUKA KEPADA [TUJUAN SPESIFIK]
[Sub-tajuk yang menangkap inti dalam satu baris]

Kepada:
[YANG BERHORMAT [NAMA MP / JAWATAN],
[Jawatan Rasmi]
[Alamat Rasmi]]

Tarikh: [Tarikh]
Rujukan: [Nombor rujukan dalaman jika ada]
```

## Salutation

```
Yang Berhormat [Nama MP / Pengerusi Jawatankuasa],

Saya menulis surat ini sebagai warga Malaysia yang prihatin dengan [institusi/topik]
dan ingin berkongsi beberapa pemerhatian untuk pertimbangan [Yang Berhormat /
Jawatankuasa / Parlimen].
```

## Body Section 1: Konteks & Pengakuan

```
Saya sedar [Yang Berhormat / Jawatankuasa] telah pun menjalankan beberapa
langkah berkaitan [topik] -- termasuk [rujuk siasatan/audit/pertanyaan
parlimen yang relevan]. Saya menghargai kerja tersebut dan surat ini
bertujuan untuk menambah perspektif, bukan menggantikannya.
```

## Body Section 2: Fakta yang Boleh Disemak

Setiap angka mesti ada sumber. Setiap baris mesti ada dalam laporan awam.

```
Berdasarkan [nama laporan rasmi] yang diaudit oleh [nama juruaudit]
untuk tempoh [tahun]:

[Tarikh / Tahun]   [Perkara]                    [Sumber]

[Setiap baris data mestilah sesuatu yang pembaca boleh semak dalam
lima minit melalui carian web biasa.]
```

## Body Section 3: Analisis / Pemerhatian

```
[Ini bahagian di mana penceritaan berlaku. Gunakan voice yang
sesuai (Bahasa Makcik untuk Arif).]

Cerita pertama: [Fakta utama]
Cerita kedua: [Muka manusia -- jiran/orang biasa yang terkesan]
Cerita ketiga: [Pola sistemik]
Cerita keempat: [Soalan akauntabiliti -- siapa jaga?]
```

## Body Section 4: Permintaan Spesifik (SATU)

```
Berdasarkan pemerhatian di atas, saya memohon [Yang Berhormat /
Jawatankuasa] mempertimbangkan satu tindakan khusus:

"[PERMINTAHAN YANG SPESIFIK, BOLEH DIUKUR, SUKAR DITOLAK]"

Tindakan ini:
- Boleh dilaksanakan dalam tempoh [X] bulan tanpa peruntukan tambahan
- Boleh diukur melalui [metrik yang jelas]
- Tidak memerlukan pendedahan maklumat sulit atau sensitif
- Akan meningkatkan ketelusan awam tanpa menjejaskan operasi
```

## Body Section 5: Penutup

```
Saya tidak mendakwa [permintaan] akan menyelesaikan semua isu.
Saya hanya percaya satu langkah yang boleh diukur adalah lebih baik
daripada seribu rungutan tanpa tindakan.

Saya sedia untuk [memberikan maklumat tambahan / mengemukakan
dokumen sokongan / hadir memberi penjelasan] sekiranya diperlukan.

Sekian, terima kasih.
```

## Sign-off (Anonim)

```
Yang benar,

[Seorang Warganegara Malaysia]
[Tarikh]
[Bandar]
```

**JANGAN letak nama, alamat rumah, e-mel peribadi, atau apa-apa
yang boleh dikesan kepada penulis dalam masa kurang dari 4 klik.**

## Cryptographic Footer (ZKPC Seal)

Letak visual ZKPC seal di sini atau di muka surat terakhir.
Rujuk `templates/zkpc_visualization.py` untuk generate.

```
[Visual SHA-256 + Merkle root seal]

Penjelasan ringkas: Setiap angka dalam surat ini boleh disemak
melalui [nama laporan] di [URL]. Tanda hash di atas mengesahkan
bahawa data adalah sama dengan apa yang dilaporkan secara awam.
Pengarang surat ini kekal tidak dinamakan untuk melindungi
keselamatan peribadi dan profesional.
```

## Pitfalls Yang Kena Elak (Bahasa Malaysia Version)

| Pitfall | Contoh Buruk | Contoh Baik |
|---|---|---|
| Label moral | "Tengku Taufik seorang yang tamak" | "Jawatan Presiden & Ketua Pegawai Eksekutif Kumpulan mengesyorkan dividen RM32 bilion untuk FY2025" |
| Analogi geopolitik | "Ini macam Israel-Palestin" | "Apabila [pihak A] mengambil tanpa had, dan [pihak A] tidak pernah cukup, dan setiap kali [pihak A] mengambil lagi -- itu bukan strategi" |
| Baseline shopping | "Untung turun 58%" (ukur dari puncak FY2022) | "Untung turun 17% YoY pada FY2025; dan dividen tetap RM32 bilion, meningkatkan kadar pengekstrakan" |
| Dakwaan palsu | "Tiada siasatan dijalankan" | "Tiga siasatan telah dijalankan, termasuk Jawatankuasa Pilihan Khas Parlimen Oktober 2025; saya memohon [badan] mempertimbangkan status pelaksanaan syor-syor tersebut" |
| Permintaan kabur | "Hentikan rasuah" | "Isytihar secara terbuka bila kadar pengekstrakan dividen melebihi 65% PAT" |

## Quick Reference: Bahasa Makcik vs Formal BM

| Formal BM (Jangan Guna) | Bahasa Makcik (Guna Jika Arif) |
|---|---|
| "Berdasarkan analisis data..." | "Makcik kira duit." |
| "Terdapat beberapa faktor..." | "Hang baca betul." |
| "Saya memohon pertimbangan..." | "Makcik nak tanya..." |
| "Tidak dapat dinafikan bahawa..." | "Ini fakta. Bukan cerita WhatsApp." |
| "Pihak kami menyarankan..." | "Satu benda yang Makcik nampak." |
| "Untuk maklumat lanjut..." | "Kalau hang nak tahu lagi..." |