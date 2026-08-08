/**
 * ART Gate — Admission Gate for AAA Gateway.
 * 
 * Question: "May this call enter?"
 * 
 * For MUTATE/DEPLOY/IRREVERSIBLE actions, delegates to arifOS kernel
 * for constitutional admission review.
 * For OBSERVE/REASON/DRAFT, passes through.
 * 
 * DITEMPA BUKAN DIBERI.
 * Forged: 2026-08-08 by 333-AGI.
 */

const crypto = require('crypto');

const ARIFOS_URL = process.env.ARIFOS_LOCAL_URL || 'http://127.0.0.1:8088';

/**
 * Classify action from intent text.
 * @param {string} text - Intent text
 * @returns {string} Action class: OBSERVE | REASON | DRAFT | MUTATE | DEPLOY | IRREVERSIBLE
 */
function classifyAction(text) {
  const lower = (text || '').toLowerCase();
  
  // Irreversible
  if (/rm\s+-rf|drop\s+table|force\s+push|delete\s+vault|chattr\s+\-a/i.test(lower)) {
    return 'IRREVERSIBLE';
  }
  // Deploy
  if (/deploy|production|caddy\s+reload|docker\s+push|systemctl\s+restart/i.test(lower)) {
    return 'DEPLOY';
  }
  // Mutate
  if (/edit|write|commit|push|restart|build|forge|create\s+file|update|modify|patch|install|unlink|mutate/i.test(lower)) {
    return 'MUTATE';
  }
  // Draft
  if (/generate|draft|scaffold|plan|propose|design/i.test(lower)) {
    return 'DRAFT';
  }
  // Reason
  if (/analyze|evaluate|simulate|compare|audit|review|judge|think/i.test(lower)) {
    return 'REASON';
  }
  return 'OBSERVE';
}

/**
 * Call arifOS kernel for constitutional ART review.
 * @param {object} params
 * @param {string} params.actionClass - Action class
 * @param {string} params.agentId - Agent ID
 * @param {string} [params.toolName] - Tool being called
 * @param {string} [params.intentText] - Intent text
 * @returns {Promise<{pass: boolean, verdict: string, reason: string, details: object}>}
 */
async function artGate(params = {}) {
  const { actionClass, agentId, toolName, intentText } = params;
  
  // OBSERVE and REASON always pass
  if (actionClass === 'OBSERVE' || actionClass === 'REASON') {
    return { pass: true, verdict: 'PROCEED', reason: `${actionClass} exempt from ART`, details: {} };
  }
  
  // DRAFT gets local pass (full ART deferred)
  if (actionClass === 'DRAFT') {
    return { pass: true, verdict: 'PROCEED', reason: 'DRAFT — local heuristic pass', details: { note: 'full ART deferred' } };
  }
  
  // MUTATE, DEPLOY, IRREVERSIBLE → call kernel
  const tierMap = {
    MUTATE: 'mutate',
    DEPLOY: 'deploy', 
    IRREVERSIBLE: 'irreversible',
  };
  
  try {
    const resp = await fetch(`${ARIFOS_URL}/mcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'tools/call',
        params: {
          name: 'arif_judge',
          arguments: {
            mode: 'judge',
            candidate: toolName || actionClass,
            action_tier: tierMap[actionClass] || 'standard',
            actor_id: agentId || 'aaa-gateway',
          },
        },
      }),
      signal: AbortSignal.timeout(5000),
    });
    
    if (!resp.ok) {
      throw new Error(`Kernel returned ${resp.status}`);
    }
    
    const data = await resp.json();
    const result = extractMcpResult(data);
    const verdict = (result.verdict || 'UNMEASURED').toUpperCase();
    
    if (verdict === 'VOID') {
      return {
        pass: false,
        verdict: 'VOID',
        reason: `Kernel ART VOID: ${JSON.stringify(result.reasons || ['constitutional block'])}`,
        details: result,
      };
    }
    if (verdict === 'HOLD') {
      return {
        pass: false,
        verdict: 'HOLD',
        reason: `Kernel ART HOLD: ${JSON.stringify(result.reasons || ['requires review'])}`,
        details: result,
      };
    }
    if (verdict === 'SABAR') {
      return {
        pass: true,
        verdict: 'SABAR',
        reason: `Kernel ART SABAR — proceeding with caution`,
        details: result,
      };
    }
    // SEAL or OK
    return { pass: true, verdict: 'PROCEED', reason: 'Kernel ART passed', details: result };
    
  } catch (err) {
    console.warn(`[art-gate] Kernel unreachable: ${err.message}`);
    // Fail-closed for DEPLOY/IRREVERSIBLE, degraded for MUTATE
    if (actionClass === 'DEPLOY' || actionClass === 'IRREVERSIBLE') {
      return {
        pass: false,
        verdict: 'HOLD',
        reason: `Kernel unreachable for ${actionClass}: ${err.message}`,
        details: { error: err.message },
      };
    }
    return {
      pass: true,
      verdict: 'SABAR',
      reason: `Kernel unreachable (degraded): ${err.message}`,
      details: { error: err.message },
    };
  }
}

/**
 * ACT Gate — Execution Gate for AAA Gateway.
 * 
 * Question: "May reality now change?"
 * 
 * Validates session token presence for MUTATE+ actions.
 * IRREVERSIBLE requires sovereign acknowledgment.
 * 
 * @param {object} params
 * @param {string} params.actionClass
 * @param {string} [params.sessionToken] - ACT/SCT token
 * @param {string} [params.agentId]
 * @returns {{pass: boolean, verdict: string, reason: string, details: object}}
 */
function actGate(params = {}) {
  const { actionClass, sessionToken, agentId } = params;
  
  // OBSERVE/REASON/DRAFT exempt
  if (actionClass === 'OBSERVE' || actionClass === 'REASON' || actionClass === 'DRAFT') {
    return { pass: true, verdict: 'PROCEED', reason: `${actionClass} exempt from ACT`, details: {} };
  }
  
  // MUTATE+ requires session token
  if (!sessionToken) {
    return {
      pass: false,
      verdict: 'HOLD',
      reason: `${actionClass} requires session_token (call arif_init first or provide ACT/SCT token)`,
      details: { missing: 'session_token' },
    };
  }
  
  // Validate format
  if (!sessionToken.startsWith('act_v1.') && !sessionToken.startsWith('sct_v1.')) {
    return {
      pass: false,
      verdict: 'HOLD',
      reason: `Invalid session_token format. Expected act_v1.* or sct_v1.*, got: ${sessionToken.substring(0, 20)}...`,
      details: { invalid_format: true },
    };
  }
  
  // IRREVERSIBLE requires explicit ack
  if (actionClass === 'IRREVERSIBLE') {
    return {
      pass: false,
      verdict: 'HOLD',
      reason: 'IRREVERSIBLE actions require explicit sovereign acknowledgment (ack_irreversible)',
      details: { required: 'ack_irreversible or F13 approval' },
    };
  }
  
  return { pass: true, verdict: 'PROCEED', reason: 'ACT gate passed', details: {} };
}

/**
 * Extract result from MCP JSON-RPC response (handles SSE wrapping).
 */
function extractMcpResult(data) {
  if (!data || !data.result) return data || {};
  const inner = data.result;
  if (inner && Array.isArray(inner.content)) {
    for (const item of inner.content) {
      if (item && item.text) {
        try {
          return JSON.parse(item.text);
        } catch (_) { /* not JSON */ }
      }
    }
  }
  return inner;
}

module.exports = { artGate, actGate, classifyAction };
