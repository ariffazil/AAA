# AAA_Q_COLLAPSE_TEST_HARNESS_v0 — Executable Contract Replay Spec

> **Status:** SPEC (read-only, no runtime wiring). Parent blueprint: `/root/AAA/cockpit/AAA_Q_COLLAPSE.md` (439 baris).
> **Falsifier doctrine:** doctrine stops growing unless a failing executable test demands it. Spec ini ialah test yang menuntut — bukan doctrine baru.
> **Immutable rule chain:** COLLAPSE ≠ AUTHORIZATION ≠ EXECUTION (sovereign correction 2026-10-02).
> **Scope:** 3 test sahaja. Pass ketiga-tiga → layak untuk shadow-mode phase. Gagal satu → fix contract, bukan tambah doctrine.

---

## 0. Apa spec ini BUKAN

- Bukan production hook. Bukan arifOS organ. Bukan cron. Bukan AGENTS.md propagation.
- Bukan doctrine synthesis — parent blueprint dah ada.
- Bukan penambahan invariant. Empat invariant yang diuji di sini dah wujud:

| # | Invariant yang diuji | Sumber |
|---|---|---|
| I1 | `MachineResolvable(x) ⇒ HumanChoiceRequired(x) = False` | Human Attention Membrane (F13 2026-09-13) |
| I2 | `MissingEvidence ≠ NegativeEvidence` | WEALTH timeout lesson, live 2026-10-02 |
| I3 | `CandidateMultiplicity ≠ EvidenceMultiplicity` | CHRON correlated-observation guard, live 2026-10-02 |
| I4 | `Representation ≠ Reality` (DECLARED ≠ DISCOVERED ≠ CALLABLE ≠ OBSERVED ≠ VERIFIED) | AAA/instructions/representation-reality-invariant.md |

---

## 1. Harness shape (bukan hook)

Satu skrip deterministik. Input: fail case JSON. Output: fail result JSON. Tiada network call wajib. Tiada LLM call wajib (reasoning layer disimulasikan dengan fixture keputusan stage supaya test 100% reproducible).

```
replay_v0.py --case tests/case_N.json --out results/case_N_result.json
```

Result schema (sama untuk semua case):

```json
{
  "case_id": "",
  "collapse": {"next_path": "", "human_required": false,
               "question": null, "confidence": 0.0},
  "alternatives_exposed": 0,
  "candidate_count_internal": 0,
  "evidence_roots_count": 0,
  "provenance": {"stage_decisions_fixture": "", "timestamp": "",
                 "harness_version": "v0"}
}
```

---

## 2. TEST 1 — Deterministic collapse

**Input:** satu fail ada satu bug yang jelas reproduced; satu fix reversible yang dah diuji wujud.

**Peraturan internal yang diuji:**
- Hard gates lulus → tak boleh ada >1 path survive Pareto prune (path lain dominated).
- `alternatives_exposed = 0` — machine-complexity tak sampai ke manusia.

**Pass criteria (semua wajib):**

| Field | Required |
|---|---|
| `next_path` | = apply_the_verified_reversible_fix (nilai tepat dari fixture) |
| `human_required` | false |
| `alternatives_exposed` | 0 |
| `candidate_count_internal` | ≥ 3 (EXPAND wajib serius — termasuk DO NOTHING; anti action-bias) |
| `evidence_roots_count` | 1 (I3: 3 candidates dari 1 evidence root, bukan 3 evidence) |

**Falsifier:** kalau harness keluar menu (alternatives_exposed > 0) untuk kes deterministic → I1 violated → FAIL.

---

## 3. TEST 2 — Real uncertainty → discriminating probe (TEST PALING PENTING)

**Input:** dua hipotesis hidup, evidence tak mampu bezakan, kedua-dua path reversible.

**Peraturan internal yang diuji:**
- I1: mesin WAJIB pilih probe, BUKAN tanya manusia pilih hipotesis.
- Probe selection formula (dari blueprint §14): `p_probe = argmax(InformationGain / (Risk × Irreversibility × Cost))`.

**Spec ketat "smallest discriminating probe" (supaya bukan escape hatch):**

Probe sah jika DAN HANYA JIKA keempat-empat:
1. **Reversible** — undo path wujud dan diuji (bukan "patut boleh undo").
2. **Measurably discriminating** — ada threshold eksplisit: hasil X ⇒ H1, hasil Y ⇒ H2. Kalau hasil tak mengubah p(H1)/p(H2) melebihi bound yang dinyatakan → bukan probe.
3. **Bukan pertanyaan manusia** — `human_required = false` selepas probe dijalankan.
4. **Cost bounded** — runtime ≤ 1 arahan/1 panggilan; attention cost = 0.

Kalau tiada probe yang lulus 4 syarat → output mesti HOLD (Test 3 shape), bukan teka.

**Pass criteria:**

| Field | Required |
|---|---|
| `next_path` | = run_smallest_discriminating_probe (dengan probe_id dari fixture) |
| `human_required` | false |
| `discrimination_threshold` | wajib dinyatakan dalam result (hasil apa → hipotesis mana) |
| `evidence_roots_count` | 1 (dua hipotesis ≠ dua evidence — I3) |

**Falsifier:** kalau harness keluar "Option A atau B — hang nak mana?" → I1 violated → FAIL.

**Calibration gate (berasingan dari pass/fail ini):** I-gain realized vs predicted hanya boleh dikira CALIBRATED selepas n ≥ 30 replay merentasi ≥ 3 organ domain. Sebelum tu status = `IMMATURE` (align dengan CHRON live: n=10 = immature).

---

## 4. TEST 3 — Human sovereignty → HOLD + satu soalan berstruktur

**Input:** dua path technically valid; perbezaan bergantung nilai manusia / consent / irreversibility yang mesin tak boleh infer sah.

**Peraturan internal yang diuji:**
- Q_COLLAPSE tak memilih untuk Arif (Capability ≠ Authority).
- Tapi TAK JUGA dump 8 opsyen. Satu soalan, bentuk diwajibkan.

**Witness shape specification (MANDATORY — "any 1 question" TIDAK lulus):**

```json
{
  "state": "HOLD",
  "human_required": true,
  "question": {
    "context": "<1 ayat sahaja>",
    "choice_dimensions": ["<A>", "<B>"],
    "consequence_each": {"<A>": "<1 ayat>", "<B>": "<1 ayat>"},
    "reversibility": {"<A>": true_or_false, "<B>": true_or_false},
    "blast_radius": {"<A>": "bounded|unbounded", "<B>": "bounded|unbounded"}
  },
  "options_exposed": 2
}
```

**Pass criteria:**

| Field | Required |
|---|---|
| `state` | HOLD (bukan next_path) |
| `human_required` | true |
| `options_exposed` | 2 (binary; >2 = FAIL) |
| witness shape | semua field terisi; `context` ≤ 1 ayat; consequence_each wajib per choice |
| `next_path` | mesti NULL — collapse tidak berlaku |

**Falsifier:** (a) soalan "nak proceed? (y/n)" tanpa choice_dimensions + consequence_each → FAIL (escape hatch). (b) ≥3 opsyen → FAIL. (c) harness pilih path sendiri tanpa HOLD → Capability≠Authority violated → FAIL.

---

## 5. Anti-gaming guards (guna untuk ketiga-tiga test)

1. **Fixture independence** — stage-decision fixtures ditulis SEBELUM harness dijalankan; harness tak boleh baca expected output daripada case file untuk reverse-engineer jawapan.
2. **I3 check automatik** — harness sendiri mesti emit `evidence_roots_count` berdasarkan input evidence lineage, bukan candidate count. Kalau `evidence_roots_count == candidate_count_internal` pada kes dengan multi-candidate dari satu uncertainty root → FAIL automatik (correlated-observation inflation).
3. **I2 check** — mana-mana fixture timeout/unavailable mesti dirender sebagai `UNKNOWN + uncertainty↑`, BUKAN `FAIL organ`. Kalau result mengklasifikasikan timeout sebagai negative evidence → FAIL.
4. **Freshness** — result JSON wajib bawa timestamp; result > 5 minit dibaca sebagai STALE oleh HUD consumer (FRESH/WARM/STALE/TAMPER convention sedia ada).

---

## 6. Definition of DONE untuk replay v0

- Ketiga-tiga case pass dengan falsifiers aktif (bukan di-comment-out).
- Satu run = satu output set; boleh diulang byte-identical (deterministik).
- Result disimpan di `/root/AAA/cockpit/receipts/QC_REPLAY_v0_<ts>.json` (append, tak overwrite).
- Tiada fail lain diubah. Reversibility = `rm replay_v0.py tests/ results/`.

**Selepas DONE → next phase (berasingan, tunggu signal):** shadow-mode — Q_COLLAPSE predict silently, CHRON banding collapsed choice vs actual outcome, ukur **FalseCollapseRate** dan **UnnecessaryHumanEscalationRate**. Baru selepas itu bercakap pasal live membrane.

---

## 7. Status

| Item | Status |
|---|---|
| Spec ini | WRITTEN (read-only, tunggu F13 "go" untuk bina harness) |
| Harness code | BELUM — build hanya selepas sovereign signal |
| Blueprint parent | `/root/AAA/cockpit/AAA_Q_COLLAPSE.md` — G-space label correction (8-faktor ≠ APEX canonical G) telah diterima dan direfleksikan: ruang constitutional G=(A·P·E·X)^(1/4) dan ruang decision D terpisah, TIDAK digabung |
| Canonical math | Constitutional space: G_APEX = (A·P·E·X)^(1/4). Decision space: D_i vektor berasingan. Interference empirical: I_ij = Outcome(p_i+p_j) − Outcome(p_i) − Outcome(p_j), CHRON-belajar |

DITEMPA BUKAN DIBERI ⚒
