#!/usr/bin/env python3
"""
APEX LADDER WITNESS — DISPLAY_ONLY telemetry
F13 PARTIAL verdict 2026-10-07: ZEN CANDIDATE++, deployed as witness + falsification instrument ONLY.

Law candidate (Part A):  "State does not exist without an aggregation law."
                          Evidence -> Aggregation Law -> State -> Verdict

WITNESS ONLY (F13 HARAM list, sovereign 2026-10-07):
  - never governs      (no verdict, no authority)
  - never mutates      (no kernel state, no automation trigger)
  - never acts alone   (evidence goes to 888-APEX / CHRON, humans decide)

Usage:
  apex_ladder.py observe kernel                    # live: 4 measured apex_scalars from :8088
  apex_ladder.py observe 0.95 0.85 0.20 0.90       # any positive vector (labeled SPEC)
  apex_ladder.py log kernel                        # observe + append to telemetry JSONL
  apex_ladder.py report                            # tension trend from telemetry
"""

import json, math, os, sys, time, urllib.request

TELEMETRY = "/root/AAA/federation/apex_ladder_telemetry.jsonl"
KERNEL = "http://127.0.0.1:8088/health"


def _var(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def ladder(d):
    """Five aggregation laws over one positive vector + derived governance indices."""
    d = [float(x) for x in d]
    if not d or any(x <= 0 for x in d):
        raise ValueError("all components must be > 0")
    n = len(d)
    H = n / sum(1 / x for x in d)  # weakest gets most votes
    G = math.prod(d) ** (1.0 / n)  # log-equal votes (none dominates)
    A = sum(d) / n  # equal votes
    RMS = math.sqrt(sum(x * x for x in d) / n)  # magnitude-weighted
    C = sum(x * x for x in d) / sum(d)  # value votes for itself
    tension = (C - H) / A  # aspiration-authority vs constraint-authority
    return {
        "H": round(H, 6),
        "G": round(G, 6),
        "A": round(A, 6),
        "RMS": round(RMS, 6),
        "C": round(C, 6),
        "tension": round(tension, 6),
        "coherence": round(1 - tension, 6),
        "aggregation_variance": round(_var([H, G, A, RMS, C]), 6),
        "rawls_sacrifice_1_minus_H_over_A": round(1 - H / A, 6),
        "atkinson_g_1_minus_G_over_A": round(1 - G / A, 6),
        "bottleneck_value": round(min(d), 6),
        "bottleneck_index": d.index(min(d)),
        "chain_product": round(math.prod(d), 6),
    }


def observe(arg):
    """arg = 'kernel' | comma/space-separated positive numbers."""
    if arg == "kernel":
        h = json.load(urllib.request.urlopen(KERNEL, timeout=30))
        sc = h.get("apex_scalars", {})
        pairs = [(k, v["value"]) for k, v in sc.items() if v.get("status") == "MEASURED" and v.get("value") is not None]
        keys, vals = [p[0] for p in pairs], [p[1] for p in pairs]
        return {
            "label": "OBS",
            "source": "arifOS :8088/health apex_scalars — kernel OUTPUT scalars "
            "(G,C_dark,h,QDF), NOT APEX dial inputs (dials not exposed at /health)",
            "vector": dict(zip(keys, [round(v, 6) for v in vals])),
            "ladder": ladder(vals),
        }
    vals = [float(x) for x in arg.replace(",", " ").split()]
    return {
        "label": "SPEC",
        "source": "caller-supplied vector (exemplar, not live state)",
        "vector": vals,
        "ladder": ladder(vals),
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    mode = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if mode == "report":
        if not os.path.exists(TELEMETRY):
            print("no telemetry yet")
            return
        rows = [json.loads(l) for l in open(TELEMETRY) if l.strip()]
        print(f"{len(rows)} observations")
        for r in rows:
            L = r["ladder"]
            print(
                f"{r['ts']}  [{r['label']}]  tension={L['tension']:.4f}  "
                f"H={L['H']:.4f} G={L['G']:.4f} A={L['A']:.4f}  "
                f"bottleneck[{L['bottleneck_index']}]={L['bottleneck_value']:.4f}  {r['source'][:60]}"
            )
        return

    row = dict(ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **observe(arg))

    if mode == "log":
        with open(TELEMETRY, "a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"appended -> {TELEMETRY}")
    elif mode != "observe":
        print(f"unknown mode: {mode}")
        return

    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
