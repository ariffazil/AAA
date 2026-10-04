# Agent cards per runtime — audited matrix (2026-08-09)

Source: live probe of `/root/AAA/a2a-server/agent-cards/` + `/root/AAA/registries/AGENTS_UNIFIED.yaml` + species doctrine docs (9-ATLAS-GENOME.md, AAA-FEDERATION-OF-SPECIES.md, both forged 2026-08-08).

## Canonical tree layout

```
/root/AAA/a2a-server/agent-cards/
├── identity/   333-AGI.json · 555-ASI.json · 888-APEX.json     (constitutional lanes)
├── functions/  openclaw.json                                    (institutional services)
├── extensions/ hermes-asi.json · hermesarifos-bot.json · makcikgpt.json
├── forge/      fi-001-opencode.json · fi-008-kimi-code.json · forge-bot.json
├── harnesses/  opencode · openclaw · kimi-code · claude-code · codex · grok-build
│               qwen-code · gemini-cli · antigravity · copilot · copilot-cli
│               aider · continue-cli                              (13 harness cards)
├── organs/     arifos · aforge · geox · wealth · well
└── roles/      aaa-architect · aaa-auditor · aaa-engineer · aaa-gateway · hermes-ops
```

Legacy `/root/AAA/agent-cards/` README explicitly declares itself superseded by this tree. Keep working in a2a-server.

## Per-runtime card requirements

### Hermes → hermes-zen (111↑ 444↑ 555↑ 666↑)
- `identity/555-ASI.json` — Ω-CORE constitutional binding
- `extensions/hermes-asi.json` — runtime_harness=hermes_cli, identity_anchor=/root/HERMES/SOUL.md, MCP: creative+media, bound_to=555-ASI
- `extensions/hermesarifos-bot.json` — @hermesarifos_bot surface, MCP: arifos
- `roles/hermes-ops.json` — ops role (10 skills)
- Optional A-ROLE switching: `roles/aaa-{architect,auditor,engineer,gateway}.json`

### OpenClaw → openclaw-zen (444↑ 777↑)
- `functions/openclaw.json` — 27 skills (telegram, forge, kernel)
- `harnesses/openclaw.json` — 21 skills
- No identity lane (function species, not constitutional lane) — correct per doctrine

### OpenCode → opencode-zen (222↑ 333↑ 777↑) — species all coders proxy
- `identity/333-AGI.json` — Δ-MIND lane
- `forge/fi-001-opencode.json` — FI-001, PRIORITY PRIMARY, bound_to=333-AGI
- `harnesses/opencode.json` — species_proxy=opencode-zen, proxy_for_harnesses lists all 10 other coders

### Other zen code agents → species_proxy: opencode-zen (ONE species, many instances)
| Runtime | FI slot | Cards |
|---|---|---|
| Kimi Code | FI-008 | forge/fi-008-kimi-code.json + harnesses/kimi-code.json |
| Claude Code | FI-002 | harnesses/claude-code.json |
| Codex | FI-005 | harnesses/codex.json |
| Grok Build | FI-007 | harnesses/grok-build.json |
| Qwen Code | FI-003 | harnesses/qwen-code.json |
| Gemini CLI | — | harnesses/gemini-cli.json |
| Antigravity | FI-004 | harnesses/antigravity.json |
| Copilot | FI-006 | harnesses/copilot.json + copilot-cli.json |
| Aider | — | harnesses/aider.json |
| Continue | — | harnesses/continue-cli.json |

### Shared substrate (not per-runtime)
- `identity/888-APEX.json` — the chair, not an agent; HARAM-8≠9: expression_weights.888/999 must be 0.0 for every phenotype
- `organs/{arifos,aforge,geox,wealth,well}.json`
- `forge/forge-bot.json` — @arifOS_bot executor (MCP: aforge)

## Verified drift findings (F2, live probes)

1. **AGENTS_UNIFIED.yaml points at LEGACY paths**: canonical_card refs = 3× `agent-cards/identity/...`, 0× `a2a-server/agent-cards/`. SOT registry card paths stale.
2. **Missing forge instrument cards**: only fi-001-opencode + fi-008-kimi-code exist under forge/. FI-002 (claude-code), FI-003 (qwen-code), FI-004 (antigravity), FI-005 (codex), FI-006 (copilot), FI-007 (grok-build) are registered in AGENTS_UNIFIED.yaml but have NO forge card artifact.
3. **OpenClaw harness card half-migrated**: `species: {}` empty — v2.2.0 schema requires the W-vector block (compare harnesses/opencode.json which has full species block with expression_weights + proxy_for_harnesses).

## Reusable probe (card landscape dump)

```python
import json, glob
for path in sorted(glob.glob('/root/AAA/a2a-server/agent-cards/**/*.json', recursive=True)):
    c = json.load(open(path))
    print(f"{path.split('/agent-cards/')[1]:<40} id={c.get('id')} class={c.get('class')} bound_to={c.get('bound_to')} skills={len(c.get('skills',[]))}")
```
