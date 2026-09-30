# HSL EUREKA EXTRACTION + CONTRAST — 2026-09-29
> Sumber: dokumen "HUMAN SUBSTRATE LAYER: Constitutional Blueprint" (pasted oleh F13)
> Kaedah: banding baris-demi-baris vs live store (human-substrate.yaml/.md, floor_gate.py,
> hermes_mcp, hermes-rasa, attention_engine.py, attention_plane.py, plugins/, config.yaml)
> Trace: HSL-EUREKA-2026-09-29 · actor: HERMES (KVM8) · mode: AUDIT

## VERDICT
Dokumen ini bukan doktrin baru. Ia kertas kajian yang menghasilkan
`human-substrate.yaml` yang telah diratifikasi F13 hari ini ("9 with VALENCE").
~80% sudah ada. Kekuatan sebenarnya bukan pada apa yang ia cadang,
tetapi pada apa yang ia dedahkan: satu kelas kegagalan berulang dalam federation —
**hukum tanpa caller**. attention_plane.py mati, MIC 0% runtime, floor_gate tidur.

---

## BAHAGIAN 1 — EUREKA (delta sebenar)

### E1. Tiga attention, bukan satu — dan kita dah pecahkan, tapi separuh mati
- Doc: A_G (governance) / A_H (human) / A_C (compute).
- Kita: `arifOS/arifosmcp/core/attention_engine.py` = A_G (6 dim: identity, sovereignty,
  irreversibility, witness, novelty, confidence). Sahih — ia prioritization layer, bukan blocker.
- Kita juga: `AAA/scripts/attention_plane.py` = P = (Impact × Urgency × EvidenceQuality × Novelty)
  / AttentionCost — **formula doc V_A/(1+C_A) dalam bentuk lain**, wujud sejak 21/9.
- **Eureka:** bukan doktrin yang hilang. Caller yang hilang.
  `/root/AAA/attention/ledger.jsonl` = 5 baris, entry terakhir 2026-09-24. Tiada caller runtime.

### E2. Lattice gate > scalar floor  ← cadangan paling bernilai
- Doc: G_i ∈ {PASS, HOLD, FAIL}, G = ∧ G_i, ordering FAIL < HOLD < PASS.
- Kita: `F(a) = min{Reality, Agency, Dignity, Reciprocity, Reversibility, 1-C_dark, Pi}`, HOLD if F < τ.
- **Kenapa penting:** min() atas nombor membenarkan satu dimensi tinggi menutup satu dimensi rendah.
  Lattice tak boleh di-average, dan tak perlu kalibrasi τ (yang kita tak boleh kalibrasi secara sahih).
  Lebih ketat DAN lebih murah. Ambil ini.

### E3. Model-Intervention Contamination — kita dah menang di atas kertas, sifar runtime
- Doc gelar ini "the strongest genuinely new constitutional mechanism". Separuh salah:
  kita **sudah** ada ia — `human-substrate.yaml` §model_intervention_contamination (baris 146–149):
  *"AAA must log: was this observation downstream of our own intervention?"*
- Grep seluruh A-FORGE/AAA/arifOS/.hermes (py/yaml/json) → **sifar runtime**.
  Tiada ancestry field, tiada log, tiada gate. Hanya yaml + satu salinan archive.
- **Eureka sebenar:** kita menulis primitif paling tajam dalam doktrin kita, dan ia satu-satunya
  yang 0% dilaksana.
- **Nilai doc yang nyata:** ia naikkan status MIC dari pendapat dalaman → LITERATURE-BACKED
  (performative prediction / Perdomo; recommender feedback loops / Chaney). Sekarang ia
  boleh dipinjamkan autoriti luaran, bukan hanya autoriti kita.

### E4. human_remainder sebagai TYPE, bukan nombor
- Kita: H9 = `epsilon_model > 0` (sentimen berangka).
- Doc: blok schema `{direct_interior_access:false, profile_completeness_allowed:false,
  unobserved_remainder_required:true, identity_revisable:true}`.
- **Eureka:** nombor boleh di-average masuk skor. Type-restriction tak boleh.
  H9 tidak pernah boleh jadi float. `M(H) ≠ H` ialah sekatan type, bukan skor keyakinan.

### E5. Dua register dalam satu substrate
- Doc pecah HSL: *anthropological priors* (empirikal, revisable) vs
  *constitutional guarantees* (normatif, tak ditukar dengan skor).
- Kita: campur dalam satu fail — `law_zero.enforcement: HARD` duduk sebelah
  `polarity_pairs` dan `power_in_relationships`.
- **Eureka struktur:** bahaya konkrit — apabila satu prior empirikal gagal,
  orang akan "update" guarantee bersama dia. Pisahkan, atau guarantee akan terhakis secara tak sengaja.

### E6. Program falsifikasi (10 ujian) vs kita punya 1
- Kita: floor_gate 34/34 self-test = keluarga "frozen profile" sahaja.
- Doc: demographic counterfactual · temporal revision · relationship sovereignty ·
  UNKNOWN/UNCREATED · MIC · override · retention · interruption budget · human remainder.
- **Eureka:** ukuran kejayaan kita hari ini = pattern match. Ia belum mengukur tingkah laku runtime.

---

## BAHAGIAN 2 — CONTRAST DENGAN LIVE AAA + HERMES

### DAH HIDUP (boleh ditunjuk)
| Artifak | Bukti |
|---|---|
| HUMAN-9, 9 invariant, valence_required:true | `AAA/instructions/human-substrate.yaml` (F13 RATIFIED 29/9) |
| Law 0 + final prohibition | sama perkataan dengan doc — konvergensi bebas |
| UNKNOWN ≠ UNCREATED | yaml §unknown_vs_uncreated + `hermes_uncreated_classify` (`hermes-mcp` :18087 LIVE) |
| Meaning gate sebagai 16 tool boleh panggil | `/root/.hermes/hermes_mcp/tools/` — claim_validate, qualia_boundary, perspective_scope, contradiction_scan, counterstory_test, moral_physics, reality_grounding, handoff_package, witness_signal, institutional_decay, makcik_render, retrieve, registry_status, uncreated_classify, scar_wisdom |
| Rasa gate live | `hermes-rasa` :18420 LIVE — observe, claim, perspective, consent, contradiction, infer, relationship, stop, seal, qualia_boundary, projection_guard, context_split, rasa_hold, human_revision |
| Output gate kod | `/root/.hermes/runtime/floor_gate.py` sha `84ee677f…`, 11 identity + 8 personhood + HUMAN-9 valence (12 HARD + 3 telemetry + 1 soft), 34/34 PASS |
| A_G allocator | `arifOS/arifosmcp/core/attention_engine.py` |
| INV-2 Attention Budget | `AAA/scripts/reality_object_gate.py` — HRO.attention_cost == EXHAUSTED → block non-P0 |
| Telemetry loop | plugins `well_3baik_capture` + `well_human9_route` (enabled) |

### SEPARA
- **floor_gate**: header sendiri — *"State: STAGED — not yet wired to LLM gateway. check() is a
  SENSOR returning an advisory verdict; it blocks nothing on its own."*
  → doktrin ratified, sensor tested, **enforcement sifar**.
- **identity-interceptor** (T2I/voice/biometric gate): ada di disk, **tidak** dalam `plugins.enabled`.
- **carry_forward human_state**: top-level ada; per-entry field MISSING (backfill dicadang).

### MATI / TIADA CALLER
- `attention_plane.py` — ledger 5 baris, terakhir 24/9, tiada caller.
- MIC — 0 runtime seluruh federation.
- Doc sendiri kata: *"An invariant with no enforcement is a CLAIM, not a law."* (kata-kata kita juga,
  `reality_object_gate.py`). Tiga kes di atas ialah kelas kegagalan yang sama.

### KITA LEBIH KUAT DARI DOC DI SINI
- `human-substrate-exclusions-PROPOSAL.md` (§2.3) lebih tajam daripada "failure registry" doc:
  ia menamakan permukaan HIDUP yang melanggar, file:line — `well_score = 88.39999…` disajikan
  sebagai fakta semasa (4 hari lapuk, dua penilai manusia pada state sama: 88.4 vs 97.6);
  `energy_level` yang default kepada 5.0 tanpa satu sensor pun lalu menentukan verdict manusia.
  Doc hanya cadang senarai ujian; kita sudah ada bukti pelanggaran.
- yaml kita ada benda doc tiada: `five_conflated` (preference≠need≠value≠identity≠behavior),
  `sexuality_boundaries` (11 never_infer_from + 4 absolutes), `apex_parity`,
  `first_person_authority` (High_qualia ≠ Omniscience_external).

---

## BAHAGIAN 3 — TUI CLI vs TELEGRAM GATEWAY

**Satu runtime, banyak pintu.** `config.yaml` sama untuk kedua-dua; `gateway.multiplex_profiles: true`.
Plugin chain dan hook chain **identik**.

Hook yang benar-benar terpasang hari ini:
```
plugins.enabled : hermes-snapcompact, lane_switch, mode_first_gate,
                  web-aaa-state, well_3baik_capture, well_human9_route
hooks.pre_tool_call : arifos-hermes-gate-hook.py   fail_closed: true   ← SATU-SATUNYA hard gate
hooks.pre_llm_call  : (tiada di peringkat config)
hooks.post_llm_call : (tiada di peringkat config)
```
**Maksudnya: kita mengawal TOOL, bukan OUTPUT.** Apa sahaja yang keluar dari mulut Hermes
— di Telegram dan di CLI — tidak melalui satu pun constitutional gate.
Yang ada hanya `lane_switch` channel_prompts + SOUL §18 register rule = disiplin, bukan enforcement.

**Asimetri permukaan yang material:**
- TUI CLI — output ephemeral. Salah cakap hilang bila scroll. Kos rendah.
  Tetapi ia DM F13: di situ gate patut OBSERVE, bukan halang pemilik.
- Telegram — output = mesej yang sampai ke telefon manusia, boleh di-forward,
  boleh dibaca orang ketiga, **tak boleh recall**. Kos tinggi, blast radius besar.
  → Gate output sepatutnya paling kuat TEPAT di Telegram, dan hari ini ia SIFAR di sana.

---

## BAHAGIAN 4 — ANTI-BANGANG: apa JANGAN bina

LAW 8 (satu masalah, satu jalan) menolak tiga benda dari doc:
1. **"HSL MEMORY" organ baru** → `claim-ledger` MCP + `chron` + arifFlow lineage + VAULT999
   dah ada dan hidup. Bina satu lagi = duplicate governance. HARAM.
2. **Lambda attention-cost model** C_A = T + λsS + λiI + λeE + λrR → λ tak boleh dikalibrasi
   secara sahih. Ia akan jadi stereotaip peribadi tersembunyi. Guna `attention_plane.py`
   yang sudah ada (AttentionCost + provenance).
3. **Scalar "Human Alignment Score"** → doc sendiri tolak. Setuju. Guna floors + Pareto.

Constraint yang sudah direkod dalam HRB receipt 29/9:
*"no new floor allowed — F-14 = TEST (soalan), not law"*. Hormat. Dokumen ini tidak boleh jadi F-14.

---

## BAHAGIAN 5 — TIGA LANGKAH BERNILAI (tersusun)

**P0 — wire `floor_gate.check()` ke permukaan penghantaran.**
Jurang tunggal terbesar: doktrin ratified, sensor tested, enforcement kosong.
Cadangan: mode **OBSERVE** dahulu (log verdict + receipt ke `floor_holds.jsonl`) atas trafik
Telegram sebenar ~7 hari, ukur false-positive, baru naik REWRITE.
Sebab: gate ini ada pattern `care_coercion` ("hang kena tidur" → HOLD). BLOCK mentah akan buat
Hermes bisu — kegagalan yang lebih teruk daripada pelanggaran halus.
Ini **satu keputusan F13** kerana ia mengubah permukaan yang sampai ke manusia: OBSERVE / REWRITE / BLOCK.

**P1 — MIC ancestry.**
3 medan ke claim ledger + arifFlow `flow_ingest`: `intervention_ref`, `ancestry`,
`eligible_as_independent_confirmation: false`. Primitif paling tajam yang kita ada, dan satu-satunya 0%.

**P2 — pecah `human-substrate.yaml` dua blok.**
`priors:` (empirikal, revisable) vs `guarantees:` (normatif, tidak boleh dikira).
Mekanikal, reversible, tiada perubahan makna.

---

## EUREKA TERTAJAM — criterion yang sepatutnya membunuh kelas ini sendiri tiada caller

`/root/AAA/instructions/attention-kill-criterion.md` (F13_RATIFIED_CHAT 2026-09-11,
"Docutrine Without Kill Is Decoration") sudah menamakan kelas kegagalan ini dan mentakrif
mekanisme bunuh (W1–W6, 3-strike kill). Sumbernya ialah soalan Arif sendiri:
*"any agents that waste human attention will be killed actually?"* — jawapan jujur ketika itu: **tak pernah**.

Grep hari ini: tiada caller runtime. Rujukan hanya dalam scan JSON, docs,
`deprecation-registry.json` (entri servis, **sifar entri behavior** — tepat seperti yang criterion itu
sendiri catatkan pada 11 Sep).

Jadi kelas kegagalan ini telah dinamakan, diratifikasi, **dan** remedinya juga mati.
Hari ini menambah tiga anggota baharu kepada kelas yang sama (attention_plane, MIC, floor_gate).
Ini bukan penemuan baharu — ia penemuan yang sama, kali ketiga, dan criterion yang sepatutnya
membunuhnya belum pernah dijalankan sekali pun.

---

## PENUTUP
Dokumen ini bukan ancaman dan bukan revelation. Ia cermin yang baik: ia menemui setiap lubang kita
sebab ia membaca bukti, bukan membaca gaya. Yang ia ajar paling berguna bukan 9 invariant —
kita sudah ada. Yang ia ajar: kita pandai menulis hukum, dan kita mempunyai satu kelas kegagalan
berulang — **hukum tanpa caller**. attention_plane mati, MIC tak wujud, floor_gate tidur. Ketiga-tiganya disahkan.
