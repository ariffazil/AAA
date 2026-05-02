/**
 * WebMCP Tools for arif-fazil.com (BODY Layer)
 * 
 * Phase 1: Read-only governance tools
 * Purpose: Make human context machine-legible and verifiable
 * Floor Compliance: F1 (Amanah - reversible), F2 (Truth - factual), F9 (Anti-Hantu - no agency claims)
 */

import '@mcp-b/global';

type ToolResult = {
  content: Array<{ type: 'text'; text: string }>;
  isError?: boolean;
};

type WebMcpTool = {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, never>;
    required: string[];
  };
  execute: () => Promise<ToolResult> | ToolResult;
};

type ModelContext = {
  registerTool: (tool: WebMcpTool) => void;
};

type NavigatorWithModelContext = Navigator & {
  modelContext: ModelContext;
};

// Wait for polyfill to be ready
if (typeof navigator !== 'undefined' && 'modelContext' in navigator) {
  const mcp = (navigator as NavigatorWithModelContext).modelContext;

  // Tool 1: Get LLMs.txt (Sovereign Memory Context)
  mcp.registerTool({
    name: 'get_llms_txt',
    description: 'Retrieve the canonical llms.txt context file - human identity, scars, operating principles, and Trinity architecture',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    async execute() {
      try {
        const response = await fetch('/llms.txt', { cache: 'no-store' });
        const text = await response.text();
        return {
          content: [{
            type: 'text',
            text: `# BODY Layer Context (arif-fazil.com/llms.txt)\n\n${text}`
          }]
        };
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: `Error: Unable to fetch llms.txt - ${error}`
          }],
          isError: true
        };
      }
    }
  });

  // Tool 2: Get humans.txt (Team & Acknowledgments)
  mcp.registerTool({
    name: 'get_humans_txt',
    description: 'Retrieve humans.txt - people, technology stack, and acknowledgments behind arif-fazil.com',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    async execute() {
      try {
        const response = await fetch('/humans.txt', { cache: 'no-store' });
        const text = await response.text();
        return {
          content: [{
            type: 'text',
            text
          }]
        };
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: `Error: Unable to fetch humans.txt - ${error}`
          }],
          isError: true
        };
      }
    }
  });

  // Tool 3: Get Trinity Architecture Links
  mcp.registerTool({
    name: 'get_trinity_links',
    description: 'Return canonical Trinity architecture links (HUMAN, THEORY, APPS, BACKEND)',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    async execute() {
      const trinity = {
        architecture: 'Trinity (HUMAN ↔ THEORY ↔ APPS)',
        layers: {
          HUMAN: {
            url: 'https://arif-fazil.com',
            symbol: 'Δ',
            function: 'Epistemic - The Body',
            ai_context: 'https://arif-fazil.com/llms.txt'
          },
          THEORY: {
            url: 'https://apex.arif-fazil.com',
            symbol: 'Ψ',
            function: 'Authority - The Soul',
            ai_context: 'https://apex.arif-fazil.com/llms.txt'
          },
          APPS: {
            url: 'https://arifos.arif-fazil.com',
            symbol: 'Ω',
            function: 'Safety - The Mind',
            ai_context: 'https://arifos.arif-fazil.com/llms.txt'
          },
          BACKEND: {
            url: 'https://mcp.arif-fazil.com',
            mcp_endpoint: 'https://mcp.arif-fazil.com/mcp',
            health: 'https://mcp.arif-fazil.com/health',
            function: 'MCP Runtime - Governance Execution'
          }
        },
        motto: 'Ditempa Bukan Diberi (Forged, Not Given)',
        contact: 'arifos@arif-fazil.com'
      };

      return {
        content: [{
          type: 'text',
          text: JSON.stringify(trinity, null, 2)
        }]
      };
    }
  });

  // ============================================================
  // AAA Federation WebMCP Tools (AAA Gateway Layer)
  // Phase 1: Read-only discovery + draft task submission
  // Floor Compliance: F1 (reversible), F2 (factual), F12 (graceful degradation)
  // ============================================================

  // Tool: Get A2A Agent Card
  mcp.registerTool({
    name: 'get_aaa_agent_card',
    description: 'Retrieve the AAA Gateway A2A v1.0.0 agent card — returns capabilities, skills, authentication schemes, and governance posture',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    async execute() {
      try {
        const response = await fetch('/a2a/agent-card.json', { cache: 'no-store' });
        const card = await response.json();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(card, null, 2)
          }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: `Error: Unable to fetch agent card — ${error}` }],
          isError: true
        };
      }
    }
  });

  // Tool: Discover A2A Skills
  mcp.registerTool({
    name: 'discover_a2a_skills',
    description: 'List all available A2A skills on the AAA Gateway — agent-dispatch, agent-handoff, status-query — with descriptions and approval policies',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    async execute() {
      try {
        const response = await fetch('/a2a/agent-card.json', { cache: 'no-store' });
        const card = await response.json();
        const skills = card.skills || [];
        return {
          content: [{
            type: 'text',
            text: skills.map((s: { id: string; name: string; description: string; tags?: string[]; examples?: string[] }) =>
              `## ${s.name}\nID: ${s.id}\n${s.description}\nTags: ${(s.tags || []).join(', ')}\nExamples: ${(s.examples || []).join(' | ')}`
            ).join('\n\n')
          }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: `Error: ${error}` }],
          isError: true
        };
      }
    }
  });

  // Tool: Explain Governance Model
  mcp.registerTool({
    name: 'explain_aaa_governance',
    description: 'Explain the AAA Gateway governance model — 13 constitutional floors, 888_JUDGE verdict system, VAULT999 audit, and A2A protocol boundaries',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    execute() {
      const governance = {
        summary: 'AAA Gateway enforces arifOS constitutional Floors F1-F13 on all A2A task routing. No agent can self-approve consequential actions.',
        constitutional_floors: {
          F1_AMANAH: 'No irreversible action without human acknowledgment',
          F2_TRUTH: 'Factual claims require citation or declaration of UNKNOWN',
          F3_TRIWITNESS: 'human + AI + earth signal corroboration',
          F4_CLARITY: 'Scale, CRS, and provenance must be explicit',
          F5_PEACE: 'Harm potential must be >= 1.0',
          F6_EMPATHY: 'Stakeholder safety >= 0.90',
          F7_HUMILITY: 'Confidence bounded within [0.03, 0.15]',
          F8_GENIUS: 'Quality score >= constitutional threshold',
          F9_ANTIHANTU: 'Zero hallucination — physics or VOID',
          F10_ONTOLOGY: 'AI=tool, Model!=Reality',
          F11_AUDIT: 'Every decision logged with full provenance',
          F12_RESILIENCE: 'Graceful degradation always',
          F13_SOVEREIGN: 'Human holds final veto — supreme'
        },
        verdict_codes: {
          SEAL: 'Approved — safe to execute (888_JUDGE only)',
          HOLD_888: 'Human review required before execution',
          VOID: 'Constitutional violation — rejected',
          SABAR: 'Cooling required — pause and re-ground',
          CLAIM_ONLY: 'Tool claim only — requires ratification'
        },
        vault: 'VAULT999 — append-only constitutional ledger',
        key_invariant: 'Protocol does not grant authority. A2A enables coordination. Permission is separate.'
      };
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(governance, null, 2)
        }]
      };
    }
  });

  // Tool: Submit Draft Task
  mcp.registerTool({
    name: 'submit_draft_task',
    description: 'Prepare an A2A task for submission. Returns a formatted draft packet. DRAFT ONLY — requires human approval via 888_JUDGE before execution.',
    inputSchema: {
      type: 'object',
      properties: {
        skill_id: { type: 'string', description: 'Skill ID: agent-dispatch, agent-handoff, or status-query' },
        message: { type: 'string', description: 'Task description or query text' }
      },
      required: ['skill_id', 'message']
    },
    execute() {
      return {
        content: [{
          type: 'text',
          text: '## DRAFT ONLY — Human Approval Required\n\nThis tool prepares a task packet but does NOT execute it. To submit:\n\n1. Copy the draft packet below\n2. POST to https://aaa.arif-fazil.com/tasks with bearer authentication\n3. Wait for 888_JUDGE verdict\n4. Execution occurs only after SEAL verdict\n\nFor status-query: submit directly — on-demand approval\nFor agent-dispatch and agent-handoff: MUST receive SEAL from 888_JUDGE before routing'
        }]
      };
    }
  });

  // Tool: Check Federation Manifest
  mcp.registerTool({
    name: 'get_federation_manifest',
    description: 'Retrieve the arifOS federation peer manifest — lists registered agents, constitutional floors, and governance root',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    async execute() {
      try {
        const response = await fetch('/.well-known/arifos-federation.json', { cache: 'no-store' });
        const manifest = await response.json();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(manifest, null, 2)
          }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: `Error: Unable to fetch federation manifest — ${error}` }],
          isError: true
        };
      }
    }
  });

  // Tool: Explain A2A Protocol
  mcp.registerTool({
    name: 'explain_a2a_protocol',
    description: 'Explain the A2A (Agent-to-Agent) protocol v1.0.0 — what it is, what it enables, and its boundaries compared to MCP',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    execute() {
      const explanation = {
        protocol: 'A2A v1.0.0 — Agent-to-Agent',
        what_it_is: 'A protocol for agents to communicate, coordinate, and collaborate. NOT a tool-calling protocol (that is MCP).',
        purpose: 'Enables: task delegation, status sharing, bidirectional handoff, streaming responses between agents',
        key_distinction: {
          A2A: 'agent-to-agent collaboration (who talks to whom)',
          MCP: 'agent-to-tool capability (what the agent can do)',
          arifOS: 'governance kernel (what is allowed)'
        },
        a2a_endpoints: {
          POST_tasks: 'Create a task',
          GET_tasks_id: 'Retrieve task by ID',
          GET_tasks_id_stream: 'SSE stream for task progress',
          POST_tasks_id_cancel: 'Cancel a task',
          GET_tasks_id_subscribe: 'SSE subscription for task updates'
        },
        governance_note: 'A2A enables coordination. It does NOT grant authority. Every consequential action still requires 888_JUDGE approval.',
        auth: 'Bearer token or x-a2a-key required for all task endpoints'
      };
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(explanation, null, 2)
        }]
      };
    }
  });

  console.log('[WebMCP] BODY layer tools registered (3 read-only tools)');
  console.log('[WebMCP] AAA Federation tools registered (5 discovery + draft tools)');
}
