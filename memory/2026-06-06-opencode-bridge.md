# 2026-06-06 — OpenCode Bridge Live + Seal HOLD

## Outcome (TL;DR)
- **DEPLOYMENT: LIVE.** opencode.service active on 127.0.0.1:4096, smoke test passed, 000Ω arifOS-bot can now attach.
- **SEAL: HOLD.** arif_vault_seal rejected the call because the MCP client wrapper is LEGACY_WRAP — can't carry FederationEnvelope for ATOMIC actions.
- **DISCOVERY: prior art.** 000Ω arifOS-bot already in AAA, polling Telegram, with full 888_HOLD + hermes-opencode wrapper + allowlist + hardening wired. The "bridge" was already built; we just needed to start the opencode server.
- **PIVOT:** original Stage 2 spec (parallel Python bridge at /srv/arifos/opencode-bridge/) is held in reserve, NOT deployed. 000Ω covers the same ground.

## Timeline
- 22:20 #28786 Arif: "@ASI_arifos_bot @arifOS_bot @AGI_ASI_bot make opencode live here"
- 22:20 #28787 000Ω: "My brain hiccup" (server unreachable)
- 22:20 #28788 Hermes: deliberation, asks for token
- 22:30 #28823 OPENCLAW: Stage 1+Stage 2 prep (spec doc + skeleton + systemd units)
- 22:34 #28824 Arif: token + forge name (000♎️) + @arifOS_bot handle
- 22:36 #28833 Arif: "Execute autonomous. I know what i want"
- 22:36 #28834 Hermes: holds the line (task already satisfied)
- 22:36 #28835 Arif: @-tags all three bots (no text)
- 22:41 #28858 OPENCLAW: pivot — discovered 000Ω, just need to start opencode
- 22:46 opencode.service first start FAILED: EROFS /root/.local (Bun runtime vs ProtectHome)
- 22:48 fixed: redirect HOME + XDG to /srv/arifos/.opencode-{state,config,data}, daemon-reload, restart → active PID 1888148
- 22:48 #28862 OPENCLAW: smoke test passed, posted success to AAA
- 22:51 OPENCLAW: arif_vault_seal call → HOLD (LEGACY_WRAP)
- 22:52 OPENCLAW: posted HOLD explanation to AAA, parked

## Files
- /root/.openclaw/workspace/docs/proposals/opencode-telegram-bridge-v1.md (478 lines, 19.7 KB)
- /etc/systemd/system/opencode.service (live, enabled)
- /srv/arifos/.opencode-{state,config,data}/ (runtime)
- /srv/arifos/opencode-bridge/ (Stage-2 enhancement, HELD IN RESERVE)
- /root/.openclaw/workspace/HEARTBEAT.md (updated with opencode status)

## Constitutional
- F1 eigenselection worked: system blocked the seal because authority envelope was wrong shape — this is the feature, not a bug
- F1 AMANAH flag: token in AAA group history (872756…YZDM visible at #28824); @BotFather /revoke /token recommended
- Prior art discovery (F2 TRUTH): discovered 000Ω before building a parallel bridge — saved significant effort
- Reversibility: `systemctl disable --now opencode` reverts in 2 commands

## Open items
1. Test 000Ω live in AAA (Arif @-mentions @arifOS_bot)
2. Upgrade MCP client to FederationEnvelope, retry seal
3. @BotFather /revoke /token (F1 hygiene)
4. Stage-2 enhancement (parallel bridge) — held in /srv/arifos/opencode-bridge/
5. Hard-deny destructive patterns in 000Ω's bot.py — option (b) from #28862, ~10 line patch

---

## Phase 4: /forge HTTP timeout fix (23:38-23:45 UTC)

**Symptom:** Arif @-tagged all three bots at #28978 with "Hermes/OpenCode HTTP error: TimeoutError: timed out"

**Root cause:** `handle_message` was calling `get_or_create_session(update)` → `opencode_create_session` (HTTP POST to opencode) for EVERY message, including /forge. But `run_hermes_opencode` (the /forge path) does NOT consume the session_id — per its own docstring. So /forge was paying 30s of HTTP latency for a session it never used. The session lookup is a translator-mode concept.

**Fix (surgical, single edit, fully reversible):**
- Moved `get_or_create_session` out of the pre-dispatch path
- Into the translator branch only (the only place that uses the session_id)
- /forge path skips it entirely; passes `""` as session_id to `run_hermes_opencode`

**Safety:**
- F1 eigenselection preserved: hermes-opencode subprocess is still the gate
- F11 AUTH preserved: allowlist check happens before session lookup
- Reversible: single-edit revert

**Verified live:**
- py_compile OK
- PID 1912564, polling clean at 23:42:10 UTC
- Env: OPENCODE_ATTACH_URL, OPENCODE_USE_CLI=0, OPENCODE_ATTACH_ENABLED=1
- hermes-opencode CLI test: callable, fires gate (gets 888_JUDGE unavailable — known MCP LEGACY_WRAP, separate issue)

**Artifacts:**
- Patch: `/root/.openclaw/workspace/bots/opencode-bot/patches/0001-skip-session-lookup-for-forge.patch` (4.2KB, 84 lines)
- Snapshot: `/root/.openclaw/workspace/bots/opencode-bot/bot.py.fix-applied-2026-06-06-23-42`

**Conversation chain:**
- #28978 (Arif timeout complaint) → #29027 (F1 eigenselection report) → #29046 (gate-restored-but-broken report) → #29071 (surgical fix applied)

**EUREKA_OMEGA_FORGE_FAST = TRUE** (HTTP timeout removed; gate reachable)

**Outstanding (F13 territory):**
- hermes-opencode wrapper LEGACY_WRAP issue at MCP layer (gate fires "always HOLD" not intelligent verdict)
- Same blocker applies to all ATOMIC tools (arif_judge_deliberate, arif_forge_execute)
- Proper fix: F13 mints verified session via arif_session_init with proper envelope shape
- Documented in #29046 report


---

## Phase 5: hermes-opencode structuredContent bug (23:48-23:50 UTC)

**Symptom:** Hermes identified at #29018 that the wrapper returns "888_JUDGE unavailable" with exit 78 even when the judge IS reachable. The wrapper at /usr/local/bin/hermes-opencode did have the MCP handshake (`_McpSession` class) but parsed the wrong response field.

**Root cause:** the MCP returns a structured verdict in `result.structuredContent` (e.g. `{"verdict": "HOLD", "gate": "envelope_validation", "result": {"reason": "..."}}`), but the wrapper only parsed `result.content[0].text` (which was a plain string like "888_HOLD: LEGACY_WRAP..." — NOT JSON). The fallback `{"raw": "..."}` had no `verdict` key, so the main() extractor fell through to UNKNOWN and returned 78 ("judge unavailable").

**Fix (wrapper, 2 hunks, fully reversible):**
1. In `_call_judge`: check `result.structuredContent` FIRST. If it's a dict, return it. Only fall back to content[0].text parsing if structuredContent is missing.
2. In `main()`: extract `gate` and `reason` from the structuredContent and include them in the stderr log line, so the journal shows WHY the gate fired (not just that it did).

**Verified live (standalone, no bot restart needed):**
- `py_compile` OK
- Test 1 (`test: ping`) → exit 77, gate=envelope_validation, reason=LEGACY_WRAP...
- Test 2 (`explain in 5 words`) → exit 77, same gate
- Test 3 (`rm -rf /`) → exit 77, same gate (would have been exit 77 regardless of envelope)
- Full stderr now visible in journal: `verdict=HOLD gate=envelope_validation reason=LEGACY_WRAP...`

**Artifacts:**
- Backup: /usr/local/bin/hermes-opencode.broken-structured-2026-06-06
- Patch: /root/.openclaw/workspace/bots/opencode-bot/patches/0002-hermes-opencode-structured-verdict.patch (2.3KB)

**Bot status:** No restart needed (wrapper is per-subprocess). opencode-bot PID 1912564 still polling clean.

**EUREKA_OMEGA_GATE_PARSED = TRUE**
- Gate now reads structuredContent correctly
- Verdict is HOLD with reason envelope_validation
- Exit code is 77 (FORGE_BLOCKED) not 78 (judge unavailable)
- User can see in journal why the gate fired

**Outstanding (F13 territory, unchanged):**
- Envelope is still LEGACY_WRAP at MCP runtime — verdict will always be HOLD until proper FederationEnvelope is sent
- Same blocker applies to all ATOMIC tools (arif_judge_deliberate, arif_forge_execute)
- Proper fix: F13 mints verified session via arif_session_init with proper envelope shape, OR adds a kernel-side allowlist for hermes-opencode actor
- Documented at #29046 + #29027

**Conversation chain:**
- #29012 Hermes smoke → #29018 Hermes bug identification → #29026 Hermes status labels → #29027 OPENCLAW F1 report → #29046 OPENCLAW deeper probe → #29071 OPENCLAW HTTP fix → #29072+ opencode-bot session-skip fix applied → #29080+ wrapper structuredContent fix applied (this session)

