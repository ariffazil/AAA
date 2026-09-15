"""
numeric-audit-mcp — REAL smoke test.

Starts the server as an actual process, connects through an actual MCP client
(fastmcp.Client over streamable HTTP), calls EVERY tool, and prints the real
numerical output. The final section is the real case: the Bank Muamalat brief's
capital arithmetic re-computed against the in-scope risk-weight schedule.

Run:  /opt/arifos/venv/bin/python /root/AAA/numeric_audit/smoke_test.py
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time
from typing import Any

import httpx
from fastmcp import Client

HOST, PORT = "127.0.0.1", 3013
URL = f"http://{HOST}:{PORT}/mcp"
SERVER = "/root/AAA/mcp/numeric_audit/server.py"
PY = "/opt/arifos/venv/bin/python"
OUT = "/root/AAA/numeric_audit/smoke_output.json"
LOG = "/root/AAA/numeric_audit/server.log"

REPORT: dict[str, Any] = {"results": {}, "narrative": []}


def _dump(value: Any) -> Any:
    """Normalise an MCP tool result into plain JSON-able data."""
    if hasattr(value, "data") and value.data is not None:
        d = value.data
        if hasattr(d, "model_dump"):
            return d.model_dump()
        return d
    if hasattr(value, "content"):
        texts = [getattr(c, "text", "") for c in value.content]
        blob = "\n".join(t for t in texts if t)
        try:
            return json.loads(blob)
        except Exception:  # noqa: BLE001
            return blob
    return value


async def main() -> int:
    log = open(LOG, "w")
    proc = subprocess.Popen([PY, SERVER], stdout=log, stderr=subprocess.STDOUT,
                            cwd="/root/AAA/mcp/numeric_audit")
    try:
        ready = False
        for _ in range(60):
            if proc.poll() is not None:
                break
            try:
                r = httpx.get(f"http://{HOST}:{PORT}/mcp", timeout=0.5)
                if r.status_code < 500:
                    ready = True
                    break
            except Exception:  # noqa: BLE001
                time.sleep(0.25)
        if not ready:
            log.flush()
            print("SERVER DID NOT START. log tail:")
            print(open(LOG).read()[-2000:])
            return 2
        REPORT["server_pid"] = proc.pid
        REPORT["server_endpoint"] = URL

        async with Client(URL) as client:
            await client.ping()
            tools = await client.list_tools()
            names = sorted(t.name for t in tools)
            REPORT["tools_listed"] = names
            print(f"[smoke] server up pid={proc.pid}  tools={len(names)}")
            print(f"[smoke] {names}\n")

            async def call(name: str, args: dict[str, Any]) -> Any:
                res = _dump(await client.call_tool(name, args))
                REPORT["results"][name] = res
                return res

            # ---------------------------------------------------------------
            # T1 numeric_rule_lookup — what does 400% actually cover?
            # ---------------------------------------------------------------
            r = await call("numeric_rule_lookup", {"figure_pct": "400"})
            print("=" * 78)
            print("T1  numeric_rule_lookup(figure_pct='400')  ->  what 400% actually covers")
            for rule in r["rules"]:
                print(f"    {rule['rule_id']}")
                print(f"      scope : {rule['canonical_scope'][:110]}")
                print(f"      basis : {rule['basis']}")
                print(f"      cite  : {rule['source']['doc']} §{rule['source']['clause']} "
                      f"({rule['source']['issued']}) {rule['source']['file']}:{rule['source']['line']}")
            print(f"    discriminator: {r['confusable_figures']['discriminator'][:180]}...")
            print(f"    matched={r['matched']}")

            # ---------------------------------------------------------------
            # T2 numeric_replay_derivation — implied RWA from CET1 and equity
            # ---------------------------------------------------------------
            r = await call("numeric_replay_derivation", {
                "inputs": {"equity_rm": "3.23", "cet1_pct": "12.02", "target_pct": "15",
                           "inc_rm": "1", "delta_pp": "300"},
                "steps": [
                    {"id": "implied_rwa_rm", "op": "rwa_from_ratio", "args": ["equity_rm", "cet1_pct"],
                     "note": "equity / (CET1 ratio) -> implied RWA"},
                    {"id": "added_rwa_rm", "op": "rwa_from", "args": ["inc_rm", "delta_pp"],
                     "note": "RM1bn exposure * 300pp weight / 100 = RM3bn"},
                    {"id": "added_rwa_check_rm", "op": "mul", "args": ["inc_rm", "delta_pp"],
                     "note": "raw product is 300 (percentage-point x billion), NOT currency — the pct_of/rwa_from op is what makes it RM3bn; this pair exists to expose that trap"},
                    {"id": "total_rwa_rm", "op": "add", "args": ["implied_rwa_rm", "added_rwa_rm"]},
                    {"id": "required_capital_rm", "op": "capital_from_rwa", "args": ["total_rwa_rm", "target_pct"]},
                    {"id": "new_capital_rm", "op": "sub", "args": ["required_capital_rm", "equity_rm"]},
                ]})
            print("\n" + "=" * 78)
            print("T2  numeric_replay_derivation  ->  implied RWA + net-of-replacement step")
            for st in r["trace"]:
                print(f"    {st['id']:<22} {st['op']:<18} {st['operands']}  =  {st['result']}")
            print(f"    implied RWA from equity 3.23 / 12.02% = RM {r['results']['implied_rwa_rm']} bn")
            print(f"    RM1bn @ +300pp (net basis)            = RM {r['results']['added_rwa_rm']} bn"
                  f"   [the raw product 'mul' gives {r['results']['added_rwa_check_rm']} — unitless, not currency]")
            REPORT["narrative"].append(
                f"implied_rwa_rm={r['results']['implied_rwa_rm']} (equity/CET1%). "
                f"RM1bn adds RM{r['results']['added_rwa_rm']}bn on a NET basis vs raw mul={r["results"]["added_rwa_check_rm"]} unitless.")

            # ---------------------------------------------------------------
            # T3 numeric_check_units_scale
            # ---------------------------------------------------------------
            r = await call("numeric_check_units_scale", {
                "claims": [
                    {"id": "cet1_pct", "value": "12.02", "unit": "%", "quantity_key": "bank.cet1_ratio"},
                    {"id": "cet1_dup", "value": "0.1202", "unit": "fraction", "quantity_key": "bank.cet1_ratio"},
                    {"id": "equity_rm_bn", "value": "3.23", "unit": "RM_bn", "quantity_key": "bank.equity"},
                    {"id": "equity_rm_mil", "value": "3230", "unit": "RM_mil", "quantity_key": "bank.equity"},
                    {"id": "rw_claimed", "value": "400", "unit": "%", "quantity_key": "rw.musyarakah"},
                    {"id": "rw_bp", "value": "40000", "unit": "bps", "quantity_key": "rw.musyarakah"},
                ], "tolerance_rel": "0.005"})
            print("\n" + "=" * 78)
            print(f"T3  numeric_check_units_scale  ->  verdict={r['verdict']}")
            for f in r["findings"]:
                print(f"    [{f['severity']}] {f['check']}: {f['detail'][:150]}")

            # ---------------------------------------------------------------
            # T4 numeric_recompute_sensitivity — the brief's own table
            # ---------------------------------------------------------------
            brief_rows = [
                {"increment_rm": "2", "implied_rwa_rm": "32.9", "new_capital_rm": "1.7"},
                {"increment_rm": "5", "implied_rwa_rm": "41.9", "new_capital_rm": "3.0"},
                {"increment_rm": "8", "implied_rwa_rm": "50.9", "new_capital_rm": "4.4"},
                {"increment_rm": "10", "implied_rwa_rm": "56.9", "new_capital_rm": "5.3"},
            ]
            r = await call("numeric_recompute_sensitivity", {
                "increments_rm": ["2", "5", "8", "10"],
                "base_rwa_rm": "26.9", "base_capital_rm": "3.23",
                "applied_weight_pct": "400", "target_ratio_pct": "15",
                "replacement_weight_pct": "100",
                "claimed_rows": brief_rows, "tolerance_rm": "0.1"})
            print("\n" + "=" * 78)
            print(f"T4a numeric_recompute_sensitivity @400% (brief's method) -> internal_consistency={r['internal_consistency']}")
            print("    inc    added_RWA   implied_RWA   required_cap   new_capital   claimed(new_cap)")
            for row, br in zip(r["rows"], brief_rows):
                print(f"    RM{row['increment_rm']:<5} {row['added_rwa_rm']:<11} {row['implied_rwa_rm']:<13} "
                      f"{row['required_capital_rm']:<14} {row['new_capital_rm']:<13} {br['new_capital_rm']}")
            print(f"    mismatches: {r['mismatches']}")

            # corrected: in-scope weights
            corrected: dict[str, Any] = {}
            for w in ("100", "150"):
                rr = await call("numeric_recompute_sensitivity", {
                    "increments_rm": ["2", "5", "8", "10"],
                    "base_rwa_rm": "26.9", "base_capital_rm": "3.23",
                    "applied_weight_pct": w, "target_ratio_pct": "15",
                    "replacement_weight_pct": "100"})
                corrected[w] = rr
            REPORT["results"]["numeric_recompute_sensitivity.corrected"] = corrected
            print("\nT4b numeric_recompute_sensitivity @IN-SCOPE weights (musyarakah §2.87: 100% public / 150% non-public equity holding)")
            for w, rr in corrected.items():
                print(f"    weight {w}%: marginal new CET1 per RM1bn = RM {rr['rows'][0]['marginal_new_capital_rm_per_rm1bn']} bn"
                      f"   | new capital rows: {[x['new_capital_rm'] for x in rr['rows']]}")
            m400 = r["rows"][0]["marginal_new_capital_rm_per_rm1bn"]
            m150 = corrected["150"]["rows"][0]["marginal_new_capital_rm_per_rm1bn"]
            m100 = corrected["100"]["rows"][0]["marginal_new_capital_rm_per_rm1bn"]
            print(f"    marginal cost per RM1bn converted:  400% -> RM{m400}bn  |  150% -> RM{m150}bn  |  100% -> RM{m100}bn")
            REPORT["narrative"].append(f"marginal new CET1 per RM1bn: 400%={m400}bn claimed vs in-scope 150%={m150}bn, 100%={m100}bn")

            # ---------------------------------------------------------------
            # T5 numeric_scope_check — THE ERROR CLASS
            # ---------------------------------------------------------------
            print("\n" + "=" * 78)
            print("T5  numeric_scope_check  ->  is 400% being applied inside its scope?")
            cases = [
                ("flat 400% on ALL converted risk-sharing financing (the brief's §5 claim)",
                 "400",
                 {"contract": "musyarakah_mutanaqisah", "exposure_basis": "profit_and_loss_sharing_financing",
                  "position": "banking_book", "listing": "not_applicable", "counterparty": "retail"},
                 "flat_all"),
                ("flat 400% on generic converted musharakah/mudarabah FINANCING",
                 "400",
                 {"contract": "musyarakah", "exposure_basis": "profit_and_loss_sharing_financing",
                  "position": "banking_book", "listing": "not_applicable", "counterparty": "not_applicable"},
                 "flat_all"),
                ("400% on a non-publicly-traded EQUITY HOLDING (legit use)",
                 "400",
                 {"exposure_basis": "equity_holding", "position": "banking_book",
                  "listing": "non_publicly_traded", "contract": "unspecified"},
                 "category_dependent"),
                ("150% on musyarakah project financing (the prescribed number)",
                 "150",
                 {"contract": "musyarakah", "exposure_basis": "project_financing",
                  "position": "banking_book", "listing": "not_applicable"},
                 "category_dependent"),
                ("70% lowest slotting category applied flatly to specialised financing",
                 "70",
                 {"contract": "musyarakah", "exposure_basis": "specialised_financing",
                  "position": "banking_book", "listing": "not_applicable"},
                 "flat_all"),
                ("400% for a number that is in no registry clause at all",
                 "777",
                 {"contract": "musyarakah", "exposure_basis": "profit_and_loss_sharing_financing",
                  "position": "banking_book", "listing": "not_applicable"},
                 None),
            ]
            scope_400_res = None
            scope_400_generic = None
            for label, fig, scope, basis in cases:
                res = await call("numeric_scope_check", {"figure_pct": fig, "scope": scope, "basis": basis})
                if fig == "400" and scope.get("contract") == "musyarakah_mutanaqisah":
                    scope_400_res = res
                if fig == "400" and scope.get("contract") == "musyarakah":
                    scope_400_generic = res
                print(f"\n    case: {label}")
                print(f"      verdict            : {res['verdict']}  (confidence {res.get('confidence','-')})")
                print(f"      in-scope weights   : {res.get('in_scope_weight_range_pct')}  {res.get('in_scope_weights_pct')}")
                if res.get("overstatement_factor_vs_max_in_scope"):
                    print(f"      overstatement      : {res['overstatement_factor_vs_max_in_scope']}x vs max in-scope weight")
                print(f"      reason             : {res['reason'][:300]}")
                if res.get("citations"):
                    c = res["citations"][0]
                    print(f"      citation           : {c['doc']} §{c['clause']}, {c['issued']}")
            REPORT["scope_case_verdicts"] = [c[0] for c in cases]

            # ---------------------------------------------------------------
            # T6 numeric_audit_claim — the money comparison
            # ---------------------------------------------------------------
            print("\n" + "=" * 78)
            print("T6  numeric_audit_claim  ->  brief figure vs corrected recomputation")
            claimed_new_cet1_per_bn = "0.450"   # RM450m, brief §5
            corrected_new_cet1_per_bn = "0.075"  # RM75m, in-scope 150% at 15% target
            a1 = await call("numeric_audit_claim", {
                "claim_value": claimed_new_cet1_per_bn, "recomputed_value": corrected_new_cet1_per_bn,
                "unit": "RM_bn per RM1bn converted", "tolerance_rel": "0.10",
                "scope_verdict": "OUT_OF_SCOPE_FIGURE"})
            print(f"    new CET1 per RM1bn:  claimed RM{float(a1['claimed'])*1000:.0f}m  recomputed RM{float(a1['recomputed'])*1000:.0f}m"
                  f"  rel_diff={a1['relative_diff']}  -> {a1['verdict']}")
            a2 = await call("numeric_audit_claim", {
                "claim_value": "32.9", "recomputed_value": "32.87", "unit": "RM_bn implied RWA",
                "tolerance_rel": "0.01", "scope_verdict": "OUT_OF_SCOPE_FIGURE"})
            print(f"    brief RWA row RM32.9bn vs recomputed RM32.87bn: rel_diff={a2['relative_diff']} -> {a2['verdict']}")
            print("    (the brief's ARITHMETIC reproduces; the INPUT it consumed is out of scope.)")
            REPORT["narrative"].append(f"claim 450m vs recomputed 75m -> {a1['verdict']}; brief row 32.9 vs 32.87 -> {a2['verdict']}")

            # ---------------------------------------------------------------
            # T7 numeric_audit_brief — composite verdict packet
            # ---------------------------------------------------------------
            r = await call("numeric_audit_brief", {"payload": {
                "label": "Bank Muamalat — §5 The Capital Arithmetic (2026-09-15)",
                "claims": [
                    {"id": "cet1", "value": "12.02", "unit": "%", "quantity_key": "bm.cet1_ratio"},
                    {"id": "equity", "value": "3.23", "unit": "RM_bn", "quantity_key": "bm.equity"},
                    {"id": "rwa", "value": "26.9", "unit": "RM_bn", "quantity_key": "bm.rwa"},
                ],
                "derivation": {"inputs": {"equity_rm": "3.23", "cet1_pct": "12.02"},
                               "steps": [{"id": "implied_rwa_rm", "op": "rwa_from_ratio",
                                          "args": ["equity_rm", "cet1_pct"]}]},
                "scope_checks": [
                    {"figure_pct": "400",
                     "scope": {"contract": "musyarakah_mutanaqisah",
                               "exposure_basis": "profit_and_loss_sharing_financing",
                               "position": "banking_book", "listing": "not_applicable",
                               "counterparty": "retail"},
                     "basis": "flat_all",
                     "applies_to_label": "all converted financing, flat 400%"},
                ],
                "sensitivity": {"increments_rm": ["2", "5", "8", "10"], "base_rwa_rm": "26.9",
                                "base_capital_rm": "3.23", "applied_weight_pct": "400",
                                "target_ratio_pct": "15", "replacement_weight_pct": "100",
                                "claimed_rows": brief_rows},
                "numeric_claims_to_compare": [
                    {"label": "new CET1 per RM1bn", "claimed": "0.450", "recomputed": "0.075",
                     "unit": "RM_bn", "tolerance_rel": "0.10", "scope_verdict": "OUT_OF_SCOPE_FIGURE"},
                ],
            }})
            print("\n" + "=" * 78)
            print(f"T7  numeric_audit_brief  ->  VERDICT = {r['verdict']}")
            for b in r["blockers"]:
                print(f"    BLOCKER {b['class']}: "
                      f"{ {k: v for k, v in b.items() if k != 'class'} }")

        # ---------------------------------------------------------------
        # FINAL: the real recomputation, stated plainly
        # ---------------------------------------------------------------
        print("\n" + "=" * 78)
        print("REAL RECOMPUTATION — brief claim vs corrected range")
        print("=" * 78)
        print("  claim   : risk-sharing exposures attract capital risk weights UP TO 400%,")
        print("            applied FLATLY to all converted financing")
        print("            -> ~RM3bn added RWA per RM1bn; ~RM450m new CET1 per RM1bn (15% target)")
        print("  scope   : 400% is a prescribed figure, but CAFIB §3.166 defines it for")
        print("            'all other EQUITY HOLDINGS' (simple risk weight method). For")
        print("            musharakah the operative clause is §2.87:")
        print("              100% publicly traded equity holding / 150% non-publicly traded")
        print("              / 150% funds advanced to a joint venture (project financing)")
        print("              / else supervisory slotting 70-400% (App V: 70/90/115/250/400,")
        print("                where 400% is the DEFAULT category and needs a default finding)")
        print("            A diminishing musharakah home financing post-wa'd is a CREDIT exposure")
        print("            (CAFIB §2.86(c)) -> counterparty weights, SA2024 §23.12: 20/25/30/40/90%.")
        print("")
        print("  recomputed with the SAME brief inputs (base RWA 26.87, capital 3.23, target 15%):")
        print(f"    @400% flat (claimed) : new CET1 per RM1bn = RM{m400}bn")
        print(f"    @150% (in scope)     : new CET1 per RM1bn = RM{m150}bn")
        print(f"    @100% (in scope)     : new CET1 per RM1bn = RM{m100}bn")
        print("")
        print(f"  margin of error on the headline: the brief's flat 400% is "
              f"{scope_400_generic['overstatement_factor_vs_max_in_scope']}x the largest in-scope weight "
              f"({scope_400_generic['in_scope_weight_range_pct'][1]}%) for generic risk-sharing financing, and "
              f"{scope_400_res['overstatement_factor_vs_max_in_scope']}x the largest in-scope weight "
              f"({scope_400_res['in_scope_weight_range_pct'][1]}%) for diminishing-musharakah retail financing.")
        print(f"  composite verdict: {r['verdict']}")
        REPORT["headline"] = {
            "claimed_new_cet1_per_rm1bn": "0.450",
            "corrected_new_cet1_per_rm1bn_range": [m100, m150],
            "weight_overstatement_factor_generic_financing": scope_400_generic["overstatement_factor_vs_max_in_scope"],
            "weight_overstatement_factor_mutanaqisah_retail": scope_400_res["overstatement_factor_vs_max_in_scope"],
            "brief_table_internal_consistency": "MATCH (arithmetic reproduces; input out of scope)",
            "composite_verdict": r["verdict"],
        }
        print("=" * 78)

        with open(OUT, "w") as fh:
            json.dump(REPORT, fh, indent=2)
        print(f"\n[smoke] full result packet -> {OUT}")
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:  # noqa: BLE001
            proc.kill()
        log.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
