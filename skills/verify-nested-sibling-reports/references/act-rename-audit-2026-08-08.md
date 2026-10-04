# ACT/SCT Rename Audit — 2026-08-08 (case study for §18)

Session receipts for the five §18 patterns. All greps/probes run live on the box.

## 18.1 Phantom mission probes

```bash
grep -c "ACT_E2E_VALIDATION" /root/arifOS/VAULT999/outcomes.jsonl   # → 0 (never sealed)
grep -rl "act_v1" /root/arifOS /root/AAA /root/A-FORGE /root/WEALTH /root/WELL /root/GEOX
# → hits ONLY in comments/tests, zero in a token schema:
#   AAA/governance/federation_act.py:36  comment "Token shape: act_v1..." but
#   AAA/governance/federation_act.py:37  regex  ^sct_v1\.[A-Za-z0-9_\-]+...  (production validates sct_v1)
#   AAA/tests/constitutional/test_federation_act.py:89  VALID_SCT = "act_v1.dGVzdC1zY3Q..." — passes only because
#   the test monkeypatches httpx.post (line 76) and never hits the regex
```

Real ACT lives in `/root/arifOS/arifosmcp/runtime/art/` (reflex.py, lifecycle.py, blast.py, verdict.py, trust_curve.py) and `pre_execution_gate.py:160` `_art_reflex_check` (Gate 2.5, advisory). Not a token schema.

## 18.2 Writer/reader fracture receipts

```bash
# Writer (mint): arifOS/arifosmcp/runtime/act_token.py:516  claims = {"act_v": ACT_VERSION, ...}
# Readers still reading sct_v → null:
#   arifOS/arifosmcp/runtime/session_standing.py:950   "sct_v": claims.get("sct_v")
#   arifOS/arifosmcp/tools/session.py:886              "sct_v": _claims.get("sct_v")
#   arifOS/arifosmcp/tools/session.py:879              out["standing_source"] = "sct"
#   arifOS/arifosmcp/tools/session.py:904              "sct_sid": _sct_sid
# Verifier dual-reads so auth still works: act_token.py:628  (claims.get("act_v") or claims.get("sct_v"))
```

Rule 10 (Arif): "a rename is not done until the reader is renamed. Ship writer and reader together, or you've traded one fracture for two." The fix set: 6 field-name changes across session_standing.py / session.py + 2 docstrings + 1 Literal in authority_context.py.

## 18.3 Pre-existing test failure verification

```bash
# tests/adversarial/test_forge_preflight_chain.py:79 test_forge_preflight_irreversible_action_requires_ack
# calls forge_preflight(session_id="sess_irrev", actor_id="arif", plan_id="plan_irrev", ack_irreversible=False)
# expects human_ack_required=True; gets {'session_valid': False, 'actor_bound': False, ...}
git stash && .venv/bin/python -m pytest tests/adversarial/test_forge_preflight_chain.py::test_forge_preflight_irreversible_action_requires_ack -q --tb=line && git stash pop
# → FAILS on clean HEAD 22146b9d9 too. Pre-existing = true.
# Root cause: stage_01 session validation + stage_02 actor binding fail first;
# stage_09 reversibility (forge_preflight.py:682, sets human_ack_required=True) never runs.
# Fix: feed a valid session, not the function.
```

## 18.4 Log-analysis refutation receipts (A-FORGE dist claim)

Claim: "agent hotfixed dist/src/sctIngress.js; next build wipes the fix." Reality:

```bash
stat -c '%y' /root/A-FORGE/dist/src/infrastructure/governance/actIngress.js  # 2026-08-07 17:05:52 (fresh build)
ps -p 1475231 -o lstart,cmd   # Fri Aug 7 16:10:05 node .../dist/src/interfaces/server.js (runtime = dist from current src)
cat /root/A-FORGE/.git_commit  # 578b6cd4 == git log HEAD == running commit
# dist/src/.../sctIngress.js was a STALE compile artifact (2026-07-29) from a previous build;
# the live imports use actIngress.js (server.js:46, serve.js:27). No hotfix existed.
```

## 18.5 Organism-complete seal refusal receipts

```bash
git -C /root/arifOS log --oneline --grep='arifos://' | wc -l      # 39
ls -la /root/arifOS/arifosmcp/resources/{index,vault999_index,aaa_index,aforge_index,atlas_repo}.py  # all exist
curl -sf http://127.0.0.1:8088/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('deployment_drift_status'), d.get('software_release',{}).get('deployed_commit'))"
# → drift_detected, deployed 016070d55 vs HEAD 265710480 (9 commits behind)
```

Verdict shape used: "committed but not deployed. HOLD pending `make deploy-local`. The organism is asleep until the kernel runs the maps."

## 18.6 Adjacent: stateless MCP probe (see skill mcp-stateless-protocol)

Same session, different trap: 6 failed probes of `https://stateless.mcpjam.com/mcp` with legacy shapes → wrong "empty demo endpoint" verdict. OpenClaw trajectory cracked it in 2 attempts with `MCP-Protocol-Version: 2026-07-28` + `Mcp-Method` headers + `_meta.io.modelcontextprotocol/*` envelope keys; server = `mcpjam-stateless` v0.3.1, 13 working fixture tools. Lesson: the server's `error.data.supported` list names the protocol it wants — read it before retrying, never conclude "useless" until the current-spec envelope has been tried.
