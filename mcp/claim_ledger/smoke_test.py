#!/usr/bin/env python3
"""
claim-ledger-mcp SMOKE TEST — real MCP client, every tool called at least once.

Seeds the ledger with claims from two REAL forged intelligence briefs on disk,
citing their REAL sha256 hashes, then reads them back through the ledger.

Run:  /opt/arifos/venv/bin/python /root/AAA/mcp/claim_ledger/smoke_test.py
"""

import asyncio
import json
import os
import sqlite3
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

ENDPOINT = "http://127.0.0.1:8791/mcp"
DB = "/root/AAA/claim_ledger/claims.db"

BRIEF_A = "2026-09-15-syed-mokhtar-bank-consolidation"
BRIEF_B = "2026-09-15-bank-muamalat-authenticity"

PDF_A = "/root/AAA/forge_work/2026-09-15-syed-mokhtar-bank-consolidation/Bank-Muamalat-Consolidation-Brief-2026-09-15.pdf"
SHA_A = "7342084b77bdace0dcd30e606e6a6ed1fd5b919221cf99ba8c82588f9d7616f0"
PDF_B = "/root/AAA/forge_work/2026-09-15-bank-muamalat-authenticity/Bank-Muamalat-Shariah-Authenticity-Report-2026-09-15.pdf"
SHA_B = "c23df37d93222f80ceca2e7bb04e96870a455c22c7ba6e11e4901b19086838a0"

# (claim_id, brief, type, claim_text, quote, locator, artifact_id, confidence)
SEED = [
    (f"{BRIEF_A}-c01", BRIEF_A, "OBS",
     "Bank Muamalat's retail funding is 12% of deposits plus investment accounts with 47% top-20 depositor concentration and 90.2% deposit funding.",
     "The real strategic driver is funding, not size. Bank Muamalat's retail funding is 12% of deposits plus investment accounts, with a 47% top-20 depositor concentration and 90.2% deposit funding.",
     "p.2 Executive Read, finding 5", "art-" + SHA_A[:16], 0.92),
    (f"{BRIEF_A}-c02", BRIEF_A, "DER",
     "MBSB Bank + Bank Muamalat = RM110.1bn versus Bank Islam's RM106.7bn: first place by RM3.4bn, or 3%.",
     "MBSB Bank (RM64.4bn) + Bank Muamalat (RM45.7bn) = RM110.1bn, versus Bank Islam's RM106.7bn — first place by RM3.4bn, or 3%.",
     "p.2 Executive Read, finding 2", "art-" + SHA_A[:16], 0.9),
    (f"{BRIEF_A}-c03", BRIEF_A, "VOID",
     "No fresh 2026 Bank Muamalat merger negotiation is verifiable in the public record.",
     "I could not verify any fresh 2026 merger negotiation in the public record. No Bursa announcement, no BNM approval notice, no adviser mandate, no 2026 news report of revived talks.",
     "p.2 Executive Read, finding 9", "art-" + SHA_A[:16], 0.99),
    (f"{BRIEF_A}-c04", BRIEF_A, "OBS",
     "MARC affirmed Bank Muamalat A+/MARC-1/Stable in August 2026 with LCR 160.3% and NSFR 108.3%.",
     "MARC affirmed A+/MARC-1/Stable in August 2026 with LCR 160.3% and NSFR 108.3%.",
     "p.2 Executive Read, finding 3", "art-" + SHA_A[:16], 0.93),
    (f"{BRIEF_A}-c05", BRIEF_A, "OBS",
     "Financing growth collapsed from 14.1% (2024) to 4.6% (2025) against a 7.9% sector average; gross impaired financing rose to 1.43% (2025) and 1.52% (1Q26).",
     "Financing growth collapsed from 14.1% (2024) to 4.6% (2025) against a 7.9% sector average, and the gross impaired financing ratio rose to 1.43% (2025) and 1.52% (1Q26), exceeding the industry for the first time in recent years, driven by ~RM100m of retail accounts routed to AKPK after the early-2025 multi-bank fraud incident.",
     "p.2 Executive Read, finding 4", "art-" + SHA_A[:16], 0.91),
    (f"{BRIEF_B}-c01", BRIEF_B, "OBS",
     "Commodity murabahah and tawarruq are reported at 'almost 90% or more' of the Islamic banking sector.",
     'Commodity murabahah and tawarruq are reported at "almost 90% or more" of the Islamic banking sector. Malaysian risk-sharing financing measures between roughly 0.36% and 0.87% on narrow definitions, or up to 10-15% on broad ones.',
     "p.2 Executive Read, finding 2", "art-" + SHA_B[:16], 0.9),
    (f"{BRIEF_B}-c02", BRIEF_B, "DER",
     "Each RM1bn converted to risk-sharing adds roughly RM3bn of RWA and, at a 15% CET1 target, about RM450m of new equity.",
     "Mushārakah and muḍārabah exposures are reported in the literature as attracting capital risk weights up to 400%, against far lower treatment for debt-based financing. Each RM1bn shifted adds roughly RM3bn of RWA and, at a 15% CET1 target, about RM450m of new equity.",
     "p.2 Executive Read, finding 7", "art-" + SHA_B[:16], 0.85),
    (f"{BRIEF_B}-c03", BRIEF_B, "OBS",
     "Home financing 33.51% and personal financing 28.6% of gross financing; home financing and Ar Rahnu both structured on tawarruq.",
     "Home financing 33.51% and personal financing 28.6% of gross financing — home financing and Ar Rahnu both structured on tawarruq. Nothing in the current mix is a genuine profit-and-loss-sharing exposure of scale.",
     "p.2 Executive Read, finding 3", "art-" + SHA_B[:16], 0.92),
    (f"{BRIEF_B}-c04", BRIEF_B, "INT",
     "Converting funding from deposit-led to investment-account-led is simultaneously the doctrinally coherent move and the commercially rational fix.",
     "Converting funding from deposit-led to investment-account-led is simultaneously the doctrinally coherent move and the commercially rational fix for the 12%-retail / 47%-top-twenty-concentration problem. Doctrine and economics converge here — and almost nowhere else.",
     "p.2 Executive Read, finding 4", "art-" + SHA_B[:16], 0.7),
    (f"{BRIEF_B}-c05", BRIEF_B, "FIQH",
     "Malaysia's Shariah Advisory Council accepts organised tawarruq and bay' al-'inah; the OIC Fiqh Academy (2003) and AAOIFI reject them.",
     "Malaysia's Shariah Advisory Council accepts organised tawarruq and bay' al-'inah; the OIC Fiqh Academy (2003) and AAOIFI reject them. Both positions are legitimate scholarly positions.",
     "p.2 Executive Read, finding 8", "art-" + SHA_B[:16], 0.95),
]

FAILURES = []
CALLED = []


async def call(session, name, args):
    CALLED.append(name)
    res = await session.call_tool(name, args)
    if getattr(res, "structuredContent", None):
        out = res.structuredContent
        if isinstance(out, dict) and set(out.keys()) == {"result"}:
            out = out["result"]
        return out
    for blk in res.content:
        if getattr(blk, "type", "") == "text":
            try:
                return json.loads(blk.text)
            except json.JSONDecodeError:
                return {"_raw": blk.text}
    return {}


def check(label, cond, detail=""):
    mark = "PASS" if cond else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail else ""))
    if not cond:
        FAILURES.append(f"{label}: {detail}")
    return cond


async def main():
    fresh = "--append" not in sys.argv
    if fresh:
        removed = []
        for p in (DB, DB + "-wal", DB + "-shm"):
            if os.path.exists(p):
                os.remove(p)
                removed.append(os.path.basename(p))
        print(f"== reset ledger for a deterministic run: removed {removed or 'nothing'}")
    else:
        print("== --append: running against the existing ledger (counts will not match)")

    async with streamablehttp_client(ENDPOINT) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print(f"== MCP session initialized against {ENDPOINT}")

            tools = await session.list_tools()
            names = sorted(t.name for t in tools.tools)
            print(f"== Tools advertised ({len(names)}): {', '.join(names)}\n")

            # ---- 1. init -------------------------------------------------
            print("== [1] claim_ledger_init")
            r = await call(session, "claim_ledger_init", {})
            check("ledger initialized", r.get("ok") is True, r.get("db_path", ""))
            check("append-only triggers active", r.get("append_only_enforced") is True,
                  f"triggers={r.get('triggers')}")
            print(f"     tables={r.get('tables')} counts={r.get('row_counts')}")

            # ---- 2. register artifacts (real hashes) ---------------------
            print("\n== [2] claim_artifact_register (declared hash vs disk)")
            ra = await call(session, "claim_artifact_register",
                            {"path": PDF_A, "sha256": SHA_A, "title":
                             "Syed Mokhtar's Bank and the Islamic Mega-Bank Question",
                             "pages": 20})
            check("brief A registered", ra.get("ok") is True, ra.get("artifact_id", ""))
            check("declared sha256 matches disk", ra.get("declared_hash_match") is True,
                  ra.get("sha256", ""))
            rb = await call(session, "claim_artifact_register",
                            {"path": PDF_B, "sha256": SHA_B, "title":
                             "From Compliance to Conviction",
                             "pages": 20})
            check("brief B registered", rb.get("ok") is True, rb.get("artifact_id", ""))
            check("declared sha256 matches disk", rb.get("declared_hash_match") is True,
                  rb.get("sha256", ""))
            # negative: wrong declared hash must be rejected
            bad = await call(session, "claim_artifact_register",
                             {"path": PDF_A, "sha256": "deadbeef" * 8})
            check("NEGATIVE wrong sha256 rejected", bad.get("ok") is False,
                  str(bad.get("error"))[:60])

            # ---- 3. record claims ----------------------------------------
            print("\n== [3] claim_record (10 real claims, 2 briefs)")
            ids = []
            for cid, brief, ctype, text, quote, loc, art, conf in SEED:
                r = await call(session, "claim_record", {
                    "claim_id": cid, "brief_id": brief, "claim_text": text,
                    "claim_type": ctype, "source_quote": quote, "locator": loc,
                    "artifact_id": art, "confidence": conf,
                    "source_ref": "forged brief on disk (see artifact path)"})
                ids.append(cid)
                if not r.get("ok"):
                    check(f"record {cid}", False, str(r.get("error")))
            check("all 10 claims recorded", len(ids) == 10)
            one = await call(session, "claim_get", {"claim_id": ids[0]})
            check("claim bound to artifact hash", bool(one.get("artifact_sha256")),
                  str(one.get("artifact_sha256"))[:24] + "...")
            # negative: bad claim_type
            badtype = await call(session, "claim_record",
                                 {"brief_id": BRIEF_A, "claim_text": "x", "claim_type": "MAYBE"})
            check("NEGATIVE invalid claim_type rejected", badtype.get("ok") is False,
                  str(badtype.get("allowed")))
            # negative: unregistered artifact
            badart = await call(session, "claim_record",
                                {"brief_id": BRIEF_A, "claim_text": "x", "artifact_id": "art-nope"})
            check("NEGATIVE unknown artifact rejected", badart.get("ok") is False)

            # ---- 4. append-only correction path (supersede) --------------
            print("\n== [4] claim_record superseding (append-only correction)")
            sup = await call(session, "claim_record", {
                "claim_id": f"{BRIEF_A}-c05r1", "brief_id": BRIEF_A, "claim_type": "OBS",
                "claim_text": "CORRECTED: financing growth 14.1% (2024) -> 4.6% (2025); GIF ratio 1.43% (2025), 1.52% (1Q26).",
                "source_quote": "Financing growth collapsed from 14.1% (2024) to 4.6% (2025)",
                "locator": "p.2 Executive Read, finding 4", "artifact_id": "art-" + SHA_A[:16],
                "supersedes_claim_id": f"{BRIEF_A}-c05"})
            check("superseding claim appended", sup.get("ok") is True, sup.get("claim_id", ""))
            got = await call(session, "claim_get", {"claim_id": f"{BRIEF_A}-c05"})
            check("original claim still intact + shows superseded_by",
                  len(got.get("superseded_by", [])) == 1,
                  got["superseded_by"][0]["claim_id"] if got.get("superseded_by") else "")

            # ---- 5. verifications ----------------------------------------
            print("\n== [5] claim_verify (varied verdicts, live artifact re-hash)")
            vplan = [(ids[0], "CONFIRMED", "source document re-read at cited page"),
                     (ids[1], "CONFIRMED", "arithmetic recomputed: 64.4+45.7=110.1 vs 106.7"),
                     (ids[2], "CONFIRMED", "public-record search returned no 2026 announcement"),
                     (ids[4], "PARTIAL", "figures present; AKPK attribution single-sourced"),
                     (ids[6], "PARTIAL", "risk-weight ceiling 400% contested in literature"),
                     (ids[8], "REFUTED", "clause read as interpretation not observation")]
            for i, (cid, verdict, method) in enumerate(vplan):
                r = await call(session, "claim_verify", {
                    "claim_id": cid, "verdict": verdict, "method": method,
                    "evidence": f"smoke-test verification {i+1}", "verifier": "i-ARIF"})
                check(f"verify {cid} -> {verdict}",
                      r.get("ok") and r.get("verdict") == verdict,
                      f"artifact_recheck={r.get('artifact_recheck')}")
                if r.get("ok"):
                    check(f"  live artifact hash matched for {cid}",
                          r.get("artifact_recheck") == "match",
                          f"live={str(r.get('live_sha256'))[:16]}...")
            badv = await call(session, "claim_verify", {"claim_id": ids[0], "verdict": "MAYBE"})
            check("NEGATIVE invalid verdict rejected", badv.get("ok") is False)

            # ---- 6. trace -------------------------------------------------
            print("\n== [6] claim_trace")
            t = await call(session, "claim_trace", {"claim_id": ids[5]})
            check("trace returned", t.get("ok") is True)
            check("trace is end-to-end traceable", t.get("traceable") is True,
                  f"disk_state={t.get('artifact', {}).get('disk_state')}")
            check("trace gap list empty", t.get("trace_gaps") == [], str(t.get("trace_gaps")))
            check("trace has chain link", len(t.get("chain", [])) >= 1,
                  f"seq={t['chain'][0]['seq'] if t.get('chain') else None}")
            print(f"     {t.get('claim_id')} | {t.get('claim_type')} | "
                  f"{t.get('latest_verdict')} | sha={str(t.get('artifact', {}).get('sha256_recorded'))[:16]}...")

            # ---- 7. list --------------------------------------------------
            print("\n== [7] claim_list")
            allc = await call(session, "claim_list", {})
            check("list returns 11 claims (10 + 1 superseding)", allc.get("count") == 11,
                  f"count={allc.get('count')}")
            la = await call(session, "claim_list", {"brief_id": BRIEF_A})
            check("filter by brief_id", la.get("count") == 6, f"count={la.get('count')}")
            lb = await call(session, "claim_list", {"claim_type": "OBS"})
            check("filter by claim_type=OBS", lb.get("count") >= 5,
                  f"count={lb.get('count')}")

            # ---- 8. stats -------------------------------------------------
            print("\n== [8] claim_ledger_stats")
            s = await call(session, "claim_ledger_stats", {})
            check("stats ok", s.get("ok") is True)
            check("by_type spans the brief vocabulary", len(s.get("by_type", {})) >= 5,
                  json.dumps(s.get("by_type")))
            check("unverified count exposed", "claims_unverified" in s,
                  f"total={s.get('claims_total')} verified={s.get('claims_verified')} "
                  f"unverified={s.get('claims_unverified')}")
            print(f"     verdicts={s.get('by_verdict')}")

            # ---- 9. export ------------------------------------------------
            print("\n== [9] claim_export_brief")
            e = await call(session, "claim_export_brief", {"brief_id": BRIEF_B})
            check("export ok", e.get("ok") is True)
            check("export has 5 claims", e.get("claim_count") == 5,
                  f"count={e.get('claim_count')}")
            check("export is itself hashable", bool(e.get("bundle_sha256")),
                  str(e.get("bundle_sha256"))[:24] + "...")
            check("every exported claim carries artifact + quote",
                  all(c.get("artifact") and c.get("source_quote") for c in e["claims"]))

            # ---- 10. chain verification -----------------------------------
            print("\n== [10] claim_ledger_verify_chain")
            v = await call(session, "claim_ledger_verify_chain", {})
            check("hash chain intact", v.get("chain_ok") is True,
                  f"length={v.get('chain_length')} broken={v.get('broken_links')}")
            check("no record/chain mismatches", v.get("record_chain_mismatches") == 0)
            check("record content matches chained payloads", v.get("payload_ok") is True,
                  f"mismatches={v.get('payload_mismatches')} checked={v.get('records_checked')}")
            check("all artifacts re-hash match on disk", v.get("artifacts_ok") is True,
                  json.dumps(v.get("artifacts")))
            check("ledger_verified", v.get("ledger_verified") is True)
            print(f"     chain_length={v.get('chain_length')} head_seq={v.get('head', {}).get('seq')} "
                  f"records_checked={v.get('records_checked')}")

            # ---- 11. out-of-band: SQLite rejects UPDATE/DELETE directly ----
            print("\n== [11] out-of-band: SQLite rejects UPDATE/DELETE directly")
            con = sqlite3.connect(DB)
            for sql, label in [
                (f"UPDATE claims SET claim_text='tampered' WHERE claim_id='{ids[0]}'", "UPDATE claims"),
                (f"DELETE FROM claims WHERE claim_id='{ids[0]}'", "DELETE claims"),
                ("UPDATE verifications SET verdict='CONFIRMED'", "UPDATE verifications"),
                ("DELETE FROM ledger_chain", "DELETE ledger_chain")]:
                try:
                    con.execute(sql)
                    con.commit()
                    check(f"DB blocks {label}", False, "mutation SUCCEEDED — not append-only")
                except sqlite3.IntegrityError as ex:
                    check(f"DB blocks {label}", "APPEND_ONLY" in str(ex), str(ex))
            con.close()

            # ---- 12. tamper detection on a copy (trigger bypassed) --------
            print("\n== [12] tamper detection: trigger bypassed on a DB copy")
            probe = "/root/AAA/claim_ledger/tamper_probe.db"
            for p in (probe, probe + "-wal", probe + "-shm"):
                if os.path.exists(p):
                    os.remove(p)
            src, dst = sqlite3.connect(DB), sqlite3.connect(probe)
            src.backup(dst); src.close(); dst.close()
            pcon = sqlite3.connect(probe)
            pcon.execute("DROP TRIGGER trg_claims_no_update")
            pcon.execute("UPDATE claims SET claim_text=?, source_quote=NULL WHERE claim_id=?",
                         ("TAMPERED: retail funding is 99% of deposits", ids[0]))
            pcon.commit()
            print(f"     silently rewrote claim_text + nulled source_quote on copy "
                  f"({os.path.basename(probe)})")
            tv = await call(session, "claim_ledger_verify_chain",
                            {"db_path": probe, "recheck_artifacts": False})
            check("tampered copy FAILS verification", tv.get("ledger_verified") is False)
            check("chain links alone still look intact (weak check would pass)",
                  tv.get("chain_ok") is True)
            check("payload cross-check catches the edit", tv.get("payload_ok") is False,
                  f"{len(tv.get('payload_mismatches', []))} mismatch(es)")
            check("tamper is attributed to the right claim",
                  any(m.get("id") == ids[0] for m in tv.get("payload_mismatches", [])),
                  json.dumps(tv.get("payload_mismatches", []))[:120])
            live = await call(session, "claim_ledger_verify_chain", {})
            check("LIVE ledger unaffected and still verifies",
                  live.get("ledger_verified") is True)
            pcon.close()
            for p in (probe, probe + "-wal", probe + "-shm"):
                if os.path.exists(p):
                    os.remove(p)
            print("     probe copy deleted; live ledger untouched")

            # ---- coverage --------------------------------------------------
            print("\n== TOOL COVERAGE")
            missing = [n for n in names if n not in set(CALLED)]
            check("every advertised tool was called", not missing, f"never called: {missing}")
            for n in names:
                print(f"     {n}: {CALLED.count(n)} call(s)")

    print("\n" + "=" * 62)
    if FAILURES:
        print(f"SMOKE TEST: FAILED ({len(FAILURES)} failures)")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    print("SMOKE TEST: ALL CHECKS PASSED")
    print("=" * 62)


if __name__ == "__main__":
    asyncio.run(main())
