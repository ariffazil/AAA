# Archived Session Archaeology — live-probe-audit-pattern + live-multiwriter-audit

> Session-specific worked examples, scar narratives, and detailed pitfall stories removed during the v2 merge (2026-09-17).
> These are historical evidence, not active procedures. Reference them when a new audit hits the same class.

## Reader-Called-but-Empty: HIB Dormancy (2026-08-13)

**Signal:** Access log shows Qdrant `query_points` count ZERO over 24h, yet code path exists.

**First, prove the reader fires under the SERVICE's own venv:**
```python
import sys, os
sys.path.insert(0, "/opt/arifos/app")
os.environ.setdefault("PYTHONPATH", "/opt/arifos/app")
from arifosmcp.hib import HibGate
gate = HibGate()
r = gate.interrogate_sync(query_text="<real query>", tau_threshold=0.0, limit=5)
print(r.verdict, r.match_count, r.error)   # tau=0.0 MUST match everything
```

**CRITICAL:** Run under the service's interpreter (`/opt/arifos/venv/bin/python`), not bare `python3`. Wrong env produces false "dormant" verdict.

**The smoking-gun:** cosine search with threshold=0.0 returning ZERO hits is a FILTER problem, not similarity. The WRITER stored points with `blast_radius=<NONE>` — the field was never populated at write time. Every query got classified L3/L2/L1, the filter required matching labels, no stored point had a label, result was `HIB_NONE` silently forever.

**Fix options:** (A) writer populates field at write time (root cause), (B) reader skips filter when no point carries it. Do NOT change the tau threshold — it's not the problem.

## Hash-Chain Integrity Audit (2026-08-13)

**The trap:** `SEALED_EVENTS.jsonl: prev_hash[N+1] != chain_hash[N] for 956 events (71.5%)` — false alarm.

**Three probe methods, three answers:**
- Row-order comparison → ~71% "broken" (wrong: file order ≠ chain order)
- `chain_position` linear order → ~99.9% "broken" (wrong: many records are chain ROOTS)
- **Lineage-aware (GENESIS = valid root)** → ~0.3% genuinely broken (CORRECT)

952/957 chained records carry `prev_hash = GENESIS` — independent chain roots, not broken links.

```python
prev_lineage = {}
ok = bad = 0
for r in sorted_by_chain_position:
    pv = str(r.get('prev_hash',''))
    if pv.upper() in ('GENESIS','') or pv == 'NONE':
        ok += 1; prev_lineage[ch] = pos
    elif pv in prev_lineage:
        ok += 1
    else:
        bad += 1
```

## Invariant-Preservation Audit (2026-08-03)

**Scar:** Federation Context Compiler claimed "2,930 bytes instead of 31,298... zero information loss." Live probe: constitutional floors table had **10 floors, not 13** — F3, F5, F12 silently dropped from the generator's hardcoded template.

**The loss lives in the template, not the algorithm.** Restoring dropped invariants costs a few hundred bytes and barely dents the ratio (2,913 → 3,142, still ~90% reduction).

**Reduction % vs hardcoded baseline = benchmark theater.** The compiler's "naive full-dump = 34,000 tokens" was a constant in source, never measured. Before citing any reduction ratio, grep source for the baseline constant. If assigned rather than computed, the ratio is unverifiable.

**Attention reduction ≠ access reduction.** Excluded tools stay CALLABLE if MCP server is still wired. "Tool not present = can't be called wrong" is only true with runtime schema gating.

## Config/Env Wiring Claim Audit (2026-08-01, Qwen Token Plan)

| Claim | Probe | Verdict |
|---|---|---|
| "config.yaml modified" | `stat -c '%y'` mtime AFTER claimed change | ✅ TRUE — via CLI, NOT refused patch tool |
| "keys wired in vault" | read vault env file | ✅ TRUE (3× REAL sk-sp-*) |
| "21 models per seat" | `GET {base}/models` per key | ✅ TRUE |
| "chat OK" (Pro seat) | `POST /chat/completions` | ✅ TRUE |
| "HERMES-SEAT-OK" (Standard) | `POST /chat/completions` same key | ❌ FALSE — 429 ×4 |
| "seats.yaml updated" | read seat-by-seat | ⚠️ PATCHED WRONG — agent patch contradicts own comment |
| "restart will pick it up" | `/proc/<pid>/environ` chain | ❌ FALSE — key absent from process env |

**401 vs 429:** 401 = wrong key; 429 = valid but throttled. dotenv files with `export KEY=value` format break naive parsers → false "vault empty" alarm.

## Autonomous Deployment Overclaims (2026-07-29)

| Claim | What to Probe | Expectation |
|-------|---------------|-------------|
| "FQ 1.50 BALANCED" | `curl :7073/health \| jq .fq` | May be stale — actual could be 9.88 OVERHEAT |
| "All gaps closed" | carry_forward + goal_registry | Usually 3-4 pending |
| "Autonomous AGI" | Check git for 888_HOLD records | Usually bounded autopilot |
| "7/7 organs" | Health probe all ports | Usually correct (thyroid-level) |

**FQ Overheat Diagnostic:** AED fires every 5 min, EXECUTE + SEAL both push execute counter. If VERIFY doesn't keep pace → FQ spikes. When AED itself is the dominant consumer, the system is heating itself.

## Code-Edit Receipt Verification (2026-08-19)

When a receipt claims "edited serve.js to use process.env.MCP_PROTOCOL_VERSION" or "patched 6 sites":
```bash
file="/root/A-FORGE/dist/src/interfaces/mcp/serve.js"
pattern='"2025-11-25"'
echo "Hardcoded sites: $(grep -c "$pattern" $file)"
# Compare against claim ("6 sites swapped")
# For env-var claims, verify BOTH sides: set in unit AND read in code
# "Wire-verified" without the wire response is narrative, not witness
```

A prior session sealed "wire-verified" on a different file version. Re-verify every time.

## Cron-Generated Telemetry: Hardcoded Theater (2026-07-31)

Audit claimed "live telemetry" with 15-min cron refresh, but sentiment data (PH 39.8%, BN 39.2%, PN 21%) never changes — hardcoded values with fresh timestamp.

**Detection:** Force cron tick manually, check source file vs webroot, compare timestamps. If sentiment percentages identical across runs → script is faking it.

## Unification Receipt Audit (2026-08-21)

**1 — Inverted canonicality:** 88 entries in /root/AAA/skills were symlinks → /root/HERMES/skills (holding 502 SKILL.md). "One source" was actually three physical stores.

**2 — Dead-lane residue:** /root/.kimi → /root/.arifos/agents/kimi still held 146 stale copies after live lane cleaned. Dormant ≠ gone.

**3 — Divergence direction:** 236 shared names → 124 diverged, 111 runtime-newer than "canonical" — the canonical side was the STALE side.

**4 — Non-reproducible counts:** "42 agents clean" matched no surface (33 active cards, 39 dirs, 19 registry entries); "9 commits" vs `git log --since=<midnight>` = 14.

## Cross-Witness Session (2026-07-28)

Single-agent internal audit is ~60% accurate on first pass. OpenCode (FI-001) produced 7-layer audit with 14 findings. Hermes independently verified: 3 of 8 core claims were false (MCP resources=0, vault silent 4 days, kernel F2 violation). Without cross-witness, those 3 false claims would have been sealed as truth.

MCP resource inflation: claimed count included every `skill://` entry (filesystem mirrors). Count `arifos://` + `tree777://` only → ~34 operational resources, not 294.

## Agent-Card Federation Alignment (OpenClaw, 2026-07-29)

12 findings across 5 categories: 3 CRITICAL (orphan skills, deprecated kernel refs, duplicate bare strings), 4 HIGH (all 5 MCP tool lists wrong, intelligence tier contradiction, missing arifFLOW organ). Each finding maps to a diff-ready edit.

## Identity Anchor Discipline (2026-07-19)

Arif typos persona ("Mr Jon") → accept correction, log briefly, continue with canonical identity. Identity claims from sovereign get one acknowledgment, not adoption. Anchor: Hermes = ASI tier on arifOS, sovereign = Arif (F13).

## Lazy Service-Disabling (2026-08-13)

When audit flags a service as "100% CPU parasite" and kills/disables it — check `journalctl -u <service>` first. High CPU is frequently a fast restart-loop from trivial permission error (`chmod 644` fix) or missing PYTHONPATH. Disabling local capability vs 1-line fix = feature loss.

## Truncated-Read False Negatives (2026-08-02)

Verifier claimed "NO entry" in 1328-line config. Block was at lines 1279-1291. Verifier read first ~80 lines. **Rule:** absence claim requires full-file evidence (`grep -n`), not partial read.

## MCP SSE Session Lifecycle

MCP over SSE requires 3-step handshake: `initialize` → capture `Mcp-Session-Id` → `notifications/initialized` (202, empty body!) → THEN `tools/list` works. One-shot curl returns 0 tools or HTTP 400.

## FastMCP Verbosity Trimming (2026-07-27)

MCP tool handler `verbosity="minimal"` strips `apex_scalars`, `session_birth`, `atlas333`, and 30+ fields. Detection: direct Python call vs MCP HTTP call produces different key sets. Fix: change default to `"standard"`.

## S24 Passive Sensor (2026-07-24)

S24 timeout on HTTP probe ≠ "Termux asleep." S24 is passive sensor in data diode architecture — collects when polled, sleeps between cycles. Check telemetry JSONL for last successful entry.

## MCP Resource/List Probing

```python
import urllib.request, json
body = json.dumps({"jsonrpc":"2.0","id":1,"method":"resources/list","params":{}}).encode()
req = urllib.request.Request("http://localhost:<port>/mcp", data=body,
    headers={"Content-Type": "application/json",
             "Accept": "application/json, text/event-stream"})
resp = urllib.request.urlopen(req, timeout=5)
```

405 = GET not POST; 406 = missing Accept header; 400/Missing session ID = organ requires MCP session auth.

## Session ID Truncation Bug (arifOS → GEOX bridge)

`arif_init` returns 22-char session_id, bridge truncates to 19 chars → GEOX rejects as `SESSION_INVALID`. Low-binding tools work; strict-binding tools fail. Workaround: call GEOX tools directly bypassing `arif_route`.

## DeepSeek BYOK Anthropic Endpoint (2026-07-19)

DeepSeek exposes Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`. Must use `provider_type=anthropic` (not `openai` — triggers HTTP 400 on reasoning_content echo). Verified 17 agents consume this pattern.

## GEOX Tool Count

Health endpoint says `public_tools=24`. Registry says 77. SACRED_SURFACE says 139. Health endpoint is ground truth. Never cite 77 or 139 as live tool count without verifying against health.
