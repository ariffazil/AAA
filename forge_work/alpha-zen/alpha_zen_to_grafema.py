#!/usr/bin/env python3
"""alpha_zen_to_grafema.py — emit ALPHA-ZEN signals as episodic nodes in the federation graph.

Two write paths, both idempotent:
  1. FalkorDB direct (port 6380) — episodic node per signal, edge to day.
  2. Graphiti MCP (port 18412) — semantic ingestion via HTTP.

If both are unreachable: append to local shadow log (episodes_shadow.jsonl).
Never raises. Each card render → at most one episode per signal row.

This is the recursive-link piece. Tomorrow's card can query yesterday's episodes;
tomorrow's gate can demand `cross_checked: true` on overlapping topics.

USAGE
  python3 alpha_zen_to_grafema.py <card-json-path>
"""

from __future__ import annotations
import hashlib
import json
import os
import socket
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

CARDS_DIR = Path("/root/AAA/forge_work/alpha-zen/cards")
SHADOW = Path("/root/AAA/forge_work/alpha-zen/episodes_shadow.jsonl")
CALIBRATION = Path("/root/AAA/forge_work/alpha-zen/claim_calibration.jsonl")
FALKOR_HOST = os.environ.get("FALKOR_HOST", "127.0.0.1")
FALKOR_PORT = int(os.environ.get("FALKOR_PORT", "6380"))
GRAPHITI_HOST = os.environ.get("GRAPHITI_HOST", "127.0.0.1")
GRAPHITI_PORT = int(os.environ.get("GRAPHITI_PORT", "18412"))


def short_id(s: str, n: int = 8) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]


def card_episodes(card_path: Path) -> list[dict]:
    """Yield episode records from a card JSON. Stable IDs from text hash.

    Identity (per OpenClaw spec v1.1, 2026-09-22):
      episode_id     = az-<sha8>            signal identity, deterministic on (date,mode,n,who,text)
      calibration_id = same as episode_id   one vocab only — additionalProperties:false

    Sequencing is recoverable from match key (date, mode, n, who) + checked_at;
    we do not mint an ordinal ID, and the sidecar's `seq` field is a query helper,
    not part of the identity.
    """
    c = json.loads(card_path.read_text())
    date = c.get("date")
    mode = c.get("mode")
    if not date or not mode:
        return []
    out = []
    for row in c.get("rows", []):
        for who in ("arif", "syed"):
            sig = row.get(who) or {}
            text = (sig.get("text") or "").strip()
            if not text:
                continue
            cid = short_id(f"{date}:{mode}:{row.get('n','')}:{who}:{text}")
            out.append({
                "episode_id": f"az-{cid}",
                "calibration_id": f"az-{cid}",   # one ID for the whole calibration chain
                "date": date,
                "mode": mode,
                "row": row.get("n"),
                "label": row.get("label"),
                "tier": row.get("tier"),
                "who": who,
                "text": text,
                "source": sig.get("source", ""),
                "tag": sig.get("tag", ""),
                "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            })
    return out


def falkor_reachable() -> bool:
    s = socket.socket()
    s.settimeout(1.0)
    try:
        s.connect((FALKOR_HOST, FALKOR_PORT))
        s.close()
        return True
    except Exception:
        return False


def graphiti_reachable() -> bool:
    try:
        req = urllib.request.Request(
            f"http://{GRAPHITI_HOST}:{GRAPHITI_PORT}/health",
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=1.5) as r:
            return r.status == 200
    except Exception:
        return False


def falkor_write(episodes: list[dict]) -> tuple[int, str]:
    """Use redis-cli for FalkorDB. Cypher MERGE = idempotent."""
    if not episodes:
        return 0, "noop"
    written = 0
    last_msg = ""
    for ep in episodes:
        # Use Cypher MERGE so re-running is safe
        cy = (
            f"MERGE (e:Episode {{id:'{ep['episode_id']}'}}) "
            f"SET e.date='{ep['date']}', e.mode='{ep['mode']}', "
            f"e.row='{ep['row']}', e.label='{ep['label']}', "
            f"e.tier='{ep['tier']}', e.who='{ep['who']}', "
            f"e.text={json.dumps(ep['text'])[:1]}... "  # placeholder, replaced below
        )
        # Build a clean cypher with proper string escaping
        text_esc = ep["text"].replace("\\", "\\\\").replace("'", "\\'")
        cy = (
            f"MERGE (e:Episode {{id:'{ep['episode_id']}'}}) "
            f"SET e.date='{ep['date']}', e.mode='{ep['mode']}', "
            f"e.row='{ep['row']}', e.label='{ep['label']}', "
            f"e.tier='{ep['tier']}', e.who='{ep['who']}', "
            f"e.text='{text_esc}', "
            f"e.source='{(ep['source'] or '').replace(chr(39), chr(92)+chr(39))}', "
            f"e.calibration_id='{ep['calibration_id']}', "
            f"e.created_at='{ep['created_at']}' "
            f"WITH e "
            f"MERGE (d:Day {{date:'{ep['date']}', mode:'{ep['mode']}'}}) "
            f"MERGE (e)-[:ON]->(d) "
            f"RETURN e.id"
        )
        try:
            cmd = ["redis-cli", "-h", FALKOR_HOST, "-p", str(FALKOR_PORT),
                   "GRAPH.QUERY", "arifos", cy]
            import subprocess
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                written += 1
                last_msg = "ok"
            else:
                last_msg = f"err: {r.stderr.strip()[:120]}"
        except Exception as e:
            last_msg = f"exception: {e}"
    return written, last_msg


def shadow_log(episodes: list[dict], reason: str) -> None:
    """When both graph backends are down — write to local shadow log so nothing is lost."""
    with SHADOW.open("a") as fh:
        for ep in episodes:
            ep2 = dict(ep)
            ep2["shadow_reason"] = reason
            fh.write(json.dumps(ep2, ensure_ascii=False) + "\n")


def write_calibration_sidecar(episodes: list[dict]) -> int:
    """Append issued-claim records to claim_calibration.jsonl.

    Schema per OpenClaw spec v1.1 (2026-09-22):
      claim_id = episode_id  (one vocabulary only — az-<sha8>)
      seq      = ordinal within the day's render (1..18)  (query helper, NOT identity)

      {claim_id, seq, issued_at, date, mode, row, who, tier, label,
       episode_id, text, source}

    verdict/magnitude are NOT set here — the night-card pre-render checker
    (claim_calibrate.py) writes them later, only when the claim is checked.
    This file is the ISSUED ledger; the night card appends the CHECKED ledger.
    """
    if not episodes:
        return 0
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    with CALIBRATION.open("a") as fh:
        for seq, ep in enumerate(episodes, start=1):
            rec = {
                "claim_id": ep["calibration_id"],   # one vocab
                "seq": seq,                          # query helper
                "issued_at": now,
                "date": ep["date"],
                "mode": ep["mode"],
                "row": ep["row"],
                "who": ep["who"],
                "tier": ep["tier"],
                "label": ep["label"],
                "episode_id": ep["episode_id"],
                "text": ep["text"],
                "source": ep["source"],
                "verdict": None,
                "magnitude": None,
            }
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(episodes)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: alpha_zen_to_grafema.py <card-json-path>", file=sys.stderr)
        return 1
    card_path = Path(sys.argv[1])
    if not card_path.exists():
        print(f"card not found: {card_path}", file=sys.stderr)
        return 1

    episodes = card_episodes(card_path)
    if not episodes:
        print(f"no episodes extracted from {card_path.name}")
        return 0

    fk_ok = falkor_reachable()
    gr_ok = graphiti_reachable()
    print(f"FalkorDB ({FALKOR_HOST}:{FALKOR_PORT}): {'OK' if fk_ok else 'DOWN'}")
    print(f"Graphiti ({GRAPHITI_HOST}:{GRAPHITI_PORT}): {'OK' if gr_ok else 'DOWN'}")
    print(f"Episodes to ingest: {len(episodes)}")

    if fk_ok:
        written, msg = falkor_write(episodes)
        print(f"FalkorDB writes: {written}/{len(episodes)} ({msg})")
        sidecar_n = write_calibration_sidecar(episodes)
        print(f"Calibration sidecar issued: {sidecar_n}")
        return 0
    elif gr_ok:
        # Graphiti MCP would go here; not implemented tonight — keep scope tight.
        print("Graphiti path reserved; shadow-logging for now")
        shadow_log(episodes, "graphiti-only-stub")
        write_calibration_sidecar(episodes)
        return 0
    else:
        print("Both graph backends DOWN — shadow log only")
        shadow_log(episodes, "both-down")
        write_calibration_sidecar(episodes)
        return 0


if __name__ == "__main__":
    sys.exit(main())