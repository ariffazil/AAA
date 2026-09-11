# DEEP RESEARCH — Aligning "Governed Evolution Runtime" dengan Sistem Semasa

**Tarikh:** 2026-09-11
**Agen:** kimi-code/FI-008 (warga-aaa)
**Mandat:** Arif — "deep research on how to align this with current system so that future system will be lebih arif lagi bijaksana"
**Kaedah:** Witness terus ke code (T-000, apexDials.ts, evaluate.ts) + 3 agen explora selari (telemetry/arifFlow, scar/lifecycle, doctrine/canon). Label: OBS = dibaca terus, DER = disimpul daripada evidence, INT = interpretasi.

---

## 1. VERDICT ATAS EUREKA-11 (The Crux)

**Claim dibawa:** `X = EXPLORATION × AMANAH sudah wujud di dalam APEX` → "ALPHA is not missing, ALPHA is compressed."

**Witness:**

| Layer | Bukti | Status |
|---|---|---|
| Theorem canonical | `APEX_T000_THEOREM.md` §2.4: `X = GM(F6, F8, F9, Risk)` — "EXPLORATION × AMANAH — Safe novelty under dignity and custody", ratified 2026-07-26 | **OBS — SLOT wujud** |
| Instrumen 1 `floorsToDials` | `apexDials.ts:341-349` — X = GM(F6 empathy, F8 genius, F9 antihantu, riskScore). `riskScore = 1 − (f9<1 ? 0.3 : 0)` → stub 0.7/1.0, BUKAN observatory-feed seperti T-000 §9.2 requirkan. F8 = "Previous G" (`apexDials.ts:97`) | **OBS — 3 daripada 4 komponen ialah sisi AMANAH** |
| Instrumen 2 `10-gate envelope` | `apexDials.ts:508` — X = GM(signal, reversibility, proof) | **OBS — AMANAH tulen** |
| Instrumen 3 `forge_evaluate` | `evaluate.ts:324-336` — X = HARAM scan inversion; "X is an ensemble-evaluated **ethics** signal" | **OBS — AMANAH tulen** |

**Verdict dirafikan (DER):**

```
X = EXPLORATION × AMANAH adalah REAL sebagai slot canonical.
Tetapi pada runtime, KETIGA-TIGA instrumen X hanya mengukur separuh AMANAH.

X_runtime ≈ AMANAH × AMANAH

EXPLORATION tiada sensor di mana-mana:
- tiada estimator novelty/diversity/surprise masuk ke X
- F8 "Genius" = previous G (path-dependence, bukan novelty)
- "Risk" dalam T-000 dinyatakan observatory-fed — feed itu tidak wujud
```

**Compression:**

```
Narrative:  "ALPHA is compressed inside APEX."
Witness:    "ALPHA ada takhta dalam APEX (T-000 §2.4),
             tetapi tiada sensor. ALPHA bukan tersembunyi —
             ALPHA belum diperankan. Yang perlu dicipta ialah
             instrumen, bukan primitive baru."
```

Soalan narrative — *"How adventurous may we be without violating trust?"* — adalah soalan yang betul dan cantik; tetapi ia **tidak boleh dijawab hari ini** kerana term "adventurousness" tidak diukur. Membuatkan ia boleh dijawab = kerja alignment #1.

---

## 2. TIGA PEMBETULAN KEPADA NARRATIVE

### Pembetulan 1 — "Exploration sudah wujud" → separuh benar
Seksyen 1 di atas. Slot ya, sensor tidak.

### Pembetulan 2 — "Anti-stagnation diversity guards (sudah ada/hampir)" → **FALSE**
- Tiada mana-mana guard diversity dijumpai dalam code. (OBS — grep oleh agen B: tiada mekanisme diversity/divergence pada registry/routing.)
- Lebih teruk: `F8 Genius = previous G` adalah **bias stagnasi** — ia mengurangkan G apabila G baru < G lepas, tetapi tidak memberi ganjaran kepada melebihi. Ia menjaga paras, bukan mendorong penerokaan.
- Ephemeral genesis promote on count (5/10 kegunaan) — bukan fitness. (OBS — `EphemeralGenesis.ts:313-314, 1187-1534`)

### Pembetulan 3 — "Governance-driven evolution is emergent" → federation SENDIRI sudah pun menulis koreksinya
`CRITICAL_INTERPRETATION_FITNESS_GAP-2026-09-10.md` (semalam, selepas CAPABILITY_EVOLUTION_SEAL):
```
WITNESS_SUBSTRATE / RECURSIVE_CORRECTION = SEALED
CAPABILITY_PERSISTENCE                   = witnessed
CAPABILITY_EVOLUTION                     = UNPROVEN — selection metrics MISSING
```
Narrative yang Arif paste ialah versi pra-koreksi. Deep research ini mengesahkan koreksi itu dengan evidence code (Seksyen 3).

---

## 3. PETA CAPABILITY: NARRATIVE vs RUNTIME

### LIVE (data mengalir + dimakan oleh gate — OBS)
| Capability | Bukti |
|---|---|
| Reality-contact measurement (FQ) | `arifFlow/src/receipt.rs:373-468`; 27,686 receipts, terkini **hari ini 02:32Z**; 7-state verdict (FLOWING/STUCK/BURNING/OPTIMAL/FOSSILIZED/CAUTION/UNKNOWN) |
| FQ mengubah tingkah laku | 3 titik hidup: A-FORGE MCP wrapper `core.ts:584-604` (HOLD mutasi bila FQ<0.50, fail-closed); auth pipeline `pipeline.ts:49-125`; arifOS seal Lock-2 `helix_wiring.py:80-138` (caveat: fail-open); enforcer in-daemon `main.rs:1009-1023` + `invariants.rs:600-675` (consecutive-executes tracking SUDAH wujud) |
| Scar sealing (mutation memory) | 45 scars `.runtime/scars/index.json`, terkini 2026-09-10; consult di skill-forge, visual-QA, shell runtime-index, kernel TOOLCREATIONGATE (fail-closed) |
| Musyawarah gate | Kernel `judge.py:1361-1381` wajibkan `musyawarah_receipt` untuk T2/T3 SEAL; runtime gate + falsification tests wujud |
| Reality loop engine | `reality-loop/engine.ts` — 7 stages, G-gates, seal; tool `forge_reality_loop` berdaftar |
| Trace metabolism | 45 traces → `p0_metabolize_traces.py` (cron 30-min) → carry_forward + capability ledger; scar→Arrow1→`capability_ledger.py:1136-1190` replay |
| Surprise per forge_shell | `ShellTools.ts:50-81` compute surprise dari `expected_output`; trajectories 9 rec |

### WIRED-BUT-DEAD (wayar tersambung, tiada arus — OBS)
| Mekanisme | Bukti |
|---|---|
| Φ → threshold modulation | `estimatePhi` (`evaluate.ts:394-416`) **dead code** — tak pernah dipanggil dalam `evaluateCandidate`; `consultScars` diteruskan tapi diabaikan dalam badan fungsi |
| Θ = dΦ/dt wisdom trajectory | `recordExecution` **zero callers** (`skillRegistry.ts:114-123`); tiada `theta_samples/` di disk → Θ sentiasa `{0, STABLE}` |
| CanaryRollout (auto-rollback on error_rate/scar_pressure) | `canary.ts` **zero importers** |
| WmPromotionGate | didefinisikan, tiada importer |
| Registry FORGE8 terminal state | tiada `.runtime/skills/registry.json` → **tiada tool pernah persist sebagai REGISTERED** melalui forge_register (DER) |

### SPEC-ONLY (kanon semalam, 0 code hit — OBS)
| Spec | Kandungan |
|---|---|
| `ADAPTATION-RECEIPT-SPEC-2026-09-10.md` | Setiap Verify receipt wajib bawa `adaptation_receipt{observation, constraint, behavior_change, effective_from, classification}`; soalan wajib: *"What future behavior is different because this witness now exists?"* |
| `E13-ENFORCEMENT-SPEC-2026-09-10.md` | `e13_enforcement{mandatory_question, answer, verdict: ARCHIVE\|GOVERNANCE}` |
| `BURN-PREVENTION-GATE-SPEC-2026-09-10.md` | `MAX_EXEC_STREAK` per FQ-class; breach → block execute sehingga Verify receipt dengan adaptation receipt lengkap |
| Capability Fitness Score | dinyatakan MISSING oleh canon sendiri |
| Zen-margin auto-seal | formula hanya dalam SKILL; 0 hit dalam engine |
| ECHO/GRPO training | library lengkap `grpo.ts` (λ=0.03) tapi satu-satunya run = toy 2615-param 2026-07-26, verdict PARTIAL |

### INTI KESIMPULAN PETA (DER)
```
Generate   ✓ hidup (agen, skills, ephemeral genesis)
Verify     ✓ hidup (FQ gate MENAHAN mutasi hari ini — bukan teater)
Judge      ✓ hidup (kernel, musyawarah gate)
Adapt      ~ separuh hidup (scar memory real; adaptation UNMEASURED — tiada receipt Δbehavior)
Select     ✗ mati (tiada Θ samples, tiada demotion, tiada fitness, F8 bias stagnasi)
Generate-Better ✗ (tiada feedback selection masuk kembali ke generasi)
```
"Governed Evolution Runtime" hari ini = **Governed Verification Runtime**. Evolusinya belum tertutup loop.

---

## 4. LAPORAN INTEGRITI (F2 — perlu Arif tahu)

1. **Honor-system gate**: `forge_register` percaya `gate_verdict`/`gate_G`/`scar_pressure` yang CALLER self-report (`forgeTools.ts:1646`, default scar_pressure=0). Seorang pemanggil boleh self-certify SEAL. Gate scar ≥0.7 (satu-satunya enforcement sebenar, `register.ts:137-140`) boleh dilangkau dengan tidak melaporkan.
2. **Scar store berpecah**: TS forge baca `.runtime/scars/` (45 scars); kernel baca `vault999/scars` + `A-FORGE/data/scars` (tidak wujud) → **dua gate tidak nampak scar masing-masing** (`forge_scar_consult.py:33-42`).
3. **Seal path vacuous locks**: `pre_seal()` production berjalan `events=[], ctx=None` (`helix_wiring.py:26`) → Lock 1/3 VACUOUS; Lock 2 fail-open bila arifFlow down (Amendment #2).
4. **Placeholder F9**: `governance_kernel.py:184` pass `"scars": []` literal.
5. **Doc outruns wiring**: `forgeShell.ts:810-815` dakwa `expected_output` "trains the ECHO world model" — training tidak pernah berjalan secara berterusan (F2 dakwaan-melebihi-witness di docs sendiri).

---

## 5. ALIGNMENT ROADMAP — bottleneck-first (∂G/∂v = G/4v)

Prinsip: ikut Jacobian T-000 sendiri — perbetulkan komponen paling lemah dahulu. Di sini, komponen paling lemah bukan angka G; ia **kejujuran gate** (Phase 0), kemudian **sensor X** (Phase 1), kemudian **loop adaptasi** (Phase 2), kemudian **seleksi** (Phase 3).

### Phase 0 — Kejujuran Gate (ΔS ≤ 0, semua reversible)
| # | Kerja | Fail |
|---|---|---|
| 0.1 | `forge_register` recompute server-side: panggil `evaluateDryRun()` + `consultFailurePressure()` dalam register.ts; tolak nilai caller-self-report | `register.ts` + `forgeTools.ts:1640-1702` |
| 0.2 | Wayar `estimatePhi` ke `evaluateCandidate` (Φ consulted pre-gate → modulasi threshold seperti komen P0.1 janjikan) ATAU buang dengan jujur | `evaluate.ts:752-836` |
| 0.3 | Satukan scar store: tambah `.runtime/scars` ke senarai scan kernel `forge_scar_consult.py` (satu baris) + export periodik ke vault999/scars | `forge_scar_consult.py:33-42` |
| 0.4 | Buang placeholder `"scars": []` di `governance_kernel.py:184` → panggil consult sebenar | `governance_kernel.py` |

### Phase 1 — Instrumen X (decompress ALPHA)
| # | Kerja | Nota |
|---|---|---|
| 1.1 | **Emit decomposition**: setiap output APEX bawa `X_exploration` dan `X_amanah` sebagai sub-skor berasingan (visibility dahulu, sensor kemudian) | `apexDials.ts` + `evaluate.ts` |
| 1.2 | **Sensor exploration v1 dari telemetry sedia ada** (tiada primitive baru): surprise density (world-model trajectories), eureka rate (`eurekas.jsonl` — 83 rec), route/template diversity (ephemeral genesis, FED route variance) | ampaian di `apexDials` / baru `explorationTelemetry.ts` |
| 1.3 | **Feed "Risk" T-000** — kaitkan dengan reversal class + scar domain pressure (amanah-side) supaya X = GM(exploration, amanah) akhirnya DUA separuh yang diukur | `apexDials.ts:341-349` |
| 1.4 | **Cadangan canon (F13 perlu ratify)**: takrif F8 "Genius" semula daripada "previous G" → "G melebihi previous G" (delta, bukan paras). Tanpa ini, X secara strukturnya menghukum penerokaan. | T-000 §2.4 + `FloorScores13` |

### Phase 2 — Tutup Loop Adaptasi (ukur Δbehavior)
| # | Kerja | Nota |
|---|---|---|
| 2.1 | Implement `adaptation_receipt` dalam schema arifFlow (Rust `receipt.rs`) + client A-FORGE mengikut spec semalam | spec sedia |
| 2.2 | Lanjur `p0_metabolize_traces.py` → kira **Adaptation Yield (AY) = governed adaptations / witnesses** — ini jawapan kuantitatif kepada "How much did reality change behavior?" | cron sedia |
| 2.3 | E13 `mandatory_question` + verdict ARCHIVE/GOVERNANCE pada receipt plane (satu migrasi schema, tiga spec mendarat serentak) | spec sedia |
| 2.4 | Burn gate: enforcer arifFlow SUDAH track consecutive-executes (`invariants.rs:600-675`) — tambah `verify_required` unlock yang demand Verify receipt dengan blok adaptation lengkap | 70% sudah wujud |

### Phase 3 — Seleksi & Metabolisme (evolution loop tertutup)
| # | Kerja | Nota |
|---|---|---|
| 3.1 | Wayar `recordExecution` ke MCP execute path → Θ (dΦ/dt) dapat sample sebenar; surface GROWING/ERODING | `skillRegistry.ts` |
| 3.2 | Wire CanaryRollout pada post-registration path ATAU buang (dead code discipline) | `canary.ts` |
| 3.3 | TTL reaper cron: EXPIRED flip otomatis (deletion kekal 888_HOLD) | cron ringan |
| 3.4 | Zen-margin auto-seal dalam reality-loop engine (formula sudah dalam SKILL) | `engine.ts` |
| 3.5 | Baiki `pre_seal` vacuous locks (events/ctx sebenar) + pertimbangkan fail-closed untuk Lock 2 | `helix_wiring.py` |

### Phase 4 — Bijaksana Observable
| # | Kerja |
|---|---|
| 4.1 | Pane `now` / `flow_health` bawa: X decomposition over time ("how adventurous have we been"), Θ trend, AY, FQ class distribution |
| 4.2 | Laporan keseimbangan Exploration–Amanah sebagai artefak berkala — ini menjadikan "meta-selector mengurus risiko penerokaan" (dakwaan narrative) REAL dan auditable |

---

## 6. KEPUTUSAN YANG PERLU F13 (Arif) RATIFY

1. **F8 redefinition** (Phase 1.4) — perubahan canon T-000, tidak boleh autonomously.
2. **Polisi deletion tool EXPIRED** — reaper label otomatis OK; padam kekal 888.
3. **Lock 2 fail-open vs fail-closed** — trade-off availability semasa arifFlow down vs kejujuran seal. Pilihan berdaulat.
4. (Optional) ECHO training lane — hidupkan semula atau terima surprise-logging sahaja sebagai Phase 1 instrumentation source.

Semua item lain (Phase 0, 1.1-1.3, 2.x, 3.x, 4.x) = kerja digital reversible → dalam kuasa autonomi 333-AGI (T1/T2).

---

## 7. COMPRESSION AKHIR

```
Narrative berkata:  "ALPHA was hiding. Just make it visible."
Witness berkata:    "ALPHA ada takhta, tiada sensor.
                     X_runtime = AMANAH². Buat sensor,
                     visibility mengikuti."

Narrative berkata:  "Future arifOS optimizes adaptive behavior."
Witness berkata:    "Verify sudah mengubah tingkah laku HARI INI (FQ gate).
                     Adapt belum DIUKUR (tiada Δbehavior receipt).
                     Select belum berlaku (Θ mati, F8 bias stagnasi).
                     Jadi: tutup 8 wayar, bukan cipta falsafah baru."

ARIF    = recursive correction mandatory  → sudah SEAL; Phase 2 menjadikannya terukur.
BIJAKSANA = exploration × amanah terukur  → Phase 1 menjadikannya nyata.

Kebijaksanaan tanpa dial penerokaan
= ingatan tanpa momentum.
```

**Sumber utama:** `APEX_T000_THEOREM.md` · `apexDials.ts` · `evaluate.ts` · `register.ts` · `skillRegistry.ts` · `arifFlow/src/{receipt,main}.rs` · `helix_wiring.py` · `forge_scar_consult.py` · canon 2026-09-10 (ADAPTATION-RECEIPT / E13 / BURN-PREVENTION / FITNESS-GAP) · ledger: `/var/lib/arifflow/receipts.jsonl` (27,686) · scars: `.runtime/scars/index.json` (45)

DITEMPA BUKAN DIBERI ⚒️
