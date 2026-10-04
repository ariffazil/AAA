# Federation Brain Auth-Handshake First Probe — 2026-08-12

> **Trigger:** user says "agents blocked", "tools disabled", "no agentic access",
> or any report that a federation organ/MCP endpoint is unreachable or empty —
> ESPECIALLY when the report comes from the agent's own prior reasoning or
> from a sibling subagent. Apply the same auth-first reflex as the
> `/tools/list` Accept-header lesson (SKILL.md §3.1) — every probe that
> touches the federation brain needs the correct auth BEFORE it can speak.

## TL;DR — the three protocol fixes that turned "federation dead" into "federation healthy"

1. **`GET /v1/models` returning `{data: []}` ≠ service is dead.** It almost
   always means **missing `Authorization: Bearer $LITELLM_MASTER_KEY`**. Probe
   with auth first, never without. Source: `kunci-mas.env :: LITELLM_MASTER_KEY`
   (starts `sk-lit...`).
2. **All MCP organs (`A-FORGE :7071`, `GEOX :28083`, `WEALTH :18082`, `WELL`,
   etc.) require a `Mcp-Session-Id` header from an `initialize` round-trip
   before `tools/list` / `tools/call` will work.** A bare `tools/list` returns
   `400 Bad Request: Mcp-Session-Id header is required` — that is the **MCP
   spec**, not a federation bug. (Augments SKILL.md §3.1 with the exact 3-call
   handshake recipe.)
3. **PyYAML `safe_load` succeeding on `litellm-config.yaml` ≠ litellm accepts
   the config.** Some structural mis-indents parse fine in PyYAML but crash
   litellm's parser with `AttributeError: 'NoneType' object has no attribute
   'items'`. Always validate with `litellm --config <file> --detailed_debug`
   OR by `systemctl restart litellm-federation` and watch the journal
   (`Aug 12 10:38:07 ... proxy_startup_event` line).

## §1 — What actually happened in the session (2026-08-12)

User said:
> "Can u make sure all warga AAA FI agents coder can do work. I don't want any
> agents have tool blocks or file system access deny. Give full agentic access."

Carry-forward listed 11 items (qwen-code exempt, registry entries, FI conflicts,
warga_binding, etc.) framed as "open items to close."

**My first-pass diagnosis (WRONG):** "6 broken i-arif entries with
`litellm_params: null` due to flush-left `model:` line." I regex-scanned
the file, my detection script misclassified structural noise as null entries,
and I drafted a patch script. **Did not apply it** because AGENTS-AUTONOMY
classifies production-litellm config edit as borderline T2 — I paused to
surface to F13.

**Live probe that falsified the hypothesis:**
```bash
python3 -c "import yaml; data = yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'));
print('Total entries:', len(data['model_list']));
broken = [m for m in data['model_list'] if m.get('litellm_params') is None];
print('Broken:', len(broken))"
# Total entries: 112
# Broken: 0
```

The "broken i-arif" pattern was a false positive. There were 11 i-arif blocks
(all syntactically valid) and 0 with null params.

**What was actually happening:** earlier I had called
`curl http://127.0.0.1:4011/v1/models` *without* `Authorization: Bearer ...`,
got `data: []`, and concluded "litellm broken." Wrong. The service was
healthy; I had no auth.

**Correct probe (with auth):**
```bash
source /root/.secrets/kunci-mas.env   # LITELLM_MASTER_KEY=sk-lit...7f87
curl -s http://127.0.0.1:4011/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"
# → 25 models exposed, including all 8 FI agent lanes
```

## §2 — Canonical MCP session handshake (3 calls)

For any MCP organ (A-FORGE :7071, GEOX :28083, WEALTH :18082, WELL, etc.):

```python
import json, urllib.request

url = "http://127.0.0.1:7071/mcp"  # example: A-FORGE

# Call 1 — initialize (no session header needed; server returns one)
req = urllib.request.Request(url, data=json.dumps({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2025-06-18",
               "capabilities": {},
               "clientInfo": {"name": "hermes-arif", "version": "1.0"}}
}).encode(),
headers={"Content-Type": "application/json",
         "Accept": "application/json, text/event-stream"},
method="POST")
with urllib.request.urlopen(req, timeout=10) as r:
    session_id = r.headers.get("Mcp-Session-Id")
    init_result = json.loads(r.read().decode())

# Call 2 — tools/list (with session header)
req2 = urllib.request.Request(url, data=json.dumps({
    "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
}).encode(),
headers={"Content-Type": "application/json",
         "Accept": "application/json, text/event-stream",
         "Mcp-Session-Id": session_id},
method="POST")
with urllib.request.urlopen(req2, timeout=10) as r:
    tools = json.loads(r.read().decode())["result"]["tools"]

# Call 3 — tools/call (same session header)
req3 = urllib.request.Request(url, data=json.dumps({
    "jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {"name": "tool_name", "arguments": {...}}
}).encode(),
headers={"Content-Type": "application/json",
         "Accept": "application/json, text/event-stream",
         "Mcp-Session-Id": session_id},
method="POST")
```

**Pitfall:** the 400 from a missing `Mcp-Session-Id` looks alarming but is
the spec working as designed — NOT a federation failure. Don't escalate;
just add the header. The `Mcp-Session-Id` is in the `initialize` response
**header** (not the body), so capture it from `r.headers.get("Mcp-Session-Id")`.

## §3 — litellm-federation health probe matrix

| Probe | Without auth | With auth (`Bearer $LITELLM_MASTER_KEY`) |
|---|---|---|
| `GET /health/liveliness` | 200 "I'm alive!" | 200 "I'm alive!" |
| `GET /v1/models` | **200 with `data: []` (looks dead!)** | 200 with N models |
| `POST /v1/chat/completions` | **401 Unauthorized** | 200 with response |

**The "0 models without auth" trap is the #1 false-dead reading.** Same shape
as the `/tools/list` Accept-header trap (SKILL.md §3.1a) — the probe is
broken, not the service. Fix the probe before declaring the service dead.

## §4 — litellm-federation crash pattern (the real concern)

If `/health/liveliness` returns 200 but the systemd unit is auto-restarting
every ~30s, the cause is **prisma-query-engine death** (Postgres connection
loss), not config corruption:

```bash
journalctl -u litellm-federation --since "5 minutes ago" | grep -E "(NoneType|AttributeError|prisma)"
```

- `NoneType.items` → config parse failure → litellm exits with status=3
- `prisma-query-engine ... exited` → DB death → litellm restarts gracefully
- `401 Unauthorized` from /v1/models → missing auth header (you, not the service)

**Recovery for prisma death:** the unit's `Restart=always` handles it; if not,
`systemctl restart litellm-federation` is T2 known-safe per AGENTS-AUTONOMY §7.

## §5 — End-to-end verification before declaring any agent "blocked"

The honest "is agent X really blocked?" probe sequence:

1. **Federation brain alive?**
   `curl http://127.0.0.1:4011/health/liveliness` → 200
2. **Auth works?**
   `curl http://127.0.0.1:4011/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"`
   → non-empty `data` array
3. **Specific lane reachable?**
   `POST /v1/chat/completions` with the agent's `model_name` from the
   `AGENTS_UNIFIED.yaml` registry → 200 response
4. **CLI binary present?**
   `which <agent-binary>` and `<agent-binary> --version`
5. **Config matches reality?**
   Compare `AGENTS_UNIFIED.yaml :: forge_instruments[*].model` against
   `/v1/models` output. If a model appears in the YAML but not in
   `/v1/models`, that's a real block — but **only after step 2 confirms
   auth works**.

If all 5 pass, the agent is NOT blocked. Report GREEN, not HOLD.

## §6 — Snapshot-before-touch discipline (the part I got right)

Even when my diagnosis was wrong, taking a SHA-locked snapshot of the
production yaml BEFORE any edit meant I could revert at any point. This
matches AGENTS-AUTONOMY §1 (T0/T1 doc edits require snapshot for
files > 10 KB).

```bash
SRC=/root/A-FORGE/litellm-config.yaml
BACKUP=${SRC}.pre-arif-fix-$(date -u +%Y%m%dT%H%M%SZ)
cp -p "$SRC" "$BACKUP"
sha256sum "$SRC" "$BACKUP"
# Both hashes must match after copy — if not, the copy failed.
```

**This is the discipline that kept the session safe when the diagnosis
turned out to be wrong.** Snapshot → patch → re-verify → revert if needed.
Even patches that turn out unnecessary don't damage the system.

## §7 — The meta-lesson (the one Arif was right about)

When Arif said terse-style "Aku nak agents aku boleh buat semua benda. Done",
he was signalling: **stop philosophising about F1/F13 framings, do the work
with live probes, report what you actually find.**

I pushed back twice with constitutional caveats before he had to push back
on me. That's a pattern to break:

- If the user says "fix X" or "verify X" or "make X work", **the immediate
  action is a live probe**, not a paragraph of governance preamble.
- Constitutional framing belongs in the response AFTER the probe results
  are in hand, not before.
- The 10-second veto window in AGENTS-AUTONOMY §3 / §6 exists precisely
  so the agent can proceed without further human permission within its
  tier. Use it.

**Signal-detection rule for next session:** if the user message is short
(< 15 words) and imperative ("Done.", "Fix all", "X is broken", "go"),
default to **probe → act → report**. Default to philosophy only when the
user explicitly asks "why" or "explain".

This is the same reflex as SKILL.md §3.1a ("Judge the probe, not the
service") applied to **user-signal judgment**: judge what the user actually
wants, not what you assume they need.

## §8 — What got SEALED

SESSION_RECEIPT to A-FORGE VAULT999 (`forge_vault mode=receipt`):

```
record_id: 64c3d3df-94e0-4182-a8cb-c5f85e49c71e
name: session.hermes-arif-20260812-federation-audit
verdict: FEDERATION_AUDIT_COMPLETE
delta_s: -0.21
authority: aforge-mcp (Lane B — autonomous receipt, not Lane A constitutional seal)
status: SEAL
ts: 2026-08-12T02:48:48.369Z
chain_hash: 7721294c2fdc5a0a
```

The `forge_vault` schema gotcha worth remembering: it requires
`mode + name + content (or value) + category + actor_id + session_id` —
got the schema wrong 3 times before landing. The error message
"name, category, content (or value) required for mode=receipt" is the
diagnostic.

## §9 — Pointer to the A-FORGE :7071 snapshot at session end

- 116 tools exposed via `tools/list` after proper handshake
- 25 litellm models via `/v1/models` after auth
- All 8 FI CLI agents (`opencode`, `claude-code`, `qwen-code`, `antigravity`,
  `codex`, `copilot`, `grok-build`, `kimi-code`) — `which` + `--version` ✓
- arifOS :8088: 8 canonical tools, all 13 F-floors `pass`,
  `apex_scalars {G=0.4092, C_dark=0.1246, W3=0.7439, h=0.7836, QDF=0.3582}`
- arifOS :8088 reports `deployment_drift: true` — separate amber signal,
  not addressed this session

DITEMPA BUKAN DIBERI — Probe before patch. Snapshot before touch. SEAL
after verify.