#!/usr/bin/env node
/**
 * Agent Card Registry — Pydantic AI A2A Discovery
 * ════════════════════════════════════════════════
 *
 * Dynamic in-memory (+ optional Postgres-backed) registry of agent cards.
 * Provides capability-based routing, search, and dynamic registration
 * following the A2A v1.0.0 pattern.
 *
 * AUTO-LOADS from ./agent-cards/ directory on creation.
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const fs = require('fs');
const path = require('path');

// ── In-memory store ─────────────────────────────────────────────────────
const cards = new Map();

// ── CIV-33 layer classification ──────────────────────────────────────────
// Maps top-level directory → CIV-33 layer label. Used to enrich normalised
// cards with `civ_layer` so /a2a/discover and dashboards can group by layer.
const CIV33_LAYERS = {
  // 3-layer geometry (2026-08-10 F13 — adat agentic update):
  //   L1 IDENTITY  — who (333/555/888) sealed rare · carries adat_agentic.forge
  //   L2 HARNESS   — where / FI runtime engines
  //   L3 BINDING   — attachment: functions + roles + organs + pillars + extensions
  // FORGE is no longer a binding layer. FORGE is adat agentic — inherited by all warga.
  // Physical folders stay. AAA = catalog. WHICH engine = FED/runtime only.
  identity: 'identity',
  harnesses: 'harness',
  functions: 'binding',
  roles: 'binding',
  organs: 'binding',
  pillars: 'binding',
  extensions: 'binding',
  federation: 'binding',  // federation.yaml generated cards (2026-08-19 registry zen)
  _retired: 'retired',
};

// ── Normalise agent card to a canonical internal shape ──────────────────
function normaliseCard(card, sourcePath) {
  if (!card || typeof card !== 'object') return null;

  // Derive agentId from various possible keys
  const agentId =
    card.agentId ||
    card.agent_id ||
    card.id ||
    (card.identity && card.identity.organId) ||
    null;

  if (!agentId) return null;

  // Derive a display name
  const name =
    card.name ||
    (card.identity && card.identity.name) ||
    agentId;

  // Derive description
  const description =
    card.description ||
    (card.identity && card.identity.description) ||
    '';

  // Normalise skills array (try multiple schemas)
  let skills = [];
  if (Array.isArray(card.skills)) {
    skills = card.skills.map((s) => {
      if (typeof s === 'string') return { id: s, name: s, description: '', tags: [] };
      return {
        id: s.id || s.name || 'unknown',
        name: s.name || s.id || 'unknown',
        description: s.description || '',
        tags: s.tags || [],
        riskClass: s.riskClass || 'low',
        executionAllowed: s.executionAllowed !== false,
      };
    });
  }

  // Collect tags from identity + skills
  const tags = new Set([
    ...((card.identity && card.identity.tags) || []),
    ...(card.tags || []),
    ...skills.flatMap((s) => s.tags || []),
  ]);

  // Collect capabilities
  const capabilities = {
    streaming: false,
    asyncTasks: false,
    pushNotifications: false,
    supportsDelegation: false,
    supportsToolDiscovery: false,
    ...(card.capabilities || {}),
  };

  // Collect endpoints
  const endpoints = {
    baseUrl: '',
    healthUrl: '',
    cardUrl: '',
    mcpUrl: '',
    a2aUrl: '',
    ...(card.endpoints || {}),
    ...(card.a2a_endpoints || {}),
  };

  // If card has a top-level url, use it
  if (card.url && !endpoints.baseUrl) {
    endpoints.baseUrl = card.url;
  }

  // Provider info
  const provider = {
    organization: 'arifOS',
    system: 'AAA',
    ...(card.provider || {}),
    ...((card.identity && card.identity.provider) || {}),
  };

  // Security
  const security = {
    authRequired: false,
    securityNote: 'Localhost IS the password (ADR-001)',
    allowedCallers: [],
    ...(card.security || {}),
  };

  // Governance
  const governance = {
    trustGrade: 'B',
    sourceClass: 'derived',
    holdCapable: false,
    floorProfile: [],
    ...(card.governance || {}),
  };

  // Version
  const version = card.version || (card.identity && card.identity.version) || 'unknown';

  // Protocol version (Tier-1.2: A2A v1.2 aligned — flat shape, Ed25519-signed)
  // Accepts: '1.2', '1.0.0', '0.2.5', 'a2a.v1' — anything not '1.2' is normalised to '1.2'
  const rawProtocol =
    card.protocolVersion ||
    card.protocol_version ||
    (card.identity && card.identity.protocolVersion) ||
    '1.2';
  const protocolVersion = rawProtocol === '1.2' ? '1.2' : '1.2';

  // Peers
  const peers = card.peers || [];

  // CIV-33 layer detection from sourcePath (e.g. .../agent-cards/identity/333-AGI/agent-card.json)
  let civLayer = null;
  if (typeof sourcePath === 'string') {
    // Physical a2a-server/agent-cards/<dir>/ → L1–L3 via CIV33_LAYERS
    const m = sourcePath.match(/\/agent-cards\/([^/]+)\//);
    if (m && Object.prototype.hasOwnProperty.call(CIV33_LAYERS, m[1])) {
      civLayer = CIV33_LAYERS[m[1]];
    }
    // Warga home cards under AAA/agents/ — classify without moving folders
    if (!civLayer) {
      const base = sourcePath.replace(/\\/g, '/');
      if (
        /\/agents\/_lanes\//.test(base) ||
        /\/agents\/333-AGI\//.test(base) ||
        /\/agents\/555-ASI\//.test(base) ||
        /\/agents\/888-APEX\//.test(base) ||
        /\/identity\/333-AGI\//.test(base) ||
        /\/identity\/555-ASI\//.test(base) ||
        /\/identity\/888-APEX\//.test(base)
      ) {
        civLayer = 'identity';
      } else if (
        /\/agents\/_external\//.test(base) ||
        /\/agents\/opencode\//.test(base) ||
        /\/agents\/kimi-code\//.test(base)
      ) {
        civLayer = 'harness';
      } else if (
        /\/agents\/hermes/.test(base) ||
        /\/agents\/makcikgpt\//.test(base) ||
        /\/agents\/main\//.test(base) ||
        /hermesarifos/.test(base)
      ) {
        civLayer = 'binding'; // edge home cards fold into L3 BINDING (3-layer final)
      } else if (
        /\/agents\/openclaw\//.test(base) ||
        /\/agents\/prospect/.test(base) ||
        /\/agents\/agentic-trading/.test(base) ||
        /\/agents\/skill-auditor\//.test(base)
      ) {
        // openclaw home + domain specialists = attachment surface
        civLayer = 'binding';
      } else if (
        /\/agents\/777/.test(base) ||
        /\/agents\/forge-bot\//.test(base)
      ) {
        // 777-FORGE retired (F13 directive 2026-08-10 — FORGE is adat agentic, not a lane)
        // forge-bot = execution bot, not an identity
        civLayer = 'retired';
      }
    }
  }

  return {
    agentId,
    name,
    description,
    version,
    protocolVersion,
    provider,
    tags: [...tags],
    capabilities,
    endpoints,
    skills,
    security,
    governance,
    peers,
    // Custom constitutional fields (hermes-asi, arifOS specific)
    class: card.class || null,
    bound_to: card.bound_to || null,
    power_band: card.power_band || null,
    skills_prefix: card.skills_prefix || [],
    runtime_harness: card.runtime_harness || null,
    identity_anchor: card.identity_anchor || null,
    // adat agentic — FORGE as inherited capability substrate (F13 directive 2026-08-10)
    adat_agentic: card.adat_agentic || null,
    forge_inherited: card.adat_agentic?.forge?.inherited === true,
    forge_access: card.adat_agentic?.forge?.access || null,
    forge_zen: card.adat_agentic?.forge?.zen || null,
    mcp_servers: card.mcp_servers || [],
    epistemic_floor: card.epistemic_floor || null,
    f1_boundary: card.f1_boundary || null,
    rollback_plan: card.rollback_plan || null,
    // CIV-33 layer classification (identity / function / extension / harness / pillar / organ / retired)
    civ_layer: civLayer,
    civ_source: sourcePath || null,
    // Keep the raw original for downstream consumers
    _raw: card,
    _normalisedAt: new Date().toISOString(),
  };
}

// ── Register a single agent card ────────────────────────────────────────
function register(card, sourcePath) {
  const normalised = normaliseCard(card, sourcePath);
  if (!normalised) {
    const err = new Error('Agent card missing agentId/identity.organId/id');
    err.code = 'INVALID_CARD';
    throw err;
  }
  // 3-layer geometry: never downgrade a classified card to unclassified.
  // The canonical agent-cards/ tree (scanned first) sets the layer; later
  // warga scans (agents/) may refresh fields but must not wipe civ_layer.
  const existing = cards.get(normalised.agentId);
  if (existing && existing.civ_layer && !normalised.civ_layer) {
    normalised.civ_layer = existing.civ_layer;
  }
  cards.set(normalised.agentId, normalised);
  return normalised;
}

// ── Register from a directory of JSON files ─────────────────────────────
function loadDirectory(dirPath) {
  const resolved = path.resolve(dirPath);
  let entries;
  try {
    entries = fs.readdirSync(resolved, { withFileTypes: true });
  } catch (e) {
    console.warn(`[agent-card-registry] Directory not found: ${resolved}`);
    return { loaded: 0, errors: [e.message] };
  }
  const jsonFiles = entries.filter((e) => (e.isFile() || e.isSymbolicLink()) && e.name.endsWith('.json'));

  const loaded = [];
  const errors = [];

  for (const entry of jsonFiles) {
    const fullPath = path.join(resolved, entry.name);
    try {
      const raw = fs.readFileSync(fullPath, 'utf-8');
      const card = JSON.parse(raw);
      // Single card
      if (card.agentId || card.id || (card.identity && card.identity.organId)) {
        const result = register(card, fullPath);
        loaded.push(result.agentId);
      } else if (entry.name !== 'aaa-cockpit.json') {
        errors.push(`${entry.name}: no identifiable agent ID in any schema`);
      }
    } catch (e) {
      errors.push(`${entry.name}: ${e.message}`);
    }
  }

  return { loaded, errors, total: jsonFiles.length };
}

// ── Recursively load all agent cards from a root directory ──────────────
// Skip noise dirs; prefer agent-card.json under agents/ trees; never treat
// identity.json / SESSION specs as cards (entropy reduction 2026-08-09).
const SKIP_DIRS = new Set([
  '_brief', '_docs', '_archive', '_retired', '_audit', '__pycache__',
  'node_modules', '.git', 'memories', 'profiles', 'dist', 'build',
]);

function isLikelyAgentCardFile(name, rootPath) {
  if (!name.endsWith('.json')) return false;
  // Explicit non-cards
  if (/^(identity|liveness|package|tsconfig|sessionspec)/i.test(name)) return false;
  if (name === 'aaa-cockpit.json') return false; // control plane meta, not agent
  // Under /agents/ only accept agent-card.json (and *agent-card*.json)
  if (rootPath.includes('/agents') && !rootPath.includes('/agent-cards')) {
    return name === 'agent-card.json' || name.endsWith('.agent-card.json');
  }
  // Under agent-cards/ tree: allow flat id.json (333-AGI.json, opencode.json, …)
  return true;
}

function loadDirectoryRecursive(rootPath) {
  const resolved = path.resolve(rootPath);
  let results = { loaded: [], errors: [], dirs: 0, skipped: 0 };
  try {
    const entries = fs.readdirSync(resolved, { withFileTypes: true });
    const jsonFiles = entries.filter(
      (e) => (e.isFile() || e.isSymbolicLink()) && isLikelyAgentCardFile(e.name, resolved)
    );
    const subdirs = entries.filter((e) => e.isDirectory() && !SKIP_DIRS.has(e.name) && !e.name.startsWith('.'));

    for (const entry of jsonFiles) {
      const fullPath = path.join(resolved, entry.name);
      try {
        const raw = fs.readFileSync(fullPath, 'utf-8');
        const card = JSON.parse(raw);
        if (card.agentId || card.id || (card.identity && card.identity.organId)) {
          const result = register(card, fullPath);
          results.loaded.push(`${entry.name} → ${result.agentId}`);
        } else {
          results.skipped += 1; // silent skip — not an error
        }
      } catch (e) {
        // Parse errors only for files we intended as cards
        results.errors.push(`${entry.name}: ${e.message}`);
      }
    }

    for (const subdir of subdirs) {
      const subPath = path.join(resolved, subdir.name);
      const sub = loadDirectoryRecursive(subPath);
      results.loaded.push(...sub.loaded.map((l) => `${subdir.name}/${l}`));
      results.errors.push(...sub.errors.map((e) => `${subdir.name}/${e}`));
      results.skipped += sub.skipped || 0;
      results.dirs += 1 + sub.dirs;
    }
  } catch (e) {
    results.errors.push(`Cannot read ${resolved}: ${e.message}`);
  }

  return results;
}


// ── Query methods ───────────────────────────────────────────────────────

function getAll() {
  return [...cards.values()];
}

function get(agentId) {
  return cards.get(agentId) || null;
}

function findByCapability(capability) {
  if (!capability || typeof capability !== 'string') return [];
  const capLower = capability.toLowerCase();
  const results = [];
  for (const card of cards.values()) {
    const caps = card.capabilities || {};
    const matches = Object.keys(caps).some(
      (k) => k.toLowerCase() === capLower && caps[k] === true
    );
    if (matches) results.push(card);
  }
  return results;
}

function findByTag(tag) {
  if (!tag || typeof tag !== 'string') return [];
  const tagLower = tag.toLowerCase();
  const results = [];
  for (const card of cards.values()) {
    if ((card.tags || []).some((t) => t.toLowerCase() === tagLower)) {
      results.push(card);
    }
    // Also check skills tags
    if (!results.includes(card)) {
      for (const skill of card.skills || []) {
        if ((skill.tags || []).some((t) => t.toLowerCase() === tagLower)) {
          results.push(card);
          break;
        }
      }
    }
  }
  return results;
}

function search(query) {
  if (!query || typeof query !== 'string') return [];
  const q = query.toLowerCase();
  const results = [];
  for (const card of cards.values()) {
    const nameMatch = card.name && card.name.toLowerCase().includes(q);
    const descMatch = card.description && card.description.toLowerCase().includes(q);
    const tagMatch = (card.tags || []).some((t) => t.toLowerCase().includes(q));
    const skillMatch = (card.skills || []).some(
      (s) =>
        (s.name && s.name.toLowerCase().includes(q)) ||
        (s.description && s.description.toLowerCase().includes(q))
    );
    const idMatch = card.agentId && card.agentId.toLowerCase().includes(q);
    if (nameMatch || descMatch || tagMatch || skillMatch || idMatch) {
      results.push(card);
    }
  }
  return results;
}

function findBySkill(skillId) {
  if (!skillId) return [];
  const sLower = skillId.toLowerCase();
  return [...cards.values()].filter((card) =>
    (card.skills || []).some((s) => s.id && s.id.toLowerCase() === sLower)
  );
}

// ── Auto-load on creation ───────────────────────────────────────────────
(function autoLoad() {
  // Primary scan: legacy a2a-server/agent-cards/ (contains symlinks → CIV-33)
  const defaultDir = path.join(__dirname, 'agent-cards');
  if (fs.existsSync(defaultDir)) {
    console.log(`[agent-card-registry] Auto-loading from ${defaultDir}...`);
    const result = loadDirectoryRecursive(defaultDir);
    if (result.loaded.length > 0) {
      console.log(`[agent-card-registry] Loaded ${result.loaded.length} agent cards (legacy path)`);
    }
    if (result.errors.length > 0) {
      console.warn(`[agent-card-registry] ${result.errors.length} load errors:`);
      for (const err of result.errors.slice(0, 5)) {
        console.warn(`  ${err}`);
      }
      if (result.errors.length > 5) {
        console.warn(`  ... and ${result.errors.length - 5} more`);
      }
    }
  } else {
    console.warn(`[agent-card-registry] Default directory not found: ${defaultDir}`);
  }

  // Secondary scan: canonical CIV-33 location /root/AAA/agent-cards/
  // (mostly redundant with symlinks above, but ensures direct access works
  //  and surfaces cards that legacy symlinks may not cover)
  const civ33Root = path.resolve(__dirname, '..', 'agent-cards');
  if (fs.existsSync(civ33Root) && path.resolve(civ33Root) !== path.resolve(defaultDir)) {
    console.log(`[agent-card-registry] Scanning canonical CIV-33 tree: ${civ33Root}...`);
    const civ33Result = loadDirectoryRecursive(civ33Root);
    console.log(`[agent-card-registry] CIV-33 scan added/refreshed ${civ33Result.loaded.length} cards`);
  }

  // Tertiary scan: warga agent cards at /root/AAA/agents/*/agent-card.json
  // (hermes, openclaw, forge-bot, 777-forge, etc. — live identity cards)
  const wargaRoot = path.resolve(__dirname, '..', 'agents');
  if (fs.existsSync(wargaRoot) && path.resolve(wargaRoot) !== path.resolve(defaultDir) && path.resolve(wargaRoot) !== path.resolve(civ33Root)) {
    console.log(`[agent-card-registry] Scanning warga agent cards: ${wargaRoot}...`);
    const wargaResult = loadDirectoryRecursive(wargaRoot);
    console.log(`[agent-card-registry] Warga scan added/refreshed ${wargaResult.loaded.length} cards`);
    if (wargaResult.errors.length > 0) {
      console.warn(`[agent-card-registry] ${wargaResult.errors.length} warga load errors (first 3):`);
      for (const err of wargaResult.errors.slice(0, 3)) {
        console.warn(`  ${err}`);
      }
    }
    if (wargaResult.skipped) {
      console.log(`[agent-card-registry] Warga non-card JSON skipped: ${wargaResult.skipped}`);
    }
  } else {
    console.warn(`[agent-card-registry] Warga agents dir not found: ${wargaRoot}`);
  }

  // Summary by CIV-33 layer
  const byLayer = {};
  for (const c of cards.values()) {
    const layer = c.civ_layer || 'unclassified';
    byLayer[layer] = (byLayer[layer] || 0) + 1;
  }
  console.log(`[agent-card-registry] Registry ready: ${cards.size} cards · ${JSON.stringify(byLayer)}`);
})();

// ── CIV-33 helpers ──────────────────────────────────────────────────────
function getByLayer(layer) {
  if (!layer || typeof layer !== 'string') return [];
  return [...cards.values()].filter((c) => c.civ_layer === layer);
}

function getStats() {
  const all = getAll();
  const skillsCount = all.reduce((acc, c) => acc + (c.skills || []).length, 0);
  const tagsCount = new Set(all.flatMap((c) => c.tags || []));
  const byLayer = {};
  for (const c of all) {
    const layer = c.civ_layer || 'unclassified';
    byLayer[layer] = (byLayer[layer] || 0) + 1;
  }
  return {
    totalAgents: all.length,
    totalSkills: skillsCount,
    uniqueTags: tagsCount.size,
    byLayer,
    agents: all.map((c) => ({ agentId: c.agentId, name: c.name, civ_layer: c.civ_layer, skills: (c.skills || []).length })),
  };
}

// ── Export ──────────────────────────────────────────────────────────────
module.exports = {
  AgentCardRegistry: {
    cards,
    register,
    loadDirectory,
    loadDirectoryRecursive,
    getAll,
    get,
    getByLayer,
    findByCapability,
    findByTag,
    findBySkill,
    search,
    getStats,
    CIV33_LAYERS,
  },
};
