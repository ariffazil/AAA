/**
 * Auto-register federation organs on AAA startup.
 * Called after server.listen() — probes each organ's health, then registers.
 */

const ORGANS = [
  {
    identity: { organId: 'arifos', name: 'arifOS Constitutional Kernel', role: 'governance' },
    endpoints: { healthUrl: 'http://127.0.0.1:8088/health', mcpUrl: 'http://127.0.0.1:8088/mcp' },
    skills: [
      { id: 'session_init', name: 'Session Init', description: 'Constitutional session binding' },
      { id: 'judge', name: 'Judge', description: 'Constitutional verdict' },
      { id: 'vault_seal', name: 'Vault Seal', description: 'Immutable ledger append' },
      { id: 'route', name: 'Route', description: 'Intent routing to organs' },
    ],
  },
  {
    identity: { organId: 'aforge', name: 'A-FORGE Execution Shell', role: 'execution' },
    endpoints: { healthUrl: 'http://127.0.0.1:7071/health', mcpUrl: 'http://127.0.0.1:7072/mcp' },
    skills: [
      { id: 'forge_execute', name: 'Forge Execute', description: 'Code execution' },
      { id: 'forge_shell', name: 'Forge Shell', description: 'Governed shell' },
      { id: 'forge_git', name: 'Forge Git', description: 'Git operations' },
    ],
  },
  {
    identity: { organId: 'geox', name: 'GEOX Earth Intelligence', role: 'evidence' },
    endpoints: { healthUrl: 'http://127.0.0.1:8081/health', mcpUrl: 'http://127.0.0.1:8081/mcp/' },
    skills: [
      { id: 'basin_resolve', name: 'Basin Resolve', description: 'Basin analysis' },
      { id: 'seismic_compute', name: 'Seismic Compute', description: 'Seismic physics' },
      { id: 'petrophysics', name: 'Petrophysics', description: 'Well log analysis' },
    ],
  },
  {
    identity: { organId: 'wealth', name: 'WEALTH Capital Intelligence', role: 'capital' },
    endpoints: { healthUrl: 'http://127.0.0.1:18082/health', mcpUrl: 'http://127.0.0.1:18082/mcp' },
    skills: [
      { id: 'emv', name: 'EMV', description: 'Expected monetary value' },
      { id: 'monte_carlo', name: 'Monte Carlo', description: 'Simulation' },
      { id: 'conservation', name: 'Conservation', description: 'Capital conservation' },
    ],
  },
  {
    identity: { organId: 'well', name: 'WELL Human Readiness', role: 'vitality' },
    endpoints: { healthUrl: 'http://127.0.0.1:18083/health', mcpUrl: 'http://127.0.0.1:18083/mcp' },
    skills: [
      { id: 'readiness', name: 'Readiness', description: 'Human readiness check' },
      { id: 'vitality', name: 'Vitality', description: 'Vitality validation' },
      { id: 'dignity', name: 'Dignity', description: 'Dignity guard' },
    ],
  },
  {
    identity: { organId: 'openclaw', name: 'OpenClaw Agentic Coder', role: 'orchestration' },
    endpoints: { healthUrl: 'http://127.0.0.1:18789/health', mcpUrl: 'ws://127.0.0.1:18789' },
    skills: [
      { id: 'agent_spawn', name: 'Agent Spawn', description: 'Spawn coding agents' },
      { id: 'cron', name: 'Cron', description: 'Scheduled tasks' },
      { id: 'telegram', name: 'Telegram', description: 'Messaging channel' },
    ],
  },
];

async function autoRegisterOrgans(port = 3001) {
  const baseUrl = `http://127.0.0.1:${port}`;
  let registered = 0;
  let failed = 0;

  for (const organ of ORGANS) {
    try {
      const resp = await fetch(`${baseUrl}/federation/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(organ),
      });
      const result = await resp.json();
      if (result.ok) {
        registered++;
      } else {
        failed++;
        console.warn(`[auto-register] ${organ.identity.organId}: ${result.error} — ${result.detail}`);
      }
    } catch (e) {
      failed++;
      console.warn(`[auto-register] ${organ.identity.organId}: ${e.message}`);
    }
  }

  console.log(`[auto-register] ${registered}/${ORGANS.length} organs registered (${failed} failed)`);
  return { registered, failed, total: ORGANS.length };
}

module.exports = { autoRegisterOrgans, ORGANS };
