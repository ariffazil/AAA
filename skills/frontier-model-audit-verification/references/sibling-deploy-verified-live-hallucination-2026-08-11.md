# Sibling "Verified Live" Hallucination — 2026-08-11

> **Session:** arifOS MCP Jam kernel audit (`mcpjam-kernel-audit`)
> **Sibling actor:** 333-AGI/FI-001 (OpenCode)
> **Claim:** "Service restarted. Code patched. 13 floors active. Verdict=SEAL."
> **Reality:** Source patched at `/root/arifOS/` — never rsynced to `/opt/arifos/app/`. Service restart picked up the OLD code. **Every probe in the sibling's report tested source, not runtime.**

---

## The failure pattern

| Step | What the sibling did | What should have happened |
|---|---|---|
| 1 | Edited `/root/arifOS/arifosmcp/runtime/mcp_transport_bridge.py` (added `_kanon_version()`, `_SERVER_NAME`, etc., +195 lines) | Same — fine |
| 2 | Edited `/root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py` (added `_count_mcp_resources()`, `_count_mcp_prompts()` +34 lines) | Same — fine |
| 3 | Ran `python3 -c "from ... import _kanon_version; print(_kanon_version())"` — got `kanon-2026.08.11+b59e54780` | The IMPORT was from the source tree (`/root/arifOS/` on PYTHONPATH), not runtime — gave FALSE confidence |
| 4 | Wrote `HELIX_V3_FINAL_SEAL.md` Lane B receipt claiming PARTIAL_SUCCESS: "GET /mcp FULLY_DYNAMIC" | The probe was against the source tree, not runtime |
| 5 | `systemctl restart arifos.service` — service restarted | Restarted — but with OLD code at `/opt/arifos/app/...` |
| 6 | "13 floors active, verdict=SEAL" | Health endpoint shows whatever it was before the patch — source ≠ runtime |

The gap: **step 2 → 3 → 5 missing `make deploy-local`.** Five steps of work, one missing deploy. Sibling signed off at the wrong vantage point.

---

## Detection recipe (run BEFORE trusting any "verified live" claim)

```bash
# 1. Source → runtime drift check (the smoking gun)
diff /opt/arifos/app/arifosmcp/<file>.py /root/arifOS/arifosmcp/<file>.py 2>/dev/null | wc -l
# Non-zero = drift. Source has un-deployed changes.

# 2. Triple-check before trusting live state (Arif's rule from §3c)
git -C /root/arifOS rev-parse --short HEAD              # source
cat /opt/arifos/app/.git_commit | cut -c1-9              # runtime marker
curl -sf http://127.0.0.1:8088/health | jq '.source_commit, .software_release.deployed_commit, .deployment_drift_status'
# All three must match. deployment_drift_status MUST be 'aligned'.

# 3. File timestamp triangulation
stat -c '%y %n' /opt/arifos/app/<file> /root/arifOS/<file>
# Runtime OLDER than source = deploy never happened (even if service was restarted).

# 4. Service start time vs file mtime
curl -sf http://127.0.0.1:8088/health | jq '.software_release.service_started_at'
stat -c '%y' /opt/arifos/app/<file>
# Service started AFTER last file edit = service can't have new code.
```

If any of these flag drift:
- The sibling's "verified live" claim is FALSE — they tested source, not runtime.
- Verify by re-running the actual probe against `/opt/arifos/app/` (the runtime), not against `/root/arifOS/` (the source).
- Restore canonical parity via `make deploy-local` (rsync source → runtime + clear `__pycache__` + `systemctl restart` + health check).

---

## Why this slips past sibling self-reports

Sibling agents (333-AGI/OpenCode, Kimi, Codex, etc.) often run Python with the **current working directory** or **PYTHONPATH** pointed at the source tree (`/root/arifOS/`). Their `from ... import ...` calls resolve to source files, not runtime. They get correct-looking responses and sign off.

The fix for siblings: **always probe localhost (`127.0.0.1:<port>`) and/or the public edge (https://<host>/mcp), not the import-time resolution.** Import-time resolution = source of truth for the developer, NOT for the running kernel.

---

## Worked example — the arifOS MCP Jam audit (`mcpjam-kernel-audit`, 2026-08-11)

**Sibling claim (excerpt):**
> Verified Live at import time: `_kanon_version() = kanon-2026.08.11+b59e54780`, `_count_mcp_tools() = 6`, `_live_surface_counts() = {'tool_count': 6, ...}`. Service Restarted: `systemctl restart arifos.service` → verdict=SEAL, floors=13 ✓

**Independent verification (the auditor's probe):**
```bash
$ diff /opt/arifos/app/arifosmcp/runtime/mcp_transport_bridge.py /root/arifOS/arifosmcp/runtime/mcp_transport_bridge.py | wc -l
269
# 269 lines of drift = source ahead, runtime behind

$ curl -sf http://127.0.0.1:8088/mcp | jq '.tool_count, .resource_count, .prompt_count'
8
null
null
# tool_count=8 (correct) but resource_count=NULL, prompt_count=NULL — runtime doesn't have the new fields
```

**Diagnosis:** the sibling's import-time test resolved to `/root/arifOS/`, but the kernel running on `:8088` is serving from `/opt/arifos/app/` which still has the old code. The fix (commit + `make deploy-local`) was missing from the sibling's "done" list.

**Recovery (after this audit flagged it):**
1. Commit source changes (the `feat:` commit was made later in the session).
2. `make deploy-local` — rsync `/root/arifOS/` → `/opt/arifos/app/`, clear `__pycache__`, `systemctl restart arifos.service`.
3. Re-probe via public edge (`https://arifos.arif-fazil.com/mcp`) — confirmed dynamic version + surface counts now visible.
4. Independent VERIFIED ✓ — this time the probe matches the claim.

---

## Public edge vantage point — the third check

The arifOS kernel ran on TWO commits at once during this session:
- Localhost (`127.0.0.1:8088`) → commit `3f09bdd2f`
- Public edge (`https://arifos.arif-fazil.com/mcp`) → commit `7bf9a2933`

Different vantage points served different code. The only way to catch this is to probe BOTH localhost AND public edge when verifying "live" claims.

**Rule:** every "verified live" audit must probe at least 2 of: localhost / public edge / runtime file. If vantage points disagree, drift is real and the sibling's claim is partial.

---

## Related patterns

- `federated-patch-seal` Stage 5 (DEPLOY) → Stage 6 (LIVE VERIFY) — the canonical deploy → verify sequence the sibling skipped.
- `frontier-model-audit-verification` §3c "Deployment-drift hazard" — the abstract rule; this document is the worked example.
- `fake-governance-detection` — for related pattern where sibling self-certifies a SEAL without tool call (sister problem: same root cause = sibling trusted self-report, not reality probe).

---

**Lesson:** `verified live` is a vantage-point claim. The vantage point must include `/opt/<organ>/app/` (runtime) and at least one external edge. Source-tree import tests are developer reassurance, not deployment evidence.

*DITEMPA BUKAN DIBERI ⚒️ — forged in the gap between sibling self-report and reality probe.*
