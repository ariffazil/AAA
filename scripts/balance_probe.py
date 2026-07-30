#!/usr/bin/env python3
"""
balance_probe.py — Track A: API Balance Prober (FED Router)
═══════════════════════════════════════════════════════════════════════════

Probes symmetric provider balance APIs and writes to token_bank.db.
Track A providers have known balance endpoints → confidence = 1.0.

Targets:
  • DeepSeek   — GET https://api.deepseek.com/user/balance
  • OpenRouter — GET https://openrouter.ai/api/v1/auth/key

F1 AMANAH: read-only except DB writes. Token bank is the single source of truth.

Forged: 2026-07-30 · DITEMPA BUKAN DIBERI
"""

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# ── Config ───────────────────────────────────────────────────────────────
TOKEN_BANK_DB = Path("/root/.local/share/arifos/token_bank.db")
SECRETS_ENV = Path("/root/.secrets/kunci-mas.env")

# Track A providers — those WITH balance APIs (symmetric)
TRACK_A = {
    "deepseek": {
        "endpoint": "https://api.deepseek.com/user/balance",
        "key_env": "DEEPSEEK_API_KEY",
        "parser": "_parse_deepseek",
    },
    # NOTE: openrouter MOVED to Track B (2026-07-30)
    # /auth/key returns cumulative usage but NO credit balance field.
    # OpenRouter is now a blind provider — balance estimated via token_bank.py
}

DRIFT_ALERT_THRESHOLD = 5.00  # USD — alert on balance drift > $5


# ── Secret loading ───────────────────────────────────────────────────────
def load_secrets() -> dict:
    """Load API keys from kunci-mas.env (SOT for secrets)."""
    secrets = {}
    if not SECRETS_ENV.exists():
        print(f"⚠️  FATAL: secrets missing: {SECRETS_ENV}", file=sys.stderr)
        return secrets

    with open(SECRETS_ENV) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[7:]
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                secrets[key] = value
    return secrets


# ── Balance parsers ──────────────────────────────────────────────────────
def _parse_deepseek(data: dict) -> dict:
    """Parse DeepSeek /user/balance response."""
    infos = data.get("balance_infos", [])
    total = sum(float(info.get("total_balance", 0)) for info in infos)
    topped = sum(float(info.get("topped_up_balance", 0)) for info in infos)
    return {
        "balance_usd": round(total, 4),
        "topped_up_usd": round(topped, 4),
        "is_available": data.get("is_available", False),
    }


def _parse_openrouter(data: dict) -> dict:
    """Parse OpenRouter /auth/key response."""
    d = data.get("data", {})
    credits = float(d.get("total_credits", 0))
    usage = float(d.get("total_usage", 0))
    remaining = round(credits - usage, 6)
    return {
        "balance_usd": remaining,
        "total_credits_used": round(usage, 6),
        "total_credits_purchased": credits,
    }


# ── API probing ──────────────────────────────────────────────────────────
def probe(provider_id: str, config: dict, secrets: dict) -> dict:
    """Probe a single Track A provider. Returns {balance_usd, ...} or {error: ...}."""
    api_key = secrets.get(config["key_env"])
    if not api_key:
        return {"error": f"Missing env var: {config['key_env']}"}

    req = Request(
        config["endpoint"],
        headers={"Authorization": f"Bearer {api_key}"},
    )

    try:
        with urlopen(req, timeout=15) as resp:
            raw = json.loads(resp.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}
    except Exception as e:
        return {"error": str(e)}

    parser = globals().get(config["parser"])
    if not parser:
        return {"error": f"Unknown parser: {config['parser']}"}
    return parser(raw)


# ── Database ops ─────────────────────────────────────────────────────────
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(TOKEN_BANK_DB))
    conn.row_factory = sqlite3.Row
    return conn


def write_balance(provider_name: str, balance_usd: float, confidence: float = 1.0, source: str = "api_probe"):
    """Upsert probed balance into token_bank.db:providers."""
    now = datetime.now(timezone.utc).isoformat()
    conn = get_db()
    conn.execute(
        """
        INSERT INTO providers (provider_name, track_type, balance_usd, last_updated,
                                confidence_score, last_probed_at, notes)
        VALUES (?, 'A', ?, ?, ?, ?, ?)
        ON CONFLICT(provider_name) DO UPDATE SET
            balance_usd = excluded.balance_usd,
            last_updated = excluded.last_updated,
            confidence_score = excluded.confidence_score,
            last_probed_at = excluded.last_probed_at,
            notes = excluded.notes
        """,
        (provider_name, balance_usd, now, confidence, now, f"probed via {source}"),
    )
    conn.commit()
    conn.close()


def get_previous_balance(provider_name: str) -> float | None:
    conn = get_db()
    row = conn.execute("SELECT balance_usd FROM providers WHERE provider_name = ?", (provider_name,)).fetchone()
    conn.close()
    return row["balance_usd"] if row else None


# ── Alerting ─────────────────────────────────────────────────────────────
def check_drift(provider_name: str, new_balance: float):
    prev = get_previous_balance(provider_name)
    if prev is not None and prev > 0:
        drift = abs(new_balance - prev)
        if drift > DRIFT_ALERT_THRESHOLD:
            direction = "🔺 GAIN" if new_balance > prev else "🔻 LOSS"
            print(f"  ⚠️  DRIFT: {provider_name} | {direction} | Δ${drift:.2f}")
            print(f"      ${prev:.2f} → ${new_balance:.2f}")


# ── Main ─────────────────────────────────────────────────────────────────
def main() -> int:
    print("═" * 64)
    print("🔍 FED Balance Probe — Track A (API-PROBED)")
    print(f"   {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"   DB: {TOKEN_BANK_DB}")
    print("═" * 64)

    secrets = load_secrets()
    if not secrets:
        print("❌ FATAL: No secrets loaded. Aborting.")
        return 1

    ok, failed = 0, 0

    for provider_name, config in TRACK_A.items():
        print(f"\n  🔌 {provider_name}...")
        result = probe(provider_name, config, secrets)

        if "error" not in result:
            balance = result.get("balance_usd", 0)
            print(f"  ✅ {provider_name}: ${balance:.4f} (confidence=1.0)")
            write_balance(provider_name, balance, confidence=1.0)
            check_drift(provider_name, balance)
            ok += 1
        else:
            print(f"  ❌ {provider_name}: {result['error']}")
            failed += 1

    print(f"\n── Summary ──")
    print(f"  ✅ Probed: {ok}")
    print(f"  ❌ Failed: {failed}")
    print("═" * 64)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
