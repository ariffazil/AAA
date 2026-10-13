"""P6 negative controls at MCP level — verify the detector does the right things."""
import json, urllib.request, re
URL = "http://127.0.0.1:18420/mcp"
SID = "edacd8b294794128828a0c0f53849345"

def call(method, params):
    body = json.dumps({"jsonrpc":"2.0","id":"neg","method":method,"params":params}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type":"application/json","Accept":"application/json, text/event-stream",
        "MCP-Protocol-Version":"2025-06-18","Mcp-Session-Id": SID})
    with urllib.request.urlopen(req, timeout=8) as resp:
        b = resp.read().decode("utf-8","replace")
    m = re.search(r"^data: (.+)$", b, re.M)
    return json.loads(m.group(1))

def inner(name, claims):
    j = call("tools/call", {"name": name, "arguments": {"claims": claims}})
    res = j.get("result", {}).get("content", [])
    return json.loads(res[0]["text"])

# 1. Identical claims (same source) -> 0 contradictions (same wire).
print("TEST 1 — identical same-source claims:")
out = inner("hermes_contradiction_scan", [
    {"id":"I1","text":"Federal spending RM510b","source":"X","principal":"budget","geography":"MY","kind":"REPORTED"},
    {"id":"I2","text":"Federal spending RM510b","source":"X","principal":"budget","geography":"MY","kind":"REPORTED"},
])
print("  count:", len(out["contradictions"]))

# 2. Identical claim, different sources — same cluster false-positive guard.
print("TEST 2 — different sources of identical text (syndication):")
out = inner("hermes_contradiction_scan", [
    {"id":"S1","text":"Federal spending RM510b","source":"reuters wire 2026-10-09","principal":"budget","geography":"MY","kind":"REPORTED"},
    {"id":"S2","text":"Federal spending RM510b","source":"theedgemalaysia.com 2026-10-09","principal":"budget","geography":"MY","kind":"REPORTED"},
])
print("  count:", len(out["contradictions"]), "(reuters vs edge — both different clusters; SAME number; we DO want to flag it as verbatim copy — at most 1 source-cluster row expected, not zero)")

# 3. Different units, same wording — should not be SCOPE-flagged.
print("TEST 3 — different units:")
out = inner("hermes_contradiction_scan", [
    {"id":"U1","text":"Federal spending RM510 billion","source":"x","principal":"budget","geography":"MY","kind":"REPORTED"},
    {"id":"U2","text":"Federal revenue USD 50 billion","source":"y","principal":"budget","geography":"MY","kind":"REPORTED"},
])
scopes = [r for r in out["contradictions"] if r["class"]=="SCOPE"]
print("  count:", len(out["contradictions"]), "scope:", len(scopes))

# 4. Side-effect check: confirm detector does NOT write a canonical store row.
#    Re-call hermes_contradiction (the STORER) for a known event_id before and after.
print("TEST 4 — side-effect probe via storer:")
import sqlite3
db_path = "/root/.hermes/hermes-rasa/state.db"  # canonical candidate
def count_rows():
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM contradictions WHERE event_id LIKE 'p6-neg-%'")
        return cur.fetchone()[0]
    except Exception as e:
        return f"DB-ERR: {e}"

# Insert a sentinel row via the storer.
sentinel = call("tools/call", {"name":"hermes_contradiction", "arguments":{
    "event_id":"p6-neg-canon-test-1",
    "human_a":"A","statement_a":"x","human_b":"B","statement_b":"y"}})
# Now invoke the detector many times.
for _ in range(5):
    inner("hermes_contradiction_scan", [{"id":"D1","text":"RM10b RM10b","source":"x","principal":"budget","geography":"MY","kind":"REPORTED"}])
print("  storer-side rows after detector stress:", count_rows())
