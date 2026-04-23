# Floor Wiring Map
**Epoch:** 2026-04-23T15:36+08 | **Commit:** b906c68 | **Pipeline:** 000-INIT → 888-JUDGE
**Scope:** `core/` + `integrations/arifos/` | **Tool:** grep -R "F0\|F1\|F2\|F9\|F10\|F13\|SEAL\|HOLD\|VOID\|VERDICT\|CAUTION\|SABAR\|COMPLY"

---

## 1. Verdict Codes — Wired vs Doc-Only

| Verdict | Defined In | Wired In Code | Notes |
|---------|-----------|---------------|-------|
| **SEAL** | `integrations/arifos/contract.yaml` | ❌ doc-only | Referenced as arifOS 999 stage authority; no `enum` or class in Python |
| **HOLD** | `integrations/arifos/contract.yaml` | ❌ doc-only | AAA holds message ingress in README §3; no runtime gate in Python |
| **PARTIAL** | `integrations/arifos/contract.yaml` | ❌ doc-only | Listed in accepted_verdicts; no Python constant |
| **CAUTION** | `integrations/arifos/contract.yaml` | ❌ doc-only | In accepted_verdicts; no Python constant |
| **VOID** | `integrations/arifos/contract.yaml` | ❌ doc-only | In accepted_verdicts; no Python constant |
| **COMPLY** | (not in canon) | n/a | Not a canonical verdict — treat as non-existent |
| **SABAR** | (not in canon) | n/a | Not a canonical verdict — treat as non-existent |

**Verdict count: governance in docs = 5, governance in code = 0**

---

## 2. Constitutional Floors — Wired vs Doc-Only

| Floor | Name | Defined In Docs | Referenced In Code | Status |
|-------|------|-----------------|--------------------|--------|
| F0 | — | *(not enumerated in README; F1-F13 declared in contract.yaml)* | ❌ not found | **MISSING — not defined** |
| F1 | Amanah (Trust/Accuracy) | `README.md` §Constitutional alignment; `skills/arifOS-sense/references/floors.md` | ✅ `kernel_loop_interface.py::ConstitutionalHooks.pre_loop_system_prompt()` — injected as system prompt string; `kernel_loop_v1.json::constitutional_pre_loop` | **PARTIAL — string injection, no runtime check** |
| F2 | Truth (Accuracy of docs) | `README.md` §Constitutional alignment | ❌ not found in code | **DOC-ONLY** |
| F3 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Hidayat — Guidance/Clarity) | ❌ not found | **DOC-ONLY** |
| F4 | Psi / Keterbukaan (Transparency) | `skills/arifOS-sense/references/floors.md` | ✅ `kernel_loop_interface.py::ConstitutionalHooks.pre_loop_system_prompt()` — injected as string | **PARTIAL — string injection, no runtime check** |
| F5 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Kesederhanaan — Simplicity) | ❌ not found | **DOC-ONLY** |
| F6 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Kebijaksanaan — Wisdom) | ❌ not found | **DOC-ONLY** |
| F7 | Omega / Keadilan (Humility/Justice) | `skills/arifOS-sense/references/floors.md` | ✅ `kernel_loop_interface.py::Constitutional_pre_loop`; `kernel_loop_v1.json::constitutional_pre_loop` | **PARTIAL — string injection, no runtime check** |
| F8 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Pertanggungjawaban — Accountability) | ❌ not found | **DOC-ONLY** |
| F9 | Anti-Hantu (No dark patterns) | `README.md` §Constitutional alignment | ✅ `kernel_loop_v1.json::constitutional_pre_loop`; `integrations/arifos/contract.yaml` | **PARTIAL — in pre_loop spec, not enforced** |
| F10 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Kelayakan — Viability) | ❌ not found | **DOC-ONLY** |
| F11 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Kemandirian — Independence) | ❌ not found | **DOC-ONLY** |
| F12 | *(not named in README)* | `skills/arifOS-sense/references/floors.md` (Kesatuan — Unity) | ❌ not found | **DOC-ONLY** |
| F13 | Sovereign (Human authority final) | `README.md` §Constitutional alignment; `contract.yaml` | ❌ not found in Python code | **DOC-ONLY** |

**Floor count: defined in docs = 13 (F1-F13), found in code = 3 (F1, F4, F7 as string injection only)**
**Runtime enforcement: 0 / 13 floors have actual runtime checks**

---

## 3. Key Findings

### Finding 1: `floors.py` is Doc-Only Ghost Reference
`core/kernel/README.md` references `core/shared/floors.py` as the single enforcement module. **This file does not exist in the repo.** It is a planned module, not an implemented one.

### Finding 2: `ConstitutionalHooks` is String Injection Only
`kernel_loop_interface.py::ConstitutionalHooks` has:
- `pre_loop_system_prompt()` — injects F1/F4/F7 as plain strings into system prompt
- `post_git_check()` — regex strip only, no Floor evaluation
- `bash_security_check()` — **stub returning `{"passed": True}`**, not implemented

This is pre-loop linting, not Floor enforcement. Floors are advisory strings, not runtime gates.

### Finding 3: Verdict `enum` Does Not Exist in Python
`integrations/arifos/contract.yaml` lists accepted verdicts (SEAL, HOLD, PARTIAL, CAUTION, VOID) but there is no Python `enum Verdict` anywhere in `core/` or `integrations/arifos/`. The verdicts are governance declarations, not enforced types.

### Finding 4: `kernel_loop_v1.json` Constitutional Pre-Loop Is Spec, Not Code
`constitutional_pre_loop.system_prompt_injection` lists F1, F4, F7, truth_power_coupling. This is architecture spec. The implementation in `kernel_loop_interface.py` is a skeleton with `NotImplementedError` on `_execute_tool()`.

### Finding 5: VAULT999 / 888_JUDGE Are Named But Not Implemented
`contract.yaml` says:
- "arifOS owns 888 JUDGE and 999 SEAL"
- "VAULT999 is the only final ledger"
- "If VAULT999 has no seal reference, AAA must treat the action as HOLD"

But `auditor_handle` in `KernelLoop.__init__()` defaults to `None`. The auditor is a placeholder slot, not a wired implementation.

---

## 4. Summary Count

| Category | Count |
|----------|-------|
| Governance defined in docs (Floors F1-F13 + 5 verdicts) | 18 |
| Governance wired in runtime code (string injection, stub, or placeholder) | 3 Floor references + 0 Verdict enums |
| Actual runtime Floor enforcement (executable checks) | **0** |
| Planned-but-missing files (`floors.py`, `auditor_handle`) | 2 |

**→ Governance in docs only: 15 | Governance in code: 0 | Gap ratio: 100%**

---

## 5. Recommended Actions (ranked)

| Priority | Action | Floor(s) Addressed | Effort |
|----------|--------|--------------------|--------|
| **P0** | Create `arifos/verdict.py` with `enum Verdict { SEAL, HOLD, PARTIAL, CAUTION, VOID }` — single source of truth, importable by all modules | All | Trivial |
| **P0** | Wire `auditor_handle` in `KernelLoop.__init__()` — even a stub that logs to VAULT999 on CONSTITUTIONAL_VIOLATION events | F8, F13 | Low |
| **P1** | Implement `arifos/floors.py` — `check_floor(tool_name, floor_level) → Verdict` — single enforcement gate | F1-F13 | High |
| **P1** | Replace `bash_security_check()` stub with actual 23-point check | F9 | Medium |
| **P2** | Promote F1/F4/F7 from string injection to runtime hooks in `ConstitutionalHooks` | F1, F4, F7 | Medium |
| **P2** | Add `F0` enumeration (if F0 = Delta/Entropy gate) — clarify what F0 is before implementing | F0 | Low |
| **P3** | `core/kernel/README.md` — remove `core/shared/floors.py` reference until file exists — removes ghost reference | F4 | Trivial |

---

## 6. Canonical Sources

| Source | What It Defines |
|--------|-----------------|
| `README.md` §Constitutional alignment | F1 Amanah, F2 Truth, F9 Anti-Hantu, F13 Sovereign |
| `skills/arifOS-sense/references/floors.md` | Full F1-F13 definitions with Malay names and epistemic rules |
| `integrations/arifos/contract.yaml` | 5 verdict codes; 000-999 pipeline authority; VAULT999 requirements |
| `core/kernel/kernel_loop_v1.json` | constitutional_pre_loop spec (F1/F4/F7/F9 in system prompt); tool tiers |
| `core/kernel/kernel_loop_interface.py` | ConstitutionalHooks (string injection + stub); ToolPolicyEngine (risk tiers); LoopEvent.CONSTITUTIONAL_VIOLATION (event emitted) |
| `core/kernel/README.md` | References `core/shared/floors.py` — **does not exist** |

---

*DITEMPA BUKAN DIBERI — 888-JUDGE ratified | 999 SEAL pending | Epoch 2026-04-23*
