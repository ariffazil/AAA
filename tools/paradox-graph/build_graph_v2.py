#!/usr/bin/env python3
"""
Paradox Knowledge Graph Builder v2 — Refined & Focused
Only core paradox files. With optional Ollama extraction.
"""

import os, re, json, hashlib, sys
from pathlib import Path
from datetime import datetime
import networkx as nx
from pyvis.network import Network

OUTPUT_DIR = "/root/AAA/tools/paradox-graph/output"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

CLUSTER_COLORS = {
    "atlas333": "#FF6B6B",
    "apex": "#FFD93D",
    "governance": "#DDA0DD",
    "genesis": "#FF8C00",
    "memory": "#4ECDC4",
    "engine": "#98FB98",
    "void": "#FF1493",
}

# ============================================================
# CORE PARADOX FILES ONLY
# ============================================================

def scan_core():
    """Scan only core paradox files — ATLAS333 P01-P35, apex dials, and named paradox docs."""
    files = []
    
    # 1. ATLAS333 P01-P35
    atlas_dir = "/root/arifOS/okf/atlas333/paradox"
    if os.path.exists(atlas_dir):
        for fname in sorted(os.listdir(atlas_dir)):
            if fname.endswith(".md") and re.match(r"P\d{2}-", fname):
                fpath = os.path.join(atlas_dir, fname)
                pid = re.match(r"(P\d{2})", fname).group(1)
                name = fname.replace(".md", "")
                parts = name.replace(f"{pid}-", "").split("-")
                
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                # Extract title from first heading
                title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                title = title_match.group(1) if title_match else name
                
                # Extract concepts from content (look for key terms)
                concepts = set(parts)
                # Find bold terms that look like concepts
                for m in re.finditer(r"\*\*(.+?)\*\*", content[:3000]):
                    term = m.group(1).strip()
                    if len(term) < 40 and not term.startswith("P"):
                        concepts.add(term.lower())
                
                files.append({
                    "id": pid,
                    "name": name,
                    "title": title,
                    "path": fpath,
                    "cluster": "atlas333",
                    "concepts": list(concepts)[:8],
                    "tension": f"{parts[0]} vs {parts[-1]}" if len(parts) >= 2 else "",
                    "content_len": len(content),
                })
    
    # 2. Apex dials
    apex_dir = "/root/arifOS/okf/atlas333/apex"
    if os.path.exists(apex_dir):
        for fname in os.listdir(apex_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(apex_dir, fname)
                dial_name = fname.replace(".md", "")
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                title = title_match.group(1) if title_match else dial_name
                files.append({
                    "id": f"APEX_{dial_name.upper().replace('-','_')}",
                    "name": dial_name,
                    "title": title,
                    "path": fpath,
                    "cluster": "apex",
                    "concepts": [dial_name],
                    "tension": "",
                    "content_len": len(content),
                })
    
    # 3. Specific paradox governance docs
    paradox_docs = [
        "/root/AAA/governance/VOID_PARADOX_DOCTRINE.md",
        "/root/AAA/governance/AGENTIC_INSTITUTION_PARADOXES.md",
        "/root/AAA/docs/PARADOX_SUBSTRATE_MAP.md",
        "/root/AAA/docs/REALITY-TRUTH-PARADOXES.md",
        "/root/AAA/docs/philosophy/PARADOX_OF_TIME_AND_TRUTH.md",
        "/root/arifOS/GENESIS/004_OPUS_NAMING_PARADOX.md",
        "/root/arifOS/GENESIS/006_PETRONAS_PARADOX.md",
        "/root/arifOS/docs/canon/paradox_anchors.md",
    ]
    for fpath in paradox_docs:
        if os.path.exists(fpath):
            fname = os.path.basename(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
            title = title_match.group(1) if title_match else fname.replace(".md", "")
            
            # Determine cluster
            cluster = "governance"
            if "GENESIS" in fpath:
                cluster = "genesis"
            elif "VOID" in fpath:
                cluster = "void"
            
            doc_id = fname.replace(".md", "").replace("_", " ").replace("-", " ")[:30]
            files.append({
                "id": doc_id,
                "name": fname.replace(".md", ""),
                "title": title,
                "path": fpath,
                "cluster": cluster,
                "concepts": [w.lower() for w in re.findall(r"[A-Z]{2,}", fname) if len(w) > 2],
                "tension": "",
                "content_len": len(content),
            })
    
    # 4. Cluster summary files
    for cluster_name in ["memory", "mind", "judge", "contour"]:
        cpath = f"/root/arifOS/okf/atlas333/clusters/{cluster_name}.md"
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            files.append({
                "id": f"CLUSTER_{cluster_name.upper()}",
                "name": f"{cluster_name} cluster",
                "title": f"ATLAS333 {cluster_name.title()} Cluster",
                "path": cpath,
                "cluster": cluster_name if cluster_name in CLUSTER_COLORS else "atlas333",
                "concepts": [cluster_name],
                "tension": "",
                "content_len": len(content),
            })
    
    # 5. A-FORGE paradox engine
    engine_path = "/root/A-FORGE/paradox-engine/engine.py"
    if os.path.exists(engine_path):
        files.append({
            "id": "ENGINE_paradox",
            "name": "paradox-engine",
            "title": "A-FORGE Paradox Engine",
            "path": engine_path,
            "cluster": "engine",
            "concepts": ["paradox", "engine", "resolution"],
            "tension": "",
            "content_len": os.path.getsize(engine_path),
        })
    
    return files

# ============================================================
# EXTRACT RELATIONSHIPS
# ============================================================

def extract_relationships(files):
    """Extract relationships from structural analysis."""
    rels = []
    file_by_id = {f["id"]: f for f in files}
    
    # 1. TENSION pairs from ATLAS333 paradoxes
    for f in files:
        if f["cluster"] == "atlas333" and f["tension"]:
            parts = f["tension"].split(" vs ")
            if len(parts) == 2:
                rels.append({
                    "source": parts[0].strip(),
                    "target": parts[1].strip(),
                    "type": "TENSION",
                    "weight": 0.9,
                    "label": f"{f['id']}: {f['tension']}",
                })
    
    # 2. Architectural wires (known from arifOS design)
    WIRES = [
        ("P01-energy", "P02-remember", "WIRES_TO"),
        ("P01-energy", "P05-order", "WIRES_TO"),
        ("P01-energy", "P10-conservation", "WIRES_TO"),
        ("P03-truth", "P32-certainty", "WIRES_TO"),
        ("P03-truth", "P17-utility", "WIRES_TO"),
        ("P03-truth", "P04-evidence", "WIRES_TO"),
        ("P04-evidence", "P18-observer", "WIRES_TO"),
        ("P09-layer", "P34-root", "WIRES_TO"),
        ("P09-layer", "P35-positive", "WIRES_TO"),
        ("P12-capability", "P13-doubt", "WIRES_TO"),
        ("P12-capability", "P29-sovereignty", "WIRES_TO"),
        ("P29-sovereignty", "P30-justice", "WIRES_TO"),
        ("P29-sovereignty", "P31-permanence", "WIRES_TO"),
        ("P29-sovereignty", "P33-self", "WIRES_TO"),
        ("P30-justice", "P33-self", "WIRES_TO"),
        ("P34-root", "P35-positive", "WIRES_TO"),
        ("P14-reason", "P13-doubt", "WIRES_TO"),
        ("P22-unity", "P11-individual", "WIRES_TO"),
        ("P21-measurable", "P01-energy", "WIRES_TO"),
    ]
    
    # Map short names to file IDs
    id_map = {}
    for f in files:
        if f["cluster"] == "atlas333":
            # Map various forms of the name
            base = f["name"].lower()
            id_map[base] = f["id"]
            # Also map with just the concept part
            match = re.match(r"P\d{2}-(.+)", base)
            if match:
                id_map[match.group(1)] = f["id"]
    
    for src, tgt, rel_type in WIRES:
        # Find matching file IDs
        src_id = None
        tgt_id = None
        for key, fid in id_map.items():
            if src.split("-")[0] in key or key.startswith(src.split("-")[0]):
                src_id = fid
            if tgt.split("-")[0] in key or key.startswith(tgt.split("-")[0]):
                tgt_id = fid
        
        if src_id and tgt_id:
            rels.append({
                "source": src_id,
                "target": tgt_id,
                "type": rel_type,
                "weight": 0.7,
                "label": f"Architectural wire",
            })
    
    # 3. Cluster membership (limited — no full clique)
    clusters = {}
    for f in files:
        c = f["cluster"]
        if c not in clusters:
            clusters[c] = []
        clusters[c].append(f["id"])
    
    for cname, cfiles in clusters.items():
        if len(cfiles) <= 1:
            continue
        # Connect each to the cluster center (first file) instead of full clique
        center = cfiles[0]
        for cfid in cfiles[1:]:
            rels.append({
                "source": center,
                "target": cfid,
                "type": "MEMBER_OF",
                "weight": 0.3,
                "label": f"{cname} cluster",
            })
    
    # 4. Cross-cluster bridges
    BRIDGES = [
        ("VOID_PARADOX_DOCTRINE", "P03-truth-uncertainty", "EXTENDS"),
        ("VOID_PARADOX_DOCTRINE", "P18-observer-observed", "EXTENDS"),
        ("VOID_PARADOX_DOCTRINE", "P19-story-structure", "EXTENDS"),
        ("REALITY-TRUTH-PARADOXES", "P03-truth-uncertainty", "REFERENCES"),
        ("PARADOX_SUBSTRATE_MAP", "P09-layer-collapse", "REFERENCES"),
        ("AGENTIC_INSTITUTION_PARADOXES", "P33-self-governance", "REFERENCES"),
        ("P01-energy-entropy", "APEX_H_HUMILITY", "INFORMED_BY"),
        ("P12-capability-authority", "APEX_G_CAPABILITY", "INFORMED_BY"),
        ("P33-self-governance", "APEX_PHI_FALSIFICATION", "INFORMED_BY"),
        ("P30-justice-mercy", "APEX_W3_TRI_WITNESS", "INFORMED_BY"),
        ("engine.py", "P23-judge-cluster", "IMPLEMENTS"),
    ]
    
    for src, tgt, rel_type in BRIDGES:
        if src in file_by_id or src in [f["name"] for f in files]:
            if tgt in file_by_id or tgt in [f["name"] for f in files]:
                rels.append({
                    "source": src,
                    "target": tgt,
                    "type": rel_type,
                    "weight": 0.5,
                    "label": f"Cross-cluster bridge",
                })
    
    return rels

# ============================================================
# OLLAMA EXTRACTION
# ============================================================

def ollama_extract(file_info):
    """Extract relationships from a single file using Ollama."""
    import urllib.request
    
    try:
        with open(file_info["path"], "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()[:2000]
    except:
        return None
    
    prompt = f"""Analyze this paradox document. Return ONLY valid JSON, no other text.

Document: {file_info['name']}
Content: {content[:1500]}

Return:
{{"tension_pair": ["concept_a", "concept_b"], "resolves_to": "concept or null", "related": ["c1", "c2", "c3"], "synthesis": "one sentence"}}"""
    
    try:
        data = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 200}
        }).encode()
        
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            text = result.get("response", "")
            json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    except Exception as e:
        print(f"  Ollama failed for {file_info['name']}: {e}")
    return None

def ollama_extract_all(files):
    """Extract with Ollama for all files."""
    rels = []
    for f in files:
        if f["content_len"] < 100:
            continue
        print(f"  Ollama: {f['name']}...")
        result = ollama_extract(f)
        if result:
            tp = result.get("tension_pair", [])
            if len(tp) == 2:
                rels.append({
                    "source": tp[0],
                    "target": tp[1],
                    "type": "LLM_TENSION",
                    "weight": 0.8,
                    "label": f"LLM-extracted from {f['name']}",
                })
            for r in result.get("related", []):
                rels.append({
                    "source": f["name"],
                    "target": r,
                    "type": "LLM_RELATED",
                    "weight": 0.5,
                    "label": f"LLM-extracted relation",
                })
            if result.get("resolves_to"):
                rels.append({
                    "source": f["name"],
                    "target": result["resolves_to"],
                    "type": "RESOLVES_TO",
                    "weight": 0.6,
                    "label": f"LLM-extracted resolution",
                })
    return rels

# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph(files, rels):
    G = nx.Graph()
    
    for f in files:
        G.add_node(f["id"], **{
            "label": f["id"],
            "full_name": f["name"],
            "title_text": f["title"],
            "cluster": f["cluster"],
            "concepts": ", ".join(f.get("concepts", [])[:5]),
            "tension": f.get("tension", ""),
        })
    
    for r in rels:
        src, tgt = r["source"], r["target"]
        if not G.has_node(src):
            G.add_node(src, label=src, full_name=src, cluster="extracted")
        if not G.has_node(tgt):
            G.add_node(tgt, label=tgt, full_name=tgt, cluster="extracted")
        
        if not G.has_edge(src, tgt):
            G.add_edge(src, tgt, **{
                "type": r["type"],
                "weight": r["weight"],
                "label": r.get("label", ""),
            })
        else:
            G[src][tgt]["weight"] = min(1.0, G[src][tgt]["weight"] + 0.1)
    
    return G

# ============================================================
# VISUALIZE
# ============================================================

def visualize(G, output_path):
    net = Network(height="900px", width="100%", bgcolor="#0d1117", font_color="#c9d1d9", notebook=False, cdn_resources="remote")
    
    net.set_options("""{
      "physics": {
        "forceAtlas2Based": {"gravitationalConstant": -80, "centralGravity": 0.008, "springLength": 180, "springConstant": 0.015, "damping": 0.5},
        "solver": "forceAtlas2Based",
        "stabilization": {"iterations": 250}
      },
      "interaction": {"hover": true, "navigationButtons": true, "keyboard": true}
    }""")
    
    centrality = nx.degree_centrality(G)
    
    for node, data in G.nodes(data=True):
        cluster = data.get("cluster", "unknown")
        color = CLUSTER_COLORS.get(cluster, "#666666")
        degree = G.degree(node)
        cent = centrality.get(node, 0)
        size = max(12, min(45, 8 + degree * 4 + cent * 20))
        
        title = f"<b>{data.get('full_name', node)}</b><br>"
        title += f"Cluster: {cluster}<br>"
        title += f"Connections: {degree}<br>"
        title += f"Centrality: {cent:.3f}<br>"
        if data.get("tension"):
            title += f"Tension: {data['tension']}<br>"
        if data.get("concepts"):
            title += f"Concepts: {data['concepts']}<br>"
        
        border_color = "#ffffff" if cent > 0.3 else color
        
        net.add_node(node, label=data.get("label", node), color={"background": color, "border": border_color}, size=size, title=title, font={"size": max(9, min(14, 7 + degree))}, borderWidth=2)
    
    EDGE_COLORS = {
        "TENSION": "#ef4444",
        "WIRES_TO": "#3b82f6",
        "REFERENCES": "#22c55e",
        "MEMBER_OF": "#4b5563",
        "EXTENDS": "#f59e0b",
        "IMPLEMENTS": "#8b5cf6",
        "INFORMED_BY": "#06b6d4",
        "RESOLVES_TO": "#fbbf24",
        "LLM_TENSION": "#fb7185",
        "LLM_RELATED": "#94a3b8",
    }
    
    for src, tgt, data in G.edges(data=True):
        etype = data.get("type", "")
        weight = data.get("weight", 0.5)
        color = EDGE_COLORS.get(etype, "#6b7280")
        dash = etype in ("REFERENCES", "LLM_RELATED")
        
        net.add_edge(src, tgt, width=max(1, weight * 3.5), color=color, title=f"{etype}: {data.get('label', '')}", dashes=dash)
    
    # Add legend as HTML
    legend_html = """
    <div style="position:fixed;top:10px;left:10px;background:#161b22;padding:15px;border-radius:8px;border:1px solid #30363d;z-index:1000;font-family:monospace;font-size:12px;color:#c9d1d9;">
    <b style="font-size:14px;">Paradox Knowledge Graph</b><br><br>
    <b>Clusters:</b><br>
    <span style="color:#FF6B6B;">●</span> ATLAS333 Paradoxes (P01-P35)<br>
    <span style="color:#FFD93D;">●</span> Apex Dials<br>
    <span style="color:#DDA0DD;">●</span> Governance<br>
    <span style="color:#FF8C00;">●</span> Genesis<br>
    <span style="color:#4ECDC4;">●</span> Memory<br>
    <span style="color:#98FB98;">●</span> Engine<br>
    <span style="color:#FF1493;">●</span> Void Paradox<br><br>
    <b>Edges:</b><br>
    <span style="color:#ef4444;">━</span> Tension (paradox pair)<br>
    <span style="color:#3b82f6;">━</span> Wires To (architectural)<br>
    <span style="color:#22c55e;">┅</span> References<br>
    <span style="color:#f59e0b;">━</span> Extends<br>
    <span style="color:#8b5cf6;">━</span> Implements<br>
    <span style="color:#06b6d4;">━</span> Informed By<br>
    </div>
    """
    
    net.save_graph(output_path)
    
    # Inject legend
    with open(output_path, "r") as f:
        html = f.read()
    html = html.replace("<body>", f"<body>{legend_html}")
    with open(output_path, "w") as f:
        f.write(html)
    
    print(f"Graph saved: {output_path}")

# ============================================================
# MAIN
# ============================================================

def main():
    use_ollama = "--ollama" in sys.argv
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("PARADOX KNOWLEDGE GRAPH v2 — Core Focus")
    print("=" * 60)
    
    # Scan
    print("\n[1/5] Scanning core paradox files...")
    files = scan_core()
    print(f"  Found {len(files)} core paradox files:")
    for f in files:
        print(f"    {f['cluster']:12s} | {f['id']:35s} | {f['title'][:50]}")
    
    # Extract
    print("\n[2/5] Extracting relationships...")
    rels = extract_relationships(files)
    print(f"  Structural: {len(rels)} relationships")
    
    if use_ollama:
        print("\n[3/5] Ollama extraction...")
        ollama_rels = ollama_extract_all(files)
        rels.extend(ollama_rels)
        print(f"  + {len(ollama_rels)} LLM relationships")
    else:
        print("\n[3/5] Ollama skipped (--ollama to enable)")
    
    # Build
    print("\n[4/5] Building graph...")
    G = build_graph(files, rels)
    print(f"  Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    
    centrality = nx.degree_centrality(G)
    print("\n  Top 10 central nodes:")
    for node, score in sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {node:35s} cent={score:.3f} deg={G.degree(node)}")
    
    # Visualize
    print("\n[5/5] Generating visualization...")
    html_path = os.path.join(OUTPUT_DIR, "paradox_graph_v2.html")
    visualize(G, html_path)
    
    # Export JSON
    json_path = os.path.join(OUTPUT_DIR, "paradox_graph_v2.json")
    data = {
        "generated": datetime.now().isoformat(),
        "stats": {"nodes": G.number_of_nodes(), "edges": G.number_of_edges()},
        "nodes": [{"id": n, **d, "degree": G.degree(n), "centrality": centrality.get(n, 0)} for n, d in G.nodes(data=True)],
        "edges": [{"source": s, "target": t, **d} for s, t, d in G.edges(data=True)],
    }
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"\n  HTML: {html_path}")
    print(f"  JSON: {json_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
