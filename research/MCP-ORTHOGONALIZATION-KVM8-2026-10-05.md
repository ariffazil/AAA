# MCP FLEET ORTHOGONALIZATION — RESEARCH + SOT AUDIT
**KVM8 (forge) · 2026-10-05 · actor kimi-code/FI-008 · session SEAL-8ae3ddee596e4f87**
Inputs: live probes (this session) + canon digest (`ARIF_FLOW_METABOLIC_PLANE.md`, `SIX_CONSTITUTIONAL_LEDGERS.md`, `topology.md`, `attention-init-boundary.md`, `organs.yaml`) + 6-harness MCP census.

---

## PART 1 — SOT AUDIT VERDICT (claim-by-claim)

Scale: ✅ CONFIRMED · ⚠️ CONFIRMED-DETAILED (numbers moved since report) · ❌ REFUTED

| # | Claim | Verdict | Live evidence (2026-10-05 23:0x MYT) |
|---|---|---|---|
| 0 | Door pattern: `https://<organ>.arif-fazil.com/mcp` untuk A–B | ⚠️ | `well/geox/wealth/hermes/fed/chron/forge` → 200+session-id ✅; `arifos` + `mcp`(hub) → 200 **stateless** (no sid); `frame` → **502 door broken** (organ hidup); `aaa` → 405 (tiada /mcp — betul, Group C); `aforge.` → **tak resolve** (door sebenar: `forge.`) |
| 0 | Group C = Tailscale mesh 100.64.0.0/10 / loopback | ✅ | headscale aktif; tailscale0=100.64.0.2/32; ~20 servis bound ke mesh IP; fed/frame/arifflow tiada vhost MCP |
| 1 | WELL degraded, source 3e2e663 ≠ deployed 7a145bf | ✅ EXACT | `:18083/health`: `source_commit:3e2e663, deployed_commit:7a145bf, drift:true`. `.git_commit`=7a145bf. Service di-restart hari ini (21:07 MYT) tapi dari **artefak lama** — pipeline deploy, bukan restart, yang rosak. Version `v2026.07.24` hardcoded di `server.py:1972,2589` |
| 2 | GEOX page 27 vs live tools | ⚠️ WORSE | Page hardcode **"27 public MCP tool"**; live `tools/list` = **20**; `apps.json` (regenerated hari ini, commit f7574fc) cakap **"7live"**. Tiga nombor terapung serentak |
| 3 | Version stamp berselerak | ✅ | Page: v2026.07.24×2 + v2026.10.03 + v2026.10.04 · llms.txt: v2026.06.14 · WELL: v2026.07.24 (hardcoded) · GEOX: 2026.10.05-regenerated-7live · **Kernel canon: 2026.10.05-2097b44** (satu-satunya yang minted/F13-ratified) |
| 4 | /metrics/json + /sse mati; counts box lari | ✅ | Kedua-dua → 404, kedua-dua di-advertise pada page ("A2A fallback", "/sse"). Counts box JS fallback=35 vs live hub `/mcp` resources=40. (Nombor report lama 4-vs-35 dah anjak, tapi discordance kekal) |
| 5 | A-FORGE handshake strict | ✅ EXACT | `tools/list` tanpa header → `400 "Bad Request: Mcp-Session-Id header is required"`; dengan sid → 200, **122 tools**. Bukan mati — strict stateful, bukan standard streamable-HTTP stateless |
| 6 | AAA :3001 + signing :18900 degraded | ✅ + WORSE | :3001 `status:degraded, deployment_drift:true` — **deployed 2caa6b0 ≠ source 3893c4c: penyakit sama seperti WELL** · G=0.583 DEGRADED · QDF=0.25. :18900 `can_sign:false, sovereign_presence_guard:UNCONFIGURED`, key_loaded:true, PAM ok, serving:true |
| V | "Semua organ hidup, 0 mati" | ✅ (asterisk) | Semua process organ aktif — frame-mcp aktif locally (`/opt/frame/mcp/frame_mcp_fastmcp.py`); tapi **frame public door 502** = satu door tak boleh connect |

**Verdict keseluruhan laporan: ~95% SOT-accurate.** Mekanisma dan struktur semua betul; beberapa nombor spesifik telah anjak lagi sejak ditulis (bukti tambahan untuk tesis "nombor tangan-maintain sentiasa basi").

### Finding BARU (di luar 6 laporan)
- **N1** `frame.arif-fazil.com/mcp` → 502 (cloudflare error). Organ hidup; vhost/gateway route patah.
- **N2** `aforge.arif-fazil.com` tidak wujud dalam DNS; `a-forge.` → 301. Penamaan ghost.
- **N3** AAA ada **deployment_drift:true** sama kelas dengan WELL → ini **debt sistemik pipeline deploy**, bukan 2 bug terpencil.
- **N4** `VAULT999/MCP_ENDPOINT_REGISTRY.md` (2026-08-01, docker-era) stale vs bare-metal live; bertentangan dengan `topology.md:49` (hub door = arifOS atau A-FORGE? — tiga-arah aliasing `arifos`/`arifosmcp`/`mcp`). **Live mengukur hub/mcp = 8 tools = arifOS-shaped** — mengesahkan undang-undang `topology.md:6`: *"live :port/health beats every prose table."*
- **N5** Skew permukaan perhatian: forge=122 tools vs organ lain 7–20. `mcp-compress.sh` (discover-then-invoke) sudah wujud sebagai preseden penyelesaian.

---

## PART 2 — DIAGNOSIS: SATU PUNCA, BUKAN TUJUH

Kesemua 6 defect + N1–N5 adalah **satu failure class**: *buku akaun fleet (kiraan, versi, endpoint, permukaan) di-maintain secara manual di N tempat, tanpa minted SOT.*

Arsitektur sudah **mereka-bentuk** penyelesaiannya dan biarkan dalam karantina:
- `TOOLS.json` — ledger ke-5 daripada Six Constitutional Ledgers, direka sebagai "governed-availability SOT" untuk fleet — **masih QUARANTINED, tak dimint** (`ARIF_FLOW_METABOLIC_PLANE.md:39`: "5 forged. TOOLS in quarantine").
- Corak yang sudah TERBUKTI berjaya untuk topology: `organs.yaml` → fragments → re-render `AGENTS.md` → `universe-drift-sentinel.sh` hourly. Buku akaun versi/kiraan hanya perlu **corak yang sama**, bukan mesin baharu (Anti-Bangang LAW 8).

> "Runtime does not discover reality. Runtime inherits reality." — SIX_CONSTITUTIONAL_LEDGERS.md:5

## PART 3 — PRINSIP: PERMUKAAN ADALAH VIEW, LEDGER ADALAH TRUTH

Setiap angka yangArif jumpa rosak hari ini ialah **salinan tangan** sesuatu yang boleh dijana:

```
                    ┌── TOOLS.json (minted, immutable, git-tagged)
MINT (on deploy) ──►├── kernel organ_shas snapshot (sudah wujud dalam arif_init!)
                    └── live /mcp tools/list + /health probe (satu laluan)

RENDER (dari MINT sahaja, tiada tangan):
  ├── page count boxes / footer version / llms.txt  (hub)
  ├── CANONICAL_PUBLIC_SURFACE.json + apps.json     (setiap organ)
  ├── version stamp → SATU nilai: kernel canon version
  └── MCP_ENDPOINT_REGISTRY.md → dijana semula / ditanda basi

VERIFY (sentinel sedia ada): universe-drift-sentinel hourly
  = bandingkan view vs live probe → lisan → tiket pembaikan automatik
```

Sekatan: **tiada fail HTML/JSON/markdown yang mengandungi angka fleet boleh di-edit tangan.** Angka hanya lahir dari MINT. Ini sahaja membaiki findings 2, 3, 4, dan N4 serentak — satu path, satu owner (generator), tiada patch berpecah.

## PART 4 — LIMA PAKSI ORTHOGONALISASI (satu invariant setiap satu)

| Paksi | Soalan | Mekanisma (SUDAH wujud dalam canon — dilanjutkan, bukan dicipta) |
|---|---|---|
| **A1 Authority** | Siapa boleh buat apa? | `authority_ceiling` per organ dalam `organs.yaml` (JUDGE_ONLY · EXECUTE_AFTER_SEAL · COMPUTE_ONLY · REFLECT_ONLY · ADVISORY_ONLY · RELAY_ONLY · METABOLIZE_ONLY · DISPLAY_ONLY · OBSERVE_ONLY) + AAA_TOOL_RIGHTS_POLICY lanes. Orthogonality paksi ini = satu organ satu ceiling, tiada tool melintasi ceiling |
| **A2 Capability** | Apakah benda ini? | Dedupe: 6 lane web-search → 1 kanonik; 3 reader → 1; 3× minimax → 1 + 1 media; 3 wiring context7 → 1; 5 memory/vector → 1 kanonik + graphiti khusus knowledge-graph; 4 DB surface → postgres-pro read-only default. Bunuh lain melalui `deprecation-registry.json` (sedia ada) dengan pointer pengganti. Undang-undang: I2 (satu kebolehan, satu lane) + I9 (dedupe/prune) |
| **A3 Attention** | Berapa banyak yang sesi nampak? | Cap sedia ada: **"<15 hot tools per lane"** (`attention-init-boundary.md` §3) + Attention Governor (session-sticky, fail-open) + `mcp-compress.sh` discover-then-invoke untuk permukaan besar (forge 122 → discover-then-invoke). "Wire MCP by JOB, not by default" (AGENTS.md:247). Harnesses-as-views (pointers.md:105) **dilanjutkan dari skills ke MCP**: setiap harness muat irisan tugasnya, bukan kesatuan |
| **A4 Transport** | Di mana pintu? | A = door awam (satu alias per organ, pola `<organ>.arif-fazil.com/mcp`) · C = mesh/loopback · EXT = SaaS · PROC = stdio. Baiki: frame vhost 502; buang ghost `aforge.`; selesaikan tiga-arah `arifos`/`arifosmcp`/`mcp` dengan ukuran live sebagai tiebreaker |
| **A5 Consequence** | Siapa ingat kesan? | arifFlow receipts → edge pipeline → metabolic proposal → 888 approve → SOT mutation. **Semua pembentukan semula fleet mengalir melalui pipeline ini** — bukan suntingan ad-hoc. "Agent does not get smarter. Federation gets smarter." (METABOLIC_PLANE.md:75) |

**Ujian orthogonaliti satu baris:** *setiap kebolehan memiliki SATU lane kanonik, SATU paksi ownership, SATU nilai versi — dan setiap permukaan yang memaparkannya adalah VIEW yang dijana, bukan salinan.*

## PART 5 — KEBANGKITAN TERJEMAAH (EMBODIED EMERGENCE) — APA YANG TIDAK BOLEH DILAKUKAN

1. **JANGAN rungkahkan organ ke dalam satu mega-MCP gateway.** Ia kelihatan "kemas" tapi membunuh tiga benda: (a) kepelbagaian W³ tri-witness (saksi perlu bebas), (b) authority ceilings (satu proses tak boleh JUDGE dan REFLECT serentak), (c) metabolism — emergence hidup di **tepi** (musyawarah 333∥555, fed_route, spine arifOS, handoff hermes→arifOS bertipe), bukan di tengah yang gemuk. Organ kecil berpandangan (satu invariant setiap satu: WELL=reflect, GEOX=evidence, CHRON=time, FRAME=evidence-never-verdict) + komposisi di tepi = dari situlah kecerdasan bersama muncul.
2. **JANGAN kongsi database kegelapan antara organ.** Seam = envelope handoff bertipe (`hermes_handoff_package` adalah preseden) — kebolehcergasan setiap organ kekal; jika seam longgar, emergens bertukar kepada kacau-bilau.
3. **Perhatian adalah PRA-SYARAT emergence, bukan trade-off.** Ejen dengan 15 hot tools per lane memutus dengan lebih baik berbanding tenggelam dalam 400. "Route by intent… fewer tools = cleaner attention = better decisions" (`attention-routing.md:36`). Sesi yang mewarisi irisan tugasnya sahaja ialah *embodiment*, bukan kekurangan.
4. **Anti-Bangang pada pelan ini sendiri:** tiada dashboard baharu, tiada protokol baharu, tiada pendaftaran selain MINTING `TOOLS.json` yang sudah direka. Kos sebenar = 1 generator + 1 jalur deploy + P0 fix. Kalau generator tak menghasilkan angka yang kekal sama selepas 2 minggu, ia gagal Ujian Syed.

## PART 6 — PELAN LAKSANA (bertahap, boleh dibalikkan)

| Fasa | Kerja | Membaiki | Anggaran |
|---|---|---|---|
| **P0 buku akaun + nadi** (minggu ini) | (a) deploy WELL 3e2e663 — baiki pipeline deploy, bukan restart sahaja (restart hari ini masih jalan artefak 7a145bf); (b) deploy AAA 3893c4c (kelas sama, baris giliran sama); (c) baiki vhost frame 502; (d) padam angka tangan GEOX (27/7live) & version stamps → render dari live + kernel canon | #1, #2, #3, #6, N1, N2, separuh #4 | 1 sesi forge |
| **P1 MINT** | Generator: probe sekali setiap door (`/mcp tools/list` + `/health` + organ_shas snapshot kernel) → emit `TOOLS.json` + jana semula count box/llms.txt/footer/`CANONICAL_PUBLIC_SURFACE.json`/registry. Sentinel jam (sedia ada) membandingkan view vs live | #4, N4, punca akar semuanya | 1–2 sesi forge |
| **P2 Dedupe kebolehan** | Satu lane kanonik per keluarga kebolehan (A2 di atas), lain ke `deprecation-registry.json` + pointer; tulis resit metabolic supaya FQ nampak penurunan | A2 | 1 sesi + musyawarah (cross-repo) |
| **P3 Harness views** | Setiap harness `mcp.json` = irisan tertapis niat, ≤15 hot + governor ekor panjang (mechanisma §3 sedia ada) | A3 | per-harness, kecil |
| **P4 Forge permukaan** | Sapukan discover-then-invoke (`mcp-compress.sh`) ke door forge 122-tool | N5 | kecil — skrip sedia ada |

**Litar pengesahan (setiap fasa):** kiraan page == live == ledger · `drift:false` merentasi organ_shas · hot tools/lane <15 · FQ (verify/execute) via arifFlow tak jatuh · CHRON boleh pegang ramalan untuk P1–P3.

## PART 7 — BUKTI (lampiran ringkas)

- Door matrix 2026-10-05 23:00 MYT: mcp 200(stateless) · well/geox/wealth/hermes/fed/chron 200+sid · arifos 200(stateless) · forge 200+sid(122 tools) · frame **502** · aaa 405 · aforge NXDOMAIN · a-forge 301
- WELL `:18083/health`: `{"status":"degraded","source_commit":"3e2e663","deployed_commit":"7a145bf","drift":true}`; `.git_commit`=7a145bf; `server.py:1972` `version="v2026.07.24"`
- AAA `:3001/health`: `deployed 2caa6b0 ≠ source 3893c4c, deployment_drift:true, G:0.583 DEGRADED, QDF:0.25`; `:18900/health`: `can_sign:false, sovereign_presence_guard:"UNCONFIGURED", key_loaded:true, pam_module_available:true`
- GEOX: page `27 public MCP tool` · live tools=20, resources=53 · `apps.json version=2026.10.05-regenerated-7live` · git f7574fc (2026-10-05)
- Live counts: hub 8t/40r · arifos 8t/40r · well 10t/30r · fed 7t/0r · wealth 15t/18r · hermes 15t/31r · chron 19t/8r · geox 20t/53r
- Kernel `vps_snapshot.organ_shas` (arif_init SEAL-8ae3ddee): arifos 2097b44 · aforge 08327e2 · aaa 3893c4c · geox f7574fc · wealth e446f92 · well 3e2e663 — **snapshot kernel adalah calon SOT semula jadi untuk versi terpasang**
- Canon: `SIX_CONSTITUTIONAL_LEDGERS.md` (TOOLS.json quarantined) · `ARIF_FLOW_METABOLIC_PLANE.md:39,75` · `attention-init-boundary.md` §3 (<15 hot) · `topology.md:6,48-49,80-96` · `organs.yaml` ceilings · `AAA_TOOL_RIGHTS_POLICY.md` · census 6-harness: kimi 22 / codex 14 / claude ~33 / opencode 23 / gemini 12 / hermes 31 server
