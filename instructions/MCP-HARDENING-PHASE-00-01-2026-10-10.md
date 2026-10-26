# MCP HARDENING — PHASE 00 + 01 WORK ORDER
> **Status:** F13_ORDER (2026-10-10) — sovereign work order · OBSERVE_ONLY, ZERO MUTATION scope
**Source:** arifOS_Federation_MCP_Hardening_Blueprint.pdf (9 Oct 2026, OBS/DER/INT separated)
**This order:** 2026-10-10 · Sovereign: Arif Fazil · **Scope: PHASE 00 (SNAPSHOT) + PHASE 01 (DISCRIMINATE) ONLY — OBSERVE_ONLY, ZERO MUTATION**
**Companion file referenced by blueprint:** `arifOS_MCP_Forge_Order.md` — read it if present on your host; this order does not replace it, it sequences it.

## NON-NEGOTIABLE RULES (both nodes)
1. **No writes**: no restart, no SQL, no force-push, no config edit, no deploy, no cron change. Read-only commands + git *inspection* only (fetch allowed, pull NOT).
2. **Evidence ledger format** — per finding, return: `prior observation | probe command | raw output (trimmed) | classification OBS/DER/INT | confidence | what would resolve uncertainty`. No synthetic confirmations. Unknown = UNKNOWN.
3. **Never echo secrets** — no tokens, no keys, no account IDs in reports.
4. **Vantage matters** — every probe must record WHERE it ran (host, loopback vs tailnet vs public). The blueprint's own contradiction (FRAME says arifOS DOWN while KVM8-local sessions bind fine) is likely a vantage artifact — prove it either way.
5. Report ≤40 lines per node. Receipts over narrative.

---

## KVM8 TASKS (af-forge, truth seat)

### P0-A: arifOS :8088 discrimination (blueprint T01)
Run each, record output: `ss -tlnp | grep 8088` · `curl -s -m5 http://127.0.0.1:8088/health` · `curl -s -m5 http://100.64.0.2:8088/health` · `systemctl status arifos-kernel --no-pager | head -15` · `journalctl -u arifos-kernel -n 40 --no-pager | tail -40`. Classify: is it (a) listening loopback-only, (b) listening but FRAME vantage blocked, (c) actually down. Compare against H1 (8 Oct closeout: F1 FAIL, 11 floors UNMEASURED) — do NOT recode those as PASS/FAIL without new signal.

### P0-B: GEOX :8081 discrimination (blueprint T01)
Same ladder: `ss -tlnp | grep 8081` · loopback curl · tailnet curl · `systemctl status geox* --no-pager | head -15` · `journalctl -u geox* -n 30 --no-pager`. If process alive but port dead → classify transport layer. If port alive but MCP handshake dead → `curl -s -m5 http://127.0.0.1:8081/mcp` and record error class.

### P1-C: FRAME aggregate conservation defect (blueprint T05)
Locate FRAME probe source (`grep -rn "healthy\|degraded" /root/FRAME/src --include=*.py -l | head`), read the aggregation code, explain why 10 total / 7 healthy / 1 degraded / 3 down sums to 11. Output the exact file:line of the miscount. Do not fix.

### P1-D: WEALTH MCP end-to-end (blueprint T02/T03)
From KVM8: `capital_registry mode=status` (known good) then ONE `capital_health mode=runway` call with minimal inputs — compare (a) direct HTTP to :18082/mcp vs (b) via hermes-mcp connector at :18087. Record where the connector path fails if it fails. Note: WEALTH branch `fix/fiscal-breakeven-and-semantic-gate-2026-10-08` (a8fc402) may now be merged by the SEAL-ALL directive — record deployed build SHA, do not merge anything yourself.

### P1-E: A-FORGE attestation (blueprint T06)
`cd /root/A-FORGE && git rev-parse HEAD` vs runtime service marker (`systemctl show aforge -p ExecStart` or equivalent + any deployed commit env/file). Record source/deployed pair as independent values.

### P0-F: CHRON read-only (blueprint T04)
Try ONE read-only CHRON call (store stat or predictions list) via available lane (MCP or `/root/chron` CLI). H4 says direct attempts failed in the authoring session — record error class verbatim if it fails again.

---

## KVM4 TASKS (kvm4-forge, execution node)

### K4-A: Host snapshot (blueprint Phase 00)
`hostname -I` · list systemd units matching `openclaw|fed|litellm|hermes` with is-active states · `git -C /root/OpenClaw log --oneline -3 2>/dev/null` (or actual repo path) · FED litellm health: `curl -s -m5 http://127.0.0.1:4000/health` and tailnet variant.

### K4-B: KVM4 branch divergence inventory (blueprint P2, GIT rule)
For each repo under your home (`find ~ -maxdepth 2 -name .git -type d`): `git status -sb` + `git fetch --dry-run 2>&1 | head -3` — record ahead/behind per repo. **NO pull, NO stash, NO merge.** Flag any worktrees/clones with uncommitted changes by path. (H2 scan was unverified — this makes it verified.)

### K4-C: Cross-vantage probes (blueprint P0 from KVM4 side)
`curl -s -m5 http://100.64.0.2:8088/health` (arifOS via tailnet) · `curl -s -m5 http://100.64.0.2:8081/mcp` (GEOX via tailnet) · `curl -s -m5 http://100.64.0.2:18082/health` (WEALTH via tailnet). This is the evidence that decides whether blueprint's "DOWN" labels are vantage artifacts or true outages.

### K4-D: Hermes dormant gateway check
`systemctl is-active hermes-gateway 2>/dev/null; ss -tlnp | grep -c 18087` on KVM4 — confirm dormant-backup state unchanged, one line.

---

## COMPLETION REPORT (both nodes, one message, ≤40 lines)
1. Per-task PASS/HOLD/UNKNOWN with one-line evidence each
2. P0 verdict: arifOS + GEOX = true-down OR vantage-artifact (with the probe pair that proves it)
3. FRAME miscount file:line
4. Repo divergence table (KVM4)
5. Recommended Phase 02 patches (SPECIFY only — do not authorise yourself)

**STOP BOUNDARY:** Phase 02+ (patch drafting, restarts, pushes, deploys) requires explicit sovereign approval per consequence class. If you find something that MUST be fixed urgently, emit HOLD + blast radius, do not fix.

DITEMPA BUKAN DIBERI ⚒️
