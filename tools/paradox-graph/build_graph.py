#!/usr/bin/env python3
"""
Paradox Knowledge Graph Builder — 100% Local
Scans all paradox MD files in arifOS, extracts concepts & relationships,
builds NetworkX graph, generates Pyvis interactive HTML.

Usage:
    python3 build_graph.py                    # Structural only (fast)
    python3 build_graph.py --ollama           # With LLM extraction (slower, richer)
    python3 build_graph.py --ollama --deep    # Full deep extraction
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime

import networkx as nx
from pyvis.network import Network

# ============================================================
# CONFIG
# ============================================================

SCAN_DIRS = [
    "/root/arifOS/okf/atlas333/paradox",
    "/root/arifOS/okf/atlas333/apex",
    "/root/arifOS/okf/atlas333/clusters",
    "/root/AAA/governance",
    "/root/AAA/docs",
    "/root/AAA/docs/philosophy",
    "/root/arifOS/GENESIS",
    "/root/arifOS/docs",
    "/root/AAA/memory",
    "/root/A-FORGE/paradox-engine",
]

SKIP_PATTERNS = [
    "__pycache__", "build/", ".pyc", "test_", "node_modules"
]

OUTPUT_DIR = "/root/AAA/tools/paradox-graph/output"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"
EMBED_MODEL = "nomic-embed-text:latest"

# Cluster colors
CLUSTER_COLORS = {
    "memory": "#FF6B6B",
    "mind": "#4ECDC4",
    "judge": "#45B7D1",
    "contour": "#96CEB4",
    "apex": "#FFEAA7",
    "governance": "#DDA0DD",
    "genesis": "#FF8C00",
    "engine": "#98FB98",
    "void": "#FF1493",
    "unknown": "#C0C0C0",
}

# ============================================================
# STEP 1: SCAN FILES
# ============================================================

def scan_paradox_files():
    """Scan all paradox-related MD files across the system."""
    files = []
    for scan_dir in SCAN_DIRS:
        if not os.path.exists(scan_dir):
            continue
        for root, dirs, filenames in os.walk(scan_dir):
            # Skip unwanted dirs
            dirs[:] = [d for d in dirs if not any(skip in d for skip in SKIP_PATTERNS)]
            for fname in filenames:
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(root, fname)
                # Check if paradox-related
                content_preview = ""
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content_preview = f.read(2000)
                except:
                    continue
                
                # Include if filename or content mentions paradox
                is_paradox = (
                    "paradox" in fname.lower() or
                    "paradox" in content_preview.lower() or
                    re.match(r"P\d{2}-", fname) or
                    any(kw in fname.lower() for kw in ["energy-entropy", "truth-uncertainty", "void", "humility", "sovereignty"])
                )
                
                if is_paradox:
                    # Determine cluster
                    cluster = "unknown"
                    if "paradox" in fpath and "/clusters/" in fpath:
                        cluster = os.path.basename(fpath).replace(".md", "")
                    elif "/apex/" in fpath:
                        cluster = "apex"
                    elif "/paradox/" in fpath:
                        cluster = "atlas333"
                    elif "/governance/" in fpath or "/docs/" in fpath:
                        cluster = "governance"
                    elif "/GENESIS/" in fpath:
                        cluster = "genesis"
                    elif "/memory/" in fpath:
                        cluster = "memory"
                    elif "/A-FORGE/" in fpath:
                        cluster = "engine"
                    elif "void" in fname.lower():
                        cluster = "void"
                    
                    # Extract paradox ID if present
                    paradox_id = ""
                    match = re.match(r"(P\d{2})", fname)
                    if match:
                        paradox_id = match.group(1)
                    
                    # Extract concepts from filename
                    concepts = []
                    name_clean = fname.replace(".md", "").replace("-", " ").replace("_", " ")
                    # Remove paradox ID prefix
                    name_clean = re.sub(r"^P\d{2}\s*", "", name_clean)
                    name_clean = re.sub(r"^(OPUS NAMING|PETRONAS|TWELVE|VOID PARADOX|REALITY TRUTH|AGENTIC INSTITUTION|PARADOX OF TIME|MEMORY)", "", name_clean).strip()
                    if " " in name_clean:
                        concepts = [c.strip() for c in name_clean.split(" ") if len(c.strip()) > 2]
                    elif len(name_clean) > 3:
                        concepts = [name_clean]
                    
                    files.append({
                        "path": fpath,
                        "filename": fname,
                        "cluster": cluster,
                        "paradox_id": paradox_id,
                        "concepts": concepts,
                        "content_hash": hashlib.md5(content_preview.encode()).hexdigest()[:8],
                    })
    
    return files

# ============================================================
# STEP 2: EXTRACT RELATIONSHIPS (Structural)
# ============================================================

def extract_structural_relationships(files):
    """Extract relationships from file structure, naming, and content patterns."""
    relationships = []
    
    # Build concept index
    concept_to_file = {}
    for f in files:
        for c in f["concepts"]:
            c_lower = c.lower()
            if c_lower not in concept_to_file:
                concept_to_file[c_lower] = []
            concept_to_file[c_lower].append(f)
    
    # 1. Paradox pairs from filenames (e.g., P01 = Energy vs Entropy)
    for f in files:
        if f["paradox_id"]:
            # Extract opposing concepts from filename
            name = f["filename"].replace(".md", "")
            match = re.match(r"P\d{2}-(.+)", name)
            if match:
                parts = match.group(1).split("-")
                if len(parts) >= 2:
                    concept_a = parts[0].strip()
                    concept_b = parts[-1].strip()
                    relationships.append({
                        "source": concept_a,
                        "target": concept_b,
                        "type": "TENSION",
                        "weight": 0.9,
                        "description": f"Paradox {f['paradox_id']}: {concept_a} vs {concept_b}",
                        "source_file": f["filename"],
                    })
    
    # 2. Cross-file references (content mentions)
    file_contents = {}
    for f in files:
        try:
            with open(f["path"], "r", encoding="utf-8", errors="ignore") as fh:
                file_contents[f["path"]] = fh.read()
        except:
            file_contents[f["path"]] = ""
    
    for f1 in files:
        content1 = file_contents.get(f1["path"], "")
        for f2 in files:
            if f1["path"] >= f2["path"]:
                continue
            content2 = file_contents.get(f2["path"], "")
            
            # Check if files reference each other
            f1_refs_f2 = f2["filename"].replace(".md", "") in content1
            f2_refs_f1 = f1["filename"].replace(".md", "") in content1
            
            if f1_refs_f2 or f2_refs_f1:
                source_name = f1["paradox_id"] or f1["filename"].replace(".md", "")
                target_name = f2["paradox_id"] or f2["filename"].replace(".md", "")
                relationships.append({
                    "source": source_name,
                    "target": target_name,
                    "type": "REFERENCES",
                    "weight": 0.7,
                    "description": f"Cross-reference between {f1['filename']} and {f2['filename']}",
                    "source_file": f1["filename"],
                })
    
    # 3. Cluster membership
    clusters = {}
    for f in files:
        if f["cluster"] not in clusters:
            clusters[f["cluster"]] = []
        clusters[f["cluster"]].append(f)
    
    for cluster_name, cluster_files in clusters.items():
        if len(cluster_files) > 1:
            for i, f1 in enumerate(cluster_files):
                for f2 in cluster_files[i+1:]:
                    name1 = f1["paradox_id"] or f1["filename"].replace(".md", "")
                    name2 = f2["paradox_id"] or f2["filename"].replace(".md", "")
                    relationships.append({
                        "source": name1,
                        "target": name2,
                        "type": "MEMBER_OF_SAME_CLUSTER",
                        "weight": 0.4,
                        "description": f"Both in {cluster_name} cluster",
                        "source_file": f1["filename"],
                    })
    
    # 4. Wire connections (what connects to what)
    WIRE_MAP = {
        "P01": ["P02", "P05", "P10"],  # Energy-Entropy connects to Remember-Forget, Order-Chaos, Conservation-Change
        "P03": ["P32", "P17"],  # Truth-Uncertainty connects to Certainty-Uncertainty, Utility-Truth
        "P04": ["P03", "P18"],  # Evidence-Claim connects to Truth-Uncertainty, Observer-Observed
        "P09": ["P34", "P35"],  # Layer-Collapse connects to Root-Kernel, Positive-Closed
        "P12": ["P13", "P29"],  # Capability-Authority connects to Doubt-Decision, Sovereignty
        "P18": ["P04", "P03"],  # Observer-Observed connects to Evidence-Claim, Truth-Uncertainty
        "P29": ["P30", "P31", "P33"],  # Sovereignty connects to Justice-Mercy, Permanence-Reversibility, Self-Governance
        "P30": ["P33"],  # Justice-Mercy connects to Self-Governance
        "P34": ["P35"],  # Root-Kernel connects to Positive-Closed
    }
    
    for source, targets in WIRE_MAP.items():
        for target in targets:
            relationships.append({
                "source": source,
                "target": target,
                "type": "WIRES_TO",
                "weight": 0.6,
                "description": f"Constitutional wire: {source} → {target}",
                "source_file": "architectural",
            })
    
    return relationships

# ============================================================
# STEP 3: OLLAMA EXTRACTION (Optional, deeper)
# ============================================================

def ollama_extract(file_info, content):
    """Use local Ollama to extract relationships from paradox content."""
    import urllib.request
    
    prompt = f"""Analyze this paradox document and extract:
1. The core tension (two opposing concepts)
2. Key relationships to other concepts
3. The synthesis or resolution if any

Document: {file_info['filename']}
Content (first 1500 chars):
{content[:1500]}

Return ONLY valid JSON:
{{
  "concept_a": "first concept",
  "concept_b": "second opposing concept", 
  "tension_type": "TENSION|COMPLEMENTARY|PARADOXICAL|RESOLVES_TO",
  "related_concepts": ["concept1", "concept2"],
  "synthesis": "brief synthesis if any, or null",
  "confidence": 0.0-1.0
}}"""
    
    try:
        data = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 300}
        }).encode()
        
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            response_text = result.get("response", "")
            # Extract JSON from response
            json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    except Exception as e:
        print(f"  Ollama extraction failed for {file_info['filename']}: {e}")
    
    return None

def ollama_extract_all(files, deep=False):
    """Extract relationships using Ollama for all files."""
    relationships = []
    
    for f in files:
        try:
            with open(f["path"], "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except:
            continue
        
        if len(content) < 50:
            continue
        
        print(f"  Extracting: {f['filename']}...")
        result = ollama_extract(f, content)
        
        if result:
            # Add extracted relationships
            if result.get("concept_a") and result.get("concept_b"):
                relationships.append({
                    "source": result["concept_a"],
                    "target": result["concept_b"],
                    "type": result.get("tension_type", "TENSION"),
                    "weight": result.get("confidence", 0.7),
                    "description": f"LLM-extracted: {result['concept_a']} vs {result['concept_b']}",
                    "source_file": f["filename"],
                })
            
            for related in result.get("related_concepts", []):
                main_concept = result.get("concept_a", f["paradox_id"] or f["filename"].replace(".md", ""))
                relationships.append({
                    "source": main_concept,
                    "target": related,
                    "type": "RELATED_TO",
                    "weight": 0.5,
                    "description": f"LLM-extracted relation from {f['filename']}",
                    "source_file": f["filename"],
                })
    
    return relationships

# ============================================================
# STEP 4: BUILD GRAPH
# ============================================================

def build_graph(files, relationships):
    """Build NetworkX graph from files and relationships."""
    G = nx.Graph()
    
    # Add nodes from files
    for f in files:
        node_id = f["paradox_id"] or f["filename"].replace(".md", "")
        G.add_node(node_id, **{
            "label": node_id,
            "full_name": f["filename"].replace(".md", ""),
            "cluster": f["cluster"],
            "paradox_id": f["paradox_id"],
            "path": f["path"],
            "content_hash": f["content_hash"],
            "concepts": ", ".join(f["concepts"]),
        })
    
    # Add edges from relationships
    for r in relationships:
        src = r["source"]
        tgt = r["target"]
        
        # Normalize node IDs
        if not G.has_node(src):
            G.add_node(src, **{
                "label": src,
                "full_name": src,
                "cluster": "extracted",
                "concepts": src,
            })
        if not G.has_node(tgt):
            G.add_node(tgt, **{
                "label": tgt,
                "full_name": tgt,
                "cluster": "extracted",
                "concepts": tgt,
            })
        
        # Add edge (don't duplicate)
        if not G.has_edge(src, tgt):
            G.add_edge(src, tgt, **{
                "type": r["type"],
                "weight": r["weight"],
                "description": r["description"],
                "source_file": r.get("source_file", ""),
            })
        else:
            # Strengthen existing edge
            edge_data = G[src][tgt]
            edge_data["weight"] = min(1.0, edge_data["weight"] + 0.1)
            edge_data["description"] += f" | {r['description']}"
    
    return G

# ============================================================
# STEP 5: VISUALIZE
# ============================================================

def visualize(G, output_path):
    """Generate interactive Pyvis HTML graph."""
    net = Network(
        height="900px",
        width="100%",
        bgcolor="#1a1a2e",
        font_color="white",
        directed=False,
        notebook=False,
        cdn_resources="remote",
    )
    
    # Physics settings for better layout
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.02,
          "damping": 0.4
        },
        "solver": "forceAtlas2Based",
        "stabilization": {"iterations": 200}
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      }
    }
    """)
    
    # Add nodes
    for node, data in G.nodes(data=True):
        cluster = data.get("cluster", "unknown")
        color = CLUSTER_COLORS.get(cluster, "#C0C0C0")
        
        # Size based on degree
        degree = G.degree(node)
        size = max(15, min(50, 10 + degree * 5))
        
        # Title (hover info)
        title = f"<b>{data.get('full_name', node)}</b><br>"
        title += f"Cluster: {cluster}<br>"
        title += f"Connections: {degree}<br>"
        if data.get("concepts"):
            title += f"Concepts: {data['concepts']}<br>"
        if data.get("path"):
            title += f"<br><i>{data['path']}</i>"
        
        net.add_node(
            node,
            label=data.get("label", node),
            color=color,
            size=size,
            title=title,
            font={"size": max(10, min(16, 8 + degree * 2))},
        )
    
    # Add edges
    for src, tgt, data in G.edges(data=True):
        weight = data.get("weight", 0.5)
        edge_type = data.get("type", "")
        
        # Color by type
        edge_color = "#666666"
        if edge_type == "TENSION":
            edge_color = "#FF4444"
        elif edge_type == "WIRES_TO":
            edge_color = "#44AAFF"
        elif edge_type == "REFERENCES":
            edge_color = "#44FF44"
        elif edge_type == "MEMBER_OF_SAME_CLUSTER":
            edge_color = "#888888"
        elif edge_type in ("RESOLVES_TO", "COMPLEMENTARY"):
            edge_color = "#FFD700"
        
        net.add_edge(
            src, tgt,
            width=max(1, weight * 4),
            color=edge_color,
            title=f"{edge_type}: {data.get('description', '')}",
            dashes=(edge_type == "REFERENCES"),
        )
    
    # Save
    net.save_graph(output_path)
    print(f"\nGraph saved to: {output_path}")
    return output_path

# ============================================================
# STEP 6: EXPORT JSON
# ============================================================

def export_json(G, files, relationships, output_path):
    """Export graph as JSON for paradox-engine registry."""
    data = {
        "generated": datetime.now().isoformat(),
        "stats": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "files_scanned": len(files),
            "relationships_found": len(relationships),
        },
        "nodes": [],
        "edges": [],
        "clusters": {},
    }
    
    for node, attrs in G.nodes(data=True):
        data["nodes"].append({
            "id": node,
            **attrs,
            "degree": G.degree(node),
            "centrality": nx.degree_centrality(G).get(node, 0),
        })
    
    for src, tgt, attrs in G.edges(data=True):
        data["edges"].append({
            "source": src,
            "target": tgt,
            **attrs,
        })
    
    # Cluster summary
    for node, attrs in G.nodes(data=True):
        cluster = attrs.get("cluster", "unknown")
        if cluster not in data["clusters"]:
            data["clusters"][cluster] = []
        data["clusters"][cluster].append(node)
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"JSON exported to: {output_path}")
    return output_path

# ============================================================
# MAIN
# ============================================================

def main():
    import sys
    use_ollama = "--ollama" in sys.argv
    deep = "--deep" in sys.argv
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("PARADOX KNOWLEDGE GRAPH BUILDER")
    print("=" * 60)
    
    # Step 1: Scan
    print("\n[1/6] Scanning paradox files...")
    files = scan_paradox_files()
    print(f"  Found {len(files)} paradox-related files")
    for f in files:
        print(f"    {f['cluster']:12s} | {f['paradox_id']:4s} | {f['filename']}")
    
    # Step 2: Structural relationships
    print("\n[2/6] Extracting structural relationships...")
    relationships = extract_structural_relationships(files)
    print(f"  Found {len(relationships)} structural relationships")
    
    # Step 3: Ollama (optional)
    if use_ollama:
        print(f"\n[3/6] Extracting with Ollama ({OLLAMA_MODEL})...")
        ollama_rels = ollama_extract_all(files, deep)
        relationships.extend(ollama_rels)
        print(f"  Added {len(ollama_rels)} LLM-extracted relationships")
    else:
        print("\n[3/6] Skipping Ollama (use --ollama to enable)")
    
    # Step 4: Build graph
    print("\n[4/6] Building NetworkX graph...")
    G = build_graph(files, relationships)
    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")
    
    # Compute centrality
    centrality = nx.degree_centrality(G)
    top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n  Top 10 central nodes:")
    for node, score in top_central:
        print(f"    {node:30s} centrality={score:.3f} degree={G.degree(node)}")
    
    # Step 5: Visualize
    print("\n[5/6] Generating Pyvis visualization...")
    html_path = os.path.join(OUTPUT_DIR, "paradox_knowledge_graph.html")
    visualize(G, html_path)
    
    # Step 6: Export JSON
    print("\n[6/6] Exporting JSON...")
    json_path = os.path.join(OUTPUT_DIR, "paradox_graph.json")
    export_json(G, files, relationships, json_path)
    
    print("\n" + "=" * 60)
    print("DONE")
    print(f"  HTML: {html_path}")
    print(f"  JSON: {json_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
