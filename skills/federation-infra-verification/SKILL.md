---
name: federation-infra-verification
description: "Probe declared federation infrastructure state against live evidence — MCP service quirks, SCT token decoding, fallback-chain readiness, and structured extractive-map / claims-list audits. Use when: 'is X really running?', 'test the fallback chain', 'verify these risk nodes', 'check if Y matches Z', or someone hands a list of findings to validate against the live box. Distinct from federation-runtime-forensics (reactive: something broke, why?) — this is proactive structured verification with a standard deliverable shape."
---

# Federation Infrastructure Verification

Probing, decoding, and verifying declared state against live state in a multi-agent federation. Covers arifOS kernel internals, MCP service endpoints, LiteLLM proxy, FED router, and token/session lifecycle.

## 1. Live probe > config file (always)

For any infrastructure claim, ask: **"what would the live evidence look like?"** then probe that — never trust config/docs alone.

| Declared state source | Live probe |
|---|---|
| "Service is running on :7074" | `ss -tlnp \| grep :7074` (who actually listens), then `curl :7074/health` |
| "A-FORGE is healthy" | **Probe BOTH ports**: 7071 (server.js, main sense/judge) AND 7072 (serve.js, MCP bridge). They're separate systemd units with different responsibilities |
| "Fallback chain: DS→Bailian→Kimi→HOLD" | Grep `MODEL_TIERS.json` for `fallback_rule`, then check if ANY cascade test exists in logs/pytest |
| "SCT TTL is 1 hour" | Decode the live token payload (see §2), check remaining lifetime |
| "Skills/tools registered" | `ls /root/AAA/skills/ \| wc -l`, cross-check against `registries/skills.yaml` |
| "OBSERVE bypass exists in orchestrator" | Grep orchestrator code for action_class / OBSERVE branching — not just the predict_gate |

## 2. SCT token decoding (the env-var trap)

**Pitfall:** `ARIFOS_SESSION_TTL_SECONDS` (env var, default 86400 in `runtime/session.py:170`) controls the session **record** expiry only. The SCT **token** TTL is hardcoded `SESSION_TTL_SECONDS = 3600` in `arifosmcp/runtime/session_auth.py:117` and baked into the Ed25519-signed payload. Setting the env var does NOT change token lifetime.

To decode the live SCT and check remaining lifetime:

```python
import json, base64, time
with open('/root/.arifos/federation-session.json') as f:
    d = json.load(f)
tok = d.get('session_token', '')
parts = tok.split('.')
if len(parts) >= 2:
    pad = parts[1] + '=' * (-len(parts[1]) % 4)
    payload = json.loads(base64.urlsafe_b64decode(pad))
    now = int(time.time())
    print(f"ttl={payload.get('ttl')} exp={payload.get('exp')} remaining_s={payload.get('exp',0)-now}")
```

Key claims: `ttl` = configured TTL (should be 3600), `exp` = unix expiry, remaining_s = seconds until hard cutoff. If remaining_s < 0 → token expired, `SESSION_GRACE_SECONDS` (300s) applies, then hard gate.

## 3. MCP service probing (tools-discovery + Accept-header + session-ID quirks)

The arifOS kernel and MCP services expose tool schemas, but the HTTP route names differ from what reports assume:

### 3.0 Tool discovery endpoint (verified 2026-08-06)

`curl http://127.0.0.1:8088/tools/list` returns **"Method Not Allowed"** (405). The correct path is `/tools` (or `/tools.json`). The kernel's own `source_of_truth` field says `"tools/list"` is canonical — but the HTTP route disagrees.

When probing for fabricated tool families: `curl -s http://127.0.0.1:8088/tools > /tmp/arifos-tools.json` then grep for the family name. Zero matches = fabrication. Full worked example: `references/arifos-tools-list-endpoint-2026-08-06.md`

The 8 canonical arifOS tools are: `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`. ATLAS333 and EUREKA777 are kernel modes + MCP resources, not standalone tools. If a report names `megamemory_*`, `atlas_*`, or `eureka_*` as `/tools`-level tools, it's fabricated.

**Pitfall:** Mode names in `/tools` schemas vs mode names in `arifosmcp/schemas/arifos_tool_registry.json` can diverge. E.g. `arif_think` schema exposes `default: "reason"` but the registry JSON lists 12 modes including `atlas`. When verifying "does mode X exist on tool Y", grep both.

### 3.1 Accept-header + session-ID (the double-gate)

The FED router (:7074) and other MCP services have a double-gate on tool calls:

1. **Accept header** — must include BOTH `application/json` AND `text/event-stream`:
   ```
   -H 'Accept: application/json, text/event-stream'
   ```
   Sending only `application/json` → `Not Acceptable: Client must accept both application/json and text/event-stream`

2. **Session ID** — after correct Accept, tool calls still require a valid MCP session:
   `Bad Request: Missing session ID` — you can't just `curl` a tool; you need the full MCP handshake.

**Practical workaround:** For health/readiness checks, use `curl :port/health` (no session needed). For logic inspection, grep the source directly (`/root/AAA/scripts/fed_router.py`).

#### 3.1a "Judge the probe, not the service" reflex (2026-08-06 incident)

When an MCP probe fails, the default reaction is to suspect the service. **The more common cause is the probe itself.** Specifically:

| Probe failure | What you should suspect FIRST | One-line fix |
|---|---|---|
| `Not Acceptable: Client must accept application/json` | **Your curl.** Header missing. | Add `-H 'Accept: application/json'` (and for FED-style, also `text/event-stream`) |
| `Method Not Allowed (405)` on `/tools/list` | **Your path.** Wrong endpoint. | Try `/tools` or `/tools.json` instead |
| `Bad Request: Missing session ID` | **Your invocation.** No MCP handshake. | Need `initialize` + `notifications/initialized` before tool calls |
| `0 tools returned` from `/tools/list` (no error) | **Your probe.** Same root cause as "Not Acceptable" — header missing, request quietly rejected | Add Accept header and re-run |

Worked example (2026-08-06, this skill's author): probed `:8088/mcp` with default `Accept: */*`, got "Not Acceptable"; then probed `tools/list` with the same broken header and got "0 tools". Almost wrote "kernel is broken" in the audit response. **Re-probed with correct headers → kernel returned all 8 tools.** The kernel was fine. The probe was broken.

**Rule:** before writing "X is broken" in your reply, fix the probe and re-run ONCE. If the second probe still fails, then escalate to "service genuinely broken". This protects against two failure modes at once: (a) false-negative that overwrites correct "up" state with incorrect "down"; (b) cascading confusion when sibling reports arrive that reference a "broken" state the live system never had.

The same reflex catches the **sibling-report**: a sibling may report "service X is broken" because THEIR probe failed — independent of whether X is actually down. Don't accept their conclusion until you re-probe yourself with a known-good probe.

Key service endpoints:
| Port | Service | Protocol | Live probe |
|---|---|---|---|
| :8088 | arifOS kernel | Python MCP | `curl :8088/health` |
| :7071 | A-FORGE (node) | Node.js | `curl :7071/health` |
| :7072 | A-FORGE (node, alt) | Node.js | `curl :7072/health` |
| :7074 | FED router | Python MCP | `curl :7074/health` |
| :4000 | LiteLLM proxy | Tailscale | needs auth + correct Accept |
| :11434 | Ollama (bare-metal) | text/embeddings | `curl -m 3 http://127.0.0.1:11434/api/tags` |

## 3a. Ollama's surviving role — embedding backend only

Ollama in this federation is **not** the inference engine for Hermes or any organ. Its only production job today is generating embeddings (`bge-m3`) for vector memory. Text generation was migrated to mimo via LiteLLM. Canonical statement: `ilmu_soul.yaml` comment — *"Ollama kept only for bge-m3 embeddings"*.

Wiring:
- Bare-metal Ollama (systemd) binds `localhost:11434` and serves `/opt/arifos/data/ollama/models`
- Graphiti MCP runs as a Docker container and reaches Ollama via the docker network (`ollama-engine-prod:11434`)
- Graphiti's `OPENAI_API_KEY="ollama"` is a sentinel value (not a real key) — it just routes to the local Ollama
- `/usr/local/bin/graphiti-start.sh` does a pre-flight probe and FATALs out if Ollama is unreachable (correct fail-closed F2 behavior)

Doctrine conflict (verified 2026-08-06): the systemd unit sets `Environment="OLLAMA_HOST=0.0.0.0:11434"` directly, which beats the `bind-localhost.conf` drop-in. This violates `LOCALHOST_IS_PASSWORD` doctrine — UFW masks the exposure but the bind is wrong. **Fix is to edit the unit file**, not add more drop-ins.

**2026-08-06 update — verified live:** the unit file's `Environment="OLLAMA_HOST=0.0.0.0:11434"` was either already fixed, or the drop-in DOES win under modern systemd (resolution precedence may have changed). After `systemctl start ollama` with both drop-ins set to `OLLAMA_HOST=127.0.0.1:11434`, `ss -tlnp` showed `LISTEN 127.0.0.1:11434` only — no public bind. **The bind IS correct on restart if BOTH drop-ins agree on 127.0.0.1.** Audit before editing the unit file: read both drop-ins; if they're consistent with the doctrine, restart and verify. If a restart still binds 0.0.0.0, then the unit-file edit is the right next step.

## 4. Claims-list / extractive-map audit methodology

When handed a list of claims to verify (risk nodes, audit findings, extractive-map items):

### Step 1: Classify each claim
- **Runtime state** (is X running / down) → probe with `ss`, `curl`, `ps`
- **Config/code gap** (does X enforcement exist) → grep source code, check mode lists vs contract docs
- **Architecture claim** (X needs Y) → read the architecture code, verify the claim's prerequisite

### Step 2: Per-claim evidence
For each claim, produce:
- **Verdict:** `confirmed` / `partial` / `refuted`
- **Evidence:** exact file path + line numbers, or live probe output
- **Key finding:** the most important detail (often the code-vs-doctrine gap)

### Step 3: The code-vs-doctrine gap (recurring pattern)
The single most reliable finding in federation audits: **a lifecycle/gate/floor exists in contracts or AGENTS.md but has no implementation in the actual tool code.** Before concluding an enforcement exists, grep the tool's mode lists:
```bash
grep -n "MODES\|mode.*=" /root/arifOS/arifosmcp/tools/forge.py | head -20
```
If the claimed mode name doesn't appear → gap confirmed.

### Step 4: Ranked countermeasure plan
- **Cheapest first AND reversible first** (dual sort)
- Each row: rank, node, countermeasure, cost estimate, reversible (yes/partial/no), details
- Investigation phase = zero production mutation ("Do NOT mutate production. Investigation and proposal only.")

### Step 5: Evidence path table
End with a table of all files/probes used, so the user can spot-check.

## 4a. Token budget discipline (cost ceiling for verification)

A verification session that returns 10 confirmed findings but burns 100k tokens has **negative ROI for Arif** — each token is paid-for inference. 2026-08-05 taught this the hard way: three parallel subagents verified one self-report that a single `grep` + `curl` + `diff` would have answered in ~2k tokens. Arif's exact words: *"Token pakai duit tau"* and *"Buat ja la"*.

**Heuristics before dispatching subagents or writing prose:**

| Situation | Right tool | Tokens |
|---|---|---|
| Verify a single file-path claim | `terminal` (stat/grep/diff) | ~500 |
| Verify a single runtime claim (FQ, port, health) | `terminal` (curl) | ~500 |
| Verify a 3-5 item claims list | `terminal` (one pass per claim) | ~3-5k |
| Verify a 10+ node extractive map with file:line citations | 1 subagent, not 3 | ~15-20k |
| Verify something requiring probing 2+ organs in parallel | 2-3 subagents | ~30-50k |
| Pure conceptual research / synthesis | subagent (orchestrator) | ~50-80k |

**Hard rules:**
1. **One probe per claim**, not three. If the first probe is inconclusive, escalate to a second — not parallel subagents on the first try.
2. **Subagents are for cross-organ or cross-subsystem verification** (kernel + a2a + federation state in parallel). Not for "I want a second opinion" — that's an LLM second-opinion prompt, ~1k tokens.
3. **Answer the question first, write the explanation second.** If the user said "buat ja," they did NOT ask for a 12-row evidence table. Output: action + 2-line summary + evidence path. The table is for the user who wants to spot-check.
4. **Tables are for structure, not for filling space.** A 3-row table beats a 10-row table with padding.
5. **The patch is "done" when the user's question is answered.** Not when the prose is polished.

**The Arif heuristic:** if your response is longer than 4 paragraphs for a yes/no question, you're over-investing. Cut the prose, keep the evidence path.

## 4b. "Watch item" framing hiding K1 halt-on-drift (2026-08-07)

Pattern from a singleton 888-APEX verdict session: a sibling diagnosed `drift_detected` in arifOS runtime and labeled it **"watch item, not blocking"** without running the K1/K4 hierarchy check. K1 (kernel-eurekas) says: a hard crash is infinitely safer than a silent lie. K4 says: substrate honesty is a precondition for agentic scale. **Drift on production substrate = halt and investigate, not "watch."**

The trap: "watch item" is socially polite downgrade language. It converts a constitutional halt signal into a non-urgent todo. The justification is usually "it's been like this for a while, the system is still running, let's not disrupt." That justification **violates F2 TRUTH (we're tolerating substrate lie)** and **F12 RESILIENCE (agents downstream reason on uncertain ground)**.

**Detection recipe:**
```bash
# 1. Confirm the drift claim with the canonical (K-honest) endpoint
curl -s http://127.0.0.1:8088/api/governance-status | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('drift_detected:', d.get('drift_detected'))
print('status:', d.get('status'))
print('unmeasured_floors:', d.get('unmeasured_floors'))
"

# 2. Cross-check the legacy /health endpoint (K1 pitfall: dual-path)
curl -s 'http://127.0.0.1:8088/health?nocache=1' | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('status:', d.get('status'))
print('deployment_drift_status:', d.get('deployment_drift_status'))
print('runtime_drift:', d.get('runtime_drift'))
"

# 3. If either says drift → the K1/K4 ladder says HALT, not watch
#    Use the canonical-path number (the /api/governance-status one).
#    If they disagree, the K1-substrate-truth wins; the legacy is "stale interpretation."
```

**Reply shape (verified 2026-08-07):**
> "Sibling diagnosed drift as 'watch item, not blocking.' K1 (kernel-eurekas) says drift = halt. K4 says substrate honesty is a precondition for agentic scale. Verdict: **VOID** the 'watch item' framing. Replace with: investigate `runtime_manifest_hash` reconciliation now. The subsystem where drift is tolerated is the subsystem where agents reason on lies."

**The dual-path problem compounds this trap.** `/health` and `/api/governance-status` are produced by different code paths (kernel-eurekas §Pitfalls). A sibling that quotes `/health` says `status=degraded, drift_detected`; `/api/governance-status` says `drift_detected=None`. The K-honest number lives at `/api/governance-status`. A sibling picking one without naming the path is hiding its source — and the verifier must cross-check both endpoints before declaring a sibling's drift claim verified, refuted, or silently-divergent.

## 4c. The model-alias-doesn't-exist config-bug class (2026-08-07)

Distinct from §10 (config-path-liveness): the config file claims to invoke a model that the provider has never defined. Pattern surfaced in the OpenCode multi-agent diagnostic:

- `opencode.json` top-level: `"model": "litellm-federation/opencode"`
- `litellm-federation` provider section: defines `agi-333`, `asi-555`, `asi-555-audio`, `apex-888` — **no `opencode` key**
- Sibling labelled this as "auth path unclear" — wrong. The path is fine; the alias is undefined.

This is **F2 TRUTH violation at the config layer**: a config that asserts "use model X" when X doesn't exist is a declarative lie. The system will silently fall back to a default or throw a confusing error at resolve time, and the user will chase the wrong bug.

**Detection recipe:**
```bash
# For any config that names a model, verify the model exists in the provider's model list
python3 << 'EOF'
import json
cfg = json.load(open('/root/.config/opencode/opencode.json'))
default_model = cfg.get('model', '')
provider = default_model.split('/')[0]
models = cfg.get('provider', {}).get(provider, {}).get('models', {})
defined = set(models.keys())
referenced = set()
referenced.add(default_model)
for agent, acfg in cfg.get('agent', {}).items():
    m = acfg.get('model', '')
    if m: referenced.add(m)
ref_short = {r.split('/', 1)[1] if '/' in r else r for r in referenced}
missing = ref_short - defined
if missing:
    print(f'MISSING ALIASES referenced but not defined: {missing}')
    for m in missing:
        print(f'   - {provider}/{m}: replace with one of {sorted(defined)}')
else:
    print('OK: All model references resolve')
EOF
```

**Decision tree when an alias is missing:**
1. Is the alias a typo of a defined alias? (e.g. `opencode` vs `agi-333`) → fix to the defined name
2. Is the alias a deleted/migrated model? → check git history of the config for the previous intent
3. Is the alias a metadata comment (e.g. `model: opencode` actually meant "use the opencode default")? → remove the field and let the agent's model definition win
4. If none of the above → escalate to sovereign (F13) before adding a new alias

**Reply shape (verified 2026-08-07):**
> "Config top-level `model: litellm-federation/opencode` references a model that the `litellm-federation` provider section does not define. Provider defines: `agi-333`, `asi-555`, `asi-555-audio`, `apex-888`. The `opencode` alias is undefined. This is a config-level F2 TRUTH violation. Sibling diagnosis mislabeled this as 'auth path unclear' — the auth path is fine, the alias is broken. Fix: change to `litellm-federation/agi-333` (matching `default_agent: 333-AGI`'s model) or remove the top-level field entirely."

## 4d. The "either/or" recommendation without Q2 trade-off (2026-08-07)

Sibling proposed two alternative fixes ("either `ollama pull X` or change `small_model` to Y") without ranking them on Q2 quantitative cost (BR/REV/Time/Conf/PA per path). QQQ doctrine binds every recommendation to Q1/Q2/Q3 — missing Q2 means the recommendation is **INADMISSIBLE-QQQ-INCOMPLETE**.

**Detection recipe:**
For any recommendation with 2+ paths, check:
- Q1 qualitative: are ≥5 paths evaluated (including NULL and INVERSE)?
- Q2 quantitative: is each path scored on the same axes (bytes, seconds, reversibility, confidence, side-effect)?
- Q3 quantum: does the recommendation account for precedent, interference, superposition, observer?

If any of Q1/Q2/Q3 is missing, the recommendation is not a verdict — it's a menu. **Tag it `INADMISSIBLE-QQQ-INCOMPLETE`** and surface the missing path to the sovereign.

**Reply shape (verified 2026-08-07):**
> "Sibling proposed 'either pull model or change config' without Q2 trade-off. Path A: ~1.9GB download, ~3min, restores original intent. Path B: zero disk, seconds, but substitutes a generalist model for the sovereign's deliberate choice. Both valid; the choice is the sovereign's. Tag: `INADMISSIBLE-QQQ-INCOMPLETE`. Seal a default (Path B is reversible-first per F1) but surface both options."

## 5. Federation risk node patterns (from 2026-08-05 audit)

Verified nodes that recur as common federation failure modes:

| Node | Pattern | Where to look |
|---|---|---|
| Model fallback untested | Config defines chains but no circuit breaker or cascade test | `MODEL_TIERS.json` `fallback_rule` fields, grep for "cascade" in logs |
| Session TTL hardcode | Env var only affects record, not token payload | `session_auth.py:117` (`SESSION_TTL_SECONDS`), decode live token |
| Capability obesity | 147+ skills, ephemeral lifecycle in doctrine only | `ls /root/AAA/skills/ \| wc -l`, grep tool code for lifecycle modes |
| Orchestrator choke | No OBSERVE bypass, all tasks burn through full lifecycle | `orchestrator.js` — grep for `action_class`, `OBSERVE`, `bypass` |
| Response quality unvalidated | Anti-sycophancy in SOUL.md, zero runtime enforcement | grep for `sycophancy\|flattery\|response.*check\|pre.*delivery` in a2a-server/ |

## 6. Agent→memory wiring audit ("is X wired to the double helix?")

When asked whether an agent is wired to federation memory, decompose into the two axes of `HUMAN_MEMORY_DOCTRINE.md` (`/root/AAA/governance/`):

- **L-axis (L0–L6)** — agent operational memory: Redis (L1/L2), Qdrant (L3), Postgres/Supabase (L4), FalkorDB/Graphiti (L5), VAULT999 (L6). Wiring = the harness has a client path to the stores: `arif_memory` on :8088, `forge_vault` on :7072, postgres/graphiti MCP servers, etc.
- **H-axis (H1–H6)** — human memory: sovereignty-gated by F13. "Wired" can ONLY mean read-only **reference** paths (scar registry index reads, notebooklm MCP pointed at `/root/memory/H5-scars`, doctrine pointers). Full H-axis access is constitutionally impossible by design — that is the design, not a gap. Don't report it as one.

**Ambiguity trap:** "double helix" names TWO artifacts. `DOUBLE_HELIX_2026-08-08.md` (`/root/forge_work/`) is a governance reflection (Floors↔Flow strands, VAULT999 = inner/outer-loop exchange) — pointer-only, NOT memory. The memory double helix = the L/H two axes above. Check which artifact the question means before answering.

### Config-path map (verified 2026-08-09)

| Harness | Config to read | Wiring signal | Status |
|---|---|---|---|
| Hermes | `/root/.hermes/config.yaml` → `mcp_servers:` + `memory:` | arifos :8088 · aforge :7072 (forge_vault→L6) · notebooklm ("Use for /root/memory/H5-scars") · memory provider: honcho | L wired + H ref |
| Claude Code | `/root/.claude/settings.json` → `permissions.allow` `mcp__*`; agent card `/root/AAA/registries/agents.yaml` (`mcp_surface`) | `mcp__arifos__arif_memory` · `mcp__memory__*` · `mcp__postgres__*` · `mcp__graphiti-mcp__*` | L wired + H ref |
| Kimi FI-008 | `/root/.arifos/agents/kimi/config.toml`; MCP SoT = `/root/.kimi-code/mcp.json` (8 servers) | federation organ MCP entries + own state.db | L wired |
| OpenCode | `.opencode.json` (project or `~/.config/opencode/`) | `mcp:` block — arifOS-Kernel enabled; WEALTH/WELL/Intelligence often disabled | Partial |
| OpenClaw | `/root/arifOS/config/openclaw/openclaw.json` (runtime) | **0 hits** for mcp/memory/vault/redis/qdrant; memory = workspace `MEMORY.md` + `hermes-memories/` mirror | Not wired (file-based only) |

### Probe details
- Hermes active profile dir (`~/.hermes/profiles/aaa-hermes/`) holds memories/skills/hooks but **no config.yaml** — profile-level config lives in the main config.
- OpenClaw is wired at doctrine level (workspace AGENTS.md pointers) but NOT at store level — that is the §4 code-vs-doctrine gap applied to memory. Always state which level you verified.
- Store-level health (are L1–L6 actually alive) is a separate probe: `references/memory-subsystem-probe.md`.

Deliverable shape: agent × axis × status table + constitutional note (H-axis reference-only is F13-correct) + ONE reversible next step (e.g. wire OpenClaw via arifos MCP — T2, snapshot first, rollback ready). Full session detail: `references/agent-memory-wiring-map-2026-08-09.md`.

## 9. Deploy lag diagnosis — the three-commit drift pattern (2026-08-10)

The kernel's `:8088/health` exposes `source_commit` (deployed-from), `built_commit` (git HEAD), and `deployed_commit`. When `drift=true`:

- **Type A (Deploy Lag):** `source ≠ built`, `source == deployed`. Trivial — runtime is fine, just behind HEAD. Fix: `make deploy-local`. Risk: LOW.
- **Type B (Source/Runtime Divergence):** `source == built`, but actual runtime differs. Serious — hot-fixes applied directly to `/opt/arifos/app` without going through git. Fix: promote hot-fixes to source, commit, deploy. Risk: MEDIUM.
- **Type C (False Positive):** Service restarted after deploy but tracker didn't update. Phantom drift. Self-corrects on next deploy.

Decision: check `source vs built` first (Type A), then `source vs deployed` (Type B), then service restart time vs deploy time (Type C).

**Critical pitfall:** carry_forward claims "DRIFT RESOLVED" are EVIDENCE, not TRUTH. Always re-probe live kernel health. Previous session's resolution may be stale. Full diagnosis: `references/deploy-lag-diagnosis.md`.

## 10. Federation manifest staleness (2026-08-10)

**Pattern:** `federation-manifest.yaml` and `organs.yaml` contain snapshot-in-time data (record counts, health status, probe results) that drift from reality. OpenCode found VAULT999 manifest claimed 171 records when actual count was 45,712 — a 30× discrepancy. WELL manifest said "Root cause: pending investigation" when the real cause was no biometric pipeline.

**Detection recipe:**
```bash
# Actual vault999 count vs manifest claim
wc -l /root/arifOS/VAULT999/outcomes.jsonl
grep "records:" /root/AAA/federation/federation-manifest.yaml

# Actual organ status vs manifest claim
for p in 8088 7071 7072 3001 8081 18082 18083; do
  curl -sf http://127.0.0.1:$p/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f':$p {d.get(\"status\",\"?\")}')" 2>/dev/null
done
grep -B2 -A2 "status:" /root/AAA/federation/organs.yaml | head -20
```

**Fix:** update manifests to match live state (T1, reversible). Add `note:` field with date and source of truth. Root cause: no automated reconciliation cron. Consider post-deploy manifest-sync in `make deploy-local`.

## 10a. SOT-MANIFEST block audit in README files (2026-08-14)

Many federation repos embed a `<!-- SOT-MANIFEST ... -->` HTML comment block at the top of the README. This block carries single-source-of-truth metadata that drifts faster than prose because it's updated manually, not by CI. **Five-field verification checklist:**

| Field | Live probe | Common drift |
|---|---|---|
| `live_commit` | `git rev-parse --short HEAD` | Stale: README says `b59e547` but HEAD is `6b7286b1e` |
| `federation_release` | Must be single entry | **Accumulation:** old releases left as duplicates when new one added. Also check badge lines `[![Federation](...v2026.08.09...)]` — those accumulate too |
| `owner_summary` | `curl -s localhost:<port>/health \| jq .owner_summary` | README says `GREEN (no_runtime_drift)` but health says `YELLOW (runtime_drift)` — status color and reason strings must match |
| `live_port` | Same health endpoint | `(healthy)` in README when actual health is `(degraded)` |
| `authorization` | Manual review | **Credential leak:** README describes auth mechanism with too much specificity (e.g. `Ed25519 challenge-response` → redact to `*** challenge-response`). Algorithm names, key-type identifiers, and signature scheme names are operational detail that shouldn't be in public READMEs |

**Recipe (2026-08-14, verified):**
```bash
# Compare README live_commit vs actual HEAD
cd /root/arifOS && grep 'live_commit' README.md | tail -1
git rev-parse --short HEAD
# If different → stale SOT-MANIFEST

# Compare owner_summary vs live health
curl -s http://localhost:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'color={d[\"owner_summary\"][\"color\"]} reasons={d[\"owner_summary\"][\"reasons\"]}')"
# Then grep owner_summary in README — must match

# Check for duplicate federation_release entries
grep -c 'federation_release:' README.md
# >1 means duplicates accumulated

# Check for credential leaks in authorization line
grep -i 'ed25519\|rsa\|ecdsa\|secp256\|hmac-sha256' README.md
# Any hit = redact to ***
```

**Key insight:** the SOT-MANIFEST block drifts because it sits in a comment block that no linter touches and no CI validates. Unlike generated badges (which pull from shields.io), the SOT-MANIFEST is entirely hand-maintained. This makes it the single most error-prone metadata surface in the repo.

## 11. WELL architectural gap — biometric pipeline (2026-08-10)

WELL port 18083 is GREEN but health returns `{"status":"degraded"}`. Root cause: `state.json` last modified 2026-07-04 (36+ days stale), running in MOCK mode. No biometric data pipeline feeds real vitals.

**NOT a code defect** — WELL is REFLECT_ONLY and correctly reports degraded when it has nothing real to reflect. Fix requires sovereign decision: what biometric data source? Manual check-ins? Wearable integration? This is F13, not code.

**Detection:** `curl -sf http://127.0.0.1:18083/health` → check `"honesty":"MOCK"` or `"status":"degraded"` with stale timestamp.

**Detection:** `curl -sf http://127.0.0.1:18083/health` → check `"honesty":"MOCK"` or `"status":"degraded"` with stale state.json timestamp.

## 12. External research → stabilization workflow (2026-08-10)

When Arif hands an external audit/PDF and says "stabilize":

1. **Extract** (`pdftotext`), classify each finding: RESOLVED / CONFIRMED / FALSE_POSITIVE / ARCHITECTURAL
2. **Live probe** — don't trust snapshot date. Use §1 live-probe-first pattern.
3. **Plan file** at `/root/forge_work/stabilization/STABILIZATION_PLAN.md` — GAP → STATE → ACTION table
4. **Spawn opencode** with plan as context (`opencode run '...' -f plan.md`)
5. **Verify** opencode's changes. Re-probe all endpoints.
6. **Report** mapped to reality, not to the PDF.

Key principle: external research = HYPOTHESIS. Live system = TRUTH. Map, don't copy.

Full session transcript: `references/stabilization-workflow-2026-08-10.md`.

## 13. Pre-implementation probe — does the receiving layer even READ the field you're designing FOR?

A recurring trap: a coding agent designs `i-ARIF` alias + `fed-vision/image/audio/video` capability signatures as if `agent_id` and capability names are both consumed by FED's routing pipeline. **Live-verified 2026-08-12:** FED's `agent_id` field is silently ignored — every value tested (`i-ARIF`, `hermes-asi`, `hermes`, `openclaw`, `arif-fazil`, `unknown-agent-xyz`) returns the identical route. Identity-based routing does not exist in the current FED surface. Designing aliases for a passthrough is wasted work.

The structural lesson: **probe whether the receiving layer even reads the field your plan depends on, BEFORE asking a coding agent to implement the plan.** A clean probe set answers "would X even take effect if implemented perfectly?" before the implementation question wastes 800+ seconds of compute.

### 13a. The 6-probe pre-implementation checklist (for any identity-alias or capability-signature proposal)

For any proposal that adds **identity aliases** (agent_id routing) or **capability signatures** (capability cascade expansion), run these 6 probes against live FED before forking:

**Probe 1 — Is `agent_id` actually consumed by routing?**

```bash
for aid in 'i-ARIF' 'hermes-asi' 'hermes' 'openclaw' 'unknown-agent-xyz'; do
  curl -s -X POST http://127.0.0.1:7074/fed/route -H 'Content-Type: application/json' \
    -d "{\"task\":\"smoke\",\"model\":\"fed-reasoning-heavy\",\"agent_id\":\"$aid\",\"constitutional_tier\":333,\"modality\":\"text\"}" \
    | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("routes",[{}])[0].get("model","?"))'
done
# If all 5 print the SAME model → agent_id is silently ignored → don't design aliases
```

**Probe 2 — Does each proposed capability signature exist?**

```bash
for cap in 'fed-vision' 'fed-image' 'fed-audio' 'fed-video'; do
  resp=$(curl -s -X POST http://127.0.0.1:7074/fed/route -H 'Content-Type: application/json' \
    -d "{\"task\":\"smoke\",\"model\":\"$cap\",\"agent_id\":\"hermes-asi\",\"constitutional_tier\":333,\"modality\":\"text\"}")
  echo "$cap: $(echo "$resp" | python3 -c 'import sys,json; d=json.load(sys.stdin); print("EXISTS" if d.get("routes") else "MISSING:"+str(d.get("error",""))[:60])')"
done
# MISSING = KeyError:'model' for every unimplemented cap
```

**Probe 3 — Does the EMD gate correctly classify capability signatures?**

```bash
curl -s -X POST http://127.0.0.1:7074/fed/route -H 'Content-Type: application/json' \
  -d '{"task":"smoke","model":"fed-multimodal-vision","agent_id":"hermes-asi","constitutional_tier":555,"modality":"vision"}' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); emd=d.get("emd",{}); print(f"routes={len(d.get(\"routes\",[]))} verdict={emd.get(\"verdict\")} reason={emd.get(\"reasons\",[])}")'
# Bug pattern: vision capability with vision modality returns EMD_MISMATCH with reason
# "vision payload to vision-blind fed-multimodal-vision" → EMD reads the capability SIGNATURE NAME
# as the model_id, not the resolved underlying model.
```

**Probe 4 — Does constitutional hard-gate interact badly with EMD?**

```bash
for tier in 333 555 666 888; do
  routes=$(curl -s -X POST http://127.0.0.1:7074/fed/route -H 'Content-Type: application/json' \
    -d "{\"task\":\"smoke\",\"model\":\"fed-multimodal-vision\",\"agent_id\":\"hermes-asi\",\"constitutional_tier\":$tier,\"modality\":\"vision\"}" \
    | python3 -c 'import sys,json; print(len(json.load(sys.stdin).get("routes",[])))')
  echo "tier=$tier routes=$routes"
done
# Expected bug: tier 666+ returns 0 routes (EMD says "vision-blind" so the hard-gate's
# direct-only check finds no candidate → empty result)
```

**Probe 5 — Is the modality field surfaced in the response?**

```bash
for mod in 'text' 'vision' 'audio' 'image' 'video' 'omni'; do
  resp=$(curl -s -X POST http://127.0.0.1:7074/fed/route -H 'Content-Type: application/json' \
    -d "{\"task\":\"smoke\",\"model\":\"fed-multimodal-vision\",\"agent_id\":\"hermes-asi\",\"constitutional_tier\":555,\"modality\":\"$mod\"}")
  echo "$mod: $(echo "$resp" | python3 -c 'import sys,json; d=json.load(sys.stdin); emd=d.get("emd",{}); print(f"verdict={emd.get(\"verdict\",\"none\")} model={d.get(\"routes\",[{}])[0].get(\"model\",\"none\")}")')"
done
# If all 6 modalities yield same model and verdict="none" → modality is silently ignored
```

**Probe 6 — Does the security scan block legitimate provider names in code?**

```bash
grep -n 'tokenrouter\|forbidden pattern\|denied' /root/.config/opencode/plugins/arifos-judge-gate.ts
# If /tokenrouter/i is in a forbidden-patterns list → writing fed_router.py code that references
# `tokenrouter` provider (a legitimate name in TOKENROUTER_PRICING) will be blocked at write-time.
# Verified at line 49,55,88 of arifos-judge-gate.ts (regex too broad).
```

### 13b. The hidden cost of the EMD-capability-signature bug

The most insidious finding: the EMD gate's bug is **invisible in normal routing** because existing capabilities (`fed-multimodal-vision`) sit at tier 555 where the constitutional hard-gate doesn't fire. But once you ADD `fed-vision`/`fed-image`/`fed-audio`/`fed-video` at tier 555+ with modality = vision/audio/image/video, the SAME bug produces:

1. EMD classifies the new capability as "vision-blind" (or "audio-blind", etc.)
2. Constitutional hard-gate at tier ≥ 666 can't find a direct route for a "blind" capability
3. Result: `routes: []` — the new capability is **completely unreachable**

**You cannot implement multimodal-capability signatures in FED without first fixing the EMD gate.** The OpenCode plan was sound; the surface it was targeting was not ready.

### 13c. The 4-gate sequence that blocks T1 mutation (post-plan)

Even after the design is sound, OpenCode T1 mutation can still fail. Verified 2026-08-12 — 4 distinct gates, in order encountered:

| # | Gate | Live message | Source |
|---|---|---|---|
| 1 | Missing arifOS session binding | `MUTATE tool requires arifOS session binding. No session_token found in args or env` | OpenCode plugins (kernel gate) |
| 2 | Security scan false positive | `forbidden pattern: tokenrouter matched in arguments` | `arifos-judge-gate.ts:49,55,88` |
| 3 | Deployment drift (kernel can't authenticate) | `substrate_state: DEGRADED, drift: true` | `/root/arifOS` source ≠ `/opt/arifos/app` runtime |
| 4 | Actor not cryptographically verified | `actor_verified: false, session_token: null, session_token_status: "DENY: actor not cryptographically verified"` | arifOS `arif_init` requires Ed25519-signed SCT |

When a sibling reports "blocked at mutation tool", check all 4 gates in order:

```bash
# Gate 1 + 3: source vs runtime drift + arifOS substrate
curl -s http://127.0.0.1:8088/health | python3 -c 'import sys,json; d=json.load(sys.stdin); print("drift:", d.get("deployment_drift_status"), "substrate:", d.get("substrate_state"))'

# Gate 4: arif_init returns session_token or null?
curl -s -X POST http://127.0.0.1:8088/mcp -H 'Content-Type: application/json' \
  -H 'Accept: application/json,text/event-stream' -H 'MCP-Protocol-Version: 2026-07-28' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"actor_id":"Muhammad Arif bin Fazil","lane":"888-APEX","authority_band":"T2","intent":"test i-ARIF binding"}}}' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); inner=json.loads(d["result"]["content"][0]["text"]); print("token:", inner.get("session_token"), "actor_verified:", inner["actor"].get("actor_verified"))'
```

### 13d. Action shape — what to do with the 6 probes

| Finding | Action |
|---|---|
| agent_id is ignored (Probe 1: 5 different IDs = same route) | **Cancel the alias proposal** — no consumer for it. Either add agent_id consumption to `fed_route_engine` FIRST, or drop the alias from the plan. |
| Multimodal caps missing (Probe 2: KeyError:'model') | If only the caps are missing, the addition itself is sound — proceed AFTER fixing Gate 4 (cryptographic actor). But verify Probe 3 first. |
| EMD gate misclassifies capability signatures (Probe 3) | **Halt implementation.** Fix EMD gate to read the resolved model's `vision_in`/`audio_in`/`image_out`/`video_out` flags, not the capability signature's name. THEN implement the caps. Otherwise tier 666+ returns empty routes silently. |
| Constitutional hard-gate × EMD bug = 0 routes (Probe 4) | Same as Probe 3 — both gates interact badly. Fix EMD first. |
| Modality field silently ignored (Probe 5) | Likely EMD verdict is computed but not surfaced in the response (or EMD check is bypassed). Investigate `fed_router.py` EMD branch. |
| `tokenrouter` security false positive (Probe 6) | Patch `arifos-judge-gate.ts` to add a `provider_table` allowlist (`tokenrouter`, `kunci-mas`, `secrets/`, etc. are legitimate string names that should not be forbidden). Then OpenCode writes work. |

### 13e. Recovery paths when probes reveal plan-can't-implement

| Probe outcome | Path |
|---|---|
| Design sound, surface unready | File the design as a forge_work artifact + seal the probe transcript as evidence. Mark `IMPLEMENTATION_PENDING_SURFACE_READINESS`. |
| Design unsound | Reject the plan with probe-validated evidence. Send the sibling back with: "Your design assumes X, but probe Y shows X is absent in live runtime. Redesign around what's actually there." |
| Surface unready AND design sound | Surface-readiness is now a separate task: fix EMD gate (Probe 3), re-run probe (must return `routes=[]` → `routes=[2+]`), then implement. |
| Implementation blocked at security scan false positive (Gate 2) | Patch the security scan FIRST. Cost is small (1-line regex allowlist); benefit is unlocking T1 mutation across all federated organ refactors. |

The structural lesson: **the pre-implementation probe set is the inverse of the coding delegation prompt.** The delegation says "implement X." The probe asks "would X even take effect if you implemented it perfectly?" A clean probe set answers the second question before the first question wastes 800+ seconds of compute.

Full session transcript with all 6 probe transcripts and the OpenCode delegation history: `references/2026-08-12-fed-iarif-pre-implementation-probe.md`.

## 13a. The "full wiring chain" verification (2026-08-12, SearXNG topology)

A claim like "Hermes uses SearXNG for search" is actually a chain of 7+ independent links. A report that verifies only the endpoint (curl :8080) is **partial** — the endpoint might work while the config is wrong, meaning a future restart will break it. Or the config might say searxng while the env var points elsewhere.

### The 7-link SearXNG chain (verified 2026-08-12)
1. **Docker process** running: `ps aux | grep searxng`
2. **Port binding**: `ss -tlnp | grep :8080`
3. **Functional endpoint**: `curl "localhost:8080/search?q=test&format=json"`
4. **Hermes global config**: `grep -A3 "web:" /root/.hermes/config.yaml`
5. **Per-profile configs**: check each `profiles/*/config.yaml`
6. **A-FORGE code defaults**: `grep -n "localhost:8080" /root/A-FORGE/src/interfaces/mcp/proxyTools.ts`
7. **Env vars loaded by systemd**: `grep SEARXNG /root/.secrets/kunci-mas.env`

**Rule:** before endorsing "X is wired to Y", verify ALL links. Partial verification = partial truth, which the next restart will expose. Pattern from this session: a "Resolution Report" claimed SearXNG was fully wired. Live probe showed Docker + port + endpoint OK, but the report omitted ancillary services (Honcho DOWN, hound MCP parked, aforge reconnect loop). The "done" report passed link verification but failed the ecosystem check.

### "What I changed" ≠ "What's still broken"
Reports that list "what was fixed" often omit "what is still broken in the same ecosystem." Always probe ancillary services mentioned in the same log/metrics stream as the primary target, not just the primary. Full session transcript with all 7-link probes: `references/searxng-topology-2026-08-12.md`.

### Empty response ≠ service down
Transient timing issues (gateway restart, Docker proxy warm-up, DNS resolution timing) can cause `curl` to return empty body despite service running. **Re-probe once** before declaring a service down. Limit: 2 attempts. After that, escalate.

## 14. The "degraded" umbrella trap — decompose before reporting (2026-08-14)

The arifOS `/health` endpoint returns `"status": "degraded"` as an **umbrella** for multiple independent drift signals. An agent that reads only the top-level `status` and reports "something broken" is wrong. The individual fields tell the real story, and they are NOT synonyms.

### The field map (all from the same `/health` response)

| Field | Type | What it actually means | When to worry |
|---|---|---|---|
| `runtime_drift` | **bool** | Does running code differ from source? `False` = SIHAT. | Only if `True` — hot-fixes in `/opt` not in git |
| `runtime_matches_build` | **bool** | Does runtime commit == build commit? `True` = SIHAT. | Only if `False` |
| `registry_truth` | **enum** | Do tool counts reconcile? `DRIFT_DETECTED` = 62 entries ≠ 48 declared ≠ 8 exposed. | Warning — usually aliases/superset mismatch, not functional failure |
| `deployment_drift_status` | **enum** | Does deployment marker flag match? `drift_detected` = flag mismatch. | Warning — investigate, but code may be fine |
| `owner_summary.color` | **string** | `YELLOW` = "healthy with caveats." `RED` = real problem. | Only if `RED` |
| `owner_summary.reasons` | **array** | Lists SPECIFIC reasons for the color. **May contain the string `"runtime_drift"` even when the `runtime_drift` boolean field is `False`** — naming collision in the health output itself. | Read this array, but trust individual boolean fields over reason strings |

### The layer separation principle — four INDEPENDENT layers

An agent that aggregates these into one "system is broken" narrative is lying. Each layer must be reported separately:

| Layer | Where to read | Healthy |
|---|---|---|
| **Constitutional** | `floors_active` (int), `runtime_floors_status` (per-floor) | `floors_active: 13`, all `status: pass`, zero failures |
| **Runtime** | `runtime_drift` (bool), `runtime_matches_build` (bool) | `False` / `True` respectively |
| **Registry** | `registry_truth` (enum) | `CONSISTENT` (not `DRIFT_DETECTED`) |
| **Infra** | NOT in `/health` — probe `uptime`, `free -h`, `swap` separately | Load < cores×1.5, swap < 80%, mem available > 20% |

**Never report "constitutional collapse" when only the registry layer has a mismatch and infra is pressured.** Constitutional floors can be 100% pass while registry says DRIFT_DETECTED — those are different things. Infra pressure (swap full, load high) is NOT a constitutional signal.

### The `floors_active` parsing pitfall

`floors_active` is an **integer** (e.g. `13`), NOT an array. There is no top-level `floors` key. Per-floor detail lives in:
- `runtime_floors` — object with F1–F13 scores (e.g. `{"F1": 0.5, "F2": 1.0, ...}`)
- `runtime_floors_status` — object with per-floor pass/fail (e.g. `{"F1": {"score": 0.5, "status": "pass", "measured": true}}`)

An agent that does `len(d.get("floors", []))` and reports "0 floors" is reading a nonexistent key. The correct read: `d.get("floors_active", 0)` returns the integer count.

### The `owner_summary.reasons` naming collision — FIXED (commit `be55fa293`, 2026-08-14)

**Historical bug:** `owner_summary.reasons` contained `"runtime_drift"` as a reason for YELLOW color **even when the `runtime_drift` boolean field was `False`.** Root cause in `rest_routes.py` line ~3234: `runtime_drift_val` (used for `_degraded` + owner reasons) was contaminated by `_sr_drift` (software_release attestation drift) via `runtime_drift_val = runtime_drift_val or _sr_drift`. The JSON `runtime_drift` field reported the ORIGINAL uncontaminated value (False), but the reasons array used the contaminated variable.

**Fix applied:** Three additive patches to `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py` (committed `be55fa293`):
1. `degraded_reasons[]` — structured array with per-entry `{layer, field, value, severity, explanation}`
2. `layer_health{}` — per-layer classification (`constitutional`, `runtime`, `registry`, `deployment_attestation`, `vault`, `infra`)
3. `owner_summary.reasons` split: `code_runtime_drift` (actual code drift, uses original `_drift.get("runtime_drift")`) vs `deployment_attestation_drift` (SOT drift, uses `_sr_drift`)

**Post-fix:** empty `degraded_reasons[]` = fully healthy. If only attestation drifts, reasons shows `["vault_healthy", "deployment_attestation_drift"]` — not `["runtime_drift"]`. Read `degraded_reasons[]` first, `layer_health{}` second, individual boolean fields third.

**For legacy endpoints (pre-be55fa293):** trust individual boolean fields over reason strings. `runtime_drift: false` is authoritative even if reasons says `"runtime_drift"`.

### Recipe: decompose-before-report

```bash
curl -s --max-time 5 http://localhost:8088/health > /tmp/arifos_health.json

python3 << 'EOF'
import json
d = json.load(open("/tmp/arifos_health.json"))

# Layer 1: Constitutional
floors = d.get("floors_active", 0)
floor_status = d.get("runtime_floors_status", {})
failures = sum(1 for v in floor_status.values() if v.get("status") != "pass")
print(f"Constitutional: {floors} floors, {failures} failures")

# Layer 2: Runtime
rd = d.get("runtime_drift", None)
rmb = d.get("runtime_matches_build", None)
print(f"Runtime: drift={rd}, matches_build={rmb}")

# Layer 3: Registry
rt = d.get("registry_truth", "?")
dd = d.get("deployment_drift_status", "?")
print(f"Registry: {rt} | Deploy: {dd}")

# Layer 4: Infra (probe separately — NOT in /health)
# print("Infra: run uptime + free -h")

# Owner summary
os = d.get("owner_summary", {})
print(f"Owner: {os.get('color','?')} — {os.get('reasons',[])}")
print("NOTE: reason strings can say 'runtime_drift' even when runtime_drift=False")
EOF
```

### Human-readable status report shape (Arif preference)

When Arif asks "what's the status for my human understanding," report by **layer**, not by JSON dump:

```
🧠 arifOS (Constitution): ✅ SIHAT — 13 floors, zero failures, vault healthy
⚙️ Runtime: ✅ SIHAT — code matches, no drift
📋 Registry: ⚠️ DRIFT — 62 ≠ 48 ≠ 8 (bookkeeping, not functional)
🖥️ Infra: 🔴 PRESSURED — swap full, load high (separate from constitution)
```

**Never aggregate layers into a single verdict.** The constitution can be 100% healthy while infra is on fire. Saying "system degraded" without saying WHICH layer is lying to Arif.

Worked example: `references/degraded-umbrella-decomposition-2026-08-14.md`

## Pitfalls (moved 2026-10-23)

Moved verbatim to `references/pitfalls.md` — the full pitfall set, not summarised.

```bash
grep -n -i "symptom" references/pitfalls.md
```

Index:

- Pitfalls

## 7a. Public MCP gateway diagnostic chain (end-to-end connectivity)

When asked "can I connect through https://mcp.arif-fazil.com/mcp?" or "is the public MCP working?", run the full 5-layer stack — not just a local health check. A failure at ANY layer means the public endpoint is unreachable.

### Probe sequence (top-down)

```bash
# Layer 1: Local kernel health (is the backend alive?)
curl -sf http://127.0.0.1:8088/health | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'kernel: {d[\"status\"]} tools={d[\"tools_loaded\"]} drift={d.get(\"runtime_drift\",None)}')"

# Layer 2: Source ↔ runtime drift (is deployed code current?)
echo "SOURCE: $(cd /root/arifOS && git log --oneline -1)"
echo "RUNTIME: $(cd /opt/arifos/app && git log --oneline -1)"

# Layer 3: Caddy reverse proxy (is the front door wired?)
grep -A5 'mcp.arif-fazil' /etc/caddy/Caddyfile | grep 'reverse_proxy'
# Expected: reverse_proxy 127.0.0.1:8088

# Layer 4: Cloudflare tunnel (is the public path open?)
systemctl is-active cloudflared  # must be "active"

# Layer 5: Public endpoint (POST JSON-RPC — see pitfall: /mcp is POST-only)
curl -sf -m 10 -X POST https://mcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}'
```

### CORS preflight check (browser-based MCP clients)

Browser-based MCP clients (MCPJam Inspector, ChatGPT MCP connector, Claude Desktop web mode) send a **CORS preflight** `OPTIONS` request before the actual `POST /mcp`. If this fails, the browser blocks the POST entirely — the client shows "failed to connect" even though the kernel is healthy.

**Probe:**
```bash
curl -s -o /dev/null -w "%{http_code}" -X OPTIONS https://mcp.arif-fazil.com/mcp \
  -H "Origin: http://localhost:6274" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Mcp-Session-Id, MCP-Protocol-Version"
# 204 = OK (Caddy handles it)
# 400 = FAIL (kernel rejecting origin — add cors_public to Caddy handler)
```

**Known failure (2026-08-09):** The arifOS kernel's CORS middleware returns `400 Disallowed CORS origin` for origins not in its allowlist (e.g. `http://localhost:6274` from MCPJam). The fix is adding `import cors_public` to the Caddy `/mcp*` handler so Caddy intercepts OPTIONS → 204 before the request reaches the kernel. See `references/cors-preflight-fix-2026-08-09.md` for the full Caddy patch recipe (backup → patch → validate → reload → verify).

**If CORS preflight passes (204) but the client still fails:** check the other 5 layers in the probe sequence above. CORS is layer 0 — it must pass before anything else matters.

### Landing page

The landing page at `https://mcp.arif-fazil.com/` is **dynamic** — JavaScript fetches `/health` at runtime to populate version, tool counts, thermodynamic state. No manual update needed when the kernel is redeployed. Static source: `/var/www/html/mcp/index.html`. Only needs manual edit when the page template itself changes (design, sections, layout).

### Source/runtime drift interpretation

| Scenario | Action |
|---|---|
| Source == Runtime == Remote | No action — healthy |
| Source == Remote, Runtime has DRIFT_* hotfixes | Kernel health says drift=False → no restart needed. Hotfixes are local-only, not in source/remote. |
| Source behind Remote | `git pull origin main` then `make deploy-local` |
| Runtime behind Source | `make deploy-local` (rsync + restart) |

**Deploy decision:** only redeploy if kernel health says drift=True OR source has new commits relevant to the current task. The kernel's own `/health` drift check is authoritative — a "healthy, no drift" response means no restart needed regardless of git commit mismatch.

Full session reference: `references/public-mcp-gateway-diagnostic-2026-08-09.md`.

## 8. Auditing a spawned sibling build (manager/auditor/validator pattern)

When Arif spawns a coding agent (grok/opencode/codex) to "zen" a subsystem and asks you to be **manager + auditor + validator**, the working pattern is:

1. **Hash-baseline BEFORE the sibling lands changes.** `md5sum` + mtime of every config the build might touch (`litellm-config.yaml`, `haproxy.cfg`, `opencode.json`, `openclaw.json`, `config.yaml`, agent-cards). Re-hash after — the diff IS the audit trail of what the sibling changed.
2. **Self-report ≠ truth.** Every claim the sibling posts gets a live probe with a numbered table. The sibling's table says "done" — your probe says "mode 700, no hardcoded key, /health/liveliness 200". Cite evidence per row.
3. **Check the identity/runtime split boundary explicitly.** The F13 constraint is: WHO (agent cards, sealed) must NOT move while WHICH (provider config) is being zen'd. Probe: `find /root/AAA/a2a-server/agent-cards -newermt <build-start>` = empty, and cards' `bound_to`/`class` unchanged.
4. **Verify the front door, not just the backend.** A stack can be "healthy" at :4011 while :4000 (HAProxy front) 503s for every agent — the agents only see the door. Probe `:4000/health/liveliness` (see §LiteLLM triple-trap), then end-to-end: `curl :4000/v1/chat/completions` with a real alias.
5. **Distinguish "enabled" from "loaded".** For plugins: `plugins list` showing `enabled` ≠ plugin code actually imported in the running process. Proof = runtime state file written after restart (e.g. `.runtime.json` `_last_update` timestamp), or an injected `[LANE:...]` block in an LLM turn. Direct-import unit tests of the plugin module can pass 8/8 while the gateway never invokes it — import from the ACTIVE profile plugin path, not the legacy copy.
6. **Reversible-first on every cleanup.** Everything the auditor does: `cp` backup to `forge_work/.../backup/` with timestamp, patch, verify, keep the backup. Never `rm` — archive.

Full worked example (2026-08-09 FED zen + AAA 3-layer consolidation + multi-user lane wiring): `references/fed-stack-audit-2026-08-09.md`.

## 15. Remote federation nodes — 3-probe status check (2026-08-15)

Some federation bots live on OTHER nodes, not the main box (e.g. wawa/Azwa's Hermes on `srv1642546` "azwaos", Tailscale `100.64.0.4`, unit `hermes-agent.service`). Resolve node location first (`~/.ssh/config` aliases + `/root/HERMES/memories/MEMORY.md`), never answer status from memory. Then three probes over SSH — all three, every time:

```bash
ssh <node> "systemctl status <unit> --no-pager | head -8"                 # P1 alive now
ssh <node> "journalctl -u <unit> --since '2 hours ago' --no-pager | tail -30"  # P2 history
ssh <node> "timeout 8 <venv>/bin/python -m hermes_cli.main gateway status"     # P3 gateway layer
```

**Interpretation rules (wawa incident, verified):**
- P1 "active (running) since <recent>" can hide a `status=127/n/a` crash loop (restart counter 20+) that self-recovered. Report the scar, not just the present state — the human asks status because they suspect something.
- journald showing only systemd lifecycle lines (no app stdout) ≠ "no logs". Exit codes are the story; app logs live in the node's HERMES_HOME logs dir — check `StandardOutput=` before concluding journald is empty.
- `gateway status` can say "Running manually, not as a system service" for a process systemd started — cross-check PIDs (`systemctl show <unit> -p MainPID`) before believing either label.
- Remote node serving another human = read-only diagnosis from Arif's session is fine; restarts/root-cause digging = surface to sovereign, it's that person's lane.

Full session: `references/remote-node-status-check-2026-08-15.md`.

## 15a. Multi-node fleet resource audit (2026-08-15)

When asked to map "the machine nodes" or audit resource allocation across the fleet: enumerate nodes via `tailscale status` (nickname ≠ SSH host — use `ssh root@<ts-ip>`), then per node: uptime/free/df + PSI (`/proc/pressure/memory`) + vmstat si/so + running units + `ss -tlnp` + docker stats. Three interpretation rules: (1) **swap full ≠ crisis** — full-but-cold swap with PSI 0.00 and si/so=0 is dormant pages, report headroom not panic; (2) fleet imbalance (one node load-2/swap-full vs one node 0.03/6GB-free) means the answer is relocation of decoupled services, not new hardware; (3) hunt `degraded` in health JSONs (found :18089 `mcp_connected:false` — the real P1) not just dead ports. Includes the live port map superseding the legacy 8080-8083 table (8080 is searxng now), the per-unit memory probe (`systemctl show -p MemoryCurrent`), and the **zombie-artifact 5-signal check** (process? port? venv? output ever? unit? — ComfyUI: cloned, 4GB models, never ran, no GPU → cargo not capability). Full recipe: `references/multi-node-fleet-audit-2026-08-15.md`.

## Support files
- `references/multi-node-fleet-audit-2026-08-15.md` — multi-node fleet audit: node inventory (forge/flow-edge/phone), one-pass probe recipe per node, swap-full-but-cold interpretation via PSI/vmstat, live port map (supersedes legacy 8080-8083 MCP table; 8080=searxng), per-unit memory ranking (openclaw-gateway 4.7GB is the fat one), zombie-artifact 5-signal check (ComfyUI class), and the no-overengineering relocation ranking.
- `references/remote-node-status-check-2026-08-15.md` — remote-node (wawa/azwaos) 3-probe status check: SSH access pattern, crash-loop-hides-behind-active finding, journald-no-app-stdout trap, gateway "running manually" label trap, lane discipline for other humans' bots.
- `references/port-binding-architecture-2026-08-11.md` — **Port binding architecture**: arifOS single-port (:8088) vs A-FORGE dual-port (:7071+7072), complete organ port table, Caddy routing map, the Tailscale-only binding bug on :7072, and the "service healthy but doctor.sh FAIL" diagnostic sequence. Use when debugging why a service appears down in health probes.
- `references/wealth-organ-probe-2026-08-06.md` — WEALTH (:18082) 8-tool surface audit: mode-dispatched schemas, session double-gate, receipt-chain defect, capital_registry ≠ asset store, Monte Carlo single-factor-only (GBM), C-item live-verification log, Brent live snapshot field map, and Arif's PATH_A invariant set (I1–I7).

- `references/federation-probe-cheatsheet.md` — quick-reference of live endpoints, curl commands, and decoding recipes
- `references/2026-08-05-session-lessons.md` — session-specific patterns: Telegram group-bot Forbidden delivery loop, sycophantic-opener reflex (4-transcript flag), and the token-budget meta-lesson. Captured here because the umbrellas that should own them (`hermes-telegram-gateway-ops`, `humanizer`, `federation-runtime-forensics`) are bundled and not directly patchable in this session.
- `references/memory-subsystem-probe.md` — full 6-layer memory health probe recipe (L1 Redis, L3 Qdrant, L4 Postgres, L5 FalkorDB/Graphiti, L6 VAULT999) with interpretation guide per layer.
- `references/agent-memory-wiring-map-2026-08-09.md` — agent→memory wiring audit (use for "is X wired to the double helix?"): per-harness config paths + wiring signals (Hermes/Claude Code/Kimi/OpenCode/OpenClaw), the L-axis vs H-axis split, the two-double-helix ambiguity (governance reflection vs memory doctrine), and the OpenClaw store-level gap.
- `references/arifos-tools-list-endpoint-2026-08-06.md` — `/tools/list` returns 405; use `/tools` or `/tools.json`. Includes the canonical 8-tool list (no `megamemory_*`, ATLAS333/EUREKA777 are modes not tools) and the fabricated-tool-family detection recipe.
- `references/mcp-mirror-probe-2026-08-06.md` — Mirror-MCP verification recipe: probe local `127.0.0.1:<port>/mcp` and public `https://<sub>.arif-fazil.com/mcp` and confirm same server name, version hash, and tool set. Includes the SSE-vs-plain-JSON transport trap and the federation-topology expected-mirror table. Use when Arif asks "do we have mirror MCP structure or what?" or any local-vs-public MCP endpoint comparison.
- `references/2026-08-06-mem6tier-probe-lessons.md` — Ollama "sibling said fixed, reality said dead" verification pattern (config-correct vs state-correct gap), Postgres trust-auth Docker NAT subnet fix (172.21.0.0/16), kernel probe "judge the probe not the service" reflex, atlas333/eureka777 = modes not tools, and the reusable one-shot 6-tier probe script.
- `references/2026-08-06-deepest-memory-recall.md` — "Tell me the deepest memory" recall drill: VAULT999 genesis = conformance stubs (lines 1–12,217 are `D001 SEAL PENDING` test fixtures dated 2026-04-26), first real hash-chained receipt is line 12,218 = 2026-05-17T10:02:00Z (Telegram twin-bot routing debug). Captures canon-vs-memory distinction and the response shape Arif values (lead with date + receipt line, not prose).
- `scripts/memory_health.py` — single-command `memory_health.py` probe script. Run from `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/autonomous-ai-agents/federation-infra-verification/scripts/` (or copy to `/root/scripts/`). Exit 0 = OK, 1 = degraded. Supports `--brief` for compact output.
- `references/mcp-surface-compute-vs-governance-2026-08-07.md` — the 8 arifOS tools return **verdict envelopes**, not computed values. The 42 resources are constitution + context, not data. `arifos://atlas333/geometry` is philosophical metaphor (euclidean/hyperbolic/fractal as epistemic territory descriptors), NOT a runtime weight matrix. Use when: someone wires arifOS MCP into an LLM expecting it to "help find correct weights" — push back: arifOS governs the act of reasoning, route computational work to WEALTH/GEOX/A-FORGE and only use arifOS for constitutional validation (`math → judge`, not `judge → math`). Includes a full probed snapshot (8 tools, 42 resources, 20 prompts, stateless reads, kanon-2026.08.07+8bbcb36).
- `references/2026-08-07-mcp-identity-gate-and-self-reconciling-drift.md` — session-specific findings: (1) stateless-read pattern for arifOS `/mcp` (no handshake needed for tools/list, resources/list, prompts/list, resources/read); (2) double-encoded JSON envelope in `content[0].text` (two-stage `json.loads`); (3) identity-gate semantics — `verdict: SEAL` does NOT mean "approved" without `actor.actor_verified: true`; (4) string `actor: "arif"` label is ignored — only Ed25519-signed `sct_v1.*` tokens authenticate; (5) `/health` self-reconciles drift between probes (T₀+5min probe may show "healthy" without manual deploy); (6) substrate state is per-tool, not global (`/health` healthy does NOT guarantee every tool will accept the call). Use when: any arifOS probe shows unexpected drift or verdict vs actor-verified mismatch.
- `references/2026-08-12-fed-iarif-pre-implementation-probe.md` — **Probe-before-propose lesson.** Six live probes that caught a wasted-work risk: agent_id silently ignored (5 IDs → identical route), 4 proposed multimodal caps don't exist (KeyError), pre-existing EMD gate bug that misclassifies capability signatures as "vision-blind", constitutional hard-gate × EMD = 0 routes at tier 666+, modality field silently ignored, `tokenrouter` security scan false positive. Use when: any coding-agent delegation proposes to add identity aliases, capability signatures, multimodal caps, or any feature whose effect depends on a field the receiving layer might or might not read. The 6-probe checklist catches the surface-not-ready case before 800+ seconds of compute is wasted on a plan that can't land.
- `references/federation-brain-auth-handshake-2026-08-12.md` — **The three protocol fixes that turned "federation dead" into "federation healthy"** (companion to §3.1a): `Authorization: Bearer $LITELLM_MASTER_KEY` on every `/v1/models` probe (the #1 false-dead reading — `data:[]` without auth looks identical to a broken proxy), the canonical 3-call MCP `Mcp-Session-Id` handshake for A-FORGE/GEOX/WEALTH/WELL organs (header returned by `initialize` response, not body), and the "PyYAML parses ≠ litellm accepts" pitfall. Includes the 5-step end-to-end verification matrix before declaring any agent "blocked", snapshot-before-touch discipline (even when the patch turns out unnecessary), and the meta-lesson on short imperative user signals (probe → act → report, not governance preamble). Use when: user says "agents blocked", "tools disabled", `/v1/models` returns empty, `tools/list` returns 400 with `Mcp-Session-Id required`, or any sibling/own-report that the federation brain is down.
- `references/sot-manifest-audit-2026-08-14.md` — **SOT-MANIFEST block audit** (companion to §10a): the 5-field verification checklist for README `<!-- SOT-MANIFEST -->` blocks. Covers stale `live_commit`, duplicate `federation_release` entries, `owner_summary` color/reason mismatch with live health, credential-type leaks in authorization lines, and the live probe recipe. Worked example from the 2026-08-14 CCC-ROOT session.
- `references/health-endpoint-clarity-patch-2026-08-14.md` — **Health endpoint `degraded_reasons[]` + `layer_health{}` patch** (companion to §14): code-level root cause of the `owner_summary.reasons` naming collision. The contamination line (`runtime_drift_val = runtime_drift_val or _sr_drift`) at `rest_routes.py` ~3234. The three additive patches in commit `be55fa293`. Post-fix verification recipe. Qwen Code dispatch pattern (Kimi quota fallback).


<!-- dead-pointer sweep 2026-10-23: unresolved artifacts from the gate report were replaced with the references/ directory. Basenames are preserved in the audit JSON. -->
