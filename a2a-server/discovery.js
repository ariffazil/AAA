/**
 * discovery.js — Static mesh discovery with VAULT999 receipt.
 *
 * P0 of v42.1: ping every organ's /.well-known/agent-card.json and write
 * a discovery receipt to VAULT999 telemetry.
 *
 * Dynamic registration is disabled until it returns non-empty results.
 */

const fs = require('fs');
const path = require('path');

const ORGANS = [
  { id: 'arifos', baseUrl: 'http://127.0.0.1:8088' },
  { id: 'aforge', baseUrl: 'http://127.0.0.1:7071' },
  { id: 'geox', baseUrl: 'http://127.0.0.1:8081' },
  { id: 'wealth', baseUrl: 'http://127.0.0.1:18082' },
  { id: 'well', baseUrl: 'http://127.0.0.1:18083' },
  { id: 'vault999', baseUrl: 'http://127.0.0.1:5002' },
];

const VAULT_TELEMETRY_DIR = '/root/VAULT999/telemetry';
const MESH_ID = 'AAA-MESH-v42.1';

async function fetchCard(baseUrl) {
  const urls = [
    `${baseUrl}/.well-known/agent-card.json`,
    `${baseUrl}/.well-known/agent.json`,
    `${baseUrl}/agent-card.json`,
  ];

  for (const url of urls) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
      if (res.ok) {
        const card = await res.json();
        return { url, card };
      }
    } catch (err) {
      // try next fallback
    }
  }

  return null;
}

async function runDiscovery() {
  const results = [];

  for (const organ of ORGANS) {
    const found = await fetchCard(organ.baseUrl);
    if (found) {
      results.push({
        organ_id: organ.id,
        status: 'OK',
        card_url: found.url,
        organ_id_from_card: found.card.organ_id || found.card.name || null,
        role: found.card.role || null,
        owned_mcp_count: Array.isArray(found.card.owned_mcp) ? found.card.owned_mcp.length : 0,
      });
    } else {
      results.push({
        organ_id: organ.id,
        status: 'FAIL',
        reason: 'AGENT_CARD_UNREACHABLE',
      });
    }
  }

  const receipt = {
    timestamp: new Date().toISOString(),
    mesh_id: MESH_ID,
    topology: 'governed_mesh',
    results,
    all_ok: results.every(r => r.status === 'OK'),
  };

  writeDiscoveryReceipt(receipt);
  return receipt;
}

function writeDiscoveryReceipt(receipt) {
  try {
    if (!fs.existsSync(VAULT_TELEMETRY_DIR)) {
      fs.mkdirSync(VAULT_TELEMETRY_DIR, { recursive: true });
    }
    const filePath = path.join(VAULT_TELEMETRY_DIR, `discovery-${Date.now()}.json`);
    fs.writeFileSync(filePath, JSON.stringify(receipt, null, 2), 'utf8');
    console.log(`[discovery] receipt written: ${filePath}`);
  } catch (err) {
    console.error('[discovery] failed to write receipt:', err);
  }
}

module.exports = { runDiscovery, ORGANS };

// If run directly from CLI
if (require.main === module) {
  runDiscovery().then(receipt => {
    console.log(JSON.stringify(receipt, null, 2));
    process.exit(receipt.all_ok ? 0 : 1);
  });
}
