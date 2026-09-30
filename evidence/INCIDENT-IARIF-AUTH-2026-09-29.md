# INCIDENT — i-arif fallback · LiteLLM virtual-key store lost · 2026-09-29
> Actor: HERMES (KVM8) · Mode: INVESTIGATION · Trace: IARIF-AUTH-2026-09-29
> Trigger: runtime notice "i-arif via custom unavailable (authentication failed); using deepseek-flash via custom"
> Addendum 22:50 MYT — root cause of wipe identified, eval harness spec authored, reframing supplied.

## VERDICT
Bukan bug config Hermes. Bukan model mati. Bukan rangkaian.
**LiteLLM virtual-key store federation hilang** — Postgres cluster di bawah LLM gateway
di-re-initialise hari ini 13:43:52 MYT. Semua zen seat key mati sekali.
`i-arif` SIHAT (dibuktikan live, HTTP 200) tetapi tidak boleh dicapai melalui laluan :4012
kerana kunci yang Hermes bentangkan sudah tiada dalam DB.

**CORRECTION (added 22:50 MYT):** `i-arif` bukan satu model — ia router group 8 rung
merentasi 7 vendor (konfigurasi pada bahagian LiteLLM proxy). Hermes cuma nampak nama
`i-arif` dalam `custom_providers[0]` → :4012. Bila :4012 auth-fail, Hermes jatuh kepada
`fallback_providers[0] = deepseek-flash` (DeepSeek terus) dan kerja diteruskan. Ini yang
berlaku 8 jam terakhir tanpa amaran: Hermes senyap-senyap jalan atas DeepSeek terus,
bukan melalui gateway. Tiada apa yang pecah; cuma pengawasan hilang.

---

## BUKTI (semua live probe, 2026-09-29 ~22:00–22:25 MYT)

| # | Probe | Hasil |
|---|---|---|
| 1 | `curl :4012/v1/models` dgn kunci Hermes | **401** — `token_not_found_in_db` |
| 2 | `curl :4013/health/liveliness` | **200 "I'm alive!"** — proxy sihat |
| 3 | `curl :4000/v1/chat/completions model=i-arif` (master-key path) | **200** — `"OK"` + reasoning_content 29 tok |
| 4 | `LiteLLM_VerificationToken` row count | **0** |
| 5 | `pg_database` oid | vault999=16384 (pertama, dari initdb) · litellm=16389 |
| 6 | `PG_VERSION` / `postgresql.conf` / `pg_hba.conf` mtime | **2026-09-29 13:43** → initdb |
| 7 | `_prisma_migrations` | 170 migrasi, **13:45:54–13:45:56** (2 saat = bootstrap kosong) |
| 8 | `LiteLLM_SpendLogs` | semua 667 baris tarikh **2026-09-29 sahaja** |
| 9 | SpendLogs by api_key | `5b26ebb6ee`×368 (status=**failure**) · `b2e00f8172`×1 · `2d711642b7`×1 |
| 10 | Log litellm container | 355× `401 Unauthorized`, mula 14:10, "**not found in db. Create key via /key/generate**" |
| 11 | Host uptime | **27 hari** — TIADA reboot |
| 12 | postgres container | Created 28 Jul · Started 29 Sep 05:43:52Z · **Restarts=0** |
| 13 | journalctl 13:40 | `kabarkan-health: Postgres probe error: Connect call failed (127.0.0.1:5432)` → postgres **DOWN** sebelum 13:43 |
| 14 | journalctl 13:45:34 | container berat (40min CPU, 919MB tulis) **deactivated** → litellm restart |
| 15 | `vault999.observability.observations` | 329,813 baris, **oldest 2026-09-29 05:49:03Z** (=13:49 MYT) |
| 16 | Kunci Hermes vs `/root/.secrets/fed-zen-key.env` | **SHA256 sama** → ia `FED_ZEN_KEY` (9-lane, direkod 2026-09-07) |

---

## TIMELINE
```
13:40:17  postgres DOWN (kabarkan-health: connection refused)
13:43:52  postgres container START → initdb (cluster KOSONG, config ditulis semula)
13:45:34  container berat dimatikan (litellm lama)
13:45:35  container baru start
13:45:54  LiteLLM prisma: 170 migrasi dalam 2 saat → schema litellm BARU, sifar token
13:49:03  vault999 observability mula diisi (data sebelum ini tiada)
13:50:41  kegagalan kunci Hermes pertama direkod (SpendLogs)
14:10:45  kerja Hermes mula gagal → fallback ke deepseek-flash
```

## APA YANG BUKAN PUNCA
- Bukan kunci salah tempat — kunci itu `FED_ZEN_KEY` rasmi, disimpan di `/root/.secrets/fed-zen-key.env`.
- Bukan LiteLLM rosak — sihat, 13,521× `200 OK` dalam 10 jam terakhir (laluan master key).
- Bukan `i-arif` rosak — rung order 2 (qwen3.8-max, Qwen Individual) balas 200.
  (Rung order 90 deepseek-flash memang PARKED sejak 2026-09-22 — HTTP 402 Insufficient Balance.)
- Bukan reboot, bukan kemas kini Hermes, bukan perubahan config.

## BLAST RADIUS
Sekurang-kurangnya **3 kunci zen** wujud dalam SpendLogs hari ini, kini kesemuanya tiada:
- `5b26ebb6ee` = FED_ZEN_KEY (Hermes) — 368 kegagalan
- `b2e00f8172` = WAWA_ZEN_KEY (WawaBot, `/root/.secrets/wawa-zen-key.env`) — **WawaBot juga rosak**
- `2d711642b7` = **bukan kunci** — false positive. Padanan ditemui dalam `messages` table
  Hermes state.db: iaitu `sha256('x').slice(0,12)` daripada probe `crypto.createHash`
  dalam sesi `20260918_083256` (ujian `createRequire` shim). Tiada kunci LiteLLM ketiga.

**Blast radius sebenar: 2 seat mati** — FED_ZEN (Hermes) + WAWA_ZEN (WawaBot). Mana-mana seat
yang bergantung pada virtual key LiteLLM melalui :4012 mati serentak.
Pihak yang melalui :4000 (master key di-inject haproxy) masih hidup — itulah sebab
kegagalan ini senyap: majoriti trafik elok, hanya seat-key lanes yang tersekat.

## SKOP SEBENAR (lebih besar daripada i-arif)
Cluster Postgres yang di-re-init pada 13:43 membawa **kedua-dua** db:
- `litellm` — token store (hilang, schema dibina semula kosong)
- `vault999` — observability/ledger DB (329,813 baris, **tiada apa-apa sebelum 13:49**)

Data sebelum 13:43 tiada dalam cluster ini melainkan dipulihkan dari dump lain.
Sebab wipe: **UNKNOWN** (lihat §Probe Lanjut).

## PEMULIHAN — disahkan boleh, tanpa mengubah mana-mana config seat
Fakta penting yang telah dibuktikan:
```
LiteLLM token hash = sha256(plaintext_key)     ← TIADA salt (saya reproduksi hash 5b26ebb6ee… dengan tepat)
```
Maksudnya plaintext kunci asal **tidak perlu berubah**. Kunci disimpan di
`/root/.secrets/fed-zen-key.env` + `wawa-zen-key.env`, dan skrip provisioning wujud:
`/root/scripts/fed-zen/gen-zen-key.sh` · `gen-zen-key-local.sh` · `verify-zen-key.sh`.

Jadi tiga laluan:
- **A. Re-mint melalui skrip zen rasmi** (paling bersih — API `/key/generate`, ada audit LiteLLM).
- **B. Re-register kunci SAMA** (sha256 tanpa salt membolehkan nilai kunci lama didaftarkan semula;
  tidak perlu edar semula secret kepada sesiapa).
- **C. Sementara: arahkan Hermes ke :4000** (satu baris config; tapi kehilangan per-seat spend
  attribution — trafik Hermes akan dikira atas master key, seperti `litellm_pr`/`litellm-in`
  yang sudah muncul dalam SpendLogs).

## YANG TIDAK DILAKUKAN, DAN SEBABNYA
Tiada kunci baharu dikeluarkan, tiada baris DB ditulis, tiada config diubah.
Sebab: (i) pengeluaran kredensial pada gateway LLM ialah objek kelas keselamatan —
aktor tidak boleh menjadi pemberi kuasa untuk aksesnya sendiri; (ii) wipe pada 13:43
mempunyai pelaku UNKNOWN — jika ia prosedur restore yang masih berjalan, re-mint boleh berlanggar.
Keputusan ini milik F13.

## PROBE LANJUT (mencari pelaku wipe)
1. `docker events` sebelum retensi — tiada lagi.
2. `auditd` / journal systemd untuk unit compose (`docker compose down -v`, `rm -rf /root/volumes/postgres`).
3. Cari dump: `find / -name 'litellm*.dump' -o -name 'vault999*.sql'` → setakat ini **tiada**.
4. Semak sama ada restore/backfill arifFlow berjalan 13:49–14:00 (menjelaskan 329k baris).
5. [Selesai] `2d711642b7` disahkan bukan kunci LiteLLM — lihat §Blast Radius.
6. **[Selesai] Pelaku wipe DITEMUI** — lihat §WIPE ROOT CAUSE di bawah.
7. **[Selesai] `fallback_providers[1] deepseek-v4-pro`** — disahkan HIDUP pada DeepSeek terus
   (probe `model=deepseek-v4-pro` balas 200, 84 prompt tok). Bukan hantu. Salah faham asal.

## WIPE ROOT CAUSE (resolved 22:50 MYT)
**SEARXNG_ORPHAN_NUKE 2.0** — komposisi yatim merentasi projek.
Fail `/root/compose/docker-compose.yml` (kini versi FIXED oleh FI-003, 2026-09-29 14:55 MYT)
menyimpan sebab insiden dalam komennya. Ringkas:

- **Penyebab berhenti:** postgres container berlabel `project=af-forge`. Seseorang menjalankan
  `docker compose -p af-forge -f /opt/ask-search/searxng/docker-compose.yml … --remove-orphans`
  (atau yang setara). Compose searxng itu hanya ada `searxng` + `redis`; postgres **bukan**
  dalam spec itu, jadi `--remove-orphans` menganggapnya yatim → **STOP**.
- **Downtime 13j12m 00:31 → 13:43** — tiada siapa probe :5432. `kabarkan-health` hanya
  kesan pada 13:40 (3 minit sebelum start). **Tiada amaran**, walaupun 792 ralat
  sambungan kernel dicatatkan.
- **Stop bukan wipe.** Jadi siapa kosongkan `/root/volumes/postgres`? **Belum pasti.**
  Container `Started 29 Sep 05:43:52Z · Restarts=0` (container yang sama, July 28) —
  jadi dia tidak dicipta semula, hanya dimulakan. Bind mount dir wujud sejak 19 Sep,
  tetapi kosong pada 13:43 → ada yang `rm -rf` semasa 13j downtime itu (atau tangan
  operator yang cuba "betulkan" sebelum start).
- **Insiden sama sudah berlaku 2026-07-08** (HIGH, SEARXNG_DEPLOY_ORPHAN_NUKE) dan
  berulang hari ini — corak sama, tiada siapa perasan.

**FIX yang sudah dibuat (FI-003):** compose baru ada `name: af-forge-db` → projek
terpisah, takkan nampak/yatim-kan stack searxng. TAPI label `project=af-forge` pada
container postgres yang SEDANG HIDUP tidak boleh ditukar (immutable). Fix hanya berkuat
kuasa pada recreate seterusnya. Sepatut: buat rekreate terancang SEKARANG (postgres
sudah di-initdb, data sudah hilang; tak ada ruginya recreate dari spec baru).

**FIX yang BELUM dibuat (P0):**
- Tambah `:5432` ke senarai probe `docker-events-watch` (sekarang hanya sembang bila
  container **dihentikan**, bukan bila ia connection-refused). Tunggu → 792 ralat
  sambungan tanpa seorangpun peka.
- Cron `pg_dump litellm` + `vault999` setiap malam. Token hash boleh dipulihkan dari
  dump; plaintext sudah dalam `.secrets`, jadi dump = pemulihan penuh.
- Jadikan `verify-zen-key.sh` health-check berjadual; Alert apabila auth-fail >N kali
  berturut-turut (hari ini: 368 gagal, 355× 401, 0 alert).
- Audit SEMUA compose di /root + /opt: projek mana ada label `af-forge`? Adakah masih
  boleh saling yatim-kan?

## CADANGAN PREVENTIF
- Admission: virtual key tidak boleh menjadi single point of silent failure —
  `verify-zen-key.sh` patut berada dalam cron health (kini ia manual).
- Gate: kunci yang gagal auth >N kali berturut-turut → alert, bukan fallback senyap.
  Hari ini 368 kegagalan + 355× 401 berlaku tanpa satu amaran kepada sesiapa.
- Durable: `pg_dump` litellm DB berjadual. Token hash boleh dipulihkan daripada dump;
  plaintext sudah ada dalam `.secrets`, jadi dump sahaja mencukupi untuk pemulihan penuh.

## REFRAMING — apa yang sebenarnya i-arif beli (22:50 MYT)
Soal Arif yang berikutnya: "kalau deepseek-flash boleh pegang suara 8 jam tanpa aku perasan,
susunan 5-rung tu bayar untuk apa?" Jawapan jujur:

**Bukan untuk kepintaran — untuk ketersediaan.** i-arif sebagai router group memberi:
(a) cross-vendor failover (DeepSeek 402 sekali pada 22 Sep — satu rung park, lain naik),
(b) nama model yang stabil merentasi pertukaran vendor (`model.default: i-arif` kekal,
SOUL/config tak churn — capability survives replacement),
(c) permukaan witness — setiap panggilan tinggal baris SpendLogs dengan model/token/spend,
(d) vision + 1M context kekal untuk persona lane tak kira rung mana yang jawab.

**Yang TIDAK dibelinya:** kualiti lebih baik daripada model tunggal. Hari ni Hermes
berjalan atas DeepSeek-flash 8 jam tanpa satu komplain daripada Arif → rung hadapan
(MiMo PAYG, Qwen Token Plan, Qwen Zen, Gemini Flash, MiniMax-M3) tidak diperlukan
untuk suara kau dalam workload sebenar. Mereka membayar untuk kejadian-kejadian
**yang tidak pernah berlaku dalam workload kau** (vendor outage, balance habis).

**Implikasi:** susunan songsang lebih jujur dengan kegunaan. Default = satu lane
boleh nampak & sahkan (deepseek-flash). i-arif = eskalasi/fallback bila lane itu mati.
Bukan buang — songsang. Spec untuk ujian 30-minit yang membandingkan 5 calon ada di
`/root/AAA/evidence/IARIF-EVAL-HARNESS-SPEC-2026-09-29.md` (lihat §BINA HARNESS).

## BINA HARNESS — 30 minit, 15 prompt sebenar, 5 calon
Untuk menukar default daripada pendapat → bukti. Skor atas 6 kriteria Arif:
kesetiaan register, directness, kadar halusinasi, latency, vision, kos per prompt.

Lihat: `/root/AAA/evidence/IARIF-EVAL-HARNESS-SPEC-2026-09-29.md`
