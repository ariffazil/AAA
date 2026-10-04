# Corpus Expansion from VAULT999 — Source Inventory & Pipeline (2026-08-06)

## Problem

I-ARIF-CANON has 1,521 SFT/DPO/VAL examples — 10x–66x short of viable QLoRA fine-tuning.
VAULT999 has 36,000+ receipts that represent real governance decisions. These are the richest
expansion source, but they require extraction.

## Data Sources Inventory

### VAULT999 (`/root/arifOS/VAULT999/outcomes.jsonl`)

**Critical:** Lines can be concatenated JSON objects (multiple JSON per line) AND some lines
decode as plain strings (not dicts). Always use `JSONDecoder.raw_decode()` loop, skip non-dict.

```python
import json

def iter_objs(path):
    with open(path) as f:
        for line in f:
            text = line.strip()
            if not text: continue
            decoder = json.JSONDecoder(strict=False)
            idx = 0
            while idx < len(text):
                try:
                    obj, end = decoder.raw_decode(text, idx)
                    if isinstance(obj, dict):
                        yield obj
                    idx = end
                    while idx < len(text) and text[idx] in ' \t\n':
                        idx += 1
                except json.JSONDecodeError:
                    break
```

**Verified inventory (2026-08-06):**

| record_class | Count | SFT/DPO Value |
|---|---|---|
| tool_call | ~4,846 | Low (repetitive UNKNOWN verdicts from f006-edge-probe) |
| SESSION_RECEIPT | 14 | HIGH — full governance decisions with intent/decision/evidence/effects |
| COMMIT_RECEIPT | 65 | MEDIUM — commit summaries with organ context |
| CONSTITUTIONAL_SEAL | 1 | HIGH — rare sovereign decisions |
| SOVEREIGN_SEAL | 1 | HIGH — rare sovereign decisions |
| tool_call (non-UNKNOWN) | ~0 | Low — all 4,846 had verdict:UNKNOWN |

**tool_call agent distribution:**
- f006-edge-probe: 2,610 (all UNKNOWN verdicts — probe noise, not training data)
- openclaw: 1,023 (UNKNOWN — session noise)
- ARIF: 344 (UNKNOWN — sovereign actions)
- 333-AGI: 209 (UNKNOWN — agent actions)
- agi-gate-010-cycle: 120 (UNKNOWN — gate cycle)

**tool_call tool distribution:**
- arif_init: 3,431 (session starts — not useful for SFT)
- arif_observe: 604 (observations — potentially useful)
- arif_think: 574 (reasoning — potentially useful)
- arif_judge: 135 (judgments — HIGH value)
- arif_seal: 52 (seals — HIGH value)
- arif_memory: 27 (memory — MEDIUM)
- arif_route: 18 (routing — MEDIUM)
- arif_forge: 5 (forge — HIGH value but rare)

### gate_fire.jsonl (`/root/.local/share/arifos/gate_fire.jsonl`)

99 entries. Agent tool-blocking events — when agents tried tools and got rejected.

**Schema:**
```json
{
  "timestamp": "2026-07-24T03:33Z",
  "agent": "opencode",
  "gate": "STATELESS_WHITELIST",
  "blocked_tools": ["forge_entropy_sweep", ...],
  "reason": "HTTP path requires stdio session ownership"
}
```

**Agent distribution:** opencode (4), 333-AGI (1), unknown (92 — pre-schema entries)

**SFT Value:** HIGH — these are real governance decisions (gate rejected agent action).
Each entry becomes a pair: "Agent X tried tools [Y] → BLOCKED: [reason] under [gate]".
These teach the model WHEN tools should be refused, not just HOW to call them.

### rsi-ledger.jsonl (`/root/.local/share/arifos/rsi-ledger.jsonl`)

79 entries. Session bottleneck analysis — what went wrong and how to fix.

**Schema (two variants):**
```json
// Variant 1: simple
{"session_id": "...", "bottleneck": "none", "fix": "none_required", "delta_S": 0.0, ...}

// Variant 2: trace-enriched
{"session_id": "...", "trace": {"task": "...", "tools_called": [...], "phase": "..."}, "diagnose": {...}}
```

**SFT Value:** MEDIUM — session-level analysis, not per-decision. Useful for
trajectory context ("what happened in this session") but not for single-turn SFT.

### opencode_receipts.jsonl (`/root/.local/share/arifos/opencode_receipts.jsonl`)

4,240 entries. OpenCode session events — mostly error events.

**Schema:**
```json
{"event": "session.created.error", "error": "...", "timestamp": "..."}
```

**SFT Value:** LOW for corpus — error logs, not governance decisions. Useful for
eval/negative examples only.

### arifflow_receipts.jsonl (`/root/.local/share/arifos/arifflow_receipts.jsonl`)

2,450 entries. Flow metabolism receipts.

**SFT Value:** MEDIUM — flow cycle decisions, but format needs probing.

## Pipeline Architecture

The existing `build_iarif_corpus.py` (25,901 bytes) at `/root/forge_work/i-arif-prep/` is the
canonical builder. It reads HF datasets (AAA–FFF) + local canon → SFT/DPO/VAL JSONL.

**Expansion path:** a new script (`forge_corpus_expand.py`) would:
1. Parse VAULT999 SESSION_RECEIPTs → SFT pairs (intent → decision + reasoning + evidence)
2. Parse gate_fire → SFT pairs (blocked tool request → rejection with floor reference)
3. Parse rsi-ledger trace entries → trajectory pairs (task → tools_called → outcome)
4. Synthesize multi-turn trajectories from tool_call sequences (see I-ARIF-CANON README)
5. Generate DPO pairs from gate_fire (chosen = governance-correct, rejected = blocked action)
6. Append to existing i-arif-sft.jsonl / i-arif-dpo.jsonl

**Output format must match existing schemas:**
- SFT: `{"instruction": "...", "input": "...", "output": "...", "source": "...", "type": "sft"}`
- DPO: `{"prompt": "...", "chosen": "...", "rejected": "...", "source": "...", "probe_id": "...", "type": "dpo"}`

## Trajectory Format (OpenAI messages[] — the user's spec)

The user specified the target training format as multi-turn messages[] with tool_calls:

```json
{
  "messages": [
    {"role": "system", "content": "You are Hermes..."},
    {"role": "user", "content": "[SYSTEM_EVENT]: ..."},
    {"role": "assistant", "content": "...", "tool_calls": [{"id": "call_xxx", "type": "function", "function": {"name": "...", "arguments": "..."}}]},
    {"role": "tool", "tool_call_id": "call_xxx", "content": "{...}"},
    {"role": "assistant", "content": "...", "tool_calls": [{"id": "call_yyy", "type": "function", "function": {"name": "888_judge", "arguments": "..."}}]},
    {"role": "tool", "tool_call_id": "call_yyy", "content": "{...}"},
    {"role": "assistant", "content": "...", "tool_calls": [{"id": "call_zzz", "type": "function", "function": {"name": "seal_receipt", "arguments": "..."}}]},
    {"role": "tool", "tool_call_id": "call_zzz", "content": "{...}"},
    {"role": "assistant", "content": "... [SILENT]"}
  ]
}
```

This is distinct from the flat step format in the existing 3 RL trajectories on HF.
Both formats exist in I-ARIF-CANON. The messages[] format is the one that trains
multi-turn tool-call sequences with governance decisions baked into weights.

## Key Insight

The raw numbers tell the story:
- 1,521 current examples (10x short)
- 36,000+ VAULT999 entries (but ~4,846 tool_calls are all UNKNOWN verdicts = probe noise)
- ~14 SESSION_RECEIPTs = gold (real governance decisions)
- ~99 gate_fire entries = gold (real tool rejections)
- ~79 rsi-ledger entries = silver (session analysis)

The SESSION_RECEIPTs are the highest-value extraction source because they contain the
full governance loop: intent → decision → evidence → effects → zen. Each one becomes
10-20 SFT variations with prompt rewrites (different angles on the same decision).

The gate_fire entries are the highest-value DPO source because they contain the
actual tool-rejection patterns with reasons and gates.
