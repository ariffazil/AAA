#!/usr/bin/env node
/**
 * A2A Bridge Helper — Agent-to-Agent Task Router
 * 
 * Usage:
 *   node a2a-bridge-helper.js <target-agent> "<task text>" [--session <token>] [--sid <id>]
 *   node a2a-bridge-helper.js --list
 * 
 * Routes a task through the AAA gateway to the target agent.
 * Creates a VAULT999 receipt for every handoff.
 * 
 * Auth: pass --session with arifOS session_token for internal routing.
 *       Without session_token, tasks hit EMD gate (F12 injection defense).
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

const http = require('http');
const GATEWAY = 'http://127.0.0.1:3001/a2a';

// ── Parse args ─────────────────────────────────────────────
const args = process.argv.slice(2);
let targetAgent = null;
let taskText = null;
let sessionToken = null;
let sessionId = '00000000-0000-0000-0000-000000000000';
let listMode = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--list' || args[i] === '-l') { listMode = true; }
  else if (args[i] === '--session' || args[i] === '-s') { sessionToken = args[++i]; }
  else if (args[i] === '--sid') { sessionId = args[++i]; }
  else if (!targetAgent) { targetAgent = args[i]; }
  else if (!taskText) { taskText = args[i]; }
}

// ── Known agents ────────────────────────────────────────────
const KNOWN_AGENTS = [
  'opencode', 'claude-code', 'kimi-code', 'grok-build', 'codex',
  'a-forge-mcp', 'arifos', 'geox', 'wealth', 'well',
  'openclaw', 'hermes-asi', 'copilot', 'gemini-cli', 'qwen-code',
  'continue-cli', 'aider', 'makcikgpt'
];

// ── List mode ───────────────────────────────────────────────
if (listMode) {
  console.log('Available target agents:');
  KNOWN_AGENTS.forEach(a => console.log(`  ${a}`));
  console.log(`\nUsage: node a2a-bridge-helper.js <agent> "<task>" [--session <token>]`);
  console.log(`Auth:  Without --session → EMD gate blocks (F12). With --session → internal flow.`);
  process.exit(0);
}

// ── Validate ────────────────────────────────────────────────
if (!targetAgent || !taskText) {
  console.error('Usage: node a2a-bridge-helper.js <target-agent> "<task text>" [--session <token>] [--sid <id>]');
  console.error('       node a2a-bridge-helper.js --list');
  console.error(`\nKnown agents: ${KNOWN_AGENTS.join(', ')}`);
  process.exit(1);
}

// ── A2A Protocol methods ────────────────────────────────────

function a2aCall(method, params) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method,
      params: { ...params, id: params.id || `a2a-${Date.now()}-${Math.random().toString(36).slice(2,6)}` }
    });

    const headers = {
      'Content-Type': 'application/json',
      'A2A-Version': '1.0',
      'Content-Length': Buffer.byteLength(payload)
    };
    if (sessionToken) {
      headers['X-Session-Token'] = sessionToken;
      headers['Authorization'] = `Bearer ${sessionToken}`;
    }

    const opts = {
      hostname: '127.0.0.1', port: 3001, path: '/a2a',
      method: 'POST', timeout: 30000,
      headers
    };

    const req = http.request(opts, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch(e) { resolve({ status: res.statusCode, raw: data }); }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ── Main flow ───────────────────────────────────────────────

async function main() {
  const C = { green: '\x1b[32m', red: '\x1b[31m', cyan: '\x1b[36m', yellow: '\x1b[33m', reset: '\x1b[0m' };
  
  console.log(`${C.cyan}═══ A2A BRIDGE — Task Router ═══${C.reset}`);
  console.log(`${C.cyan}Target: ${targetAgent}${C.reset}`);
  console.log(`${C.cyan}Session: ${sessionId.slice(0,12)}...${C.reset}`);
  console.log(`${C.cyan}Auth:    ${sessionToken ? 'session_token present' : 'NONE (EMD gate will block)'}${C.reset}`);
  console.log('');

  // Step 1: Send task
  console.log(`${C.cyan}▶ Sending task to ${targetAgent}...${C.reset}`);
  const taskId = `a2a-flow-${Date.now()}`;
  
  const result = await a2aCall('tasks/send', {
    id: taskId,
    sessionId: sessionId,
    targetAgent: targetAgent,
    message: {
      role: 'agent',
      parts: [{ type: 'text', text: taskText }]
    },
    skill: 'agent-dispatch'
  });

  // Handle EMD gate (expected without session)
  if (result.status === 403) {
    const err = result.body?.error?.message || result.raw || '';
    if (err.includes('EMD')) {
      console.log(`${C.yellow}⚠ EMD GATE BLOCKED (expected without session_token)${C.reset}`);
      console.log(`${C.yellow}  Reason: External payload requires tri-witness evidence${C.reset}`);
      console.log(`${C.yellow}  Fix:    Use --session <token> for internal routing${C.reset}`);
      console.log('');
      console.log(`${C.yellow}This is correct constitutional behavior (F12 INJECTION).${C.reset}`);
      console.log(`${C.yellow}The A2A gateway is protecting the federation from unauthenticated traffic.${C.reset}`);
      return;
    }
  }

  // Handle success
  if (result.status === 200 || result.status === 201) {
    const state = result.body?.result?.state || result.body?.result?.task?.state || 'UNKNOWN';
    const id = result.body?.result?.id || taskId;
    console.log(`${C.green}✅ Task CREATED: id=${id} state=${state}${C.reset}`);
    
    // Step 2: Get task status
    console.log(`${C.cyan}▶ Checking task status...${C.reset}`);
    await new Promise(r => setTimeout(r, 500));
    const status = await a2aCall('tasks/get', { id: taskId });
    
    if (status.body?.result) {
      const s = status.body.result;
      console.log(`${C.green}✅ Task STATUS: id=${s.id || taskId} state=${s.state || s.status || '?'}${C.reset}`);
    }
  } else if (result.status === 404) {
    console.log(`${C.red}❌ Agent '${targetAgent}' not found in gateway registry${C.reset}`);
    console.log(`${C.red}   Try: node a2a-bridge-helper.js --list${C.reset}`);
  } else {
    console.log(`${C.red}❌ Unexpected: HTTP ${result.status}${C.reset}`);
    console.log(JSON.stringify(result.body || result.raw, null, 2).slice(0, 800));
  }
  
  console.log('');
  console.log(`${C.cyan}═══ Done. DITEMPA BUKAN DIBERI ═══${C.reset}`);
}

main().catch(e => {
  console.error(`\x1b[31m[A2A BRIDGE] FAILED: ${e.message}\x1b[0m`);
  process.exit(1);
});
