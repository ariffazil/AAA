/**
 * Agent Discovery Routes — A2A v1.0.0 Capability-Based Service Discovery
 * ════════════════════════════════════════════════════════════════════════
 *
 * Express Router for the Pydantic AI A2A discovery pattern.
 * Mounted on /discover after auth middleware.
 *
 * ENDPOINTS:
 *   GET  /discover              — List all registered agent cards
 *   GET  /discover/stats        — Registry statistics
 *   GET  /discover/:agentId     — Get specific agent card
 *   GET  /discover/search?q=    — Full-text search across agents
 *   GET  /discover/capability/:cap  — Find agents with a capability
 *   GET  /discover/tag/:tag     — Find agents by tag
 *   GET  /discover/skill/:skillId  — Find agents with a specific skill
 *   POST /discover/register     — Dynamically register a new agent card
 *
 * WIRING INSTRUCTIONS (add to server.js):
 *   const discoveryRouter = require('./agent-discovery-routes');
 *   app.use('/a2a', authMiddleware);  // must be before this
 *   app.use('/a2a', discoveryRouter);
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const express = require('express');
const { AgentCardRegistry } = require('./agent-card-registry');

/**
 * Create an Express Router with the full discovery surface.
 * @returns {import('express').Router}
 */
function createDiscoveryRouter() {
  const router = express.Router();

  // ── GET /discover — List all registered agents ──────────────────────────
  router.get('/discover', (_req, res) => {
    const all = AgentCardRegistry.getAll();
    res.json({
      ok: true,
      count: all.length,
      agents: all.map((c) => ({
        agentId: c.agentId,
        name: c.name,
        description: c.description,
        version: c.version,
        protocolVersion: c.protocolVersion,
        provider: c.provider,
        tags: c.tags,
        capabilities: c.capabilities,
        skills: (c.skills || []).map((s) => ({
          id: s.id,
          name: s.name,
          description: s.description,
          tags: s.tags,
        })),
        endpoints: {
          baseUrl: c.endpoints.baseUrl || '',
          healthUrl: c.endpoints.healthUrl || '',
          cardUrl: c.endpoints.cardUrl || '',
        },
        // Constitutional physics — arifOS federation
        class: c.class,
        bound_to: c.bound_to,
        power_band: c.power_band,
        skills_prefix: c.skills_prefix,
        runtime_harness: c.runtime_harness,
        identity_anchor: c.identity_anchor,
        mcp_servers: c.mcp_servers,
        epistemic_floor: c.epistemic_floor,
        f1_boundary: c.f1_boundary,
        rollback_plan: c.rollback_plan,
      })),
      timestamp: new Date().toISOString(),
    });
  });

  // ── GET /discover/stats — Registry statistics ───────────────────────────
  router.get('/discover/stats', (_req, res) => {
    const stats = AgentCardRegistry.getStats();
    res.json({
      ok: true,
      ...stats,
      timestamp: new Date().toISOString(),
    });
  });

  // ── GET /discover/search?q= — Full-text search ──────────────────────────
  router.get('/discover/search', (req, res) => {
    const q = (req.query.q || '').trim();
    if (!q) {
      return res.status(400).json({
        ok: false,
        error: 'Query parameter "q" is required',
      });
    }
    const results = AgentCardRegistry.search(q);
    res.json({
      ok: true,
      query: q,
      count: results.length,
      agents: results,
      timestamp: new Date().toISOString(),
    });
  });

  // ── GET /discover/capability/:capability — Find by capability ───────────
  router.get('/discover/capability/:capability', (req, res) => {
    const { capability } = req.params;
    const results = AgentCardRegistry.findByCapability(capability);
    res.json({
      ok: true,
      capability,
      count: results.length,
      agents: results.map((c) => ({
        agentId: c.agentId,
        name: c.name,
        capabilities: c.capabilities,
        endpoints: c.endpoints,
      })),
      timestamp: new Date().toISOString(),
    });
  });

  // ── GET /discover/tag/:tag — Find agents by tag ─────────────────────────
  router.get('/discover/tag/:tag', (req, res) => {
    const { tag } = req.params;
    const results = AgentCardRegistry.findByTag(tag);
    res.json({
      ok: true,
      tag,
      count: results.length,
      agents: results.map((c) => ({
        agentId: c.agentId,
        name: c.name,
        tags: c.tags,
        skills: (c.skills || []).map((s) => ({ id: s.id, name: s.name, tags: s.tags })),
      })),
      timestamp: new Date().toISOString(),
    });
  });

  // ── GET /discover/skill/:skillId — Find agents by skill ID ──────────────
  router.get('/discover/skill/:skillId', (req, res) => {
    const { skillId } = req.params;
    const results = AgentCardRegistry.findBySkill(skillId);
    res.json({
      ok: true,
      skillId,
      count: results.length,
      agents: results.map((c) => ({
        agentId: c.agentId,
        name: c.name,
        skills: (c.skills || []).filter((s) => s.id === skillId),
      })),
      timestamp: new Date().toISOString(),
    });
  });

  // ── GET /discover/:agentId — Get a specific agent card ──────────────────
  router.get('/discover/:agentId', (req, res) => {
    const { agentId } = req.params;
    const card = AgentCardRegistry.get(agentId);
    if (!card) {
      return res.status(404).json({
        ok: false,
        error: `Agent '${agentId}' not found in registry`,
        knownAgents: AgentCardRegistry.getAll().map((c) => c.agentId),
      });
    }
    res.json({
      ok: true,
      card,
      timestamp: new Date().toISOString(),
    });
  });

  // ── POST /discover/register — Dynamically register a new agent card ─────
  router.post('/discover/register', (req, res) => {
    const card = req.body;
    if (!card || typeof card !== 'object') {
      return res.status(400).json({
        ok: false,
        error: 'Request body must be a JSON object containing an agent card',
      });
    }
    try {
      const registered = AgentCardRegistry.register(card);
      res.status(201).json({
        ok: true,
        agentId: registered.agentId,
        name: registered.name,
        skills: (registered.skills || []).length,
        timestamp: new Date().toISOString(),
      });
    } catch (e) {
      const status = e.code === 'INVALID_CARD' ? 400 : 500;
      res.status(status).json({
        ok: false,
        error: e.message,
        code: e.code || 'REGISTRATION_ERROR',
      });
    }
  });

  return router;
}

// ── Convenience: create a router that wraps /discover under a prefix ────
function createPrefixedRouter(prefix) {
  const router = express.Router();
  router.use(prefix || '/a2a', createDiscoveryRouter());
  return router;
}

// ── Legacy mount pattern (mount directly onto app) ──────────────────────
function mountDiscoveryRoutes(app) {
  app.use('/a2a', createDiscoveryRouter());
  console.log('[agent-discovery] Routes mounted: /a2a/discover/*');
}

module.exports = {
  createDiscoveryRouter,
  mountDiscoveryRoutes,
  createPrefixedRouter,
};
