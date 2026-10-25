---
name: short-stay-listing-vetting
description: "Use when vetting an Airbnb or Booking listing link."
version: 1.0.0
tags: [rental, airbnb, vetting, malaysia, travel]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Short-Stay Listing Vetting (Airbnb / Booking / Agoda)

Untuk nightly/weekly stay. Beza dari bilik sewa bulanan: harga bergantung tarikh, tuan rumah selalunya syarikat pengurusan berbilang unit, dan kontradiksi sering ada dalam teks listing itu sendiri.

## 1. Ambil isi listing

`web_extract` pulang kosong pada Airbnb (JS-rendered + consent wall). Guna browser:

```python
new_tab(url); wait_for_load()
js("(() => document.body.innerText.slice(0,12000))()")
```

`innerText` bawa description, amenities, house rules, review dan profil host dalam satu dump. Screenshot tak perlu.

## 2. Harga untuk tarikh sebenar

Tambah pada URL: `?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD&adults=N`. Baris harga keluar sebagai "X for N nights, originally Y" bersama frasa "Prices include all fees" — sahkan frasa tu ada sebelum sebut harga sebagai harga penuh. Tanpa tarikh, page cuma tulis "Add dates for prices".

## 3. Scan kontradiksi (langkah paling bernilai)

Baca description lawan amenities lawan house rules. Listing kerap bercanggah dengan dirinya sendiri — contoh lazim: WiFi tersenarai dalam amenities dan "Guest access", tapi blok "Other things to note" tulis tiada WiFi. **Jangan pilih satu dan senyap** — lapur kedua-dua versi dan jadikan ia soalan kepada host.

Yang kerap bercanggah atau tertimbus: waktu check-in (4pm) vs check-out (12pm), parking berbayar cash, deposit kad akses, denda merokok, larangan tetamu langsung, "quiet time" selepas 10pm.

## 4. Forensik host + review

- Profil host: tahun hosting, jumlah review, response rate. Host pengurusan besar bermaksud unit yang hang dapat bukan semestinya yang dalam gambar — cari ayat "a few units in the same building / may not be the exact room". Kalau ada, minta pengesahan unit dan keadaan peranti (aircond, air panas).
- Histogram rating: peratus 5★ lawan 1–2★. Baca review bintang rendah untuk kecacatan fizikal berulang. Satu review buruk pada listing 25 review = risiko spesifik pada unit, bukan bunyi statistik.

## 5. Keselamatan — sebut status, bukan andaian

Airbnb papar "Carbon monoxide alarm not reported" / "Smoke alarm not reported". Itu **tidak dilapor**, bukan **tiada**. Guna perkataan tepat tu.

## 6. Bentuk jawapan

1. Satu baris identiti listing + harga sebenar untuk tarikh diminta (tukar ke RM kalau pengguna Malaysia).
2. Senarai lulus: apa yang memang ada (TV/Netflix, mesin basuh, dapur, aircond, fasiliti bangunan + waktu operasi).
3. 2–4 gate: kontradiksi, unit bergambar vs unit sebenar, kos tersembunyi, alarm tak dilapor.
4. Satu baris verdict ikut tujuan — transit/tidur vs kerja dari bilik (kerja dari bilik perlukan WiFi disahkan bertulis oleh host).

Jangan hurai amenities satu-satu. Soalan "ada apa" jawab ada/tak ada; berat letak pada gate.

## Pitfalls

- Jangan quote harga tanpa tarikh — page tanpa tarikh tak tunjuk harga langsung.
- Jangan andaikan "WiFi" dalam amenities bermaksud WiFi berfungsi; semak blok nota bebas.
- Jangan anggap gambar = unit. Host berbilang unit akan tulis sendiri yang ia mungkin berbeza.
- Jangan lupa kos sampingan: parking harian, denda, deposit kad — jumlahkan sebelum verdict.
