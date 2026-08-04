---
id: aaa-setup-help
name: AAA-setup-help
version: 1.0.0
description: "Guide the sovereign or operator through any setup, configuration, or deployment process step by step. One atomic action per response, with a 'Still remaining' list that never exceeds 8 items. Use when Arif says 'help me set up', 'walk me through', 'setup-help', 'configure X', or any guided process that requires tracking remaining steps across multiple turns."
owner: 333-AGI
risk_tier: low
floor_scope: [F1, F2, F4, F7]
autonomy_tier: T1
forged: 2026-08-04
forged_by: 333-AGI
trigger_when:
  - "help me set up"
  - "walk me through"
  - "setup help"
  - "configure step by step"
  - "guide me through"
  - "setup-checklist"
tags: [setup, guided, step-by-step, human-in-loop, onboarding]
---

# AAA-setup-help — Guided Setup with Progress Tracking

> **Pattern origin:** David Ondrej's `setup-help` skill (davidondrej/skills).
> **Adapted for:** arifOS Federation — constitutional guardrails, Malaysian context.
> **Doctrine:** One atomic step per response. Track remaining steps. Never exceed 8 visible items. Never lose internal state.

## When to Activate

Activate this skill when Arif (or any operator) asks for **guided step-by-step help** through a process. The process could be:

- Deploying a new service or site
- Configuring a new tool or MCP server
- Setting up a development environment
- Running a multi-step repair or recovery
- Any task that spans multiple agent-response turns

**Do NOT activate for:** single-command tasks, pure information queries, or tasks the agent can complete alone without human interaction.

## Response Format (EVERY response in this mode)

```
🔹 **Current step:** [ONE atomic action — 1-2 lines max]

[Brief instruction, command to run, or field to fill. Plain language.
 If it has sub-steps, it's too big — split it.]

----

📋 **Still remaining:**
1. [Next step headline — few words only]
2. [Step after that]
3. ...
(Never more than 8 items. If >8 remain, merge later items into phase-level headlines.)

🧘 **Zen:** progress=[N]/[total] | ΔS=[-1 to 1]
```

## Rules

### Before the First Step
1. Build a **complete internal checklist** from the request, repo docs, current state, and any discovered prerequisites.
2. Classify each step: `manual` (needs human), `agent` (agent can do), `wait` (needs external event).
3. Present the first step immediately. Do NOT dump the full checklist — the "Still remaining" list handles progressive disclosure.

### During the Process
- **ONE atomic action per response.** A single click, field, command, or decision. Not a checklist.
- **"Still remaining" list ≤ 8 items.** Internally track ALL unfinished steps. If >8 remain, show nearest steps individually and merge later ones into broader phase-level items. NEVER silently drop a required step.
- **If a new required step is discovered mid-process**, add it to "Still remaining" immediately in the correct order.
- **Before every response**, audit current step + "Still remaining" against your internal checklist. If any unfinished step is missing, fix the list first.
- **Only give instructions for the current step.** Do not front-load detail into remaining items. Detail arrives when the step becomes current.
- **Verify completion** of each step before advancing. If the human reports a problem, pause and troubleshoot before continuing.

### When Finished
- When the "Still remaining" list is empty, declare setup complete.
- Do NOT show the list. Instead: `✅ Setup complete. [summary of what was accomplished].`
- Seal the setup session receipt to VAULT999.

### Agent Steps
- When a step is classified `agent` (the agent can execute it independently), offer to run it: "I can handle this step. Proceeding..." — then execute it.
- After the agent step completes, advance to the next step automatically.

## Anti-Patterns

- ❌ Dumping the full checklist upfront — overwhelming
- ❌ Multiple actions in one "Current step" — defeats the purpose
- ❌ "Still remaining" list with 12+ items — max 8, always
- ❌ Front-loading commands/URLs/values into remaining items — detail only arrives at Current step
- ❌ Skipping verification of completed steps
- ❌ Losing internal state between turns — the internal checklist is persistent

## Session Integration

- Internal checklist persists in session context (not written to disk unless sealed)
- After setup completion, seal a receipt: `AAA-setup-help::{task}::steps={N}::completed={timestamp}`
- Use `arifflow_flow_ingest` for each completed step (step_type="Execute" or "Verify")

## Example

```
User: "Help me set up a new Cloudflare Tunnel for arif-fazil.com"

Agent:
🔹 **Current step:** Create the tunnel in Cloudflare dashboard
Go to https://one.dash.cloudflare.com/ → Zero Trust → Networks → Tunnels → Create a tunnel.
Name it `arif-fazil-com`. Click "Save". Do NOT install the connector yet.

----

📋 **Still remaining:**
1. Install cloudflared connector on VPS
2. Configure tunnel config.yml
3. Point DNS CNAME to tunnel
4. Test the tunnel endpoint
5. Wire into Caddy reverse proxy
6. Verify HTTPS and health

🧘 Zen: progress=1/7 | ΔS=-0.3
```
