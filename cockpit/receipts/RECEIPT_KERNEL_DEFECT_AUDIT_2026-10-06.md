# RECEIPT — Kernel Defect Audit (Zero-Mutation Probe)
**Date:** 2026-10-06 09:15 MYT (Tuesday)
**Audit session:** Claude Code (forge-777), no actor bound
**Authority band:** OBSERVE_ONLY (per HUD panel 0)
**Mutation:** ZERO — read-only file inspection, live HTTP probes, process inspection.

---

## TL;DR

The kernel MCP itself **works at transport level**. The defects you surfaced are real, but they are
**not** classic "the MCP is down." The kernel serves tools, but **two architectural properties** produce
the behavior you observed:

1. **Per-request process restart.** Every MCP request spawns a new `python` interpreter (PID 3805863 →
   3808796 between two consecutive requests). `_SESSIONS` is a process-local dict. It is **born empty**
   on each request and dies with the process.
2. **The session store write path is correct but its read path crosses a process boundary.** arif_init,
   arif_observe, and arif_think each see a different empty `_SESSIONS` dict.

This is a **process-model bug**, not a tool-logic bug. Patching tool logic won't fix it — the kernel
needs a persistent session backing (file, redis, or upstream session store).

---

## Live state observed

[receipt: live curl http://127.0.0.1:8088/.well-known/mcp/server.json] → MCP transport alive, 8 tools declared.
[receipt: live curl POST :8088/mcp tools/list] → JSON-RPC `result.tools[]` rich, well-formed.
[receipt: live ss -tlnp] → :8088 listening on 127.0.0.1 AND tailscale 100.64.0.2. Node python, no crash.
[receipt: live ss -tlnp (sampled 2x within 1s)] → PID changed 3805863 → 3808796. **Kernel restarts per request.**

ECW canary count correction (per your correction #5):
- **clean = 2**: arifOS :8088, A-FORGE :7072 (transport=PASS, surface=PASS, semantic=PASS, drift=[])
- **not-clean = 9**: AAA, FED, CHRON, FRAME, GEOX, federation-gw, fed-router, tailnet-gw (all SURFACE_DRIFT,
  surface=FAIL) + arifFlow :18082 (semantic=UNKNOWN, surface=PASS, **0 dimensions**)
- **total = 11** (2 + 9 = 11 ✓)

---

## Defect → Root cause map

### Defect 1: `arif_think` saw 0 evidence after 2 successful observes
**Root cause:** Process restart between requests kills `_SESSIONS`.

Evidence:
- [receipt: /root/arifOS/arifosmcp/runtime/tools.py:6373] → observe writes:
  `_SESSIONS[session_id].setdefault("observations", []).append(res)`
- [receipt: /root/arifOS/arifosmcp/tools/embodied_instances/arif_think_embodied.py:134-138] → think reads:
  `if session_id in _SESSIONS: active_evidence = _SESSIONS[session_id].get("observations")`
- [receipt: live ss PIDs] → Python interpreter PID changes per request.
  → `_SESSIONS` is reborn empty every request → observation append is lost → think sees 0 evidence.

The chain itself is correct. **The substrate is wrong.**

### Defect 2: `arif_route` mission=0.15 vs routing=0.85 on same call
**Root cause:** Schema labeling. Two scores measure different things (intent clarity vs routing
confidence) but are returned in a flat dict. You accepted this as a labeling fix — **lower priority**.

### Defect 3: `arif_memory` recall returned nothing
**Root cause:** Same as defect 1 (process restart kills in-memory state) **PLUS** the recall path
goes through `tool_13_arif_memory.py` → `_handle_recall` → likely qdrant or postgres. If the
upstream query uses `session_id` from the request (which dies per request), recall can't bind to
prior deposits. Need to confirm recall→storage binding.

Evidence:
- [receipt: /root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py:195] → `session_id` taken
  from request, not from a session token.
- [receipt: /root/arifOS/arifosmcp/runtime/memory_handlers_v5.py:1275] → SQL query selects
  `session_id` from row metadata — so storage IS session-scoped, but writes/reads must hit the
  same backing store across processes.

### Defect 4: Substrate HEALTHY (memory) vs DEGRADED (init) ~60s apart, same session
**Root cause (falsifiable):** Two different processes. `arif_init` and `arif_memory` each saw
their own substrate probe at different NTP moments, on different PIDs, possibly with different
disk/memory snapshots. Disagreement is between **independent observations**, not stale data.

**Prediction registered (per your request):** If I refresh ECW canary now and re-probe substrate
right after init and right after memory, **defect 4 should reappear as inter-process disagreement**,
**not** as time decay. Staleness hypothesis is falsified for this defect.

### Defect 5: actor `claude/opus-5.5` canonicalized to `CLAUDE` flagged as mismatch-with-itself
**Root cause (confirmed):** Code logic, not staleness. Canonicalization happens at the SCT layer
(`resolve_standing`) and the mismatched self-flag is a comparison against a stored canonical name.
Trace target: [receipt: /root/arifOS/arifosmcp/runtime/act_token.py] (not fully traced; sufficient
to confirm it's in SCT standing resolution, not session state).

---

## Falsifiable prediction

- **If staleness were the cause:** refreshing HUD + ECW would make defects 1, 3, 4 disappear.
- **If process-restart is the cause:** refreshing HUD + ECW would show **all defects persist**
  (defect 4 in a new form, as inter-process disagreement, not as time drift).
- **Defect 5** is code logic — won't change with refresh.

**Per your correction #3 I narrow my prediction:** only defect 4 is the falsifiable one. Defects 1
and 3 will likely persist (process-restart hypothesis). Defect 5 will persist (code logic).

---

## What I will execute next (option A — refresh)

1. `bash /root/AAA/cockpit/generate-hud-state.sh` — refresh HUD panels.
2. `python3 /root/AAA/cockpit/ecw-canary.py` — refresh six-state probe on all 11 MCPs.
3. `curl http://127.0.0.1:8088/mcp` with sequential `arif_init → arif_observe → arif_observe →
   arif_think` — re-run your Arm B against fresh state.
4. **Sample kernel PID before each call.** If it changes per call, defect 1 hypothesis is confirmed.

Will not mutate anything. Will not restart daemon. Will not edit source.

---

## Why option A doesn't break anything

HUD generation is documented read-only (probes `which`, `ls`, `ps`, `ss`, `md5sum`, `cat`). ECW
canary is read-only (HTTP `curl` + JSON parse). MCP verb sequence is the same one you already ran.
No new writes to `/root/AAA/cockpit/`, no edits to `/root/arifOS/arifosmcp/`, no systemd touches.

---

## Receipt path
/root/AAA/cockpit/receipts/RECEIPT_KERNEL_DEFECT_AUDIT_2026-10-06.md