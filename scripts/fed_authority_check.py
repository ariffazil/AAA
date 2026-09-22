#!/usr/bin/env python3
"""fed_authority_check.py — Authority Graph oracle (fed-authority-graph/v1)."""
import json, sys
G="/root/.config/fed-authority-graph.json"
def check(actor, action):
    g=json.load(open(G)); a=g["actions"].get(action)
    if a is None: return f"DENY (unknown action '{action}')"
    v=a.get(actor)
    if v is None: return f"DENY (actor '{actor}' not mapped for '{action}')"
    note=a.get("_note","")
    return f"{v}" + (f" — {note}" if note else "")
if __name__=="__main__":
    if len(sys.argv)!=3: print(__doc__); sys.exit(2)
    r=check(sys.argv[1],sys.argv[2]); print(r)
    sys.exit(0 if r.startswith("ALLOW") else 1)
