#!/usr/bin/env bash
# Agent boot card — FILE READS ONLY. No curl. No FQ math.
# DITEMPA BUKAN DIBERI
set +e
MODE="${1:-}"
export ARIFOS_BOOT_MODE="$MODE"
exec python3 - <<'PY'
import json, os, sys
from datetime import datetime, timezone
from pathlib import Path

TERM = Path("/root/AAA/terminal")
STATE = TERM / "state.json"
MODELS = Path("/root/.config/federation-models.json")
CAPS = Path("/root/AAA/registries/models/CAPABILITIES.json")
STALE_S = 300
want_json = os.environ.get("ARIFOS_BOOT_MODE", "") in ("--json", "json")


def age_s(p: Path):
    try:
        return int(datetime.now(timezone.utc).timestamp() - p.stat().st_mtime)
    except Exception:
        return None


def load(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


st = load(STATE)
age = age_s(STATE)
fresh = st is not None and age is not None and age <= STALE_S

card = {
    "authority": (st or {}).get("authority") or "ARIF",
    "mode": (st or {}).get("mode") or "UNKNOWN",
    "fq": (st or {}).get("fq"),
    "fq_s": (st or {}).get("fq_s"),
    "fq_state": (st or {}).get("fq_state") or (st or {}).get("fq_verdict"),
    "diagnosis": (st or {}).get("diagnosis"),
    "mission": (st or {}).get("mission"),
    "today_law": (st or {}).get("today_law") or (st or {}).get("law"),
    "broadcast": (st or {}).get("broadcast"),
    "verify": (st or {}).get("verify"),
    "execute": (st or {}).get("execute"),
    "debt": (st or {}).get("debt"),
    "well": (st or {}).get("well"),
    "well_note": (st or {}).get("well_note"),
    "holds": (st or {}).get("holds") or [],
    "loop_now": (st or {}).get("loop_now"),
    "atlas": (st or {}).get("atlas") or {},
    "handover": (st or {}).get("handover") or [],
    "kernel": (st or {}).get("kernel"),
    "floors": (st or {}).get("floors"),
    "board_age_s": age,
    "board_fresh": fresh,
    "registries": {
        "law": "arifOS :8088 via arif_init (bind, do not infer FQ)",
        "state": str(STATE),
        "models": str(MODELS) if MODELS.exists() else None,
        "capabilities": str(CAPS) if CAPS.exists() else None,
        "tools": None,
        "skills": None,
    },
}

if want_json:
    print(json.dumps(card, default=str, indent=2))
    sys.exit(0 if fresh else 2)

print("=== AAA BOOT · consume, do not recompute ===")
if not st:
    print("board: MISSING — run /root/AAA/terminal/arifos-hero.sh --observe")
    print("do not curl organs to invent FQ")
    sys.exit(2)
if not fresh:
    print(f"board: STALE {age}s — run hero --observe (do not curl)")
else:
    print(f"board: FRESH {age}s")
print(f"authority : {card['authority']}")
print(f"mode      : {card['mode']}")
print(f"fq        : {card['fq_s']} {card['fq_state']}")
print(f"diagnosis : {card['diagnosis']}")
print(f"mission   : {card['mission']}")
print(f"law       : {card['today_law']}")
v, x, d = card["verify"], card["execute"], card["debt"]
if v is not None or x is not None:
    print(f"vx        : V={v} X={x} debt={d}  ← increment X")
if card.get("broadcast"):
    print(f"broadcast : {card['broadcast']}")
print(f"well      : {card['well']} ({card['well_note'] or 'ok'})")
print(f"loop      : {card['loop_now']}")
print(f"kernel    : {card['kernel']}  floors {card['floors']}/13")
holds = card["holds"][:4]
if holds:
    print("holds     :")
    for h in holds:
        print(f"  • {h}")
hops = card.get("handover") or []
if hops:
    print("handover  :")
    for h in hops[-3:]:
        print(f"  • [{h.get('time')}] {h.get('actor')}: {h.get('summary')}")
print()
print("LAW     arifOS  bind with arif_init — do not curl to infer FQ")
print(f"STATE   {card['registries']['state']}")
print(f"MODELS  {card['registries']['models']}")
print(f"CAPS    {card['registries']['capabilities']}")
print("TOOLS   (not minted — do not invent TOOLS.json)")
print("SKILLS  (not minted — do not invent SKILLS.json)")
print("order    : inherit. increment X. do not archaeologize.")
print("=== clerk ready ===")
sys.exit(0 if fresh else 2)
PY
