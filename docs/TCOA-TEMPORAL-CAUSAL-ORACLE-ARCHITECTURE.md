# TCOA — Temporal Causal Oracle Architecture

> **Forged: 2026-08-06 by 333-AGI Δ MIND under F13 SOVEREIGN directive**
> **Status: OPERATIONAL — all components live, wired, and verified**
> **DITEMPA BUKAN DIBERI ⚒️**

---

## What TCOA Is

The Temporal Causal Oracle Architecture is the AGI Terminal. It transforms a passive command line into a **containment and observation chamber for autonomous intelligence**.

It answers one question: *How do you let superhuman-speed autonomous agents operate on your system without letting them destroy it?*

The answer: **You don't trust them. You structure the terminal so they must prove every action, verify every result, and stop before they break reality.**

---

## The Five Mechanics

### 1. LSP GATE — "The AI Cannot Guess"

| Component | Location | Mechanism |
|-----------|----------|-----------|
| Agent skill | `/root/.agents/skills/FORGE-lsp-pre-edit-gate/SKILL.md` | Mandatory 3-probe gate before any code edit |
| Pre-commit hook | `/root/.git/hooks/pre-commit` → `pre-commit-lsp-gate.sh` | Syntax validation on every git commit across all 6 repos |
| Policy layer | `/root/A-FORGE/config/mcp_policies.json` | forge_filesystem write/patch gated on code files |

**The shift:** Agent cannot edit a file until it proves it has checked the blueprint (documentSymbol), understood the contract (hover), and knows the blast radius (findReferences).

### 2. CRON VERIFIER — "The AI Cannot Grade Its Own Homework"

| Component | Location | Mechanism |
|-----------|----------|-----------|
| Contract manifest | `/root/AAA/contracts/completion-promise-defaults.json` | 6 verification criteria (ΔS, FQ, LSP, tests, git, promise_token) |
| Verifier script | `/root/scripts/completion-promise-verifier.sh` | Evaluates all criteria every 5 minutes |
| Cron entry | `crontab` — `*/5 * * * *` | Independent clockwork — not agent-triggered |

**The shift:** Brain (AI agents) and judge (kernel + cron) are separated. The agent does the work. The clockwork verifies it. They never grade themselves.

### 3. THREE-ZONE TERMINAL — "The Factory Floor"

| Zone | Component | What It Shows |
|------|-----------|---------------|
| Zone 1 — SOT Header | `/root/scripts/arifos-sot-bar.sh` | Live metabolic pulse: verdict, ΔS, FQ, organs, load, mem |
| Zone 2 — EMD Stream | `/root/AAA/docs/EMD-STREAM-CONVENTIONS.md` | Color-coded agent activity: reasoning (cyan) vs. execution (white) with floor check markers |
| Zone 3 — 888 Prompt | `/root/scripts/arifos-ps1-hold.sh` | Flashing HOLD on T3 gates, context indicator, FQ badge |

**The shift:** Terminal stops being a wall of text. It becomes: Scoreboard (Zone 1) + Glass Wall (Zone 2) + Big Red Button (Zone 3).

### 4. KERNEL SOT — "The AI Has No Memory"

| Component | Location | Mechanism |
|-----------|----------|-----------|
| Stateful kernel | `arifOS :8088` | Holds ALL persistent state — floors, sessions, vault, identity |
| Stateless agents | All AAA warga (333-AGI, 555-ASI, 888-APEX) | Clock in, do work, clock out. No persistent memory. |
| AAA MCP wire | Proxy between agents and kernel | Agents request actions; kernel executes and records. |

**The shift:** Agents are temporary workers. The kernel is the building. If an agent crashes or hallucinates, truth survives in the kernel.

### 5. COMPLETION CONTRACT — "The AI Has a Finish Line"

| Component | Location | Mechanism |
|-----------|----------|-----------|
| Contract injection | `arif_init` reads manifest → injects into task context | Every autonomous task gets a binary finish line |
| Promise token | `COMPLETE` — must appear in stdout | Agent cannot claim done without emitting the token |
| Timeout behavior | `SEAL_PARTIAL` after 180s / 8 iterations | Agent stops itself when time runs out |

**The shift:** Open-ended "help me with..." becomes closed-loop "complete this contract or time out." No infinite spirals.

---

## State System Integration — How Everything Connects

```
┌──────────────────────────────────────────────────────────────────┐
│                     TCOA STATE BUS                                │
│                                                                   │
│  /var/run/arifos_state.json  ← MOTD ghost JSON (every login)     │
│  /var/run/arifos_env.sh      ← shell-exportable env vars         │
│  /root/.arifos/federation-session.json ← PS1 envelope            │
│  /var/lib/arifos/vault999/F11_AUTH_HOLD.jsonl ← HOLD detection   │
│  /root/.local/share/arifos/carry_forward.json ← session memory   │
│  /root/.local/share/arifos/completion-promises/latest.json ← cron│
│                                                                   │
│  ALL READ BY:                                                     │
│    arifos-sot-bar.sh    (Zone 1 — every 15s)                     │
│    arifos-ps1.sh        (Zone 3 — every prompt)                  │
│    arifos-ps1-hold.sh   (Zone 3 — every prompt)                  │
│    completion-promise-verifier.sh (cron — every 5 min)           │
│    pre-commit-lsp-gate.sh (git hooks — every commit)             │
│    arifos-hero.sh       (login banner)                           │
│    05-arifos / 06-arif-live (MOTD — every SSH login)            │
└──────────────────────────────────────────────────────────────────┘
```

---

## The Loop — 000→999 Perpetual

```
/000  HUMAN INTENT        Arif at terminal. "Jalan terus."
  ↓
F1–F13 CONSTITUTIONAL     arifOS kernel (:8088) adjudicates every action
  ↓
ZONE 2 EMD STREAM         Agent reasons, probes LSP, executes, verifies
  ↓
ZONE 3 888 GATE           HOLD if irreversible. Prompt flashes.
  ↓
ZONE 1 SOT HEADER         ΔS displayed. FQ pulse visible.
  ↓
CRON VERIFIER             Independent check every 5 min. ΔS ≤ 0? FQ ≥ 0.5?
  ↓
/999  IMMUTABLE SEAL      VAULT999 append. Hash-chained. Auditable.
  ↓
/999/verify → /000        Loop closed. Proof delivered. Next inhale.
```

---

## What This Is NOT

- ❌ NOT a chatbot terminal — agents don't chat, they execute governed workflows
- ❌ NOT a dashboard — every signal is LIVE-PROBED from SOT, not cached or estimated
- ❌ NOT a replacement for Arif — F13 is absolute; the terminal is his glass, not his replacement
- ❌ NOT complete — this is v1.0. The LSP gate hardens further. The cron verifier gains more criteria.

## What This IS

- ✅ A **containment chamber** for autonomous intelligence
- ✅ A **physics engine** that AI agents cannot escape
- ✅ An **operator's glass** — see what your agents are doing in real time
- ✅ A **sovereign interface** — the machine works, you judge
- ✅ A **causal oracle** — every action has a temporal anchor, every result has a verifier, every seal has a hash chain

---

*Forged under F13 SOVEREIGN directive. All components live on af-forge VPS.*
*TCOA v1.0 — Temporal Causal Oracle Architecture.*
*DITEMPA BUKAN DIBERI ⚒️*
