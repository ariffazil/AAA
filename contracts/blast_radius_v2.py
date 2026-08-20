#!/usr/bin/env python3
"""
BLAST-RADIUS v2  —  arifFLOW min-cut governance tool
Grinberg §9.4 (Edmonds-Karp / Ford-Fulkerson), zero dependencies.

Changes vs v1 (the version Arif and I forged last turn):
  - AUTHORITY split into SUBMITS_TO and COMMANDS  (closes the H5 false positive)
  - Real-registry manifest for the federation (option ii from the prior turn)
  - Multi-source blast map: min-cut from every organ to WORLD
  - Honest receipt file (no VAULT999)
"""

from collections import deque, defaultdict
import hashlib, json, os
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# EDGE SEMANTICS  (partition function, REQUIRED)
# ---------------------------------------------------------------------------
EDGE_TYPES = {
    "AUTHORITY":   "DEPRECATED — use SUBMITS_TO or COMMANDS (split for H5 directionality)",
    "SUBMITS_TO":  "child -> root: licit reporting chain (executor answers to sovereign)",
    "COMMANDS":    "would-be root -> child: HARAM H5 if from executor to higher tier",
    "DELEGATION":  "A2A: one organ may invoke another (capability, not power)",
    "ACTUATION":   "can push an irreversible action toward the WORLD",
    "SENSING":     "reads evidence FROM the world (never toward irreversible act)",
    "GATE":        "two-phase commit / F13 seal — the ONLY licensed collapse arc",
}

# Only ACTUATION and GATE arcs transmit capacity in the max-flow problem.
# All other types carry information or command, not irreversibility.
FLOW_BEARING = {"ACTUATION", "GATE"}


class Federation:
    def __init__(self, name):
        self.name = name
        self.nodes = set()
        self.arcs = {}  # (u,v) -> {"cap": int, "type": str}

    def add(self, u, v, cap, etype):
        if etype not in EDGE_TYPES:
            raise ValueError(f"unknown edge type {etype!r}")
        if etype == "AUTHORITY":
            raise ValueError("AUTHORITY is deprecated; use SUBMITS_TO or COMMANDS")
        self.nodes |= {u, v}
        self.arcs[(u, v)] = {"cap": cap, "type": etype}
        return self

    def _capacity_graph(self):
        cap = defaultdict(int)
        for (u, v), meta in self.arcs.items():
            if meta["type"] in FLOW_BEARING:
                cap[(u, v)] += meta["cap"]
        return cap

    # -------- Edmonds-Karp (BFS-augmented Ford-Fulkerson) -----------------
    def max_flow_min_cut(self, source, sink):
        if source not in self.nodes or sink not in self.nodes:
            raise ValueError("source/sink not in federation")
        cap = self._capacity_graph()
        res = defaultdict(int)
        adj = defaultdict(set)
        for (u, v), c in cap.items():
            res[(u, v)] += c
            adj[u].add(v)
            adj[v].add(u)
        flow_value = 0

        def bfs_augment():
            parent = {source: None}
            q = deque([source])
            while q:
                u = q.popleft()
                for w in adj[u]:
                    if w not in parent and res[(u, w)] > 0:
                        parent[w] = u
                        if w == sink:
                            return parent
                        q.append(w)
            return None

        while True:
            parent = bfs_augment()
            if parent is None:
                break
            v, bottleneck = sink, float("inf")
            while parent[v] is not None:
                u = parent[v]
                bottleneck = min(bottleneck, res[(u, v)])
                v = u
            v = sink
            while parent[v] is not None:
                u = parent[v]
                res[(u, v)] -= bottleneck
                res[(v, u)] += bottleneck
                v = u
            flow_value += bottleneck

        S, q = {source}, deque([source])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in S and res[(u, w)] > 0:
                    S.add(w)
                    q.append(w)
        cut_arcs = [(u, v) for (u, v), c in cap.items()
                    if u in S and v not in S and c > 0]
        return flow_value, cut_arcs, S

    # -------- HARAM scan with direction-aware H5 --------------------------
    def haram_scan(self, sovereign, executor, authority_nodes):
        findings = []

        # H2: self-loop
        for (u, v) in self.arcs:
            if u == v:
                findings.append(("H2 self-loop", (u, v), "VOID"))

        # W1 / H1: acyclicity on authority+gates (treated as DAG)
        auth_adj = defaultdict(list)
        auth_nodes = set()
        for (u, v), m in self.arcs.items():
            if m["type"] in ("SUBMITS_TO", "COMMANDS", "GATE"):
                auth_adj[u].append(v)
                auth_nodes |= {u, v}
        cyc = self._find_cycle(auth_adj, auth_nodes)
        if cyc:
            tag = "H1 cycle-through-sovereign" if sovereign in cyc else "W1 authority cycle"
            findings.append((tag, tuple(cyc), "VOID"))

        # H5 (now direction-aware): COMMANDS arc from executor to higher tier
        # is the real violation. SUBMITS_TO from executor to its sovereign is licit.
        for (u, v), m in self.arcs.items():
            if u == executor and v in authority_nodes and m["type"] == "COMMANDS":
                findings.append(("H5 executor self-authorization (COMMANDS arc)", (u, v), "HOLD/VOID"))
            # legacy AUTHORITY detection: COMMANDS is the catch-all for the haram case
            if u == executor and v in authority_nodes and m["type"] == "SUBMITS_TO":
                # licit reporting — do NOT flag
                pass

        return findings

    @staticmethod
    def _find_cycle(adj, nodes):
        color = {n: 0 for n in nodes}
        stack_path = []
        def dfs(u):
            color[u] = 1
            stack_path.append(u)
            for w in adj[u]:
                if color.get(w, 0) == 1:
                    i = stack_path.index(w)
                    return stack_path[i:]
                if color.get(w, 0) == 0:
                    r = dfs(w)
                    if r:
                        return r
            color[u] = 2
            stack_path.pop()
            return None
        for n in nodes:
            if color[n] == 0:
                r = dfs(n)
                if r:
                    return r
        return None


# ===========================================================================
# P1: re-run synthetic GOVERNED vs DRIFTED with the AUTHORITY split
# ===========================================================================
def governed_synthetic():
    F = Federation("GOVERNED-synthetic")
    # Licit arborescence toward ARIF (F13 sovereign)
    F.add("A-FORGE", "AAA",    cap=1, etype="SUBMITS_TO")
    F.add("AAA",     "arifOS", cap=1, etype="SUBMITS_TO")
    F.add("arifOS",  "ARIF",   cap=1, etype="SUBMITS_TO")
    F.add("GEOX",    "A-FORGE", cap=3, etype="DELEGATION")
    F.add("WEALTH",  "A-FORGE", cap=3, etype="DELEGATION")
    F.add("WELL",    "A-FORGE", cap=3, etype="DELEGATION")
    F.add("WORLD",   "GEOX",   cap=9, etype="SENSING")
    F.add("A-FORGE", "GATE_F13", cap=5, etype="ACTUATION")
    F.add("GATE_F13", "WORLD",   cap=1, etype="GATE")
    return F

def drifted_synthetic():
    F = governed_synthetic()
    F.name = "DRIFTED-synthetic"
    F.add("A-FORGE", "WORLD", cap=4, etype="ACTUATION")
    F.add("WEALTH",  "WORLD", cap=2, etype="ACTUATION")
    F.add("A-FORGE", "arifOS", cap=1, etype="COMMANDS")  # real H5
    return F


# ===========================================================================
# P2: real-registry manifest
# ===========================================================================
def real_registry():
    """
    Built from federation code map (memory 2026-06-22) and declared surfaces.
    Capacities are NOMINAL placeholders (INTERPRET) until sovereign declares real grants.
    """
    F = Federation("REAL-REGISTRY")
    # --- sovereign chain (licit arborescence toward F13) ---
    F.add("A-FORGE", "AAA",     cap=1, etype="SUBMITS_TO")
    F.add("AAA",     "arifOS",  cap=1, etype="SUBMITS_TO")
    F.add("arifOS",  "ARIF",    cap=1, etype="SUBMITS_TO")  # ARIF = F13 sovereign root
    # --- intra-federation A2A delegations (capability, not power) ---
    F.add("GEOX",    "A-FORGE", cap=3, etype="DELEGATION")
    F.add("WEALTH",  "A-FORGE", cap=3, etype="DELEGATION")
    F.add("WELL",    "A-FORGE", cap=3, etype="DELEGATION")
    F.add("AAA",     "GEOX",    cap=2, etype="DELEGATION")
    F.add("AAA",     "WEALTH",  cap=2, etype="DELEGATION")
    F.add("AAA",     "WELL",    cap=2, etype="DELEGATION")
    # --- sensing arcs (world -> organs; never toward irreversible) ---
    F.add("WORLD",   "GEOX",    cap=9, etype="SENSING")
    F.add("WORLD",   "WEALTH",  cap=9, etype="SENSING")
    F.add("WORLD",   "WELL",    cap=9, etype="SENSING")
    # --- THE licensed collapse: F13 gate, capacity 1 (single seal) ---
    F.add("A-FORGE", "GATE_F13", cap=5, etype="ACTUATION")
    F.add("GATE_F13", "WORLD",   cap=1, etype="GATE")
    return F


# ===========================================================================
# Reporting
# ===========================================================================
def report_p1(F, source="A-FORGE", sink="WORLD"):
    print("=" * 72)
    print(f"P1 SYNTHETIC: {F.name}    |  {source} -> {sink}")
    print("=" * 72)
    val, cut, S = F.max_flow_min_cut(source, sink)
    print(f"  BLAST RADIUS (min-cut) : {val}")
    print(f"  BOTTLENECK ARCS        :")
    for (u, v) in cut:
        t = F.arcs[(u, v)]["type"]
        c = F.arcs[(u, v)]["cap"]
        print(f"      {u:>9} -> {v:<9}  [{t}]  cap={c}")
    haram = F.haram_scan(sovereign="ARIF", executor="A-FORGE",
                         authority_nodes={"arifOS", "AAA", "ARIF"})
    if haram:
        print("  HARAM scan:")
        for tag, where, v in haram:
            print(f"      [{v:>9}]  {tag}  at {where}")
    else:
        print("  HARAM scan: clean.")
    print()


def report_p2_p3(F):
    print("=" * 72)
    print(f"P2/P3 REAL REGISTRY: {F.name}")
    print("=" * 72)
    print(f"  nodes ({len(F.nodes)}): {sorted(F.nodes)}")
    print(f"  arcs  ({len(F.arcs)})")
    print()
    print("  P3 — multi-source blast-radius map (source = each organ, sink = WORLD):")
    print("  " + "-" * 68)
    print(f"  {'SOURCE':<10} {'MIN-CUT':>8}  {'VERDICT'}")
    print("  " + "-" * 68)
    organ_list = sorted(n for n in F.nodes if n not in ("WORLD", "ARIF", "GATE_F13"))
    rows = []
    for src in organ_list:
        val, cut, _ = F.max_flow_min_cut(src, "WORLD")
        verdict = "SEAL (1)" if val <= 1 else f"HOLD ({val}) — independent paths to WORLD"
        rows.append((src, val, verdict, cut))
    rows.sort(key=lambda r: r[1])  # lowest blast radius first (most governed)
    for src, val, verdict, _ in rows:
        print(f"  {src:<10} {val:>8}  {verdict}")
    print()
    print("  Bottleneck arcs per source:")
    for src, val, _, cut in rows:
        print(f"    {src} (min-cut={val}):")
        for (u, v) in cut:
            t = F.arcs[(u, v)]["type"]
            c = F.arcs[(u, v)]["cap"]
            print(f"        {u} -> {v}  [{t}]  cap={c}")
        print()
    return rows


# ===========================================================================
# Receipt
# ===========================================================================
def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ===========================================================================
# Main
# ===========================================================================
if __name__ == "__main__":
    now = datetime.now(timezone.utc).isoformat()
    print(f"arifFLOW blast-radius audit  |  {now}")
    print(f"partition function: FLOW_BEARING={sorted(FLOW_BEARING)}, sink=WORLD (default)")
    print()

    # P1
    report_p1(governed_synthetic())
    report_p1(drifted_synthetic())

    # P2 + P3
    real = real_registry()
    rows = report_p2_p3(real)

    # Persist blast map alongside the audit artifact
    out_dir = "/root/AAA/contracts"
    blast_map_path = os.path.join(out_dir, "blast_map_2026-08-20.txt")
    with open(blast_map_path, "w") as f:
        f.write(f"arifFLOW blast-radius map  |  {now}\n")
        f.write(f"sink = WORLD (default; INTERPRET)\n")
        f.write("=" * 72 + "\n")
        f.write(f"{'SOURCE':<10} {'MIN-CUT':>8}  {'VERDICT'}\n")
        f.write("-" * 72 + "\n")
        for src, val, verdict, _ in rows:
            f.write(f"{src:<10} {val:>8}  {verdict}\n")
        f.write("\nBottleneck arcs per source:\n")
        for src, val, _, cut in rows:
            f.write(f"  {src} (min-cut={val}):\n")
            for (u, v) in cut:
                t = real.arcs[(u, v)]["type"]
                c = real.arcs[(u, v)]["cap"]
                f.write(f"      {u} -> {v}  [{t}]  cap={c}\n")
            f.write("\n")
    print(f"blast map written: {blast_map_path}")

    # Receipt
    audit_path = os.path.join(out_dir, "arifFLOW_blast_audit_2026-08-20.honest.md")
    audit_sha = sha256_of_file(audit_path)
    map_sha = sha256_of_file(blast_map_path)
    print()
    print("=" * 72)
    print("RECEIPT (local, not VAULT999)")
    print(f"  audit artifact SHA256 : {audit_sha}")
    print(f"  blast map     SHA256 : {map_sha}")
    print(f"  mode          : HONEST")
    print(f"  VAULT999 seal : NOT INVOKED  (F13 reserved)")
    print("=" * 72)
