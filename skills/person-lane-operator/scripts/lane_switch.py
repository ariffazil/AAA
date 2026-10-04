#!/usr/bin/env python3
"""
Lane-switch hook — auto-detect person trigger → load their lane assets.

Usage:
    python3 lane_switch.py '{"from_id":"1042200555","chat_id":"-1003815535761","username":"rico_ricaldo_33","text":"test"}'

Returns JSON with lane_detected + assets_loaded.

SOURCE OF TRUTH: /root/AAA/federation/person-register.json (person-register v2).
Lane config derived from register persons + /root/sado/ lane root for SYED.
Private layers NEVER loaded here — register holds DER models only, per privacy_policy.
"""
import json
import os
import sys

REGISTER_PATH = "/root/AAA/federation/person-register.json"

def load_register() -> dict:
    """Load the person register. Fail-closed: any error → empty register → main lane."""
    try:
        with open(REGISTER_PATH) as f:
            return json.load(f)
    except Exception as e:
        print(f"WARN: register unreadable ({e}) — falling back to main lane", file=sys.stderr)
        return {"persons": [], "routing": {}}

# Fallback lane roots for persons with known lane_root (register may carry it)
LANE_ROOTS = {
    "syed": "/root/sado",
}


def detect_lane(message_meta: dict) -> str:
    """Return lane_id if message matches a person trigger, else 'main'.

    Sub-context: for a person lane, returns 'syed:dm' or 'syed:sado'
    based on chat_id, so the right memory file loads.
    """
    user_id = str(message_meta.get("from_id", ""))
    chat_id = str(message_meta.get("chat_id", ""))
    username = message_meta.get("username", "").lower()
    text = message_meta.get("text", "").lower()

    register = load_register()
    persons = register.get("persons", [])
    lanes_known = register.get("routing", {}).get("lanes_known", {})

    # Direct match: telegram_id → person
    for person in persons:
        if user_id and user_id == str(person.get("telegram_id", "")):
            pid = person.get("person_id", "").lower()
            if pid in LANE_ROOTS:
                return _sub_context(pid, chat_id)
            return "main"
        # Username match for DMs/groups
        uname = str(person.get("username", "")).lower()
        if username and uname and username == uname:
            pid = person.get("person_id", "").lower()
            if pid in LANE_ROOTS:
                return _sub_context(pid, chat_id)
            return "main"

    # Chat-level: a person's group (chat_id in lane roots) — but only for the person's own group
    # NOTE: group routing needs explicit mapping; default: main lane for unknown chat senders.
    return "main"


# Per-person chat sub-contexts: chat_id → lane suffix
# SADO group for SYED; DM uses the person's own chat (user_id == chat_id)
CHAT_SUBCONTEXTS = {
    "-1003815535761": "sado",  # SADO group
}


def _sub_context(pid: str, chat_id: str) -> str:
    """Append sub-context (dm vs group) for a person lane."""
    suffix = CHAT_SUBCONTEXTS.get(chat_id, "dm")
    return f"{pid}:{suffix}"


def load_lane_assets(lane_id: str) -> dict:
    """Load memory + user + soul files for the detected lane."""
    if lane_id == "main":
        main_base = "/usr/local/lib/hermes-agent/profiles/aaa-hermes/memories"
        return {
            "lane": "main",
            "memory": open(f"{main_base}/MEMORY.md").read() if os.path.exists(f"{main_base}/MEMORY.md") else "",
            "user": open(f"{main_base}/USER.md").read() if os.path.exists(f"{main_base}/USER.md") else "",
        }

    # Person lanes: assets live in the person's lane root (e.g. /root/sado/)
    root = LANE_ROOTS.get(lane_id.split(":")[0])
    if not root:
        return {"lane": "main"}

    # Sub-context memory files (dm vs group) under the lane's telegram dir
    sub = lane_id.split(":")[1] if ":" in lane_id else "dm"
    tg_dir = os.path.join(root, "telegram")
    sub_memory = ""
    fname = f"MEMORY-syed-{sub}.md"
    p = os.path.join(tg_dir, fname)
    if os.path.exists(p):
        sub_memory = open(p).read()

    # Identity/dossier files under the lane root
    identity_dir = os.path.join(root, "identity")
    dossier = ""
    for fname in sorted(os.listdir(identity_dir)) if os.path.isdir(identity_dir) else []:
        if fname.upper().endswith((".MD", ".JSON")):
            p = os.path.join(identity_dir, fname)
            dossier += f"\n--- {fname} ---\n" + open(p).read() if os.path.exists(p) else ""

    return {
        "lane": lane_id,
        "sub_memory": sub_memory,
        "dossier": dossier,
        "canonical_refs": [os.path.join(root, d) for d in ("mak-health", "trading", "brand", "telegram") if os.path.isdir(os.path.join(root, d))],
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        meta = json.loads(sys.argv[1])
    else:
        meta = {
            "from_id": os.environ.get("TG_FROM_ID", ""),
            "chat_id": os.environ.get("TG_CHAT_ID", ""),
            "username": os.environ.get("TG_USERNAME", ""),
        }

    lane = detect_lane(meta)
    assets = load_lane_assets(lane)
    print(json.dumps({
        "lane_detected": lane,
        "assets_loaded": list(assets.keys()),
        "trigger": meta,
    }, indent=2))
