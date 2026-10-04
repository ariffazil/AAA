# arifOS Kernel Contradiction Map — 2026-08-06

Read-only recon of the live kernel after Arif said "The issue is there is some contradictions in the kernel. Go map it and stabilize the kernel." He then explicitly capped the scope: **no new laws, no new files, just stabilize.** Recon report saved to `/root/HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md`.

## Live runtime truth (from `:8088/health`)

```
status: degraded
deployment_drift_status: drift_detected
release_name: v2026.08.01 | git_commit: 4d2f51a (matches source)
tools_loaded: 8 | canonical_tools_loaded: 8 | tools_registry_size: 62 | total_declared_tools: 48
runtime_floors: {F1:0.5, F2:1.0, F3:0.93, F4:0.778, F5:1.0, F6:1.0, F7:0.04, F8:0.8, F9:0.0, L10:1.0, L11:1.0, L12:0.425, L13:1.0}
execution_readiness: held
final_authority: ARIF | authority_ceiling: SOVEREIGN
ml_floors_enabled: false | ml_method: heuristic
provider_status: primary=sea_lion (healthy), ollama_configured=false, deterministic_fallback_available=true
last_seal_timestamp: null
governance.laws_hard_active: [L01, L02, L04, L07, L09, L10, L11, L12, L13]
```

## Contradictions

### C1 — Floor ID encoding: `F#` vs `L##` everywhere (HIGH)
- GENESIS canon `/root/arifOS/GENESIS/FLOOR_TABLE.json`: `F1`–`F13`.
- `arifosmcp/constitutional_map.py:46-67`: `class Law(StrEnum)` with `L01`–`L13`.
- `arifosmcp/runtime/law.py:178-191`: `LAW_DESCRIPTIONS` keyed `L01`–`L13`.
- `runtime/tools.py`: mixed literals — count showed L01=44, F1=10, L13=15, F13=10.
- `/health` `runtime_floors`: `{F1..F9, L10..L13}` — two encodings in ONE dict.
- `tools/judge.py:8421`: `_identity_floors = {"L11", "F11", "L13", "F13"}` — an accommodation, not a unification.
- Gate at `runtime/tools.py:8522` accepts `("L01","L02","F1","F2")` as equivalent.

### C2 — `.bak` files in production tree (MEDIUM)
`/opt/arifos/app/arifosmcp/tools/judge.py.bak-20260804-194717` and `tools/session.py.bak.20260801-072815` sit beside live files. `diff -q` confirms judge.py differs from its .bak. A rollback via `cp *.bak *.py` would bypass git history.

### C3 — `F9=0.0` indistinguishable from "never measured" (MEDIUM)
`execution_readiness=held` with no diagnostic saying WHICH floor (F7=0.04 / F9=0.0 / F12=0.425) caused it. 0.0 could be a real zero-pass or a broken collector. The judge has a "fail-soft: a broken collector must NEVER crash the judge" pattern at judge.py:2801 — so a broken collector yields a silent 0.

### C4 — Deployment drift false positive (LOW-MEDIUM)
`drift_detected` but `git_commit` of deployed == source. `diff -rq /root/arifOS/arifosmcp /opt/arifos/app/arifosmcp` shows drift is `__pycache__/*.pyc` (build artifacts, py312 vs py313) + `VAULT999/harness_breaches.jsonl` (live data). Cache drift and code drift are reported identically.

### C5 — Three `arif_judge` entry points (HIGH)
- `runtime/tools.py:23696`: `"arif_judge": arif_judge_facade` (docstring: "uses kernel facade in tools/judge.py").
- `runtime/tools.py:17255`: `_arif_judge_deliberate`.
- `runtime/tools.py:18393`: `_arif_judge_deliberate_tool`.
- `tools/judge.py:1023`: `async def arif_judge` (docstring "888_JUDGE v3").
- Plus the `.bak` = a fourth interpretation. The judge is the most constitutional instrument and it is three things at once.

### C6 — `last_seal_timestamp: null` (LOW)
VAULT999 chain verifies, but `/health` shows no seal since service start (14:25 UTC). Either no seal happened or the field isn't wired.

## Stabilization candidates (risk-ranked, none executed)

| ID | Patch | Time | Risk |
|---|---|---|---|
| SC5 | Move `.bak` files out of production tree (→ `/var/lib/arifos/backups/` or git history) | 5 min | zero |
| SC3 | Wire `last_seal_timestamp` from last VAULT999 entry to `/health` | 10 min | zero |
| SC4 | `0.0` → `null` + `reason: unmeasured` when a floor has no signal this epoch | 30 min | low |
| SC6 | Distinguish cache drift (pyc, VAULT data) from code drift (.py) in `deployment_drift_status` | 1 hr | low |
| SC2 | Judge consolidation: pick ONE of facade / deliberate / judge.py; delete others + `.bak` | half day | medium |
| SC1 | Floor ID unification to `F1-F13` across Law enum, law.py, tools.py, judge.py, /health | full day | HIGHEST blast — do last |

Suggested order: SC5 → SC3 → SC4 → SC6 → SC2 → SC1. Arif's doctrine: one problem, one patch, one day — never bundle.

## The meta-lesson

The system passes its own checks (health/SOT/VAULT999) but cannot honestly answer: how many floors (F vs L keys)? which floor held execution (no diagnostic)? which judge is canonical (3 impls)? This is the RSI dialogue's "recursive self-certainty at the reporting layer" — the constitution is grounded, the constitutional REPORTING is not. The fix class is: make the kernel honest about itself, not smarter.
