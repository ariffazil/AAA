#!/usr/bin/env node
/**
 * Agent Card Updater — A2A Protocol v1.0.0 Compliance
 * 
 * Updates all agent cards in agents/ subdirectories to include:
 * - protocolVersion: "1.0"
 * - capabilities object (streaming, pushNotifications, stateTransitionHistory, extendedAgentCard)
 * - supportedInterfaces array [{url, protocolBinding, protocolVersion}]
 * - defaultInputModes, defaultOutputModes
 * 
 * PRESERVES all arifOS constitutional extensions:
 * - class, bound_to, power_band, epistemic_floor, f1_boundary, rollback_plan, identity_anchor
 * - All other existing fields
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const fs = require('fs');
const path = require('path');

const AGENTS_DIR = path.resolve(__dirname, '..', '..', 'agents');

const A2A_DEFAULTS = {
  protocolVersion: '1.0',
  supportedInterfaces: [
    {
      url: 'https://aaa.arif-fazil.com/a2a',
      protocolBinding: 'JSONRPC',
      protocolVersion: '1.0',
    },
    {
      url: 'https://aaa.arif-fazil.com/a2a/jsonrpc',
      protocolBinding: 'JSONRPC',
      protocolVersion: '1.0',
    },
  ],
  capabilities: {
    streaming: true,
    pushNotifications: false,
    stateTransitionHistory: true,
    extendedAgentCard: true,
  },
  defaultInputModes: ['text/plain', 'application/json'],
  defaultOutputModes: ['text/plain', 'application/json'],
};

// arifOS constitutional extensions to ALWAYS preserve
const CONSTITUTIONAL_EXTENSIONS = new Set([
  'class',
  'bound_to',
  'power_band',
  'epistemic_floor',
  'f1_boundary',
  'rollback_plan',
  'identity_anchor',
  'principal_agent',
  'charter',
  'apexMasterSeal',
  'constitution',
  'mcp_surface',
  'kernel_skills',
  'rsi_doctrine',
  'boot_sequence',
  'auth_note',
  '_extended',
]);

function updateAgentCard(filePath) {
  const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  const original = JSON.stringify(data, null, 2);
  let changed = false;

  // 1. Set protocolVersion to "1.0"
  if (data.protocolVersion !== '1.0') {
    data.protocolVersion = '1.0';
    changed = true;
  }

  // 2. Ensure capabilities object exists with all required fields
  if (!data.capabilities || typeof data.capabilities !== 'object') {
    data.capabilities = { ...A2A_DEFAULTS.capabilities };
    changed = true;
  } else {
    // Merge spec requirements while preserving existing
    for (const [key, val] of Object.entries(A2A_DEFAULTS.capabilities)) {
      if (data.capabilities[key] === undefined) {
        data.capabilities[key] = val;
        changed = true;
      }
    }
  }

  // 3. Add supportedInterfaces if missing
  if (!data.supportedInterfaces || !Array.isArray(data.supportedInterfaces) || data.supportedInterfaces.length === 0) {
    data.supportedInterfaces = [...A2A_DEFAULTS.supportedInterfaces];
    changed = true;
  }

  // 4. Ensure defaultInputModes exists
  if (!data.defaultInputModes || !Array.isArray(data.defaultInputModes) || data.defaultInputModes.length === 0) {
    data.defaultInputModes = [...A2A_DEFAULTS.defaultInputModes];
    changed = true;
  }

  // 5. Ensure defaultOutputModes exists
  if (!data.defaultOutputModes || !Array.isArray(data.defaultOutputModes) || data.defaultOutputModes.length === 0) {
    data.defaultOutputModes = [...A2A_DEFAULTS.defaultOutputModes];
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf-8');
    console.log(`✅ Updated: ${path.relative(AGENTS_DIR, filePath)}`);
  } else {
    console.log(`✓ Already compliant: ${path.relative(AGENTS_DIR, filePath)}`);
  }

  // Return what was done for reporting
  return {
    file: filePath,
    changed,
    hasProtocolVersion: data.protocolVersion === '1.0',
    hasCapabilities: !!data.capabilities,
    hasSupportedInterfaces: Array.isArray(data.supportedInterfaces) && data.supportedInterfaces.length > 0,
    hasInputModes: Array.isArray(data.defaultInputModes) && data.defaultInputModes.length > 0,
    hasOutputModes: Array.isArray(data.defaultOutputModes) && data.defaultOutputModes.length > 0,
    preservedExtensions: [...CONSTITUTIONAL_EXTENSIONS].filter(k => data[k] !== undefined),
  };
}

function findAgentCards(dir) {
  const results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findAgentCards(fullPath));
    } else if (entry.name === 'agent-card.json') {
      results.push(fullPath);
    }
  }
  return results;
}

function main() {
  console.log('╔══════════════════════════════════════════════════════╗');
  console.log('║  A2A v1.0.0 Agent Card Compliance Updater           ║');
  console.log('╚══════════════════════════════════════════════════════╝\n');

  const cards = findAgentCards(AGENTS_DIR);
  console.log(`Found ${cards.length} agent cards\n`);

  const results = [];
  for (const cardPath of cards) {
    try {
      const result = updateAgentCard(cardPath);
      results.push(result);
    } catch (err) {
      console.error(`❌ Error updating ${cardPath}: ${err.message}`);
    }
  }

  console.log('\n─── Summary ───');
  const updated = results.filter(r => r.changed).length;
  const compliant = results.filter(r => !r.changed).length;
  console.log(`Cards updated: ${updated}`);
  console.log(`Already compliant: ${compliant}`);
  console.log(`Total: ${results.length}`);

  return results;
}

if (require.main === module) {
  main();
}

module.exports = { updateAgentCard, findAgentCards, A2A_DEFAULTS, CONSTITUTIONAL_EXTENSIONS };
