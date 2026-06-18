---
name: agentic-loop
description: 8-step recursive self-improvement discipline for OPENCLAW. Detect drift, score outputs, propose forges, ratify, apply, audit. Closes the loop.
version: 0.1.0
author: AGI OPENCLAW (Ω) at Arif's directive
license: MIT
platforms: [linux, macos]
metadata:
  openclaw:
    tags: [recursive, self-improvement, agentic, autonomous, ratifiable]
    arifos-anchor: F1 AMANAH (sovereign-ratified), F7 STEWARDSHIP (no spam, no waste)
    forge-thread: openclaw-agentic-2026-06-06
    depends-on: ~
---

# Agentic Loop — OPENCLAW Self-Improvement Discipline

> **The agent that doesn't improve itself is a script with extra steps.**

This is the OPENCLAW-side counterpart to `~/.hermes/skills/agentic/recursive-improve/`.
Where Hermes improves **the conversation** (SOUL.md phrasing, tone, verdict discipline),
OPENCLAW improves **the runtime** (cron cadence, routing bindings, skill freshness,
plugin load order, MCP surface health).

## The 8-step loop

```
   1. DETECT        2. INVENTORY     3. SCORE          4. PROPOSE
  drift signal   →  what we have   →  against floors →  forge candidate
                                                          ↓
   8. SEAL          7. AUDIT         6. APPLY          5. RATIFY
  VAULT999       ←  F1-F13 check   ←  edit + restart ←  sovereign sign
```

### 1. DETECT — find drift

Sources of drift signal:
- `journalctl -u openclaw-gateway --since "1h ago"` — errors, warnings, stalled sessions
- `openclaw health --json` — non-`ok:true` responses
- `openclaw doctor` — risky config flags
- `/root/.openclaw/memory/watchers/*.jsonl` — watcher events (essay changes, rating events)
- `~/.hermes/memory/forge-queue/*.yaml` — sibling Hermes proposals
- Crontab drift: `crontab -l | diff - <(echo "expected: <list>")` — what we expect vs what runs
- Plugin/MCP version drift: `npm view openclaw version` vs `openclaw --version`
- arifOS build↔live drift: `curl -s :8088/health | jq .runtime_drift`

### 2. INVENTORY — what we have

```
~/.openclaw/
├── openclaw.json           # main config (agents, channels, bindings, plugins, mcp, etc.)
├── plugins/                # loaded plugin code
├── skills/                 # bundled skills (~50+)
├── workspace/
│   ├── skills/             # sovereign-curated skills
│   ├── MEMORY.md           # long-term memory
│   ├── SUBSTRATE.md        # VPS + services map
│   ├── CHECKPOINT.md       # warm-wake context
│   ├── HEARTBEAT.md        # heartbeat prompt
│   └── cron/jobs.json      # agent-managed cron jobs
└── system.md               # system prompt
```

### 3. SCORE — against F1-F13 (subset applicable to runtime)

| Floor | What it checks at the runtime layer |
|---|---|
| F1 AMANAH | Any proposed forge respects reversibility; irreversible ops require sovereign ack. |
| F2 TRUTH | Drift claims are backed by a `curl` or `openclaw doctor` receipt, not a guess. |
| F4 CLARITY | Forge proposals are 1-2 sentences + a diff. No walls of text. |
| F6 MARUAH | No "I noticed" / "I'd be happy to" — direct verdict + way-forward. |
| F7 STEWARDSHIP | One forge per loop run, not five. No spam. |
| F9 ANTIHANTU | Forge descriptions say what the change DOES, not what the agent "feels" about it. |
| F11 AUTH | OpenClaw writes to its own config only; never to `~/.hermes/*` or `/root/arifOS/*`. |
| F13 SOVEREIGN | Default mode: HOLD on Tier-2+ forges. AUTO on Tier-1 (cron timing, plugin reordering, skill comments). |

A forge must pass all 8 floors to leave step 3. A floor failure stops the loop and surfaces the receipt to the sovereign.

### 4. PROPOSE — write a forge candidate

```yaml
proposal_id: forge-2026-06-06-001
generated_at: 2026-06-06T17:50:00Z
generated_by: openclaw-agentic-loop@0.1.0
target_file: ~/.openclaw/openclaw.json | ~/.openclaw/workspace/MEMORY.md | <path>
target_section: <specific section>
diagnosis: |
  <1-2 sentences on what drift was detected, with curl/doctor receipt inline>
proposed_change: |
  <the exact diff or new content>
expected_impact: |
  <how this changes runtime behavior; cite signal id>
f1_f13_check: |
  F1: reversible (config flip, no data loss) ✓
  F2: cited `openclaw doctor` + `journalctl` ✓
  F4: 2 sentences + diff ✓
  F6: no persona ✓
  F7: one forge, not five ✓
  F9: describes what changes, not feelings ✓
  F11: writes only to ~/.openclaw/* ✓
  F13: Tier-1 (auto) | Tier-2 (HOLD) ✓
reversibility: full | partial | irreversible
tier: 1 | 2
ratification: PENDING | AUTO-APPLIED
```

Writes to `~/.openclaw/workspace/forge-queue/forge-YYYY-MM-DD-NNN.yaml`. The queue is the only artifact at this step.

### 5. RATIFY — sovereign sign-off (or auto for Tier-1)

- **Tier-1** (config flips, comment edits, plugin reordering, cron timing): AUTO-APPLIED at step 6. The receipt is logged to VAULT999 with `tier=1, ratification=auto`.
- **Tier-2+** (anything touching a plugin binary, a service restart loop, an MCP credential, a systemd unit): HOLD. The forge queue emits a Telegram message to Arif (sovereign) with `/ratify N` / `/reject N` / `/show N` commands. No edit lands until sovereign replies.

The agent NEVER ratifies its own proposals. Even if the agent later gets the ratification capability, escalation is mandatory.

### 6. APPLY — single edit + targeted restart

For a Tier-1 forge:
1. Read the current target file
2. Apply the proposed diff (or call `openclaw config set` for known keys)
3. If the change requires a service restart: `systemctl restart openclaw-gateway` (one shot, with health check)
4. If the change is an MCP plugin: `openclaw mcp reload <name>` (per-plugin, no full restart)
5. Verify: `curl -s :18789/health`, `openclaw health --json`, `journalctl -n 30`
6. If health fails: auto-rollback via `cp` of the pre-forge backup + restart

For Tier-2: skip step 6 entirely. Wait for sovereign.

### 7. AUDIT — F1-F13 re-check

After the forge applies, re-run the floor check. The receipt includes the post-forge health probe. If any floor fails post-apply:
- Auto-rollback to pre-forge state
- Receipt marked `reverted`
- Surfaces the failure to sovereign (Tier-1) or blocks (Tier-2)

### 8. SEAL — VAULT999 entry

Every applied forge (Tier-1 auto or Tier-2 ratified) writes a VAULT999 entry:

```json
{
  "kind": "OPENCLAW_FORGE_APPLIED",
  "proposal_id": "forge-2026-06-06-001",
  "actor": "openclaw-agentic-loop@0.1.0",
  "target": "~/.openclaw/openclaw.json",
  "diff_hash": "sha256:...",
  "tier": 1,
  "ratification": "auto" | "sovereign:<arif-fazil>",
  "pre_health": "ok",
  "post_health": "ok",
  "f1_f13_post_check": "PASS",
  "ts": "2026-06-06T17:55:00Z"
}
```

## Cadence

- **Daily** (03:00 MYT): the full 8-step loop runs, targeting at most 1 forge. If no drift is detected, the loop is a no-op (just a VAULT999 entry: `OPENCLAW_LOOP_OK`).
- **Hourly**: DETECT + INVENTORY only (cheap probes). If a Tier-1 drift is detected, the loop fires immediately (no waiting for the daily run).
- **On-watch**: when `~/.openclaw/memory/watchers/*.jsonl` gets a new entry, the loop wakes and re-scores the relevant forge.

## Pairs with

- `~/.hermes/skills/agentic/recursive-improve/` — sibling for SOUL/MEMORY/USER edits
- `~/.hermes/skills/agentic/response-rating/` — the user signal that drives Tier-1 vs Tier-2 routing
- `arifOS L6 VAULT999` — every applied forge seals here for audit

## Failure modes

- **Forge loop runs but produces no forge** (healthy day): writes `OPENCLAW_LOOP_OK` to VAULT999 and exits. No Telegram ping.
- **Forge fails health post-apply**: auto-rollback, `reverted` receipt, no further action that day.
- **Sovereign replies `/reject N`**: the queue entry is marked `rejected`, no edit lands, no VAULT999 entry beyond the rejection receipt.
- **Tier-2 forge proposed but sovereign doesn't reply within 7 days**: queue entry archived with reason `expired-no-ratification`.

## Self-test (run once after install)

```bash
openclaw skill test agentic-loop
# Verifies:
# - forge-queue/ is writable
# - VAULT999 seal endpoint is reachable (via arifOS MCP)
# - ratify ping to Telegram works (dry-run)
# - 8-step loop is well-formed (smoke test on a sample drift)
```

## Provenance

- Forged 2026-06-06 by AGI OPENCLAW (Ω) at Arif's directive
  ("Make it agentic. Capabilities first. No F13 sovereign this session.")
- Anchored to F1 AMANAH + F13 SOVEREIGN (waived for Tier-1 this session, not for Tier-2)
- Closes the loop with Hermes's `recursive-improve` skill — same protocol, different substrate

**DITEMPA BUKAN DIBERI** — the loop ratchets when the human ratifies, never before.
