<!-- DELETED | 2026-08-09 -->
<!-- STATUS: REMOVED · SURVIVED → SURVIVAL_INSIGHTS.md -->
<!-- This file has been removed during docs entropy reduction (Tier B/C/D pass). -->
<!-- See docs/SURVIVAL_INSIGHTS.md for surviving insights extracted from this file. -->


# EMD STREAM CONVENTIONS — Zone 2 Formatting for arifOS Agents

> **Forged: 2026-08-06 by 333-AGI Δ MIND · F13 SOVEREIGN**
> **DITEMPA BUKAN DIBERI**
>
> Every agent operating in the arifOS terminal MUST format its output stream
> with these conventions. The stream separates ENCODE (raw inputs), METABOLIZE
> (validation + processing), and DECODE (structured outputs). This is F9
> Anti-Hantu operationalized: the machine is a tool, its operations are visible,
> and F13 remains the absolute authority.

---

## THE THREE ZONES OF THE EMD STREAM

```
┌─────────────────────────────────────────────────────────┐
│ ZONE 1: SOT HEADER (static, rendered by arifos-sot-bar) │
├─────────────────────────────────────────────────────────┤
│ ZONE 2: EMD EXECUTION STREAM (this document)            │
│   ┌─ ENCODE ───────────────────────────────────────┐   │
│   │  [OBS] Raw signal received                      │   │
│   │  [DER] Derived from observation                 │   │
│   │  [INT] Interpretation                           │   │
│   │  [SPEC] Speculation / hypothesis                │   │
│   └────────────────────────────────────────────────┘   │
│   ┌─ METABOLIZE ───────────────────────────────────┐   │
│   │  [F1✓] Reversibility check passed               │   │
│   │  [F2✓] Truth check passed                       │   │
│   │  [F4✓] ΔS ≤ 0 check passed                     │   │
│   │  [F1✗] HOLD — irreversible without 888          │   │
│   │  [LSP] LSP probe results                        │   │
│   │  [EXEC] Tool execution (forge_shell, etc.)      │   │
│   └────────────────────────────────────────────────┘   │
│   ┌─ DECODE ───────────────────────────────────────┐   │
│   │  → Structured output / result                   │   │
│   │  → Artifact path                                │   │
│   │  → Seal receipt                                 │   │
│   └────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│ ZONE 3: COMMAND PROMPT (⬡[SEAL] root@forge:~#)         │
└─────────────────────────────────────────────────────────┘
```

## EMD MARKERS — MANDATORY for all agents

### ENCODE Phase (Sensory Input)

| Marker | Meaning | When to use |
|--------|---------|-------------|
| `[OBS]` | Direct observation | Live probe result, file read, health check |
| `[DER]` | Computation from OBS | Math result, parsed JSON field |
| `[INT]` | Interpretation | Reasoning about evidence |
| `[SPEC]` | Hypothesis | Speculation, prediction, proposal |

**Rule:** Every claim MUST carry an epistemic marker. No unlabeled claims.
**Anti-pattern:** `[OBS] The system is healthy` — what probe? Show the raw output.

### METABOLIZE Phase (Validation)

| Marker | Meaning | When to use |
|--------|---------|-------------|
| `[F1✓]` | Reversibility pass | Action is reversible with rollback |
| `[F1✗]` | Reversibility fail | HOLD — needs 888 |
| `[F2✓]` | Truth check pass | Evidence verified |
| `[F4✓]` | Entropy gate pass | ΔS ≤ 0 confirmed |
| `[LSP]` | LSP probe | documentSymbol/hover/findReferences result |
| `[EXEC]` | Tool execution | forge_shell, forge_filesystem, forge_git |
| `[VERIFY]` | Verification | Post-execution check |
| `[HOLD]` | Gate blocked | Waiting for sovereign or condition |
| `[SEAL]` | Immutable record | Writing to VAULT999 |

**Rule:** Tool executions and floor checks MUST be MARKED. Raw tool output follows the marker.
**Anti-pattern:** Silent tool execution — always show what ran and what it returned.

### DECODE Phase (Output)

| Marker | Meaning | When to use |
|--------|---------|-------------|
| `→` | Result/artifact | Final structured output |
| `ΔS=` | Entropy delta | Session/task entropy change |
| `→ /path/` | Artifact location | File created or modified |

## COLOR CONVENTIONS (when terminal supports it)

| Color | Meaning | Usage |
|-------|---------|-------|
| **Cyan** `\033[1;36m` | Agent reasoning | Thoughts, plans, interpretations |
| **White** `\033[1;37m` | Important results | Final outputs, verdicts |
| **Green** `\033[1;32m` | Pass / success | Floor checks, test passes |
| **Yellow** `\033[1;33m` | Caution / warning | FQ dropping, HOLD pending |
| **Red** `\033[1;31m` | Block / failure | HOLD, VOID, DENY |
| **Dim** `\033[2;37m` | Metadata / provenance | Timestamps, hashes, receipts |
| **Magenta** `\033[1;35m` | Sovereign signals | F13 commands, 888 verdicts |

## FQ PULSE — Metabolic heartbeat in stream

Every agent should emit FQ at task boundaries:

```
[FQ:1.5 OPTIMAL] · execute=40 · verify=60 · ΔS=-0.55
```

If FQ < 0.5: **ALL agents HOLD non-critical work.** Show:
```
[FQ:0.4 WATCHING] ⬡ HOLD — metabolic pulse low. Reduce execution. Increase verification.
```

## REASONING vs EXECUTION — Clear visual separation

```
# Agent reasoning (what it THINKS):
[INT] This file handles authentication. Type signature is:
  authenticate(token: string): Promise<User | null>
[LSP] documentSymbol: 12 symbols (4 functions, 3 classes, 5 interfaces)
[LSP] findReferences: authenticate() called from 3 files (auth.ts, middleware.ts, api.ts)

# Agent execution (what it DOES):
[F1✓] Reversible — editing with backup
[F2✓] LSP probe complete — blast radius: 3 callers
[EXEC] forge_filesystem(mode=write, path=/root/path/auth.ts)
  → Written 245 bytes, SHA256: a1b2c3d4
[VERIFY] lsp(documentSymbol) — 0 diagnostics. Gate passed.
→ Artifact: /root/path/auth.ts (modified)
```

## ANTI-PATTERNS — Never do these in the EMD stream

- ❌ Mixing reasoning and execution without markers — "I'll fix this..." then silently executing
- ❌ Unlabeled claims — every claim needs [OBS]/[DER]/[INT]/[SPEC]
- ❌ Silent tool calls — always show [EXEC] marker + what ran
- ❌ Floor checks buried in prose — [F1✓] markers MUST be visible
- ❌ Skipping FQ pulse at task boundaries — the metabolic heartbeat must be visible

---

*Forged: 2026-08-06 by 333-AGI Δ MIND under F13 SOVEREIGN "three-zone terminal architecture" directive.*
*This is the EMD stream contract. All AAA warga agents are bound by it.*
*DITEMPA BUKAN DIBERI ⚒️*
