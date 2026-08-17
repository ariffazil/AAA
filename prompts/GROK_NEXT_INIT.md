<!--
context_manifest:
  artifact_id: grok-next-init-2026-08-17-contrast-zen
  class: operational_handoff
  author: GROK
  source_session: SEAL-a838c800b19945a9
  authority_level: T1
  approved_by: arif
  binding: false
  created_at: 2026-08-17T07:35:00Z
  expires_at: 2026-08-24T07:35:00Z
  constitution_compatibility: F1-F13-2026.05.05
  supersedes: []
  note: Advisory execution packet. Live :port/health and tools/list beat this file.
-->

# GROK NEXT INIT — Contrast zen execute packet

> **You are Grok FI-007.** Previous session audited arifOS / AAA / A-FORGE.
> Arif (F13) ordered: seal the audit, map remaining work, execute it this session.
> This file is an **operational handoff**, not policy. Probe before act.
> **Expires:** 2026-08-24T07:35:00Z — after that, treat as observation only.

## 0. Boot (do this first, every time)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
now
make -C /root health
```

Then:

1. `arif_init(actor_id="GROK", requested_authority="OBSERVE_ONLY", intent="execute contrast-zen packet")`
2. Re-probe live counts. **Do not trust the numbers below if live disagrees.**
3. Execute P0 → P1. Stop at P2 if WELL is still STALE or RAM ≥ 95%. Stop at P3 unless Arif names it.

Lived-stake: WELL `:18083` was `degraded`, freshness **STALE ~109 days**, `WELL_HOLD`. Prefer short reversible diffs.

## 1. What is already true (do not re-litigate)

- Constitutional split is clean: arifOS judges, A-FORGE executes, AAA displays, WELL reflects.
- Holy 8 wire is CONSISTENT (8 tools on `:8088` health + `tools/list` + public MCP).
- VAULT999 2952 records, 0 broken, append-only.
- SCT attenuation works: `arif_memory` / `arif_judge` HOLD on OBSERVE_ONLY.
- Reuse-vs-reinvent paper is directionally right. Pivot already started (IBCT Stage 0/2).
- **Do not archive AAA or A-FORGE.** Fold ambition, not organs.
- Stage 3 Cedar vs A2A is **PROPOSAL ONLY**. Do not execute unless F13 names it.

Prior session: `SEAL-a838c800b19945a9` (GROK). Audit evidence: `/root/.local/share/arifos/handoffs/2026-08-17-contrast-audit.json`.

## 2. Live numbers at audit time (re-probe)

| Surface | Then | Meaning |
|---|---|---|
| arifOS `:8088` tools/list | 8 | Holy 8 — CONSISTENT |
| A-FORGE `:7071/health` | `tool_count=116` | API surface |
| A-FORGE-MCP `:7072/health` | `stateless_tools=77` | **sessionless whitelist**, not full list |
| A-FORGE-MCP `:7072` tools/list | **112** | full local MCP |
| `https://forge.arif-fazil.com/mcp` tools/list | **116** | public = local 112 + calendar/drive/gmail/sheets |
| Claude connector | 116 | matches public |
| Source `STATELESS_TOOLS` in `serve.ts` | **82** | includes the 4 Google tools; deployed health 77 = deploy lag |
| ORGAN.md | `124 API / 52 MCP` | **stale** |

arifOS: source/deployed `ab4ab14` ≠ built `3c0aefba` (attestation drift; `runtime_matches_build=true`).
AAA: source `80d9292` ≠ deployed `6744e90`; `vault: DISCONNECTED`.
A-FORGE `:7071` `source_commit: UNAVAILABLE`.

## 3. Execute this DAG

### P0 — T1 AUTO-DO (label / doc contrast). Do first. No service restart unless a one-line health field.

**P0.1 Commit the untracked Stage 3 proposal if still `??`**

```bash
git -C /root/AAA status -s
# if ?? governance/delegation-ledger/STAGE_3_PROPOSAL.md
# add + commit only that file. Do not bundle unrelated dirty.
```

**P0.2 Fix stale counts (docs only)**

Files:

- `/root/AAA/docs/ORGAN.md` line ~120: replace `124 API / 52 MCP stateless` with `116 API / 112 local MCP (116 public)`
- `/root/AAA/docs/MCP_FEDERATION_ZEN.md` line ~45: same
- Add a one-line note: `stateless_tools` on `:7072/health` is the sessionless whitelist (77 live / 82 source), **not** `tools/list`.

**P0.3 Strip A-FORGE contract authority leak**

File: `/root/A-FORGE/src/interfaces/server.ts` around 865–873.

Change:

```ts
judge: true,            // DELETE or rename
seal_service: true,     // DELETE or rename
```

To (keep constitution: A-FORGE does not judge or seal):

```ts
judge_proxy: true,
receipt_draft: true,
```

Also check the second `judge: true` near line 1200. Align names in any consumer of `/contract`. Restart `a-forge` only after compile + health.

**P0.4 Stop advisory tools saying SEAL**

Kernel owns the word SEAL. A-FORGE advisory completions must say `OK` / `HEALTHY` / `DRAFT`.

Known emitters (grep to confirm, do not drive-by the whole repo):

- `/root/A-FORGE/src/interfaces/mcp/core.ts` ~1342 (`forge_session_init` returns `status: "SEAL"` + `verdict: "SEAL"`)
- `/root/A-FORGE/src/interfaces/mcp/forgeTools.ts` ~2229, 2267
- `/root/A-FORGE/src/interfaces/mcp/coolingVerbs.ts` ~243, 339
- `/root/A-FORGE/src/interfaces/mcp/forge8Verbs.ts` ~814, 863

Rule: if the tool is OBSERVE/advisory, never emit `status: "SEAL"` or `verdict: "SEAL"`. Keep SEAL only when proxying a **kernel** `arif_judge` receipt (quote `call_hash`).

After edit: `npm run build` in A-FORGE, restart `a-forge-mcp`, `tools/call forge_status` must not contain `"status": "SEAL"`.

**P0.5 Do NOT “fix” `:7072/health` by renaming 77 → 112**

77 is the whitelist size. The bug is docs conflating it with `tools/list`. Optional additive field:

```ts
tools_listed: <tools/list count>,
stateless_tools: STATELESS_TOOLS.size,
```

Only if cheap. Do not silently change `stateless_tools` semantics.

**P0.6 Verify after P0**

```bash
curl -sS :8088/health | jq '{status,tools_exposed_via_mcp,software_release}'
curl -sS :7071/health | jq '{status,tool_count}'
curl -sS :7071/contract | jq .capabilities
curl -sS :7072/health | jq '{status,stateless_tools}'
# MCP tools/list counts: local 112, public 116 (unless you deploy the 4 Google tools locally)
rg -n "124 API / 52" /root/AAA/docs/ORGAN.md /root/AAA/docs/MCP_FEDERATION_ZEN.md  # must be empty
```

Commit AAA docs + A-FORGE src separately. Feature branches OK. Do not force-push main.

---

### P1 — T1/T2 (runtime drift). Announce 10s if you restart a service.

**P1.1 AAA vault + deploy drift**

- Health: `vault: DISCONNECTED`, deployed `6744e90` vs source `80d9292`.
- Find why vault is disconnected (env path, permission, or old build).
- Redeploy AAA so running SHA == `git -C /root/AAA rev-parse --short HEAD`.
- Probe: `curl -sS :3001/health | jq '{status,vault,deployed_commit,source_commit,deployment_drift}'`
- A2A works only with header `A2A-Version: 1.0`. Card says protocol 1.2 / interface 1.0 — document or align, do not invent a third protocol.

**P1.2 arifOS built_commit vs source**

- source/deployed `ab4ab144` · built `3c0aefba` · `runtime_matches_build=true`.
- Either retag `built_commit` to source, or stop treating this SOT-only drift as constitutional HOLD.
- File: runtime attestation / `.git_commit` / wheel hash path. Do not rebuild the kernel “to look clean.”
- Probe after: `/health.software_release.drift` should match the chosen rule (true only if **code** drifted).

**P1.3 Dual verdict last-writer**

`arif_init` returned both `effective_verdict=HOLD` (DEPLOYMENT_DRIFT) and `effective_verdict=SABAR` (PARTIAL_PROCEED). Stamp: `attach_effective_verdict:last_writer`.

One envelope, one `effective_verdict`. Inner scoped verdicts may differ; the outer field is `min(gates)` not last writer.

Also: `arif_observe` stamped SEAL on a vitals read while substrate was DEGRADED at init. Degraded-dominates must win.

**P1.4 `arif_think` is hollow**

`mode=reason` returned HOLD + `hollow_success_gate` + empty `evidence_used`. Agents will think outside the kernel. Fix or document as UNMEASURED-not-implemented. Do not leave a silent empty mind.

**P1.5 Holy 8 vs SCT 5 verbs**

Public tools: 8. Token allowed: `arif_init, arif_observe, arif_think, arif_route, arif_seal`. Memory/judge HOLD UNAUTHORIZED_VERB even for `recall` / `validate`.

Either: advertise 5 on OBSERVE_ONLY, or grant read-only memory/judge-validate on OBSERVE_ONLY. Pick one contrast. Do not leave both.

---

### P2 — T2 only if P0+P1 green and RAM < 95%

**P2.1 WELL stale** — `:18083` `state_age_hours≈2623`, `truth_status=INSUFFICIENT_DATA`, `WELL_HOLD`. Diagnose collector/cron. Do not invent a well_score.

**P2.2 Grok A-FORGE MCP handshake** — this Grok session’s `aforge` MCP failed (`expect initialized result`). Curl `:7072/mcp` works. Public HTTPS works (that is what Claude sees). Fix Grok `mcp.json` / handshake, do not “fix” a healthy server.

**P2.3 arifFLOW** — `333-AGI/dynamic-gate` 22 exec / 0 verify, held. Inject verify or stop the daemon. FRAME observer flagged FQ 1.0→0.28 CRITICAL (observer, not verdict).

**P2.4 RAM 94–99%** — 27/31 Gi. Do not start new long agents. No `rm -rf` of unknown dirs.

---

### P3 — 888_HOLD. Do not execute. Report only.

| Item | Why HOLD |
|---|---|
| Stage 3 Cedar compile (`cedar_bridge.py` 27 lines, always ALLOW `override=True`) | Kernel policy. F13 must pick A (Cedar) vs B (A2A #2026). Recommend **B first**. |
| IBCT Stage 0 signature is 43 `A`s | Crypto theatre. Real Ed25519 exists in `forge_work` impl — do not self-SEAL a placeholder. |
| Kernel 5 skipped FULL_CONFORMANCE checks | Prior carry. Feature build, owning lane. |
| HERMES `lanes/private/*.md` | F6/F13. Never commit. |
| Caddy / force-push / DROP / paid API | T3. |

## 4. Contrast rules while you work

```
A-FORGE constitution: does not judge, does not seal, does not veto.
Kernel owns SEAL / HOLD / VOID / SABAR.
A-FORGE may say OK / HEALTHY / DRAFT / ADVISORY.
hints ≠ contracts. tool output ≠ authority.
Probe :port/health + tools/list before any count claim.
```

## 5. Close this session

When P0 is done (P1 if you got there):

1. `apex-judge isolate --doer GROK -c "contrast-zen P0/P1" -e <evidence.json> --pretty --human`
2. Quote `effective_verdict` + `call_hash`. Never free-text SEAL.
3. Update `/root/.local/share/arifos/carry_forward.json` (backup first).
4. Lane B receipt default. Lane A only if Arif says seal again.

## 6. Files to open

| Path | Why |
|---|---|
| `/root/.local/share/arifos/handoffs/2026-08-17-contrast-audit.json` | Full audit map |
| `/root/.local/share/arifos/carry_forward.json` | Live carry (this packet prepended) |
| `/root/AAA/docs/ORGAN.md` | Stale count |
| `/root/A-FORGE/src/interfaces/server.ts` | contract leak |
| `/root/A-FORGE/src/interfaces/mcp/serve.ts` | STATELESS_TOOLS whitelist |
| `/root/A-FORGE/docs/CONSTITUTION.md` | “does not judge / seal” |
| `/root/AAA/governance/delegation-ledger/STAGE_3_PROPOSAL.md` | Not executed |
| `/root/arifOS/arifosmcp/arifos_policy/cedar_bridge.py` | Stub — do not treat as live policy |

DITEMPA BUKAN DIBERI.
