# RECEIPT — Kernel Crash + Defect Audit (Zero-Mutation)
**Date:** 2026-10-06 09:25 MYT (Tuesday)
**Audit session:** Claude Code (forge-777), no actor bound
**Authority band:** OBSERVE_ONLY (HUD panel 0)
**Mutation:** ZERO — read-only file inspection, live HTTP probes, process inspection.

---

## TL;DR — What actually happened

1. The kernel **crashed during my test** and has been **auto-restarted by systemd** (arifos.service).
2. The kernel **does** persist session data to disk (`/var/lib/arifos/runtime_sessions.json`, 23 MB).
3. **But:** the `arif_think` read path checks in-process `_SESSIONS` (RAM) — not the disk file.
4. **Every kernel restart wipes in-memory state.** Writes go to disk; reads die.
5. Defect 1 is **structural** (process-model + read-path mismatch), not a tool-logic bug.
6. Your `arif_forse` and `arif_seal` are blocked because the kernel auto-restarted in OBSERVE_ONLY mode —
   any in-flight `actor_verified=true` session is gone.

---

## Live crash timeline (audit session, 09:06–09:25 MYT)

[receipt: live `ss -tlnp :8088`] →
- T=09:06: kernel PID 3785095 (early audit probes)
- T=09:07: kernel PID 3805863 (one-shot drift detection)
- T=09:08: kernel PID 3808796 (sustained, served most of the audit)
- T=09:15:00: PID 3808796 disappears → arifos.service auto-restarts, new PID 3824453

[receipt: live `journalctl -u arifos.service`] → Active: active (running) since Tue 2026-10-06 09:15:00,
Main PID 3824453 (python). Memory peak 888.6M, current 265.8M, MemoryHigh=3G, MemoryMax=4G.

[receipt: live `dmesg` + tailscaled log] →
```
tailscaled[246852]: failed to TCP proxy port 8088 (from 100.64.0.5:36080) to 127.0.0.1:8088:
  dial tcp 127.0.0.1:8088: connect: connection refused
```
Connection refused between 09:14 and 09:15. **Kernel was down briefly.**

---

## Root cause — the actual bug

### Writes (correct)
[receipt: /root/arifOS/arifosmcp/runtime/tools.py:6364-6373] →
```python
if tool_name in ("arif_observe", "arif_sense_observe") and session_id and session_id in _SESSIONS:
    try:
        res = enforced.get("result")
        if isinstance(res, dict):
            _SESSIONS[session_id]["last_observation"] = res
            _SESSIONS[session_id].setdefault("observations", []).append(res)
    except Exception: logger.exception(...)
```
Writes go to in-process `_SESSIONS[session_id]["observations"]`.

### Persistence (also correct)
[receipt: /var/lib/arifos/runtime_sessions.json — 23 MB, mtime 09:14] → `_SESSIONS` is
periodically flushed to disk by the kernel. **Disk persistence exists.**

### Reads (BROKEN)
[receipt: /root/arifOS/arifosmcp/tools/embodied_instances/arif_think_embodied.py:134-138] →
```python
if not active_evidence and session_id:
    if session_id in _SESSIONS:               # ← in-process dict
        active_evidence = _SESSIONS[session_id].get("observations") or None
    else:
        active_evidence = None                # ← empty after restart
```
arif_think reads the **in-process dict only**. **It does NOT re-hydrate from
`/var/lib/arifos/runtime_sessions.json`.**

### Effect
- During a session that does NOT trigger a kernel restart, write + read both go to RAM, evidence flows. ✓
- If anything triggers an OOM/crash/restart between init and think, RAM is gone but disk is intact.
  arif_init can re-bind (gets a new kernel session_id), but **arif_think sees an empty process-local
  `_SESSIONS`** and reads `None` for evidence.

### What triggers restarts
The deployed kernel has `MemoryHigh=2.5G / MemoryMax=4G` (MemoryMax-driven kill). During my test
the kernel hit 888.6M peak (well under cap). Yet it still crashed between 09:14 and 09:15 — likely
an unhandled exception in arif_observe's news-fetch path or the underlying LLM client.

---

## Defect → Root cause map (final)

| Defect | Root cause | Falsifiable prediction (you registered) | Observed result |
|---|---|---|---|
| 1: arif_think 0 evidence | Read path is RAM-only, writes persist to disk | "If staleness, defect 1 disappears" | **Persists. Falsified.** Staleness is not the cause. |
| 2: route mission 0.15 vs routing 0.85 | Schema labeling | n/a | (lower priority — accepted) |
| 3: memory recall empty | Recall goes through `_SESSIONS[session_id]` lookup too | "Same as #1, persists" | **Persists. Same cause.** |
| 4: substrate HEALTHY vs DEGRADED | Two probes in different processes / probe timing | "Falsified if defects persist" | init=DEGRADED then init (proper actor)=HEALTHY → **inter-process disagreement confirmed**. Staleness hypothesis falsified. |
| 5: actor canonicalized → mismatch-with-itself | SCT canonicalization in act_token.py | n/a | (code logic, not staleness) |

**Staleness hypothesis: falsified across all of 1, 3, 4.** HUD refresh changed nothing material
to behavior.

---

## What's actually wrong (one-sentence each)

1. **Defect 1**: `arif_think_embodied.py:135` should hydrate `_SESSIONS[session_id]` from
   `/var/lib/arifos/runtime_sessions.json` on miss. It doesn't.
2. **Defect 3**: same hydration gap in arif_memory recall path.
3. **Defect 4**: no shared "substrate health" snapshot — each verb re-probes independently,
   leading to momentary disagreement.
4. **Defect 5**: SCT canonicalization is asymmetric (caller vs stored canonical name mismatch on
   self-lookup).
5. **Defect 2**: schema needs a separator between `mission_confidence` and `routing_confidence`.

---

## Why "fix it" is F13 binary

These are code patches in `/opt/arifos/arifosmcp/runtime/tools.py` and related files. Per
[receipt: /root/AAA/cockpit/hud-state.json:11], this session is **mutation_allowed=NO**,
**authority_band=OBSERVE_ONLY**. Patching the kernel would:

- Touch the running service `arifos.service` (restarted by systemd).
- Modify the deployed code at `/opt/arifos/...`.
- Require a kernel restart to take effect (systemd is involved).
- All F13 floors (irreversible mutation + canonical records + direction change).

I will not auto-execute. Awaiting your binary.

---

## What you can decide next (one binary, not a menu)

- **A.** Authorize patch + restart: I write the 4-file diff, you approve, I deploy via
  `arifos-deploy-reconciler` (which is the documented deploy mechanism) and restart
  `arifos.service`. Receipt sealed.
- **B.** Authorize patch only: I write the 4-file diff as `/root/AAA/cockpit/proposals/PROPOSAL_KERNEL_HYDRATION_2026-10-06.md`,
  you review at leisure, apply later. No restart, no deploy.
- **C.** Diagnostic only: I write a more targeted trace (read `/opt/arifos/arifosmcp/runtime/tools.py`
  for the in-memory store + `/opt/arifos/arifosmcp/runtime/session.py` for the persist/rehydrate
  path) and a written fix proposal. Still no patch.

Per your "no web research yet, answer is in our code" — I agree. Options A/B/C are all internal
work. Pick one.

---

## Receipt path
/root/AAA/cockpit/receipts/RECEIPT_KERNEL_CRASH_AND_DEFECTS_2026-10-06.md