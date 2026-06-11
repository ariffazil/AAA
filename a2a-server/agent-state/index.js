/**
 * AGENT STATE — AAA Agent State Layer
 * 
 * "AAA is not a swarm. AAA is the state that makes swarms lawful."
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

const registry = require('./registry');
const schemas = require('./schemas');

/**
 * Bootstrap all known forge instruments into the Agent Registry.
 * Called once at AAA server startup.
 */
async function bootstrapForgeInstruments() {
  const instruments = [
    {
      agent_name: 'OpenCode',
      agent_class: 'agent',
      identity: { claimed_by: 'opencode CLI', body: { runtime: 'local', model: 'deepseek-v4-pro', host: 'af-forge' } },
      manifest: { purpose: 'Code generation, deployment, multi-step orchestration', tools: ['arifOS:13', 'mcp:22'], version: '1.15.0' },
    },
    {
      agent_name: 'Claude Code',
      agent_class: 'agent',
      identity: { claimed_by: 'claude CLI', body: { runtime: 'local', model: 'deepseek-v4-pro', host: 'af-forge' } },
      manifest: { purpose: 'Complex refactors, seatbelt sandbox, audit trails', tools: ['arifOS:13', 'mcp:10'], version: '2.1.160' },
    },
    {
      agent_name: 'QWA (Qwen AAA)',
      agent_class: 'observer',
      identity: { claimed_by: 'qwen CLI', body: { runtime: 'local', model: 'MiniMax-M3', host: 'af-forge' } },
      manifest: { purpose: 'Deep analysis, federation state ingestion, contradiction audit', tools: ['arifOS:7', 'mcp:5'], version: '0.17.1' },
    },
    {
      agent_name: 'Gemini CLI',
      agent_class: 'observer',
      identity: { claimed_by: 'gemini CLI', body: { runtime: 'local', model: 'gemini-2.5-flash', host: 'af-forge' } },
      manifest: { purpose: 'Quick scans, web research, lightweight reasoning', tools: ['arifOS:7', 'mcp:13'], version: '0.43.0' },
    },
    {
      agent_name: 'Codex CLI',
      agent_class: 'observer',
      identity: { claimed_by: 'codex CLI', body: { runtime: 'local', model: 'GPT-5.5', host: 'af-forge' } },
      manifest: { purpose: 'Coding (observer until MCP verified)', tools: ['arifOS:3'], version: '0.136.0' },
    },
    {
      agent_name: 'Copilot CLI',
      agent_class: 'agent',
      identity: { claimed_by: 'copilot CLI', body: { runtime: 'local', model: 'github-copilot', host: 'af-forge' } },
      manifest: { purpose: 'Parallel exploration, GitHub integration', tools: ['arifOS:7', 'mcp:11'], version: '1.0.61' },
    },
    {
      agent_name: 'AAA Gateway',
      agent_class: 'gateway',
      identity: { claimed_by: 'AAA runtime', body: { runtime: 'local', model: 'deterministic_service', host: 'af-forge' } },
      manifest: { purpose: 'Cockpit, A2A mesh, human veto surface', tools: ['A2A'], version: '1.0.0' },
    },
    {
      agent_name: 'A-FORGE',
      agent_class: 'forge',
      identity: { claimed_by: 'A-FORGE runtime', body: { runtime: 'local', model: 'deterministic_service', host: 'af-forge' } },
      manifest: { purpose: 'Execution broker — dry-run first, never sovereign', tools: [], version: 'W2/W3' },
    },
    {
      agent_name: 'Hermes ASI',
      agent_class: 'gateway',
      identity: { claimed_by: 'Hermes runtime', body: { runtime: 'local', model: 'MiniMax-M3', host: 'af-forge' } },
      manifest: { purpose: 'ASI relay — Telegram ↔ federation bridge', tools: ['arifOS:13'], version: '1.0.0' },
    },
    {
      agent_name: 'OpenClaw',
      agent_class: 'gateway',
      identity: { claimed_by: 'OpenClaw runtime', body: { runtime: 'local', model: 'MiniMax-M3', host: 'af-forge' } },
      manifest: { purpose: 'A2A mesh gateway', tools: ['A2A'], version: '1.0.0' },
    },
  ];

  const results = [];
  for (const inst of instruments) {
    try {
      const existing = await registry.listAgents();
      const already = existing.find(a => a.agent_name === inst.agent_name);
      if (already) {
        // Update manifest
        await registry.manifestAgent(already.agent_id, inst.manifest);
        results.push({ agent_name: inst.agent_name, status: 'updated', agent_id: already.agent_id });
      } else {
        const agent = await registry.registerAgent({
          agent_name: inst.agent_name,
          agent_class: inst.agent_class,
          identity: inst.identity,
          manifest: inst.manifest,
        });
        results.push({ agent_name: inst.agent_name, status: 'registered', agent_id: agent.agent_id });
      }
    } catch (e) {
      results.push({ agent_name: inst.agent_name, status: 'error', error: e.message });
    }
  }

  return results;
}

// ── Exports ─────────────────────────────────────────────────────────

module.exports = {
  ...registry,
  schemas,
  bootstrapForgeInstruments,
};
