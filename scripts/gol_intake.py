#!/usr/bin/env python3
"""GOL intake — append gut-override rows to the CHRON side-table.

Enforces gut-override-ledger-spec.md (Amendments 1-2):
  A1. gut_read: the sovereign's verbatim words or empty. Non-empty rows MUST
      carry gut_read_provenance="human_verbatim" (agent synthesis forbidden).
  A2. Third-party privacy pass: durable rows carry role labels, never names.

Usage:  gol_intake.py <json-file>     # one row (dict) or many (list)
        gol_intake.py --verify        # validate existing ledger
"""
import json, sys, uuid, datetime, pathlib

DATA = pathlib.Path("/root/chron/data/gut_overrides.jsonl")
REQUIRED = ["domain", "evidence", "hermes_recommended", "arif_did",
            "gut_read", "outcome_state"]
ALLOWED_OUTCOMES = {"in_progress", "proven", "proven_songsang", "pending", "unresolvable"}
FORBIDDEN_NAMES = ["kak su", "kuan hoong", "thu ya", "laletha", "puan laletha",
                   "syed", "abah"]  # third parties -> role labels (A2)

def validate(row: dict) -> list:
    errs = []
    for k in REQUIRED:
        if k not in row: errs.append(f"missing required field: {k}")
    if row.get("outcome_state") not in ALLOWED_OUTCOMES:
        errs.append(f"outcome_state must be one of {sorted(ALLOWED_OUTCOMES)}")
    gr = row.get("gut_read", "")
    if gr and row.get("gut_read_provenance") != "human_verbatim":
        errs.append("gut_read non-empty but gut_read_provenance != 'human_verbatim' (A1)")
    blob = json.dumps(row, ensure_ascii=False).lower()
    for n in FORBIDDEN_NAMES:
        if n in blob:
            errs.append(f"third-party name detected: '{n}' -> use role label (A2)")
    return errs

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print(__doc__); sys.exit(0)
    if sys.argv[1] == "--verify":
        bad = 0; n = 0
        for line in DATA.read_text().splitlines():
            if not line.strip(): continue
            n += 1; errs = validate(json.loads(line))
            if errs: bad += 1; print(f"row {n}: {errs}")
        print(f"{n} rows checked, {bad} invalid"); sys.exit(1 if bad else 0)
    rows = json.load(open(sys.argv[1]))
    if isinstance(rows, dict): rows = [rows]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out = []
    for r in rows:
        errs = validate(r)
        if errs: print(f"REJECTED {r.get('case_id','?')}: {errs}"); sys.exit(1)
        r.setdefault("override_id", f"gol-{uuid.uuid4().hex[:12]}")
        r["recorded_at"] = now
        out.append(json.dumps(r, ensure_ascii=False))
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with DATA.open("a") as f:
        f.write("\n".join(out) + "\n")
    print(f"appended {len(out)} row(s) -> {DATA}")

if __name__ == "__main__":
    main()
