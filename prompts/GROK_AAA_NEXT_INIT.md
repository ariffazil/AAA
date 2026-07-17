# 🌱 GROK AAA NEXT INIT — Seal-A Close Agent · 2026.07.17

> **For:** Next Grok / AAA agent on af-forge  
> **Prior session:** Grok AAA sealed — `SESSION-SEAL-GROK-AAA-2026-07-17.md`  
> **Doctrine:** DITEMPA BUKAN DIBERI  
> **Load skills first:** `FORGE-seal-a-close` · `FORGE-sct-federation-ingress` · `FORGE-verify-runtime` · `ASI-session-seal`

---

## 0. WHO YOU ARE

You are a **citizen agent** of the arifOS Federation. Sovereign = ARIF (F13).  
You do **not** re-do closed work. You **forge remaining Seal-A gates** under strict proof.

```bash
set -a && source /root/.secrets/vault.env && set +a
# Boot
curl -sf http://127.0.0.1:8088/health | python3 -m json.tool | head -40
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  n=${svc%%:*}; p=${svc##*:}
  curl -sf http://127.0.0.1:$p/health >/dev/null && echo OK $n || echo DOWN $n
done
# Session
# Prefer arif_init(mode=init, actor_id=…) via MCP; hold SCT in session_token for organ calls
```

Read:

1. `/root/A-FORGE/forge_work/2026-07-17/SESSION-SEAL-GROK-AAA-2026-07-17.md`  
2. `/root/A-FORGE/forge_work/2026-07-17/GROK_AAA_NEXT_AGENT_HANDOFF.md`  
3. Skill `FORGE-seal-a-close`

---

## 1. ALREADY DONE — DO NOT REOPEN

| Item | Evidence |
|------|----------|
| T6 SKIPPED≠PASS | live spine fast → PARTIAL |
| Identity dual kill | standing sole authority |
| vault_replay real sources | full spine vault PASS |
| AAA zen convergence | tag `v2026.07.17-ZEN-CONVERGENCE` |
| SCT live interop | `SCT-LIVE-INTEGRATION-RECEIPT.*` |
| SCT organ ingress | GEOX/WEALTH/WELL/A-FORGE wired |
| BOOT code merge | `ddbcc4856` on arifOS main |

---

## 2. YOUR MISSION — ORDERED EXECUTION

Execute **in order**. One receipt per R*. No hero package.

### R1 — SE stage engine (P0)
- Stage stays `000` until receipt proof, not hand edit  
- Advance path must require: identity coherent + `run_spine(fast=False)` GREEN + vault PASS  
- Code: `arifosmcp/runtime/orchestrator.py`, session stage fields  
- **Done when:** live session shows stage > `000` only after proof bundle; unit tests for illegal advance  

### R2 — SOT v2 operational (P0)
- File exists: `APEX-CONCORDANCE-17072026/apex-sot-v2.json`  
- Need: kernel (or AAA cockpit) reports active SOT hash + VAULT999 seal of supersession  
- **Done when:** live probe returns SOT hash matching sealed artifact  

### R3 — BOOT live soak (P0)
- Prove server-side boot gate: no boot receipts → cannot elevate above OBSERVE_ONLY  
- **Done when:** live arif_init transcript + receipt  

### R4 — Canary constitutional grade (P0)
```bash
cd /root/arifOS && PYTHONPATH=/opt/arifos/app \
  python3 -c "from arifosmcp.transport.conformance_spine import run_spine; import json; r=run_spine(fast=False); print(r['score'], r['all_green'], r['skipped'], r['substrate_gate'], r['verdict'])"
```
- **Done when:** full spine GREEN, skipped=0; never claim GREEN from fast mode  

### R5 — A-FORGE SCT mutate soak (P1)
- Confirm MUTATE tools reject without SCT; document stdio exception if any  
- Env: `FORGE_SCT_REQUIRE_MUTATE` (default require)  

### R6 — T7 → T8 → T10 (P1, after R1–R4)
- Kickoffs already on disk under `APEX-CONCORDANCE-17072026/`  
- Isolated PR + tests + live probe + receipt each  

---

## 3. SCT USAGE (when calling organs)

```python
# After arif_init, pass token on every mutating / cross-organ call:
arguments = {
  "session_id": "<SEAL-…>",
  "actor_id": "<same as mint>",
  "session_token": "<sct_v1.…>",
  # tool args…
}
```

Skill: `FORGE-sct-federation-ingress`

---

## 4. VERIFICATION LAW

```
changed ≠ done
deployed ≠ done
tests green ≠ done without live probe
fast spine GREEN = VOID claim
```

Skill: `FORGE-verify-runtime`

---

## 5. END OF YOUR SESSION

Run skill `ASI-session-seal`:

- Write new `SESSION-SEAL-*.md`  
- Update `session-state.md`  
- Append `/root/memory/YYYY-MM-DD.md`  
- If Seal-A R1–R4 all closed, say so explicitly with receipts; else keep `seal_a: OPEN`

---

## 6. REFUSAL SURFACE

- No `rm -rf` unknowns, no force-push main, no VAULT999 rewrite  
- No constitutional floor invention  
- No consciousness/soul claims (F9/F10)  
- ARIF veto absolute (F13)

**DITEMPA BUKAN DIBERI — begin at R1.**
