---
name: a-forge-ops
description: "Operate, verify, and extend the A-FORGE execution organ (/root/A-FORGE, API :7071, MCP :7072). Covers the canonical build/test workflow (tsc then dist tests — the dist/ trap), tools_sot.yaml tool surface, LSP pre-commit gate, the forge_fetch governed-egress socket (EgressPolicy.ts), deploy sequence, and verifying sibling claims about A-FORGE. Trigger: any A-FORGE code work, egress/proxy questions, tool-surface drift checks, or claims that 'A-FORGE already does X'."
---

# A-FORGE Operations

## Topology (probe before act)
- Source: `/root/A-FORGE` — ESM + NodeNext, strict TS, explicit `.js` import suffixes.
- Runtime: `/opt/a-forge/app`; API `:7071`, MCP `:7072` (units `a-forge.service`, `a-forge-mcp.service`).
- Tool surface SOT: `/root/A-FORGE/tools_sot.yaml`; live `:7072/tools/list` beats the file.
- Canonical test registry = `package.json` `scripts.test` (tsc compile + `node --test dist/test/<listed files>`).

## Build / test — the dist/ trap
- Canonical: `npm test` = `tsc -p tsconfig.json && node --test dist/test/<listed files>`.
- PITFALL: `node --test test/foo.test.ts` (source tree) FAILS with `ERR_MODULE_NOT_FOUND` — ESM imports resolve `.js` suffixes to `dist/`. Always compile first, then run the compiled `dist/test/<name>.js`.
- `git commit` runs an LSP pre-commit gate automatically on staged code files (output: `LSP GATE: PASSED — N/N files clean`, F2/F4 enforced). Stage before committing.

## forge_fetch governed-egress socket (forged 2026-08-07)
- Chokepoint: `executeFetch()` in `src/interfaces/mcp/proxyTools.ts` (~line 1067+): `ssrfCheck(url)` → `checkRobotsTxt(url)` → `fetch(url)` → result envelope. All fetch aliases (`forge_fetch_url/json/metadata/links`) collapsed into `forge_fetch(mode=...)` in the 2026-07-31 entropy sweep — `forge_fetch` is THE tool.
- EgressPolicy: `src/infrastructure/egress/EgressPolicy.ts`. Profiles: `default | direct | mubeng | corp-proxy | tor`. Only `default`/`direct` resolve `{type:"direct"}`; others resolve `{type:"unavailable", reason}` — honest, never silent fallback (F9).
- Cache key MUST include `egress_profile`: `sha256(url|query|mode|egress_profile)`. Cross-profile cache leak = F1/F2 violation (direct content cached under a proxy profile leaks IP attribution).
- Response envelope carries an `egress` block: `{profile, provider, proxy_id, mcp_session}` — F11 audit trace; `mcp_session` comes from the MCP handler `extra.sessionId`, threaded via internal `_mcp_session_id` param (underscore prefix = internal, not in Zod schema).
- Actuator doctrine: mubeng (Go proxy rotator) = future actuator only — HOLD until a real per-IP 429/ban trigger (Yahoo Finance, SSM, gov portals). Cloudflare/JS walls are NOT proxy-class problems (TLS fingerprint + JS + reputation); cheap datacenter pools are MORE suspicious than one clean origin.
- Tests: `test/egressPolicySocket.test.ts` (17 cases: profile resolution, unavailable→BLOCKED, cache isolation, default-profile regression).

## Verify-before-seal (sibling/delegated claims about A-FORGE)
- Commit exists ≠ wired ≠ tested. Grep the import + call site, read the schema, run the dist test, check `git status --short --branch` for uncommitted remnants.
- `ahead N from origin` → not deploy-ready. Push first, then deploy. (Note: the `make deploy-local` HOLD rule belongs to arifOS — A-FORGE's deploy target is `make deploy`, see Deploy section below.)
- **Sibling's stated test count ≠ canonical runner output.** When a sibling/session reports "X/Y tests pass", run the canonical registry yourself (`npm test` per `package.json` scripts.test) and quote the actual tail. Sibling counts often differ — pre-existing failures may be missing or platform-specific numbers may be inflated. (2026-08-07: sibling said "45/45 tests pass"; actual `npm test` = 183/200 with 17 pre-existing failures in `EphemeralGenesisRunner` / `compute_fn` — zero regressions from the egress diff, but the sibling's number was wrong.)

## Deploy
- Green tests → `make deploy` (NOT `make deploy-local` — that target is arifOS-only) → rsync `dist/` to `/opt/a-forge/app/dist/` → restart only the affected unit → poll `:7071/health` + `:7072` tools/list.

### forge_vault receipt write (Lane B session close — new 2026-08-08)
- `forge_vault(mode="receipt")` is a **stateful MCP tool** on `:7071/mcp`. Requires `initialize` handshake → capture `Mcp-Session-Id` header → use header on all subsequent calls. Cannot be hit with a single REST-style curl.
- Receipt `content` must NOT contain F13 self-claim language ("F13 ratified", "F13 SOVEREIGN acknowledged") — F12 AUTHORITY_SMUGGLING will VOID it. Cite the sealing document, not the authority.
- Full recipe with three pitfall patterns: `references/forge-vault-receipt-recipe.md`

## Forge artifacts destined for Arif (channel routing — new 2026-08-08)

- **Pattern**: coding agents (OpenCode, Kimi, Codex) cannot DM Arif directly. Their Telegram bots (`@arifOS_bot` for FORGE, `@AGI_ASI_bot` for OpenClaw) don't have webhook access to `@ASI_arifos_bot` (the primary DM-bearing bot on chat_id `267378578`).
- **Two-step routing**: forge artifact → A-FORGE `forge_send_confirm` (form mode) or `forge_transfer_confirm` (financial) → Hermes bridge → Arif's DM. Don't let coder harnesses discover chat_id directly.
- **Why this matters**: OpenCode spent 2+ minutes trying `getChat(1003753855708)` (missing `-100` prefix) and `getUpdates` (blocked by webhook on the FORGE bot) before falling back to "give Arif the path manually." The path is the bridge, not the harness.
- **Cross-organ parallel**: same catch-22 exists for arifOS `git push origin main` ↔ `make deploy-local` — both sides require the other to be in sync first. RSI doctrine: report three resolution paths (force-push T3 ACK_M10 / reset-soft / defer) and wait for the sovereign choice, don't bypass.

### FORGE's OWN duty reports → AAA group DIRECTLY (2026-08-08 — the opposite of the bridge)

The bridge pattern above applies to **coding-agent artifacts**. FORGE's own duty notifications (constitutional-sync / drift-scanner / vitality-pulse) post **directly** to the AAA supergroup via `duties/forge-notify.sh` — no Hermes hop. Arif's explicit preference (verbatim: "kalau dia post personal aku penat nak copy paste"): duty reports go to the group, NOT his DM.

- `forge-notify.sh` is the single Telegram egress for all three duties. Token: `/root/.secrets/tokens/telegram-opencode-bot` (= @arifOS_bot). Destination lives in one line: `CHAT_ID`.
- **Chat-ID semantics:** Arif DM = `267378578` (bare user id). AAA supergroup = `-1003753855708` — **supergroups REQUIRE the `-100` prefix**; bare `1003753855708` fails. When moving a notifier from DM to group, change BOTH the `CHAT_ID` and the success log line, and test-send once before trusting the crontab.
- **parse_mode gotcha:** `forge-notify.sh` accepts a `PARSE_MODE` arg (`${2:-Markdown}`) but the curl call does NOT pass it — Telegram still renders `*bold*` / `` `code` `` as Markdown because raw chars pass through. Don't "fix" this by adding parse_mode unless you also sanitize `≤`/`≥`/`ΔS` first (the script already sed-strips them). Messages truncated at 4000 chars.
- **Duty scripts are bash, run from source by crontab — no dist/, no /opt copy.** Editing `duties/*.sh` in the repo IS the deploy for the NEXT crontab tick; there is no `make deploy` step for duties (unlike `dist/`). Verify what the cron will actually run with `git show HEAD:duties/forge-notify.sh | grep CHAT_ID` — a change already committed by a sibling/past session won't show in `git status` even if the working file looks patched.
- **UTC-clock pitfall:** duty report headers say "07:00 MYT" but crontab entries are UTC (`0 7 * * *` = 07:00 UTC = 15:00 MYT). Actual MYT runtimes: drift-scanner 10:00, constitutional-sync 15:00, vitality-pulse 23:00. Headers lie; crontab is truth. When Arif asks "when did X fire", convert from the crontab line, not the report filename.

### Constitutional-sync scanner: the two compliance warnings (98% → 100% fix, 2026-08-09)

`forge-constitutional-sync.sh` emits `Warnings: 2` (→ 98%) from exactly two sources. Both are cheap to clear:

1. **Skills missing floor_scope token.** Scanner greps every `/root/.agents/skills/*/SKILL.md` for `floor_scope|floors|F1|F2|F4`. A skill whose frontmatter/body lacks all of those → "N/166 skills missing floor_scope declaration". Fix: add `floor_scope: [F2, F4, F9, F12]` + `autonomy_tier: T1` to the frontmatter (see `aaa-skill-authoring-craft` for the AAA frontmatter convention). Note `.agents/skills/` is symlinked into `/root/AAA/skills/` — patch the resolved path.
2. **Deprecation registry entries without `reviewed`.** Scanner counts entries where `not it.get('reviewed')`; every entry in `/root/AAA/docs/deprecation-registry.json` must carry `reviewed: true` + `reviewed_date` + `reviewed_by`. To clear the queue: verify each entry's `replacement` path exists on disk, then stamp the three fields (11/11 cleared 2026-08-09). **Do not delete tombstones** — reviewed history is healthy, not warning-worthy.

Verification loop: `bash duties/forge-constitutional-sync.sh` → latest report shows `100% (190/190)`, `Issues: 0 | Warnings: 0`, and the test send lands in the AAA group.

**Arif expects duty reports as PDF, not .md paths.** When he replies "mana pdf" to a report link, render the report: markdown → self-contained HTML (cover + KPI row + tables) → `/usr/bin/python3.13 -c "import weasyprint; weasyprint.HTML('x.html').write_pdf('x.pdf')"` — the `pdf-report-generation` skill has the full pipeline (14mm margins, navy/gold, verify with `pdfinfo` + `pdftotext`). Deliver via `MEDIA:<path>`. The system python3.13 carries weasyprint 69; the WEALTH venv python3 does NOT.

## Apex scalar replication from arifOS (2026-08-14)

A-FORGE's `/health` endpoint delegates all 5 apex scalars (G, C_dark, W3, h, QDF) to arifOS but historically reported `{ value: null, status: "UNMEASURED" }` despite documenting `replication_strategy: "A-FORGE reads apex_scalars from arifOS /health"`. The replication was specified but never wired.

**Committed `b2a0dd7a`:** `GovernanceBridge.fetchApexScalars()` generalizes the existing `fetchCanonicalG()` pattern to all 5 scalars. `/health` handler became `async`, calls `fetchApexScalars()` with 3s timeout. Status is `"REPLICATED"` (not `"MEASURED"`) — provenance preserved (F2+F7). Graceful fallback: `null / "UNREACHABLE"` when arifOS is down. `apex_scalars_policy` gained `replicated_from`, `replication_status`, `replication_latency_ms`. No caching — freshness > perf for low-freq endpoint. 7 test cases in `test/apexScalarReplication.test.ts`.

**General federation pattern:** any organ that delegates measurement to the kernel should have a replication path wired into its own `/health`. Specified delegation without runtime replication = documentation theater. When a health endpoint says `delegated_to` or `replication_strategy`, grep for the actual fetch call in the source — if missing, it's documentation theater.

## Federation health check script (2026-08-14)

CCC(OpenCode) built `/root/AAA/scripts/federation-health.sh` — a single bash script that probes all 6 organs (HTTP health), checks git clean across 3 repos, verifies dream engine timer cadence, counts VVV entries, and checks apex scalar replication status. Outputs single-line `GREEN/YELLOW/RED | organs:N | vvv:N | apex_replicated:N/5 | reasons`. Exit codes: GREEN→0, YELLOW→1, RED→2. Zero dependencies beyond bash/curl/git/systemctl/python3.

## CCC coder federation (2026-08-14)

CCC (Codex Coder Compiler) = worker contract, not identity. Any CLI takes the contract: `CCC(Kimi)`, `CCC(Qwen)`, `CCC(OpenCode)`, etc. Full YOLO file+tool access, but **berdosa** (forbidden) to self-authorize production mutations, self-seal verdicts, or self-promote to sovereign. Roles temporary per-task: builder/verifier/reviewer/deployer.

**SEAL terminology separation (critical):**
```
worker SEAL = "evidence-complete commit candidate" — I'm done, here's my proof
APEX SEAL   = judgment — authorized or rejected
A-FORGE     = authorized integration — merge/deploy
arifFlow    = receipt — recorded what happened
VAULT999    = witness — immutable attestation
```

Flow: `ARIF → AAA → FED → CCC(harness, role) → A-FORGE → arifFlow → VAULT999`

No FI numbers (Arif rejected: "serabut la number"). Names only.
Maps: `/root/AAA/agents/CCC_FLOW.md`, `/root/AAA/agents/AAA_STATE_MAP.md`.

**Gemini CLI overclaim pattern:** Good as `role=reviewer` (text analysis, summarization). Dangerous as verifier/auditor — produces authoritative-sounding prose from shallow tool calls. `CCC(Gemini, role=reviewer)` only.

**Dispatch pattern when Kimi quota dead:** Write SPEC.md → dispatch via `qwen -p "$(cat SPEC.md)" --output-format text` → verify worker output independently → deploy. Kimi Code v0.35 uses MiniMax-M3 (managed quota often exhausted) — Qwen Code v0.21 uses GLM-5.2 via z.ai (more reliable for SPEC-driven headless dispatch).

## Deploy pitfalls (2026-08-07 session additions)

### systemd CHDIR permission denied — forge user + /root WorkingDirectory (2026-08-14)

The service unit sets `WorkingDirectory=/root/A-FORGE` and `ExecStart=node /root/A-FORGE/dist/...`, but a systemd override (`cap-narrow-batch1.conf`) changes `User=forge` `Group=forge`. User `forge` cannot access `/root/` → service fails with `code=exited, status=200/CHDIR` and restart-loops.

**FIRST thing to check when A-FORGE won't start after a deploy.** Symptoms: `systemctl is-active` shows `activating` (restart loop), journalctl shows `Failed at step CHDIR`. The service may have been running fine before because it was started as root before the override took effect.

**Fix — override WorkingDirectory + ExecStart to /opt/a-forge/app:**
```bash
cat > /etc/systemd/system/a-forge.service.d/fix-chdir.conf << 'EOF'
[Service]
WorkingDirectory=/opt/a-forge/app
ExecStart=
ExecStart=/usr/bin/node /opt/a-forge/app/dist/src/interfaces/server.js
EOF
systemctl daemon-reload && systemctl restart a-forge.service
```

**Critical:** `make deploy` (or manual `rsync dist/ /opt/a-forge/app/dist/`) is mandatory before restart — compiled output must be in `/opt/a-forge/app/dist/`. The `ExecStart=` with empty value is REQUIRED to clear the original before setting the new one.

- **`make deploy-local` does NOT exist in A-FORGE.** For A-FORGE, `make deploy` runs `tsc` then `rsync dist/ /opt/a-forge/app/dist/`. Verifying with `cat Makefile | sed -n '/^deploy:/,/^[a-z][a-z_-]*:/p'` saves 30s of staring at "No rule to make target" errors.
- **Deployed path is `/opt/a-forge/app/dist/src/...`, not `/opt/a-forge/app/dist/...`.** `tsc` preserves source-relative path under `dist/`, so `src/infrastructure/egress/EgressPolicy.ts` lands at `dist/src/infrastructure/egress/EgressPolicy.js`. Never assume `dist/infrastructure/...`.
- **Stale MCP commit string on `:7072/health`.** Even after a fresh deploy, `:7072/health` may report `commit:"<old-sha>"` because the MCP health response reads from a build-time string baked into `package.json` metadata, not from git head. The `:7071/health` is canonical deployment-truth (`deployed_commit`, `source_commit`, `deployment_drift:false`). Trust `:7071`, not `:7072`'s commit string.
- **`dist/build-commit.txt` is the bridge's BUILD_COMMIT source — must be rewritten on every deploy** (verified 2026-08-08). `npm run build` regenerates `dist/src/**/*.js` but does NOT touch `dist/build-commit.txt`. The bridge at `:7072` reads that file (see `dist/src/interfaces/mcp/serve.js` line ~37: `fs.readFileSync('${AFORGE_ROOT}/dist/build-commit.txt')`). Only the canonical `make deploy` rewrites it. **After running `npm run build` for any reason (LSP fix, hand edit), always also do `git rev-parse --short HEAD > dist/build-commit.txt` BEFORE restarting `a-forge-mcp.service`**, otherwise the bridge will report a stale commit and the federation probe (`forge-federation-probe --phase=drift`) flags drift. `make deploy-local` (added 2026-08-08, `e1eb1d4f`) does this for you.
- **`:7072/health` and `:7071/health` are TWO separate `/health` handlers** (verified 2026-08-08). The bridge payload lives in `dist/src/interfaces/mcp/serve.js` and is intentionally minimal (`{ok, service, version, commit, sessions, ...}`); the canonical payload lives in `dist/src/interfaces/server.js` and carries authority_ceiling + apex_scalars_policy. **Adding a field to `:7071/health` does not propagate to `:7072/health`** — patch `serve.ts` separately. The federation probe checks BOTH ports; forgetting the bridge causes the probe to FAIL authority check even after the canonical fix.
- **Verification requires a live MCP roundtrip.** `curl :7072/health` does NOT prove new behavior landed. Use the MCP SDK via `/root/A-FORGE/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js` + `StreamableHTTPClientTransport(new URL("http://127.0.0.1:7072/mcp"))`, call `forge_fetch` with `egress_profile="mubeng"`, expect `status=BLOCKED, reason="egress profile 'mubeng' not yet configured..."` in `content[0].text`. Bare `curl -X POST /mcp` against SSE transports returns empty without an Accept header `application/json, text/event-stream` and a proper MCP client. See `references/live-mcp-probe-recipe.md`.

## Kill-switch bypass test (forged 2026-10-23)

A revocation is only real if **every adapter path** returns HOLD. Do not accept "MCP is gated" as closure.

Test sequence, with a non-destructive read verb:
1. `apa-revoke revoke gmail --reason bypass-test --by <actor>`
2. Probe: MCP `forge_gmail`, APA bridge `:18097` direct POST, `gws_bridge.py` CLI, `google_workspace` import, Telegram bridge `:18096` direct POST.
3. `apa-revoke clear gmail`; probe again to prove reversibility.

Live result 2026-10-23: MCP, APA bridge, `gws_bridge.py`, `google_workspace` import and Telegram bridge all returned `APA_REVOKED`; the `gws` **binary** still returned Gmail messages. That residual is a root-shell / token-custody problem — close it with non-root agents, a secret broker, or an egress policy, not another wrapper. A kill switch tested only at one path is a rumour.
