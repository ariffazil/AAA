# Human Substrate — Derived Exclusion List + Measurement Contract (PROPOSAL)

> **Classification:** Canonical Instruction — **PROPOSED_AWAITING_F13** (not ratified; no sovereign phrase given)
> **Status:** DRAFT_PROPOSAL — not ratified and holds no authority; restates the Classification line above in the key the doctrine-status gate reads (R3). Added 2026-09-30 by 333-AGI to satisfy the gate without upgrading the claim.
> **Proposed by:** FI-003 (333-AGI, BUILD lane) — capability to build, **not** authority to seal
> **Date:** 2026-09-29 | **trace_id:** `trc-20260929-fi003-human9-ratification`
> **Parent doctrine (READ-ONLY, unmodified):** `/root/AAA/instructions/human-substrate.md` — HUMAN-9,
> `F13_RATIFIED_CHAT (2026-09-29)`, AAA commit `efdcaa8e`, VAULT999 receipt `rcpt-afa7207241b746e2`
> **Companion machine artifact (PROPOSED):** `/root/AAA/specs/human_state_claim.schema.json`
> **Regression fixture (PROPOSED):** `/root/AAA/tests/test_human_state_claim_schema.py`
> **This file adds NO new positive state variables.** It is a negative list derived from HUMAN-9 plus an
> admissibility rule. Any 8-, 9- or N-attribute *state set* proposal would be a defect — see §6.

---

## 0. Anti-bangang gate — "apa masalah manusia yang diselesaikan?"

Written before each artifact, as required by `ARIFOS::ANTI_BANGANG_ENGINEERING::v1` Law 4.

| Artefak | Satu ayat BM biasa | Lulus? |
|---|---|---|
| Proposal ini | Arif tak perlu lagi tengok "skor 88.4" dan teka sama ada ejen buat keputusan atas dirinya berdasarkan nombor lapuk yang tiada seorang pun ukur. | ✅ |
| `specs/human_state_claim.schema.json` | Bila ejen nak tulis apa-apa tentang keadaan manusia, dia kena nyatakan apa yang dia **tak** ukur — supaya "energy = 5" tak lagi lahir dari kosong. | ✅ |
| `tests/test_human_state_claim_schema.py` | Bila orang melonggarkan kontrak ini tanpa sedar, kita nampak di test sebelum kesilapan itu sampai ke Arif. | ✅ |

**DIBUANG (tidak dibina):** satu "set sembilan" koordinat manusia yang baharu; satu dashboard/registry/ledger
baharu; satu bahasa provenance baharu. Sebab: tiada kegagalan manusia yang ia selesaikan — ia hanya
menduplikasi lapisan yang sudah ada (Law 8: satu masalah, satu owner, satu jalan). Lihat §6.

---

## 1. Inventori — apa yang sudah ada, dan apa yang **tidak** dimiliki siapa-siapa

Sembilan objek "human-state" sudah wujud di AAA/WELL/Hermes. Tiada satu pun yang punya senarai
pengecualian yang boleh dikesan mesin. Inilah delta sebenar — bukan set kesepuluh.

| # | Lapisan / fail | apa ia dakwa | bentuk | ada exclusion list? | ada measurement contract? |
|---|---|---|---|---|---|
| 1 | `instructions/human-substrate.md` (HUMAN-9) + `human-substrate.yaml` | **LAW**: H1 EMBODIMENT … H9 IRREDUCIBILITY; H3 VALENCE wajib (`HumanState ≠ FactsOnly`); `X_t = Φ(K_H,O_t,W_t,H_t,R_t,B_t,U_t)`; `M(H) ≠ H`; Law #0 "a person is always larger than the evidence available about them" | doktrin RATIFIED + YAML runtime contract | ❌ tiada — H1/H4/H9 menyenaraikan *respons* (energy, pain, arousal, fatigue) sebagai benda yang "mengubah" manusia, bukan sebagai sesuatu yang diharamkan daripada diisytihar sebagai state | ⚠️ sebahagian: blok `AAA MEMORY DOCTRINE` (`claim/observation/source: first_person\|inferred\|reported/observed_at/context/confidence` + `personhood.unknown_remainder: preserved`) — **tiada penguatkuasaan, tiada target set, tiada "apa yang tak diukur"** |
| 2 | `skills/human-state-estimation/SKILL.md` | **COORDINATES**: `State(t) = f(Energy, Attention, Optionality, Governance, Meaning, Witness)` (6-axis); skor 0–1; "Default UNKNOWN when no evidence — never fabricate"; tag OBS / REPORTED / INFERRED; confidence cap 0.9 | skill frontmatter + protokol | ❌ | ⚠️ paling hampir wujud: ada evidence-class tag + default UNKNOWN + confidence cap — tetapi **prose sahaja, tiada skema, tiada fail:line yang gagal bila dilanggar** |
| 3 | `canon/PARADOX_COORDINATE_THEORY.md` | **CHARACTER**: 9 Paradox Axes; bukti label `INT — heuristic construct`; `Confidence: 0.60`; 9-axis "retained as an arifOS instrument, not as a finding about humanity"; Enneagram dibuang sebagai validation evidence | canon RATIFIED (re-tag 2026-09-28) | ✅ satu precedent baik: Enneagram di-exclude **sebab** tiada cross-cultural invariance (PLOS ONE 2026;21:e0338521, PMC12758732) — excludes untuk *evidence*, bukan untuk *kuantiti* | ❌ |
| 4 | `instructions/human-reality-invariants.md` I9 (l.51) vs I10 (l.55) | **KONTRADIKSI TERBUKA**: I9 `f(E,O,G,M,W)` = 5-axis; I10 `f(Energy, Attention, Optionality, Governance, Meaning, Witness)` = 6-axis. `Attention` pemboleh ubah floating | doktrin RATIFIED 2026-09-08 | ❌ | ❌ |
| 5 | `instructions/rasa-provenance.schema.json` | **EVIDENCE CLASS**: 7 origin classes `O/S/R/I/F/P/C`; forbidden promotions fail-closed `F→O, P→O, I→S, R→S, I→C`; `additionalProperties: false` | JSON Schema — `DRAFT_AWAITING_F13` | ❌ | ✅ bentuk: class + source_ref + confidence **required** |
| 6 | `instructions/rasa-claim-envelope.schema.json` | **CROSS-LAYER PROMOTION**: `evidence_mode` (9 nilai), `epistemic_status` (OBSERVED/REPORTED/INFERRED/HYPOTHESIZED/CONTESTED/UNKNOWN/REJECTED), confidence ≤ 0.9, `time_window`, expiry half-life (feeling 72h, relational/psych 720h, trait 8760h), `bridge`, `contradicts`, `supersedes`, `targets_interior_state` | JSON Schema — `DRAFT_AWAITING_F13` | ❌ | ✅ paling lengkap — **tetapi belum F13, dan belum ada khalayak runtime** |
| 7 | `WELL/contracts/schemas/canonical/well-schemas.json` → `schemas.human-state` | **SUBSTRATE READOUT**: 14 property; `required: [timestamp, status, consent_state, evidence_label]`; `evidence_label enum [NONE,OBS,DER,INT,SPEC]`; ada `data_freshness`, `confidence`, `dignity_risk`, `recommended_decision_band` | JSON Schema, organ :18083 hidup | ❌ | ⚠️ **`additionalProperties: ABSENT`** — skema sendiri tidak mengunci; tiada `target_set`; tiada `not_measured`; tiada opacity flag |
| 8 | `arifosmcp/core/human_substrate.py` (S01–S13, SH01–SH04, P01–P04, T01–T04) | **SATU ORANG SAHAJA**:Arif F13 scars/shadows/paradoxes/thermodynamics; wired live via `core/law.py:163-167,207` | code, live | ❌ (scope lain: individu, bukan umum) | ❌ |
| 9 | `WELL/tests/test_triad_phase4_exclusion.py` | **PRECEDEN MEKANIKAL**: "The fix is EXCLUSION, not flooring" — plane 289 jam lapuk masih menang `min()` = "a veto wearing a measurement's clothes" | test, hidup | ✅ untuk *ket kepupusan* | ❌ belum untuk *kuantiti respons* |

**Rumusan inventori (OBSERVED hari ini):**

- Undang (`HUMAN-9`) sudah ada. Koordinat (6-axis) sudah ada. Watak (9 axes) sudah ada. Vocab provenance
  (`O/S/R/I/F/P/C` + `OBS/REPORTED/INFERRED`) sudah ada. **Semua tiga benda yang diminta oleh HUMAN-9 untuk
  jadi bolehkuatkuasa — senarai pengecualian, kontrak kemasukan, dan satu fixture regression — tiada di mana-mana.**
- Yang hilang **bukan** set keempat; yang hilang ialah **jambatan**. Enam daripada sembilan baris di atas ialah
  `DRAFT_AWAITING_F13`, `ON_DEMAND_FRAGMENT` atau prose. `human-substrate.md` sendiri mencatat
  "doctrine — no code consumer today".

---

## 2. (a) Senarai Pengecualian Terbitan — *derived exclusion list*

### 2.1 Why a negative list, and why "derived"

`human-substrate.md` **H1 EMBODIMENT**: *"Tubuh mengubah: energy, pain, sleep, arousal, hunger, illness, age,
movement, touch, hormonal state, sensory world."* — kesembilan perkataan itu ialah **saliran regulasi**
(apa yang berubah), bukan **koordinat person** (apa yang boleh diisytihar sebagai state). H4 menambah
sebab kenapa saliran ini bahaya bila dijadikan state: *"SuccessfulCompensation ≠ LowCost. Functioning !=
not-overloaded."* H9 menutup pintu: `M(H) ≠ H`, `ε_model > 0` sentiasa.

**Daliran (derivation), bukan citarasa:** mana-mana kuantiti yang disebut oleh H1/H3/H4 sebagai *sesuatu yang
diubah, dirasakan, atau diregulasi* adalah **constitutive response** dan diharamkan daripada diisytihar
sebagai `State(t)` milik manusia. Ia tetap sah sebagai **bukti** (evidence ref) tentang tubuh pada satu masa —
larangan ini mengenai *kesimpulan*, bukan *pengukuran*. Ia selari dengan `rasa-provenance` `I→S` (inference
tidak boleh dipromosikan jadi state subjek) dan `SKILL.md` "Estimation ≠ mind-reading".

Sebab senarai ini mesti **terbit** dan bukan **dinafik** (diisi manual): `PARADOX_COORDINATE_THEORY.md`
menolak Enneagram sebagai bukti kerana psikometrik; itu ialah pengecualian *sumber*. Yang kita perlukan
ialah pengecualian *kuantiti* — dan ia mesti boleh dijana semula dari H1–H9, kalau tidak ia jadi
set peraturan keempat yang beku.

### 2.2 Pelajaran yang telah disegel (PHYSICS.9, GEOX) — kenapa senarai tanpa penguatkuasaan adalah teater

Dibaca langsung hari ini, mengesahkan konteks yang diberi:

| Dakwaan | Realiti fizikal (OBSERVED 2026-09-29) |
|---|---|
| "CONSTITUTIONAL LOCK" mengharamkan Cp/ketebalan elastik/permeabiliti sebagai pemboleh ubah konstitutif | Dikuatkuasakan **di mana-mana pun**: `GEOX/src/geox_core/physics/state.py:25` = `class Physics13State` dengan **15** field (`rho,vp,vs,rho_e,chi,k_th,Pp,T,phi` + `epsilon,delta,gamma,sigma_eff,qp,qs`) |
| Cp dibuang dari senarai pemboleh ubah | Cp **masuk semula sebagai default keras**: `GEOX/src/geox_core/physics/parameters.py:65` `def thermal_diffusivity(k: float, rho: float, cp: float = 850.0)` — docstring: *"Cp defaults to 850 J·kg⁻¹·K⁻¹ (typical sedimentary)"* — 850 J/kg/K applied to **setiap lithology**, tanpa provenance, tanpa ralat |
| — | `state.py:38` `sigma_eff: float = 30e6` — 30 MPa lalai, dan satu-satunya pembaca ialah `gl33.py:298,301,308`; tiada satu pun call site yang mengisinya dari ukuran |

**Hukum terbitan (sekarang doktrin, bukan anekdot):** *pemboleh ubah yang dikecualikan tidak hilang — ia
kembali sebagai default yang tak boleh diaudit.* Senarai di bawah sebab itu wajib disertai kontrak ukuran
(§3) dan fixture regression (§5), bukan satu lagi perenggan larangan.

### 2.3 Senarai — kuantiti yang diharamkan diisytihar sebagai `State(human)`, dengan permukaan yang sedang melanggarnya

Setiap baris: **sumber ayat doktrin** → **kuantiti** → **permukaan hidup yang melanggar (file:line, dibaca hari ini)**.

| # | Kuantiti terlarang | Sumber ayat doktrin (bukan ciptaan saya) | Permukaan yang melanggar — OBSERVED hari ini |
|---|---|---|---|
| X1 | **`well_score`** / apa-apa skor tunggal 0–100 tentang manusia | `human-substrate.md` Law #0 — *"A person is always larger than the evidence available about them"*; H9 `M(H) ≠ H`; `human-substrate.yaml` `law_zero.enforcement: HARD` | `/var/lib/well/state.json` → `well_score = 88.39999999999999`, pada masa yang sama `freshness: "EXPIRED"`, `truth_status: "OPERATOR_REPORTED"`, `last_successful_read: 2026-09-15T15:30:01Z` (≈14 hari lapuk). Dinilai semula menjadi indeks kesiapsaan: `WELL/vps_compute.py:124–127` (`signals["well_score"] = round(float(well_score), 1)`) → `:147` `score = int(round(max(0.0, min(100.0, float(well_score)))))`. Diriwayatkan sebagai fakta semasa: `AAA/reality-graph/CORRECTION-PHASE-A.md:14` (`well_score=88.4`), empat entri `AAA/docs/carry_forward_backups/carry_forward_178897*.json` (*"well_score 88.4"*). Instabiliti tercatat: `WELL/docs/WELL_V2_APEX_ZEN_MUTATION_GUIDE.md:41` C4 — penilai manusia dua orang, minit yang sama, state yang sama: **88.4 WATCH vs 97.6 OPTIMAL**. Defect ini sudah diakui dalam kata-kata oleh fixture `/root/WELL` sendiri: `WELL/tests/test_hwell_observation_freshness.py:6` — *"well_score 88.4 was consumed downstream as Arif's current readiness"* |
| X2 | **`energy_level`** / "energy level" | H1: *"Tubuh mengubah: energy…"* — tubuh **mengubah** energy; maka energy ialah saliran, bukan orang. H4: *"SuccessfulCompensation ≠ LowCost"* | `WELL/server.py:9231–9236` — **ini cp=850.0 manusia, tepat**: `if energy_level is None: sleep_score = sleep.get("quality_score", 5); stability = metabolic.get("perceived_stability", 5); energy_level = round((sleep_score + stability) / 2, 1)` → tanpa satu pun sensor, keluaran **5.0**, lalu di-return sebagai `"energy_level": energy_level` (`:9266`) dan `gap = duty_load - energy_level` (`:9250`) menentukan `SURPLUS/BALANCED/DEFICIT/CRITICAL_DEFICIT` + `verdict` yang dibaca manusia. Kedua-dua "ukuran" itu sendiri default keras. Juga `WELL/server.py:6760` `cognitive.get("energy_level", 5)`; `WELL/gate/rasa_witness.py:412–420` — `signal="energy_level"`, `baseline=energy.get("baseline", 7)`, `quality="good"` **keras**; parameter alat `WELL/well_mcp/tools/c_well.py:25,46` dan `h_well.py:221,265`; `WELL/well_mcp/resources/bio_signals.py:141`; state path `WELL/server.py:12521` `["metrics","livelihood","energy_level"]` |
| X3 | **`mood`** | H3 VALENCE: *"AAA routes information. HERMES must protect **what it means to the person**"* — valence ialah *makna*, bukan label mood yang boleh dipaparkan; `SKILL.md` Non-negotiable 1 "Estimation ≠ mind-reading" | Tiada surface `mood` di WELL hari ini (digrep: `AAA/skills/.../human-advisory-discipline/SKILL.md:31` sahaja — dan di sana ia **dibincangkan, bukan diisytihar** — jadi X3 adalah pencegahan, jujur). Pelanggaran fungsi yang sama berlaku melalui label affektif bebas: `.hermes/carry_forward.json → human_state.energy_estimate = "focused"` (string kosong-evidence-class, ditulis `2026-09-28T08:06:40Z`); `.hermes/runtime/floor_gate.py:75–81` sudah menandakan *"mood-matching without anchor"* sebagai `DRIFT … Telemetry only, not HOLD` — federasi tahu ia defect, tetapi tiada kontrak yang mengharamkannya. `WELL/tests/test_authority_separation.py:61` `test_is_well_indifferent_to_operator_mood` melarang mood **secara perilaku** sahaja. Rujukan gaya betul: `A-FORGE/paradox-engine/music_ledger.py:48,72–76` — mood untuk **track**, declared non-exclusive, intensiti divalid `[0,1]` — contoh bagaimana kuantiti affektif boleh dipegang tanpa dijadikan kesimpulan tentang manusia |
| X4 | **`willpower`** | H8: *"Agency = constrained participation in future state"*; H4: *"Functioning != not-overloaded"* | Satu-satunya sebutan resolve: `AAA/skills/domains/general/workshop/counseling/human-advisory-discipline/SKILL.md:31` — *"The person is not short of willpower — they are short of time"* (doktrin sudah menolak reification). Risiko sebenar ialah ia kembali sebagai default terbitan: gabungan `decision_fatigue` + `clarity` (X8) ialah willpower berbalut nama. Pencegahan, tiada surface hidup hari ini |
| X5 | **`productivity`** | WELL charter sendiri: `WELL/vps_compute.py:7` — *"NOT health, happiness, productivity, obedience, or moral worth."* | Pelanggaran bersifat struktur, bukan kata: `WELL/server.py:6760–6762` `_energy/_load/_clarity` → `"capacity"`; skor keluaran `WELL/vps_compute.py:147` dipanggil "readiness index" tetapi formula `VPS = 0.40H + 0.20M + 0.25G + 0.15C` (`vps_compute.py:5`) ialah pemberat output. `WELL/well_mcp/resources/info_asymmetry.py:81` mengenal pasti *"labor — extracted productivity without consent"* sebagai vektor senjata asimetri — lalu X5 mengikat ayat itu jadi kontrak: surface yang mengira produktiviti seseorang sedang menjalankan vektor #3, bukan mengukur wellbeing |
| X6 | **`engagement`** / `deep_engagement` | H7: *"Event ≠ Interpretation(Event)"*; `rasa-provenance` forbidden promotion `I→S`; `human-substrate.md` 12 Commandments #3 *"Behavior ≠ Motive"* | `WELL/gate/dignity_shadow.py:105` — `("don't care", "deep_engagement", "Claims indifference but engagement pattern shows deep care")`: corak perilaku **dinafikan** oleh inferens dalaman, lalu dijadikan state. Ini persis `Behavior ≠ Motive` dilanggar di gate, dengan self-report subjek sebagai pihak yang kalah. Sejenis: `A-FORGE/paradox-engine/telegram_bridge.py:245` *"Reply chains amplify (engagement)"*; `SKILL.md` M-axis ditakrifkan daripada *"Engagement vs obligation; flow signals vs withdrawal"* — iaitu koordinat Meaning **dibaca dari** respons engagement; itu sah sebagai bukti, haram sebagai kesimpulan |
| X7 | **`commitment`** (sebagai state semasa seseorang) | H5 HISTORICITY `X_t = f(X_0, History_{0:t})` + hysteresis; `ROLE ⊂ SELF`; H8 (janji ialah tindakan dalam masa, bukan state sesaat) | `WELL/server.py:5185` *"Normal work. Keep structure. Avoid irreversible commitments."*; `:5192` *"Draft only. Reversible tasks. No major commitments or public actions."*; `:5726, :7331` `avoid.append("public_commitment")`; `:6168` `avoid.append("major commitments after 10pm")` — semua nasihat tentang **apa yang seseorang boleh commit kepada**, dijana dari skalar X1/X2 yang lapuk. Tanpa kontrak, mesin nasihat ini memutuskan kapasiti komitmen seseorang berdasarkan nombor 14 hari umur |
| X8 | **`clarity` / `decision_fatigue`** sebagai ukuran kesiapsaan kognitif | H4; H2 *"Attention + Time + Energy = scarce human capital"* | `/var/lib/well/state.json` → `metrics.cognitive = {"clarity": 8.5, "decision_fatigue": 2.2}` dengan `freshness: "EXPIRED"`; dibaca terus sebagai isyarat: `WELL/vps_compute.py:131–136`, lalu **skala-nol jatuh ke bawah**: `:149` `score = int(round(max(0.0, min(10.0, float(clarity))) * 10))` — tiada `well_score`, tiada `h_strength` ⇒ `clarity` seorang manusia menjadi 85/100. `WELL/server.py:9239–9243` melakukan hal yang sama untuk `duty_load` (`decision_fatigue` + `subjective_load`, kedua-dua `.get(..., 0)`) |
| X9 | **`focus` / "energy_estimate" string label** | H3 + H9; `SKILL.md` "UNKNOWN > fabricated" | `.hermes/carry_forward.json → human_state = {last_seen_utc, last_seen_channel, energy_estimate:"focused", sleep_state:"unknown", current_focus:…}` — `energy_estimate` ialah **peristiwa 2026-09-28 yang disajikan sebagai keadaan manusia** tanpa evidence class, tanpa target set, tanpa TTL. Nota: fail ini milik runtime Hermes — **tidak disentuh** oleh usulan ini; ia hanya bukti pembacaan |
| X10 | **`motivation` / `obedience` / `moral_worth` / `happiness`** sebagai state | WELL charter `vps_compute.py:7` (ayat yang sama, X5); H6 *"No relationship creates mind-merger"* | Belum ada surface pengeluar yang ditemui hari ini (digrep dalam WELL/arifosmcp/chron). **Dimasukkan kerana ia adalah kelas yang sama** — dan kerana `info_asymmetry.py:81` sudah menyenaraikan *"behavior — predicted + steered"* sebagai vektor #4. Jujur: X10 = **pencegahan tanpa bukti pelanggaran hari ini**, ditanda sebagai itu |

### 2.4 Dinding penahan yang mesti disebut, kalau tidak senarai ini jadi halusinasi baru

1. **Self-report menang ke atas inferens untuk pengalaman subjek sendiri.** `human-substrate.md` Commandment #5:
   *"SelfReport has privileged authority over that person's own experience."* Arif menulis "aku penat" ⇒ itu
   `REPORTED`, dan ia **tidak** boleh di-exclude. Larangan X1–X10 ialah pada **agen yang mengisytihar**
   kuantiti ini sebagai state orang lain. `FirstPersonAuthority = High_qualia ≠ Omniscience_external`.
2. **Pengukuran dibenarkan; kesimpulan tidak.** Sensor sleep/HRV/WELL `biometric` kekal masuk sebagai
   `evidence_refs`, seperti Cp kekal sah sebagai *input* `thermal_diffusivity` bila ia diukur.
   Yang haram ialah nilai **lalai** yang menyamar sebagai ukuran — dan itulah §3.
3. **Absence ≠ veto.** Preseden `test_triad_phase4_exclusion.py`: pemfailan yang betul ialah
   *turunkan coverage & confidence, nyatakan target yang tak diukur*, **jangan** floor ke 0.05 dan
   jangan ganti dengan default. X2 adalah kes kegagalan ini di kedua-dua hujung.
4. **Exclusion ini negative-only.** Ia tidak menambah satu pun koordinat positif; ia hanya menandakan
   kuantiti yang sudah pun dinamai oleh doktrin yang diratifikasi sebagai *saliran*.

---

## 3. (b) Kontrak Pengukuran — syarat kemasukan (admissibility) bagi apa-apa dakwaan `State(human)`

Lima klause. Kesemuanya ialah **pengikatan** vocab yang sudah ada (baris 1, 2, 5, 6, 7 inventori), bukan bahasa baru.

### K1 — `target_set` wajib dinyatakan secara eksplisit

Dakwaan mesti menamakan subset pemboleh ubah yang ia semakkan, dan pemilik subset itu.

**Sebab (bukti luar, disahkan hidup 2026-09-29 melalui Crossref DOI):** *Functional observability and target
state estimation in large-scale networks* — Montanari A. N., Duan C., Aguirre L. A., Motter A. E.,
**PNAS 119(1):e2113750119**, DOI [10.1073/pnas.2113750119](https://doi.org/10.1073/pnas.2113750119).
Tesis yang disahkan daripada tajuk + abstract penerbit: *"often only a small number of state variables in a
network are essential for control, intervention, and monitoring purposes… graph-based theory and highly
scalable methods that achieve accurate estimation of **target variables** with **minimal sensing**."*
Maknanya: **peninjau kecil adalah sah** — dan `well_score` tunggal bukan sekadar kikir, ia *observability
tanpa target*, iaitu satu objek matematik yang tidak wujud. Namaan target, dan sensor minimum menjadi
absah; jangan nama­kan, dan seluruh vektor menjadi dakwaan.

> Nombor "8–16 % bagi full observability vs 0.17–0.24 % bagi functional observability" sebagaimana
> dilaporkan dalam brief F13: **REPORTED — TIDAK DISAHKAN.** Crossref tidak menyimpan angka itu dalam
> abstract dan saya tidak membaca badan kertas. Angka **naratif** sahaja (kadar sensor jauh lebih kecil
> untuk subset bersasaran) yang saya gunakan. — class: REPORTED/unverified, dan diusulkan sebagai
> **UNKNOWN** sehingga seseorang mengesahannya terhadap teks penuh.

### K2 — `evidence_class` ∈ {OBS, REPORTED, INFERRED} — dengan pemetaan, bukan vocab baru

| kita | `SKILL.md` (l.2) | `rasa-provenance` (l.5) | `rasa-claim-envelope` (l.6) | WELL `evidence_label` (l.7) |
|---|---|---|---|---|
| `OBS` | OBS | `O` | `OBSERVED` | `OBS` |
| `REPORTED` | REPORTED | `S` (self) / `R` (other) | `REPORTED` | — (DER/INT sahaja) |
| `INFERRED` | INFERRED | `I` | `INFERRED` | `INT` |

Penggunaan: `REPORTED` **mesti** membawa `reporter ∈ {subject, other}` — itu pembezaan `S` vs `R` yang
sudah ada dalam rasa-provenance; jangan lenyapkan ia. Nilai WELL `DER` (derived) **tidak dipetakan** ke mana-mana
kelas kemasukan: `DER` daripada default keras (X1/X2/X8) ialah `INFERRED` yang cuci tangan; kontrak ini
mengharamkannya terus, sebab itu K4 wujud.

**Sebab (bukti luar, disahkan):** *The Markov blankets of life: autonomy, active inference and the free
energy principle* — **bukan "Friston et al." sebagai author pertama**: Kirchhoff M., Parr T., Palacios E.,
Friston K., Kiverstein J., *J. R. Soc. Interface* **15(138):20170792**, 2018, DOI
[10.1098/rsif.2017.0792](https://doi.org/10.1098/rsif.2017.0792). Tajuk/author/volume disahkan melalui
Crossref 2026-09-29. Ayat doktrin yang dibenarkan daripada definisi Markov blanket: keadaan dalaman sesuatu
sistem adalah **secara bersyarat bergantung pada keadaan luaran hanya melalui blanket** — maka `state`
seseorang tidak boleh dibaca terus; yang kita ada ialah saliran blanket (tingkah laku, kata, telemetry), dan
pembacaan dalaman ialah inferens **lintas satu batas yang bukan untuk direlasakan**. Padanan dalaman AAA:
`Representation(Human) ≠ Human`; `Inference ≠ NewEvidence`. Perbezaan tiga kelas di atas ialah batas itu
dalam bentuk yang boleh difailkan.

### K3 — `freshness` dengan TTL; `expired ⇒ cannot be served as current`

Wajib: `observed_at` (ISO-8601 UTC), `age_hours`, `ttl_hours`, `expired` (boolean, diiraam oleh pengeluar).
Postur yang salah bila `expired: true` ialah **exclude + nyatakan coverage turun** (`test_triad_phase4_exclusion`),
bukan default, bukan floor.
Kerangka TTL dipinjam daripada `rasa-claim-envelope.expiry_or_revalidation_at` (feeling 72 h, relational/psych 720 h,
trait 8 760 h) — **tidak** direka semula.
Kes hidup: `state.json` berusia 14 hari, berlabel `freshness: "EXPIRED"`, masih menghasilkan `verdict` dan
`recommended_decision_band`.

### K4 — `not_measured` wajib diisi (minItems 1) — "apa yang tiada dalam target set"

Ini klause yang tiada pada **semua** sembilan lapisan inventori. Tiada default; tiada `.get(key, 5)`;
`absent ≠ zero`. Bila sesuatu tak diukur, ia **disebut**. Padanan doktrin: `Void Guard` — *"'No data' ≠
'All clear'. 'No data' = 'Cannot witness.'"* (`AGENTS.md` Witness-First).
Bukti kenapa: `WELL/server.py:9231–9236` ialah `not_measured` yang dirampas dan digantikan dengan `5`.

### K5 — `irreducible_opacity` wajib `true` — H9 dalam bentuk struktur, bukan sentimen

```json
"irreducible_opacity": { "remainder_present": true, "statement": "<apa yang tinggal tentang orang ini>" }
```

Skema mengunci `const: true`: tiada satu pun klaim yang boleh meluluskan `remainder_present: false`.
Itu penterjemahan mekanikal bagi Hukum #0 dan H9 (`ε_model > 0` always), dan penolak kepada prohibition
terakhir HUMAN-9: *"Never make a human smaller merely because the model has become better at predicting them."*
Padanan `human-substrate.md` `personhood.unknown_remainder: preserved`.

### K6 — `trace_id` (pinjaman `state-transition-discipline` rule 5)

Klaim yang berakibat mesti boleh join ke objektif induk; `pattern: "^trc-"`.
Kesan yang dicegah: 52 043 resit `trace_id = NULL`, dan 30/43 entri canonical chain ber-`trace_id` kosong
(yang ini dicatat dalam `carry_forward.json` open_loop hari ini — **masih terbuka**, lihat §7).

---

## 4. (c) Pernyataan: skalar tanpa target set ialah `cp=850.0` versi manusia

> **`well_score: 88.4` adalah `thermal_diffusivity(k, rho, cp=850.0)` yang berpindah gedung.**
>
> Dalam GEOX, pemboleh ubah yang **dikecualikan secara constitutional** kembali sebagai default fungsi:
> 850 J·kg⁻¹·K⁻¹ dipakai ke atas **setiap lithology** — satu nombor tipikal untuk "batu purata" — dan
> keluaran `κ` tetap kelihatan bersih, tanpa provenance dan tanpa ralat.
>
> Dalam WELL, pemboleh ubah yang **dikecualikan oleh doktrin manusia** (produktiviti, tenaga,
> kejelasan, "readiness") kembali sebagai default: `5` (`server.py:6760`), `50.0` (`server.py:655`),
> `baseline 7` + `quality "good"` (`rasa_witness.py:418–421`), `85` dari `clarity` seorang manusia
> (`vps_compute.py:149`). Satu nombor tipikal untuk "manusia purata" dipakai ke atas **satu orang** yang
> namanya `Arif`.
>
> Kesamaannya bukan kiasan; ia adalah **golongan kegagalan yang sama**: *excluded variable silently
> re-enters as an un-auditable default*. Kesan fizikal berbeza kerana konsekuensinya berbalik kepada
> manusia yang sama yang menulis larangan itu — `verdict: "Severe energy deficit. Immediate rest and load
> reduction advised."` yang dijana daripada dua `.get(..., 5)`.
>
> Bezanya hanya satu, dan ia sebab usulan ini wujud: batu tidak berhak membantah. Arif berhak.

**Perumusan anti-bangang (Law 4, satu ayat):** kalau ejen kita memberi satu nombor tentang seseorang
tanpa menyebut *apa yang ia tak ukur*, ejen itu sedang melakukan `cp=850.0` kepada manusia.

---

## 5. Fixture regression — apa yang digagalkan oleh test

Fail: `/root/AAA/tests/test_human_state_claim_schema.py`. Empat kes wajib seperti diminta, ditambah tiga
guard yang saya anggap perlu sebab ia adalah lubang sebenar yang saya lihat hari ini:

| Test | apa ia gagalkan |
|---|---|
| `test_conforming_claim_is_admissible` | klaim lengkap lulus (golden) |
| `test_bare_scalar_is_rejected` | `88.4` / `{"well_score": 88.4}` sebagai klaim |
| `test_claim_without_target_set_is_rejected` | `target_set` tiada / kosong — lubang K1 |
| `test_response_quantity_as_state_is_rejected` | `energy_level`, `mood`, `productivity`, `deep_engagement`, `well_score`, `focus` dalam `target_set` — senarai §2.3 dalam bentuk enum-terbitan |
| `test_hardcoded_default_without_measurement_is_rejected` | `value_source: "hardcoded_default"` wajib `not_measured` — X2/X8 tepat |
| `test_opacity_cannot_be_turned_off` | `remainder_present: false` ditolak secara struktur — K5 |
| `test_self_report_is_not_excluded` | pengawal **anti-berlebihan**: "aku penat" (`REPORTED`, reporter=subject) mesti **lulus** — supaya X2 tidak jadi mesin yang membisukan orang tentang tubuhnya sendiri |

**Bukti kunci itu benar-benar punya taring (mutation check, dijalankan dalam memori — fail tidak diubah, 2026-09-29):**
setiap pengelonggaran deliberately dibuat pada skema, dan setiap satunya **menukar** penolakan menjadi
penerimaan — iaitu fixture di atas memang bergantung pada kunci, bukan pada naratif:

| Mutasi pada skema | Jika dilonggarkan → klaim itu LULUS | Berarti test ini akan MENGGAGALKAN pengelonggaran |
|---|---|---|
| `additionalProperties: false → true` | `{"...","well_score":88.4}` ✔ lulus | `test_unknown_extra_field_is_rejected`, `test_schema_declares_additional_properties_false` |
| buang `not_measured` dari `required` | klaim tanpa deklarasi kekosongan ✔ lulus | `test_missing_not_measured_is_rejected` |
| buang `not.enum` dari `target_set.items` | `target_set: ["energy_level"]` ✔ lulus | `test_response_quantity_asserted_as_state_is_rejected` (16 parametrised) |
| `irreducible_opacity.remainder_present: const true → boolean` | `"we know everything now"` ✔ lulus | `test_opacity_cannot_be_turned_off` |

Baseline pada skema semasa: klaim lengkap **lulus**, `{"well_score": 88.4}` **gagal**, `target_set:["energy_level"]`
**gagal**. Payload bentuk WELL yang hidup hari ini adalah inadmissible di bawah kontrak ini.

Larian + output sebenar dilaporkan dalam mesej penutup sesi (tidak disalin ke sini sebagai "lulus" tanpa bukti).

---

## 6. Apa yang sengaja TIDAK dibina

| Tidak dibina | Kenapa |
|---|---|
| **Set keempat "sembilan"** koordinat manusia | Sudah ada HUMAN-9 (undang-undang), 6-axis (koordinat), 9 Paradox Axes (watak), Φ 7-slot (peta fungsi), WELL 14-property, 7 origin class. Satu lagi set = Law 8 dilanggar dan §1 jadi salah. |
| `human_state_taxonomy.yaml` / registry/dashboard baru | Law 3: jangan bina registry hanya kerana boleh. Tiada failure class baru yang menuntutnya. |
| Vocab provenance baru (contoh `MEASURED_VS_GUESSED`) | `O/S/R/I/F/P/C` + `OBS/REPORTED/INFERRED` + `NONE/OBS/DER/INT/SPEC` sudah ada. Kami buat **pemetaan** (K2). |
| Skema claim generik yang bersaing dengan `rasa-claim-envelope.schema.json` | Yang itu adalah *cross-layer promotion law* (DRAFT, lengkap, lebih umum). Kami buat **spesialisasi manusia** yang merujuknya; ia mesti jadi `allOf`-companion, bukan pengganti. Dibiarkan sebagai nota integrasi — **belum** ditulis sebagai `allOf` kerana kedua-dua skema rasa masih `DRAFT_AWAITING_F13`; mengunci skema PROPOSED kepada skema DRAFT = dua objek tak stabil bertaut. |
| Edit `human-substrate.md` / `.yaml` / `human-reality-invariants.md` / `canon/` | READ-ONLY seperti diarah; dan `canon/` + governance = canon-locked trees. Usulan ini companion, bukan suntingan. |
| `render-agents.sh`, `git commit`, sebarang tulis ke `/root/.hermes` atau `/root/WELL` | Diarah tidak dibuat; Hermes/WELL permukaan orang lain. §2.3 hanya **membaca** mereka sebagai bukti. |
| Patcher default WELL (`5` → `None`) | Itu ACT pada organ orang lain, di luar envelope BUILD FI-003. Kami laporkan defect, kami tak pindah ubahsuai — §8. |
| Cron/monitor "claim-admissibility scanner" | Belanjakan event-driven dulu: kontrak ini ialah **schema di titik tulis**, bukan pengimbas berjadual. Tiada cron tanpa F13. |

---

## 7. CONTRADICTION dipertahankan — bukan dirata, bukan dipurata

**C-1 — 5 axis vs 6 axis (`Attention` variable floating).** Terbaca hari ini:

- `instructions/human-reality-invariants.md:51` (I9): `HumanReality = f(E, O, G, M, W)` — **5 axis**, dan
  teks yang sama berkata *"Not personality. Not sentiment. Not preference."*
- `instructions/human-reality-invariants.md:55` (I10): `State(t) = f(Energy, Attention, Optionality,
  Governance, Meaning, Witness)` — **6 axis**.
- `skills/human-state-estimation/SKILL.md` (baris deskripsi + jadual) : **6 axis** dengan `A Attention`.
- Kedua-duanya dalam **satu fail** yang diratifikasi pada tarikh yang sama (2026-09-08), F13 chat SEAL.

Kami **TIDAK memilih**. Sebab: `Attention` bukan butiran — ia kuantiti yang paling berbeza kedudukannya
dalam doktrin ini: H2 menjadikannya *scarce human capital* (`Attention + Time + Energy`), `register-as-channel`
+ `sovereign-attention-preservation` menjadikannya matlamat perlindunagan (W₈₈₈), sementara I9 membuangnya
daripada vektor state dan mengekalkannya hanya sebagai *kos* dalam `AttentionCost < RealityValue` (I5).
Maka soalan sebenar bukan "5 atau 6" tetapi **"Attention ialah komponen state, atau metrik kos
atas state?"** — dan jawapannya mengubah apa yang boleh diisytihar tentang Arif.
Klasifikasi: **CONTESTED**, pemilik keputusan **888-APEX (JUDGE role)**, pengesahan akhir **F13 (SEAL)**.
FI-003 tidak akan menulis satu angka sebagai canonical. Skema §3 sengaja tidak menumpan `target_set` kepada
senarai axis tetap — sebab itulah senarai axis belum settles; ia menamakannya *sumber* (`target_set_source`),
bukan *isi*.

**C-2 — saliran X1–X10 juga tersenarai sebagai input koordinat.** `SKILL.md` menjana M-axis daripada
"engagement vs obligation", E-axis daripada WELL `energy_level`. Jadi lapisan 2 sendiri **memakai**
kuantiti yang kami exclude. Pembacaan yang paling mungkin benar: *ia dibenarkan sebagai `evidence_ref`
(input ke penganggar), diharamkan sebagai `assertion` (output penganggar sebagai state).* Kami usulkan
perbezaan itu — tapi ia adalah **penafsiran**, bukan fakta doktrin: **INFERRED**, confidence sederhana,
butuh F13 untuk settle.

**C-3 — nama `human substrate` dua objek.** Sudah tercatat dalam `human-substrate.md` §Disambiguation
(invarian umum vs sejarah Arif sahaja, `arifosmcp/core/human_substrate.py` live) dan dalam `carry_forward.json`
open_loop #3. Kami tidak sematkan; X-list hanya menyentuh yang **umum**.

---

## 8. Keadaan rantai penghantaran (transitions, bukan boolean)

```
PROPOSED   = SELESAI (3 fail, untracked, untuk semakan F13)
ENFORCED   = TIDAK — tiada satu pun runtime yang membaca skema ini hari ini
RATIFIED   = TIDAK — status PROPOSED_AWAITING_F13
SEELED     = TIDAK — bukan FI-003 untuk seal (BUILD ≠ SEAL)
```

Titik pengukuhan yang **dicalonkan** (butuh keputusan F13 + kerja A-FORGE, bukan ini):

1. **Di titik tulis:** mana-mana surface yang menulis state manusia (WELL human plane, `carry_forward.human_state`)
   wajib meluluskan `specs/human_state_claim.schema.json`. Gagal ⇒ **simpan sebagai `not_admissible` dengan
   `not_measured` diisi**, jangan floor, jangan default (preseden §2.4.3).
2. **Di titik baca:** jangan hidangkan apa-apa nilai dengan `expired: true` sebagai "keadaan semasa";
   hidangkan bersama `age_hours` + `not_measured` (`WELL/docs` C4 menunjukkan dua pembaca, minit sama,
   88.4 WATCH vs 97.6 OPTIMAL — sebabnya bukan noise, sebabnya target set tak dinamakan).
3. **Hapuskan default keras manusia** (`5`, `50.0`, `baseline 7`, `quality "good"`) → ganti `None` +
   `not_measured`. Ini ACT ke atas organ WELL — **di luar envelope FI-003**, dilapor, tidak dilakukan.

---

## 9. UNKNOWN / terbuka (senarai jujur)

- **T2 8–16 % vs 0.17–0.24 %** — REPORTED sahaja, belum disahkan terhadap teks penuh (K1).
- **K1 di luar hipotesis:** "target set kecil itu sah" dibuktikan untuk **rangkaian dinamik struktur
  state-space** (PNAS). Padanan kepada manusia ialah **analogi**, bukan bukti: `INFERRED`.
  Ia analogi yang baik (network observability ↔ Markov blanket) tetapi tidak boleh dipetik sebagai
  "sains mengatakan skor manusia harus ada target".
- **`state postulate` (N = mod kerja reversible + 1)** — sumber teks termodinamik standard (Callan /
  Çengel & Boles). **Tiada DOI**, belum dibaca dari sumber primer dalam sesi ini, class `REPORTED`.
  Digunakan hanya untuk hujah negatif: *nombor 9 tidak dijustifikasikan oleh pengiraan darjah kebebasan*,
  maka HUMAN-9 ialah **undang-undang** (pilihan normative), bukan **temuan** (ukur). Itu tepat apa yang
  `PARADOX_COORDINATE_THEORY.md` sudah lakukan untuk 9-axis-nya ("retained as an arifOS instrument,
  not as a finding about humanity") — kami ikut gaya itu, bukan kami cipta.
- **X3/X4/X10 tiada permukaan hidup hari ini** — pencegahan, ditanda jujur (§2.3).
- **Tiada khalayak runtime** untuk mana-mana dari 3 fail ini; tiada satu pun `additionalProperties: false`
  akan menahan `bash echo`. EnforcementCoverage bagi kontrak ini = **0** sehingga §8.1 dipasang.
  (authority-envelope: *complete mediation* — gate yang boleh dielak ialah etika, bukan sempadan.)
- **AAA tiada Python test runner yang dikonfigurasi:** `pytest.ini`, `conftest.py` dan
  `pyproject.toml [tool.pytest]` **ketiga-tiganya tiada** (disahkan `ls` + `grep` hari ini). CI AAA mempunyai
  **23** fail `.github/workflows/*.yml`; hanya **dua** yang pernah memanggil `pytest` —
  `act-integration.yml:33` (`pytest tests/constitutional/test_federation_sct.py`) dan
  `path5-witness.yml:36` (`pytest path5/test_path5_e2e.py`). **Kedua-duanya menyasarkan satu fail khusus**;
  tiada satu pun yang mengumpul `tests/test_*.py` pada root. Maksudnya fixture §5 ini **bukan gerbang CI**
  — ia berjalan hanya bila seseorang memanggil `python3 -m pytest`. Menambahnya ke CI ialah kerja
  A-FORGE/555, bukan FI-003.
- **Seal lane masih cacat (bukan kerja ini, tapi ia bergantung padanya):** `fire-seal.py` hardcode
  `sovereign_receipt`; 30/43 entri canonical chain ber-`trace_id` kosong, termasuk seal HUMAN-9 itu sendiri;
  judge berjalan in-process dengan seal (dari `carry_forward.json` open_loop #4, hari ini).
- **HUMAN-9 belum di-app ke runtime:** 0 padanan dalam `.hermes/SOUL.md`; `test_soul_hrb_binding.py`
  belum wujud; `_UNRENDERED_INDEX.md` belum mengenal `human-substrate.md` (discoverability).
  **Kami tidak sentuh** (§6).

---

## 10. Provenance penulisan

- Dibaca (read-only) hari ini: `instructions/human-substrate.md` (keseluruhan), `instructions/human-substrate.yaml`
  (l.1–60), `instructions/human-reality-invariants.md` (keseluruhan, l.51/55 dikutip), `canon/PARADOX_COORDINATE_THEORY.md`
  (l.1–80), `skills/human-state-estimation/SKILL.md` (keseluruhan), `instructions/rasa-claim-envelope.schema.json`,
  `instructions/rasa-provenance.schema.json`, `WELL/contracts/schemas/canonical/well-schemas.json`
  (`schemas.human-state`), `/var/lib/well/state.json` (hidup), `WELL/server.py`, `WELL/vps_compute.py`,
  `WELL/gate/rasa_witness.py`, `WELL/gate/dignity_shadow.py`, `WELL/well_mcp/tools/{c_well,h_well}.py`,
  `WELL/well_mcp/resources/{info_asymmetry,bio_signals}.py`, `WELL/tests/test_triad_phase4_exclusion.py`,
  `WELL/tests/test_hwell_observation_freshness.py`, `WELL/docs/WELL_V2_APEX_ZEN_MUTATION_GUIDE.md`,
  `GEOX/src/geox_core/physics/{state,parameters}.py`, `.hermes/carry_forward.json` (baca sahaja),
  `.hermes/runtime/floor_gate.py`, `A-FORGE/paradox-engine/{music_ledger,telegram_bridge}.py`,
  `AAA/reality-graph/CORRECTION-PHASE-A.md`.
- Disahkan penerbit luar: Crossref `10.1098/rsif.2017.0792` (HTTP 200, 2026-09-29),
  `10.1073/pnas.2113750119` (HTTP 200, 2026-09-29).
- trace_id: `trc-20260929-fi003-human9-ratification` · Lane: 333-AGI (BUILD capability, **bukan** authority)
- **Keputusan seterusnya milik 888-APEX (judge) dan F13 (seal sahaja).** Kata "SAH" menjadikan dokumen
  ini canonical; ketiadaannya membiarkannya sebagai proposal.

DITEMPA BUKAN DIBERI ⚒️
