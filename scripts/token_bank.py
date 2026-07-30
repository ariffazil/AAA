#!/usr/bin/env python3
"""
token_bank.py — Track B: Shadow Ledger for Blind Providers (FED Router)
═══════════════════════════════════════════════════════════════════════════

Stateful shadow ledger for asymmetric/blind providers (MuleRouter, TokenRouter,
Bailian, MiMo). These have NO balance API — balances are estimated by tracking
tokens in/out and deducting cost from a known starting balance.

Math:
  balance_new = balance_old - cost_deducted
  confidence_new = max(0.30, confidence_old - 0.01)

Cost model:
  Reads pricing from /root/AAA/registries/models/pricing_tables.json
  cost = (tokens_in × input_price + tokens_out × output_price) / 1,000,000

Modes:
  ingest  — record a token usage event and deduct from balance
  topup   — manual top-up (reset confidence to 1.0)
  status  — print current balances

Forged: 2026-07-30 · F1 AMANAH: all mutations logged to shadow_ledger.
DITEMPA BUKAN DIBERI
"""

import json, sqlite3, sys, argparse
from datetime import datetime, timezone
from pathlib import Path

TOKEN_BANK_DB = Path("/root/.local/share/arifos/token_bank.db")
PRICING_TABLE = Path("/root/AAA/registries/models/pricing_tables.json")
CONFIDENCE_DECAY = 0.01
CONFIDENCE_FLOOR  = 0.30

def get_db():
    conn = sqlite3.connect(str(TOKEN_BANK_DB))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_provider(conn, name):
    row = conn.execute(
        "SELECT * FROM providers WHERE provider_name = ? AND track_type = 'B'",
        (name,)).fetchone()
    return dict(row) if row else None

def load_pricing():
    if not PRICING_TABLE.exists(): return {}
    with open(PRICING_TABLE) as f: return json.load(f)

def compute_cost(provider_name, model_id, tokens_in, tokens_out):
    pricing = load_pricing()
    pp = pricing.get(provider_name, {})
    if model_id and model_id in pp:
        rates = pp[model_id]
    elif "default" in pp:
        rates = pp["default"]
    else:
        rates = {"input_per_1M": 0.50, "output_per_1M": 1.50}
    pi, po = rates.get("input_per_1M", 0.50), rates.get("output_per_1M", 1.50)
    ci = (tokens_in  / 1_000_000) * pi
    co = (tokens_out / 1_000_000) * po
    return round(ci + co, 6), {"pi": pi, "po": po, "ci": round(ci,6), "co": round(co,6)}

def cmd_ingest(provider_name, tokens_in, tokens_out, model_id=None, notes=""):
    conn = get_db()
    p = get_provider(conn, provider_name)
    if not p:
        print(f"NO PROVIDER: {provider_name}"); conn.close(); return 1
    cost, bd = compute_cost(provider_name, model_id, tokens_in, tokens_out)
    ob, oc = p["balance_usd"] or 0.0, p["confidence_score"] or 0.85
    nb = round(ob - cost, 6)
    nc = round(max(CONFIDENCE_FLOOR, oc - CONFIDENCE_DECAY), 2)
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO shadow_ledger (provider_id,tokens_in,tokens_out,cost_deducted,confidence_before,confidence_after,timestamp,model_id,notes) VALUES (?,?,?,?,?,?,?,?,?)",
        (p["id"], tokens_in, tokens_out, cost, oc, nc, now, model_id, notes))
    conn.execute(
        "UPDATE providers SET balance_usd=?, confidence_score=?, last_updated=? WHERE id=?",
        (nb, nc, now, p["id"]))
    conn.commit(); conn.close()
    print(f"  {provider_name}: ${ob:.6f} -> ${nb:.6f}  (-${cost:.6f})")
    print(f"  {tokens_in:,} in / {tokens_out:,} out  |  conf {oc:.2f} -> {nc:.2f}")
    if model_id: print(f"  model: {model_id}  |  ${bd['pi']}/${bd['po']} per 1M")
    return 0

def cmd_topup(provider_name, amount):
    conn = get_db()
    p = get_provider(conn, provider_name)
    if not p:
        print(f"NO PROVIDER: {provider_name}"); conn.close(); return 1
    ob = p["balance_usd"] or 0.0
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "UPDATE providers SET balance_usd=?, confidence_score=1.0, last_updated=?, notes=? WHERE id=?",
        (amount, now, f"Manual top-up {now}", p["id"]))
    conn.commit(); conn.close()
    print(f"  {provider_name}: ${ob:.6f} -> ${amount:.2f} (conf=1.0)")
    return 0

def cmd_status(json_output=False):
    conn = get_db()
    rows = conn.execute(
        "SELECT provider_name, track_type, balance_usd, confidence_score, last_updated, last_probed_at FROM providers ORDER BY track_type, provider_name").fetchall()
    if json_output:
        print(json.dumps([dict(r) for r in rows], indent=2, default=str))
    else:
        print(f"{'Provider':<25s} {'T':<1s} {'Balance':>10s} {'Conf':>6s} {'Last Updated'}")
        print("-" * 78)
        for r in rows:
            b = r["balance_usd"] or 0.0; c = r["confidence_score"] or 0.0
            ts = (r["last_updated"] or "")[:19]
            print(f"{r['provider_name']:<25s} {r['track_type']:<1s} ${b:>9.4f} {c:>5.2f}  {ts}")
    conn.close()

def main():
    p = argparse.ArgumentParser(description="token_bank.py — Track B Shadow Ledger")
    sp = p.add_subparsers(dest="mode")
    ig = sp.add_parser("ingest"); ig.add_argument("provider"); ig.add_argument("tokens_in", type=int); ig.add_argument("tokens_out", type=int); ig.add_argument("--model","-m",default=None); ig.add_argument("--notes","-n",default="")
    tp = sp.add_parser("topup"); tp.add_argument("provider"); tp.add_argument("amount", type=float)
    st = sp.add_parser("status"); st.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.mode == "ingest": return cmd_ingest(a.provider, a.tokens_in, a.tokens_out, a.model, a.notes)
    elif a.mode == "topup": return cmd_topup(a.provider, a.amount)
    elif a.mode == "status": cmd_status(a.json); return 0
    else: p.print_help(); return 1

if __name__ == "__main__":
    sys.exit(main() or 0)
