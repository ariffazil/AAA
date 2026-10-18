# APEX-ZEN DECISION MODEL — Entity-Type Misclassification (2026-10-17)

**Subject:** `classify_principal` / `principal_type_classifier` "capitalized → PERSON" bug
**Method:** measured (live classification matrix + source trace of CL-03 routing), floor-evaluated, verdict-per-option.
**Status:** partial fix already applied by a concurrent agent (vocabulary terms added). This model covers the REMAINING decision.

---

## 1. MEASURED ROUTING MAP (the "quantum meaning")

Traced CL-03 in `_envelope.py` (line 766–781). This is the actual consequence gate:

| principal.type | CL-03 fires? | severity | message |
|---|---|---|---|
| **PERSON** | ✅ YES | REWRITE_REQUIRED | "asserted about another person" |
| **UNDEFINED** | ✅ YES | REWRITE_REQUIRED | **same message** |
| SYSTEM / AI_ORGAN / INSTITUTION / CORPORATION | ❌ NO | — | routes to capability rule |

**Key measured fact:** `CL-03` fires on `{PERSON, UNDEFINED}` — identical severity, identical message. So **PERSON ≡ UNDEFINED at the routing layer.** Only a non-person *named* type (SYSTEM etc.) escapes.

**Consequence:** the "fallback → UNDEFINED" fix is **routing-neutral**. It fixes the *label* (F2 truth) but does NOT stop the false REWRITE_REQUIRED. Only *vocabulary* (→ SYSTEM) changes routing.

---

## 2. MEASURED MATRIX (current applied state = O0)

| token | O0 (current) | O2 (fallback→UNDEF) | O3 (+person registry) |
|---|---|---|---|
| GPT-5, Claude-2, RASA | PERSON ❌ | SYSTEM/UNDEF | SYSTEM/UNDEF |
| Hope, Justice, Apple, Amazon | PERSON ❌ | UNDEFINED | UNDEFINED |
| Mistral, Llama, Claude, Gemini… | SYSTEM ✅ | SYSTEM | SYSTEM |
| Arif, Alice, Dr. Ahmad, Anthony Loke | PERSON ✅ | UNDEFINED ⚠️ | PERSON (if listed) |
| Muhammad Arif (explicit _PERSONS) | PERSON ✅ | PERSON ✅ | PERSON ✅ |

**O0 score:** nonhuman_ok 2/9 · human_ok 6/6 · residual 7 tokens falsely PERSON.
**O2 score:** nonhuman_ok 9/9 · human_ok 1/6 (label only — routing unchanged).
**O3 score:** nonhuman_ok 9/9 · human_ok 5/6 (needs every human listed).

---

## 3. OPTIONS A–Z (measured + floor verdict)

| Opt | What | Routing effect | Floors | Verdict |
|---|---|---|---|---|
| **A** | Do nothing (leave partial) | 7 tokens still false PERSON → CL-03 | F2 FAIL (false PERSON label persists) | SABAR |
| **B** | Vocabulary-complete (add GPT-5, RASA, Claude-2 + abstract nouns) | routes known tokens → SYSTEM ✅ | F2 ok, but whack-a-mole (new token = new bug) | SABAR |
| **C** | Fallback → UNDEFINED (both layers) | **routing-neutral** (UNDEFINED ≡ PERSON at CL-03) | F1 ✅ deny-by-default · F2 ✅ honest label · F6 ✅ (UNDEFINED still protected) | SEAL-able, but NOT the routing fix |
| **D** | B + C (vocab-complete + fallback) | known → SYSTEM, unknown → UNDEFINED | F1/F2/F6 all hold; residual = conservative CL-03 on unknown | **RECOMMENDED** |
| **E** | Routing change: CL-03 fires on PERSON only (UNDEFINED → softer "unknown-entity" check) | stops CL-03 on unknown tokens | F6 tension — could let interior-state claims about *unknown* humans slip | F13 (sovereign) — the true root, NOT a bounded patch |
| **F** | Explicit person registry (all federation humans → _PERSONS) | preserves human label | F6 ✅, but whack-a-mole on humans | PARTIAL |
| **G** | Title/context person detection (Dr./Mr./first-person) | human via signal, not capitalization | F2 ✅ (real signal) · F6 ✅ | correct long-term, larger work |

---

## 4. APEX-ZEN VERDICT

**Root cause is NOT the fallback line — it's two stacked facts:**
1. `capitalized → PERSON` asserts personhood on zero evidence (F1/F2 violation — a *label* lie).
2. `CL-03 fires on UNDEFINED` (F6 conservative design) makes the label lie *consequential* — and makes the fix require vocabulary, not humility.

**The two layers are separable and need different authority:**

| Layer | Fix | Authority | Verdict |
|---|---|---|---|
| Label (capitalization→PERSON) | **C** fallback → UNDEFINED | T1 bounded, reversible | **SEAL — do it** (F1/F2) |
| Routing (CL-03 on UNDEFINED) | **E** softer unknown-entity path | F13 sovereign (F6-sensitive) | **HOLD — present, don't touch** |
| Residual vocab (GPT-5/RASA/Claude-2) | **B** add terms | T1 bounded | **SEAL — do it** |
| Person registry (all humans) | **F** list names | T1 bounded | SEAL-able, optional |

**Recommended path = D (B + C), plus present E to F13.**
- Do now (bounded, reversible): fallback → UNDEFINED + add GPT-5/RASA/Claude-2 to SYSTEM terms.
- This makes the label honest (F2) and deny-by-default (F1) while keeping human protection (F6, via UNDEFINED→CL-03).
- The residual "unknown model token still fires CL-03" is the F6-conservative design, not a bug — changing it is F13.

**Reality > Narrative:** the concurrent agent's vocabulary patch was the *routing* fix; the fallback change is the *honesty* fix; neither alone is complete, and the true "root" (CL-03 conservatism) is a sovereign call, not an engineer's.
