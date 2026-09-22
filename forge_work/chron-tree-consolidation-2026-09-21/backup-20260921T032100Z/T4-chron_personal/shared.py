"""CHRON Personal Edge — shared state management and delivery.

Cycle state directory: /root/.hermes/cron/state/chron_personal/
Each cycle writes a JSON file keyed by date and slot (M/E/R).

Privacy boundary: raw personal context NEVER crosses to ALPHA-ZEN group,
shared CHRON, public artifact, or other principal's lane. Only derived
non-sensitive relevance signals may cross.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

MYT = timezone(timedelta(hours=8))
STATE_DIR = Path("/root/.hermes/cron/state/chron_personal")
ENV_FILE = Path("/root/.hermes/.env")

# Telegram delivery target — Arif DM
ARIF_CHAT_ID = "267378578"

# Privacy boundary: these fields are stripped before any cross-lane export
PRIVATE_FIELDS = {"self_report", "inner_state", "raw_feedback", "qualia"}


def now_myt() -> datetime:
    return datetime.now(MYT)


def today_str() -> str:
    return now_myt().strftime("%Y-%m-%d")


def _env() -> dict[str, str]:
    """Read .env file, never log values."""
    out: dict[str, str] = {}
    try:
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"(?:export\s+)?([A-Z0-9_]+)=(.*)$", line)
            if m:
                out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    except OSError:
        pass
    return out


# ───────────────────────── cycle state ─────────────────────────

def _state_path(date_str: str, slot: str) -> Path:
    return STATE_DIR / f"{date_str}_{slot}.json"


def write_cycle(cycle: dict) -> Path:
    """Persist cycle state to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    p = _state_path(cycle["date"], cycle["slot"])
    p.write_text(json.dumps(cycle, indent=2, default=str))
    return p


def read_cycle(date_str: str, slot: str) -> dict | None:
    """Read a cycle state from disk."""
    p = _state_path(date_str, slot)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def latest_m_cycle() -> dict | None:
    """Read today's M cycle, or yesterday's if today's not yet fired."""
    today = today_str()
    m = read_cycle(today, "M")
    if m:
        return m
    # Fall back to yesterday
    yesterday = (now_myt() - timedelta(days=1)).strftime("%Y-%m-%d")
    return read_cycle(yesterday, "M")


def latest_e_cycle() -> dict | None:
    """Read today's E cycle."""
    return read_cycle(today_str(), "E")


def latest_r_cycle() -> dict | None:
    """Read today's R cycle."""
    return read_cycle(today_str(), "R")


# ───────────────────────── data access ─────────────────────────

def git_activity_since(since_hours: int = 12) -> dict[str, list[str]]:
    """Git log across federation repos since N hours ago."""
    import subprocess

    repos = ["arifOS", "A-FORGE", "AAA", "GEOX", "WEALTH", "WELL"]
    result: dict[str, list[str]] = {}
    for name in repos:
        repo = f"/root/{name}"
        if not os.path.isdir(f"{repo}/.git"):
            continue
        try:
            p = subprocess.run(
                ["git", "log", "--oneline", f"--since={since_hours} hours ago"],
                capture_output=True, text=True, timeout=10, cwd=repo,
            )
            lines = [l.strip() for l in p.stdout.strip().splitlines() if l.strip()]
            if lines:
                result[name] = lines
        except Exception:
            pass
    return result


def activity_count(git: dict[str, list[str]]) -> int:
    return sum(len(v) for v in git.values())


def _alive(url: str, timeout: float = 3.0) -> bool:
    """Conventions (AGENTS.md): HTTP 401/403 on health = UP."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        urllib.request.urlopen(req, timeout=timeout).read(2048)
        return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def federation_status() -> tuple[int, int, list[str]]:
    """Probe federation organs. Returns (alive, total, down_list)."""
    organs = {
        "kernel": "http://127.0.0.1:8088/health",
        "aforge": "http://127.0.0.1:7072/health",
        "geox": "http://127.0.0.1:8081/health",
        "wealth": "http://127.0.0.1:18082/health",
        "well": "http://127.0.0.1:18083/health",
        "frame": "http://127.0.0.1:18085/health",
        "arifflow": "http://127.0.0.1:7073/health",
        "aaa": "http://127.0.0.1:3001/health",
    }
    down = [n for n, u in organs.items() if not _alive(u)]
    return len(organs) - len(down), len(organs), down


def get_flow_health() -> dict | None:
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:7073/health",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=4) as r:
            return json.loads(r.read())
    except Exception:
        return None


def carry_forward_entries(hours: int = 12) -> list[str]:
    """Read recent carry_forward entries."""
    cf = Path("/root/.local/share/arifos/carry_forward.json")
    if not cf.exists():
        return []
    try:
        data = json.loads(cf.read_text())
        entries = data.get("entries", [])
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        recent = [
            e.get("content", "")[:120]
            for e in entries
            if e.get("timestamp", "") >= cutoff and e.get("content")
        ]
        return recent[-10:]  # Last 10
    except Exception:
        return []


def niat_execution_log(hours: int = 24) -> list[dict]:
    """Read recent NIAT executions."""
    log = Path("/root/.local/share/arifos/niat_execution_log.jsonl")
    if not log.exists():
        return []
    entries = []
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    try:
        for line in log.read_text().strip().splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get("timestamp", "") >= cutoff:
                entries.append(entry)
    except Exception:
        pass
    return entries[-10:]


# ───────────────────────── delivery ─────────────────────────

def send_telegram(text: str) -> tuple[bool, str]:
    """Send message to Arif DM via Telegram API."""
    env = _env()
    token = env.get("ASI_ARIFOS_BOT_TOKEN")
    if not token:
        return False, "token missing"
    payload = json.dumps({
        "chat_id": ARIF_CHAT_ID,
        "text": text,
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = json.loads(r.read().decode())
        return bool(body.get("ok")), body.get("description", "delivered")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}"


# ───────────────────────── niat candidate generation ─────────────────────────

def write_niat_candidates(candidates: list[dict], source: str) -> int:
    """Append niat candidates to the shared sidecar file.

    Same format as morning_briefing.py. Dedupes by intent.
    Returns count of NEW candidates written.
    """
    if not candidates:
        return 0
    niat_path = Path("/root/.local/share/arifos/niat_candidates.json")
    niat_path.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    try:
        existing = json.loads(niat_path.read_text()).get("candidates", [])
    except Exception:
        pass

    existing_intents = {c.get("intent") for c in existing}
    new = [c for c in candidates if c["intent"] not in existing_intents]
    if not new:
        return 0

    payload = {
        "$schema": "niat_candidates_v1",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": source,
        "candidates": existing + new,
    }
    niat_path.write_text(json.dumps(payload, indent=2, default=str))
    return len(new)


# ───────────────────────── privacy enforcement ─────────────────────────

def strip_private(obj: dict) -> dict:
    """Remove private fields before cross-lane export."""
    return {k: v for k, v in obj.items() if k not in PRIVATE_FIELDS}
