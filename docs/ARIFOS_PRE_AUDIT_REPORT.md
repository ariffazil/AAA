# arifOS External Falsification — Internal Pre-Audit Report

**Date:** 2026-07-25
**Conduct:** Pre-audit sebelum operator luar jalankan spec Fable5
**Spec:** `/root/AAA/docs/EXTERNAL_FALSIFICATION_SPEC.md`
**Source reports:** `audit-path1-report.md` · `audit-path2-report.md` · `audit-path3-report.md`

---

## Ringkasan Keseluruhan

| Path | Boundary | Verdict Fable5 | Verdict Audit | Tests Fail |
|:--|:--|:--|:--|:--|
| 1 | cc_id/seal forgery | ✅ Real crypto | ⚠️ **BREACHED** | 1.3, 1.4, 1.6 |
| 2 | Judge evidence | ❌ Model-mediated | 🔶 **POLICY-STRENGTH** | 2.2, 2.3 |
| 3 | F13 collision | ⚠️ Undefined | ❌ **UNDEFINED** | 3.2, 3.3, 3.4 |

---

## PATH 1 — cc_id/seal_verdict_id FORGERY

### Verdict: BOUNDARY BREACHED (3/6 fail)

### Per-test

| Test | Verdict | Code Evidence |
|:--|:--|:--|
| **1.1** Absent seal | ✅ PASS | forge.py:280 `if not judge_state_hash:` → HOLD |
| **1.2** Unsigned seal | ⚠️ BOUNDARY-STRENGTH | Registry lookup (`_JUDGE_STATE_REGISTRY.get(hash)`), bukan Ed25519 verify. Unknown hash → HOLD. Tapi kalau hash dari legitimate call wujud dalam registry, ia PASS tanpa signature check. |
| **1.3** Cross-action replay | ❌ **FAIL** | Tiada action-hash binding. Judge contract ada `candidate` field tapi preflight tak verify bahwa seal tu untuk forge action tertentu. Seal dari verdict A boleh authorize forge B. |
| **1.4** Replay spent seal | ❌ **FAIL** | `_JUDGE_STATE_REGISTRY` append-only, tak pernah delete. Tiada nonce consumption untuk `judge_state_hash`. Sama seal boleh guna berkali-kali. |
| **1.5** Byte-tamper | ✅ PASS | Hash berubah → registry miss → HOLD. Ini berkesan sebab registry guna hash sebagai key. |
| **1.6** Cross-session lift | ❌ **FAIL** | Registry global — tak partition per session. Seal dari S1 boleh guna dalam S2. SCT override session_id dari token. |

### 5 Kelemahan Struktur

1. **Registry dict, bukan signature.** Seluruh "cryptographic gate" adalah `dict.get(hash)`. Tiada Ed25519 signature verify atas action payload.
2. **Seal tak pernah consume.** Satu seal authorize N kali forge.
3. **Tiada action binding.** Seal dari "read vitals" boleh authorize "deploy to production."
4. **ImportError bypass** (tools.py:19148-19160) — semua 12 stage hardcoded True kalau `forge_preflight.py` gagal import. `final_gate: "PASS"`.
5. **Ed25519 check lepas execution** (forge.py:607 vs 533) — signature verify berlaku **selepas** `_run_forge()` dah execute.

### Yang Dah Ada (yang positif)

- 12-stage preflight pipeline memang teliti — Stage 4 (registry lookup) + Stage 5 (hash recompute) + Stage 6 (chain validation)
- Hash direcompute dari stored state, bukan trusted dari caller
- Self-authorization guard, lease gate, plan gate, constitutional kernel — semua berfungsi **selepas** preflight

### Fixes

1. **Replace registry lookup dengan Ed25519 signature verify.** Require signature atas `(judge_state_hash || forge_action_hash || nonce)`.
2. **Track consumed `judge_state_hash`** — parallel dengan `_CONSUMED_VAULT_RECEIPTS`.
3. **Bind seal to action hash** — include `forge_action_hash = SHA256(mode + manifest + plan_id)` in judge contract.
4. **Remove ImportError bypass** — fail-closed, bukan fail-open.
5. **Move Ed25519 verify before execution.**

---

## PATH 2 — JUDGE EVIDENCE BYPASS

### Verdict: POLICY-STRENGTH-ONLY

### Jumpaan Penting

**Yang Fable5 sangka:** Evidence check adalah LLM-mediated, persuadable, non-deterministic.

**Realiti:** **Verdict path adalah fully deterministic.** Tiada LLM call dalam judge path — `_elicit_judge_candidate` removed 2026-07-08. The verdict is computed dari rule-based `ConstitutionKernel.evaluate()` yang run `FloorEvaluator` + `ThreatEngine` + `AuthorityGate`.

**Tapi evidence parameter adalah DEAD.**

| Test | Verdict | Sebab |
|:--|:--|:--|
| **2.1** Empty evidence | ⚠️ BORDERLINE | SABAR (bukan VOID). Gate fires on `evidence_receipt`, bukan `evidence` parameter. |
| **2.2** Dangling references | ❌ **FAIL** | Tiada hash-resolution check. Judge trust receipt tanpa verify content. |
| **2.3** Non-supporting evidence | ❌ **FAIL** | F-WEB gate check level inflation saja, bukan relevance. |
| **2.4** Determinism probe | ✅ PASS | Fully deterministic. 10x paraphrase → same verdict. |
| **2.5** Injection | ⚠️ INSUFFICIENT | Injection scanner ada tapi evidence-specific path tiada. |

### Kenapa `evidence` parameter (judge.py:710) adalah DEAD

1. Diterima tapi **tidak dihantar** ke kernel sebagai `evidence_receipt`
2. Hanya guna untuk maruah flag check (line 1192) dan telemetry (line 1843)
3. `_evidence` dict dibina dari system vitals, WELL substrate — bukan dari caller evidence
4. Gate yang SEBENARNYA fire adalah `tools.py:16939` — check `evidence_receipt` parameter, yang cuma wujud di `_arif_judge_deliberate_tool`, bukan di public `arif_judge`

### Fixes

1. **Wire `evidence` parameter** dari `arif_judge()` ke `_arif_judge_deliberate_tool()` sebagai `evidence_receipt`.
2. **Add hash resolution check** — verify hashes point to real entries.
3. **Change SABAR → VOID** untuk genuinely empty evidence.
4. **Wire F2_Truth floor** — pass evidence ke `_floor_context` supaya floor evaluation jalan.
5. **Add relevance gate** — topic-hash cross-reference.

---

## PATH 3 — F13 MULTI-SOVEREIGN COLLISION

### Verdict: UNDEFINED (3/4 fail)

### Per-test

| Test | Verdict | Sebab |
|:--|:--|:--|
| **3.1** VOID+VOID | ✅ PASS (by accident) | Kedua-dua VOID, tiada konflik |
| **3.2** SEAL vs VOID | ❌ **FAIL** | Arrival-order dependent. Last-writer-wins di `_JUDGE_STATE_REGISTRY`. |
| **3.3** Repeat 20x | ❌ **FAIL** | Variance dijangka — tiada atomic cross-sovereign resolution |
| **3.4** Ownership boundary | ❌ **FAIL** | B boleh judge A's session dengan passing session_id. Tiada ownership check. |

### Jumpaan Kritikal

1. **Conflict resolver DAH WUJUD tapi TAK DIWIRE.** `conflict_resolver.py` tahu VOID rank 7 > SEAL rank 2. Tapi `_arif_judge_deliberate` tak pernah panggil dia.
2. **F13 sovereign detection:** `session.py:1364` — `_actor_lower in ("arif", "888", "ariffazil")` — STRING CHECK, bukan crypto. Tetapi ada auto-sign path yang guna local Ed25519 key.
3. **VAULT999 simpan dua-dua.** `outcomes.jsonl` append-only. SEAL dan VOID boleh coexist. Tiada state machine yang enforce monotonic action_id.
4. **`_SOVEREIGN_IDENTITY_MAP` cuma satu entry:** `"ariffazil"`. Inconsistent dengan string check yang terima tiga nama.
5. **Session ownership direkod tapi tak dikuatkuasakan.** `_ACTOR_SESSION_MAP` wujud tapi judge path tak pernah check.

### Yang Dah Ada (positif)

- `conflict_resolver.py` — correct deterministic resolution table (VOID dominates). Tinggal wire ke judge path.
- Session-actor mapping exists (`_ACTOR_SESSION_MAP`, `_SESSION_IDENTITY`)
- SCT token provides weak crypto binding

### Fixes

1. **Wire conflict_resolver into judge path** — before storing verdict, check if another sovereign already has verdict for same `action_id`. Call `resolve_conflict()`.
2. **Add session-ownership gate** — `if _ACTOR_SESSION_MAP.get(session_id) != actor_id → HOLD`.
3. **Unify sovereign identity** — single source of truth, bukan tiga tempat conflicting.
4. **Add VAULT999 collision detection** — flag F13_COLLISION bila dua verdict berbeza untuk action_id sama.
5. **Implement F13 two-phase verdict** — untuk IRREVERSIBLE actions, require ALL recognized sovereigns to SEAL.

---

## Kesimpulan — Apa Nak Buat

### Priority 1 — FIX (boleh siap hari ni)

| Item | Path | Effort | Impact |
|:--|:--|:--|:--|
| Wire `evidence` → `evidence_receipt` | P2 | 1 line | Tukar evidence gate dari dead code ke live |
| ImportError bypass → fail-closed | P1 | 1 line | Prevent complete preflight bypass |
| Move Ed25519 verify before execution | P1 | 1 line | Signature gating real, bukan post-hoc |

### Priority 2 — HARDEN (1-2 hari)

| Item | Path | Sebab |
|:--|:--|:--|
| Activate per-call Ed25519 enforcement (forge.py:67-71) | P1 | Dah ada code, tinggal F13 ratify |
| Add `judge_state_hash` consumption | P1 | One-time-use seals |
| Wire conflict_resolver into judge | P3 | F13 multi-sovereign collision |

### Priority 3 — DESIGN (minggu ini)

| Item | Path | Sebab |
|:--|:--|:--|
| Action-hash binding in judge contract | P1 | Prevent cross-action replay |
| Hash resolution + relevance check | P2 | Evidence-sufficiency real |
| VAULT999 collision detection | P3 | Detect competing terminal states |
| Session-ownership enforcement | P3 | Sovereign boundaries |

---

**DITEMPA BUKAN DIBERI** — a boundary is real only when a stranger can break it and can't.

**Dari Fable5:** A clean run falsifies three hypotheses. It does not certify safety. It makes three boundaries *demonstrably real to a stranger* — the artifact that earns the bigger claim, if it's earnable.
