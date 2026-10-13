# RECEIPT — 2026-10-07 Stabilization & Entropy Reduction

**Actor:** kimi-code/FI-008 · **Sessions:** `SEAL-473f60865b044309` → `SEAL-d00a229113ad431a`
**Constitutional seal:** ⛔ **REFUSED** — `f13_promoted_allow_to_seal: false` under `LIMITED_MUTATE`.
This receipt is the durable record. The kernel seal is F13-gated and was not circumvented.

---

## Outcome

**COMPLETE_WITH_INCIDENT.** All work committed locally. Nothing pushed.

## Entropy removed (measured)

| # | Reduction | Evidence |
|---|---|---|
| 1 | **Deployment drift CLEARED** | `source == built == deployed` at `28e88aacc`; `drift=False` |
| 2 | arifFlow unit hardened in repo | repo was 504 B unhardened vs live 1251 B `ProtectSystem=full` — a rebuild would have shipped the weak version |
| 3 | FRAME unit + deployed MCP synced | repo ran `User=root`; live runs `User=frame` + `ProtectHome=read-only`. `make deploy` would have reverted it. Repo also lacked `frame_behavioral_drift`, which actually serves `:18086` |
| 4 | CHRON broken-commit hazard closed | `chron_cron_verify.py:92` imported `chron_gut_override.py`, which was never committed — a fresh clone would crash |
| 5 | WEALTH `DIRTY` → `CLEAN` | committed `.gitignore`, popped the stash pending since 2026-10-05, corrected `organ.yaml` pointer from a non-existent `/root/AAA/organ.yaml` to `/root/AAA/federation/organs.yaml` |
| 6 | 2 phantom A-FORGE worktrees pruned | gitdir files pointed at deleted dirs |
| 7 | VAULT999 classification corrected | 13 rows → **5 real defects**; `1180` → `1142` fixture records; removed the 4a/4f double-count (951 records counted twice) |

## Observability added

- **`layer_health.constitutional.floors_failing`** + **`floors_detail`** — `/health` reported `10/13` without naming which 3 failed. **Now live.**
- **`AAA/scripts/hab.py`** — Human Attention Burden. Refuses to print a ratio below 20 samples; reports `INSUFFICIENT_DATA`. It records a counter, it does not invent a number.

---

## INCIDENT — critical, self-inflicted

**Deploy of `4a31010d1` took `arifos.service` down for ~2 minutes.**

```
public_registry._spec_for_name -> FunctionTool.from_function
ValueError: Functions with *args are not supported as tools
```

The P2 stub registered at `_RUNTIME_HANDLERS['wealth_npv_reward']` was defined
as `(*args, **kwargs)`. FastMCP refuses to introspect `*args` into a tool, so
kernel boot died. Only 1 of the 10 P2 stubs was wired — that one was enough.

**Recovery:** unregistered the single handler (`28e88aacc`), redeployed, kernel
restored. All 8 federation ports returned 200.

**The lesson, stated plainly:** the hazard was named in `4a31010d1`'s own commit
message — *"ANY deploy today would silently ship 78 lines of unreviewed runtime
change into the 888 organ"* — and the deploy was then run anyway.

**Why it compiled and passed anyway:** `python -m py_compile` accepts `*args`. It
is not a registration test. The stub dies only when FastMCP introspects its
signature at boot. **A green syntax check is not evidence that a tool registers.**

---

## F2 traced (the question that started the health work)

`_FLOOR_DEFAULTS` is documented in-source as *"a visualizer placeholder, not a
measurement"*, built from each floor's own threshold.

| Floor | live | placeholder default | verdict |
|---|---|---|---|
| **F2 TRUTH** | 0.5 | 0.99 | **real measured value** — genuinely fails `P(truth) ≥ 0.99` |
| **F5 PEACE²** | 0.5 | 1.0 | **real measured value** |
| **F6 EMPATHY** | 0.5 | 0.7 | **real measured value** |
| F7 humility | 0.04 | **0.04** | ⚠️ **IS a placeholder — and renders PASS** |

The F2/F5/F6 failure is genuine, not a stub. The source of F2's 0.5 is **not yet
traced**.

**Secondary finding:** `floor_provenance` is already computed
(`governance_kernel` / `governance_kernel_alias` / `unmeasured_default`) but is
**not exposed on `/health`**. So F7 — a placeholder — currently passes as green and
nobody can tell. That is the SCAR-OBS-GREENWASH failure the provenance mechanism
was built to prevent, still occurring because the provenance never surfaces.

---

## Correctly *not* changed

`verify_attestation.py:76` requires `status == "healthy"` with `fail=True`. The
kernel is `degraded` because F2/F5/F6 genuinely fail, so the attestation gate
returned `WARN` and refused to seal.

**This is correct.** A deploy may succeed on a degraded baseline; a *seal* should
not. The script was left alone deliberately — it is the same shape as the bug I
did fix in `deploy-release.sh`, but here the strictness is the point.

---

## Open items

1. **F2 TRUTH 0.5 source untraced** — against a 0.99 floor. Real measurement, cause unknown.
2. **Expose `floor_provenance` on `/health`** — would make F7's placeholder-green visible.
3. **Nothing pushed.** 7 repos divergent; WEALTH `ahead 15 / behind 13`.
4. **Public site canonical URL** → `mcp.arif-fazil.com` (a 405 transport). Blocked by `file-authority.yaml`: `public/**/*.html` is `DERIVED / hand_edit: false`, no generator exists, no lease held. Proposal at `forge_work/proposals/kimi-code/mcp-canonical-url/PROPOSAL.md`.
5. **Public observatory publishes the vault ledger filesystem path.** Redaction must occur **pre-signature** or the attestation signature breaks.
6. `/root/FORGE-musyawarah-gotong` vs `-musyawawah-gotong` — divergent forks, neither canonical, no registered consumer. Sovereign decision.