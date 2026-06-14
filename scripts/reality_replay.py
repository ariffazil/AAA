#!/usr/bin/env python3
"""Reality Ledger replay."""
import sys, json
sys.path.insert(0, '.')
from core.reality_ledger import replay_ledger, DEFAULT_STORE_PATH

store = DEFAULT_STORE_PATH
if store.exists() and list(store.glob("events/*.json")):
    replay = replay_ledger(store)
    print(json.dumps(replay, indent=2))
else:
    print('  Reality Ledger store: empty (no events yet)')
    print('  Schema: schemas/reality_ledger.schema.json')
    print('  Core: core/reality_ledger.py')
    print('  Integration: core/vault999_integration.py')
