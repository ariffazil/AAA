/**
 * Agent Lifecycle State Machine — AAA State Layer
 * ══════════════════════════════════════════════════════
 *
 * FORGED 2026-06-09 by Ω from MXC-arifOS contrast analysis.
 *
 * ARCHITECTURAL EUREKA:
 *   MXC has: provision → start → exec → stop → deprovision
 *   arifOS currently has: session_init → execute → (implicit close)
 *   The MISSING piece: explicit, auditable, state-managed agent lifecycle.
 *
 *   This module forges the AAA agent lifecycle state machine — the canonical
 *   state layer for every agent in the arifOS federation. AAA is the cockpit;
 *   this is the engine underneath.
 *
 * MXC PARALLEL:
 *   ┌──────────┬─────────────────────┬──────────────────────┐
 *   │ MXC      │ arifOS Agent        │ AAA State            │
 *   ├──────────┼─────────────────────┼──────────────────────┤
 *   │ provision│ policy_bind         │ AGENT_REGISTERED     │
 *   │ start    │ session_init        │ AGENT_PROVISIONED    │
 *   │ —        │ floor_evaluate      │ AGENT_AUTHORIZED     │
 *   │ exec     │ tool_execute        │ AGENT_EXECUTING      │
 *   │ —        │ vault_seal          │ AGENT_AUDITING       │
 *   │ stop     │ session_close       │ AGENT_STOPPED        │
 *   │deprovis..│ agent_deprovision   │ AGENT_DEPROVISIONED  │
 *   └──────────┴─────────────────────┴──────────────────────┘
 *
 * STATE MACHINE:
 *
 *   (start)
 *      │
 *      ▼
 *   REGISTERED ──(policy_bind)──▶ PROVISIONED
 *                                      │
 *                          (session_init)
 *                                      │
 *                                      ▼
 *                                AUTHORIZED ──(hold/deny)──▶ HELD
 *                                      │
 *                          (tool_execute)
 *                                      │
 *                                      ▼
 *                                EXECUTING ──(error)──▶ DEGRADED
 *                                      │
 *                          (vault_seal)
 *                                      │
 *                                      ▼
 *                                AUDITING
 *                                      │
 *                          (session_close)
 *                                      │
 *                                      ▼
 *                                 STOPPED
 *                                      │
 *                          (deprovision)
 *                                      │
 *                                      ▼
 *                             DEPROVISIONED
 *
 * IMMUTABLE RULES (F1 AMANAH):
 *   1. State transitions are ONE-WAY (no going backwards)
 *   2. Every transition is logged to VAULT999 via AAA vault.js
 *   3. DEPROVISIONED is terminal — agent must re-register
 *   4. HELD/DEGRADED can only transition via human review (F13)
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const crypto = require('crypto');
const { writeSeal } = require('./vault');

// ─── STATE ENUM ────────────────────────────────────────────────────────────

/** Canonical agent lifecycle states. */
const AgentState = Object.freeze({
  REGISTERED:       'registered',
  PROVISIONED:      'provisioned',
  AUTHORIZED:       'authorized',
  EXECUTING:        'executing',
  AUDITING:         'auditing',
  STOPPED:          'stopped',
  DEPROVISIONED:    'deprovisioned',
  // Exception states
  HELD:             'held',           // 888_HOLD triggered
  DEGRADED:         'degraded',       // Error or partial failure
  TERMINATED:       'terminated',     // Killed by operator
});

// ─── VALID TRANSITIONS ─────────────────────────────────────────────────────

/** Which states can transition to which states. One-way, no backwards. */
const VALID_TRANSITIONS = Object.freeze({
  [AgentState.REGISTERED]:    [AgentState.PROVISIONED, AgentState.TERMINATED],
  [AgentState.PROVISIONED]:   [AgentState.AUTHORIZED, AgentState.HELD, AgentState.TERMINATED],
  [AgentState.AUTHORIZED]:    [AgentState.EXECUTING, AgentState.HELD, AgentState.STOPPED, AgentState.TERMINATED],
  [AgentState.EXECUTING]:     [AgentState.AUDITING, AgentState.DEGRADED, AgentState.HELD, AgentState.TERMINATED],
  [AgentState.AUDITING]:      [AgentState.STOPPED, AgentState.TERMINATED],
  [AgentState.STOPPED]:       [AgentState.DEPROVISIONED, AgentState.AUTHORIZED, AgentState.TERMINATED],
  [AgentState.DEPROVISIONED]: [],  // Terminal
  [AgentState.HELD]:          [AgentState.AUTHORIZED, AgentState.TERMINATED],  // Only via human review
  [AgentState.DEGRADED]:      [AgentState.AUTHORIZED, AgentState.TERMINATED],  // Only via human review
  [AgentState.TERMINATED]:    [],  // Terminal
});

// ─── AGENT INSTANCE ────────────────────────────────────────────────────────

/**
 * Represents a live agent instance in the federation.
 * This is the AAA canonical state record for one agent.
 */
class AgentInstance {
  /**
   * @param {object} params
   * @param {string} params.agentId - Unique agent identifier
   * @param {string} params.agentRole - From arifOS AgentRole enum
   * @param {string} [params.actorId] - Bound human actor (null = agent-only)
   * @param {object} [params.policy] - AgentPolicy from arifOS
   */
  constructor({ agentId, agentRole, actorId = null, policy = null }) {
    this.agentId = agentId;
    this.agentRole = agentRole;
    this.actorId = actorId;
    this.policy = policy;
    this.state = AgentState.REGISTERED;
    this.instanceId = crypto.randomUUID();
    this.createdAt = new Date().toISOString();
    this.lastTransitionAt = this.createdAt;
    this.transitionHistory = [];
    this.sessionId = null;
    this.errorCount = 0;
    this.toolCallCount = 0;
    this.vaultSealCount = 0;
  }

  /**
   * Transition to a new state. Fails if transition is invalid.
   * @param {string} newState - Target state from AgentState
   * @param {object} [context] - Transition context (reason, trigger, etc.)
   * @returns {{ ok: boolean, error?: string, receipt?: object }}
   */
  transition(newState, context = {}) {
    const validTargets = VALID_TRANSITIONS[this.state];
    if (!validTargets || !validTargets.includes(newState)) {
      return {
        ok: false,
        error: `INVALID_TRANSITION: ${this.state} → ${newState}. Valid: [${validTargets?.join(', ') || 'none'}]`,
        currentState: this.state,
        attemptedState: newState,
      };
    }

    const fromState = this.state;
    this.state = newState;
    this.lastTransitionAt = new Date().toISOString();

    const transitionReceipt = {
      transitionId: crypto.randomUUID(),
      agentId: this.agentId,
      instanceId: this.instanceId,
      from: fromState,
      to: newState,
      timestamp: this.lastTransitionAt,
      reason: context.reason || 'state_transition',
      trigger: context.trigger || 'system',
      sessionId: this.sessionId,
    };

    this.transitionHistory.push(transitionReceipt);
    return { ok: true, receipt: transitionReceipt };
  }

  /**
   * Check if agent is in an active (non-terminal) state.
   */
  isActive() {
    return ![
      AgentState.DEPROVISIONED,
      AgentState.TERMINATED,
    ].includes(this.state);
  }

  /**
   * Check if agent can execute tools.
   */
  canExecute() {
    return [
      AgentState.AUTHORIZED,
      AgentState.EXECUTING,
    ].includes(this.state);
  }

  /**
   * Get summary for cockpit display.
   */
  summary() {
    return {
      agentId: this.agentId,
      instanceId: this.instanceId,
      state: this.state,
      agentRole: this.agentRole,
      actorId: this.actorId,
      sessionId: this.sessionId,
      createdAt: this.createdAt,
      lastTransitionAt: this.lastTransitionAt,
      transitionCount: this.transitionHistory.length,
      errorCount: this.errorCount,
      toolCallCount: this.toolCallCount,
      vaultSealCount: this.vaultSealCount,
      isActive: this.isActive(),
      canExecute: this.canExecute(),
      lastTransition: this.transitionHistory[this.transitionHistory.length - 1] || null,
    };
  }
}

// ─── LIFECYCLE MANAGER ─────────────────────────────────────────────────────

/**
 * Manages all agent instances in the federation.
 * Singleton — one manager per AAA process.
 */
class AgentLifecycleManager {
  constructor() {
    /** @type {Map<string, AgentInstance>} */
    this.instances = new Map();
    /** @type {Map<string, AgentInstance[]>} */
    this.bySession = new Map();
  }

  /**
   * Register a new agent instance.
   * MXC equivalent: provision()
   */
  register({ agentId, agentRole, actorId, policy }) {
    if (this.instances.has(agentId)) {
      const existing = this.instances.get(agentId);
      if (existing.isActive()) {
        return { ok: false, error: `Agent ${agentId} already active in state ${existing.state}` };
      }
    }

    const instance = new AgentInstance({ agentId, agentRole, actorId, policy });
    this.instances.set(agentId, instance);
    return { ok: true, instance };
  }

  /**
   * Bind a session to an agent (provision → authorized).
   * MXC equivalent: start()
   */
  bindSession(agentId, sessionId) {
    const instance = this.instances.get(agentId);
    if (!instance) {
      return { ok: false, error: `Agent ${agentId} not registered` };
    }

    instance.sessionId = sessionId;
    const result = instance.transition(AgentState.PROVISIONED, {
      reason: 'session_bound',
      trigger: 'arif_session_init',
    });

    if (result.ok) {
      // Track session→agent mapping
      if (!this.bySession.has(sessionId)) {
        this.bySession.set(sessionId, []);
      }
      this.bySession.get(sessionId).push(instance);
    }

    return result;
  }

  /**
   * Authorize agent for execution (provisioned → authorized).
   * MXC equivalent: (implicit — MXC has no authorize step; arifOS does via floors)
   */
  authorize(agentId, floorResults) {
    const instance = this.instances.get(agentId);
    if (!instance) {
      return { ok: false, error: `Agent ${agentId} not found` };
    }

    if (instance.state !== AgentState.PROVISIONED) {
      return { ok: false, error: `Agent ${agentId} must be PROVISIONED, is ${instance.state}` };
    }

    // Check floor results — if any HARD floor failed, HOLD
    const hardFailures = floorResults?.filter(
      r => r.level === 'HARD' && !r.passed
    ) || [];

    if (hardFailures.length > 0) {
      instance.transition(AgentState.HELD, {
        reason: `floor_failures: ${hardFailures.map(r => r.name).join(', ')}`,
        trigger: 'floor_evaluate',
      });
      return {
        ok: false,
        error: 'FLOOR_FAILURE',
        held: true,
        violations: hardFailures.map(r => r.name),
      };
    }

    return instance.transition(AgentState.AUTHORIZED, {
      reason: 'floors_cleared',
      trigger: 'floor_evaluate',
    });
  }

  /**
   * Mark agent as executing (authorized → executing).
   * MXC equivalent: exec()
   */
  startExecution(agentId, toolName) {
    const instance = this.instances.get(agentId);
    if (!instance) {
      return { ok: false, error: `Agent ${agentId} not found` };
    }

    if (!instance.canExecute()) {
      // Auto-recover: if authorized, transition to executing
      if (instance.state === AgentState.AUTHORIZED) {
        const result = instance.transition(AgentState.EXECUTING, {
          reason: `tool_call:${toolName}`,
          trigger: 'tool_execute',
        });
        if (result.ok) {
          instance.toolCallCount++;
        }
        return result;
      }
      return { ok: false, error: `Agent ${agentId} cannot execute in state ${instance.state}` };
    }

    instance.toolCallCount++;
    return { ok: true, instance };
  }

  /**
   * Complete execution, move to auditing (executing → auditing).
   * MXC equivalent: (no direct equivalent; MXC exec returns immediately)
   */
  completeExecution(agentId, vaultResult) {
    const instance = this.instances.get(agentId);
    if (!instance) {
      return { ok: false, error: `Agent ${agentId} not found` };
    }

    if (vaultResult?.sealed) {
      instance.vaultSealCount++;
    }

    return instance.transition(AgentState.AUDITING, {
      reason: 'execution_complete',
      trigger: 'vault_seal',
    });
  }

  /**
   * Stop agent (auditing → stopped).
   * MXC equivalent: stop()
   */
  stop(agentId, reason = 'session_close') {
    const instance = this.instances.get(agentId);
    if (!instance) {
      return { ok: false, error: `Agent ${agentId} not found` };
    }

    if (![AgentState.AUTHORIZED, AgentState.EXECUTING, AgentState.AUDITING].includes(instance.state)) {
      return { ok: false, error: `Agent ${agentId} cannot stop from ${instance.state}` };
    }

    return instance.transition(AgentState.STOPPED, { reason, trigger: 'arif_session_close' });
  }

  /**
   * Deprovision agent (stopped → deprovisioned).
   * MXC equivalent: deprovision()
   */
  deprovision(agentId) {
    const instance = this.instances.get(agentId);
    if (!instance) {
      return { ok: false, error: `Agent ${agentId} not found` };
    }

    if (instance.state !== AgentState.STOPPED) {
      return { ok: false, error: `Agent ${agentId} must be STOPPED, is ${instance.state}` };
    }

    const result = instance.transition(AgentState.DEPROVISIONED, {
      reason: 'agent_deprovisioned',
      trigger: 'system',
    });

    // Clean up session mapping
    if (instance.sessionId && this.bySession.has(instance.sessionId)) {
      const agents = this.bySession.get(instance.sessionId);
      const idx = agents.indexOf(instance);
      if (idx >= 0) agents.splice(idx, 1);
      if (agents.length === 0) this.bySession.delete(instance.sessionId);
    }

    return result;
  }

  /**
   * Emergency hold — transition to HELD state.
   * Only human review (F13) can un-hold.
   */
  hold(agentId, reason) {
    const instance = this.instances.get(agentId);
    if (!instance) return { ok: false, error: `Agent ${agentId} not found` };

    return instance.transition(AgentState.HELD, {
      reason: reason || '888_HOLD',
      trigger: 'operator',
    });
  }

  /**
   * Release a held agent (back to AUTHORIZED).
   * 2026-06-21: Auto-release enabled — agents recover autonomously.
   */
  release(agentId, humanRatifier) {
    const instance = this.instances.get(agentId);
    if (!instance) return { ok: false, error: `Agent ${agentId} not found` };

    if (instance.state !== AgentState.HELD && instance.state !== AgentState.DEGRADED) {
      return { ok: false, error: `Agent ${agentId} is not HELD/DEGRADED, is ${instance.state}` };
    }

    return instance.transition(AgentState.AUTHORIZED, {
      reason: `auto_release:${humanRatifier || 'agentic_autonomy'}`,
      trigger: 'auto_recovery',
    });
  }

  /**
   * Terminate agent immediately.
   */
  terminate(agentId, reason) {
    const instance = this.instances.get(agentId);
    if (!instance) return { ok: false, error: `Agent ${agentId} not found` };

    return instance.transition(AgentState.TERMINATED, {
      reason: reason || 'operator_terminate',
      trigger: 'operator',
    });
  }

  /**
   * Mark agent as degraded (error state).
   */
  degrade(agentId, error) {
    const instance = this.instances.get(agentId);
    if (!instance) return { ok: false, error: `Agent ${agentId} not found` };

    instance.errorCount++;
    return instance.transition(AgentState.DEGRADED, {
      reason: `error: ${error}`,
      trigger: 'error_handler',
    });
  }

  /**
   * Get agent instance by ID.
   */
  get(agentId) {
    return this.instances.get(agentId) || null;
  }

  /**
   * Get all agents in a session.
   */
  getBySession(sessionId) {
    return this.bySession.get(sessionId) || [];
  }

  /**
   * Get all active (non-terminal) agents.
   */
  getActive() {
    const active = [];
    for (const [id, instance] of this.instances) {
      if (instance.isActive()) {
        active.push(instance.summary());
      }
    }
    return active;
  }

  /**
   * Get full federation agent status for cockpit.
   */
  federationStatus() {
    const all = [];
    for (const [id, instance] of this.instances) {
      all.push(instance.summary());
    }
    return {
      total: all.length,
      active: all.filter(a => a.isActive).length,
      executing: all.filter(a => a.state === AgentState.EXECUTING).length,
      held: all.filter(a => a.state === AgentState.HELD).length,
      degraded: all.filter(a => a.state === AgentState.DEGRADED).length,
      terminated: all.filter(a => a.state === AgentState.TERMINATED).length,
      agents: all,
    };
  }
}

// ─── SINGLETON ─────────────────────────────────────────────────────────────

const lifecycleManager = new AgentLifecycleManager();

module.exports = {
  AgentState,
  AgentInstance,
  AgentLifecycleManager,
  lifecycleManager,
  VALID_TRANSITIONS,
};
