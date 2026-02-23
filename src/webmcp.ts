/**
 * WebMCP Tools for arif-fazil.com (BODY Layer)
 * 
 * Phase 1: Read-only governance tools
 * Purpose: Make human context machine-legible and verifiable
 * Floor Compliance: F1 (Amanah - reversible), F2 (Truth - factual), F9 (Anti-Hantu - no agency claims)
 */

import '@mcp-b/global';

// Wait for polyfill to be ready
if (typeof navigator !== 'undefined' && 'modelContext' in navigator) {
  const mcp = (navigator as any).modelContext;

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
            url: 'https://arifosmcp.arif-fazil.com',
            mcp_endpoint: 'https://arifosmcp.arif-fazil.com/mcp',
            health: 'https://arifosmcp.arif-fazil.com/health',
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

  console.log('[WebMCP] BODY layer tools registered (3 read-only tools)');
}
