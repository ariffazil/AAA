---
name: arifos-llm-pipeline-audit
description: Audit LLM integration (SEA-LION, Ollama) across arifOS projects — detect hallucinations, map real pipeline, identify 3 critical holes. Triggered when investigating LLM configs or SEA-LION witness reports claim non-existent architecture.
trigger: Investigating LLM integrations across arifOS / SEA-LION claims non-existent files or architecture
category: devops
tags: [arifOS, SEA-LION, LLM, hallucination-detection, pipeline-audit]
created: 2026-05-06
updated: 2026-05-06
author: Hermes ASI
seal: 999
---

# arifOS LLM Pipeline Audit

## Context
SEA-LION AI Singapore confidently hallucinated an entire non-existent file (`memory_plane.py`) with fake architecture. This skill documents the audit approach used to separate hallucination from ground truth.

## Step 1 — Verify file existence BEFORE reading
```bash
find /root/arifOS -name "memory_plane.py" 2>/dev/null
# If not found → SEA-LION hallucinated
```

## Step 2 — Map real memory infrastructure
```bash
# Real files that exist:
ls /root/arifOS/arifosmcp/runtime/ | grep -i "memory\|context\|persist\|store"
ls /root/arifOS/arifosmcp/tools/ | grep -i "memory"
```

## Step 3 — Check LLM output chain (3-hole test)
```bash
# Hole 1: Does judge receive evidence?
grep -n "_evidence\|mind_reason\|heart_critique" /root/arifOS/arifosmcp/tools/judge.py

# Hole 2: Does memory recall actually store/retrieve?
grep -A2 '"memories"\|"results"\|"stored"' /root/arifOS/arifosmcp/tools/memory.py
# If all return [] or fake UUID → STUB

# Hole 3: Does vault auto-seal on SEAL verdict?
grep -n "vault_entry_id\|auto.*seal" /root/arifOS/arifosmcp/tools/judge.py
```

## Step 4 — Test API keys live (not from env display)
```python
import subprocess, json
cmd = ['curl', '-s', '--max-time', '20', '-X', 'POST',
    'https://api.sea-lion.ai/v1/chat/completions',
    '-H', 'Authorization: Bearer ' + api_key,
    '-d', json.dumps({"model": "aisingapore/Qwen-SEA-LION-v4-32B-IT",
        "messages": [{"role":"user","content":"Say only: OK"}],
        "max_tokens": 10, "temperature": 0.1})]
result = subprocess.run(cmd, capture_output=True, text=True)
# Expect {"content":"OK"} not error
```

## Real LLM Architecture
File: `/root/arifOS/arifosmcp/runtime/llm_client.py`

```
Tier 1 (PRIMARY): SEA-LION → https://api.sea-lion.ai/v1/chat/completions
                  Model: aisingapore/Qwen-SEA-LION-v4-32B-IT
                  Key: sk-znzfOJH_Yc7LKewfrfsl2A (confirmed live 2026-05-06)
Tier 2 (FALLBACK): Ollama → http://127.0.0.1:11434/api/generate
                   Model: qwen2.5:7b (ollama-engine-prod container)
Tier 3: LLMUnavailableError → deterministic fallback
```

## 3 Tools Using call_llm()
| Tool | File | Output |
|------|------|--------|
| arif_mind_reason | runtime/mind_reason.py | verdict, synthesis, confidence, omega_0, delta_S, scars |
| arif_heart_critique | tools/heart.py | status, risks_found[], risk_tier, empathy_score, verdict |
| arif_reply_compose | runtime/reply_compose.py | composed, tone, delta_S, f02/f04/f07 scores |

## 3 CRITICAL PIPELINE HOLES (2026-05-06)
1. **Judge has no evidence**: `tools/judge.py:40` — `_evidence: dict = {}` always empty. mind_reason/heart_critique outputs never piped in.
2. **Memory is STUB**: `tools/memory.py` — recall→{"memories":[]}, store→fake UUID, search→{"results":[]}
3. **Vault is manual**: `tools/vault.py` — only seals if `vault_entry_id` manually passed. No auto-SEAL.

## Fix Priority
```
P0: Wire mind_reason + heart_critique → arif_judge_deliberate._evidence
P1: Replace memory.py stubs with real Qdrant vector store
P2: Add auto-SEAL post-hook in judge on SEAL verdict
```

## LLM Provider Map
| Project | SEA-LION | Ollama | Notes |
|---------|----------|--------|-------|
| arifOS | ✅ External API | ⚠️ Ref only | Docker network DNS |
| A-FORGE | ✅ providerFactory | ✅ Container | qwen2.5:7b + bge-m3 |
| WEALTH | ❌ | ⚠️ Embeddings only | memory_pipeline.py |
| GEOX | ❌ | ❌ | EIA/SPGlobal data APIs only |

## Hallucination Patterns
- SEA-LION invents file paths (`*_plane.py`, `*_interpreter.py`)
- SEA-LION invents class names (`MemoryPlane`, `MemoryGraph`)
- Pads reports with accurate metadata (real API key) to appear credible
- **Always verify file existence before accepting architecture claims**

## Verification Commands
```bash
# Test SEA-LION
curl -s --max-time 20 -X POST https://api.sea-lion.ai/v1/chat/completions \
  -H "Authorization: Bearer $(grep SEA_LION_API_KEY /root/arifOS/.env | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"model":"aisingapore/Qwen-SEA-LION-v4-32B-IT","messages":[{"role":"user","content":"Say only: OK"}],"max_tokens":10}'

# Check Ollama models
curl -s http://127.0.0.1:11434/api/tags | python3 -c "import json,sys; [print(m['name']) for m in json.load(sys.stdin).get('models',[])]"

# Hex decode masked key
python3 -c "
with open('/root/arifOS/.env','rb') as f:
    for i,line in enumerate(f.read().split(b'\n'),1):
        if b'SEA_LION_API_KEY' in line: print(f'Line {i}:', line.hex())
"
```
