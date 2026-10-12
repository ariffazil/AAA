#!/usr/bin/env python3
"""
migrate_cards.py — executor for forge_card_migrate skill (owner: 333-AGI).

Contract (skill spec, non-bypassable):
  F1  .bak-<ts>-pre-migration companion before every write
  F2  registry_receipt_hash NEVER fabricated — existing receipts untouched;
      only MISSING hashes are noted (not invented)
  F11 one log line per mutation: path · mutations[] · sha256-after
  F13 additive only: schemaVersion + $schema bump. No content synthesis.
      Apex-zen rich fields (jituGate/hassabisInversion/etc.) are a separate
      per-card ratified alignment workstream — NOT part of this migration.

Usage: python3 migrate_cards.py [--dry-run]
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENTS = Path("/root/AAA/agents")
TARGET_SCHEMA = "arifOS/agent-card/v2.3.0"
TARGET_VERSION = "2.3.0"
DRY = "--dry-run" in sys.argv
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

migrated, skipped = 0, 0
for card in sorted(AGENTS.glob("*/agent-card.json")):
    try:
        data = json.loads(card.read_text())
    except Exception as e:  # noqa: BLE001
        print(f"SKIP unparseable {card}: {e}")
        skipped += 1
        continue
    cur = data.get("$schema", "")
    if cur == TARGET_SCHEMA:
        skipped += 1
        continue
    if DRY:
        print(f"DRY {card}: {cur} -> {TARGET_SCHEMA}")
        migrated += 1
        continue
    bak = card.with_name(f"agent-card.json.bak-{TS}-pre-migration")
    bak.write_text(card.read_text())
    mutations = []
    if data.get("$schema") != TARGET_SCHEMA:
        data["$schema"] = TARGET_SCHEMA
        mutations.append("$schema")
    if data.get("schemaVersion") != TARGET_VERSION:
        data["schemaVersion"] = TARGET_VERSION
        mutations.append("schemaVersion")
    if not mutations:
        skipped += 1
        continue
    card.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    post = hashlib.sha256(card.read_bytes()).hexdigest()
    print(f"MIGRATED {card} · {mutations} · sha256:{post[:16]} · bak={bak.name}")
    migrated += 1

print(f"=== {migrated} migrated · {skipped} skipped/unified · dry_run={DRY} ===")
