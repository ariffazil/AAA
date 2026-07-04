# Layer 5: Knowledge Graph (Graphiti)

Layer 5 provides structural understanding and relationship mapping. It bridges the gap between semantic "vibes" (L3) and relational "facts" (L4).

## Graphiti MCP Surface
The `graphiti` MCP server provides the following core capabilities:
- `get_nodes`: Retrieve specific entity nodes.
- `get_edges`: Retrieve relationships between entities.
- `search_nodes`: Semantic search within the graph.
- `add_node`: Create a new entity in the knowledge base.
- `add_edge`: Define a relationship between existing nodes.

## Relationship to other Layers
- **L3 → L5:** When a vector search in Qdrant returns a high-confidence match, use the entity names to query L5 for context (e.g., "Who else is connected to this project?").
- **L4 → L5:** When storing a durable record in Postgres, extract named entities and ensure they are represented in the graph.

## Graph Integrity
- **Entity Linking:** Always check if a node exists before adding a duplicate.
- **Relational Types:** Use consistent relationship labels (e.g., `WORKS_ON`, `DEPENDS_ON`, `CONTROLS`).
- **Constitutional Nodes:** High-level entities (arifOS, Vault999) must be treated as "Sacred" nodes.

"A fact without context is a point without a line. The graph is the line."
