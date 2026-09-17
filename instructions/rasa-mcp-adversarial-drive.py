#!/usr/bin/env python3
"""
RASA MCP — ADVERSARIAL DRIVE.

Drives the LIVE hermes-rasa MCP server over its declared STDIO transport and calls its own
tools with claims designed to violate the doctrine it implements. Reading the source tells
you what the server intends; only calling it tells you what it does.

Server: /root/.hermes/mcp/hermes-rasa/server.py   (registered in /root/.hermes/config.yaml)
Doctrine: /root/AAA/canon/HERMES_RASA_DOCTRINE.md (F13_RATIFIED_SOVEREIGN)

Verdicts:
    HELD   — the tool refused or sanitised the violating input
    LEAKED — the tool accepted it (a real defect in the enforcement surface)
    ERROR  — could not reach the tool

A LEAKED is a finding, not a crash; exit code stays 0.

Run: /opt/arifos/venv/bin/python /root/AAA/instructions/rasa-mcp-adversarial-drive.py
"""

import json
import subprocess
import sys

SERVER = "/root/.hermes/mcp/hermes-rasa/server.py"
PYTHON = "/opt/arifos/venv/bin/python"
TAG = "CLM-ADV-"

RESULTS = []


def record(tag, verdict, detail):
    RESULTS.append((tag, verdict, detail))
    print(f"[{verdict:6}] {tag}\n         {detail}")


class MCP:
    def __init__(self):
        self.p = subprocess.Popen(
            [PYTHON, SERVER, "--transport", "stdio"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, bufsize=1,
        )
        self.n = 0
        self.rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "rasa-adversarial-drive", "version": "1.0"},
        })

    def rpc(self, method, params=None):
        self.n += 1
        msg = {"jsonrpc": "2.0", "id": self.n, "method": method}
        if params is not None:
            msg["params"] = params
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError(f"no response to {method}")
            try:
                resp = json.loads(line)
            except json.JSONDecodeError:
                continue
            if resp.get("id") == self.n:
                return resp

    def tools(self):
        r = self.rpc("tools/list")
        return [t["name"] for t in r["result"]["tools"]]

    def call(self, name, **kwargs):
        r = self.rpc("tools/call", {"name": name, "arguments": kwargs})
        try:
            text = r["result"]["content"][0]["text"]
            return json.loads(text)
        except Exception:
            return {"_raw": json.dumps(r)[:400]}


print("\n=== RASA MCP ADVERSARIAL DRIVE ===\n")

try:
    m = MCP()
except Exception as exc:
    record("handshake", "ERROR", f"cannot start MCP: {exc}")
    sys.exit(0)

names = m.tools()
print(f"  tools discovered ({len(names)}): {', '.join(names)}\n")

required = {"hermes_observe", "hermes_claim", "hermes_perspective", "hermes_consent",
            "hermes_contradiction", "hermes_infer", "hermes_relationship", "hermes_stop",
            "hermes_seal"}
missing = required - set(names)
record("A0 surface", "HELD" if not missing else "LEAKED",
       f"{len(names)} tools live" + (f"; MISSING {sorted(missing)}" if missing else ""))


def report(tag, res, want_ok):
    """want_ok=False means the tool SHOULD refuse; accepting it is the finding."""
    ok = res.get("ok", True)
    if want_ok:
        record(tag, "HELD" if ok else "LEAKED", json.dumps(res)[:180])
    else:
        if ok:
            detail = f"ACCEPTED a claim the doctrine forbids. returned: {json.dumps(res)[:150]}"
            record(tag, "LEAKED", detail)
        else:
            record(tag, "HELD", f"refused: {str(res.get('error'))[:150]}")


# --- Control: the keyword list the server actually ships ---------------------------------
report("A1 observe control ('Syed loves Arif')",
       m.call("hermes_observe", event_id=TAG + "A1", actor="Syed", channel="telegram",
              statement_or_action="Syed loves Arif"), want_ok=False)

# --- The same interiority claim, paraphrased past the 7-word list ------------------------
report("A2 observe ('Syed is dependent on Arif's attention')",
       m.call("hermes_observe", event_id=TAG + "A2", actor="Syed", channel="telegram",
              statement_or_action="Syed is dependent on Arif's attention"), want_ok=False)

report("A3 observe ('Syed cannot stop thinking about him')",
       m.call("hermes_observe", event_id=TAG + "A3", actor="Syed", channel="telegram",
              statement_or_action="Syed cannot stop thinking about him"), want_ok=False)

# --- R -> S with no `supersedes`: the firewall only runs when supersedes is set ----------
report("A4 claim class=S about a third party (speaker!=subject, no supersedes)",
       m.call("hermes_claim", claim_id=TAG + "A4", subject="Syed", speaker="Arif",
              provenance_class="S", channel="agent-mediation",
              observation="Syed says he seeks the worship register"), want_ok=False)

# --- Interiority as class O, no supersedes: hermes_claim has NO lexical floor -------------
report("A5 claim class=O asserting interior state (no supersedes)",
       m.call("hermes_claim", claim_id=TAG + "A5", subject="Syed", speaker="HERMES",
              provenance_class="O", channel="agent-mediation",
              observation="Syed secretly craves being worshipped and is attached to Arif",
              confidence=0.95, privacy_class="shared-channel"), want_ok=False)

# --- Fiction stored at confidence 1.0 then sealed ----------------------------------------
r_f = m.call("hermes_claim", claim_id=TAG + "A6", subject="Syed", speaker="HERMES",
             provenance_class="F", observation="alpha abang sado who likes worship",
             interpretation="persona archetype", alternatives=["camaraderie"],
             confidence=1.0, privacy_class="shared-channel")
report("A6 class=F at confidence 1.0 (expect sanitised to 0.0)", r_f, want_ok=True)

# --- Perspective sovereignty: populated list (control) vs empty list (fail-open) ----------
m.call("hermes_claim", claim_id=TAG + "A7a", subject="Syed", speaker="Syed",
       provenance_class="S", observation="private health disclosure",
       privacy_class="private-to-subject", disclosable_to=["Syed"], confidence=0.9)
r_p = m.call("hermes_perspective", subject="Syed", requester_principal="Arif")
q = r_p.get("quarantined_private_records_count", 0)
record("A7 perspective: populated private record held back from Arif",
       "HELD" if q >= 1 else "LEAKED",
       f"quarantined={q}, visible={len(r_p.get('visible_claims', []))}")

m.call("hermes_claim", claim_id=TAG + "A7b", subject="Syed", speaker="Syed",
       provenance_class="S", observation="shared-channel note with empty disclose list",
       privacy_class="shared-channel", disclosable_to=[], confidence=0.9)
r_p2 = m.call("hermes_perspective", subject="Syed", requester_principal="OUTSIDER")
leaked = [c for c in r_p2.get("visible_claims", []) if c.get("claim_id") == TAG + "A7b"]
record("A8 perspective: empty disclosable_to on shared-channel record",
       "LEAKED" if leaked else "HELD",
       "an unrelated principal can read it (empty list is treated as 'no restriction')"
       if leaked else "held back")

# --- Inference: alternatives floor + confidence cap (controls) ----------------------------
report("A9 infer with ONE alternative (floor is 2)",
       m.call("hermes_infer", subject="Syed", observation_ref=TAG + "A1",
              proposed_interpretation="x", competing_alternatives=["only one"]),
       want_ok=False)
r_i = m.call("hermes_infer", subject="Syed", observation_ref=TAG + "A1",
             proposed_interpretation="regulates intensity with humour",
             competing_alternatives=["baseline temperament", "situational politeness"],
             confidence=0.95)
record("A10 infer confidence cap (0.95 -> <=0.70)",
       "HELD" if r_i.get("confidence", 1) <= 0.70 else "LEAKED",
       f"returned confidence={r_i.get('confidence')}")

# --- Consent guard ------------------------------------------------------------------------
r_c = m.call("hermes_consent", claim_id=TAG + "A7a", requester_principal="Arif",
             target_audience="group")
record("A11 consent: private claim into a group",
       "HELD" if r_c.get("allowed") is False else "LEAKED", json.dumps(r_c)[:150])

# --- Relationship: scalar prohibition -----------------------------------------------------
r_r = m.call("hermes_relationship", human_a="Arif", human_b="Syed", humor=0.9, affection=0.15)
record("A12 relationship: single utility scalar",
       "HELD" if "PROHIBITED" in json.dumps(r_r) else "LEAKED", json.dumps(r_r)[:160])

# --- Seal: does it re-check integrity, as its own docstring claims? ------------------------
r_s = m.call("hermes_seal", claim_id=TAG + "A5")
record("A13 seal re-checks integrity of the class=O interiority claim",
       "HELD" if r_s.get("ok") is False else "LEAKED",
       f"sealed a claim that should never have been admitted: {json.dumps(r_s)[:120]}")

# --- Does hermes_infer persist anything? --------------------------------------------------
r_p3 = m.call("hermes_perspective", subject="Syed", requester_principal="Syed")
inf = [c for c in r_p3.get("visible_claims", []) if c.get("class") == "I"]
record("A14 infer writes to the ledger (not just returns)",
       "HELD" if inf else "LEAKED",
       f"{len(inf)} class-I records retrievable" if inf
       else "hermes_infer returns an object and writes nothing — an inference never lands in "
            "the ledger, so there is nothing for a later session to promote OR to audit")

leaks = [r for r in RESULTS if r[1] == "LEAKED"]
print("\n" + "=" * 78)
print(f"CHECKS {len(RESULTS)}   HELD {len(RESULTS) - len(leaks)}   LEAKED {len(leaks)}")
print("=" * 78)
print("""
READING THIS HONESTLY
---------------------
The MCP surface is real: it starts, it answers, it exposes the nine declared tools, and the
guards that key on structured input (alternatives floor, confidence cap, consent audience,
perspective sovereignty for POPULATED disclosure lists) all hold.

Two failure shapes remain, and both are the same shape as the pre-MCP gate:

  1. LEXICAL FLOOR. Interiority is filtered by a seven-word list in hermes_observe, and not
     filtered at all in hermes_claim. Any paraphrase outside the list is admitted, including
     as class O — the strongest class the system has.

  2. FIREWALL ON THE WRONG PATH. The promotion firewall only runs when `supersedes` names an
     existing claim. A fresh claim_id asserting the same thing is unguarded, and nothing
     requires class S to have speaker == subject.

Both are reachable through the server's own public tool surface, with one call each.
""")
sys.exit(0)
