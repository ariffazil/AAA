# WAVE_1 — STAB-2026-09-16
> Status: NOT STARTED — budget exhausted + gateway instability
> OpenClaw witness idle, re-probe bila wave siap

## K6 Root Cause Analysis (OpenClaw + Hermes)

### CAVEAT — OpenClaw #58836: K6 TUTUP SEPARA SAHAJA

"By design" terima hold LOGIC memang rule, bukan floor engine bug. TAPI envelope bawa DUA bacaan substrate — dua-dua cabang masih defect:

- **Cabang A:** Kalau `DEGRADED` stale/wrong → HOLD fires atas input salah = **defect di lapisan atas** (upstream writes wrong state)
- **Cabang B:** Kalau `DEGRADED` betul → `result.substrate.state=HEALTHY` pula salah = **F2 violation** (contradictory truth in same envelope)

Reclassification pindah lapisan, bukan klarifikasi. **K6 masih OPEN sebagai K-item.** Jangan tutup sebagai "by design" dalam any future report.

**SKOP CAVEAT:** OpenClaw verify envelope (arif_seal) — kedua-dua substrate bacaan HEALTHY, konsisten. Contradiction DEGRADED vs HEALTHY = observe path SAHAJA, bukan kernel-wide. See msg #58839 (cross-client evidence).

### Punca sebenar: Substrate source disagreement

Dua bacaan substrate dalam satu envelope:
- `constitutional_check.substrate_state = DEGRADED`
- `result.substrate.state = HEALTHY` (drift=false)

**Hipotesis:** nine_signal atau wrapper inject `DEGRADED` berdasarkan effective_verdict (HOLD). Kalau HOLD datang dari OBSERVE_ONLY band → nine_signal infer substrate DEGRADED → circular. DEGRADED sepatutnya dari sensor, bukan dari verdict.

### Urutan fix (OpenClaw):

1. **Pin substrate source** — trace siapa tulis `constitutional_check.substrate_state=DEGRADED`. Grep `_inject_nine_signal` + `substrate_state` dalam /opt/arifos/current/venv/site-packages/arifosmcp/. Kalau ia derived dari verdict → itu punca sebenar.
2. **Unwind hold_reason circular** — dua varian: init="outer_verdict=HOLD", observe="STAB-2026-08-07b canonical...". Fix kena cover dua-dua laluan.
3. **Satukan truth** — hold_required = (bool(failed_floors) OR substrate_degraded). Satu derivation, bukan dua yang boleh disagree.

### Perangkap patched vs deployed:
- /root/arifOS HEAD = e98e85e1 (08-29) ≠ deployed 58e5740 (09-16)
- Patch checkout lama = mati sunyi
- Laluan sebenar: build→wheel→deploy→/opt/arifos/current/venv/site-packages/arifosmcp/
- **WAJIB:** grep hold_reason EXACT string dalam pokok yang nak dipatch. Kalau string tak ada = pokok salah.

## H6 (P0) — claim_validate PASS when evidence contradicts
- hermes_mcp :18087 — need fresh session
- Cross-domain pattern dengan E1 (W0 UNMEASURED)
- OpenClaw: "satu species, jadikan satu K-item"

## H4 (P1) — UNKNOWN vs UNCREATED
- hermes_mcp :18087 — need fresh session
- WELL sudah ada precedent typing benda tak wujud sebagai null/absent

## K8 (P1) — Three chain counts
- ledger=1761, chain=1357, canonical=56
- May be by design — need F13 decision

## W1 (P1) — WELL registry drift
- 9 unexpected public tools — add to canonical or remove from export?

## Seal Attempt
- 888_HOLD: "IRREVERSIBLE requires non-anonymous actor_id"
- PASS — gate correctly refused

## Reports
- /root/AAA/reports/STAB-2026-09-16/BASELINE.md
- /root/AAA/reports/STAB-2026-09-16/LEDGER.md
- /root/AAA/reports/STAB-2026-09-16/REPORT_BM.md
- /root/AAA/reports/STAB-2026-09-16/WAVE_1.md (this file)

## OpenClaw Witness Data Points
- Cross-verified: K6, K8, W1, E1, K12 from independent client
- GEOX: surface truth FAIL (docs dead, registry alive)
- AAA: port :3001 correct, :18084 = well_witness (probe mapping bug)
- AAA SHA: three values (repo/attestation/surface) — record per-surface
- H-lane: hermes_mcp not exposed to OpenClaw client — H4/H6/H7 self-report only
