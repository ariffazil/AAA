# FASA A — AUDIT KONTRAK & NAMESPACE FEDERASI

> **Dijana:** FI-003 (Qwen Code, 333-AGI) · 2026-09-25 · arahan F13: "jalankan audit Fasa A now A-Z"
> **Skop:** sensus namespace 000–999 + sensus skema kontrak merentas organ (namespace, authority, execution, temporal, attention, witness, capability surface, ownership). **Read-only sepenuhnya — sifar mutasi.**
> **Luar skop (dinyatakan):** probe health endpoint live, audit kod dalaman organ, keputusan design. Laporan ini adalah *bahan JUDGE*, bukan verdict.
> **Epistemik:** setiap dapatan dilabel CONFIRMED (probe sesi ini, resit fail) / DERIVED (rumusan daripada CONFIRMED) / CADANGAN (perlu kuasa 888/F13).
> **Kunci audit (dari distil F13):** *No observational surface may certify its own completeness.* Setiap seksyen menyatakan apa yang ia TIDAK nampak.

---

## A. Kaedah

- Model empat-keadaan kebolehcapaian digunakan untuk semua dakwaan keupayaan: `DECLARED → EXPORTED → REACHABLE → OBSERVED`. Ketiadaan pada satu permukaan ≠ ketiadaan sistem (resit: CHRON — pagi 2026-09-25).
- Kiraan hanya selepas identiti: `NAME → IDENTIFY → DEDUPE → CLASSIFY → COUNT → INTERPRET → CLAIM` (resit: eksport registry MCP v1→v2, hari yang sama).
- Probe: bacaan fail langsung `/root/arifOS`, `/root/A-FORGE`, `/root/AAA`, `/root/chron`, `/root/FRAME` + konteks permukaan MCP sesi ini. Tiada mutasi. Tiada probe health (luar skop).

## B. Sensus namespace 000–999 — EMPAT peta bertindih, DUA diratifikasi bercanggah

CONFIRMED (fail dibaca, baris dirujuk):

| Sumber | Status ratifikasi | 333 | 555 | 666 | 777 | 888 | 999 |
|---|---|---|---|---|---|---|---|
| `arifOS/kernel-sot.yaml` (§resolutions.stage_numbering, L59-63) | **F13 RATIFIED 2026-07-31** | think | **memory** | **judge** ("888=COMPOSE retired") | forge | (retired) | seal |
| `AAA/instructions/apex-zen-alignment.md` (L15) | **F13_RATIFIED 2026-09-16** | BUILD | **VERIFY** | — | — | **JUDGE** | — (SEAL=F13) |
| Linkgraph dalam `AGENTS.md` (rendered, SCAR-2026-09-23-002) | rendered sahaja — **tiada fragment tuan** (glob `**/*linkgraph*` di /root/AAA: 0 fail) | DEVELOP | PRODUCTION/DECIDE | DEPLOY | DEPLOY | ENHANCEMENT/**ABANDON** | **ABANDON** |
| Kernel resources (`trinity.py` L50, `loop_engineering.py` L64, `agent_geometry.py` L30) | dalaman kernel | metabolize | memory layers | critique/ASI | — | "canonical for 666/**888**/999" (residu) | — |

**Dapatan B-1 (CONFIRMED):** `kernel-sot.yaml` dan `apex-zen-alignment.md` kedua-duanya diratifikasi F13 dan **bercanggah terus**: JUDGE=666 (2026-07-31, "888=COMPOSE retired") vs JUDGE=888 (2026-09-16). Tiada dokumen damai antara mereka.
**Dapatan B-2 (CONFIRMED):** 555 = MEMORY (kernel SOT, arif_memory=`KERNEL 555`) vs VERIFY=555 (APEX-ZEN) vs PRODUCTION/DECIDE (linkgraph).
**Dapatan B-3 (CONFIRMED):** 999 = SEAL (kernel, `arif_seal=KERNEL 999`) vs ABANDON (linkgraph). Agen baru yang membaca AGENTS.md sahaja akan warisi dua makna untuk nombor yang sama — risiko `semantic_authority_gap`.
**Dapatan B-4 (CONFIRMED):** `agent_geometry.py` masih merujuk 888 sebagai "canonical" walaupun kernel-sot.yaml telah bersara 888 — residu dalaman.
**Dapatan B-5 (DERIVED):** lifecycle kernel (`kernel-sot.yaml` §lifecycle: INIT→OBSERVE→THINK→JUDGE→ACT→SEAL) TIDAK menggunakan nombor langsung — ini asas damai yang paling bersih: nombor adalah *label ABI*, lifecycle adalah *state machine*. Cadangan damai di §K.

## C. Kontrak authority (kernel + ACT)

CONFIRMED:
- Tuple 10-medan wujud & diratifikasi: `⟨Actor, Session, Host, Objective, Operation, Scope, Target, Issuer, Expiry, ExpectedPostcondition⟩` (`AAA/instructions/authority-envelope.md` L24-26) + complete-mediation trinity + TOCTOU `TargetHash` + EnforcementCoverage metrics (L57-60) + witness tuple (L67-69).
- ACT mint (`A-FORGE/governance/canonical_actor_binding_schema.md` L54-77): 11 authority bands, mutation gate ⊇ EXECUTE_REVERSIBLE, seal gate ⊇ MUTATE, `idempotency_key` wajib, `expires_at` dipulangkan kernel.

JURANG:
- **C-1 (CONFIRMED):** tiada medan `Budget` dalam tuple ATAU dalam ACT mint payload — kuota per-envelope tiada wakil kontrak.
- **C-2 (CONFIRMED):** tiada medan `RevocationRef` — pembatalan tiada rujukan kontrak dalam envelope (Expiry bukan revocation; revocation yang tak propagate = bukan revocation).
- **C-3 (CONFIRMED):** EnforcementCoverage/PreventedUnauthorizedRate/UnauthorizedEscapeRate **definisikan metrik tapi tiada instrument berterusan** yang mengukurnya (grep A-FORGE: tiada UNKNOWN_OUTCOME; tiada coverage meter).
- **C-4 (CONFIRMED):** `canonical_actor_binding_schema.md` menunjukkan arif_init boleh memulangkan `MUTATE` kepada mana-mana canonical actor melalui Ed25519 — kapasiti ini sah; tapi tiada kaitan eksplisit dalam schema antara band yang diminta dan *objective/task* tertentu (Objective dalam tuple wujud dalam fragment, tidak nampak dalam medan mint).

## D. Kontrak execution (A-FORGE)

CONFIRMED:
- Idempotency separa: `idempotency_key` (ACT mint), receipt-hash idempotent (test WAJIB #37, `tests/adversarial/test_attack_vectors.py` L116-131), kabarkan `ON CONFLICT DO NOTHING` (`kabarkan/worker.py` L126).
- organs.yaml: A-FORGE `authority_ceiling: EXECUTE_AFTER_SEAL`, 124 API tools / 52 MCP stateless.

JURANG:
- **D-1 (CONFIRMED):** status `UNKNOWN_OUTCOME` TIADA dalam repo (grep: 0 match) — timeout tidak dibezakan daripada kegagalan dalam state machine. Cadangan blueprint (timeout ≠ gagal; reconcile-before-retry) tiada wakil kod.
- **D-2 (DERIVED):** idempotency sedia ada adalah per-substrat (mint, receipt, observability) — bukan kontrak universal actuator. Tiada jaminan "sekali sahaja" merentas retry.
- **D-3 (CADANGAN):** default long-run actuator perlu checkpoint+resumable+label-jurang (template terbukti hari ini: registry walker 84k+ rekod, `walkComplete:false`, resume dari cursor, sifar kehilangan data).

## E. Kontrak temporal (CHRON)

CONFIRMED:
- Lifecycle kod: `CREATED → ACTIVE → VERIFIED_CORRECT | VERIFIED_INCORRECT | EXPIRED_UNVERIFIED` (`chron/chron_prediction.py` L8-10). Medan: claim, expected_outcome, confidence, verify_at, assumptions, source, source_id, principal, horizon.
- organs.yaml: CHRON COMPUTE_ONLY, port 18102, mcp_tools senarai 8 — **tiada chron_create_event / chron_record_verification** dalam SOT, tapi kedua-duanya diiklankan pada permukaan MCP langsung sesi ini → SOT-vs-surface drift.

JURANG (digabung dengan audit pagi):
- **E-1 (CONFIRMED):** tiada status `DUE` / `AWAITING_EVIDENCE` — due-for-review vs resolved tidak dibezakan ("tiba masa ≠ terbukti" tiada wakil enum).
- **E-2 (CONFIRMED, audit pagi):** kecacatan kontrak konkrit dalam rekod aktif: verify_at lebih awal daripada ketersediaan bukti (bil Jan-2027 disemak 31-Dis-2026); ambang `> 4500` (claim) vs `>= 4500` (expected) bercanggah pada tepat 4500; `horizon: "5s"` = lima sesi dagangan, boleh dibaca lima saat.
- **E-3 (CONFIRMED):** 0/21 ramalan aktif ada `verifier_command`; 15/21 ada falsifier; 13/21 ada verifier_method — kontrak penyelesaian tidak seragam (verifier sah ≠ command sahaja).
- **E-4 (CONFIRMED):** kalibrasi: 3 sampel pemerhatian sebenar (4 termasuk sintetik) — terlalu kecil untuk dakwaan dipercayai/tidak.
- **E-5 (CONFIRMED):** SOT organs.yaml (8 tools) ≠ permukaan hidup (≥10 tools termasuk create/record/reconcile/proxy_reality) — kemas kini SOT perlu (milik AAA registry).

## F. Kontrak attention (AAA)

CONFIRMED:
- `attention_formula: P = (Impact × Urgency × EvidenceQuality × Novelty) / AttentionCost`, `EvidenceQuality = (1 - Uncertainty) × Reversibility` (`AAA/README.md` L18-20).
- Double-count reversibility: `hard_overrides: irreversibility_floor: P ≥ 0.85` (L24-28) — satu pembolehubah dikira di DUA tempat dengan dua mekanisma (pengganda + floor).
- Projection doctrine SUDAH canon: `README_state = projection(registry_state)`, `counts_are_live` (L45-48).

JURANG:
- **F-1 (CONFIRMED):** reversibility adalah *risiko tindakan*, bukan *kualiti bukti* — bukti kuat untuk tindakan tak boleh balik mesti kekal boleh dibezakan daripada bukti kuat untuk tindakan boleh balik. Cadangan: `EvidenceQuality = (1-Uncertainty)` sahaja; Reversibility keluar sebagai ActionRisk gate berasingan.
- **F-2 (DERIVED):** AAA identity `(evidence, state, deadlines, drift, uncertainty) → AttentionPacket` belum menetapkan bahawa capability adalah ciri pasangan (organ, laluan) — resit CHRON pagi menunjukkan permukaan berbeza mengiklankan subset berbeza.

## G. Kontrak witness & evidence

CONFIRMED:
- Witness tuple 6-medan + syarat CLOSE (`ObservedState ⊨ ExpectedPostcondition`) + three independences (epistemic/authority/observational) dalam `authority-envelope.md` L67-69.
- "52k-receipts-with-null-trace_id defect" didokumen dalam fragment — causal fabric (ObjectiveID+TraceID+StateTransition+ActorIdentity) adalah penawar yang ditetapkan; instrumentasi berterusan tidak ditemui dalam probe ini.

JURANG:
- **G-1 (DERIVED):** empat-keadaan `DECLARED → EXPORTED → REACHABLE → OBSERVED` belum dienkwarkan dalam schema mana-mana organ — ia hidup sebagai disiplin audit, bukan medan kontrak. Cadangan: setiap capability claim membawa `surface` + `state` medan.
- **G-2 (CADANGAN):** kunci "No observational surface may certify its own completeness" patut menjadi invariant ujian (setiap snapshot/census membawa medan `coverage` + `cursor`/`excluded`).

## H. Permukaan keupayaan (capability surface)

CONFIRMED (resit dari konteks sesi + fail):
- CHRON: permukaan MCP langsung mengiklankan `chron_create_event`, `chron_record_verification`, `chron_reconcile_state`, `chron_proxy_reality_*` — SOT organs.yaml senaraikan 8 tools sahaja (E-5). Laluan connector A-FORGE pula mengiklankan subset (audit pagi).
- A-FORGE: 52 MCP stateless tools (SOT) + 124 API (SOT); SOT vs live perlu re-probe berjadual (luar skop hari ini).
- Registry luar (pelajaran hari yang sama): kiraan tanpa dedupe menghasilkan leaderboard palsu — 25 "server" = 25 version-record satu server; ai.* hanya 10% syarikat sebenar, bukan "noise floor" seperti dakwaan slice.

## I. Ownership & higiene registry

CONFIRMED:
- `organs.yaml` = machine SOT (904 baris, 37 komponen, `truth_rule: live_health_beats_file`, port_observability direkod, tombstone `non_components` termasuk i-arif lama).
- `deprecation-registry.json` HIDUP dan dipantau: v2026.09.20, audit terakhir 2026-09-24 oleh FI-003, 16 services + 19 skills + 8 tools + 14 files + 2 endpoints ditombstoned, 14 open divergences, alias_law dengan invariant `Canonical(x) => DiscoverableExactlyOnce(x)`.
- `AAA/registry/mcp-servers.yaml` (dari audit 2026-09-10) wujud sebagai registry MCP dalaman.

JURANG:
- **I-1 (CONFIRMED):** linkgraph 000–999 tiada artifact tuan dalam /root/AAA (B-3/B-4) — rendered sahaja. Render adalah *paparan*, bukan *tuan*.
- **I-2 (CONFIRMED):** SOT CHRON tools lapuk berbanding permukaan hidup (E-5).
- **I-3 (DERIVED):** organs.yaml `live_probe` medan adalah snapshot tarikh-baka (2026-07-30 / 2026-09-18) — selari dengan projection doctrine, tapi tiada age-limit yang memaksa re-probe sebelum dakwaan.

## J. Register dapatan (severity · pemilik · next-proof)

| ID | Dapatan | Keterukan | Pemilik semula jadi | Next-proof |
|---|---|---|---|---|
| B-1 | JUDGE=666 vs JUDGE=888 — dua sumber F13-ratified bercanggah | **TINGGI** | F13 (damai) + arifOS | Keputusan damai + kemaskini fragment/SOT |
| B-3 | 999=SEAL vs 999=ABANDON; linkgraph tiada tuan | TINGGI | AAA instructions | Fragment linkgraph + prefix namespaced |
| C-1/C-2 | Tiada Budget/RevocationRef dalam tuple+ACT | SEDANG | arifOS + A-FORGE schema | Kemaskini schema + ujian mint |
| C-3 | Metrik EnforcementCoverage tak berinstrument | SEDANG | A-FORGE | Meter + laporan berkala |
| D-1 | UNKNOWN_OUTCOME tiada | SEDANG | A-FORGE | Ujian timeout→UNKNOWN→reconcile→resolve-sekali |
| E-1/E-2 | Enum CHRON tiada DUE/AWAITING_EVIDENCE; ambang/unit/tarikh cacat | SEDANG | CHRON owner | Betulkan rekod aktif (sejarah dipelihara) |
| E-5/I-2 | SOT CHRON ≠ permukaan hidup | RENDAH | AAA registry | Kemas kini organs.yaml |
| F-1 | Reversibility double-count dalam formula AAA | SEDANG | AAA | Refaktor formula + ujian regression |
| G-1 | 4-keadaan belum dienkwarkan | RENDAH | AAA/schema | Medan surface+state dalam capability claim |
| I-3 | Snapshot SOT tanpa age-limit | RENDAH | AAA | Dasar re-probe sebelum dakwaan |

## K. Permintaan keputusan (untuk 888 JUDGE / F13)

1. **Namespace damai:** adopsi prefix namespaced (`kernel:666=judge`, `az:888=judge-lane`, `lg:999=abandon`) ATAU penyatuan penuh ke satu peta. Kernel-sot.yaml not "888=COMPOSE retired" vs apex-zen "JUDGE=888" perlu satu fatwa.
2. **Tuple tambahan:** lulus/tolak `Budget` + `RevocationRef` sebagai medan wajib envelope ACT baharu.
3. **UNKNOWN_OUTCOME:** adopsi sebagai status kelas pertama A-FORGE execution state machine.
4. **CHRON contract:** lulus status `DUE`/`AWAITING_EVIDENCE` + pemeriksaan verify_at≥bukti tersedia + normalisasi ambang/unit (pindaan sejarah dipelihara, invariant #11).
5. **AAA formula:** pisah Reversibility daripada EvidenceQuality.
6. **Linkgraph fragment:** wujudkan `AAA/instructions/reality-linkgraph.md` dengan namespace tersendiri; AGENTS.md kekal renderer, bukan tuan.

## L. Kriteria masuk Fasa B

Fasa B ("satu tugas lengkap terbukti" merentas propose→authority→act→witness→consequence) BOLEH bermula serentak dengan keputusan K1-K6, TETAPI laporan Fasa B mesti merujuk keputusan tersebut — jika tidak, tugas lengkap pertama akan membekukan kontrak yang masih dipertikaikan.

---

### Lampiran — resit probe utama

- `/root/arifOS/kernel-sot.yaml` L59-63 (stage_numbering; judge: 666; 888 retired), §lifecycle (INIT→OBSERVE→THINK→JUDGE→ACT→SEAL), §capabilities (arif_init=000 … arif_memory=555).
- `/root/AAA/instructions/apex-zen-alignment.md` L15 (BUILD=333 · VERIFY=555 · JUDGE=888 · SEAL=F13).
- `/root/AAA/instructions/authority-envelope.md` (tuple L24-26; coverage L57-60; witness L67-69; TOCTOU; 4 planes).
- `/root/A-FORGE/governance/canonical_actor_binding_schema.md` (ACT fields L54-77; bands L23-27).
- `/root/chron/chron_prediction.py` L8-10 (lifecycle), L86-95 (fields), `_emit_ariflow_predict` (bridge :7073).
- `/root/AAA/federation/organs.yaml` L27-120 (arifos/a-forge/aaa), L435-480 (chron, 8 tools, port 18102), L771-895 (port_observability; non_components tombstones).
- `/root/AAA/docs/deprecation-registry.json` (v2026.09.20, 16+19+8+14+2, 14 open divergences).
- Grep: `UNKNOWN_OUTCOME` di /root/A-FORGE = 0 match; `idempot` = 63 match (mint/receipt/kabarkan); `**/*linkgraph*` di /root/AAA = 0 fail.
- Sesi ini: permukaan MCP CHRON langsung mengiklankan chron_create_event/chron_record_verification/chron_reconcile_state/chron_proxy_reality_*.

*Laporan ini read-only; ia tidak mengubah mana-mana organ. DITEMPA BUKAN DIBERI ⚒️*
