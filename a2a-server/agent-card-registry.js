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

// ── Normalise agent card to a canonical internal shape ──────────────────
function normaliseCard(card) {
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

  // Protocol version
  const protocolVersion = card.protocolVersion || card.protocol_version || 'a2a.v1';

  // Peers
  const peers = card.peers || [];

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
    // Keep the raw original for downstream consumers
    _raw: card,
    _normalisedAt: new Date().toISOString(),
  };
}

// ── Register a single agent card ────────────────────────────────────────
function register(card) {
  const normalised = normaliseCard(card);
  if (!normalised) {
    const err = new Error('Agent card missing agentId/identity.organId/id');
    err.code = 'INVALID_CARD';
    throw err;
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
        const result = register(card);
        loaded.push(result.agentId);
      } else {
        errors.push(`${entry.name}: no identifiable agent ID in any schema`);
      }
    } catch (e) {
      errors.push(`${entry.name}: ${e.message}`);
    }
  }

  return { loaded, errors, total: jsonFiles.length };
}

// ── Recursively load all agent cards from a root directory ──────────────
function loadDirectoryRecursive(rootPath) {
  const resolved = path.resolve(rootPath);
  let results = { loaded: [], errors: [], dirs: 0 };
  try {
    const entries = fs.readdirSync(resolved, { withFileTypes: true });
  const jsonFiles = entries.filter((e) => (e.isFile() || e.isSymbolicLink()) && e.name.endsWith('.json'));
    const subdirs = entries.filter((e) => e.isDirectory());

    // Load JSON files at this level
    for (const entry of jsonFiles) {
      const fullPath = path.join(resolved, entry.name);
      try {
        const raw = fs.readFileSync(fullPath, 'utf-8');
        const card = JSON.parse(raw);
        if (card.agentId || card.id || (card.identity && card.identity.organId)) {
          const result = register(card);
          results.loaded.push(`${entry.name} → ${result.agentId}`);
        } else {
          results.errors.push(`${entry.name}: no identifiable agent ID`);
        }
      } catch (e) {
        results.errors.push(`${entry.name}: ${e.message}`);
      }
    }

    // Recurse into subdirectories
    for (const subdir of subdirs) {
      const subPath = path.join(resolved, subdir.name);
      const sub = loadDirectoryRecursive(subPath);
      results.loaded.push(...sub.loaded.map((l) => `${subdir.name}/${l}`));
      results.errors.push(...sub.errors.map((e) => `${subdir.name}/${e}`));
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

function getStats() {
  const all = getAll();
  const skillsCount = all.reduce((acc, c) => acc + (c.skills || []).length, 0);
  const tagsCount = new Set(all.flatMap((c) => c.tags || []));
  return {
    totalAgents: all.length,
    totalSkills: skillsCount,
    uniqueTags: tagsCount.size,
    agents: all.map((c) => ({ agentId: c.agentId, name: c.name, skills: (c.skills || []).length })),
  };
}

// ── Auto-load on creation ───────────────────────────────────────────────
(function autoLoad() {
  const defaultDir = path.join(__dirname, 'agent-cards');
  if (fs.existsSync(defaultDir)) {
    console.log(`[agent-card-registry] Auto-loading from ${defaultDir}...`);
    const result = loadDirectoryRecursive(defaultDir);
    if (result.loaded.length > 0) {
      console.log(`[agent-card-registry] Loaded ${result.loaded.length} agent cards`);
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
    console.log(`[agent-card-registry] Registry ready: ${cards.size} cards`);
  } else {
    console.warn(`[agent-card-registry] Default directory not found: ${defaultDir}`);
  }
})();

// ── Export ──────────────────────────────────────────────────────────────
module.exports = {
  AgentCardRegistry: {
    cards,
    register,
    loadDirectory,
    loadDirectoryRecursive,
    getAll,
    get,
    findByCapability,
    findByTag,
    findBySkill,
    search,
    getStats,
  },
};
