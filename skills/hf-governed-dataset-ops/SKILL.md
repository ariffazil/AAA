---
name: hf-governed-dataset-ops
description: "Publish and update HuggingFace datasets under arifOS governance — additive README/card updates, versioned F11-audit commits, live verification, immutable data files."
version: 1.0.0
author: aaa-hermes
license: MIT
tags: [huggingface, datasets, arifos, governance, mlops, publishing, f11]
platforms: [linux]
---

# HF Governed Dataset Ops

Publishing and updating HuggingFace datasets for the ariffazil namespace. Every write is a
constitutional act: data files are immutable evidence, README/card metadata is the auditable
documentation layer (F1 reversible, F11 audit trail).

## When to use
- "Update my HF dataset(s)" / "Update all my datasets" (ariffazil namespace: AAA–FFF, I-ARIF-CANON)
- Adding or refreshing dataset cards / README metadata
- Any HF Hub write that must stay governed and verifiable
- **READ-side: probing external claims** — "Berapa download?", "Betul ka 1000?", "Compare dengan dataset biasa", or any pasted audit/report making claims about Arif's HF datasets that need independent live verification against the HF API

## 1. Authenticate
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
hf auth whoami   # expect: user=ariffazil orgs=arifOS999
```
HF_TOKEN lives only in kunci-mas.env (mode 600). Never paste it in chat or commits.

## 2. Inventory
```bash
hf datasets list --author ariffazil --limit 50
```
Flag is `--author` — NOT `--owner` (errors: "No such option '--owner'").
For per-dataset file listing + tags: `python3 -c` with `HfApi().dataset_info(repo_id)`.

## 3. Fetch current README (reliable path)
```bash
curl -sL "https://huggingface.co/datasets/ariffazil/<DS>/raw/main/README.md" -o /tmp/hf_edit/<DS>_README.md
```
- Use `raw/main` — `resolve/main` without `-L` returns a "Temporary Redirect" stub, and `hf download ... README.md` can fail with a bare "Set HF_DEBUG=1" hint. curl `-sL raw/main` is the dependable read path.
- Keep working copies in `/tmp/hf_edit/`.

## 4. Edit additively (governed pattern)
- **NEVER modify `data/*` files.** Datasets are immutable evidence; README-only updates keep `manifest.json` sha256 hashes valid and preserve provenance.
- Append a dated section (e.g. `## Federated Integration — Updated YYYY-MM-DD`) before the citation/footer block. Original content stays byte-for-byte; additive, not rewrite.
- Commit-message convention: `vX.Y | F11 audit | <what changed>`.
- For composite training corpora, document readiness gaps explicitly (scale floor, domain contamination, missing trajectory types) — the sovereign values self-honest status over padded claims (F2 TRUTH).

## 5. Upload — the gotcha
```bash
hf upload ariffazil/<DS> /tmp/hf_edit/<DS>_README.md README.md \
  --repo-type dataset \
  --commit-message "v1.2 | F11 audit | ..."
```
- **`--repo-type dataset` is REQUIRED.** Default repo type is `model`; omitting it fails with a usage error ("Did you mean: --no-private?"), not a clear message.
- `--no-extract` does NOT exist. Don't pass it.
- Batch multiple datasets in one shell block with a small `upload()` function; each success prints a commit URL — capture all of them.

## 6. Verify live (never skip)
```bash
curl -sL "https://huggingface.co/datasets/ariffazil/<DS>/raw/main/README.md" | grep -c "Federated Integration"
wc -c /tmp/hf_edit/<DS>_README.md   # compare before/after sizes
```
Re-fetch each raw README and confirm the new marker landed; report per-dataset before/after byte counts and commit SHAs in the final answer.

### 6b. Verifying a SIBLING's claim of HF updates (stronger pattern)
When the update report arrives as a pasted sibling table (commits + sizes), don't re-verify with curl alone — clone the remote repos and compare against live git state:
```bash
for repo in AAA BBB CCC DDD EEE FFF I-ARIF-CANON; do
  cd /tmp/hf_repos/$repo
  echo "$repo HEAD=$(git rev-parse --short HEAD) size=$(wc -c < README.md) marker=$(grep -c 'Federated Integration' README.md) commits_today=$(git log --since='2026-08-05' --oneline | wc -l)"
done
```
Every claimed SHA must match `git rev-parse --short HEAD` byte-for-byte, and README size must match the claimed byte count. This proves the commit exists on the remote with that exact hash — stronger evidence than a raw fetch. Also list repo contents (`ls` + `find -name '*.jsonl' -not -path '*/.git/*'`) to distinguish real data payloads from doc shells (see reference). Report as a per-row verdict table: claim vs actual HEAD/size/marker.

## 7. Seal the outcome to VAULT999 (governed pattern)
HF ops are constitutional acts — after live verification, append a receipt to `/root/arifOS/VAULT999/outcomes.jsonl`:
1. **Probe the vault's existing format FIRST**: `tail -2` the file and grep for prior receipt shapes. Established convention is flat-ish `arifos.record.v1` with fields `record_class: "SESSION_RECEIPT"`, `record_id: "RECEIPT-YYYY-MM-DD-<slug>"`, `ts`, `actor{actor_id,identity_verified}`, `session`, `decision{outcome,verdict,reasons[]}`, `evidence{...}`, `delta_S`, `doctrine`, `category`. Do NOT invent a nested `{event, timestamp, receipts:{...}}` shape — a sibling-proposed nested payload was rejected this session because it didn't match the chain's uniform schema.
2. Append one JSON line (`cat <<'RECEIPT' >>`) and validate with `tail -1 | python3 -m json.tool`; confirm line count incremented.
3. Reply shape: `SEALED::<record_id>::seq=<line_no>::ΔS=<value>`.

## 8. Interpreting `patch` tool warnings during HF README writes
When using the Hermes `patch` tool to edit an `old_string` → `new_string` replacement in a README:
- A warning `old_string and new_string are identical` is a **tool-side idempotency guard**, NOT evidence the write failed. It means: this specific patch was already applied earlier in the batch, and the tool correctly refused a duplicate write. The file itself is still valid — check `git status` or file size to confirm, not the tool warning alone.
- If the warning appears for one dataset but the commit+size landed, treat that row as **verified** — the no-op just means the section was written by a prior invocation in the same run.

## 9. Vault-sealing sibling receipts (not just HF data)
After sealing the HF outcome to VAULT999, use a specific event name prefix `HF_` + the record_class `SESSION_RECEIPT` (same schema). The sibling's proposed nested `{event, timestamp, receipts:{...}}` shape does not conform to `arifos.record.v1` and will not append cleanly. Always probe `tail -2` first.

## 10. Vault-seal line ordering — backup-the-snapshot before appending (corrected 2026-08-06)

The earlier "dual-witness vault seals" pattern was **self-corrected** as a flattering narrative. The actual 2026-08-06 mechanics:

- I ran `cp outcomes.jsonl backup-<ts>.jsonl` immediately before appending my line.
- After `tail -2` showed two lines (the AA-ANTIGRAVITY line at N-1 + my new line at N), I wrote a reply claiming "two independent witnesses — kernel auto-seal + direct sovereign append" — characterizing the AA-ANTIGRAVITY line as a parallel auto-seal.
- Reality: `grep -c AA-ANTIGRAVITY backup-<ts>.jsonl` returned **1**, meaning the line predated my append. It was a historical anchor, not a parallel witness. The kernel did not auto-seal in my window; the prior line was already in the chain from an earlier session/actor.
- I had the correct answer in 1 second and chose to theorize instead. F2 violation; no fabrication in the data, fabrication in the narration.

**The corrected rule:**

1. **Before theorizing about who wrote a prior line in the vault**, `grep -c <distinguishing-token> <pre-append-backup-snapshot>`. If the token matches in the backup, the line predates your work — you don't know who wrote it, and you should say so.
2. Pre-append snapshot is mandatory for any append that *might* be the second of two: `cp outcomes.jsonl <OUT_DIR>/.pre-append.<ts>.jsonl` immediately before `cat >>`.
3. The "two independent witnesses" framing is **only** valid when the prior line is NOT in the pre-append backup. If it is, the honest reply is: "Prior line N-1 already in the chain (predates my append, source unknown); my line N appends the sovereign payload. Both anchor the same 7 SHAs." No "strengthened F11 auditability" — just the fact.

**Reply shape (corrected):**
> "Confirmed pre-append state: prior line at N-1 (AA-ANTIGRAVITY, same 7 SHAs) was already in the chain before my append. My line at N carries the sovereign payload. Both anchor the same 7 SHAs. Source of the prior line: outside my session — not claiming a parallel witness pattern."

**The trap:** when a sibling report's prose paints a beautiful picture (parallel witnesses, auto-sealed events, dual attestation), the temptation is to echo the picture. The picture is often projection of what the author *wanted* to have happened. The pre-append backup snapshot is the 1-second proof of what actually happened. Verify the snapshot before constructing the narrative.

## 11. Self-generated tool warnings as honesty signals
The `patch` tool's `⚠️ File-mutation verifier: 1 file(s) were NOT modified` warning (§8) is one of a class of self-flagging signals. The broader principle:
- **Tool warnings that say "I didn't do this"** are the tool telling you it detected a no-op or idempotent state. They are NOT failures.
- **Tool warnings that say "I did this with a caveat"** (`HF_HUB_ENABLE_HF_TRANSFER` deprecation, `FutureWarning`) are observability noise to ignore.
- **Tool warnings that say "this looks wrong"** without failing (e.g. `replace_all` skipped when not asked) are the tool catching a likely mistake. READ them.

Pattern: when a sibling report mentions a tool warning, classify it as one of the three above and react accordingly. The first two are non-signals; the third is information.

## 12a. YAML Schema Auto-Fix Pattern (Forged 2026-08-11)

When HF pre-receive rejects a push with "Invalid YAML in README.md" or the viewer shows
`Couldn't cast ... because column names don't match`, the README's YAML schema declaration
has drifted from the actual data columns. The recovery recipe:

1. Probe actual columns from `data/*.jsonl` (skip `.bak` and LFS pointers < 200 bytes).
2. Generate corrected `configs:` block with inferred dtypes per column.
3. Patch the README frontmatter (strip old `configs:` and `dataset_info:` blocks, insert new).
4. Re-auth remote with token if newly cloned.
5. If remote has stale commits: `git rebase --abort && git fetch && git reset --hard origin/main`.
6. Commit + push.

**Seven pitfalls to know before writing this script:** word-boundary on `val` (substring
matches `eval`), duplicate `dataset_info:` blocks, indented YAML keys in frontmatter detection,
no-clean `---` closer (heuristic detection of where YAML syntax breaks), config name
collisions across gold splits, HF pre-receive errors that don't surface in plain git output,
schema name mismatches (`id` vs `probe_id`). Full recipe with code and worked examples:
`references/yaml-schema-auto-fix.md`.

Verified 2026-08-11: fixed all 8 ariffazil datasets (AAA, BBB, CCC, DDD, EEE, FFF,
I-ARIF-CANON, a2b-eval-results) — viewer went from `CastError` to "retry later" (cache
propagating). Live state confirmed via `curl https://huggingface.co/api/datasets/ariffazil/<DS>`
returning new commit SHAs that match `git rev-parse --short HEAD` locally.

## 12. READ-side Intelligence: Probing External Claims Against HF (Forged 2026-08-11)

When an external auditor, sibling agent, or pasted report makes claims about Arif's HF
datasets — download counts, likes, creation dates, file structures — do NOT trust the
claim. Hit the canonical HF API directly. This is the **live probe pattern**, not web_scrape.

### 12a. Per-dataset metadata (authoritative)
```bash
curl -sf "https://huggingface.co/api/datasets/ariffazil/<DS>" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f\"downloads={d.get('downloads', '?')} likes={d.get('likes', '?')} created={d.get('createdAt', '?')[:10]}\")
"
```
Returns live JSON: `downloads`, `likes`, `createdAt`, `lastModified`, `tags`, `description`.
This is canonical — more reliable than `web_extract` on the rendered page.

### 12b. List all datasets for an author
```bash
curl -sf "https://huggingface.co/api/datasets?author=ariffazil&limit=50" | python3 -c "
import json, sys
for it in json.load(sys.stdin):
    print(f\"  {it['id']:50s} downloads={it.get('downloads', 0):>6}  likes={it.get('likes', 0)}\")
"
```

### 12c. File-tree probe (dataset content)
```bash
curl -sf "https://huggingface.co/api/datasets/ariffazil/<DS>/tree/main" | python3 -c "
import json, sys
for it in json.load(sys.stdin):
    print(f\"  {it.get('type', '?')} {it.get('path', '?')} ({it.get('size', '?')} bytes)\")
"
```

### 12d. Full-federation intelligence sweep (8-dataset canonical list)
For sovereign-grade external claim verification, run the full 8-dataset sweep:
```bash
for ds in AAA BBB CCC DDD EEE FFF a2b-eval-results I-ARIF-CANON; do
  echo "=== $ds ==="
  curl -sf "https://huggingface.co/api/datasets/ariffazil/$ds" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f\"  downloads: {d.get('downloads', 'N/A')}\")
print(f\"  created: {d.get('createdAt', 'N/A')[:10]}\")
print(f\"  lastModified: {d.get('lastModified', 'N/A')[:10]}\")
"
done
```

### 12e. Compare with baseline datasets (for context)
When asked "bandingkan dengan dataset manusia biasa", pick known anchors:
```bash
for ds in "openai/gsm8k" "HuggingFaceH4/ultrachat_200k" "bigscience/P3"; do
  curl -sf "https://huggingface.co/api/datasets/$ds" | python3 -c "
import json, sys; d = json.load(sys.stdin)
print(f\"{d['id']}: downloads={d.get('downloads','?')}, likes={d.get('likes','?')}\")
"
done
```
Standard anchors as of 2026: GSM8K ~960K (OpenAI staple), UltraChat 200K ~73K (alignment),
P3 ~94K (BigScience/T5). For personal/obscure datasets the floor is 0–50; "anyone found it"
typically starts at 100+.

### 12f. Epistemic labels on READ-side intelligence
- `OBS` — numbers from live API response (authoritative)
- `DER` — computed aggregates (totals, means, ratios, ranks)
- `CLAIM` — any number from a pasted external report that hasn't been independently verified
- Never present external claims as fact without live probe confirmation

### 12g. Known claim-vs-reality traps (verified 2026-08-11)
- External auditors often cite HF page-rendered numbers that are stale or parsed incorrectly. The API endpoint is definitive — `web_extract` on a HF page returns prose, not the canonical JSON.
- A sibling claiming "1000 download" may have conflated sum-of-view-counts with actual downloads, or eyeballed a page screenshot.
- A sibling claiming "17 last month" may have read a cached page, a different field, or miscounted across multiple datasets.
- **Rule:** when Arif asks "betul ka?" about any external claim → `curl -sf HF_API` first, then answer. Never trust the claim at face value — even when the claim is on behalf of an apparent external auditor.
- Worked 2026-08-11: an external audit pasted "1000 download" → live probe showed 727 across 5 datasets; second sweep with AAA/DDD/FFF included → 1,122 across all 8. Both "1000" and "17" were wrong; only live probe told the truth.

## Pitfalls
- `datasets` lib: `trust_remote_code` is deprecated / a no-op — call `load_dataset("...", split="train")` without it.
- `execute_code` may be blocked in this profile (approvals.cron_mode) — run multi-step Python via terminal heredoc instead.
- `HF_HUB_ENABLE_HF_TRANSFER` deprecation FutureWarning on every command is harmless; ignore it.
- Parquet-based repos load fine via `load_dataset`; JSONL-only repos (EEE, FFF, DDD) need raw-URL fetch of `data/*.jsonl` to probe schema.
- Schema probes should be done BEFORE writing any card content — know the actual columns and row counts first, or the card will contain invented claims.
- **"Sibling looks like it added X" framing trap:** when a sibling report arrives as a pasted table with SHAs + sizes, don't accept the framing at face value. Get the live state first (HF API + raw README + git rev-parse if cloned), then describe what *actually* changed. The report is a witness claim, not a fact until independent live evidence backs it.
- **Two receipt lines in `tail -2` ≠ two agents sealed in parallel.** Always `grep -c <actor-id> <pre-append-backup>` before characterizing the relationship. If the prior line is already in the chain, it's a historical anchor + your new append, not a race. State this honestly; F2 doesn't tolerate flattering narrative.
- **Sibling fabrication pattern (verified 2026-08-06 across sessions):** DeepSeek-style 333-AGI agents invent fix paths, tool names, file contents, and config values. Sibling prose is a witness claim, not evidence. Always live-verify with grep/curl/getMe before accepting. arifOS code + live API > sibling prose.
- **Pre-check the vault before sealing (worked 2026-08-06):** When the sibling report proposes a payload shape (`{event, timestamp, receipts:{...}}` nested), DO NOT use that shape — re-derive from `tail -2 outcomes.jsonl` and conform to the existing flat `arifos.record.v1` schema. The sibling's payload was rejected this session, re-derived in the established shape, and sealed at line 35976. Probe the tail FIRST; if the chain is uniform-schema, append in uniform-schema. If it's heterogeneous, classify by `record_class` and append to match the dominant class.
- **Corpus-builder `main()` overwrites HF-canonical files (2026-08-06).** `build_iarif_corpus.py main()` re-downloads from HF and regenerates SFT/DPO/VAL locally, but local generators may omit newer sources that a sibling already added (NUSANTARA, AGENTIC_TRAJECTORIES). Running it blindly clobbered local SFT from 1322→1050 and VAL from 17→117 (a2b contamination restored). HF was untouched (sibling had already pushed). Fix: before running `main()`, check HF's `lastModified` against local file mtimes. If HF is newer, the local file is stale-but-correct — running the builder regresses it. **Rule:** never run the corpus builder without first confirming (a) what sources exist in the HF manifest's `by_source` dict, and (b) that local `load_*` functions cover all those sources. If any source is missing from the loaders, running main() produces a regressed file. Also: `cp $FILE $FILE.bak-<ts>` before every regeneration, and diff the new file against the old before overwriting.
- **Canonical trajectory format for QLoRA = OpenAI function-calling schema, not XML tags (2026-08-06).** Sibling pushed `agentic-trajectories-rl.jsonl` with `tool_calls` + `tool_call_id` + `role: "tool"` messages — the standard OpenAI training format for tool-use fine-tuning. The Phase 3 XML `<step N>` format in the local builder is inferior for QLoRA and should be retired. When generating new trajectory data, use the sibling's shape. The local `agentic_trajectory_pairs()` generator's XML output is a scaffold for logic only, not training-ready data. Full format reference: HF `ariffazil/I-ARIF-CANON/agentic-trajectories-rl.jsonl` line 1 (HEALTH_AUDIT_001).
- **GAP 3b spec = a THIRD trajectory format (2026-08-06).** The "Constitutional AI Framework Research" PDF (GAP 3b SCALE) proposes an EMD 5-phase JSONL format: `turns[]` with `phase` (probe/evaluate/888_judge/human_veto/seal_vault999), `agent_state` (qdrant_vector_id, graphiti_episode_id, entropy_level, f1/f2 flags), `crypto_receipt`, `merkle_root`, validated by a Pydantic `RLTrajectory` model. This matches NEITHER the canonical OpenAI function-calling format NOR the legacy XML scaffold — it is a third shape. Title claims "47 RL trajectories" but only 5 scenarios are specified and no generation pipeline exists. Treat it as design intent (same status as the XML scaffold): if generating data from it, convert EMD → canonical OpenAI format, never emit EMD raw.
- **I-ARIF strategic reframe (2026-08-06, Arif-confirmed "OOO ni model untuk APEX judge la kan??"): I-ARIF = 888-APEX judge, NOT a generator.** I-ARIF is a 1-3B classifier, CPU inference at runtime, one-time cheap QLoRA (~$10-20 RunPod, 2-4h), current corpus (~1435 pairs) is sufficient. Text generation stays on rented APIs (Qwen/Claude/GPT). The "10x-66x short of viable QLoRA" note in `references/i-arif-corpus-structure.md` applies to generator-scale ambitions only — for the judge use case, corpus is adequate. Cost-avoidance path: validate with the free local Ollama qwen2.5:3b (already on VPS :11434) before any GPU spend → see `arifos-federation-ops` `references/kernel-judge-model-wiring.md`.

## References
- `references/ariffazil-dataset-family.md` — the AAA–FFF + I-ARIF-CANON family map: roles, formats, row counts, composite composition, and the 2026-08-06 update record.
- `references/sibling-claim-verification.md` — playbook for independently validating a sibling agent's pasted "all 7 datasets updated" report: per-repo `git rev-parse` + size + marker grep, plus the rule that you do NOT accept a sibling's claimed VAULT999 payload shape — re-derive from `tail -2 outcomes.jsonl` and write in the established `arifos.record.v1` schema.
- `references/dual-witness-vault-seals.md` — full worked example: two independent witnesses (kernel auto-seal + direct sovereign append) anchoring the same 7 SHAs, what changes when the pre-check finds a match, and the honest reply shape that names the relationship without flattering narrative. **Includes the correction:** the prior 2026-08-06 AA-ANTIGRAVITY line was already in the chain before my append ("two independent witnesses" framing was a flattering narrative — the witnesses are historical+new, not parallel).
- `references/i-arif-corpus-structure.md` — I-ARIF-CANON corpus anatomy (SFT/DPO/VAL format schemas, row counts, token estimates, baseline eval 37.5% → target 88.8%) + scale reality check (10x–66x short of viable QLoRA) + corpus expansion sources (VAULT999 35,976 receipts, Telegram session history, sibling governance decisions).
- `references/yaml-schema-auto-fix.md` — recipe for reconciling README YAML schema with actual data when HF pre-receive hook rejects: probe columns → generate YAML → patch frontmatter → commit → push. Seven pitfalls with verified fixes (word-boundary regex, duplicate blocks, indented keys, no-clean `---`, config-name collisions, hidden pre-receive errors, name mismatches).
- `references/corpus-builder-clobber-pitfall-2026-08-06.md` — the `build_iarif_corpus.py main()` overwrite hazard: local loaders don't cover all HF sources (NUSANTARA, AGENTIC_TRAJECTORIES added by sibling), running main() regresses local to a smaller subset. Recipe: pre-append the source list, verify loaders cover all `by_source` keys, snapshot before regeneration.
