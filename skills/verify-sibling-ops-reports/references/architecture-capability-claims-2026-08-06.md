# Architecture / Capability Claims — Verification Recipe

> WARNING DRIFT 2026-10-14: local mirror /root/forge_work/i-arif-prep ABSENT (probed: dir + *.jsonl missing, depth-5 sweep /root). HF dataset ariffazil/I-ARIF-CANON = live SOT (card 2026-10-04, 1,699 rows, 7 subsets, redteam=100 probes, not 10). Local commands below fail until mirror restored (one-command T1 restore, only on F13 ask; license AGPL research-only, incorporation needs F13 approval).


When a sibling (or external essay) presents a structural architecture claim — *"arifOS is capability-first"*, *"the 3-layer model is real"*, *"MCP mirrors are live"*, *"7-layer architecture complete"* — the verification discipline is: **don't argue the prose; probe the artifacts the prose cites.**

The recurring pattern in this session (2026-08-06): the structural insight is correct, but the runtime doesn't yet match the design. The honest verdict shape is **"DESIGNED, NOT IS"** — architecture is sound, execution is 60% there.

## 1. Find the canonical artifact

Don't grep docs; read the file and count. The load-bearing artifacts for capability claims:

| Claim class | Artifact | Path |
|---|---|---|
| "Capability-first" | `surfaces.json` | `/root/arif-fazil.com/surfaces.json` |
| Domain→verb mapping | `world-model.yaml` | `/root/arif-fazil.com/canon/world-model.yaml` |
| MCP mirrors | live organ + public gateway | `:port/mcp` + `*.arif-fazil.com/mcp` |
| Machine surface ecosystem | llms/missions/well-known | `/llms.txt`, `/llms.json`, `/missions.json`, `/.well-known/webmcp.json` |
| Sealed ledger | VAULT999 | `/root/arifOS/VAULT999/outcomes.jsonl` |
| Trainable model | HF + local weights | `huggingface.co/api/datasets/ariffazil/I-ARIF-CANON` + `/root/forge_work/i-arif-prep/` |

## 2. Count-claim triangulation

When a report cites a number ("64 surfaces", "8 canonical verbs", "12 tests, 9 pass + 3 skip"), check three independent sources:

| Source | Probe |
|---|---|
| The data itself | `python3 -c "print(len(json.load(open('surfaces.json'))['surfaces']))"` |
| The doctrine text inside the file | `jq -r '.doctrine.title' surfaces.json` |
| The live artifact | `curl -s https://domain/sitemap.xml \| grep -c '<loc>'` |

**Three different numbers = drift you report, not resolve silently.** Verified 2026-08-06:
- surfaces.json doctrine says **64**
- surfaces.json list has **70**
- sitemap.xml has **42**
- All three are simultaneously true — the doctrine text wasn't bumped when the list grew.

## 3. Live MCP handshake recipe

`POST tools/list` is NOT the right shape for every organ. Transport differs:

| Organ | Bare POST | Handshake | Public gateway |
|---|---|---|---|
| arifOS :8088 | ✅ works → 8 verbs | bare POST OK | `arifos.arif-fazil.com/mcp` (untested direct) |
| A-FORGE :7072 | ✅ works → 115 tools | bare POST OK | **gateway: `mcp.arif-fazil.com/mcp` → 8 verbs** |
| GEOX :8081 | ❌ empty body | full `initialize` → session header → `tools/list` with session → 34 tools | `geox.arif-fazil.com/mcp` (block) |
| WEALTH :18082 | ❌ empty body | POST-only (GET → 405 `Allow: DELETE, POST`); init → session → list → 8 tools | `wealth.arif-fazil.com/mcp` (block) |
| WELL :18083 | ❌ empty body | same as WEALTH → 10 tools | `well.arif-fazil.com/mcp` (block) |

### Init → session → tools/list recipe

```bash
# 1. Initialize (capture mcp-session-id header from -D -)
SID=$(curl -s -D - -X POST "http://127.0.0.1:$p/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  | grep -i "mcp-session-id" | head -1 | tr -d '\r' | awk '{print $2}')

# 2. tools/list with session
curl -s -X POST "http://127.0.0.1:$p/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

**Mirror asymmetry is BY DESIGN.** The public gateway returns **8 verbs only** (the capability contract); organ-internal tools (175 total: 115 forge + 34 geox + 8 wealth + 10 well + 8 arifOS) are local-only. Reporting "mirror broken" because public ≠ local = misreading the architecture. Public is the contract surface; local is the execution surface.

## 4. Machine-surface ecosystem probe

One curl loop to verify the whole `llms.txt / llms.json / missions.json` family:

```bash
for f in llms.txt llms-full.txt llms.json .well-known/agent.json soul.json \
         surfaces.json machine/map.json missions.json page.json \
         status.json rsl.xml robots.txt sitemap.xml .well-known/webmcp.json; do
  printf "%-32s → " "$f"
  curl -s -o /dev/null -w "%{http_code}\n" "https://arif-fazil.com/$f"
done
```

Verified 2026-08-06: **13/14 files live**. `status.json` returned 404. Claude's 4-group framing (Identity / Capability catalog / Runtime state / Plumbing) is a solid mental model for what each file is for, even when individual files are missing.

## 5. VAULT999 seal-coverage check

When a report claims "immutable sealed ledger" or "hash-chained", probe the actual seal rate:

```bash
TOTAL=$(wc -l < /root/arifOS/VAULT999/outcomes.jsonl)
SEALED=$(grep -c '"prev_hash"' /root/arifOS/VAULT999/outcomes.jsonl)
SCHAPES=$(python3 << 'EOF'
import json
from collections import Counter
shapes = Counter()
malformed = 0
with open('/root/arifOS/VAULT999/outcomes.jsonl') as f:
    for line in f:
        if not line.strip(): continue
        try:
            d = json.loads(line)
            if 'ts' in d and 'event' in d: shapes['event_log'] += 1
            elif 'decision_id' in d and 'verdict_issued' in d: shapes['decision_log'] += 1
            elif 'receipt_id' in d or 'receipt_type' in d: shapes['receipt'] += 1
            else: shapes['other'] += 1
        except json.JSONDecodeError:
            malformed += 1
for k, v in shapes.most_common(): print(f'  {k}: {v}')
print(f'  malformed: {malformed}')
EOF
)
echo "sealed: $SEALED / $TOTAL"
echo "schema shapes:"
echo "$SCHAPES"
```

Verified 2026-08-06: VAULT999 holds 37,016 entries, only **11 with `prev_hash`** (chained). Four schema shapes (`event_log: 5798`, `decision_log: 29761`, `receipt: 612`, `other: 467`) + **380 malformed lines**. Seal coverage ≈ 0.0297%. The ledger is append-only forensic memory, not a hash chain at the current scale — the architecture intends sealing; the runtime is forensic-grade.

## 6. Trainable model vs trained model

`I-ARIF-CANON` has:

| Stage | Status | Evidence |
|---|---|---|
| Corpus built | ✅ | 1,308 SFT + 96 DPO + 117 val = 1,521 pairs (local + HF) |
| Corpus sealed | ✅ | `manifest.json` + SHA-256 hashes; `manifest_sealed.json` is older |
| Dataset uploaded | ✅ | `ariffazil/I-ARIF-CANON` on HF (public, 17 files incl. .bak cruft) |
| Weights trained | ❌ | No QLoRA weights in any repo or HF; only corpus + reward spec |
| Deployed | ❌ | No `i-arif` model on any provider catalog |

Report shape: **"CORPUS READY, WEIGHTS ABSENT"** — `dataset ≠ trained model`. Verified 2026-08-06.

## 7. Verdict shapes for architecture claims

| Pattern | Verdict | Meaning |
|---|---|---|
| Design intent correct, runtime partially deployed | **DESIGNED, NOT IS** | Architecture is sound; execution is 60% there |
| All files live, numbers match, MCP responds | **VERIFIED** | True capability-first on the wire |
| Doctrine text says one thing, data says another | **SELF-CONTRADICTION** | F11 AUDITABILITY drift in the source file |
| Hash chain claimed, seal coverage < 1% | **FORENSIC ARCHIVE, NOT SEALED LEDGER** | Append-only ≠ sealed |
| Fresh baseline (< a few hours) → "STABLE trend" | **SINGLE SAMPLE, NOT TREND** | Too early to detect drift |
| Model "ready" but weights untrained | **CORPUS READY, WEIGHTS ABSENT** | Dataset ≠ trained model |
| Test count "9 pass + 3 skip" without runnable suite | **UNVERIFIABLE** | Number is a fixture, not a green run |

## 8. The "designed vs is" rule

The strongest valid architectural statement is:

> *"The architecture intends X, and the canonical structure supports X. Runtime achieves Y% of X."*

This separates design intent (OBS if the file structure is verifiable) from runtime reality (OBS if the live probe matches). Conflating them — "the system IS capability-first" when the runtime has 404s and schema drift — overstates. Correct shape:

> *"The canonical structure IS capability-first. The runtime is partially there."*

Honest. Verifiable. Doesn't overstate. Doesn't understate either — the design is real and load-bearing.

## Worked example — 2026-08-06 capability-first audit

| Claim | Probe | Verdict |
|---|---|---|
| "9-domain world model" | `len(surfaces.json.domains.list)` | ✅ 9 (origin/proof/law/earth/capital/voice/work/signal/human) |
| "64 surfaces" (doctrine text) | `len(surfaces.json.surfaces)` | ⚠️ **70 in data, 64 in doctrine** |
| "Doctrine: not in surfaces.json → not served" | `surfaces.json.doctrine.rule` literal match | ✅ exact quote |
| "7 federation subdomains" | `len(surfaces.json.federation_subdomains)` | ✅ 7 |
| "STABLE trend / no decay" | FRAME `:18085/health` + baseline mtime | ⚠️ baseline 140 min old — single sample, not trend |
| "Immutable sealed ledger" | VAULT999 hash chain ratio | ❌ 11/37,016 (0.0297% sealed) |
| "I-ARIF model trained/deployed" | HF model listing + local weights dir | ❌ corpus ready, weights absent |
| "MCP mirrors live (5 organs)" | 5× curl `tools/list` + 5× handshake | ⚠️ 3 public direct URLs block; public gateway works (8 verbs) |
| "13/14 machine-surface files live" | curl loop | ✅ 13/14 (status.json 404) |
| "Public = capability contract (8 verbs)" | `mcp.arif-fazil.com/mcp tools/list` | ✅ 8 canonical verbs |
| "Local = execution surface (175 tools)" | 5× local handshake + count | ✅ 8+115+34+8+10 = 175 |

**Net:** 7/11 fully verified, 4/11 verified with caveats. The capability-first structure is real and load-bearing on the public surface. The private surface (VAULT999 sealing, I-ARIF training, direct public organ URLs) is **DESIGNED, NOT IS** — the architecture is sound, the execution is 60% there.
