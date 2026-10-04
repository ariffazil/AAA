# Agent-Card Registry — Per-Runtime Requirements (verified 2026-08-09)

Live-probed against `/root/AAA/a2a-server/agent-cards/` (canonical, schema v2.2.0) and `/root/.config/federation-models.json`. Use when asked "what agent cards does runtime X need" or when wiring a new harness into the federation.

## The 4-layer card model

Every runtime needs: **harness card** (runtime identity) + **identity/lane binding** + **forge/FI tier** (execution) + **extension/function** (peripheral) — plus the shared kernel-skill set and the lane's role-binding skill.

## Per-runtime card map

| Runtime | Harness card | Identity binding | Forge / FI | Extension / Function | Model (federation-models.json) |
|---|---|---|---|---|---|
| **Hermes** | — (edge bridge) | `identity/555-ASI` (Ω HEART) + polymorphic 333/888 | — | `extensions/hermes-asi.json` + `extensions/hermesarifos-bot.json` + `roles/hermes-ops.json` | `minimax/MiniMax-M3` |
| **OpenClaw** | `harnesses/openclaw.json` (topological_role=Metabolizer) | `identity/333-AGI` (Δ MIND) | — | `functions/openclaw.json` (gateway, model MiniMax-M3) | `deepseek/deepseek-v4-pro` |
| **OpenCode** | `harnesses/opencode.json` (PRIMARY; `replaces: [codex, claude-code]`; `proxy_for_harnesses` = 10 vendors) | `identity/333-AGI` | `forge/fi-001-opencode.json` (FI-001) | `agents/opencode/` full set (SOUL, identity, KERNEL.md, identity.key…) | `litellm-federation/opencode` ⚠️ FED-dependent |
| **Grok Build** | `harnesses/grok-build.json` (FI-008, xAI) | 333-AGI (via species) | — | `agents/grok-build/AGENTS.md` (`/root/.grok/`) — **no identity.json/key minted** | `xai/grok-4.5` |
| **Kimi Code** | `harnesses/kimi-code.json` (FI-003) | — | `forge/fi-008-kimi-code.json` | `agents/kimi-code/` (agent-card + WARGAAA_CARD.md) | `kimi-k3` |
| **Claude Code** | `harnesses/claude-code.json` (FI-002, BIJAKSANA — spawnable by Hermes+OpenClaw, 2026-08-08) | — | — | `agents/forge-bot/agent-card.json` (bound 333-AGI) | `deepseek/deepseek-v4-pro` |
| **Codex** | `harnesses/codex.json` (FI-004) | — | — | — (no `agents/codex/` folder) | `deepseek/deepseek-v4-pro` |
| Copilot / Gemini-CLI / Qwen-Code / Antigravity / Continue / Aider | harness card each (FI-005/007/011/009/010/006) | — | — | — | copilot=`z-ai/glm-5.2`, others vendor-native |

## Role cards (AAA-side ops, not runtime cards)

`roles/aaa-engineer.json` (11 skills), `roles/aaa-auditor.json` (6), `roles/aaa-architect.json` (5), `roles/aaa-gateway.json` (6), `roles/hermes-ops.json` (10). These govern how AAA dispatches work to runtimes, not what a runtime needs to boot.

## Species bindings in harness cards (genome wiring)

| Harness | species_id | primary_loci | expression_weights (excerpt) |
|---|---|---|---|
| opencode | opencode-zen | 222, 333, 777 | 222=0.9, 333=0.85, 777=0.95, 888=0.0, 999=0.0 |
| grok-build | (via species) | generator | topological_role=Generator |

## Kernel skills every runtime must carry (9 substrate-primitive)

`KERNEL-reality-skills` (F2) · `KERNEL-sovereign-recognize` (F13) · `KERNEL-session-inhabit` (INIT→OBSERVE→JUDGE→SEAL) · `RSI-recursive-improvement` (ΔS<0) · `KERNEL-trinity-33` · `SHADOW-diagnostic` · `CLAIM-verification-gate`. Embedded in every card's `skills[]` (grok-build and hermes-asi both list the 7 in their tails).

Role-binding skills by lane: 333-AGI=`role-binding-delta` (Δ MIND, loads arifos-mcp-federation/agent-landscape/paradox-engine) · 555-ASI=`role-binding-omega` (Ω HEART, loads humility-godel/sovereign-entropy-guard/tiered-memory/dream-engine) · 888-APEX=`role-binding-phi` (ΦΙ JUDGE, narration/request only — never final verdict).

## Probe recipes (how this map was built)

```bash
# 1. Full canonical tree
find /root/AAA/a2a-server/agent-cards -type f | sort

# 2. Per-card key fields (id/class/bound_to/tier/model)
python3 - <<'EOF'
import json, glob
for f in sorted(glob.glob('/root/AAA/a2a-server/agent-cards/harnesses/*.json')):
    d = json.load(open(f))
    print(d.get('id'), '|', d.get('class') or d.get('role'), '|', d.get('bound_to'), '|', d.get('tier'), '|', d.get('model'))
EOF

# 3. Live model map (deprecated AGENT_MODEL_MAP.json → federation-models.json)
python3 - <<'EOF'
import json
d = json.load(open('/root/.config/federation-models.json'))
for a in d.get('agents', []):
    print(a.get('agent_id'), '→', a.get('primary_model'))
EOF
```

## Gaps found (2026-08-09 audit)

- `agents/grok-build/` and `agents/codex/` have NO identity.json / identity.key / agent-card.json — only harness cards. If "complete runtime" is required, mint the identity files (mirror `agents/opencode/` layout: identity.json + identity.key + agent-card.json).
- `aaa-cockpit.json` sits at tree root (id field absent — display card, never adjudicates).
- Legacy `/root/AAA/agent-cards/agents/identity.json` exists but is part of the superseded tree — do not treat as canonical.
