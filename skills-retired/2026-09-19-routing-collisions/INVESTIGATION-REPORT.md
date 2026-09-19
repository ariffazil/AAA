# SIASATAN — `diverged: 1` dan asal usul fail dalam commit 1882799ee

**Tarikh:** 2026-09-19 · **Autoriti:** arahan Arif (F13) — siasat punca, HOLD dari semua mutasi, bentang laporan
**Status:** PUNCA DIASINGKAN · **TIADA MUTASI DIBUAT** sepanjang siasatan ini

---

# BAHAGIAN A — `diverged: 1` bukan defect store. Ia defect detector.

## Apa yang census buat

`/root/scripts/skills-census.py:81-101` membina indeks skill berkunci pada **laluan relatif
direktori**:

```python
rel = os.path.relpath(dp, root)      # cth: federation-topology/bridge-lane-functional-probe
out[rel] = {...}
```

Kemudian blok divergence (baris 187-190) **mengurangkan kunci itu dengan `basename` SEBELUM
memadankan**:

```python
cbase = {os.path.basename(k): v for k, v in canon.items()}
hbase = {os.path.basename(k): v for k, v in herm.items()}
shared = set(cbase) & set(hbase)
diverged = sorted(k for k in shared if cbase[k]["sha"] != hbase[k]["sha"])
```

Nama folder daun **tidak unik** merentas store. Bila dua skill berbeza berkongsi nama folder daun,
dict comprehension menyimpan SATU sahaja — dan pasangan yang tinggal itu dibandingkan lalu dilapor
sebagai "skill yang sama telah diverge".

## Bukti — pasangan yang dibandingkan SEKARANG

```
census melaporkan `diverged` = 1 : ['claude']
  kunci nama : 'claude'
  sisi kanun : apex_verdict_hold/claude         (11071 B)
  sisi hermes: FORGE-onboarding/claude          ( 5914 B)
```

Dua ini **skill yang berlainan sepenuhnya** — satu skill APEX verdict-hold, satu prosedur
onboarding agent. Yang sama cuma nama folder daun `claude`. Tiada apa-apa yang "diverge".

## Kenapa angka itu berubah bila aku betulkan case-twin tadi

Laporan sebelum ini menyebut `diverged: ['claude']` juga — tetapi pasangannya berbeza:
masa itu ia `apex_verdict_hold/claude` lawan `FORGE-onboarding/claude` **di dalam kanun sendiri**.
Bila aku bekukan `FORGE-onboarding/claude`, pasangan itu hilang — dan pasangan tak sengaja yang
BARU muncul (kanun lawan pokok hermes). **Angka itu bukan mengukur drift; ia mengukur pasangan mana
yang kebetulan terakhir menang dalam dict.** Itu tandanya metrik ini tidak pernah bermakna.

## Saiz kerosakan

| Ukuran | Nilai |
|---|---|
| set kunci yang dipadankan | **1** (sepatutnya ~642) |
| nama daun ambigu dalam kanun | **42** nama, menelan **103** entri menjadi 42 |
| nama daun ambigu dalam pokok hermes | **3** |
| **divergence SEBENAR** (padan ikut laluan relatif) | **0** |

Jadi verdict `WARN` yang keluar semalam **dipacu sepenuhnya oleh false positive**. Bahagian yang
paling serius: bila 103 entri mengecut jadi 42, mana-mana divergence YANG SEBENAR pun boleh
tertelan senyap — detector ini bukan sekadar memberi false positive, ia juga boleh memberi
false negative.

## Adakah ia pernah betul?

Tidak dapat disemak dari git: `skills/skill-library-integrity/scripts/skills-census.py` **tidak
ditrack** dalam repo /root/AAA. Salinan kanun ada di `/root/scripts/skills-census.py`. Tiada
sejarah commit untuk blok ini — jadi aku tidak boleh kata bila ia rosak, dan aku tidak akan
andaikan.

---

# BAHAGIAN B — 46 fail dalam commit 1882799ee: 29 kerja aku, 17 kerja lane lain

Aku commit dengan `git add skills/ skills-retired/ forge_work/` — dan `forge_work/` itu
menyapu kerja lane lain yang belum di-commit.

| Asal | Bilangan | Isi |
|---|---|---|
| Kerja aku (`skills/`, `skills-retired/`) | 29 | collision fix, ledger, corpse repair, alat |
| Lane lain (`forge_work/`, `scripts/`) | 17 | edition-004 cron output (mtime 06:07-06:08), alpha-zen cards, `publish_skills.py`, `served-surface-drift.md` |

**Kesalahan aku:** aku sapu kerja orang lain ke dalam commit yang mesejnya mengaku kerja aku.
Salah satu subagent aku sendiri **perasan dan sengaja mengecualikan** lane serentak daripada
commitnya — jadi bukti bahawa amalan itu memang ada, dan aku yang langgar.

## Asal `references/served-surface-drift.md`

- Ditulis **09:40:xx**, oleh lane serentak (bukan mana-mana subagent aku — tiada ledger aku
  menyebutnya; aku semak kesemua tujuh).
- Ia pasangan kepada `/root/scripts/publish_skills.py`, ditulis **09:36** oleh lane yang sama.
- **Ia dokumen yang sah dan berkualiti** — kelas yang sama aku geluti sepanjang hari ini
  (katalog sebagai salinan lawan sebagai pandangan). Ia menyebut alat yang benar-benar wujud,
  dan menerangkan tiga kerosakan berasingan yang masing-masing ada tandatangan dan ubat sendiri.

**Tetapi angka di dalamnya tidak boleh direproduksi:**

| Dakwaan dokumen | Ukuran aku sekarang |
|---|---|
| served root: 223 entri | **624** |
| 155 daripadanya mendedahkan SKILL.md | **601** |
| 18 entri adalah symlink keluar dari root | **31** |

Penjelasan paling konsisten: angka dokumen itu ialah keadaan **SEBELUM** alat itu dijalankan, dan
dokumen itu tidak melabelkannya sebagai sebelum — jadi ia gambar objek bergerak yang
dipersembahkan sebagai gambar mati. Itu **tepat kelas kesilapan yang aku dokumenkan pagi ini**
dalam `auditable-numeric-artifacts`. Aku tidak boleh sahkan keadaan sebelum itu (aku tidak
menangkapnya), jadi aku tidak akan tuduh ia salah. Aku cuma kata: ia tidak boleh direproduksi
daripada keadaan sekarang, dan sebabnya munasabah.

---

# BAHAGIAN C — PERCANGGAHAN LINTAS-LANE (penemuan paling penting)

Root yang dihidangkan kernel (`/etc/arifos/skills`) mengandungi **sembilan skill `understand-*`
sebagai SALINAN**:

```
understand  understand-chat  understand-dashboard  understand-diff  understand-domain
understand-explain  understand-figma  understand-knowledge  understand-onboard
```

**Dan salinan itu byte-identik dengan sumber VENDOR**, bukan dengan apa-apa dalam kanun:

```
understand-chat     served=5f1da70e0849ec2f  vendor=5f1da70e0849ec2f  IDENTICAL
understand-onboard  served=e5be45248859ca82  vendor=e5be45248859ca82  IDENTICAL
```

Kronologi:

```
09:20:42  aku bekukan sembilan understand-* dari kanun (sebab: 713 KB prosa vendor,
          sifar capability federasi, setiap badan menamakan plugin pihak ketiga)
09:36     lane serentak tulis /root/scripts/publish_skills.py
09:37:15  lane itu jalankan alat itu — root yang dihidangkan ditulis semula
09:40     lane itu tulis dokumen served-surface-drift.md
```

**Percanggahan:** pada 09:37 kanun SUDAH TIADA `understand-*`. Tetapi alat itu hanya berjalan atas
satu mesh (`LIVE_MESH = /root/AAA/skills`, baris 49) — jadi ia tidak boleh mendapatkannya dari
kanun. Penjelasan yang konsisten dengan kod alat itu sendiri: entri itu sudah ada dalam root
terhidang sebagai **symlink keluar**, dan pembetulan alat itu ("Guard collision → publish a copy,
not a link") menukarnya jadi salinan. Dir mtime 09:37 menyokong pembacaan itu.

**Aku tidak boleh sahkan sepenuhnya tanpa menjalankan semula alat itu — dan aku tidak akan, di
bawah HOLD.** Jadi aku laporkan apa yang diukur dan apa yang tinggal sebagai penjelasan yang
munasabah tetapi belum disahkan.

**Kenapa ini perlu keputusan, bukan pembersihan:** dua lane dalam sistem yang sama membuat
penilaian bertentangan tentang perkara yang sama. Aku kata sembilan skill ini **bukan** capability
federasi dan mengeluarkannya dari katalog kanun. Lane lain **menghidangkannya kepada kernel**.
Kalau seorang agent bertanya kernel "skill apa yang ada", ia akan melihat sembilan benda yang
kanun kata tidak wujud. Itu persis penyakit yang aku namakan pagi ini — katalog tidak sepadan
dengan realiti — kecuali kali ini dua permukaan yang kedua-duanya "rasmi" tidak sepadan.

---

# BAHAGIAN D — Apa aku TIDAK buat (HOLD dipatuhi)

Tiada satu pun daripada ini aku lakukan, seperti diarahkan:

- ✗ tiada pemadaman
- ✗ tiada repoint
- ✗ tiada mutasi state
- ✗ tiada suntingan pada `skills-census.py`
- ✗ tiada suntingan pada root terhidang `/etc/arifos/skills`
- ✗ tiada commit

Siasatan ini **baca sahaja**. Satu-satunya fail yang ditulis ialah laporan ini dan
`DIVERGENCE-INVESTIGATION.json` (artifak siasatan).

---

# BAHAGIAN E — Cadangan, sedia untuk dilaksanakan, menunggu keputusan

| # | Cadangan | Risiko | Boleh undur |
|---|---|---|---|
| 1 | **Betulkan detector** — gantikan padanan `basename` dengan padanan laluan relatif, dengan `basename` sebagai sandaran HANYA bila nama itu unik dalam kedua-dua pokok; tambah medan `ambiguous_leaf_names` supaya kerosakan itu kelihatan | rendah — fail bukan-kanun, tiada skill tersentuh | ya (git) |
| 2 | **Betulkan mesej commit** yang mengaku kerja lane lain sebagai kerja aku — atau terangkan dalam commit susulan | rendah | ya |
| 3 | **Label angka dalam `served-surface-drift.md` sebagai SEBELUM**, kerana nilai sekarang 624/601/31 — jika tidak ia jadi dokumen tak boleh disemak | rendah | ya |
| 4 | **Naikkan percanggahan `understand-*` kepada F13** — sama ada kernel patut menghidangkan katalog yang berbeza daripada kanun, atau tidak. Ini keputusan pemilik, bukan pembersihan | — | — |

Cadangan 4 ialah satu-satunya yang aku rasa perlu keputusan hang, sebab ia tentang **apa yang
kernel patut hidangkan sebagai capability**, dan itu soalan autoriti, bukan soalan kebersihan.

DITEMPA BUKAN DIBERI ⚒️
