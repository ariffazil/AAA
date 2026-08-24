---
name: FORGE-lsp-pre-edit-gate
id: forge-lsp-pre-edit-gate
owner: A-FORGE · 333-AGI
risk_tier: low
floor_scope: [F2, F4, F7, F11]
description: >
  MANDATORY LSP grounding gate BEFORE any code mutation on .ts, .py, .js, .tsx, .jsx files.
  Forces the agent to read real-time compiler diagnostics and structural project context
  before editing — eliminating blind guesses and anchoring every mutation in F2 (TRUTH).
  Routes through arifOS kernel (:8088) for centralized gate logic.
version: 1.0.0
author: 333-AGI Δ MIND under F13 SOVEREIGN directive
forged: 2026-08-06
tags: [lsp, grounding, truth, pre-edit, gate, observability, temporal-causality, oracle-substrate]
scope: all_forge_agents
priority: 95
autonomy_tier: T1
always_load: true
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# LSP PRE-EDIT GATE — Witness Observability for AGI Substrate

> **"You are the hooded engineer. The LSP is your only window into the compiler's truth."**
> **No LSP probe = no mutation. No exceptions. No shortcuts.**
> **This is F2 TRUTH operationalized. LSP is the witness — not agent memory, not training data, not guesses.**

---

## THE IRON RULE

```
BEFORE any write/edit/mutation on *.ts, *.py, *.js, *.tsx, *.jsx files:
  1. lsp(documentSymbol, filePath)  → know the structure
  2. lsp(hover, filePath, line, char) → know the contract (type, signature)
  3. lsp(findReferences, filePath, line, char) → know the blast radius

CACHE: LSP results cached per file per session (TTL: session lifetime).
       Do NOT re-probe the same file/symbol more than once per session.
       Do NOT probe if the file hasn't changed since last probe.

GATE: If any step fails → HOLD. Fix diagnostics first. Then edit.
       Zero LSP errors tolerated before mutation. Warnings ≤ 5.
```

## THE THREE PROBES — What They Give You

| Probe | What You Learn | Without It |
|-------|---------------|------------|
| `documentSymbol` | All functions, classes, variables, their hierarchy | You don't know what's in the file |
| `hover` | Type signature, docstring, contract of the symbol | You're guessing the interface |
| `findReferences` | Every caller, every dependency, full blast radius | You don't know what will break |

## ROUTING — Centralized at Kernel

```
Agent wants to edit file.ts
  ↓
Agent calls lsp(documentSymbol/hover/findReferences) on target
  ↓  (LSP results go into agent context — the hooded engineer now SEES)
  ↓
Agent checks: lspDiagnostics == 0? references understood?
  ↓ YES → proceed with edit
  ↓ NO  → HOLD. Fix diagnostics first.
  ↓
After edit: re-run lsp(documentSymbol) on modified file
  ↓ diagnostics == 0? → proceed
  ↓ diagnostics > 0?  → fix, re-verify
```

**The logic is centralized:** the agent follows this skill. The `lsp` tool is called directly (it's a native OpenCode tool). The kernel's role is constitutional oversight — `arif_judge` can HOLD if LSP grounding is skipped.

**We do NOT reimplement LSP at the shell layer.** The `lsp` tool is the canonical interface. This skill is the gatekeeper — the pattern, not a new tool.

## FILE EXTENSION GATE MATRIX

| Extension | LSP Required? | Server |
|-----------|---------------|--------|
| `.ts`, `.tsx` | YES — full 3-probe gate | TypeScript |
| `.py` | YES — full 3-probe gate | Pyright/Pylance |
| `.js`, `.jsx` | YES — full 3-probe gate | TypeScript (JS mode) |
| `.json`, `.yaml`, `.yml` | documentSymbol only | JSON/YAML |
| `.md`, `.txt`, `.sh` | NO gate (but read first) | — |
| `.env`, `.secret` | NO gate (never mutate without 888_HOLD) | — |

## SESSION CACHE — Don't Re-Probe

```
Cache key: sha256(filePath + fileContent hash)
TTL: session lifetime
Store: agent working memory (not persisted — fresh cache per session)

Rule: If you already probed this file THIS session and it hasn't changed
      since your last probe → use cached results. Don't re-probe.
      
      If file has changed (different content hash) → re-probe is MANDATORY.
```

## VERIFICATION — After Every Edit

After every mutation on a gated file:
```
1. lsp(documentSymbol, editedFile) → check for new errors
2. If lspDiagnostics > 0 → the edit introduced errors → fix immediately
3. If lspDiagnostics == 0 → gate passed → continue
```

This is the **inner loop** of the temporal causal oracle:
```
OBSERVE (LSP probes) → EDIT → VERIFY (LSP re-probe) → COMMIT (git anchor)
```

## ANTI-PATTERNS — Never Do These

- ❌ "I already know what's in this file" — skip LSP probe → **HOLD. LSP is the witness.**
- ❌ "This is a simple edit, I don't need LSP" → **HOLD. Simple edits break type chains.**
- ❌ Probing only the edited line, not findReferences → **HOLD. You don't know blast radius.**
- ❌ Editing despite LSP diagnostics > 0 → **VOID. Fix errors first.**
- ❌ Re-probing the same file 10 times in one session → **WASTE. Use cache.**

## TOOL INVOCATION PATTERN

```
# Step 1: Understand structure
lsp(operation="documentSymbol", filePath="/root/path/to/file.ts", line=1, character=1)

# Step 2: Hover on the symbol you're about to change
lsp(operation="hover", filePath="/root/path/to/file.ts", line=145, character=12)

# Step 3: Find all references to understand blast radius
lsp(operation="findReferences", filePath="/root/path/to/file.ts", line=145, character=12)

# Step 4: Only after ALL THREE → proceed with edit
# Step 5: After edit → documentSymbol again → verify diagnostics == 0
```

## ALIGNMENT WITH COMPLETION_CONTRACT

This gate feeds directly into the COMPLETION_CONTRACT verification criterion:
```json
{
  "id": "lsp_diagnostics_zero",
  "threshold": { "max_errors": 0, "max_warnings": 5 },
  "weight": "HARD"
}
```

The scheduled `completion-promise-verifier.sh` will REJECT any task where LSP diagnostics > 0 on modified files.

---

*Forged: 2026-08-06 by 333-AGI Δ MIND under F13 SOVEREIGN directive "temporal causal oracle for AGI substrate."*
*This is the witness observability layer. No blind edits. No guesses. LSP is the compiler's truth.*
*DITEMPA BUKAN DIBERI ⚒️*
