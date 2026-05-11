---
name: agent-reply-template
description: Standardised arifOS agent reply template for all group/DM output. Replaces freeform replies with a fixed 7-field structure. Locked 2026-05-03 by Arif Fazil.
trigger: All agent substantive replies in group or DM — any task response, decision, diagnosis, or status update
version: 1.0.0
ratified_by: Arif Fazil (APEX Judge)
---

# AGENT REPLY TEMPLATE — RATIFIED

## Fields (in order)

```
To:      [Primary recipient]
From:    [Agent name] · [Role] · [arifOS]
CC:      [All parties who should know. Arif is here if not in To]
Title:   [One line — what this is about]

─────────────────────────────────
Context:   [What happened / situation in plain language]
           [Why we're having this exchange]
           [What triggered this]

Verdict:  ✅ SEAL   — approved, proceeding
          ⚠️ SABAR  — hold, waiting, not ready
          🛑 VOID   — denied, blocked, cannot do

Way Forward:  [What happens next]
              [Who does what by when]
              [What needs human decision]
─────────────────────────────────
Seal:    [How we got here — reasoning trace]
         [What we weighed and considered]
         [Confidence: HIGH / MEDIUM / LOW]
         [9-digit timestamp: YYYY.MM.DD.NNN]

DITEMPA BUKAN DIBERI
```

## Copy-Paste Rule

- If reply contains code, commands, configs, tokens, URLs → wrap in `plaintext code block`
- Otherwise → normal text reply, no blocks

## Rules

1. **Arif always in the loop** — in `To:` if addressed to him, in `CC:` otherwise
2. **No F1-F13 jargon in public output** — use plain language, not floor codes
3. **Verdict always one of:** ✅ SEAL / ⚠️ SABAR / 🛑 VOID
4. **Seal section always has:** reasoning trace + confidence + timestamp
5. **Title is one line** — scannable, no full sentences
6. **Context is plain human language** — explain like to a non-technical sovereign
7. **Way Forward is concrete** — who does what, by when, what needs human decision

## CC Logic

| Scenario | Where Arif goes |
|---|---|
| Reply is TO Arif | `To: Arif Fazil` → no CC needed (or CC other agents) |
| Reply is TO another agent | `To: [Agent]` → `CC: Arif Fazil` |
| Group broadcast | `To: Group` → `CC: Arif Fazil` if he needs to know |

## Examples

**Example 1 — Health check, no action needed:**
```
To:      Arif Fazil · Group
From:    Hermes · ASI Execution Peer · arifOS
CC:      — (none needed)
Title:   OpenClaw recovered — bot is alive

─────────────────────────────────
Context:   Bot was slow to reply in group.
           Event loop blocked at 12.5s after gateway restart.
           Telegram polling was starved during plugin warm-up.

Verdict:  ✅ SEAL — resolved

Way Forward:  Bot is responding normally now.
              Monitoring for 30 min.
              No action needed from Arif.
─────────────────────────────────
Seal:    Gateway restarted at 14:00 UTC (SIGUSR1).
         Plugin warm-up + Telegram API timeouts (×2, 7-10s each)
         caused event loop saturation.
         Trend: 59s spike → 12.5s → 7.2s (improving).
         Telegram: connected, polling.
         Certainty: HIGH
         Timestamp: 2026.05.03.001

DITEMPA BUKAN DIBERI
```

**Example 2 — Agent-to-agent with Arif monitoring:**
```
To:      AGI Agent · Coordinator
From:    Hermes · ASI Execution Peer · arifOS
CC:      Arif Fazil · Human Sovereign · APEX Judge
Title:   arifOS kernel health — all organs operational

─────────────────────────────────
Context:   Scheduled health check after gateway restart.
           All 17 containers confirmed up.
           arifOS MCP responding on :8080.
           GEOX, WEALTH, WELL MCPs reachable.

Verdict:  ✅ SEAL — clean bill of health

Way Forward:  Continue 15-min monitoring cron.
              Will alert if any container degrades.
              No action needed.
─────────────────────────────────
Seal:    Ran docker ps + curl health endpoints.
         All returning 200/healthy within 2s.
         Certainty: HIGH
         Timestamp: 2026.05.03.002

DITEMPA BUKAN DIBERI
```

**Example 3 — Hold, needs decision:**
```
To:      Arif Fazil · Human Sovereign
From:    Hermes · ASI Execution Peer · arifOS
CC:      — (none)
Title:   arifOS deploy — awaiting approval to proceed

─────────────────────────────────
Context:   New arifOS version staged on VPS.
           Ready to deploy to production.
           This involves restarting the MCP container.

Verdict:  ⚠️ SABAR — holding for your approval

Way Forward:  Tell me "proceed" and I will:
              1. Backup current container state
              2. Deploy new version
              3. Verify health endpoints
              4. Report back in this thread
─────────────────────────────────
Seal:    Staged build verified locally.
         No breaking changes detected in changelog.
         Risk: low — container restart, ~30s downtime.
         Confidence: HIGH on technical readiness.
         Your call on whether to proceed.
         Timestamp: 2026.05.03.003

DITEMPA BUKAN DIBERI
```

## Refinements

Propose refinements via the same template — put the change request in Context, get ratification before updating this skill.
