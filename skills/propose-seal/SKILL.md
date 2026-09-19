---
name: propose-seal
description: "Use when an agent submits /propose-seal to 888-APEX after a code mutation or completed work."
tags: [constitutional, seal, propose, substrate-primitive, canonical, telegram-native, openclaw, opencode, hermes]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
canonical: true
supersedes: [openclaw-propose-seal, opencode-propose-seal, hermes-propose-seal]
merged_from:
  - /root/.hermes/skills/openclaw-propose-seal
  - /root/.hermes/skills/opencode-propose-seal
  - /root/.config/opencode/skills/opencode-propose-seal
  - /root/.kimi-code/skills/opencode/opencode-propose-seal
  - /root/.kimi-code/skills/openclaw-propose-seal
  - /root/.kimi-code/skills/hermes/hermes-propose-seal
  - /root/.hermes/skills/domains/general/apex/verdict/hermes-propose-seal
triggers:
  - "/propose-seal"
  - "OpenClaw agent submits /propose-seal to 888-APEX after a code mutation"
  - "OpenCode agent submits /propose-seal to 888-APEX after a code mutation"
  - "proposing a sealed candidate to 888-APEX"
  - "agent wants to append to VAULT999"
  - "never self-seals"
---

# /propose-seal — Canonical Substrate Primitive (all harnesses)

> **Canonical.** One doctrine, one file, one home (`/root/AAA/skills/propose-seal`). Merged 2026-09-19
> under F13 sovereign order to compress namespace entropy. Before the merge, agents loaded three
> harness-local copies of this doctrine from outside the canonical store; every distinct step, schema,
> refusal case, receipt format and warning of all copies is preserved below, labelled by harness.
> Originals frozen (not deleted) at
> `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/propose-seal/` — see `LEDGER.json` there.
> Old paths (`openclaw-propose-seal`, `opencode-propose-seal`, `hermes-propose-seal`) are symlinks to this folder.

**The invariants all three harnesses share:**

- A user or agent types `/propose-seal <description>`; the harness **compiles evidence** and submits the candidate to 888-APEX for constitutional verdict.
- **The proposer NEVER self-seals.** All sealing routes through 888-APEX.
- `/seal` is **BLOCKED** — no self-sealing, from any harness.
- **999 is witness, not authority** — the witness path runs ONLY after an 888 verdict.
- **F13 (Arif) is the final authority** for T3 irreversible sealing.
- Never free-text `"888-APEX JUDGMENT"`. Quote the kernel's `effective_verdict` + `call_hash` (Gödel lock).

## Harness surface map

| Harness | Invocation surface | Proposer line | Kernel actor flag |
|---|---|---|---|
| OpenClaw | `/propose-seal <description>` to the OpenClaw bot (Telegram-native) | OpenClaw (333 THINK + 444 ORCHESTRATE) | `apex-judge --actor OPENCLAW` |
| OpenCode | `/propose-seal` after a code mutation | OpenCode-Zen (222 ARCHITECT + 333 THINK + 777 EXECUTE) | `arif_judge` via arifOS MCP |
| Hermes | `/propose-seal <description>` in Telegram | Hermes (555-ASI / Ω CORE) | `apex-judge --actor HERMES` |

---

## → OpenClaw variant

When a user types `/propose-seal <description>` to the OpenClaw bot, OpenClaw compiles evidence and submits the candidate to 888-APEX for constitutional verdict.

**OpenClaw NEVER self-seals.** All sealing routes through 888-APEX.

### Output format (OpenClaw)

```
SEAL REQUEST ROUTED
────────────────────────────────────
Request:      <description of what is being sealed>
Proposer:     OpenClaw (333 THINK + 444 ORCHESTRATE)
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
  F1  AMANAH      ✅
  F2  TRUTH       ✅
  F4  CLARITY     ✅
  F7  HUMILITY    ✅
  F11 AUDIT       ✅
  F13 SOVEREIGN   ⚠️ Awaits verdict
────────────────────────────────────
→ Routing to 888-APEX for constitutional verdict
→ 999-VAULT999 will record decision
→ Poll: /seal-status <request_id>

DITEMPA BUKAN DIBERI 🔥
```

### Evidence requirements (F2 TRUTH) — OpenClaw

Before `/propose-seal` can be routed, these must be present:

| Evidence | Required | Check |
|---|---|---|
| SHA-256 of work product | ✅ | `sha256sum <file>` |
| Git commit reference | ✅ | `git log --oneline -1` |
| At least 1 live probe result | ✅ | `curl :PORT/health` or equivalent |
| Epistemic label (OBS/DER) | ✅ | Embedded in evidence chain |
| Ω₀ stated | ✅ | "Ω₀ = 0.XX" in request |

Without all **5**, the proposal is **INADMISSIBLE-QQQ-INCOMPLETE**.

### Pipeline (OpenClaw)

```
/propose-seal <description>
   ↓
OpenClaw compiles evidence (auto-detect recent files, git refs, live probes)
   ↓
OpenClaw submits via `apex-judge --actor OPENCLAW` (or arif_init→arif_judge MCP).
   Never free-text "888-APEX JUDGMENT". Quote effective_verdict + call_hash.
   ↓
Kernel arif_judge returns SEAL | HOLD | VOID | SABAR
   ↓
If SEAL → OpenClaw appends correction receipt to VAULT999 via forge_vault(mode="receipt")
   ↓
OpenClaw replies with verdict receipt
```

### Verdict responses — OpenClaw

| Verdict | What OpenClaw sees |
|---|---|
| **SEAL** | `✅ SEALED — {receipt_hash} added to VAULT999` |
| **SEAL-CONDITIONAL** | `⚠️ CONDITIONAL — {gaps} must resolve before final seal` |
| **HOLD** | `🛑 HOLD — {reason}, placed in open_loops_888_HOLD` |
| **VOID** | `❌ VOID — {reason}, work not sealed` |
| **SABAR** | `⏳ SABAR — {reason}, wait for next cycle` |

### ZEN (OpenClaw)

```
/propose-seal answers:  CAN THIS BE SEALED?
         → OpenClaw compiles evidence
         → 888 judges
         → 999 witnesses (if SEAL)

OpenClaw is the courier. Not the judge. Not the witness.
```

---

## → OpenCode variant

When OpenCode completes a code mutation, it does NOT self-seal. It calls `/propose-seal` to submit the candidate to 888-APEX for constitutional verdict.

### Output format (OpenCode)

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

### Evidence requirements (F2 TRUTH) — OpenCode

| Evidence | Required | How |
|---|---|---|
| SHA-256 of commit | ✅ | `git rev-parse HEAD` |
| Commit short hash | ✅ | `git log --oneline -1` |
| Test results | ✅ | LSP gate output |
| Diff stat | ✅ | `git show --stat HEAD` |
| Epistemic label | ✅ | OBS (test results), DER (computed stats) |
| Ω₀ stated | ✅ | "Ω₀ = 0.XX" |

Without all **6**, the proposal is **INADMISSIBLE-QQQ-INCOMPLETE**.

### Pipeline (OpenCode)

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

### Implementation (OpenCode)

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

### Verdict responses — OpenCode

| Verdict | What OpenCode sees |
|---|---|
| **SEAL** | `✅ SEALED — commit <hash> added to VAULT999` |
| **SEAL-CONDITIONAL** | `⚠️ CONDITIONAL — <gaps> must resolve before final seal` |
| **HOLD** | `🛑 HOLD — <reason>, commit not sealed. Fix and re-propose.` |
| **VOID** | `❌ VOID — <reason>, commit rejected. Revert or amend.` |
| **SABAR** | `⏳ SABAR — <reason>, wait for next cycle` |

### ZEN (OpenCode)

```
OpenCode cycle:
  /init → /forge (code mutation) → /propose-seal → 888 verdict → 999 record

OpenCode is the compiler. 888 is the judge. 999 is the witness.
OpenCode does NOT seal its own work.
```

---

## → Hermes variant

When a user types `/propose-seal <description>` in Telegram, Hermes compiles evidence and submits the candidate to 888-APEX for constitutional verdict. **Hermes NEVER self-seals.**

### Output format (Hermes)

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

### Implementation (Hermes)

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

### Pipeline (Hermes)

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

### ZEN (Hermes)

```
/propose-seal answers:  CAN THIS BE SEALED?
         → Hermes compiles evidence
         → 888 judges
         → 999 witnesses (if SEAL)

Without /init:  /propose-seal returns ERROR (no actor)
Without /propose-seal:  no permanent record possible

Hermes is the courier. Not the judge. Not the witness.
```

---

## Refusal / HOLD cases (union of every source body)

| Case | Result |
|---|---|
| No `/init` session bound | `ERROR: /init first.` (OpenCode) / `ERROR: /init first. No session bound.` (Hermes) — no proposal is built; no actor to attribute |
| OpenClaw evidence missing any of the 5 items | **INADMISSIBLE-QQQ-INCOMPLETE** |
| OpenCode evidence missing any of the 6 items | **INADMISSIBLE** / **INADMISSIBLE-QQQ-INCOMPLETE** |
| Attempt to `/seal` directly (any harness) | **BLOCKED** — no self-sealing |
| Free-text `"888-APEX JUDGMENT"` instead of kernel receipt | Forbidden (Gödel lock) — must quote `effective_verdict` + `call_hash` |
| Kernel returns **HOLD** | Work not sealed; OpenClaw places it in `open_loops_888_HOLD`; OpenCode must fix and re-propose |
| Kernel returns **VOID** | Work not sealed; OpenCode reverts or amends |
| Kernel returns **SEAL-CONDITIONAL** | Listed gaps must resolve before final seal |
| Kernel returns **SABAR** | Wait for the next cycle |
| 999 (witness) invoked before an 888 verdict | Refused — witness runs ONLY after the verdict |
| T3 irreversible seal | Awaits F13 (Arif) — the final authority |

## Doctrine (shared, all variants)

- `/propose-seal` is the **ONLY** way an agent submits to VAULT999 via 888-APEX.
- `/seal` is BLOCKED — no self-sealing (OpenClaw explicitly; "from OpenCode either").
- 999 is **witness, not authority** — runs ONLY after the 888 verdict.
- F13 (Arif) is the final authority for T3 irreversible sealing.
- OpenCode builds evidence (commit hash, test results, diff stat) and submits; 888 judges; 999 witnesses; F13 authorizes.
- Without all evidence items, the proposal is INADMISSIBLE.

## Preserved source frontmatter (verbatim)

Kept so no field of the retired copies is lost.

```yaml
# openclaw-propose-seal  (/root/.hermes/skills, .kimi-code/skills)
name: openclaw-propose-seal
description: "Use when OpenClaw agent submits /propose-seal to 888-APEX after a code mutation. NEVER self-seals. OpenClaw-native /propose-seal — proposes a sealed candidate to 888-APEX. NEVER self-seals. Pipeline: agent proposes → 888 judges → F13 authorizes → 999 executes (append to VAULT999)."
tags: [constitutional, seal, propose, substrate-primitive, telegram-native, openclaw]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
```

```yaml
# opencode-propose-seal  (/root/.hermes/skills, /root/.config/opencode/skills, .kimi-code/skills/opencode)
name: opencode-propose-seal
description: "Use when OpenCode agent submits /propose-seal to 888-APEX after a code mutation. NEVER self-seals. OpenCode-native /propose-seal — proposes a sealed candidate to 888-APEX after a code mutation. NEVER self-seals. Pipeline: OpenCode compiles evidence → 888 judges → F13 authorizes → 999 appends to VAULT999."
tags: [constitutional, seal, propose, substrate-primitive, opencode, coding-agent]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
```

```yaml
# hermes-propose-seal  (/root/.hermes/skills/domains/general/apex/verdict, .kimi-code/skills/hermes)
name: hermes-propose-seal
description: "Use when proposing a sealed candidate to 888-APEX. NEVER self-seals; pipeline goes through 888 judge and F13 authorization. Substrate primitive /propose-seal — proposes a sealed candidate to 888-APEX. NEVER self-seals. The flow: agent proposes → 888 judges → F13 authorizes → 999 executes (append to VAULT999)."
tags: [constitutional, seal, propose, substrate-primitive, telegram-native, hermes]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
```

## Provenance

| Source | Harness | SKILL.md sha256 (before merge) |
|---|---|---|
| `/root/.hermes/skills/openclaw-propose-seal/SKILL.md` | OpenClaw (Hermes tree) | `7cf064d091253a6ae07dd305f087ade34ef3e512872efebf3f47fff5a2bf8ea1` |
| `/root/.kimi-code/skills/openclaw-propose-seal/SKILL.md` | OpenClaw (Kimi tree) | `0a8349e239cbdfe80372b424ce00b39f7c81d61272fac033806f85b1598d87a2` |
| `/root/.hermes/skills/opencode-propose-seal/SKILL.md` | OpenCode (Hermes tree) | `c8fc449ecc6f23c32faca225c21df7d22f2299f7868bd8a52a827950136b00d8` |
| `/root/.config/opencode/skills/opencode-propose-seal/SKILL.md` | OpenCode (opencode config tree) | `e1a8037f47ef85dc1e1fdec6fdc940473c86f506c668bcabb006091e429f8c31` |
| `/root/.kimi-code/skills/opencode/opencode-propose-seal/SKILL.md` | OpenCode (Kimi tree) | `dd7b9761f387cecd9a98ede1f2a54e3cbc30dae5659f18f3eb813b12e856a066` |
| `/root/.kimi-code/skills/hermes/hermes-propose-seal/SKILL.md` | Hermes (Kimi tree) | `8353777f910422ee50ea392c52cd4febb6bbbaf91c3b8cda9fb0d2a1397b5bb4` |
| `/root/.hermes/skills/domains/general/apex/verdict/hermes-propose-seal/SKILL.md` | Hermes (apex/verdict tree) | `59230b3aec2c48e3e3b9156d1fe2cf8d197b4e49d83323d8c88ab80f0f9cb75d` |

Frozen copies + LEDGER.json:
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/propose-seal/`

DITEMPA BUKAN DIBERI 🔥
