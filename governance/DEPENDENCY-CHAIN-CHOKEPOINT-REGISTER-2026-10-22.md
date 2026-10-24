# DEPENDENCY CHAIN MAP — CHOKEPOINT REGISTER (2026-10-22, F13 'go' item #6)

> **Status:** `DRAFT_REGISTER 2026-10-24` — observational register, no ratification claimed. Label added by kimi-code/FI-008 housekeeping (DOCTRINE-STATUS GATE requires a Status line).

Hukum SpankPay: de-sentral satu lapisan tak tolong kalau lapisan atas masih chokepoint.
Setiap lapisan: siapa upstream, apa mode kegagalan, rail kedua di mana.
ANGGAP SETIAP UPSTREAM AKAN HOSTILE SUATU HARI. Semak suku tahunan.

## LAYER MAP (atas = paling hampir manusia, bawah = paling asas)

| Lapisan | Komponen | Upstream | Mode kegagalan | Rail kedua |
|---|---|---|---|---|
| Delivery | Telegram ASI_arifos_bot | Telegram DC + ISP + fon F13 | Bot ban, DC outage, handset mati | FORGE_BOT_TOKEN (bot kedua); userbot listener silent; email Brevo |
| Model brains | litellm-federation → deepseek-flash | Qwen token-plan key, provider chain | Quota habis (BUKTI 22/10: perplexity+mmx), 402, vendor TOS | fed chain order=1..n; Venice/Spicy seat (BELUM, tunggu key F13); rollover = revalidate |
| Vision/ASR | vision lanes + GLM-ASR | token-plan wallet sama | 429/1113 quota | kvm8-media-lane-fallbacks (MMS CTC witness, dll) |
| Voice | sado (MiniMax via mmx) | api.minimax.io + /root/.mmx/config.json | credit habis (BUKTI 20/10+22/10), base_url 404 | Qwen token-plan TTS; clause-split retry fail-closed |
| Media gen | mmx image/video | MiniMax + Qwen Token Plan | usage limit (BUKTI 22/10) | qwencloud-image lane; comfyui lokal |
| MCP surface | hermes_mcp :18087 | /usr/bin/python3.13 | import rot, port lock | stdio entry server.py |
| Organs | geox :8081, wealth, well, arifflow :7075 | systemd units | crash-loop, venv rot (BUKTI: geox WAL fix 22/10) | systemd restart + mesh-hosts drop-ins |
| Kernel | arifos :8088 | /opt/arifos/current deploy | /health non-deterministik (scar tercatat) | floor_truth() probe; jangan percaya self-report |
| Compute | KVM8 host, KVM4 peer | Hetzner/ISP, Tailscale | VPS mati, tailscale derp | KVM4 node terpisah (scope per-node); Honor weak rail |
| Mesh | Tailscale headscale | coord server + DERP | coord mati = LAN-only | direct IP fallback (MAP nodes) |
| DNS/Domain | arif-fazil.com | registrar + Cloudflare + Caddy | DNS lapse, cert expiry | forge-infra-guardian probe; vhosts/*.conf |
| Payment | (tiada rail aktif federation sendiri) | — | — | — |

## HUKUM OPERASI
1. Quota habis bukan kerosakan — keadaan biasa upstream. Lane tanpa fallback setempat = tidak produksi-ready.
2. Self-report upstream (env var, config) bukan bukti wallet hidup — probe bila murah (mmx config trap 20/10).
3. Rail kedua diuji SEBELUM upstream pertama mati, bukan selepas.
4. Entri BELUM = open debt dengan owner jelas (F13 key/kredit), bukan senyap.

## PROBE RECEIPT 22/10
- perplexity 401 quota (free tier rescued) — lapisan model rapuh
- mmx usage limit — lapisan media
- geox WAL no-op FIXED & verified (failure-wal-2026-10-22.jsonl)
- Telegram 2 delivery OK (bot 8410138119)
- browser reachability thisvid/xvideos OK

## DOCTRINE BINDING — FEDERATION_INIT::DEPENDENCY_CHAIN_IDENTITY_SURFACE::v1 (F13, 22/10)

AUTHORITY (bind always): Human sovereign kekal. Capability ≠ Authority. Measurement ≠ Permission. Policy ≠ Reality.

ENAM HAZARD KELAS PERTAMA: dependency-chain blindness · identity-surface confusion · context leakage · missing witness · missing falsifier · authority drift.

HUKUM:
1. SURVIVABILITY > OPTIMIZATION — sebelum build: siapa boleh stop/revoke/bill/deplatform, siapa owner upstream. Namakan chokepoint. Provider ≠ system.
2. IDENTITY > MEMORY — setiap actor wajib owner + authority + scope + boundary. Memory tanpa boundary = leakage. Capability tanpa ownership = drift. Identity = enforcement boundary, bukan label.
3. WITNESS > MUTATION — probe, ukur, verify dulu. Task stale = defect. Task terbukti salah = closure.
4. KIQ > COLLECTION — setiap research mula dengan satu KIQ (soalan yang ubah keputusan). Kumpul tanpa KIQ = entropy.
5. TRACE > OUTPUT — rekod apa dipilih, apa ditolak, kenapa, ketidakpastian, kegagalan, override. Optimize untuk kualiti pembelajaran, bukan kuantiti output.
6. CLAIM COMPARTMENT = BUKTI — lane A tak boleh retrieve lane B sahaja compartment wujud. Policy separation ≠ process ≠ context ≠ authority separation.
7. ANGGAP DAKWAH = HIPOTESIS — summary/report/claim delegasi/naratif jana = hipotesis sehingga diwitness. Tiada data ≠ all-clear. Tiada kontradiksi ≠ verified.
8. FALSIFIER BEBAS — verifier tak kongsi optimization target executor. Model sama + prompt lain + objektif sama ≠ independent (costume verifier, scar-2026-10-01-002).
9. LOOP BELAJAR = ADA PENGGUNAAN — output mesti ubah selection akan datang. Telemetry rekod ≠ learning. Receipt stor ≠ adaptation.
10. LAPOR REALITI, BUKAN HARAPAN — PROVEN / PARTIAL / CLAIMED / UNKNOWN / HOLD. Jangan gabung kategori.

UJIAN PENUTUP: Apa berubah realiti? Apa hasilkan bukti? Apa kurangkan ketidakpastian? Apa masih bergantung pada kepercayaan? Tak dapat jawab = kerja tak siap.

## IDENTITY SURFACE — medan tetap (F13 verdict PARTIAL-PROMOTE, 22/10)

LENSA AUDIT: setiap entri register/ledger operasi wajib bawa dua muka —
DEPENDENCY SURFACE (siapa boleh: hentikan · nyahplatform · batalkan · bilkan · menapis)
IDENTITY SURFACE (siapa: pemilik · pemberi kuasa · pelaksana · saksi — dengan Owner/Authority/Scope/Boundary).
Dua soalan ni menggantikan 50 halaman dokumentasi bila audit kegagalan.

STATUS IDENTITY SURFACE kini (diprobeh 22/10, bukan diandaikan):
- Telegram delivery — Owner: F13 token custody · Authority: F13 sahaja boleh revoke bot · Scope: delivery sahaja, bukan judge · Boundary: bot_notify dah dipadam (userbot silent).
- litellm/model chain — Owner: FED SOT /root/A-FORGE/litellm-config.yaml (Arif pegang) · Authority: key = F13 · Scope: routing, bukan kandungan · Boundary: alias-trap dah scar.
- sado/voice — Owner: mmx config /root/.mmx/config.json · Authority: F13 render order · Scope: private-lane sealed DO-NOT-PUBLISH · Boundary: wallet boleh mati senyap (probe bila murah).
- Kernel/arifOS :8088 — Owner: /root/arifOS (F13) · Authority: 7 verdicts; agent tiada self-seal · Scope: governed verbs · Boundary: /health bukan kebenaran (floor_truth()).
- Site arif-fazil.com — Owner: domain F13 (registrar+CF) · Authority: deploy binary = Arif · Scope: vhosts/*.conf · Boundary: satu agent satu promotion (multi-agent law).
- SELAPUT (enforcement) — BELUM: tiada mekanisme yang GAGALKAN entri register tanpa Identity Surface. Ini governance-by-doctrine, bukan mechanism. Open debt, owner F13 (putus sama ada perlu mechanism atau cukup doctrine).

## UJIAN LENSA — tiga contoh auditor diprobeh (22/10, PROVEN)
Contoh "defect teknikal = defect identiti menyamar", kini disaksi bukan dipetik:
1. WEALTH — wealth.service = MASKED/inactive, tapi capability WEALTH HIDUP sebagai gas-api.service, klci-api.service, wealth MCP. Siapa cakap "WEALTH rosak" tengok nama servis; realiti = nama servis BUKAN organ. Identity surface: repo /root/WEALTH (F13), runtime pecah ikut API kecil, mask = keputusan lama tanpa pointer.
2. FRAME — frame-organ + frame-mcp + kabarkan-health semua active, runtime /opt/frame (venv python3), repo /root/FRAME. Baseline/refresh owner = F13 melalui repo; unit systemd root-run. Lens: tiada defect nama-nama, ada gap dokumentasi owner schema.
3. A-FORGE — drift authority = /root/A-FORGE/litellm-config.yaml (FED SOT); bridge state owner = unit-by-unit systemd. Health mismatch claims mesti ditanya: health SIAPA (self-report vs probe).
KESIMPULAN: lensa Dependency+Identity Surface mengklasifikasikan ketiga-tiga dengan betul pada probe pertama. Consumption pertama TERCIPTA (UNKNOWN -> diukur pada contoh ini sahaja).

STATUS LENSA (F13 verdict, 22/10): IDENTITY SURFACE LENS = PARTIAL-PROMOTED.
PROVEN: lensa boleh mengubah klasifikasi kes hidup (3 kes di atas). PARTIAL: consumption = 1 kali (possible, bukan habit). UNKNOWN: penggunaan berulang oleh agen lain; kesan kadar defect federation. Jangan naikkan status tanpa consumption kedua yang diukur.
