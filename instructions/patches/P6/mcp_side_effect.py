import json, urllib.request, re, sqlite3, os
URL = "http://127.0.0.1:18420/mcp"
SID = "edacd8b294794128828a0c0f53849345"
def call(method, params):
    body = json.dumps({"jsonrpc":"2.0","id":"se","method":method,"params":params}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type":"application/json","Accept":"application/json, text/event-stream",
        "MCP-Protocol-Version":"2025-06-18","Mcp-Session-Id": SID})
    with urllib.request.urlopen(req, timeout=8) as r:
        b = r.read().decode("utf-8","replace")
    m = re.search(r"^data: (.+)$", b, re.M)
    return json.loads(m.group(1))

# Look at the actual storer DB.
db = "/root/.hermes/hermes-rasa/state.db"
if not os.path.exists(db): db = "/root/.hermes/state/rasa_mcp.sqlite3"
print("db:", db, "exists:", os.path.exists(db))

def total_rows():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM contradictions")
    return cur.fetchone()[0]

T0 = total_rows()
print("pre-scan total rows in contradictions table:", T0)
# 10 detector scans, varied inputs.
for _ in range(10):
    call("tools/call", {"name":"hermes_contradiction_scan","arguments":{"claims":[
        {"id":"X"+str(_),"text":f"RM{_+1}b vs RM{_+2}b","source":"reuters","principal":"budget","geography":"MY","kind":"REPORTED"},
        {"id":"Y"+str(_),"text":f"RM{_+3}b vs RM{_+4}b","source":"edge","principal":"budget","geography":"MY","kind":"REPORTED"},
    ]}})
T1 = total_rows()
print("post-scan total rows in contradictions table:", T1, "delta:", T1 - T0)

# Now invoke the STORER once, with a unique event_id, and verify the row count increments by exactly 1.
EVENT = f"p6-side-effect-{T1+99999}"
res_storer = call("tools/call", {"name":"hermes_contradiction","arguments":{
    "event_id":EVENT,"human_a":"A","statement_a":"x","human_b":"B","statement_b":"y"}})
print("storer result ok:", res_storer.get("result",{}).get("ok"))
T2 = total_rows()
print("post-storer total rows:", T2, "delta:", T2 - T1)

# Verify the storer row exists with the exact event_id we passed.
conn = sqlite3.connect(db); cur = conn.cursor()
cur.execute("SELECT event_id FROM contradictions WHERE event_id = ?", (EVENT,))
print("storer-write canonical-id present:", [r[0] for r in cur.fetchall()])
conn.close()
