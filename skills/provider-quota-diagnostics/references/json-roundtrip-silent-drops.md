# JSON Round-Trip Silent Drops

**Session:** 2026-08-07 (Qwen Individual Pro FED wiring)
**Skill:** federation-model-routing (bundled, read-only)
**Affected files:** Large JSON configs with nested structures (observed: OpenCode `opencode.json` at 2200+ lines)

## The bug

Using Python `json.load() → mutate → json.dump()` on OpenCode's `opencode.json` **silently dropped 3 entries from the top-level `enabled_providers` array** (`bailian-token-plan-payments`, `qwen-token-plan`, `qwen-responses`). The resulting file was valid JSON, all other fields intact — no errors, no warnings, no syntax issues.

```bash
# Before (backup):
"enabled_providers": ["bailian-token-plan-payments","deepseek","kimi","litellm-federation","mimo-token-plan","minimax","ollama","qwen-responses","qwen-token-plan","qwen-token-plan-individual"]

# After (python3 json.load → json.dump):
"enabled_providers": ["deepseek","kimi","litellm-federation","mimo-token-plan","minimax","ollama","qwen-responses","qwen-token-plan-individual"]
# bailian-token-plan-payments, qwen-token-plan — gone
```

Root cause: **not fully diagnosed.** Could be (a) serialization order issue where `json.dump` skips unsorted keys, (b) file read from a stale snapshot during concurrent writes, or (c) Python version/implementation quirk with indent mode on large arrays.

## Impact

The dropped entries silently disabled 2 providers in OpenCode's runtime. Agents using `bailian-token-plan-payments/qwen3.7-plus` as their primary model would silently fall back to an error or default model at next invocation — a silent regression until the next agent session runs.

## Detection

**Always diff against backup after any json.load/dump mutation:**

```bash
# After mutation:
diff <(python3 -m json.tool /root/forge_work/backups/opencode.json-*.json | grep -v _last | grep -v _patch) \
     <(python3 -m json.tool /root/.config/opencode/opencode.json | grep -v _last | grep -v _patch) | head -50

# Look specifically for lines prefixed with "<" (removed) that have no "+" (added) partner:
# Those are drops, not changes.
```

## Safe alternatives

| Method | When | Risk |
|---|---|---|
| `patch` tool (string find-replace) | Adding/removing individual items in a known block | **Lowest** — text-based, no structural risk |
| `python3` with **post-write diff** | Bulk changes needing structural validity | Medium — requires mandatory diff check |
| `jq` for array/object surgery | Single-key operations on well-formed JSON | Low — jq's serialization is more predictable |
| Hand-edit via `read_file` + `patch` | One-or-two line changes | Low — manual but precise |

**Iron rule:** Never declare a json.dump result "good" without a `diff` against the backup. The absence of syntax errors does not mean the absence of data loss.

## The fix applied

After discovering the drop, restored the `enabled_providers` array from the backup using a targeted Python script that only overwrites that single key:

```python
import json
backup = json.load(open('/path/to/backup.json'))
current = json.load(open('/target/file.json'))
current["enabled_providers"] = backup["enabled_providers"]
with open('/target/file.json', 'w') as f:
    json.dump(current, f, indent=2, ensure_ascii=False)
```

The drop was caught before any agent session consumed the corrupted config.
