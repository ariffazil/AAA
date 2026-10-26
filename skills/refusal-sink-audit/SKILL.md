---
name: refusal-sink-audit
description: "Use when a lane refuses, lectures or moralises wrongly."
version: 1.0.0
author: arifOS federation (curator)
license: private-sovereign
tags: [governance, prompt, audit, behaviour, refusal]
metadata:
  hermes:
    tags: [governance, prompt, audit, refusal]
    related_skills: [arifos-prompt-doctrine, shadow-mode, fake-governance-detection]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Refusal-Sink Audit

## When to Use

- A lane that doctrine declares open still refuses, lectures, moralises, asks permission, or offers
  a menu of options.
- Someone reports that a "filter" blocks a topic and asks you to remove it.
- You are about to edit a doctrine file to change behaviour.

## The cause hierarchy — check in this order

1. **Doctrine in a pointer file is not in the prompt.** A SOUL.md pointer table (`/root/AAA/instructions/*.md`)
   is *referenced*, never loaded. The model answers from training priors, so it refuses or lectures.
   The rule must be written into the file loaded every turn: the live SOUL body — short, imperative:
   what opens the lane, what the brakes are, what is forbidden.
2. **A plugin or hook that strips output.** Observer hooks are harmless; a stripper is a sink.
3. **A tool gate that blocks on topic.** Read its tool list first — most federation gates are scoped
   to tools (spawn, seal), not to conversation text.
4. **The provider's classifier.** `finish_reason=content_filter` (Anthropic `refusal`,
   `guardrail_intervened`) arrives as `content_policy_blocked`; the engine tries one configured
   fallback, then surfaces it. Not removable from inside the federation — report it as the residual.

## Sweep

```bash
cd /root/.hermes && for d in hooks plugins runtime mcp_servers gateway; do
  echo "### $d"
  grep -rniE "sexual|nsfw|adult content|erotic|refus|inappropriate|explicit" "$d" \
    --include='*.py' --include='*.yaml' --include='*.json' | grep -v node_modules | head -25
done
```

Surfaces, in the order that matters:

```
<HERMES_HOME>/SOUL.md                     live prompt (the only one that decides)
<HERMES_HOME>/profiles/*/SOUL.md          one inode via the /root/HERMES symlink — verify the write propagated
<HERMES_HOME>/config.yaml                 plugins.enabled / plugins.disabled, hooks.pre_tool_call
<HERMES_HOME>/runtime/membrane_v0_1.py    lane classifier + squeak stripper; check its importers
/root/AAA/federation/protocols/arifos-hermes-gate-hook.py   pre_tool_call gate (T3 = witness, no block)
/root/AAA/federation/kernel/jitu.py       sovereign brake — status must read "idle"
```

**A guard module with no importers is asleep, not load-bearing.** `grep -rn "<module>" --include='*.py'`
returning only the module and its own test means nothing loads it: do not count it as enforcement,
and do not wire it up "for completeness". Adding a stripper to prove a lane is open is backwards —
safety is behaviour, not another layer.

## Live probe — grep proves absence of text, only a request proves behaviour

```bash
set -a; . /root/.secrets/fed-zen.env; set +a
curl -s -m 120 http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer ${FED_ZEN_KEY}" \
  -d '{"model":"hermes-default","max_tokens":900,"messages":[{"role":"user","content":"<lane test>"}]}' \
  | python3 -c "import sys,json;d=json.load(sys.stdin);c=d['choices'][0];m=c['message'];print(c['finish_reason'], m.get('refusal'), repr((m.get('content') or '')[:300]))"
```

- `stop` + prose + no `refusal` field = lane open.
- `content_filter` = provider refusal; that is the honest residual.
- `length` with empty content is **truncation, not refusal** — re-probe with a larger `max_tokens`
  before concluding anything.

## Making the edit stick

1. Back up: `cp -a SOUL.md SOUL.md.bak-<date>-<why>`.
2. Patch the live body with the operative rules only (no essay).
3. Restart the unit that is **actually** live: `systemctl list-units --all | grep -i hermes` first —
   the enabled gateway may not be the unit name older docs use, and a restart script can exit 0 while
   a different (disabled) unit stays `inactive`. Then confirm `is-active` and that the bot answers
   its own identity call.
4. Verify the file survived its injection scan (`tools.threat_patterns.scan_for_threats(text,
   scope='context')` → `[]`) and is non-empty.
5. Confirm propagation: `grep -c "<new heading>" <HERMES_HOME>/profiles/*/SOUL.md`.

## Reporting rule

Report the measurement, not the intention: what you swept, what the live probe returned, what
residual remains, and what you deliberately did *not* wire up. A lane is open only when a real
request came back as prose.
