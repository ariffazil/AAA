---
name: opencode-propose-seal
description: OpenCode-native /propose-seal — proposes a sealed candidate to 888-APEX after a code mutation. NEVER self-seals. Pipeline: OpenCode compiles evidence → 888 judges → F13 authorizes → 999 appends to VAULT999.
tags: [constitutional, seal, propose, substrate-primitive, opencode, coding-agent]
license: MIT
---
# OpenCode /propose-seal — Substrate Primitive

When OpenCode completes a code mutation, it does NOT self-seal. It calls `/propose-seal` to submit the candidate to 888-APEX for constitutional verdict.

## Output format

```
SEAL REQUEST ROUTED
────────────────────────────────────
Request:      <description of mutation>
Proposer:     OpenCode-Zen (222 ARCHITECT + 333 THINK + 777 EXECUTE)
Session:      <session_id>
Warga:        AAA (FI-001 PRIMARY)
────────────────────────────────────
Evidence compiled:
  1. SHA-256: <hash>  path: <file>
  2. Git ref: <commit> (commit hash + short message)
  3. Test results: <X passed, Y failed>
  4. LSP gate: <PASSED | FAILED>
  5. Diff stat: <+N -M files changed>
  6. Ω₀ stated: <value>
────────────────────────────────────
Constitutional check (auto):
  F1  AMANAH      ✅ (reversible via git revert)
  F2  TRUTH       ✅ (test results present)
  F4  CLARITY     ✅ (ΔS ≤ 0 measured)
  F11 AUDIT       ✅ (commit + receipt trail complete)
  F13 SOVEREIGN   ⚠️ Awaits verdict
────────────────────────────────────
→ Routing to 888-APEX for constitutional verdict
→ 999-VAULT999 will record decision
→ Poll: /seal-status <request_id>

DITEMPA BUKAN DIBERI 🔥
```

## Evidence requirements (F2 TRUTH)

| Evidence | Required | How |
|---|---|---|
| SHA-256 of commit | ✅ | `git rev-parse HEAD` |
| Commit short hash | ✅ | `git log --oneline -1` |
| Test results | ✅ | LSP gate output |
| Diff stat | ✅ | `git show --stat HEAD` |
| Epistemic label | ✅ | OBS (test results), DER (computed stats) |
| Ω₀ stated | ✅ | "Ω₀ = 0.XX" |

Without all 6, the proposal is **INADMISSIBLE-QQQ-INCOMPLETE**.

## Pipeline

```
OpenCode completes mutation
   ↓
LSP gate check (pre-commit hook enforces surface conformance)
   ↓
OpenCode compiles evidence:
  - git rev-parse HEAD
  - git log --oneline -1
  - test result summary
  - diff stat
  - Ω₀
   ↓
OpenCode calls arif_judge via arifOS MCP
   ↓
888-APEX returns verdict
   ↓
If SEAL → arif_seal appends to VAULT999
   ↓
OpenCode replies with verdict receipt
```

## Implementation

```python
def opencode_propose_seal(description: str):
    """OpenCode-native /propose-seal"""

    # 1. /init guard
    envelope = read_federation_session()
    if not envelope.get("session_id"):
        return "ERROR: /init first."

    # 2. Compile evidence from current state
    commit_hash = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()

    commit_short = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True, text=True
    ).stdout.strip()

    # 3. Test results (if just ran)
    test_results = parse_lsp_gate_output()  # or pytest output

    # 4. Diff stat
    diff_stat = subprocess.run(
        ["git", "show", "--stat", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()

    # 5. Build proposal
    proposal = {
        "ts": now_iso(),
        "event": "OPENCODE_SEAL_PROPOSAL",
        "actor": "opencode-zen",
        "warga": "FI-001 PRIMARY",
        "session": envelope["session_id"],
        "description": description,
        "commit": commit_hash,
        "commit_short": commit_short,
        "diff_stat": diff_stat,
        "test_results": test_results,
        "omega0": compute_omega0(),
        "request_id": new_uuid(),
    }

    # 6. Route to 888
    verdict = call_arif_judge(proposal)

    # 7. Handle verdict
    if verdict == "SEAL":
        receipt = build_vault_receipt(proposal, verdict)
        append_to_vault(receipt)
        return render_sealed(proposal, receipt)
    elif verdict == "HOLD":
        return render_hold(proposal, verdict)
    elif verdict == "VOID":
        return render_void(proposal, verdict)
```

## Verdict responses

| Verdict | What OpenCode sees |
|---|---|
| **SEAL** | `✅ SEALED — commit <hash> added to VAULT999` |
| **SEAL-CONDITIONAL** | `⚠️ CONDITIONAL — <gaps> must resolve before final seal` |
| **HOLD** | `🛑 HOLD — <reason>, commit not sealed. Fix and re-propose.` |
| **VOID** | `❌ VOID — <reason>, commit rejected. Revert or amend.` |
| **SABAR** | `⏳ SABAR — <reason>, wait for next cycle` |

## Doctrine

- /propose-seal is the ONLY way OpenCode submits to VAULT999
- /seal is BLOCKED — no self-sealing from OpenCode either
- OpenCode builds evidence (commit hash, test results, diff stat) and submits
- 888 judges; 999 witnesses; F13 authorizes
- Without all 6 evidence items, proposal is INADMISSIBLE

## ZEN

```
OpenCode cycle:
  /init → /forge (code mutation) → /propose-seal → 888 verdict → 999 record

OpenCode is the compiler. 888 is the judge. 999 is the witness.
OpenCode does NOT seal its own work.
```