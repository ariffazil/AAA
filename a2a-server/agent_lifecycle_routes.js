/**
 * AAA Agent Lifecycle API Routes
 * ═════════════════════════════════
 *
 * FORGED 2026-06-09 by Ω — MXC-arifOS connectivity pipeline.
 *
 * WIRING INSTRUCTIONS:
 *   Add this to AAA a2a-server/server.js:
 *
 *   const { lifecycleManager, AgentState } = require('./agent_lifecycle');
 *   require('./agent_lifecycle_routes')(app, lifecycleManager);
 *
 * ENDPOINTS (all POST /api/agents/*):
 *   /register          — Register new agent
 *   /bind-session      — Bind session to agent
 *   /authorize          — Authorize agent after floor evaluation
 *   /start-execution    — Mark agent as executing
 *   /complete-execution — Mark execution complete
 *   /stop               — Stop agent
 *   /deprovision        — Deprovision agent
 *   /hold               — Emergency hold
 *   /degrade            — Mark degraded
 *   /release            — Release held agent (F13)
 *   /terminate          — Terminate agent
 *   /federation-status  — Get all agent statuses
 *   /agent/:id          — Get single agent status
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

/**
 * Mount lifecycle routes on Express app.
 * @param {import('express').Express} app
 * @param {import('./agent_lifecycle').AgentLifecycleManager} manager
 */
function mountLifecycleRoutes(app, manager) {

  // ── REGISTER ──────────────────────────────────────────────────────────
  app.post('/api/agents/register', (req, res) => {
    const { agent_id, agent_role, actor_id, policy } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.register({
      agentId: agent_id,
      agentRole: agent_role || 'analyst',
      actorId: actor_id || null,
      policy: policy || null,
    });
    if (result.ok) {
      res.json({
        ok: true,
        instance_id: result.instance.instanceId,
        state: result.instance.state,
        summary: result.instance.summary(),
      });
    } else {
      res.status(409).json(result);
    }
  });

  // ── BIND SESSION ──────────────────────────────────────────────────────
  app.post('/api/agents/bind-session', (req, res) => {
    const { agent_id, session_id } = req.body;
    if (!agent_id || !session_id) {
      return res.status(400).json({ ok: false, error: 'agent_id + session_id required' });
    }
    const result = manager.bindSession(agent_id, session_id);
    if (result.ok) {
      res.json({
        ok: true,
        state: manager.get(agent_id)?.state,
        receipt: result.receipt,
      });
    } else {
      res.status(409).json(result);
    }
  });

  // ── AUTHORIZE ─────────────────────────────────────────────────────────
  app.post('/api/agents/authorize', (req, res) => {
    const { agent_id, floor_results } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.authorize(agent_id, floor_results);
    if (result.ok) {
      res.json({
        ok: true,
        state: manager.get(agent_id)?.state,
        receipt: result.receipt,
      });
    } else if (result.held) {
      res.json({
        ok: false,
        held: true,
        state: 'held',
        violations: result.violations,
      });
    } else {
      res.status(409).json(result);
    }
  });

  // ── START EXECUTION ───────────────────────────────────────────────────
  app.post('/api/agents/start-execution', (req, res) => {
    const { agent_id, tool_name } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.startExecution(agent_id, tool_name || 'unknown');
    if (result.ok) {
      res.json({
        ok: true,
        state: manager.get(agent_id)?.state,
      });
    } else {
      res.status(409).json(result);
    }
  });

  // ── COMPLETE EXECUTION ────────────────────────────────────────────────
  app.post('/api/agents/complete-execution', (req, res) => {
    const { agent_id, vault_sealed } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.completeExecution(agent_id, { sealed: !!vault_sealed });
    if (result.ok) {
      res.json({
        ok: true,
        state: manager.get(agent_id)?.state,
      });
    } else {
      res.status(409).json(result);
    }
  });

  // ── STOP ──────────────────────────────────────────────────────────────
  app.post('/api/agents/stop', (req, res) => {
    const { agent_id, reason } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.stop(agent_id, reason || 'api_call');
    if (result.ok) {
      res.json({ ok: true, state: 'stopped' });
    } else {
      res.status(409).json(result);
    }
  });

  // ── DEPROVISION ───────────────────────────────────────────────────────
  app.post('/api/agents/deprovision', (req, res) => {
    const { agent_id } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.deprovision(agent_id);
    if (result.ok) {
      res.json({ ok: true, state: 'deprovisioned' });
    } else {
      res.status(409).json(result);
    }
  });

  // ── HOLD ──────────────────────────────────────────────────────────────
  app.post('/api/agents/hold', (req, res) => {
    const { agent_id, reason } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.hold(agent_id, reason || 'api_hold');
    if (result.ok) {
      res.json({ ok: true, state: 'held' });
    } else {
      res.status(409).json(result);
    }
  });

  // ── DEGRADE ───────────────────────────────────────────────────────────
  app.post('/api/agents/degrade', (req, res) => {
    const { agent_id, error } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.degrade(agent_id, error || 'unknown_error');
    if (result.ok) {
      res.json({ ok: true, state: 'degraded' });
    } else {
      res.status(409).json(result);
    }
  });

  // ── RELEASE (F13) ─────────────────────────────────────────────────────
  app.post('/api/agents/release', (req, res) => {
    const { agent_id, human_ratifier } = req.body;
    if (!agent_id || !human_ratifier) {
      return res.status(400).json({ ok: false, error: 'agent_id + human_ratifier required' });
    }
    // F13 check: only arif-fazil can release
    if (human_ratifier !== 'arif-fazil') {
      return res.status(403).json({ ok: false, error: 'F13_SOVEREIGN: only arif-fazil may release agents' });
    }
    const result = manager.release(agent_id, human_ratifier);
    if (result.ok) {
      res.json({ ok: true, state: 'authorized' });
    } else {
      res.status(409).json(result);
    }
  });

  // ── TERMINATE ─────────────────────────────────────────────────────────
  app.post('/api/agents/terminate', (req, res) => {
    const { agent_id, reason } = req.body;
    if (!agent_id) {
      return res.status(400).json({ ok: false, error: 'agent_id required' });
    }
    const result = manager.terminate(agent_id, reason || 'api_terminate');
    if (result.ok) {
      res.json({ ok: true, state: 'terminated' });
    } else {
      res.status(409).json(result);
    }
  });

  // ── FEDERATION STATUS (must be before :agentId to avoid route collision) ──
  app.get('/api/agents/federation-status', (req, res) => {
    const status = manager.federationStatus();
    res.json({
      ok: true,
      ...status,
      timestamp: new Date().toISOString(),
    });
  });

  // ── ACTIVE AGENTS ─────────────────────────────────────────────────────
  app.get('/api/agents', (req, res) => {
    const active = manager.getActive();
    res.json({
      ok: true,
      count: active.length,
      agents: active,
    });
  });

  // ── SINGLE AGENT STATUS (must come AFTER /federation-status and / path) ──
  app.get('/api/agents/:agentId', (req, res) => {
    const instance = manager.get(req.params.agentId);
    if (!instance) {
      return res.status(404).json({ ok: false, error: `Agent ${req.params.agentId} not found` });
    }
    res.json({
      ok: true,
      ...instance.summary(),
      transitionHistory: instance.transitionHistory.slice(-10),
    });
  });

  console.log('[AAA] Agent lifecycle routes mounted: /api/agents/*');
}

module.exports = { mountLifecycleRoutes };
