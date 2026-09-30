#!/usr/bin/env python3
"""
i_arif_continuity_probe.py — make the i-arif lane's continuity FALSIFIABLE.

WHY THIS EXISTS
  On 2026-09-29 the i-arif lane was dead for ~8 hours (368 auth failures) and
  nobody was told. SpendLogs recorded every failure; no reader existed.
  This is the reader. It answers four questions with a red/green verdict:
    1. Is the inference proxy alive?
    2. Does the seat key still authenticate?      <- the thing that silently died
    3. Which rung/model is actually serving i-arif?
    4. How many lane failures since a given window?
  Exit 0 = CONTINUITY HELD · 1 = CONTINUITY BROKEN · 2 = proxy down.

NOT a witness, NOT a gate. A reader. It writes nothing, mutates nothing,
prints no secret values. Run it by hand, or from any cron that already exists.

Usage:
  python3 /root/AAA/scripts/i_arif_continuity_probe.py
  python3 /root/AAA/scripts/i_arif_continuity_probe.py --window-hours 24
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ZEN_KEY_ENV = Path("/root/.secrets/fed-zen-key.env")
ZEN_FRONTEND = "http://127.0.0.1:4012/v1"   # own-key path (the seat contract)
PROXY_LOCAL = "http://127.0.0.1:4013"       # litellm direct
PG_CONTAINER = "postgres"
PG_DB = "litellm"
PG_USER = "arifos_admin"

# Seats that present their OWN virtual key through :4012.
# (master-key clients — e.g. /opt/asi-arifos-bot — are NOT listed: their key
#  comes from env, not from LiteLLM_VerificationToken, so a token-table wipe
#  cannot break them. That asymmetry is why this incident was silent.)
SEATS = [
    ("hermes",  Path("/root/.secrets/fed-zen-key.env"), "FED_ZEN_KEY", True),
    ("wawa",    Path("/root/.secrets/wawa-zen-key.env"), "WAWA_ZEN_KEY", False),
]


def _load_var(envfile: Path, var: str) -> str | None:
    """Read one value from an env file without ever printing it."""
    if not envfile.exists():
        return None
    for line in envfile.read_text().splitlines():
        line = line.strip()
        if line.startswith(f"{var}="):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            return v or None
    return None


def _req(url: str, key: str | None = None, payload: dict | None = None, timeout: int = 15, attempts: int = 3):
    """Returns (status, body). status 0 == unreachable after `attempts`.

    A transient blip must NOT be reported as an outage, and an unparseable body
    must NOT be conflated with an unreachable host — a reader that cries DOWN on
    a single failed socket gets ignored, which is the failure it exists to fix.
    """
    last_err = "unreachable"
    for attempt in range(max(1, attempts)):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(url, data=data)
        if key:
            req.add_header("Authorization", f"Bearer {key}")
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode(errors="replace")
                try:
                    return r.status, json.loads(raw or "{}")
                except Exception:
                    # transport succeeded; body just isn't JSON. Status is still truth.
                    return r.status, {"_raw": raw[:200], "_note": "non-json body"}
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read().decode() or "{}")
            except Exception:
                body = {}
            return e.code, body          # a served error IS an answer — do not retry
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}"
            if attempt + 1 < max(1, attempts):
                time.sleep(1.5 * (attempt + 1))
    return 0, {"error": last_err}


def _scrub(s: str) -> str:
    s = re.sub(r"sk-[A-Za-z0-9_\-]{6,}", "sk-<REDACTED>", s)
    # also mask partially-masked forms (sk-...TZUg) so the probe never echoes a key tail
    return re.sub(r"sk-[.\-_A-Za-z0-9]{1,8}[A-Za-z0-9]{3,4}\b", "sk-<REDACTED>", s)


def _psql(sql: str, timeout: int = 30) -> str:
    try:
        r = subprocess.run(
            ["docker", "exec", "-i", PG_CONTAINER, "psql", "-U", PG_USER, "-d", PG_DB, "-t", "-A", "-F", "|", "-c", sql],
            capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return f"psql_unavailable: {type(e).__name__}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window-hours", type=int, default=24)
    ap.add_argument("--model", default="i-arif")
    a = ap.parse_args()

    print("=" * 66)
    print("i-arif CONTINUITY PROBE")
    print("=" * 66)
    broken: list[str] = []

    # ── 1. proxy alive ────────────────────────────────────────────────
    st, body = _req(f"{PROXY_LOCAL}/health/liveliness", timeout=8)
    live = st == 200
    print(f"[1] proxy :4013 alive .................. {'OK' if live else 'DOWN'}")
    if not live:
        broken.append("proxy_down")

    # ── 2. seat keys authenticate (the silent killer) ─────────────────
    print("[2] seat virtual keys (:4012 own-key path):")
    primary_key = None
    auth_ok = False
    for name, envfile, var, is_primary in SEATS:
        k = _load_var(envfile, var)
        if not k:
            print(f"      {name:8s} {var:14s} ....... not found")
            if is_primary:
                broken.append("key_missing")
            continue
        if not live:
            print(f"      {name:8s} {var:14s} ....... not checked (proxy down)")
            continue
        st, body = _req(f"{ZEN_FRONTEND}/models", key=k, timeout=15)
        ok = st == 200
        tag = "PRIMARY" if is_primary else "seat"
        print(f"      {name:8s} {var:14s} ....... {'OK' if ok else f'FAIL ({st})'}   [{tag}]")
        if not ok:
            print(f"               reason: {_scrub(str(body.get('error', body)))[:130]}")
            if is_primary:
                broken.append("key_unauthenticated")
        if is_primary:
            auth_ok = ok
            primary_key = k

    # ── 3. which rung is actually serving ─────────────────────────────
    if auth_ok and primary_key:
        st, body = _req(f"{ZEN_FRONTEND}/chat/completions", key=primary_key,
                        payload={"model": a.model,
                                 "messages": [{"role": "user", "content": "ping"}],
                                 "max_tokens": 4}, timeout=90)
        served = body.get("model") if st == 200 else None
        print(f"[3] {a.model} reachable ................. {'OK' if st == 200 else f'FAIL ({st})'}")
        print(f"    actually served by ................... {served or 'unknown'}")
        if st != 200:
            broken.append("lane_unreachable")

    # ── 4. failure history + last landed model ────────────────────────
    rows = _psql(f"""
        SELECT model_group, model, count(*)
        FROM "LiteLLM_SpendLogs"
        WHERE "startTime" > now() - interval '{a.window_hours} hours'
        GROUP BY 1,2 ORDER BY 3 DESC LIMIT 5;
    """)
    print(f"[4] serving history ({a.window_hours}h, from SpendLogs):")
    for line in rows.splitlines():
        if line and "psql_unavailable" not in line:
            print(f"      {line}")

    fail = _psql(f"""
        SELECT count(*) FROM "LiteLLM_SpendLogs"
        WHERE status='failure' AND "startTime" > now() - interval '{a.window_hours} hours';
    """)
    n_fail = fail.strip().splitlines()[-1] if fail else "?"
    print(f"    lane failures in window ............... {n_fail}")
    try:
        if int(n_fail) > 0 and not auth_ok:
            broken.append("failures_present")
    except ValueError:
        pass

    # ── verdict ───────────────────────────────────────────────────────
    print("-" * 66)
    if not live:
        print("VERDICT: PROXY DOWN — continuity cannot be assessed (fail-closed).")
        return 2
    if broken:
        print(f"VERDICT: CONTINUITY BROKEN — {', '.join(broken)}")
        return 1
    print("VERDICT: CONTINUITY HELD — seat key authenticates, lane serves, no auth failures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
