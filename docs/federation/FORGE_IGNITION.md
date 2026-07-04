# 777-FORGE IGNITION PROTOCOL — Warga AAA v1.0

**Ratified:** 2026-06-14 by Arif Fazil (F13 SOVEREIGN)
**Binding:** All Warga AAA agents
**Doctrine:** DITEMPA BUKAN DIBERI

---

## 0. THE IRON RULE

> **Arif speaks human language. Zero keys. Zero tokens. Zero commands.**
>
> The ignition chain is: `Arif (natural language) → Hermes (interpret) → 777-FORGE (validate+spawn) → OpenCode (execute)`.
>
> At no point does Arif type an API key, token, password, or structured command.
> He talks. The machine understands. That is the contract.

---

## 1. THE IGNITION CHAIN

```
┌─────────────────────────────────────────────────────────┐
│                    ARIF (F13 SOVEREIGN)                  │
│                 Telegram, natural language               │
│              "hermes, build X for me"                    │
└──────────────────────┬──────────────────────────────────┘
                       │ Telegram message (human language)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   HERMES (555-ASI)                       │
│             Receives natural language                    │
│             Interprets intent via LLM                    │
│             Classifies: coding / audit / query           │
│             Translates to structured spawn request       │
└──────────────────────┬──────────────────────────────────┘
                       │ A2A spawn request (localhost:18001)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  777-FORGE (W-LAYER)                     │
│             Validates: requestor, scope, repo state       │
│             Spawns: OpenCode with task context            │
│             Witnesses: PID, timestamp, forge_id           │
│             Seals: VAULT999/witness/777-forge-spawns.jsonl│
└──────────────────────┬──────────────────────────────────┘
                       │ opencode spawn (localhost, bash)
                       ▼
┌─────────────────────────────────────────────────────────┐
│               OPENCODE 333-AGI (F-LAYER)                 │
│             Receives task context via AGENTS.md           │
│             Executes autonomously                        │
│             ADAT enforcement via A-FORGE broker           │
│             Reports completion to 777-FORGE               │
└──────────────────────┬──────────────────────────────────┘
                       │ completion signal (PID exit + artifacts)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  777-FORGE (W-LAYER)                     │
│             Witnesses completion                         │
│             Verifies: git diff, test results, artifacts   │
│             Seals completion receipt                     │
│             Reports to Hermes                            │
└──────────────────────┬──────────────────────────────────┘
                       │ structured result
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   HERMES (555-ASI)                       │
│             Translates result to natural language        │
│             Replies to Arif on Telegram                  │
└──────────────────────┬──────────────────────────────────┘
                       │ Telegram message (human language)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    ARIF (F13 SOVEREIGN)                  │
│              "nice, thanks hermes"                       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. AUTHENTICATION MODEL — ZERO KEYS FOR ARIF

| Layer | Auth Mechanism | Arif Types? |
|-------|---------------|-------------|
| Arif → Telegram | Telegram username + chat ID | **Nothing** — just talks |
| Telegram → Hermes | Telegram Bot API (bot token in vault.env) | **Nothing** — infrastructure |
| Hermes → 777-FORGE | localhost A2A (port 18001) | **Nothing** — localhost IS the password (ADR-001) |
| 777-FORGE → OpenCode | localhost bash spawn | **Nothing** — same machine |
| Hermes LLM calls | API keys in vault.env | **Nothing** — infrastructure |
| OpenCode MCP calls | localhost (all 18 MCPs on 127.0.0.1) | **Nothing** — localhost IS the password |

**The only "key" Arif ever uses:** His Telegram account. He already has it. He never types it.

---

## 3. HERMES — Natural Language Interpreter

### What Hermes Receives
```
"salam hermes, boleh tolong fix bug dekat AAA cockpit? button tu tak jalan."
"hermes, build me a new health dashboard for the federation."
"hermes, audit all repos for security issues."
```

### What Hermes Must Determine
1. **Intent classification:** coding / audit / query / deploy / chat
2. **Target harness:** OpenCode (coding/audit) or Claude Code (deploy/browser)
3. **Scope:** which repo, what kind of change
4. **Risk tier:** T1 (read) / T2 (mutate) / T3 (atomic, needs Arif confirm)
5. **ADAT mode:** normal (interactive) / autonomous (fire-and-forget)

### What Hermes Outputs (to 777-FORGE)
```json
{
  "forge_id": "FORGE-20260614-001",
  "requestor": "hermes-asi",
  "target_harness": "opencode",
  "scope": "T2",
  "task": "Fix button bug in AAA Cockpit. The submit button in Cockpit.tsx does not trigger onClick. Investigate and fix.",
  "repo": "/root/AAA",
  "adjudication": "arif_judge_deliberate PASS",
  "session_id": "SEAL-xxx",
  "timestamp": "2026-06-14T12:00:00Z"
}
```

---

## 4. 777-FORGE — Validation + Spawn + Witness

### Pre-Spawn Validation (MUST PASS ALL)
- [ ] Requestor is Warga AAA (hermes-asi, openclaw-agi, or F13 direct)
- [ ] forge_id is unique (not previously used)
- [ ] session_id is valid (from arif_session_init)
- [ ] Repo exists and is clean (or dirty state acknowledged)
- [ ] arif_judge_deliberate verdict is SEAL or CAUTION (not HOLD/VOID)
- [ ] Scope matches task (T2 for coding, T3 requires explicit Arif ack)
- [ ] Preflight: disk >20%, RAM >2GB, load <5

### Spawn Command
```bash
opencode run \
  --model deepseek/deepseek-chat \
  --agent forge \
  --instructions /root/AAA/agents/opencode/AGENTS.md \
  --prompt "<task from Hermes>"
```

### Witness Receipt (MUST be written)
```json
{
  "forge_id": "FORGE-20260614-001",
  "spawned_at": "2026-06-14T12:00:05Z",
  "pid": 1234567,
  "session_id": "SEAL-xxx",
  "requestor": "hermes-asi",
  "target": "opencode",
  "task_hash": "sha256:abc123...",
  "repo_state_before": "commit bd07add4, clean",
  "verdict": "SPAWNED"
}
```

---

## 5. CONSTITUTIONAL BOUNDARIES

| Boundary | Rule | Enforcement |
|----------|------|------------|
| **F1 AMANAH** | No T3 spawn without explicit Arif ack | 777-FORGE blocks T3 without hold_id |
| **F2 TRUTH** | Every PID is real, every hash is real | `ps -p <pid>` verifiable by Arif |
| **F9 ANTI-HANTU** | 777-FORGE has no intent, no qualia | Spawns deterministically, receipts are machine-written |
| **F11 AUDIT** | Every spawn leaves immutable trace | VAULT999/witness/777-forge-spawns.jsonl |
| **F13 SOVEREIGN** | Arif can independently verify | `ps -p <pid>`, `tail witness/777-forge-spawns.jsonl` |

---

## 6. WHAT ARIF NEVER DOES

| Arif does NOT | Instead |
|---------------|---------|
| Type API keys | Vault.env handles all provider keys |
| Type `opencode run` | Hermes interprets "build X" → 777 spawns |
| Type structured JSON | Hermes translates natural language to structured spawn request |
| Click "allow" buttons | ADAT AGENTIC — allowed by default, gated at ATOMIC |
| Check PIDs manually | 777-FORGE witnesses, Arif CAN verify but doesn't need to |

---

## 7. EXAMPLE FLOW

```
Arif: "hermes, AAA cockpit health page broken. fix it."

Hermes: "Arif, I'll have OpenCode fix the AAA cockpit health page.
        Task: Investigate and fix broken health page in AAA Cockpit.tsx.
        Scope: T2 (code change, reversible). Proceed?"

Arif: "yes"

Hermes → 777-FORGE: spawn request {
  forge_id: "FORGE-20260614-002",
  target: opencode,
  task: "Fix broken health page in AAA Cockpit.tsx...",
  scope: T2
}

777-FORGE: validates → spawns OpenCode → writes witness receipt

OpenCode: investigates → finds bug → fixes → tests → reports done

777-FORGE: witnesses completion → reports to Hermes

Hermes: "Arif, done. Button onClick handler was missing. Fixed in Cockpit.tsx:42.
        Tested, built, pushed. Commit: f57b3b96."

Arif: "thanks hermes"
```

**Zero keys. Zero tokens. Pure human language. Warga AAA chain.**

---

*Forged: 2026-06-14 by FORGE (000Ω) — F13 SOVEREIGN ratified*
