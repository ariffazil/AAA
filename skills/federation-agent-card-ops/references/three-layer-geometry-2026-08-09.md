# Three-Layer Geometry — 2026-08-09 compression transcript

## The compression (Arif's words)

1. Presented 7-layer tree (identity/harnesses/forge/extensions/functions/roles/organs).
2. Arif: "No 3. No 5 no 6, 7 i think can compress into one" → forge+functions+roles+organs → BINDING (4 layers).
3. Executed 4-layer patch → Arif: "Nope. I want three only" → extensions also folded into BINDING.

Final: **IDENTITY (3) · HARNESS (12) · BINDING (16)** + 7 legitimately unclassified (test/retired/persona cards).

## CIV33_LAYERS before/after

```js
// BEFORE (7 layers)
const CIV33_LAYERS = {
  identity: 'identity',
  functions: 'function',
  extensions: 'extension',
  harnesses: 'harness',
  pillars: 'pillar',
  organs: 'organ',
  _retired: 'retired',
};

// AFTER (3 layers)
const CIV33_LAYERS = {
  identity: 'identity',
  harnesses: 'harness',
  forge: 'binding',
  functions: 'binding',
  roles: 'binding',
  organs: 'binding',
  extensions: 'binding',
  pillars: 'binding',
  _retired: 'retired',
};
```

## The register() guard (fixes warga-scan overwrite)

```js
function register(card, sourcePath) {
  const normalised = normaliseCard(card, sourcePath);
  if (!normalised) { /* ...throw INVALID_CARD... */ }
  // 3-layer geometry: never downgrade a classified card to unclassified.
  const existing = cards.get(normalised.agentId);
  if (existing && existing.civ_layer && !normalised.civ_layer) {
    normalised.civ_layer = existing.civ_layer;
  }
  cards.set(normalised.agentId, normalised);
  return normalised;
}
```

Root cause: registry is a Map keyed by agentId; scan order is legacy a2a-server/agent-cards/ → AAA/agent-cards/ → AAA/agents/ (warga, LAST). Warga paths don't match the `/agent-cards/([^/]+)/` civ-layer regex, so the last write wiped civ_layer to null → 26 unclassified before guard, 7 after.

## Live verification command

```bash
cd /root/AAA && node -e "
const { AgentCardRegistry } = require('./a2a-server/agent-card-registry');
const s = AgentCardRegistry.getStats();
console.log('byLayer:', JSON.stringify(s.byLayer));
const b = AgentCardRegistry.getByLayer('binding') || [];
const h = AgentCardRegistry.getByLayer('harness') || [];
const i = AgentCardRegistry.getByLayer('identity') || [];
console.log('identity (' + i.length + '):', i.map(c=>c.agentId||c.id||c.name).join(', '));
console.log('harness (' + h.length + '):', h.map(c=>c.agentId||c.id||c.name).join(', '));
console.log('binding (' + b.length + '):', b.map(c=>c.agentId||c.id||c.name).join(', '));
" 2>&1 | grep -vE '^\[|no identifiable' | tail -6
```

Result 2026-08-09: `{"binding":16,"harness":12,"identity":3,"unclassified":7}`.

## A2A HTTP surface ≠ registry (gotcha)

- `POST /a2a` method `agent/getCard` returns the **gateway's own card** regardless of params.
- `agents/discover` returned 0 agents via HTTP — the internal registry is not exposed the way the discover route implies.
- Authoritative check = require the registry module directly (above), not the HTTP surface.

## Identity-split evidence (for the WHO/WHICH doctrine)

- Agent card fields: `model` and `bound_to` coexist independently (opencode: model=deepseek-v4-pro, bound_to=333-AGI).
- `principal_agent.principle_origin`: "Underlying LLM provider (Anthropic/OpenAI/Google/Moonshot/xAI)".
- opencode harness card: `replaces: [codex, claude-code]` — harness swap without identity change.
- 9-ATLAS tensor: cognitive function = WHAT (constitutional), harness = WHERE (replaceable).
- federation-models.json (agents[].primary_model) is the operational provider contract, separate from cards.

## Unclassified 7 (not bugs)

agy · mesa-test-agent · 777-forge (RETIRED) · agentic-trading-companion · hermes (bare card; real identity is extensions/hermes-asi.json) · arifOS_bot · PROSPECT-MATURATION
