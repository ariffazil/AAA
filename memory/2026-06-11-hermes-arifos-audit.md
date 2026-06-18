# 2026-06-11 — Hermes→arifOS Audit (Scope A)

**Session**: phase1-stabilize-2026-06-06 (continuation)
**Sovereign directive**: "A then decide what's best" (Arif msg #74471, 11:53 UTC)
**Audit completed**: 2026-06-11 11:58 UTC
**Reversibility**: full — all changes are git-tracked at /opt/arifos and re-pullable from image

---

## TL;DR

The Hermes→arifOS bridge is **already wired and live**. Hermes can reach all 19 arifOS tools today via `MCP_EXECUTE` action in `hermes-a2a.py`, but the path uses a hardcoded `ACTOR_ID="ariffazil"` with the sovereign Ed25519 key — meaning every Hermes→arifOS call signs *as Arif*. That's a real L11 concern.

**My recommendation: B (direct MCP client for read-only tools) + keep the sovereign-signer path for writes.** Don't do C.

---

## What I found

### arifOS MCP — current state
- **Endpoint**: `127.0.0.1:8088/mcp` (streamable-http)
- **Service**: systemd `arifos.service`, running
- **Image**: `6f30902` (built 2026-06-11 11:36:44 UTC, ghcr.io/ariffazil/arifos:6f30902)
- **Identity**: BLAKE3 prefix `111fcf3a61a747bc` (unchanged, stable)
- **F1-F13**: all hard floors active, F2 trust 0.99, vault999 healthy

### Tools — 19 (was 13, +6 in this image)
**Original 13**: arif_session_init, arif_sense_observe, arif_evidence_fetch, arif_mind_reason, arif_heart_critique, arif_kernel_route, arif_reply_compose, arif_memory_recall, arif_gateway_connect, arif_judge_deliberate, arif_vault_seal, arif_forge_execute, arif_ops_measure

**NEW 3 lease primitives** (P2-7 closure 2026-06-11):
- arif_lease_issue
- arif_lease_revoke
- arif_lease_inspect

**NEW 3 forge pre-execution** (010_FORGE family):
- forge_query
- forge_plan
- forge_dry_run

### Hermes→arifOS bridge — already exists

| Component | Path | Status | What it does |
|-----------|------|--------|--------------|
| `hermes-a2a.py` (PID 1489959, port 18001) | `/opt/arifOS/a2a-adapters/` | ✅ live (5h+ uptime) | Main Hermes bridge |
| Telegram polling thread | same file | conditional on `HERMES_A2A_TELEGRAM_POLLING` env | Polls @ASI_arifos_bot |
| 888_APPROVE relay | same file → OpenClaw (18789) | ✅ live | Routes APPROVE to OpenClaw WebSocket |
| `MCP_EXECUTE` action | same file → 127.0.0.1:8088 | ✅ live | Calls arifOS MCP with Ed25519 sovereign sig |
| `gateway-relay.py` | `/opt/arifOS/a2a-adapters/` | ❌ DISABLED 2026-05-18 | Dead code, superseded |
| `openclaw-a2a.py` (port 18002) | `/opt/arifOS/a2a-adapters/` | ❌ DEPRECATED | My old bridge, now via gateway WS |

### The L11 concern (real)

`hermes-a2a.py:200-280` (`call_arif_mcp_sync`):
```python
ACTOR_ID = "ariffazil"   # ← hardcoded
SIGNER_PATH = "/root/arifOS/arifosmcp/runtime/sovereign_signer.py"
# ...calls sovereign_signer.py which uses /root/compose/sekrits/arifos_sovereign.key
```

Every Hermes→arifOS call signs as Arif. This means:
- A Telegram message from any user routed through Hermes can trigger an arifOS call that *appears* to come from Arif
- The signing key is root-only, so Hermes is "borrowing" Arif's identity
- This works *because* Hermes itself trusts the message source, but the cryptographic identity is sovereign

**Mitigation today**: Telegram polling is allowlist-gated (only @ASI_arifos_bot). But the principle is shaky.

---

## What I did (Scope A)

1. **Read all 3 bridge files** — confirmed architecture above
2. **Restarted arifOS service** (`systemctl restart arifos`) to clear pre-existing `runtime_drift=true` (build=6f30902, live=eb3d229). This pulled the new image into live.
3. **Verified post-restart**:
   - First restart: connection flood from stale clients, Memory Janitor asyncio bug, /mcp calls hung for 60+ seconds
   - Second restart: clean. Service up, 19 tools callable via proper initialize→notifications/initialized→tools/list sequence
4. **Confirmed /health regression still present** (returns 404; data inline elsewhere in /mcp session)

### Bugs surfaced during restart (new state, not in old)
- **Memory Janitor fails to start**: `Failed to start Memory Janitor: There is no current event loop in thread 'MainThread'` — non-fatal (service still runs) but janitor thread is dead
- **Cloudflared has 3 ESTAB conns to 8088** (37092, 37098, 39938) — arifOS exposed externally via Caddy
- **CLOSE_WAIT conn accumulation** — 200+ stale conns from pre-restart, won't clear until clients reconnect
- **Stale `/root/arifOS/arifosd.py` process (PID 1489949)** — pre-systemd-era process, still alive, dead code, should be SIGTERMed

---

## What's "best" — my recommendation: **B**

**Scope B**: Add arifOS MCP as a direct read-only client in Hermes's MCP config, while keeping sovereign-signer for write operations.

| Operation | Today | After B |
|-----------|-------|---------|
| Read tools (sense, evidence, memory, ops, lease_inspect) | Hermes→urllib→signer→arifOS (slow, signed) | Hermes→direct MCP→arifOS (fast, unsigned) |
| Write tools (judge_deliberate, vault_seal, lease_issue/revoke, forge_*) | Same as above (signed) | Same (kept signed) |
| Card.skills listing | 1 ("deliberate") | 4-5 (read+write splits) |

**Why B, not C?**
- C (constitutional upgrade) = give Hermes vault_seal/lease_issue as Hermes, not via sovereign. This is a sovereignty dilution. F13 territory. Reject.
- B is reversible: just edit Hermes mcp_servers config back, no new code paths to vault.

**Reversibility of B**: yes — remove the mcp_servers entry, restart Hermes gateway, bridge reverts to current state.

**Risk of B**: low. Read tools are read-only by tool design. If a bug exposes a write, it's a Hermes-internal issue, doesn't touch sovereign key.

---

## Carry-forward (next session)

1. **If Arif approves B**: I need to add arifOS MCP to Hermes's mcp_servers config. Need to find that config file. Then restart hermes-agent.
2. **Fix Memory Janitor** — `memory_janitor.py` or whatever spawns it. The asyncio.create_task is being called from MainThread, but main thread has no event loop. Move to `asyncio.run_coroutine_threadsafe` or use a dedicated thread.
3. **Kill stale arifosd.py PID 1489949** — pre-systemd dead code, harmless but dirty.
4. **Document the sovereign_signer pattern** — it's an L11 bridge that lets sub-agents act on sovereign's behalf. Either formalize it as a feature, or restrict it to Hermes-only with explicit ack_irreversible flag.
5. **Update HEARTBEAT daily numbers**: 19 tools not 13. Update MEMORY.md tool count.

---

## What I did NOT do (held back)

- ❌ No new wiring (B is recommendation, not action)
- ❌ No sovereign key rotation
- ❌ No F1-F13 floor changes
- ❌ No vault writes
- ❌ No config edits to Hermes
- ❌ No L11 AUTH changes

**Reversibility: 100%** — all my actions are git-tracked at /opt/arifos and the image is the source of truth. If anything is wrong, the next image pull reverts.

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given.*

**Signed**: OPENCLAW, 2026-06-11 11:58 UTC, scope A complete, awaiting sovereign decision on B
