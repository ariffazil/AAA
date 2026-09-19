# 06 — RECEIPT / LEDGER / WITNESS APPARATUS

> **Audit:** acah-audit-2026-09-19 · FINDING CLASS: THEATRE + WRITE-ONLY, with one REAL gate that writes a WRITE-ONLY pile
> **Method:** strictly read-only. No ledger appended to, no receipt created, nothing modified. Measuring the write path was done by importing the gate module and calling `classify()` only — `write_receipt()` was never invoked (see §7).
> **Snapshot:** 2026-09-19 ~02:50–03:05 UTC. All ledgers are live-appending; counts drift by ~13,000 records/day (measured, §7), so every number below is a timestamped snapshot, not a constant.
> **Doctrine under test:** `/root/AAA/instructions/state-transition-discipline.md` · `/root/AAA/instructions/authority-envelope.md` · `/root/AAA/skills/seal-discipline/SKILL.md`

---

## 0. VERDICT IN ONE PARAGRAPH

The apparatus is **93.08% non-causal by its own definition**. Of 272,334 records across 24 ledgers, 253,499 carry no `trace_id` — the doctrine's own test for "an event-pile entry, not a causal-ledger entry" (`state-transition-discipline.md:49`). Where `trace_id` *is* present it is functionally dead: in the only high-coverage ledger, **92.14% of trace_ids appear exactly once**, so the "causal join key" joins nothing — it is a per-call random nonce, not a thread from a parent objective. The ledger the doctrine names as **"constitutional truth source"** (`seal-discipline/SKILL.md:199`) contains **1 record**. Meanwhile the largest receipt ledger, `apex-zen-receipts.jsonl` (30,399 records, 100% trace-null), is 93.4% metric telemetry mislabelled as receipts, and its **only** reader is a compactor that deletes it. The single genuine read-that-changes-an-outcome in the whole apparatus is `apex-zen-consequence-router.py:33-44`, which reads `apex-zen-witness.jsonl` to set a `witness_backing` label — and that label is written into a ledger nobody reads. **One control genuinely blocks** (the Hermes `pre_tool_call` gate, 1,036 block events measured). It leaves its receipts in a file no gate reads back. Its cost is a **~45 ms fail-closed subprocess spawn on every single tool call**, of which 17,195 of 18,233 receipts (94.3%) are records of an *allow* — the ledger's dominant content is the record of a non-event.

---

## 1. INVENTORY — what exists

All 9 named candidates exist. A full sweep found far more.

```
$ find /root -name '*.jsonl' 2>/dev/null | grep -iE 'receipt|vault' | wc -l
~180   (incl. .quarantine/, hermes_work/ copies, snapshots — excluded from measurement)
```

Measured set: the 24 live ledgers listed in §2. Excluded as non-live: `/root/.quarantine/**`, `/root/hermes_work/**`, `/root/.local/share/arifos/snapshots/**`.

```
$ ls -ld /root/VAULT999
lrwxrwxrwx 1 root root 21 Aug  3 14:18 /root/VAULT999 -> /root/arifOS/VAULT999
```
Note: writers reference `/root/VAULT999/...` while this report cites `/root/arifOS/VAULT999/...` — same file, via symlink. Both spellings appear in code.

**Disk cost (measured):**
```
$ du -sh /root/arifOS/VAULT999 /root/.local/share/arifos
1.2G    /root/arifOS/VAULT999
210M    /root/.local/share/arifos
$ df -h / | tail -1
/dev/sda1       387G  307G   81G  80% /
```
`df -h` output is the **host** filesystem (307 G used, 80%). VAULT999 is the largest single subtree at 1.2 GB.

---

## 2. PER-LEDGER MEASUREMENT

Measured with `/tmp/measure_ledgers.py` (parse every line, classify `trace_id`, count key-set variants) and `/tmp/totals.py` (aggregate). Method for "null": `"trace_id" not in d` **or** `d["trace_id"] is None` **or** it is a whitespace-only string.

### 2.1 Aggregate (the headline)

```
$ python3 /tmp/totals.py
LEDGER COUNT (existing files measured): 24
TOTAL RECORDS      : 272334
trace_id NULL/EMPTY: 253499  (93.08%)
trace_id PRESENT   : 18835  (6.92%)
TOTAL ON-DISK BYTES: 104618866  (99.8 MiB)
MEAN RECORD BYTES  : 384.2
```

### 2.2 The candidate ledgers, measured

| # | Ledger (under `/root/`) | Recs | `trace_id` null | Span (days) | Rate **/day** | B/rec | Class |
|---|---|---|---|---|---|---|---|
| 1 | `arifOS/VAULT999/RECEIPTS/receipts.jsonl` | 2 | **100.00%** | 3.6 | 0.6 | 3288 | WRITE-ONLY |
| 2 | `arifOS/VAULT999/RECEIPTS/session_receipts.jsonl` | 5 | **100.00%** | — | — | 727 | WRITE-ONLY |
| 3 | `arifOS/VAULT999/receipts_v2.jsonl` | 11 | **100.00%** | 6.1 | 1.8 | 1406 | WRITE-ONLY |
| 4 | `arifOS/VAULT999/apex-zen-receipts.jsonl` | **30,399** | **100.00%** | 5.66 | **5,375.0** | 329 | **THEATRE / WRITE-ONLY** |
| 5 | `arifOS/VAULT999/wealth/receipts.jsonl` | 2,868 | 93.17% | 43.81 | 65.5 | 749 | WRITE-ONLY |
| 6 | `arifOS/VAULT999/frame/receipts.jsonl` | 28 | **100.00%** | 33.5 | 0.8 | 1820 | WRITE-ONLY |
| 7 | `arifOS/VAULT999/sro_expiry_receipts.jsonl` | 11 | **100.00%** | 7.0 | 1.6 | 142 | WRITE-ONLY |
| 8 | `arifOS/arifosmcp/gateway/receipts.jsonl` | 160 | 97.50% | 3.7 | 43.2 | 484 | **STALE** (last write 2026-06-16) |
| 9 | `.hermes/gate/receipts/hermes_actions.jsonl` | 13 | **100.00%** | — | — | 389 | WRITE-ONLY |
| 10 | `.local/share/arifos/opencode_receipts.jsonl` | **118,799** | **100.00%** | 38.16 | **3,113.2** | 398 | WRITE-ONLY |
| 11 | `.local/share/arifos/opencode_nudge_receipts.jsonl` | 46,763 | **100.00%** | 36.49 | 1,281.4 | 180 | WRITE-ONLY |
| 12 | `.local/share/arifos/arifflow_receipts.jsonl` | 35,788 | **100.00%** | 52.69 | 679.2 | 307 | WRITE-ONLY |
| 13 | `.local/share/arifos/hermes_hook_receipts.jsonl` | 18,155 | **0.10%** | 42.88 | 423.4 | 275 | **BY-PRODUCT OF A REAL GATE** |
| 14 | `arifOS/VAULT999/apex-zen-witness.jsonl` | 8,184 | **100.00%** | 5.66 | 1,446.6 | 1761 | WRITE-ONLY, one dead-end read edge |
| 15 | `arifOS/VAULT999/apex-zen-telemetry.jsonl` | 4,651 | **100.00%** | 5.50 | 845.1 | 666 | WRITE-ONLY (input to #4) |
| 16 | `A-FORGE/data/gateway_receipts.jsonl` | 2,947 | **100.00%** | 94.21 | 31.3 | 292 | WRITE-ONLY |
| 17 | `.local/share/arifos/vault999/wealth/receipts.jsonl` | 2,391 | 99.83% | — | — | 604 | WRITE-ONLY |
| 18 | `.local/share/arifos/seal_receipts.jsonl` | 114 | **100.00%** | 0.07 | 1628.6 | 152 | WRITE-ONLY |
| 19 | `.local/share/arifos/geox_receipt_ledger.jsonl` | 220 | **100.00%** | — | — | 329 | WRITE-ONLY |
| 20 | `.local/share/arifos/world-model/promotion_receipts.jsonl` | 463 | **0.00%** | — | — | 446 | **UNPROVEN** — 100% singleton traces (§3) |
| 21 | `arifOS/VAULT999/reality_ledger/entries.jsonl` | 13 | **100.00%** | 1.9 | 6.8 | 1776 | WRITE-ONLY |
| 22 | `A-FORGE/data/vault999_chain.jsonl` | 73 | **100.00%** | 78.1 | 0.9 | 1038 | WRITE-ONLY |
| 23 | **`arifOS/VAULT999/seal_chain.jsonl`** | **1** | 100.00% | — | — | 1283 | **BROKEN-BY-POINTER** (§4) |
| 24 | `.local/share/arifos/vault999/seal_chain.jsonl` | 267 | — | — | — | 1676 | live chain (read by gates) |

**Rate method** (`/tmp/rates.csv` driver): first/last ISO-8601 timestamp per file, parsed, span in days, `records / days`. Example command output:
```
VAULT999/apex-zen-receipts.jsonl    rec= 30399 span= 5.66d rate=  5375.0/day avg=  329 B/rec  2026-09-13T11:05:54 .. 2026-09-19T02:50:03
.local/opencode_receipts.jsonl      rec=118799 span=38.16d rate=  3113.2/day avg=  398 B/rec  2026-08-11T23:03:36 .. 2026-09-19T02:53:48
.local/hermes_hook_receipts.jsonl   rec= 18155 span=42.88d rate=   423.4/day avg=  275 B/rec  2026-08-07T05:54:03 .. 2026-09-19T02:59:06
```

**Note on `apex-zen-receipts` growing mid-audit:** it read 30,398 in my first pass and 30,399 in the second; `hermes_hook_receipts` read 17,623 → 18,144 → 18,155. The apparatus appends while being audited. (This is also why the doctrine's own figure is stale — see §5.)

---

## 3. THE `trace_id` JOIN TEST — the decisive measurement

A `trace_id` that appears once joins nothing. This is the measurement the doctrine never performs on itself.

```
$ python3 /tmp/trace_multiplicity.py
--- hermes_hook_receipts (the only high-trace ledger)
    records=18144  with_trace=18126  distinct_trace=16751
    multiplicity histogram: {1: 15434, 2: 1316, 60: 1}
    traces appearing exactly ONCE: 15434 (92.14% of traces)
    mean records per trace_id: 1.082
    top 5 busiest trace_ids: [('trc-selftest', 60), ('trc-adbe7757edfd', 2), ...]
--- world-model/promotion_receipts
    records=463  with_trace=463  distinct_trace=463
    traces appearing exactly ONCE: 463 (100.00% of traces)
    mean records per trace_id: 1.000
--- VAULT999/wealth/receipts
    records=2868  with_trace=196  distinct_trace=23
    mean records per trace_id: 8.522
--- arifosmcp/gateway/receipts
    records=160  with_trace=4  distinct_trace=4
    traces appearing exactly ONCE: 4 (100.00%)
```

**Reading:**

- `hermes_hook_receipts` — the only ledger with near-full `trace_id` coverage — has **mean 1.082 records per trace**. Strip the single `trc-selftest` trace (60 records, a self-test) and the join ratio is effectively **1.0**. A trace that spans one record is a distinct nonce, not a causal thread.
- The cause is in the writer itself, `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py:547`:
  ```python
  # F3: causal join key — ARIFOS_TRACE_ID env if the parent objective set one,
  # else mint a session-scoped trace so every receipt is joinable.
  trace_id = os.environ.get("ARIFOS_TRACE_ID") or f"trc-{uuid.uuid4().hex[:12]}"
  ```
  When `ARIFOS_TRACE_ID` is unset the hook **mints a fresh random 12-hex nonce**. The comment claims this makes "every receipt joinable"; measured, it makes every receipt *individually identifiable* and *mutually unjoinable*. The field is satisfied; the function is not. This is precisely the distinction `state-transition-discipline.md:49` draws — and the code passes the field test while failing the doctrine it was written to serve.
- `.local/share/arifos/world-model/promotion_receipts.jsonl` is 100.00% singletons despite 0% null. Presence of `trace_id` is therefore **not** evidence of causal joinability anywhere in the federation.
- `VAULT999/wealth/receipts.jsonl` is the **only** ledger where `trace_id` actually joins in the doctrine's sense (mean 8.5 records/trace, e.g. `FI003-WEALTH-TEST-20260916` spans 35 records). But only 196 of 2,868 records (6.8%) carry one. So the capability exists and is used in exactly one organ, on 6.8% of its records.

---

## 4. WHO WRITES / WHO READS — per ledger, with the decision it changes

### 4.1 WHO WRITES (code that appends, cited)

| Ledger | Writer | Cite |
|---|---|---|
| `arifOS/VAULT999/apex-zen-receipts.jsonl` | `apex-zen-consequence-router.py` | path `:17` `RECEIPTS_OUTPUT = Path('/root/VAULT999/apex-zen-receipts.jsonl')`; append `:274-276` `with output_path.open('a') as f: … f.write(json.dumps(r) + '\n')` |
| `arifOS/VAULT999/apex-zen-witness.jsonl` | `apex-zen-reality-binder.py` | path `:26` `OUT = Path("/root/VAULT999/apex-zen-witness.jsonl")`; append `:156` `with OUT.open("a") as f:` → `:161` `f.write(json.dumps(wo) + "\n")` |
| `.local/share/arifos/hermes_hook_receipts.jsonl` | `arifos-hermes-gate-hook.py` | path `:36` `RECEIPT_PATH = "…/hermes_hook_receipts.jsonl"`; append `:443-446` `os.makedirs(…)` / `with open(RECEIPT_PATH, "a") as f:` / `f.write(json.dumps({…}) + "\n")` |
| `.local/share/arifos/opencode_receipts.jsonl` | `arifos-judge-gate.ts` (OpenCode plugin) | `:123` `const RECEIPT_PATH = "…/opencode_receipts.jsonl"`; append `:139` `appendFileSync(RECEIPT_PATH, JSON.stringify(payload) + "\n", "utf8")` |
| `arifOS/VAULT999/wealth/receipts.jsonl` | WEALTH MCP organ | not traced to a line in this session — **UNDETERMINED** |
| `arifOS/arifosmcp/gateway/receipts.jsonl` | unknown, **stale** | last record `2026-06-16T13:05:55Z`; no live writer found — **UNDETERMINED** |
| `opencode_nudge_receipts`, `arifflow_receipts`, `A-FORGE/data/gateway_receipts` | schemas indicate TS/Python producers (`hermes-nudge-injector.ts`, arifFlow service) | **UNDETERMINED** — not confirmed to a line |

### 4.2 WHO READS, and what decision changes

This is the definitional test. Listed strictly: **a ledger nobody reads cannot govern anything.**

**`apex-zen-receipts.jsonl` — 30,399 records, THEATRE + WRITE-ONLY.**
Full reader set (searched `/root` for `apex-zen-receipts.jsonl` across `*.py|*.sh|*.js|*.ts`):
```
/root/AAA/scripts/apex-zen-consequence-router.py:17,30   ← the WRITER
/root/AAA/scripts/apex-zen-compact.py:19,20,119-165      ← the only READER
/root/AAA/scripts/reality_substrate_classify.py:72       ← static path→domain table, not a read
/root/AAA/scripts/apex-zen-announce-consumer.py:7        ← comment referencing the .state.json watermark
```
The one real reader, `apex-zen-compact.py:122` `lines = RECEIPTS.read_text().strip().split('\n')`, then `:150-159` gzip-archives and `os.replace` — **it compacts and deletes the ledger.** No code path anywhere branches on a receipt's content to ALLOW, HOLD, downgrade, or restrict anything. The file `APEX-ZEN-CONSEQUENCE-LADDER.md:88` prescribes "apply runtime restrictions" on WARNING+ — I found no reader implementing that restriction. **Verdict: the control cannot influence any decision; it only accumulates.** THEATRE.

**Schema reality of `apex-zen-receipts.jsonl` — mislabelled.** Key-set histogram:
```
keys x28389: ['action_withheld','consequence','doctrine_status','metric','severity','source','threshold','timestamp','value','witness_backing']
keys x1802 : [...same... , 'receipt_id']
keys x207  : (third variant)
```
**28,389 of 30,398 records (93.4%) carry no `receipt_id` at all** — they are metric/threshold samples. A file named `receipts` is 93% telemetry. Nothing distinguishes them: no `type` field, no discriminator. An auditor or a downstream gate cannot separate a receipt from a sample without heuristic reasoning about which keys are present.

Its own writer documents that this was worse and was only *partially* fixed — `apex-zen-consequence-router.py:19-29`:
> "Without it the router re-dumps the entire backlog every cycle … `timestamp` is stamped with now(), so each re-emission LOOKS unique while being content-identical — there is no dedup key to detect it. Measured 2026-09-13T14:00Z: 27,280 rows carrying only 116 distinct signals (sev,metric,source,value) = **99.6% redundant, ~74 MB/day** appended to a disk at 79%. Fix: emit a signal once on appearance…"

So the file's own history is: 99.6% redundant, ~74 MB/day, self-diagnosed. The watermark fix landed; the **absence of a dedup/join key was not fixed**, which is why `trace_id` is 100% null and `receipt_id` absent in 93% of rows.

**`hermes_hook_receipts.jsonl` — the ONE ledger fed by a REAL gate.**
Event mix, measured:
```
event                         count
  hermes-gate.witnessed       17195
  hermes-gate.blocked          1036
  hermes-gate.jitu_tripped        2
classification                count
  T2                          15818
  W_SCAR                       2181
  T3                            203
  TRANSPORT_LOCK                 31
top tools: terminal 10232 · skill_manage 1986 · execute_code 1907 · write_file 1491 · patch 1251
```
1,036 block events is real enforcement — this gate *does* change outcomes (`sys.exit(2)` T3 / `sys.exit(3)` JITU, e.g. `arifos-hermes-gate-hook.py:600,615`). But note the shape: **94.3% of all receipts record an ALLOW.** The ledger's dominant content is the record of a non-event. The gate is REAL; the ledger it writes is a by-product, and readers of it are reporting-only:
```
/root/AAA/federation/probes/compute_regret_signal.py:27,58,86   ← samples first 1000, emits a "signal"
/root/A-FORGE/scripts/recovery/forge_closure_slo.sh:31          ← reads unsealed>24h, reports
/root/AAA/scripts/cockpit_probe.py:33                           ← reports a count
/root/AAA/skills/hermes-ops/hermes-runtime-audit/SKILL.md:291   ← `wc -l … # is the gate deciding at all?`
```
No gate reads a receipt to decide. `hermes-runtime-audit/SKILL.md:291` is telling: the receipt file's documented use is *counting lines to ask whether the gate is alive* — i.e. even its own operator manual treats it as a liveness counter, not a decision input.

**`arifOS/VAULT999/seal_chain.jsonl` — declared "constitutional truth source", contains 1 record.** See §5.

**`apex-zen-witness.jsonl` — the only read that changes an output.**
`apex-zen-consequence-router.py:33-44`:
```python
WITNESS_INPUT = Path('/root/VAULT999/apex-zen-witness.jsonl')
def load_witness_sources() -> set:
    ...
        srcs.add(str(json.loads(line).get('session_source', '')))
...
def witness_backing(source: str, witness_sources: set) -> str:
    if not source or source == 'unknown': return 'MISSING'
    ...
    for ws in witness_sources:
        if ws.endswith(source) or source.endswith(ws): return 'BOUND (session witness)'
    return 'MISSING'
```
This is a genuine read→branch→changed-output edge: witness presence alters a field in every emitted receipt. It is the strongest causal edge in the apparatus. But the field it changes (`witness_backing`, present in all 30,399 rows) is consumed by **nobody** — it lands in the ledger whose only reader deletes it. **REAL EDGE, DEAD END.**

Also note the binding test is `ws.endswith(source) or source.endswith(ws)` — a substring match, not an identity match. A `session_source` of `"a"` would bind to any witness path ending in `a`. That is a false-positive surface in the one place the apparatus claims "no metric may be promoted without a witness object" (`router:32`).

### 4.3 Classification summary

| Class | Ledgers | Basis |
|---|---|---|
| **REAL** (read, changes outcome) | `seal_chain.jsonl` (via `vault_verify.py`), the `pre_tool_call` gate itself | `vault_verify.py:105-118` branches on staleness >168h; gate exits 2/3 |
| **THEATRE** | `apex-zen-receipts.jsonl` | control cannot influence any decision; only accumulates (§4.2) |
| **WRITE-ONLY** | 1,2,3,5,6,7,9,10,11,12,14,15,16,17,18,19,21,22 (18 ledgers) | data written; no code path branches on it |
| **BROKEN-BY-POINTER** | `arifOS/VAULT999/seal_chain.jsonl` | declared truth source holds 1 record (§5) |
| **STALE** | `arifosmcp/gateway/receipts.jsonl` | last write 2026-06-16; dead 95 days |
| **UNPROVEN** | `world-model/promotion_receipts.jsonl` | 100% singleton traces — no evidence of joinability |

---

## 5. THE DOCTRINE'S OWN NUMBERS, TESTED

### 5.1 "52,043 receipts with trace_id=NULL"

Cited at `/root/AAA/instructions/state-transition-discipline.md:3`:
> "Codified from the two-KVM coherence experiment (R3 delivery deadlock; **52,043 receipts with trace_id=NULL**; 17k→12.4k claim retraction)."

Where does that number live?
```
$ grep -rn "52,043" /root/arifOS          → (no output — zero hits)
$ grep -rn "52,043" /root/AAA             → exactly 1 hit:
  /root/AAA/instructions/state-transition-discipline.md:3
```
(All other `52043` matches on disk were coincidental digit-runs inside hashes and float arrays — not the claim.)

**Verdict: UNREPRODUCIBLE TODAY.** It appears **once**, as prose, in the document that asserts it. There is no receipt, no measurement script, no dated probe attached. It matches no ledger I measured: the nearest candidates are `apex-zen-receipts` (30,399) and `arifflow_receipts` (35,788); no combination of the nine named candidates equals it. I cannot confirm it was ever true, and I will not repeat it as a current fact.

**What is true today, measured:** **253,499 of 272,334 records (93.08%)** have no `trace_id`. The defect the doctrine named is real and **has grown ~4.9×** past the figure used to describe it. The doctrine diagnosed correctly and then did not fix, or did not re-measure. A governance document carrying a stale count for its own central defect is exactly the class of artifact the principal asked about.

### 5.2 "constitutional truth source" = 1 record

`/root/AAA/skills/seal-discipline/SKILL.md:199`:
> `- `/root/arifOS/VAULT999/seal_chain.jsonl` — constitutional truth source`

Measured:
```
$ ls -l /root/arifOS/VAULT999/seal_chain.jsonl
-rw-r--r-- 1 root root 1283 Sep 18 01:14 /root/arifOS/VAULT999/seal_chain.jsonl
$ wc -l < /root/arifOS/VAULT999/seal_chain.jsonl
1
```
**One record**, dated `2026-09-17T17:14:30Z`, of `"type":"session_receipt"` — i.e. by the skill's own taxonomy (Class 2: RECEIPT, Lane B) **not a SEAL**.

The live 267-record chain is at a *different path*: `/root/.local/share/arifos/vault999/seal_chain.jsonl` (447,447 bytes, mtime Sep 17 02:41). `causal_spine.py:34` reads the `.local` path; `vault_verify.py:175` falls back to `VAULT_DIR / "seal_chain.jsonl"`.

So the skill that governs seal vocabulary points the reader at a **1-record stub** while the actual chain lives elsewhere. Any agent following `seal-discipline/SKILL.md:199` to verify a SEAL — the exact anti-pattern the skill forbids at line 193, "Trusting carry_forward `verdict=SEAL` without checking `seal_chain.jsonl`" — reads an almost-empty file and would conclude the federation has sealed essentially nothing. This is a **cross-surface conformance failure inside the governance layer itself**, and it is load-bearing: the skill's whole purpose is to make agents check that file.

---

## 6. THE LOAD-BEARING EXAMPLE — VERIFIED, AND IT CONTRADICTS ITS OWN DOCUMENT

`authority-envelope.md` rests its authority on a single incident:
- `:3` — "ground truth = Grok unauthorized-commit incident (**commit 7b4a228ce**, 2026-09-16) + code audit TR-MUTATION-GATE-20260916"
- `:82` — "**Regression fixture — Grok incident (commit 7b4a228ce):** … Expected: `RESOLVED=TRUE, PATCH_READY=TRUE, AUTHORIZED=FALSE, MUTATION=BLOCKED, WITNESS=N/A, STATE=MUTATION_HELD`"

I tried to verify it, expecting failure. **It verified.**

```
$ git -C /root/AAA cat-file -t 7b4a228ce
commit
$ git -C /root/AAA rev-parse 7b4a228ce
7b4a228ce2b91140976a1ef5ba5c69c3d1a5ef11
$ git -C /root/AAA show -s --format='%H%n%ci%n%an%n%s' 7b4a228ce
7b4a228ce2b91140976a1ef5ba5c69c3d1a5ef11
2026-09-16 11:28:14 +0800
333-AGI
fix(identity): conform FI roster to registry SOT — Grok FI-007 (not FI-010), FI-011=Continue CLI (not Kimi),
FI-010 Gemini CLI deceased; resolve without sovereign round-trip
$ git -C /root/AAA merge-base --is-ancestor 7b4a228ce HEAD && echo "YES ancestor of HEAD"
YES ancestor of HEAD
$ git -C /root/AAA branch -r --contains 7b4a228ce
  origin/HEAD -> origin/main
  origin/main
$ git -C /root/AAA cat-file -p 7b4a228ce | head -12
tree 7835ddfb…
parent 2665d282…
author 333-AGI <333-AGI@arifos.local> 1789529294 +0800
committer 333-AGI <333-AGI@arifos.local> 1789529294 +0800
gpgsig -----BEGIN SSH SIGNATURE-----
 U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAg3if17nc8dwrx7b1BA0nsZPWeEV
…
 -----END SSH SIGNATURE-----
```
(`git cat-file -t 7b4a228ce` → `fatal: Not a valid object name` in `/root/arifOS`, `/root/A-FORGE`, `/root/GEOX`, `/root/WEALTH`, `/root/WELL`, `/root/.hermes`, `/root/scripts`. It resolves only in the governance repo `/root/AAA`. It is tagged `v2026.09.18-skills-audit`.)

**What this means, stated carefully:**

1. The hash is **not** fabricated — it is a real, SSH-signed commit.
2. The commit **landed**. It is an ancestor of `HEAD`, present on `origin/main`, and pushed to the remote.
3. Its own subject line reads **"resolve without sovereign round-trip"** — the author explicitly recorded that this was done without F13. The incident is real.
4. The document's `MUTATION=BLOCKED` is presented under **"Expected:"** — i.e. it is the *desired* fixture outcome, not a claimed observation. Read strictly, the doctrine does **not** lie about the block.

**But:** the doctrine calls this its "ground truth" and builds its entire enforcement-coverage claim (`EnforcementCoverage → 1.0`) on it — and nowhere in 272,334 records across 24 ledgers is there a receipt recording that the monitor returned `AUTHORIZED=FALSE` / `MUTATION=BLOCKED` for it. Searched every ledger by hash:
```
$ for f in hermes_hook_receipts.jsonl hermes_actions.jsonl apex-zen-receipts.jsonl \
         opencode_receipts.jsonl receipts_v2.jsonl hermes_falsification_metrics.jsonl; do
    printf "%-40s hits=%s\n" "$f" "$(grep -c '7b4a228' "$f")"; done
hermes_hook_receipts.jsonl               hits=0
hermes_actions.jsonl                     hits=0
apex-zen-receipts.jsonl                  hits=0
opencode_receipts.jsonl                  hits=3
receipts_v2.jsonl                        hits=0
hermes_falsification_metrics.jsonl       hits=0
```
All 3 hits in `opencode_receipts.jsonl` are **the authoring session's own `tool.mutate` records** — the bash invocations that *wrote the doctrine* and rendered `AGENTS.md` (lines 98531, 98609, 98625; `sessionID: ses_f57d4d1eeffeEPxHcAfQpg5hAp`, 2026-09-16T03:31–03:41Z). Not one is a block event.

**The finding:** the apparatus cannot witness its own founding counter-example. The doctrine's load-bearing incident has a verified landing commit and **zero** enforcement receipts. The observed outcome for that objective was `MUTATION=LANDED`, signed and on the remote. `PreventedUnauthorizedRate` for the one case the document itself selected as its proof is **0**.

---

## 7. COST — measured, not assumed

### 7.1 The forcing apparatus

`/root/.hermes/config.yaml:187-190`:
```yaml
hooks:
  pre_tool_call:
    - command: python3 /root/AAA/federation/protocols/arifos-hermes-gate-hook.py
      fail_closed: true
      timeout: 10
```
This is the hook that forces receipt-writing on the Hermes lane. **Quoted line, verbatim:** `- command: python3 /root/AAA/federation/protocols/arifos-hermes-gate-hook.py`, with `fail_closed: true` and `timeout: 10`.

It runs on **every tool call**. `write_receipt` (`arifos-hermes-gate-hook.py:433-460`) appends one JSON line per invocation, with the comment `"""Append to gate receipt trail. Never block on failure (E-11)."""` and `except Exception: pass  # Never block`. So the write itself never blocks — but the **hook is `fail_closed: true`**, meaning a 10-second-timeout failure of this writer is a *blocking* condition on the agent's tool call.

Parallel forced writer on the OpenCode lane: `/root/.config/opencode/plugins/arifos-judge-gate.ts:139` `appendFileSync(RECEIPT_PATH, JSON.stringify(payload) + "\n", "utf8")` inside a `try { } catch (_) { /* never block */ }`, invoked from `"tool.execute.before"` (`:483`).

Cron-side: `/etc/cron.daily/opencode-receipt-rotate:2-3` — `# Auto-rotate opencode receipt trails to prevent disk bloat.` / `# Keeps last 14 days of receipts, gzip-compressed.` Rotation exists *because* the write rate was a disk problem.

### 7.2 The per-tool-call tax — measured without triggering a write

Method: `python3 -c "pass"` for the interpreter floor; `importlib` load of the gate module (safe: `main()` is `__main__`-guarded at `:743-744`) plus `classify()` micro-benchmarks. **`write_receipt()` was never called.**

```
$ python3 /tmp/hookcost.py
interpreter floor (python3 -c pass): median 40.6 ms  (n=7)
module import+exec: 4.3 ms  (one-off per process)
classify(terminal  ) median     6.3 us
classify(terminal  ) median     9.4 us
classify(read_file ) median     0.1 us
classify(write_file) median    10.6 us
NOTE: write_receipt() NOT called — this measurement appends nothing.
```

**~45 ms of pure process overhead per tool call** (40.6 ms interpreter spawn + 4.3 ms module import), blocking and fail-closed. The governance logic itself costs **0.1–10.6 microseconds** — six orders of magnitude less.

That is the shape of the tax: **the apparatus pays its price almost entirely in process spawn, not in reasoning.** A 200-tool-call session burns ~9 seconds of wall clock on interpreter startup for a check whose own logic is 10 µs. This cost is unavoidable for every agent that touches the lane, and it is not reducible by making the doctrine better — only by not spawning a process.

**Honest gap:** total added *latency* per call could not be measured end-to-end. Measuring it requires invoking the hook, which appends a receipt, which my read-only mandate forbids. **The apparatus cannot be benchmarked read-only, because the act of measurement writes to the thing measured.** That is itself an auditability finding: a control whose cost cannot be measured without producing side effects is a control whose cost will never be measured.

### 7.3 Disk and volume

```
TOTAL ON-DISK BYTES: 104,618,866  (99.8 MiB)   over the 24 measured ledgers
MEAN RECORD BYTES  : 384.2
du -sh: VAULT999 1.2 G · .local/share/arifos 210 M
df -h /: 307G used of 387G (80%)
```
**Write rate, summed from §2.2 measured rates:** 5,375.0 + 1,446.6 + 845.1 + 3,113.2 + 1,281.4 + 679.2 + 423.4 + 65.5 + 31.3 ≈ **13,260 records/day** (~5.1 MB/day at 384 B/record).

Disk is therefore **not** the acute cost at current rates — `apex-zen-receipts` runs ~1.8 MB/day (9,993,632 B / 5.66 d), a ~40× reduction from the self-documented 74 MB/day pre-watermark. The cost is **time per agent per tool call** (§7.2) and **the unusability of the corpus**: 100 MiB and 272,334 records that cannot be joined to an objective, an owner, or a decision.

---

## 8. WHAT THE APPARATUS IS SUPPOSED TO DO — and where measured reality differs

### 8.1 The stated design

**`state-transition-discipline.md:47-49`** — the receipt contract:
> ## Receipts: trace_id Required
> A receipt without `trace_id` is an event-pile entry, not a causal-ledger entry. On every consequential mutation: mint/accept a trace_id from the parent objective, stamp every receipt, reference it in the closing claim. Logging ≠ memory. Memory ≠ causal memory.

**`authority-envelope.md`** — the causal fabric and closure:
> ## Four Planes + Causal Fabric
> 1. COGNITION … 2. AUTHORITY … 3. EXECUTION … 4. REALITY
> ↓ all four threaded by the causal fabric: `ObjectiveID + TraceID + StateTransition + ActorIdentity`
> ↓ **CAUSAL CLOSURE (VAULT999)** — binds cycle only when reality matches projection
> "Without the fabric you cannot answer: which action is this authority for? Which objective did this mutation come from? What is this witness attesting? Which loop does this closure close? That is the 52k-receipts-with-null-trace_id defect: not missing logs — missing **causal joinability**."

And the three coverage targets that would make it a boundary rather than a suggestion:
```
EnforcementCoverage        → 1.0   (no mutation path bypasses the check)
PreventedUnauthorizedRate  → 1.0   (all out-of-envelope attempts are blocked)
UnauthorizedEscapeRate     → 0.0   (zero unauthorized mutations reach reality)
```
Plus, from the witnesses section: "**CLOSE occurs only when `ObservedState ⊨ ExpectedPostcondition`** — not when the executor says 'done.'" And `seal-discipline/SKILL.md:37-46`: a SEAL requires `judge_state_hash`, `lane == "A"`, sovereign witness > 0.5, **and** `seal_chain.jsonl` gains a new entry.

The intent is coherent and unusually well-specified. It is a **causal ledger**: the join is supposed to let you answer "which objective did this mutation come from."

### 8.2 Where measured reality differs

| Doctrine says | Measured | Gap |
|---|---|---|
| "receipt without trace_id = event-pile entry, not causal-ledger" (`STD:49`) | **253,499 / 272,334 = 93.08%** have no trace_id | The federation's own disqualifying test fails on 93% of its records. Not a defect at the margin — the *dominant* state. |
| "52,043 receipts with trace_id=NULL" (`STD:3`) | Count appears **once on disk, as prose**; equals no ledger; today's measured null-trace total is **253,499** | Stale by ~4.9×. Cannot be reproduced. Carries no measurement receipt. |
| "threaded by the causal fabric: ObjectiveID + TraceID + …" (`AE`) | TraceIDs present in `hermes_hook_receipts` are **92.14% singletons**, mean 1.082 rec/trace | The join key exists as a field and joins nothing. Writer at `hook:547` mints a random nonce when `ARIFOS_TRACE_ID` is unset, under a comment claiming this makes "every receipt joinable." |
| "CAUSAL CLOSURE (VAULT999) — binds cycle only when reality matches projection" (`AE`) | `arifOS/VAULT999/seal_chain.jsonl` = **1 record**; the live 267-record chain is at a different path | The declared closure surface is a stub. `seal-discipline/SKILL.md:199` sends agents to the wrong file. |
| "EnforcementCoverage → 1.0 … UnauthorizedEscapeRate → 0.0" (`AE`) | Founding incident commit `7b4a228ce` **landed, is SSH-signed, and is on `origin/main`**; **0 receipts** of a block in any of 24 ledgers | `PreventedUnauthorizedRate` for the document's own chosen proof case = 0. |
| "every ALLOW/HOLD decision is receipted and auditable" (`AE`, complete mediation §3) | 1,036 block receipts **do** exist, in `hermes_hook_receipts.jsonl` | Verifiability holds *here* — the one genuinely real control. But no gate reads these back (§4.2). |
| Witness: "no metric may be promoted without a witness object" (`router:32`) | `witness_backing` IS computed from `apex-zen-witness.jsonl` (`router:33-44`) | Genuine read→branch edge, but it tests membership by `endswith()` substring (false-positive surface), and its output is consumed by nobody. |
| `SEAL` requires `seal_chain.jsonl` gains a new entry (`seal-discipline:46`) | That file has 1 record, of `type: session_receipt` — a Lane B RECEIPT, not a SEAL | Following the skill's own verification lattice (`:121-139`) against the file it points to yields near-zero SEALs. The skill's "26-Day Silence Problem" (`:141-149`) may be partly an artifact of this pointer. |
| `APEX-ZEN-CONSEQUENCE-LADDER.md:88`: "apply runtime restrictions" on WARNING+ | No reader implements a restriction | The consequence ladder's output is a receipt nobody acts on. |

### 8.3 The one-line answer to the principal's question

The apparatus is not a causal ledger and not (mostly) a fraud. It is **an event pile wearing a causal ledger's vocabulary**, plus **one real brake**:

- **Real:** the `pre_tool_call` gate blocks — 1,036 events measured, `fail_closed: true`, exits 2/3. Enforcement is genuine on that lane.
- **Theatre:** the 30,399-record `apex-zen-receipts` ledger, whose own writer documented it as 99.6% redundant, and whose only reader deletes it. It governs nothing.
- **Write-only:** 18 further ledgers, 220k+ records, read by post-hoc reporters only.
- **The cost to every agent:** ~45 ms of blocking subprocess spawn per tool call to record — 94.3% of the time — that nothing was blocked.

The cheapest high-value fixes, in order: (1) put `ARIFOS_TRACE_ID` into every agent's environment so `hook:547` stops minting nonces; (2) collapse the 24 ledgers into one schema with a required `trace_id` and a `type` discriminator, so a receipt is distinguishable from a sample; (3) make the gate write receipts only on **decision** events (block / hold), not on allow; (4) fix `seal-discipline/SKILL.md:199` to point at the live chain; (5) attach a measurement command to every number in `state-transition-discipline.md:3`.

---

## 9. METHOD / EVIDENCE LEDGER

Read-only throughout. Scripts written this session (all in `/tmp`, none inside the audited tree): `/tmp/measure_ledgers.py`, `/tmp/trace_multiplicity.py`, `/tmp/totals.py`, `/tmp/hookcost.py`, `/tmp/rates.csv`.

| § | Command | Result |
|---|---|---|
| 1 | `find /root -name '*.jsonl' \| grep -iE 'receipt\|vault'` | ~180 paths; 24 live measured |
| 2.1 | `python3 /tmp/totals.py` | 272,334 rec · 253,499 null (93.08%) · 99.8 MiB · 384.2 B/rec |
| 2.2 | `python3 /tmp/measure_ledgers.py` | per-ledger table §2.2 |
| 2.2 | rate driver (§7.3) | `apex-zen-receipts` 5,375.0/day over 5.66 d, etc. |
| 3 | `python3 /tmp/trace_multiplicity.py` | 92.14% singleton traces; mean 1.082 |
| 4.1 | `grep -rn "open(\|append" <writers>` | cite table §4.1 |
| 4.2 | `search_files "apex-zen-receipts\.jsonl" /root/AAA` | 10 files; 1 true reader (`apex-zen-compact.py`) |
| 4.2 | event histogram `python3 -` over `hermes_hook_receipts` | witnessed 17,195 · blocked 1,036 · jitu 2 |
| 5.1 | `grep -rn "52,043" /root/AAA` / `/root/arifOS` | 1 hit (`STD:3`) / 0 hits |
| 5.2 | `wc -l /root/arifOS/VAULT999/seal_chain.jsonl` | `1` |
| 6 | `git -C /root/AAA cat-file -t 7b4a228ce` + `-p`, `merge-base --is-ancestor`, `branch -r --contains` | `commit`; ancestor of HEAD; on `origin/main`; SSH-signed |
| 6 | `grep -c '7b4a228' <6 ledgers>` | 0 / 0 / 0 / 3 (authoring session) / 0 / 0 |
| 7.1 | `sed -n '187,190p' /root/.hermes/config.yaml` | `fail_closed: true`, `timeout: 10` |
| 7.2 | `python3 /tmp/hookcost.py` | 40.6 ms floor + 4.3 ms import; classify 0.1–10.6 µs |
| 7.3 | `du -sh`, `df -h /` | 1.2 G · 210 M · 80% (307 G/387 G) |

### UNDETERMINED
- Line-level writer for `VAULT999/wealth/receipts.jsonl`, `opencode_nudge_receipts.jsonl`, `arifflow_receipts.jsonl`, `A-FORGE/data/gateway_receipts.jsonl` — schemas imply producers; not traced to source this session.
- Whether `arifosmcp/gateway/receipts.jsonl` (last write 2026-06-16) still has a live writer. No writer found; not proven dead.
- End-to-end per-call latency added by the hook — unmeasurable read-only (§7.2).
- Whether 52,043 was ever an accurate count. Cannot reconstruct; no historical probe attached.

### NOT DONE (read-only mandate)
No ledger appended to. No receipt created. `/root/AAA/reports/acah-audit-2026-09-19/06-receipts-ledger.md` is the only file written.

---

*DITEMPA BUKAN DIBERI — but a receipt that joins nothing is not forged, it is filed.*
