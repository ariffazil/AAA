# OBSERVATORY SOT RECEIPT — 2026-10-06 00:3x–00:4x MYT
**FI-008 · session SEAL-b4e43ac3ee9e48b5 · F13 arahan: "make the site observability dynamic SOT" · protokol 8-peringkat arifOS dipatuhi (BACKUP→MUTATE→VERIFY→NOTIFY)**

## Akar & pembaikan
| Simptom (dump observatory) | Akar sebenar | Fix | Sah |
|---|---|---|---|
| `kernel epoch v1!2026.10.1` | `pyproject.toml version="1!2026.10.1"` (epoch PEP-440) jadi satu-satunya sumber `release_tag`; F13 canon (`/etc/arifos/canon/canon-release.json` → `2026.10.05-8d2d0be`) diabaikan | `build.py` — satu penerbit: env deploy → **canon-release.json** → pyproject (backup `.bak-20261006T0035-fi008-sot`) | ✅ snapshot `runtime_identity.kernel_epoch = 2026.10.05-8d2d0be` |
| `signature key_id/payload/signed_at: unavailable` | Snapshot 16:00Z dijana tanpa kunci dalam env | Emitter segar | ✅ `signature.state=signed, ed25519:sha256:698cc1ab…` — F-007 RESOLVED |
| `freshness: stale / 16m old` | cron 30-min | cron observatory sahaja **30→10 min** (backup `/root/crontab.bak-20261006T0040-fi008`; dua percubaan gagal pertama DITOLAK crontab validator — tiada kerosakan, sedia ada utuh) | ✅ `*/10 * * * * emit_observatory_snapshot` |
| Snapshot basi di webroot | — | Publish semula + `build_public_state.py` | ✅ `obs_20261005_163421` @ 16:34:21Z, headline "GATEWAY OPERATIONAL · GOVERNANCE HOLD", apex_G=0.875 |

## Yang dibiarkan JUJUR (bukan cacat)
- `organs.arifos.contract = v1!2026.10.1` — kernel yang **terpasang** (wheel 8d2d0be, kod build.py lama) melapor diri sehingga deploy akan datang. Realiti terpasang ≠ aspirasi kanon; observatory mesti laporkan yang sebenar. Bila 333-AGI deploy semula dengan build.py baharu, medan ini bertukar sendiri. **Flag untuk lane 333: sertakan build.py patch ini dalam deploy akan datang.**
- `capability tests 1/8, truth unavailable` — kebenaran ujian datang dari panggilan sebenar (arif_init 9s = panggilan aku). 7 verb tak diuji 2.6 hari = kebenaran, bukan bug paparan. P1: cron capability-probe ringan (arif_init/observe/route/think probe sekali sejam) supaya "tested" hidup.
- `drift: schema=UNKNOWN · route=UNKNOWN · upstream_repository=UNVERIFIED` — kolektor belum wujud untuk medan itu; paparan jujur "unknown" > hijau palsu. P1.
- `floors: 13/13 loaded · 2 measured` — placeholder confidence:0 dilabel "not measured, never green" — reka bentuk jujur (F2/F4/F5… perlu pengukur sebenar, bukan auto-pass).
- chain-health: 266 entries, 0 corrupt, **41 gaps** → didokumen dalam `observatory-chain-health.json` (kuarantin dilaporkan, tanpa senyap-baiki — F1).

## Baki terbuka (andaian "finish all tasks")
- **P0' memori** (semalam): audit-set refresh + kelas `witness_semantic` + FI-009/kimi-twin — sedia, sesi segar ini boleh terima order
- **P1**: reindex vault_canon(0)/petronas(90) · SATU SOT declaration (5 pendaftar) · skills reconciliation FAIL · SKILLS.json + TOOLS.json mint · audit→CI · capability-probe cron
- **333-AGI coordination**: kernel 8d2d0be deploy malam ini + build.py patch aku = dua lane sentuh repo sama; build.py aku di repo (belum commit — gitwrap) dan TIDAK mengubah runtime wheel; sertakan dalam deploy seterusnya

## Bukti
`obs_20261005_163421` (signed, canon epoch) di `/var/www/html/arifos/.well-known/observatory.json` + `public-state.json` ×3 path · emitter log stderr (publish OK, chain-health) · crontab line 52 `*/10` · `build.py.bak-20261006T0035-fi008-sot`
