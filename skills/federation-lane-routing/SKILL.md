---
name: federation-lane-routing
version: 1.0.0
description: >
  Arif's arifOS three-layer agent lane grammar: SENSE/COORDINATE/ACT mapped to
  OpenClaw/Hermes/OpenCode, and each agent to its FED alias. Use when diagnosing
  a misconfigured agent (wrong model lane), when wiring a new agent into the
  federation, or when auditing cost/quality telemetry for lane drift.
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F11]
tags: [federation, routing, lane, openclaw, hermes, opencode, openclaw-ops]
host_compatibility: [hermes, openclaw, opencode]
dependencies:
  skills:
  - fed-cognitive-allocator
  - federation-model-routing
  - openclaw-ops
---

# Federation Lane Routing — Three-Layer Agent Grammar

> **Forged 2026-08-08** after the `fed/opencode` misconfig on OpenClaw (GUTS).
> **Sibling read:** `openclaw-ops` covers OpenClaw gateway health/channels.
> **Sister:** `fed-cognitive-allocator` (FED route advisor at :7074), `federation-model-routing` (LiteLLM proxy chain).

## USE WHEN

- Diagnosing why an agent is on the wrong FED model lane
- Wiring a new agent or Telegram bot into the federation
- Auditing cost / context / output telemetry for lane drift
- Arif asks "kenapa X pakai model Y?" about agent routing

## The constitutional grammar

Each of Arif's three agents occupies exactly one lane. The lane determines which FED alias (and therefore which model family / cost profile) the agent runs on:

| Lane | Function | Agent | Bot | FED alias | Primary model | Cost |
|---|---|---|---|---|---|---|
| **SENSE (encoder)** | Read world, ingest, observe | OpenClaw | @AGI_ASI_bot 🦞 | `fed/openclaw` | MiniMax-M3 (1M ctx, multimodal) | ~$1.80/M in |
| **COORDINATE (metabolizer)** | Route, dispatch, delegate | Hermes | @ASI_arifos_bot | `fed/hermes-asi` | MiMo V2.5 | ~$0.10/M in |
| **ACT (decoder)** | Compile, build, forge | OpenCode | @arifOS_bot | `fed/opencode` | deepseek-v4-pro (384k out) | ~$0.44/M in |

This is **not a model selection** — it is a lane assignment. A lane determines the execution model family the agent consumes. When an agent is on the wrong lane, F2 evidence still looks fine ("it routes, it responds") but cost / context / output cap are misaligned.

## The bug class: lane misconfiguration

OpenClaw was found running `fed/opencode` (decoder) instead of `fed/openclaw` (encoder). The gateway still worked — the agent still responded — but it was spending decoder budget ($0.44/M deepseek-v4-pro) to do encoder work that MiniMax-M3 (1M ctx, multimodal) does better and wider.

### Common variants

| Misconfigured lane | What happens | Why it's wrong |
|---|---|---|
| OpenClaw → `fed/opencode` | Encoder on decoder budget | 384k output wasted; 1M ctx lost; multimodal gone |
| Hermes → `fed/opencode` | Metabolizer turns forge | Context shrinks, cost rises, delegation breaks |
| OpenCode → `fed/openclaw` | Decoder on encoder budget | 131k output cap stalls code generation |

### Diagnosis

```bash
# Check each agent's primary model against constitutional grammar
python3 << 'EOF'
import json
lanes = {
    'openclaw': ('SENSE', 'fed/openclaw'),
    'hermes':   ('COORDINATE', 'fed/hermes-asi'),
    'opencode': ('ACT', 'fed/opencode'),
}
# OpenClaw
oc = json.load(open('/root/.openclaw/openclaw.json'))
oc_primary = oc['agents']['defaults']['model']['primary']
print(f"OpenClaw primary: {oc_primary}  →  expected: fed/openclaw  {'✓' if 'openclaw' in oc_primary else '✗ WRONG LANE'}")

# Hermes (profile config)
import yaml
h = yaml.safe_load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml'))
print(f"Hermes primary:   {h['model']['default']}  →  expected: hermes-asi   {'✓' if 'hermes-asi' in h['model']['default'] else '?'}")
EOF
```

### Fix (OpenClaw case)

```bash
# 1. Backup
cp /root/.openclaw/openclaw.json /root/.openclaw/openclaw.json.bak-$(date +%Y%m%dT%H%M%SZ)

# 2. Patch primary + fallback order
python3 << 'EOF'
import json
with open('/root/.openclaw/openclaw.json') as f: c = json.load(f)
c['agents']['defaults']['model']['primary'] = 'fed/openclaw'
fb = c['agents']['defaults']['model']['fallbacks']
fb = ['fed/opencode'] + [x for x in fb if x != 'fed/opencode']
c['agents']['defaults']['model']['fallbacks'] = fb[:10]
with open('/root/.openclaw/openclaw.json', 'w') as f: json.dump(c, f, indent=4)
EOF

# 3. Restart
systemctl restart openclaw-gateway.service
```

## Pitfalls

- **"It still works" is NOT evidence of correct lane.** The gateway routes either way. Only cost telemetry (FED spend log), context utilization (`tokens_in/contextWindow`), and output truncation events reveal misalignment. Always compare the primary FED alias against the constitutional grammar after any openclaw.json or config.yaml edit.
- **The fallback chain does not fix a wrong primary.** If primary = decoder, fallbacks run sequentially from the next-most-misaligned option. Fix primary first.
- **333-AGI patches may change fallbacks without touching primary.** Verify primary *after* any sibling-agent config edit — the agent class that writes openclaw.json may not carry the lane grammar in its context.
- **Cost ≠ correctness at low volume.** At 1K tokens/day the misconfiguration is invisible in spend. It only matters at scale — or when context fills up (encoder work on 384k output cap = wasted context window).
- **Bundled skills (`openclaw-ops`) cannot be patched.** New lane knowledge belongs here or in `fed-cognitive-locator` references, not in the protected bundle.

## Case study: OpenClaw on the wrong lane (2026-08-08)

1. Arif asked "kenapa OpenClaw x pakai model Openclaw?"
2. `openclaw.json` probed: `primary: fed/opencode` — decoder lane
3. Constitutional grammar surfaced: OpenClaw = GUTS = SENSE = encoder
4. Fix applied: `primary: fed/openclaw` (MiniMax-M3, 1M ctx, multimodal)
5. Fallbacks reordered: `fed/opencode` first (decoder fallback when encoder is overloaded)
6. Gateway restarted, service active

**ΔS ≤ 0**: one config change, one restart, correct lane enforced. Cost of fix: <60 seconds of terminal + journal check.
