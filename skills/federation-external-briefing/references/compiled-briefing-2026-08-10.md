# External Architecture Reference — Compiled 2026-08-10

## Copy-Paste Prompt Block (primary deliverable)

```
Read these URLs to understand the arifOS federation architecture:

SITE OVERVIEW (START HERE):
https://arif-fazil.com/llms.txt

AGENT DISCOVERY:
https://arif-fazil.com/.well-known/agent.json
https://arif-fazil.com/.well-known/identity.json
https://arif-fazil.com/.well-known/capability.json
https://arif-fazil.com/.well-known/did.json
https://arif-fazil.com/.well-known/webmcp.json
https://arif-fazil.com/.well-known/arifos-federation.json

CONSTITUTIONAL FLOORS:
https://arif-fazil.com/floors.json
https://arif-fazil.com/policy.json

FEDERATION GRAPH:
https://arif-fazil.com/graph.json
https://arif-fazil.com/knowledge/corpus.json
https://arif-fazil.com/llms.json

SOVEREIGN CLAIMS (Gödel Lock, ZKPC):
https://arif-fazil.com/000/claims.json

PUBLIC DOCTRINE:
https://arif-fazil.com/words/doctrine
https://arif-fazil.com/doctrine/apex-theory
https://arif-fazil.com/000
https://arif-fazil.com/999

GITHUB (all public):
https://github.com/ariffazil/arifOS
https://github.com/ariffazil/A-FORGE
https://github.com/ariffazil/AAA
https://github.com/ariffazil/GEOX
https://github.com/ariffazil/WEALTH
https://github.com/ariffazil/WELL
https://github.com/ariffazil/HERMES
https://github.com/ariffazil/arifFLOW

MCP:
https://mcp.arif-fazil.com/mcp

After reading, explain:
1. What arifOS is
2. 6-organ federation + ports + ceilings
3. 13 constitutional floors
4. 8 canonical MCP tools
5. APEX Theory (3 layers)
6. EUREKA 6-plane architecture
7. EMD reflex arc
8. Authority chain
```

## Reality Context (what was live at compile time)

| Endpoint | HTTP | Notes |
|----------|------|-------|
| arif-fazil.com/llms.txt | 200 | Machine-readable site overview |
| .well-known/agent.json | 200 | Identity + capabilities + constitutional floors |
| .well-known/identity.json | 200 | W3C identity (did:web:arif-fazil.com) |
| .well-known/capability.json | 200 | MCP gateway, A2A gateway, observation modes |
| .well-known/did.json | 200 | W3C DID document |
| .well-known/arifos-federation.json | 200 | Federation manifest (6 organs) |
| .well-known/webmcp.json | 200 | WebMCP tool surface (verify_did, get_floors, get_missions, etc.) |
| arif-fazil.com/floors.json | 200 | F1-F13 machine-readable |
| arif-fazil.com/policy.json | 200 | Public action policy |
| arif-fazil.com/graph.json | 200 | Knowledge graph (organ nodes + edges) |
| arif-fazil.com/knowledge/corpus.json | 200 | Knowledge sources index |
| arif-fazil.com/llms.json | 200 | Structured route map |
| arif-fazil.com/000/claims.json | 200 | Sovereign claims (Gödel Lock, ZKPC) |
| arif-fazil.com/words/doctrine | 200 | 13 Floors visual canon |
| arif-fazil.com/doctrine/apex-theory | 200 | APEX Theory architecture |
| arif-fazil.com/000 | 200 | Genesis + sovereign identity |
| arif-fazil.com/999 | 200 | Proof + verification |
| mcp.arif-fazil.com/mcp | 200 | MCP gateway (streamable HTTP) |
| arifos.arif-fazil.com/health | 200 | Kernel health |
| geox.arif-fazil.com/health | 200 | Earth health |
| wealth.arif-fazil.com/health | 200 | Capital health |
| well.arif-fazil.com/health | 200 | Vitality health |
| github.com/ariffazil/arifOS | 200 | Constitutional kernel |
| github.com/ariffazil/A-FORGE | 200 | Execution shell |
| github.com/ariffazil/AAA | 200 | Control plane |
| github.com/ariffazil/GEOX | 200 | Earth intelligence |
| github.com/ariffazil/WEALTH | 200 | Capital intelligence |
| github.com/ariffazil/WELL | 200 | Human readiness |
| github.com/ariffazil/HERMES | 200 | Telegram bridge |
| github.com/ariffazil/arifFLOW | 200 | Receipt metabolism |

## Key Design Decisions

1. **llms.txt as entry point** — This is the single file any AI can read first. It contains site overview, organ topology, constitutional floors, and MakcikGPT links.
2. **.well-known endpoints** — Standard agent discovery. Any AI with WebMCP or well-known support can auto-discover.
3. **floors.json** — Machine-readable F1-F13. Better than scraping the doctrine HTML page.
4. **graph.json** — Knowledge graph with organ nodes and edges. Shows the topology at a glance.
5. **000/claims.json** — Sovereign claims. Gödel Lock, ZKPC, membrane principle. Unique to this system.
6. **GitHub repos** — All 8 production repos are public. READMEs contain substantial architecture docs.
