# Corpus-Builder `main()` Overwrite Hazard (2026-08-06)

## The pattern

`build_iarif_corpus.py main()` regenerates local SFT/DPO/VAL JSONL files from HF sources. It is a clone-and-overwrite pipeline:
1. Download from HF (`ariffazil/AAA`, `BBB`, `CCC`, `DDD`, `EEE`, `FFF`, `a2b-eval-results`)
2. Download from local canon (`/root/arifOS/GENESIS`, `/root/AAA/docs`, `/root/AAA/agents`, `/root/AAA/prompts`)
3. Run generators against the loaded rows
4. Write JSONL files to `OUT_DIR`

## The hazard: HF grows, local loaders don't

When a sibling pushes a new HF update that adds **new sources** (e.g. NUSANTARA for BM/Penang loghat, AGENTIC_TRAJECTORIES for multi-turn agentic SFT), the local generator code does NOT automatically know about those sources. Running `main()` re-clones HF, but the local generators only emit the row patterns they were coded to emit. The output regresses to the older subset.

**Concrete 2026-08-06 regression:**

| File | Pre-run (HF canonical) | Post-run (my main()) | Net delta |
|---|---|---|---|
| `i-arif-sft.jsonl` | 1,322 pairs (26 FLOOR + 258 NUSANTARA + 1,024 CANON + 14 AGENTIC) | 1,050 pairs (26 FLOOR + 1,024 CANON) | -272 (lost NUSANTARA + AGENTIC) |
| `i-arif-val.jsonl` | 17 probes (5 EEE + 12 FFF, F1-F13 clean) | 119 probes (5 EEE + 12 FFF + 102 a2b contamination) | +102 (a2b back in VAL gate) |
| `i-arif-dpo.jsonl` | 96 pairs | 96 pairs | 0 (stable) |

HF was untouched (sibling had already pushed 04:41:56; my run at 04:42:29 only touched local files). After restart, I pulled HF canonical down to revert local state.

## The pre-flight recipe

Before running `python3 build_iarif_corpus.py`:

```bash
# 1. Get HF manifest's `by_source` dict (ground truth)
curl -sf https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/manifest.json | \
  python3 -c "import json,sys; m=json.load(sys.stdin); print(json.dumps(m.get('sft',{}).get('by_source',{}), indent=2))"
# Output should be: {"FLOOR_TABLE": 26, "CANON": 1024, "NUSANTARA": 258, "AGENTIC_TRAJECTORIES": 14}

# 2. Search local builders for source coverage
grep -E "source.*==.*[\"']|source.*startswith\(" /root/forge_work/i-arif-prep/build_iarif_corpus.py | grep -E "NUSANTARA|AGENTIC"
# 0 hits = local builders don't cover HF sources

# 3. If 0 hits, DO NOT run main() — pull HF canonical instead
curl -sf https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/i-arif-sft.jsonl -o /root/forge_work/i-arif-prep/i-arif-sft.jsonl
# (then verify SHA matches)
```

## Forward fix (not yet applied)

Add a sanity check at the top of `main()`:

```python
# Pre-flight: warn if HF sources exceed local coverage
HF_MANIFEST = json.loads(requests.get(
    "https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/manifest.json",
    timeout=10).text)
HF_SOURCES = set(HF_MANIFEST['sft'].get('by_source', {}).keys())
LOCAL_LOADERS = {'FLOOR_TABLE', 'CANON', 'AAA_DOC', 'AGENT_CARD', 'PROMPT'}  # what loaders cover
missing = HF_SOURCES - LOCAL_LOADERS
if missing:
    print(f"⚠️  HF has sources {missing} that local loaders don't cover.")
    print(f"   Running main() will regress SFT/DPO/VAL to a smaller subset.")
    print(f"   Press Ctrl-C to abort, or pass --force-clobber to proceed.")
    if not getattr(main, 'force_clobber', False):
        sys.exit(1)
```

This is the structural fix. The structural fix is not yet applied; the recipe above is the runtime workaround.

## Recovery recipe (when clobbered)

```bash
cd /root/forge_work/i-arif-prep
# Snapshot the regressed files first (for traceability)
cp i-arif-sft.jsonl backup-clobbered-sft-$(date -u +%Y%m%dT%H%M).jsonl
cp i-arif-val.jsonl backup-clobbered-val-$(date -u +%Y%m%dT%H%M).jsonl

# Pull HF canonical
curl -sf https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/i-arif-sft.jsonl -o i-arif-sft.jsonl
curl -sf https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/i-arif-dpo.jsonl -o i-arif-dpo.jsonl
curl -sf https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/i-arif-val.jsonl -o i-arif-val.jsonl
curl -sf https://huggingface.co/datasets/ariffazil/I-ARIF-CANON/raw/main/manifest.json -o manifest.json

# Verify SHA matches (stale but directionally right)
sha256sum i-arif-sft.jsonl i-arif-dpo.jsonl i-arif-val.jsonl
```

## The structural lesson

The `build_iarif_corpus.py` pipeline is a **regenerative copy** — it should be a one-way mirror from HF to local, not a regenerator. If the loader doesn't cover all sources, the generator should refuse to write or write only a properly-labeled subset. The current code writes if asked, regresses silently, and only surfaces the damage when the next SHA check fails.

This is the same pattern as the JS `dist/` stale-source trap (skill `verify-sibling-ops-reports` §1) — a source-vs-runtime drift where the regen produces a file that does not match the upstream it claims to mirror. The fix is the same shape: make the regen either (a) refuse on incomplete coverage, or (b) emit a side-by-side diff that the user must approve before overwrite.

## Related references

- `hf-governed-dataset-ops` §7 — vault-seal schema before appending (same probing-before-acting discipline).
- `verify-sibling-ops-reports` §1 — "Already patched" / "source fixed / runtime not" trap family.
- `ariffazil-dataset-family.md` — the AAA–FFF + I-ARIF-CANON family map; track each repo's "last sibling update" date so you know when local loaders may have gone stale.
