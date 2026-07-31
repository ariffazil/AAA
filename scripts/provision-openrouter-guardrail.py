#!/usr/bin/env python3
"""Provision AAA sovereign guardrails in OpenRouter workspace via Management API.

Place at /root/AAA/scripts/provision-openrouter-guardrail.py
Run with: python3 provision-openrouter-guardrail.py
Requires OPENROUTER_MANAGEMENT_KEY in env.

Forged: 2026-07-31 by 333-AGI (Δ MIND) — previously documented but never created.
"""

import os, json, sys, requests

KEY = os.environ.get("OPENROUTER_MANAGEMENT_KEY")
if not KEY:
    print("ERROR: OPENROUTER_MANAGEMENT_KEY not set in environment.")
    print("Run: source /root/.secrets/kunci-mas.env && python3 provision-openrouter-guardrail.py")
    sys.exit(1)

BASE = "https://openrouter.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

# ── Step 1: List current keys ──
print("=" * 60)
print("STEP 1: Current workspace keys")
print("=" * 60)
r = requests.get(f"{BASE}/keys", headers=HEADERS)
if r.status_code != 200:
    print(f"FAILED: {r.status_code} {r.text[:200]}")
    sys.exit(1)

keys = r.json().get("data", [])
for k in keys:
    print(f"  {k['name']}: usage=${k.get('usage', 0):.2f} limit={k.get('limit', 'unlimited')} disabled={k['disabled']}")

# ── Step 2: Set monthly limits on each key ──
print()
print("=" * 60)
print("STEP 2: Setting monthly limits")
print("=" * 60)

for k in keys:
    name = k["name"]
    khash = k["hash"]

    # Federation key: $10/mo cap
    if "federation" in name.lower():
        limit = 10
    # Hermes key: $5/mo cap
    elif "hermes" in name.lower():
        limit = 5
    else:
        limit = 5

    r = requests.patch(f"{BASE}/keys/{khash}", headers=HEADERS, json={"limit": limit})

    if r.status_code == 200:
        print(f"  ✅ {name}: limit set to ${limit}/month")
    else:
        print(f"  ❌ {name}: {r.status_code} — {r.text[:150]}")

# ── Step 3: Create workspace guardrail ──
print()
print("=" * 60)
print("STEP 3: Creating workspace guardrail")
print("=" * 60)

GUARDRAIL = {
    "name": "aaa-sovereign-guardrail",
    "limit_usd": 50,
    "reset_interval": "daily",
    "allowed_models": [
        "z-ai/*",
        "mistralai/*",
        "x-ai/*",
        "meta-llama/*",
        "deepseek/*",
        "qwen/*",
        "xiaomi/*",
        "google/gemma-4-31b-it:free",
        "google/gemma-4-26b-a4b-it:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b:free",
    ],
    "blocked_models": ["minimax/*"],  # SHADOW-MM-001
    "content_filter_builtins": [
        {"slug": "regex-prompt-injection", "action": "block"},
        {"slug": "email", "action": "redact"},
        {"slug": "phone", "action": "redact"},
        {"slug": "ip_address", "action": "redact"},
    ],
    "zdr": True,
}

r = requests.post(f"{BASE}/guardrails", headers=HEADERS, json=GUARDRAIL)
print(f"  Status: {r.status_code}")
try:
    print(json.dumps(r.json(), indent=2))
except:
    print(r.text[:300])

# ── Step 4: Apply guardrail to federation key ──
print()
print("=" * 60)
print("STEP 4: Applying guardrail to federation key")
print("=" * 60)

for k in keys:
    if "federation" in k.get("name", "").lower():
        # Update key to use guardrail
        r = requests.patch(
            f"{BASE}/keys/{k['hash']}", headers=HEADERS, json={"guardrails": ["aaa-sovereign-guardrail"]}
        )
        print(f"  {k['name']}: {r.status_code} — {r.text[:200]}")

print()
print("=" * 60)
print("DONE. Verify on: https://openrouter.ai/settings/keys")
print("=" * 60)
