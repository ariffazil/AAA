#!/usr/bin/env python3
"""
backfill_qualification.py — add arifOS/qualification/v1 block to every AAA agent card.

F13 order 2026-09-25: backfill the cards (audit FL-4). Rules:
- math_competency derives from the card's OWN declared lane, mapped through
  APEX-MATH-CANON-2026-09-23 §5 signatures. Source and claim_state are carried
  on the card — CANON_DERIVED is never written as MEASURED.
- epistemic_typing is MEASURED only where an OBS/DER marker exists in the card.
- irfan.least_power is MEASURED only where an authority field exists.
- Human principal (F13) gets claim_state HUMAN_PRINCIPAL — machines never
  declare a human's competency.
Idempotent: re-running updates in place. Backup tar is created by the caller.
"""
from __future__ import annotations
import glob, json, os, re, sys
from datetime import datetime, timezone

AAA = "/root/AAA"
CANON = f"{AAA}/canon/APEX-MATH-CANON-2026-09-23.md"

ALL_LAYERS = ["L0","L0.5","L1","L1.5","L2","L3","L4","L4.5","L5","L6",
              "L7","L7.5","L8","L8.5","L9","L10","L11","L12"]

# APEX-MATH §5 — canon table (claim_state CANON_DERIVED)
SIG_CANON = {
    "333":      ["L0","L0.5","L1","L2","L3","L9","L12"],
    "555":      ["L0","L0.5","L1","L1.5","L2","L4","L5","L8","L10"],
    "888":      ["L0","L0.5","L6","L8.5","L10","L11"],
    "A-FORGE":  ["L3","L4","L4.5","L8"],
    "HERMES":   ["L1","L2","L6","L7.5"],
    "VAULT999": ["L2","L9","L10"],
    "GEOX":     ["L4.5","L5","L6","L7.5","L8","L8.5"],
    "WEALTH":   ["L1","L1.5","L3","L6","L10"],
    "WELL":     ["L4","L4.5","L8","L10"],
    "I-ARIF":   ALL_LAYERS,
}

# lane string → §5 role
LANE_MAP = [
    (r"333-AGI|EXECUTION",            "333"),
    (r"555-ASI|VERIFICATION",         "555"),
    (r"888-APEX|GOVERNANCE",          "888"),
    (r"FORGE-777",                    "A-FORGE"),
    (r"EVIDENCE-111",                 "GEOX"),
    (r"ADVISORY-222",                 "WEALTH"),
    (r"REFLECT-666",                  "WELL"),
    (r"TEMPORAL-777",                 "CHRON"),
    (r"IDENTITY",                     "I-ARIF"),
]

# id → §5 role when no lane declared
ID_MAP = [
    (r"geox",                    "GEOX"),
    (r"wealth",                  "WEALTH"),
    (r"well",                    "WELL"),
    (r"chrono",                  "CHRON"),
    (r"forge|a-forge",           "A-FORGE"),
    (r"hermes|openclaw|makcik",  "HERMES"),
    (r"arifos",                  "KERNEL"),
    (r"gateway",                 "GATEWAY"),
    (r"333|think",               "333"),
    (r"555|dream",               "555"),
    (r"888|judge",               "888"),
    (r"i-arif|sovereign|arif",   "I-ARIF"),
]

# FI-003 derivations (claim_state UNVERIFIED — pending empirical audit)
SIG_DERIVED = {
    "CHRON":   (["L1","L2","L5","L8","L10"], "temporal consequence: probability, information, dynamics, active inference, thermodynamic cost"),
    "KERNEL":  (["L0","L0.5","L6","L8.5","L10"], "constitutional judge machinery: logic, constraint solving, multi-agent equilibrium, causality, cost"),
    "GATEWAY": (["L2","L6"], "intent routing: information theory, multi-agent game"),
}

def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def classify(card_id, lane, text):
    if lane and lane.upper().startswith("F13"):
        return None, "HUMAN_PRINCIPAL", "human principal — competency never machine-declared"
    for pat, role in LANE_MAP:
        if lane and re.search(pat, lane, re.I):
            if role in SIG_CANON:
                return SIG_CANON[role], "CANON_DERIVED", f"APEX-MATH-CANON-2026-09-23 §5 via declared lane ({role})"
            if role in SIG_DERIVED:
                return SIG_DERIVED[role][0], "UNVERIFIED", f"FI-003 derivation: {SIG_DERIVED[role][1]}"
    for pat, role in ID_MAP:
        if re.search(pat, card_id, re.I):
            if role in SIG_CANON:
                return SIG_CANON[role], "CANON_DERIVED", f"APEX-MATH-CANON-2026-09-23 §5 via id ({role})"
            if role in SIG_DERIVED:
                return SIG_DERIVED[role][0], "UNVERIFIED", f"FI-003 derivation: {SIG_DERIVED[role][1]}"
    return None, "UNVERIFIED", "no lane/id mapping — awaiting §5 empirical audit"

def main():
    paths = sorted(set(
        glob.glob(f"{AAA}/agent-cards/**/agent-card*.json", recursive=True)
        + glob.glob(f"{AAA}/agents/_external/*/agent-card.json")))
    touched, skipped = [], []
    for p in paths:
        if os.path.getsize(p) < 1024:
            skipped.append((p, "junk-size <1KB"))
            continue
        try:
            d = json.load(open(p))
        except Exception as e:
            skipped.append((p, f"parse-fail: {e}"))
            continue
        card_id = str(d.get("id") or d.get("agentId") or d.get("name") or os.path.basename(os.path.dirname(p)))
        wb = d.get("warga_binding") or {}
        lane = wb.get("lane") or d.get("emd_lane") or d.get("lane") or ""
        text = json.dumps(d)

        layers, cstate, source = classify(card_id, lane, text)
        mc = ({"layers": layers, "source": source, "claim_state": cstate}
              if layers is not None
              else {"layers": None, "source": source, "claim_state": cstate})

        epi = bool(re.search(r"OBS.?/? ?DER|epistemic|OBS/DER", text, re.I))
        epistemic = ({"declared": True, "labels": ["OBS","DER","INT","SPEC","UNKNOWN"],
                      "evidence": "epistemic label marker present in card",
                      "claim_state": "MEASURED"} if epi else
                     {"declared": False, "labels": ["OBS","DER","INT","SPEC","UNKNOWN"],
                      "evidence": None, "claim_state": "UNVERIFIED"})

        auth_val = (wb.get("authority_level") or d.get("authority_level")
                    or d.get("authority_ceiling") or "")
        lp = ({"declared": True, "evidence": f"authority bound declared: {auth_val or 'present'}",
               "claim_state": "MEASURED"} if (auth_val or re.search(r"authority_ceiling|authority_level", text)) else
              {"declared": False, "evidence": None, "claim_state": "UNVERIFIED"})
        abst = bool(re.search(r"abstain|abstention|restraint|SABAR", text, re.I))
        irfan = {"least_power": lp,
                 "abstention": ({"declared": True, "evidence": "abstention/restraint marker present", "claim_state": "MEASURED"}
                                if abst else {"declared": False, "evidence": None, "claim_state": "UNVERIFIED"}),
                 "thesis_ref": f"{AAA}/canon/IRFAN-ANTI-EXTRACTION-THESIS-2026-09-23.md"}

        d["qualification"] = {
            "schema": "arifOS/qualification/v1",
            "added": utc(),
            "added_by": "FI-003 under F13 order 2026-09-25 (backfill-the-cards)",
            "math_competency": mc,
            "epistemic_typing": epistemic,
            "irfan": irfan,
        }
        with open(p, "w") as f:
            json.dump(d, f, indent=2, ensure_ascii=True)
            f.write("\n")
        touched.append((p.replace(AAA + "/", ""), card_id, cstate, epi, bool(auth_val)))

    print(f"backfilled {len(touched)} · skipped {len(skipped)}")
    for p, cid, cs, epi, auth in touched:
        print(f"  {cid:<18} math={cs:<15} epi={'M' if epi else '.'} lp={'M' if auth else '.'}  {p}")
    for p, why in skipped:
        print(f"  SKIP {why}: {p}")
    # referential check: canon file must exist for CANON_DERIVED sources
    assert os.path.exists(CANON), f"canon source missing: {CANON}"
    return 0

if __name__ == "__main__":
    sys.exit(main())
