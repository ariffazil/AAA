---
name: hermes-propose-seal
description: "Substrate primitive /propose-seal — proposes a sealed candidate to 888-APEX. NEVER self-seals. The flow: agent proposes → 888 judges → F13 authorizes → 999 executes (append to VAULT999)."
tags: [constitutional, seal, propose, substrate-primitive, telegram-native, hermes]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# Hermes /propose-seal — Substrate Primitive

When a user types `/propose-seal <description>` in Telegram, Hermes compiles evidence and submits the candidate to 888-APEX for constitutional verdict. **Hermes NEVER self-seals.**

## Output format (when user invokes)

```
SEAL REQUEST ROUTED
────────────────────────────────────
Request:      <description of what is being sealed>
Proposer:     Hermes (555-ASI / Ω CORE)
Session:      <session_id>
Actor:        ariffazil (F13 SOVEREIGN)
────────────────────────────────────
Evidence compiled:
  1. SHA-256: <hash>  path: <file>
  2. Git ref: <commit>
  3. Live probe: <:PORT/health output>
  4. Epistemic tag: OBS | DER | INT | SPEC
  5. Ω₀ stated: <value>
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

## Implementation

```python
def hermes_propose_seal_handler(event, description: str):
    """Telegram-native /propose-seal handler for Hermes"""

    # 1. /init guard — must be bound first
    envelope = read_federation_session()
    if not envelope.get("session_id"):
        return "ERROR: /init first. No session bound."

    # 2. Compile evidence chain
    evidence = []
    # Auto-detect what was just done in this session
    last_files = probe_recent_file_writes()
    for f in last_files:
        evidence.append({
            "path": f,
            "sha256": sha256_of_file(f),
            "epistemic_tag": "OBS"
        })

    # 3. Live probe (one minimum)
    health = probe_organ_health()

    # 4. Compute Ω₀ from session entropy
    omega0 = compute_omega0()

    # 5. Build proposal payload
    proposal = {
        "ts": now_iso(),
        "event": "SEAL_PROPOSAL",
        "actor": "hermes-audit",
        "session": envelope["session_id"],
        "description": description,
        "evidence": evidence,
        "omega0": omega0,
        "request_id": new_uuid(),
    }

    # 6. Kernel judge only — NEVER free-text "888-APEX JUDGMENT" (Gödel lock)
    # Prefer: subprocess apex-judge --actor HERMES --candidate description
    # Or MCP: arif_init → arif_judge; quote effective_verdict + call_hash
    verdict = call_arif_judge(proposal)  # must be kernel receipt, not prose

    # 7. If SEAL → append correction receipt to VAULT999
    if verdict == "SEAL":
        receipt = build_vault_receipt(proposal, verdict)
        append_to_vault(receipt)  # via forge_vault(mode="receipt")
        return render_sealed(proposal, receipt)
    elif verdict == "HOLD":
        return render_hold(proposal, verdict)
    elif verdict == "VOID":
        return render_void(proposal, verdict)
```

## Pipeline

```
/propose-seal <description>
   ↓
Hermes compiles evidence (auto-detect recent files, git refs, live probes)
   ↓
Hermes submits via `apex-judge --actor HERMES` (or arif_init→arif_judge MCP).
   Never free-text self-SEAL. Quote effective_verdict + call_hash.
   ↓
Kernel arif_judge returns SEAL | HOLD | VOID | SABAR
   ↓
If SEAL → Hermes calls forge_vault(mode="receipt") → append to VAULT999
   ↓
Hermes replies with verdict receipt
```

## Doctrine

- **/propose-seal is the ONLY way an agent submits to VAULT999** via 888-APEX
- /seal is BLOCKED — no self-sealing
- 999 is witness, not authority — the witness path runs ONLY after 888 verdict
- F13 (Arif) is the final authority for T3 irreversible sealing

## ZEN

```
/propose-seal answers:  CAN THIS BE SEALED?
         → Hermes compiles evidence
         → 888 judges
         → 999 witnesses (if SEAL)

Without /init:  /propose-seal returns ERROR (no actor)
Without /propose-seal:  no permanent record possible

Hermes is the courier. Not the judge. Not the witness.
```