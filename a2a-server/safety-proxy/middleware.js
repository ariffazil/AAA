#!/usr/bin/env node
/**
 * middleware.js — hermes_safety_proxy Express Middleware
 * ======================================================
 * The Constitutional Interceptor.
 *
 * Sits between every agent request and the A-FORGE MCP execution layer.
 * Intercepts → Classifies → Validates → Routes → Audits.
 *
 * Flow:
 *   1. Extract tool_name, command, action_class from request
 *   2. Classify via policy engine (AUTO_PASS / JITU_REQUIRED / DENY)
 *   3. If JITU_REQUIRED: validate JITU token
 *   4. If DENY: block + log to seal_chain
 *   5. If AUTO_PASS or valid JITU: forward + log to seal_chain
 *
 *   ┌─────────┐     POST /tool     ┌──────────────────┐     forward     ┌──────────┐
 *   │  Agent  │ ──────────────────► │  safety_proxy    │ ──────────────► │  A-FORGE │
 *   │         │ ◄────── 403 ─────── │  middleware.js   │ ◄── deny ─────  │  MCP     │
 *   └─────────┘                     └────────┬─────────┘                 └──────────┘
 *                                            │
 *                                            ▼
 *                                   ┌────────────────┐
 *                                   │  seal_chain.js │   ← every decision logged
 *                                   └────────────────┘
 *
 * F1 AMANAH: Every decision is reversible (forward) or logged (deny).
 * F11 AUDIT: Every decision writes to the hash chain.
 * F13 SOVEREIGN: DENY actions cannot be overridden without physical Arif approval.
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

const crypto = require('crypto');
const { classifyAction, isReadOnlyMode, TIERS } = require('./policy');
const { validateJituToken, hashPayload, createJituToken } = require('./jitu_token');

// ── Seal chain writer (lazy-loaded to avoid circular deps) ────────────────

let _writeSeal = null;

function getSealWriter() {
  if (_writeSeal) return _writeSeal;
  try {
    const sealChain = require('../seal_chain');
    _writeSeal = sealChain.writeSeal || sealChain.write_seal;
    return _writeSeal;
  } catch {
    // Fallback: log to console if seal_chain not available
    return (entry) => {
      console.warn('[safety-proxy] seal_chain unavailable, logging to console:', JSON.stringify(entry));
    };
  }
}

// ── Statistics ────────────────────────────────────────────────────────────

const stats = {
  total: 0,
  auto_pass: 0,
  jitu_required: 0,
  jitu_granted: 0,
  jitu_denied: 0,
  deny: 0,
  errors: 0,
  started_at: new Date().toISOString(),
};

// ── Request extraction ────────────────────────────────────────────────────

/**
 * Extract action metadata from an Express request.
 * Handles multiple payload shapes:
 *   - A2A task dispatch: { task: { tool_name, arguments } }
 *   - Direct MCP call: { tool_name, arguments, command }
 *   - Forge shell: { command, cwd }
 *   - Generic: { action, payload }
 */
function extractActionMetadata(req) {
  const body = req.body || {};

  // Shape 1: A2A task dispatch
  if (body.task) {
    const task = body.task;
    return {
      tool_name: task.tool_name || task.tool || null,
      command: task.command || task.arguments?.command || null,
      action_class: task.action_class || task.actionClass || null,
      actor_id: task.actor_id || task.actor || body.actor_id || req.headers['x-actor-id'] || 'unknown',
      arguments: task.arguments || {},
      session_id: task.session_id || body.session_id || req.headers['x-session-id'] || null,
    };
  }

  // Shape 2: Direct tool call
  if (body.tool_name || body.tool) {
    return {
      tool_name: body.tool_name || body.tool || null,
      command: body.command || body.arguments?.command || null,
      action_class: body.action_class || body.actionClass || null,
      actor_id: body.actor_id || req.headers['x-actor-id'] || 'unknown',
      arguments: body.arguments || {},
      session_id: body.session_id || req.headers['x-session-id'] || null,
    };
  }

  // Shape 3: Forge shell command
  if (body.command && !body.tool_name) {
    return {
      tool_name: 'forge_shell',
      command: body.command,
      action_class: 'MUTATE',
      actor_id: body.actor_id || req.headers['x-actor-id'] || 'unknown',
      arguments: body,
      session_id: body.session_id || req.headers['x-session-id'] || null,
    };
  }

  // Shape 4: Generic — classify by HTTP method
  return {
    tool_name: null,
    command: null,
    action_class: req.method === 'GET' ? 'OBSERVE' : 'MUTATE',
    actor_id: body.actor_id || req.headers['x-actor-id'] || 'unknown',
    arguments: body,
    session_id: body.session_id || req.headers['x-session-id'] || null,
  };
}

// ── Audit logging ─────────────────────────────────────────────────────────

/**
 * Log a safety proxy decision to the seal chain.
 * Fire-and-forget — never blocks the request.
 */
function auditDecision(decision) {
  const writeSeal = getSealWriter();
  if (!writeSeal) return;

  const entry = {
    event_type: 'safety_proxy.decision',
    principal: `agent:${decision.actor_id}`,
    verdict: decision.tier === TIERS.DENY ? 'VOID' : (decision.tier === TIERS.AUTO_PASS ? 'SEAL' : 'HOLD'),
    payload: {
      tool_name: decision.tool_name,
      tier: decision.tier,
      reason: decision.reason,
      floor: decision.floor,
      pattern: decision.pattern,
      jitu_token: decision.jitu_token ? 'present' : 'absent',
      jitu_valid: decision.jitu_valid || false,
      session_id: decision.session_id,
      command_preview: decision.command ? decision.command.substring(0, 200) : null,
    },
  };

  try {
    writeSeal(entry);
  } catch (err) {
    console.error('[safety-proxy] seal write failed:', err.message);
  }
}

// ── Main middleware ────────────────────────────────────────────────────────

/**
 * Create the safety proxy middleware.
 *
 * @param {object} [options]
 * @param {string[]} [options.exempt_paths] — paths to skip (e.g., ['/health', '/approvals'])
 * @param {boolean} [options.dry_run] — if true, log but don't block
 * @param {Function} [options.on_deny] — callback on deny events
 * @param {Function} [options.on_jitu] — callback on JITU_REQUIRED events
 * @returns {Function} Express middleware
 */
function createSafetyProxy(options = {}) {
  const {
    exempt_paths = ['/health', '/approvals', '/approvals/pending', '/.well-known', '/a2a/agents.json'],
    dry_run = false,
    on_deny = null,
    on_jitu = null,
  } = options;

  return function safetyProxyMiddleware(req, res, next) {
    // Skip exempt paths
    if (exempt_paths.some(p => req.path.startsWith(p))) {
      return next();
    }

    // Skip GET requests (read-only by HTTP semantics)
    if (req.method === 'GET') {
      stats.total++;
      stats.auto_pass++;
      return next();
    }

    // Extract action metadata
    const meta = extractActionMetadata(req);
    stats.total++;

    // Classify the action
    const classification = classifyAction(meta);

    // Handle read-only mode overrides for multi-mode tools
    if (classification.tier === TIERS.JITU_REQUIRED && isReadOnlyMode(meta.tool_name, meta.arguments)) {
      classification.tier = TIERS.AUTO_PASS;
      classification.reason = `AUTO_PASS: tool '${meta.tool_name}' in read-only mode (${meta.arguments?.mode})`;
      classification.floor = null;
    }

    // ── AUTO_PASS: forward immediately ─────────────────────────────────
    if (classification.tier === TIERS.AUTO_PASS) {
      stats.auto_pass++;

      // Attach classification to request for downstream use
      req._safetyProxy = {
        tier: TIERS.AUTO_PASS,
        classification,
        meta,
        timestamp: new Date().toISOString(),
      };

      auditDecision({
        ...classification,
        ...meta,
        jitu_valid: false,
      });

      return next();
    }

    // ── DENY: block immediately ────────────────────────────────────────
    if (classification.tier === TIERS.DENY) {
      stats.deny++;

      auditDecision({
        ...classification,
        ...meta,
        jitu_valid: false,
      });

      if (on_deny) {
        on_deny({ classification, meta, req });
      }

      if (dry_run) {
        console.warn(`[safety-proxy] DRY_RUN DENY: ${classification.reason} | tool=${meta.tool_name} actor=${meta.actor_id}`);
        req._safetyProxy = { tier: TIERS.DENY, classification, meta, dry_run: true };
        return next();
      }

      return res.status(403).json({
        error: 'CONSTITUTIONAL_DENY',
        tier: 'DENY',
        reason: classification.reason,
        floor: classification.floor,
        tool: meta.tool_name,
        hint: classification.floor === 'F13'
          ? 'This action requires explicit F13 SOVEREIGN approval (Arif). Contact the sovereign directly.'
          : 'This action violates constitutional floors. Review and reformulate.',
        receipt: {
          timestamp: new Date().toISOString(),
          actor: meta.actor_id,
          tool: meta.tool_name,
        },
      });
    }

    // ── JITU_REQUIRED: validate token ──────────────────────────────────
    if (classification.tier === TIERS.JITU_REQUIRED) {
      stats.jitu_required++;

      // Extract JITU token from headers or body
      const jituToken = req.headers['x-jitu-token']
        || req.body?.jitu_token
        || req.body?.task?.jitu_token
        || null;

      // Compute payload hash for binding check
      const payloadHash = hashPayload(meta.arguments);

      // Validate token
      const validation = validateJituToken(jituToken, {
        tool_name: meta.tool_name,
        actor_id: meta.actor_id,
        payload_hash: payloadHash,
      });

      if (validation.valid) {
        // Token valid — forward
        stats.jitu_granted++;

        req._safetyProxy = {
          tier: TIERS.JITU_REQUIRED,
          classification,
          meta,
          jitu_payload: validation.payload,
          timestamp: new Date().toISOString(),
        };

        auditDecision({
          ...classification,
          ...meta,
          jitu_token: jituToken ? 'present' : 'absent',
          jitu_valid: true,
        });

        return next();
      }

      // Token invalid or missing
      stats.jitu_denied++;

      auditDecision({
        ...classification,
        ...meta,
        jitu_token: jituToken ? 'present' : 'absent',
        jitu_valid: false,
      });

      if (on_jitu) {
        on_jitu({ classification, meta, jituToken, validation, req });
      }

      if (dry_run) {
        console.warn(`[safety-proxy] DRY_RUN JITU_REQUIRED: ${classification.reason} | tool=${meta.tool_name} actor=${meta.actor_id} error=${validation.error}`);
        req._safetyProxy = { tier: TIERS.JITU_REQUIRED, classification, meta, dry_run: true };
        return next();
      }

      return res.status(401).json({
        error: 'JITU_REQUIRED',
        tier: 'JITU_REQUIRED',
        reason: classification.reason,
        floor: classification.floor,
        tool: meta.tool_name,
        jitu_error: validation.error,
        hint: 'This action requires a valid JITU token. Request approval from the sovereign or use an auto-approved path.',
        get_token: {
          endpoint: '/safety-proxy/request-jitu',
          method: 'POST',
          body: {
            tool_name: meta.tool_name,
            actor_id: meta.actor_id,
            command: meta.command,
            justification: 'Describe why this action is needed',
          },
        },
        receipt: {
          timestamp: new Date().toISOString(),
          actor: meta.actor_id,
          tool: meta.tool_name,
        },
      });
    }

    // Should not reach here, but safe default
    stats.errors++;
    return res.status(500).json({
      error: 'CLASSIFICATION_ERROR',
      detail: 'Action could not be classified. Defaulting to deny.',
    });
  };
}

// ── Stats endpoint handler ────────────────────────────────────────────────

function getStats() {
  return {
    ...stats,
    uptime_seconds: Math.floor((Date.now() - new Date(stats.started_at).getTime()) / 1000),
    grant_rate: stats.jitu_required > 0
      ? (stats.jitu_granted / stats.jitu_required * 100).toFixed(1) + '%'
      : 'N/A',
  };
}

// ── Exports ───────────────────────────────────────────────────────────────

module.exports = {
  createSafetyProxy,
  extractActionMetadata,
  auditDecision,
  getStats,
  stats,
};
