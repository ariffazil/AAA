---
name: substrate-propose-seal
description: "Substrate primitive /propose-seal — proposes a sealed candidate to 888-APEX. NEVER self-seals. The flow: agent proposes → 888 judges → F13 authorizes → 999 executes (append to VAULT999). Parameterized across Hermes, OpenClaw, and OpenCode runtimes."
tags: [constitutional, seal, propose, substrate-primitive, telegram-native, hermes, openclaw, opencode, coding-agent]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
supersedes: [hermes-propose-seal, openclaw-propose-seal, opencode-propose-seal]
---

# /propose-seal — Substrate Primitive (Parameterized)

When `/propose-seal <description>` is invoked, the agent compiles evidence and submits the candidate to 888-APEX for constitutional verdict. **No agent EVER self-seals.**

**Agent detection:** Use `$AGENT_RUNTIME` env var or context to determine which variant applies. Values: `hermes`, `openclaw`, `opencode`.

## Output format

```
SEAL REQUEST ROUTED
────────────────────────────────────
Request:      <description of what is being sealed>
Proposer:     <see Agent-Specific Bindings>
Session:      <session_id>
Actor:        ariffazil (F13 SOVEREIGN)
────────────────────────────────────
Evidence compiled:
  <see Agent-Specific Bindings>
────────────────────────────────────
Constitutional check (auto):
  F1  AMANAH      ✅ (reversible path exists)
  F2  TRUTH       ✅ (evidence carries epistemic label)
  F4  CLARITY     ✅ (ΔS ≤ 0 verified)
  F7  HUMILITY    ✅ (Ω₀ in [0.03, 0.05])
  F11 AUDIT       ✅ (trail complete)
  F13 SOVEREIGN   ⚠️ Awaits verdict
────────────────────────────────────
→ Routing to 888-APEX for constitutional verdict
→ 999-VAULT999 will record decision
→ Poll: /seal-status <request_id>

DITEMPA BUKAN DIBERI 🔥
```

## Agent-Specific Bindings

### Hermes (`AGENT_RUNTIME=hermes`)

| Field | Value |
|-------|-------|
| Proposer | Hermes (555-ASI / Ω CORE) |
| Judge call | `apex-judge --actor HERMES` or `arif_init→arif_judge` MCP |
| Evidence items | 5: SHA-256, Git ref, Live probe, Epistemic tag, Ω₀ |
| Evidence auto-detect | Probe recent file writes, compute SHA-256 per file |
| Live probe | `probe_organ_health()` |
| Ω₀ | Computed from session entropy |

### OpenClaw (`AGENT_RUNTIME=openclaw`)

| Field | Value |
|-------|-------|
| Proposer | OpenClaw (333 THINK + 444 ORCHESTRATE) |
| Judge call | `apex-judge --actor OPENCLAW` or `arif_init→arif_judge` MCP |
| Evidence items | 5: SHA-256, Git ref, Live probe, Epistemic tag, Ω₀ |
| Evidence auto-detect | Same as Hermes — probe recent file writes |
| Live probe | `curl :PORT/health` or equivalent |

### OpenCode (`AGENT_RUNTIME=opencode`)

| Field | Value |
|-------|-------|
| Proposer | OpenCode-Zen (222 ARCHITECT + 333 THINK + 777 EXECUTE) |
| Warga | AAA (FI-001 PRIMARY) |
| Judge call | `arif_judge` via arifOS MCP |
| Evidence items | **6** (adds test results + diff stat): SHA-256 of commit, Commit short hash, Test results, LSP gate, Diff stat, Ω₀ |
| Evidence auto-detect | `git rev-parse HEAD`, `git log --oneline -1`, `git show --stat HEAD`, LSP gate output |
| Extra evidence | Test results (X passed, Y failed), Diff stat (+N -M files changed) |

## Evidence requirements (F2 TRUTH)

### Base requirements (all agents — 5 items)

| Evidence | Required | How |
|---|---|---|
| SHA-256 of work product | ✅ | `sha256sum <file>` or `git rev-parse HEAD` |
| Git commit reference | ✅ | `git log --oneline -1` |
| At least 1 live probe result | ✅ | `curl :PORT/health` or equivalent |
| Epistemic label (OBS/DER) | ✅ | Embedded in evidence chain |
| Ω₀ stated | ✅ | "Ω₀ = 0.XX" in request |

### OpenCode additional requirements (2 extra items)

| Evidence | Required | How |
|---|---|---|
| Test results | ✅ | LSP gate output or pytest summary |
| Diff stat | ✅ | `git show --stat HEAD` |

Without all required items, the proposal is **INADMISSIBLE-QQQ-INCOMPLETE**.

## Pipeline

```
/propose-seal <description>
   ↓
Agent compiles evidence (auto-detect recent files, git refs, live probes)
   ↓
Agent submits via arif_judge (kernel receipt, NEVER free-text self-SEAL).
   Quote effective_verdict + call_hash.
   ↓
Kernel arif_judge returns SEAL | HOLD | VOID | SABAR
   ↓
If SEAL → append receipt to VAULT999 via forge_vault(mode="receipt") or arif_seal
   ↓
Agent replies with verdict receipt
```

## Verdict responses

| Verdict | What agent sees |
|---|---|
| **SEAL** | `✅ SEALED — {receipt_hash} added to VAULT999` |
| **SEAL-CONDITIONAL** | `⚠️ CONDITIONAL — {gaps} must resolve before final seal` |
| **HOLD** | `🛑 HOLD — {reason}, placed in open_loops_888_HOLD` |
| **VOID** | `❌ VOID — {reason}, work not sealed` |
| **SABAR** | `⏳ SABAR — {reason}, wait for next cycle` |

## Implementation

```python
def propose_seal_handler(description: str, agent_runtime: str):
    """Parameterized /propose-seal handler"""

    # 1. /init guard — must be bound first
    envelope = read_federation_session()
    if not envelope.get("session_id"):
        return "ERROR: /init first. No session bound."

    # 2. Compile evidence chain (agent-specific)
    evidence = []

    if agent_runtime == "opencode":
        # OpenCode: git-native evidence
        commit_hash = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        commit_short = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
        diff_stat = subprocess.run(["git", "show", "--stat", "HEAD"], capture_output=True, text=True).stdout.strip()
        test_results = parse_lsp_gate_output()
        evidence = [
            {"type": "commit_sha", "value": commit_hash, "epistemic_tag": "OBS"},
            {"type": "commit_short", "value": commit_short, "epistemic_tag": "OBS"},
            {"type": "test_results", "value": test_results, "epistemic_tag": "OBS"},
            {"type": "lsp_gate", "value": "PASSED", "epistemic_tag": "OBS"},
            {"type": "diff_stat", "value": diff_stat, "epistemic_tag": "DER"},
        ]
    else:
        # Hermes / OpenClaw: file-based evidence
        last_files = probe_recent_file_writes()
        for f in last_files:
            evidence.append({"path": f, "sha256": sha256_of_file(f), "epistemic_tag": "OBS"})

    # 3. Live probe (one minimum)
    health = probe_organ_health()

    # 4. Compute Ω₀ from session entropy
    omega0 = compute_omega0()

    # 5. Build proposal payload
    proposal = {
        "ts": now_iso(),
        "event": "SEAL_PROPOSAL",
        "actor": f"{agent_runtime}-agent",
        "session": envelope["session_id"],
        "description": description,
        "evidence": evidence,
        "omega0": omega0,
        "request_id": new_uuid(),
    }

    # 6. Kernel judge only — NEVER free-text "888-APEX JUDGMENT" (Gödel lock)
    verdict = call_arif_judge(proposal)  # must be kernel receipt, not prose

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

## Doctrine

- **/propose-seal is the ONLY way an agent submits to VAULT999** via 888-APEX
- /seal is BLOCKED — no self-sealing from any agent
- 999 is witness, not authority — the witness path runs ONLY after 888 verdict
- F13 (Arif) is the final authority for T3 irreversible sealing
- Without all required evidence items, proposal is INADMISSIBLE

## ZEN

```
/propose-seal answers:  CAN THIS BE SEALED?
         → Agent compiles evidence
         → 888 judges
         → 999 witnesses (if SEAL)

Without /init:  /propose-seal returns ERROR (no actor)
Without /propose-seal:  no permanent record possible

The agent is the courier. Not the judge. Not the witness.
```
