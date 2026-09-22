---
name: graphiti-temporal-memory-ops
description: "Use when running or debugging Graphiti/FalkorDB temporal memory. Covers the wrong-graph trap."
version: 1.0.0
owner: AAA
category: forge
tags: [graphiti, falkordb, memory, temporal, graph, mcp]
floor_scope: [F2, F4, F9]
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Graphiti Temporal Memory — Operations

## Where the data actually lives (the trap that cost a session)

**The FalkorDB driver names the graph after the `group_id`, NOT after
`FALKORDB_DATABASE`.** Verified 2026-09-16: with `FALKORDB_DATABASE=graphiti_temporal`
and `GRAPHITI_GROUP_ID=arifos`, every node landed in the graph **`arifos`**.

Consequence: a health check that queries `FALKORDB_DATABASE` returns **0 nodes on a
perfectly healthy system**. I declared Graphiti "FAILED — no nodes after 604s" while both
test episodes had in fact persisted correctly. The system logged
`Completed add_episode` / `Successfully processed episode` and I disbelieved it because I
read the wrong store.

**Rule:** never assert on a store location you have not confirmed by *finding a record you
just wrote*. Before any count-based health check, confirm the write target:

```bash
# list graphs, then find YOUR episode by name across all of them
docker exec falkordb redis-cli -p 6379 GRAPH.LIST
docker exec falkordb redis-cli -p 6379 GRAPH.QUERY <graph> \
  "MATCH (n) WHERE n.name CONTAINS '<your-episode-name>' RETURN labels(n), n.name"
```

A count can rise from another writer; **an Episodic node bearing your episode name is
proof**. Assert on that, not on a number.

## Graphiti + FalkorDB on this machine

```
container : graphiti-mcp        (image zepai/knowledge-graph-mcp:latest, --network host)
transport : streamable HTTP     127.0.0.1:18412/mcp/
graph     : the GROUP_ID  (default container ships group_id=main!)
shared DB : falkordb :6380 — 14 graphs, federation infrastructure, NOT Graphiti's private store
tools     : add_memory · search_nodes · search_memory_facts · get_episodes ·
            add_triplet · get_episode_entities · build_communities · clear_graph · get_status
```

**`add_memory` is asynchronous** — it returns `"queued for processing"`. Poll
`get_status`, or read the graph directly; do not treat "queued" as "done".

**Run the image with `--entrypoint ""`.** The bundled `/start-services.sh` hardcodes
`redis-server --port 6379 --daemonize yes`, which collides with any existing Redis on 6379
and silently creates a *second* database the MCP server then talks to. Launch the MCP
process directly and point `FALKORDB_URI` at the existing instance.

**FalkorDB is shared.** On this host it holds `arifos_federation`, `af_forge`, `mesh`,
`skill_mesh`, `knowledge`, `sado_knowledge`, `arifOS`, `atlas333_graph`… Never migrate or
drop it as if it belonged to one consumer. Give Graphiti its own **group_id** and treat
that graph as its namespace.

## Provider configuration

The container speaks the OpenAI protocol, so a local Ollama works with no proxy:

```yaml
llm:      { provider: openai, model: ${MODEL_NAME:qwen2.5:7b},
            providers: { openai: { api_url: ${OPENAI_API_URL:http://127.0.0.1:11434/v1} } } }
embedder: { provider: openai, model: ${EMBEDDER_MODEL:bge-m3:latest}, dimensions: 1024 }
```

- **Set `dimensions` to match the embedder.** `bge-m3` is **1024**, not the shipped
  default 1536. A mismatch fails at index time, not at boot — so it survives startup
  checks and breaks later.
- `OPENAI_API_URL` must be reachable **from the container**, not from your shell. With
  `--network host` that is `127.0.0.1`; otherwise it is the docker bridge address.
- Containers ignore the host's `ENVIRONMENT` — pass everything via `-e`.

## Realistic throughput (set expectations before promising anything)

Measured 2026-09-16, 4 vCPU CPU-only, `NUM_PARALLEL=1`:

| operation | measured |
|---|---|
| embedding (bge-m3) | ~4 s |
| extraction call (qwen2.5:7b, ~120 tok out) | **1m30s – 3m06s** |
| **one episode end-to-end (~17 sequential calls)** | **13.9 min** |

Entity extraction is **many sequential LLM calls per episode** — it is not one prompt.
On CPU-only hardware this is minutes-to-tens-of-minutes per episode. Decide up front
whether that is acceptable; if not, host only extraction/dedup elsewhere and keep
embeddings + graph local.

**Dedup degrades with small models.** A 7B produced `audit-probe-p1-04`,
`audit_probe_p1_04` and `audit_proprobe-p1-04` as three separate entities, with
`LLM returned invalid duplicate_facts idx values` warnings. Dedup is a
reasoning-heavy step; budget a stronger model for it than for plain extraction.

## Pitfalls

- **Never restart the inference provider while a consumer has an in-flight request.**
  Restarting Ollama mid-episode produced a `500 after 2m57s` that I first misread as a
  capacity failure — the log line that solved it was `systemd: Stopping ollama.service` at
  the exact timestamp of the error. Sequence: quiesce consumer → change provider → verify.
- **Check your own recent mutations first** when diagnosing an error timestamp.
- **`KEEP_ALIVE` matters.** Cold-load on CPU is ~45 s; with a short keep-alive every
  consumer pays it repeatedly. Use 30m for a dedicated inference node.
- Whisper-style hallucination risk does not apply here, but the same discipline does:
  if the output looks wrong, verify the *plumbing* before blaming the model.

## Relationship to other skills

| This skill | Other skills |
|---|---|
| Graphiti/FalkorDB operations | `arifos-memory-architecture` — how memory flows in the federation |
| Provider-side tuning | `local-memory-retrieval`, `fed-model-chain-editing` |
| Test discipline | `claim-level-verification`, `live-probe-audit-pattern` |
