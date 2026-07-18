#!/usr/bin/env node
/**
 * A2A Agent Seed — registers all 8 forge instruments at AAA boot.
 * Called after agent-card-registry auto-loads CIV-33 cards.
 */

const http = require('http');

const AGENTS = [
  { id: 'opencode',     fi: 'FI-001', model: 'deepseek/deepseek-v4-pro',          mcp: 13, role: 'orchestrator' },
  { id: 'claude-code',  fi: 'FI-002', model: 'deepseek/deepseek-v4-pro (Anthropic)', mcp: 20, role: 'architect' },
  { id: 'qwen-code',    fi: 'FI-003', model: 'MiniMax-M3',                        mcp: 0,  role: 'dormant' },
  { id: 'antigravity',  fi: 'FI-004', model: 'Gemini 3.5 Flash',                  mcp: 6,  role: 'executor' },
  { id: 'codex-cli',    fi: 'FI-005', model: 'gpt-5.6-sol',                       mcp: 8,  role: 'forge' },
  { id: 'copilot-cli',  fi: 'FI-006', model: 'deepseek-v4-pro (Anthropic compat)', mcp: 11, role: 'forge' },
  { id: 'grok-build',   fi: 'FI-007', model: 'grok-build (xAI)',                   mcp: 0,  role: 'forge' },
  { id: 'kimi-code',    fi: 'FI-008', model: 'minimax-coding-plan/MiniMax-M3',     mcp: 9,  role: 'forge' },
];

async function seed() {
  const base = 'http://127.0.0.1:3001';
  
  for (const agent of AGENTS) {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      method: 'agent/register',
      params: {
        agent_id: agent.id,
        name: `${agent.id} (${agent.fi})`,
        model: agent.model,
        mcp_count: agent.mcp,
        role: agent.role,
        citizenship: 'warga-aaa',
        status: 'active',
      },
      id: agent.fi,
    });

    const req = http.request(`${base}/a2a/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'A2A-Version': '1.0',
        'x-a2a-key': process.env.A2A_API_KEY || 'd62a567e9ae7f383f070f3fc78aadac4c8212855285fb984bbaa4e5376bacea1',
      },
    }, (res) => {
      let data = '';
      res.on('data', (c) => data += c);
      res.on('end', () => {
        const ok = res.statusCode < 400;
        console.log(`${ok ? '✅' : '❌'} ${agent.id} (${agent.fi}) — ${res.statusCode}`);
        if (!ok) console.log(`   ${data.substring(0, 120)}`);
      });
    });
    req.on('error', (e) => console.log(`❌ ${agent.id} — ${e.message}`));
    req.write(body);
    req.end();
    await new Promise(r => setTimeout(r, 200));
  }
  console.log('\nSeed complete. 8 agents registered.');
}

seed();
