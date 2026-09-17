# REPORT_BM — STAB-2026-09-16
> 2026-09-16 · Two-client cross-verified (Hermes + OpenClaw) · 7 organ all healthy

---

## 1. APA YANG MASIH ROSAK

**K6 (P0) — HOLD tanpa floor failure (by design, bukan bug kode)**
entropy_dS mode fire HOLD dengan hold_required=true tapi failed_floors=[]. Lepas baca code: HOLD berpunca dari substrate DEGRADED (session anonymous → OBSERVE_ONLY → nine_signal inject DEGRADED). `failed_floors=[]` honest — memang takde floor yang diuji. hold_reason circular ("effective_verdict=HOLD failed_floors=[]"). **Verdict: working as designed, tapi hold_reason perlu lebih jelas** — patut tulis "substrate_degraded" atau "identity_not_bound", bukan circular reference.

**K8 (P1) — Tiga chain counts tak match**
ledger_size=1761, chain_length=1357, canonical_entries=56. Cross-verified dua client. 959 unlinked seal entries. Integrity GAPS_FOUND. **Tak fixable dari stabilization run** — perlu understand design intent (apa perbezaan ketiga counts ini?). Belum pasti ini bug atau by design (ledger = semua entries, chain = linked entries, canonical = verified entries).

**W1 (P1) — WELL registry drift**
intended=10, exported=19, 9 unexpected public tools. verdict=REGISTRY_DRIFT. Tools exported tapi tak dalam canonical list. **Perlu decide**: tambah 9 ke canonical atau remove dari export?

**E1 (P2) — W0 UNMEASURED on meta call**
capital_registry mode=status (zero-arg) fire W0 UNMEASURED dua kali. Meta/introspection tools patut exempt dari coverage gate.

**H4 (P1, self-report) — UNKNOWN vs UNCREATED**
"Adakah Syed akan setuju?" → epistemic_state=UNKNOWN. Patut UNCREATED (keputusan tak wujud lagi). NOTA: WELL sudah ada precedent typing benda tak wujud sebagai null/absent.

**H6 (P0, self-report) — PASS when evidence contradicts**
Claim "delta_S=0.42" + evidence "delta_S=0.0 + no computation" → verdict=PASS. Epistemic integrity failure. Cross-domain pattern dengan E1 — verdict terpisah dari evidence.

**AAA SHA divergence** (new — OpenClaw)
Tiga nilai beredar: repo checkout (9cc4129), attestation (188971b), surface (tak confirmed). Rekod per-surface patut jadi standard.

**AAA port probe bug** (new — OpenClaw)
well_triad map aaa↔:18084 tapi :18084 ialah well_witness. AAA sebenarnya :3001. Probe mapping bug dalam WELL.

---

## 2. APA YANG PERLU KEPUTUSAN ARIF

1. **K6**: hold_reason circular — nak tambah specific reason strings ("substrate_degraded", "identity_not_bound") ke hold_reason template? (A: fix hold_reason template / B: by design, biarkan)

2. **K8**: Tiga chain counts — ini bug atau design? Apa patut jadi source of truth: ledger_size, chain_length, atau canonical_entries? (A: canon=canonical_entries, fix ledger/chain display / B: explain three-count design / C: hold, fahami dulu)

3. **W1**: 9 unexpected public tools — tambah ke canonical atau remove dari export? (A: tambah 9 ke canonical_callable / B: remove dari exported_surface / C: hold)

4. **H6+E1 cross-domain**: Satu fix untuk both (evidence→verdict binding), atau separate patches? (A: satu unified verdict-evidence validator / B: fix domain-by-domain)

5. **AAA SHA**: Rekod tiga medan standard (repo/deployed/registry)? (A: yes, update BASELINE format / B: biarkan)

---

## 3. APA YANG DAH BETUL

| ID | Sebelum | Selepas (cross-verified) | Status |
|---|---|---|---|
| K1 | actor_id rewritten | Canonicalized at init (by design) | NOT-REPRODUCED |
| K2 | verified flips | state_version=1 stable | NOT-REPRODUCED |
| K3 | int epoch | ISO string consistent | NOT-REPRODUCED |
| K5 | mutation=true on read | affordance_contract mutation=false | NOT-REPRODUCED |
| K9 | DEPLOYMENT_DRIFT | drift=false, built==deployed | NOT-REPRODUCED |
| K11 | /999 stale | last_seal fresh, head_seq=39 | NOT-REPRODUCED |
| K12 | no delta_S | delta_S=0.0 emitted | NOT-REPRODUCED |
| K10 | schema rejected | Tak sempat uji | UNMEASURED |
| K7 | null id entries | session_id null, id OK | NOT-REPRODUCED (as described) |
| H3 | "didn't reply" template | Clean — 5 alternatives | NOT-REPRODUCED |
| H5 | kernel typed PERSON | Correctly SYSTEM | NOT-REPRODUCED |
| 7 organ | health | 200 across all | STABLE |
| arif_init | — | session bound, drift=false | STABLE |
| seal | — | canonical chain verified | STABLE |
| WEALTH | — | 12/12 registry PASS | STABLE |

---

## 4. APA YANG SAYA TAK UJI

- **F1 (A-FORGE gate)**: hermes gate truncation 500→4000, wealth SCT permission — A-FORGE MCP unreachable dari OpenClaw, Hermes budget habis
- **K10**: arif_forge schema params — belum diuji dengan runtime call
- **G1 (GEOX)**: public_count vs target — GEOX surface truth FAIL dari OpenClaw (docs kosong, registry hidup), tapi G1 spesifik tak diuji langsung
- **H7 (authorship misattribution)**: paste unlabeled text — belum diuji
- **K4 (FULL→LIMITED no event)**: takde bukti observasi
- **Deploy/verify cycle**: Tiada fix yang benar-benar deployed dan re-probed

---

## 5. RISIKO BARU

1. **Gateway instability**: Multiple shutdowns during run. 6+ restarts. Wave execution terganggu.
2. **Budget habis**: work_contract max 20 tool calls dah exceeded. Fresh session needed for code fixes.
3. **Self-report gap**: H4, H6, H7 hanya self-report — OpenClaw tak boleh verify hermes_mcp dari client lain. Before/after diff wajib untuk claim status.
4. **GEOX docs dead**: OpenClaw find — surface kosong walaupun registry hidup. Bukan dalam triage asal.
5. **WELL probe mapping**: well_triad salah map aaa↔:18084. Bukan dalam triage asal.

---

## RINGKASAN UNTUK ARIF

**7 organ sihat.** Tiada organ jatuh merah selepas session ni.

**5 item confirmed dari dua client:** K6 (by design, hold_reason circular), K8 (chain counts), W1 (registry drift), E1 (UNMEASURED meta), K12 (NOT-REPRODUCED).

**2 item self-report sahaja:** H4 (UNKNOWN vs UNCREATED), H6 (PASS walaupun contradicted). H6 ialah yang paling bahaya — epistemic integrity failure.

**Tiada fix deployed hari ini.** Budget + gateway habis. Wave 1 perlu fresh session.

**Keputusan Arif:** review 5 soalan dalam §2, lepas tu buka session baru untuk Wave 1 fixes.
