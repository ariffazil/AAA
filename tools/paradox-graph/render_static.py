#!/usr/bin/env python3
"""Generate static image of the Paradox Knowledge Graph."""

import json
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Load graph data
with open("/root/AAA/tools/paradox-graph/output/paradox_graph_v2.json") as f:
    data = json.load(f)

# Build graph
G = nx.Graph()

for node in data["nodes"]:
    G.add_node(node["id"], **{k: v for k, v in node.items() if k != "id"})

for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"], **{k: v for k, v in edge.items() if k not in ("source", "target")})

# Colors by cluster
COLORS = {
    "atlas333": "#FF6B6B",
    "apex": "#FFD93D",
    "governance": "#DDA0DD",
    "genesis": "#FF8C00",
    "memory": "#4ECDC4",
    "engine": "#98FB98",
    "void": "#FF1493",
    "extracted": "#888888",
}

node_colors = []
node_sizes = []
for node in G.nodes():
    cluster = G.nodes[node].get("cluster", "unknown")
    node_colors.append(COLORS.get(cluster, "#666666"))
    degree = G.degree(node)
    node_sizes.append(max(80, min(600, 50 + degree * 30)))

# Edge colors
edge_colors = []
edge_widths = []
for src, tgt, d in G.edges(data=True):
    etype = d.get("type", "")
    if etype == "TENSION":
        edge_colors.append("#ef4444")
        edge_widths.append(1.5)
    elif etype == "WIRES_TO":
        edge_colors.append("#3b82f6")
        edge_widths.append(1.0)
    elif etype == "MEMBER_OF":
        edge_colors.append("#4b5563")
        edge_widths.append(0.5)
    elif etype == "EXTENDS":
        edge_colors.append("#f59e0b")
        edge_widths.append(1.0)
    elif etype == "REFERENCES":
        edge_colors.append("#22c55e")
        edge_widths.append(0.8)
    else:
        edge_colors.append("#6b7280")
        edge_widths.append(0.5)

# Layout
plt.figure(figsize=(24, 18), facecolor="#0d1117")
ax = plt.gca()
ax.set_facecolor("#0d1117")

# Use spring layout with adjustments
pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.4, ax=ax)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, edgecolors="white", linewidths=0.5, ax=ax)

# Labels - only for important nodes
labels = {}
for node in G.nodes():
    degree = G.degree(node)
    if degree >= 3 or G.nodes[node].get("cluster") in ("atlas333", "apex", "void"):
        labels[node] = node

nx.draw_networkx_labels(G, pos, labels, font_size=7, font_color="#c9d1d9", font_weight="bold", ax=ax)

# Title
ax.set_title("ATLAS333 Paradox Knowledge Graph — 40 Paradoxes × 5 Clusters\nForged by F13 SOVEREIGN · 2026-08-16", 
             fontsize=16, color="white", fontweight="bold", pad=20)

# Legend
legend_elements = [
    mpatches.Patch(facecolor="#FF6B6B", label="ATLAS333 (P01-P40)"),
    mpatches.Patch(facecolor="#FFD93D", label="APEX Dials"),
    mpatches.Patch(facecolor="#DDA0DD", label="Governance"),
    mpatches.Patch(facecolor="#FF8C00", label="Genesis"),
    mpatches.Patch(facecolor="#4ECDC4", label="Memory"),
    mpatches.Patch(facecolor="#98FB98", label="Engine"),
    mpatches.Patch(facecolor="#FF1493", label="Void Paradox"),
]
legend = ax.legend(handles=legend_elements, loc="upper left", fontsize=10, 
                   facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")

# Stats text
stats = f"Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()} | Clusters: 5 | Paradoxes: 40"
ax.text(0.5, 0.02, stats, transform=ax.transAxes, fontsize=10, color="#8b949e",
        ha="center", va="bottom")

plt.tight_layout()
output_path = "/root/AAA/tools/paradox-graph/output/paradox_graph.png"
plt.savefig(output_path, dpi=150, facecolor="#0d1117", bbox_inches="tight")
plt.close()

print(f"Saved: {output_path}")
