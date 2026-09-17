# Reconciliation Probes — concrete commands

Recipes for `divergent-claim-reconciliation`. Adapt paths; the shape is the asset.

## 1. Stamp your own vantage first

```bash
hostname; hostname -I | tr ' ' '\n' | grep -E '^100\.'
```

Match that against the topology SOT (e.g. `AAA/docs/MACHINE_MAP.md`) to learn which node role
this seat holds. Never assert a role from memory — read the map, then state it.

## 2. Enumerate every surface that reports the same fact

Do not stop at one. Probe each directly.

**HTTP projection (may diverge from the wire):**
```bash
curl -s http://127.0.0.1:<port>/tools
```

**MCP wire over JSON-RPC — the surface clients actually use:**
```python
import json, urllib.request
URL = "http://127.0.0.1:<port>/mcp"
H = {"Content-Type": "application/json",
     "Accept": "application/json, text/event-stream"}

def rpc(payload):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers=H, method="POST")
    return urllib.request.urlopen(req, timeout=25).read().decode()

rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
     "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                "clientInfo": {"name": "probe", "version": "1"}}})

# tools — surface A
print(json.loads(rpc({"jsonrpc": "2.0", "id": 2,
                      "method": "tools/list", "params": {}}))["result"]["tools"])
# prompts — surface B; compare its claims against tools
print(json.loads(rpc({"jsonrpc": "2.0", "id": 3,
                      "method": "prompts/list", "params": {}}))["result"]["prompts"])
```

**Reading an MCP tool result:** the payload is nested. Text lives at
`result.content[0].text` and is itself usually a JSON string:

```python
out = rpc({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
           "params": {"name": "<tool>", "arguments": {...}}})
d = json.loads(out)
inner = json.loads(d["result"]["content"][0]["text"])
```

If `inner` fails to parse, the server returned a plain string (e.g. `Unknown tool: '...'`) —
treat that string as the finding. Do **not** try `unicode_escape` on it; raw backslashes raise
`UnicodeDecodeError`.

**Source canon:** read the module that declares the fact, and note its file path.

## 3. Deployed vs checkout — hash both before blaming the server

```bash
sha256sum <checkout>/<module>.py \
          /opt/<organ>/current/venv/lib/python3.*/site-packages/<pkg>/<module>.py
```

Identical → canon is deployed; the divergence lies elsewhere (usually a *second* module
hardcoding the same fact). Different → you are reading the wrong tree.

## 4. Run a verifier in the DEPLOYED environment

Never diagnose a composite gate from its boolean. Import the verifier from the installed
package and read the per-item table:

```bash
cd /opt/<organ>/current && ./venv/bin/python - <<'PY'
import sys, json
sys.path.insert(0, "/opt/<organ>/current/venv/lib/python3.*/site-packages")
from <pkg>.runtime.<verifier> import verify_<gate>
r = verify_<gate>()
print(json.dumps(r.to_dict() if hasattr(r, "to_dict") else r, indent=1, default=str))
PY
```

Iterate the per-item dict and print every item that is not a pass — those items name the cause.

## 5. Existence check on each candidate the gate names

A verifier often probes a list of candidate paths. Test each, and test its **type**:

```bash
for p in <candidate1> <candidate2> <candidate3>; do
  if   [ -f "$p" ]; then echo "FILE   : $p"
  elif [ -d "$p" ]; then echo "DIR    : $p  (a file-open probe can never pass here)"
  else                   echo "ABSENT : $p"
  fi
done
```

Then check whether the path is archived or deleted, and whether the check's reader has a
fallback — a broad `except OSError: continue` turns every candidate into a silent negative.

## 6. Concurrent-writer check before any mutation

A divergence may be caused by another session writing while you probe.

```bash
cd <repo> && git log -6 --format='%h | %an | %ci | %s'
ls -la <repo>/.git/index.lock 2>/dev/null || echo "no lock"
find <repo> -maxdepth 2 -newermt "-10 minutes" -type f ! -path '*/.git/*' | head
```

If a registered seat is committing on the truth node, coordinate — do not race. Patch against
the deployed artifact path, never a moving checkout.
