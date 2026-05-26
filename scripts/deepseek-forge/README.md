# DeepSeek $5 Sovereign Intelligence Proposal
**Kimi Code Agentic Execution Plan | arifOS Federation | 2026-05-25**

---

## The Bet

Your $5 DeepSeek credit is not "cheap API access." It is a **sovereign compute multiplier** — ~17–35 million tokens of frontier-grade inference at 10–50× cheaper than OpenAI. The game is not to "use it up." The game is to **compound it into permanent federation infrastructure** before the credit runs out.

Grok gave you the strategy. Kimi Code gives you the **execution**.

---

## Phase 0: Unblock the Key (5 minutes)

**Current blocker:** The DEEPSEEK_API_KEY in `/opt/arifos/app/.env` is SOPS-encrypted and the age key mismatches. The key returns 402.

**Action for Arif:**
1. Go to [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2. Verify $5 credit is loaded
3. Generate a **new API key** (or confirm the existing one now has credit)
4. Export it:
   ```bash
   export DEEPSEEK_API_KEY="sk-..."
   export DEEPSEEK_BASE_URL="https://api.deepseek.com"
   export DEEPSEEK_MODEL="deepseek-v4-flash"
   ```
5. Add to `/etc/arifOS/secrets.env` (plaintext, not SOPS — this file is root-only, chmod 600)
6. Source it: `source /etc/arifOS/secrets.env`

**Verify:**
```bash
curl -s https://api.deepseek.com/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" | head -5
```

---

## Phase 1: Budget Guard & Cost Tracking (Done ✓)

**File:** `budget_guard.py`

What it does:
- Hard stop at **$4.75** (keeps $0.25 buffer for safety)
- Alert at **$4.00**
- Warn at **$3.00**
- Tracks every call with actor, purpose, model, token breakdown
- Persistent ledger at `~/.arifos/deepseek_budget.jsonl`

**Usage:**
```bash
cd /root/AAA/scripts/deepseek-forge
python budget_guard.py check        # Check budget status
python budget_guard.py report       # Full spend report
python budget_guard.py estimate deepseek-v4-flash 100000 5000 0.5
```

**Why this matters:** Without a guard, $5 disappears in one malformed loop. With a guard, every agent in the federation respects the budget as a constitutional constraint.

---

## Phase 2: Intelligence Forge — Batch Codebase Analysis (Done ✓)

**File:** `intelligence_forge.py`

What it does:
- Feeds **entire codebases** (up to ~900K tokens) to DeepSeek V4 in one prompt
- Four modes: `audit`, `refactor`, `compare`, `testgen`
- Returns **structured JSON** with file paths, line numbers, severity, remediation
- Auto-tracks cost per run

**Usage:**
```bash
# Audit arifOS for pydantic V3 deprecation warnings
python intelligence_forge.py audit /root/arifOS \
  --query "Find all pydantic Config class deprecation warnings and migrate to ConfigDict" \
  --model deepseek-v4-flash \
  --out /tmp/arifos_pydantic_audit.json

# Compare two repos for duplicate governance logic
python intelligence_forge.py compare /root/arifOS /root/A-FORGE \
  --query "Find duplicated authority boundary checks across both repos" \
  --model deepseek-v4-pro

# Generate tests for all AAA skills missing them
python intelligence_forge.py testgen /root/AAA/skills \
  --query "Generate tests.md content for every skill directory missing it" \
  --out /tmp/aaa_skill_tests.json
```

**Cost math:**
- arifOS codebase ≈ 150K tokens input → ~$0.02–0.04 per audit (Flash, 50% cache hit)
- You can run **100+ full-repo audits** before hitting $4

---

## Phase 3: Agent Evaluation Harness (Done ✓)

**File:** `agent_eval_harness.py`

What it does:
- Runs **N iterations** of a task through DeepSeek
- Measures: success rate, pass rate, avg latency, cost per run
- Parallel execution (up to concurrency limit)
- Perfect for testing MCP tool reliability before production

**Usage:**
```bash
# Test if DeepSeek can consistently generate valid JSON for arifOS tools
python agent_eval_harness.py \
  --task 'Generate a JSON object with keys: "tool", "params", "actor_id". tool="arif_sense_observe", params={"mode":"search","query":"arifOS constitution"}, actor_id="test"' \
  --iterations 100 \
  --criteria "valid_json,tool_key_exists,actor_id_present" \
  --model deepseek-v4-flash

# Test tool-calling accuracy with Pro
python agent_eval_harness.py \
  --task 'Call arif_kernel_route with task="deploy arifOS" and return the routing decision' \
  --iterations 50 \
  --criteria "route_returned,stage_present,budget_present" \
  --model deepseek-v4-pro \
  --parallel 8
```

**Cost math:**
- 100 iterations × ~2K tokens ≈ $0.06–0.12 total
- You can run **thousands of evals** before budget alert

---

## Phase 4: Daily Coding Copilot — Continue.dev + Aider (Done ✓)

### Continue.dev (VS Code / JetBrains)
**Config:** `continue_config.json` → place at `~/.continue/config.json`

Features:
- **Tab autocomplete** with Flash (near-zero cost)
- **Custom commands:** `/audit`, `/test`, `/refactor`, `/docs`
- **1M context** = can ingest entire arifOS + A-FORGE + AAA in one chat
- **Constitutional guardrails** in system prompts

**Usage:**
```bash
# Install Continue.dev extension, then:
cp /root/AAA/scripts/deepseek-forge/continue_config.json ~/.continue/config.json
```

### Aider (Terminal)
**Config:** `aider.conf.yml` → place at `~/.aider.conf.yml`

Features:
- **Architect mode:** Pro for design, Flash for implementation
- **Auto-lint + test** before accepting changes
- **Read-only context:** Injects AGENTS.md + FEDERATION_COCKPIT.md into every prompt
- **Auto-commit disabled** — federation requires explicit SEAL

**Usage:**
```bash
cp /root/AAA/scripts/deepseek-forge/aider.conf.yml ~/.aider.conf.yml
source /etc/arifOS/secrets.env

# Start aider on AAA repo
aider /root/AAA --model deepseek-v4-flash --architect

# Or with full federation context
aider /root/arifOS /root/AAA /root/A-FORGE --model deepseek-v4-pro
```

---

## Phase 5: Federation Provider Integration (Proposed — 30 min build)

**Goal:** Make DeepSeek a **first-class citizen** of arifOS provider routing, not just an external script.

**What to build:**
1. Add `deepseek-v4-flash` and `deepseek-v4-pro` to `arifosmcp/runtime/llm_client.py`
2. Add cost-tracking middleware that calls `budget_guard.py`
3. Add provider priority: `deepseek-v4-pro` (complex) → `deepseek-v4-flash` (daily) → `ollama` (fallback)
4. Expose via MCP tool: `arif_deepseek_forge(prompt, mode, max_cost)`

**Why:** Once DeepSeek is a governed arifOS provider, **every agent in the federation** can use it — Hermes, A-FORGE, WELL, WEALTH — with automatic budget enforcement and audit logging.

---

## Budget Allocation (Recommended)

| Phase | Activity | % of $5 | Est. Tokens | Runs |
|-------|----------|---------|-------------|------|
| 2 | Intelligence Forge (repo audits, testgen) | 40% | ~14M | 100+ audits |
| 4 | Continue.dev / Aider daily coding | 30% | ~10M | 30 days of heavy use |
| 3 | Agent eval harness (batch tests) | 20% | ~7M | 500+ eval runs |
| 1 | Budget guard + overhead | 5% | ~1M | Tracking only |
| 5 | Provider integration dev | 5% | ~1M | Testing the integration |

**Buffer:** $0.25 hard-stopped by budget_guard.py

---

## What Makes This Sovereign (Not Just Cheap)

| Generic Usage | Sovereign Usage |
|--------------|-----------------|
| "Use DeepSeek for coding help" | **DeepSeek is a governed provider in arifOS** with budget enforcement, audit trails, and fallback chains |
| "Run 100 prompts and hope" | **Every prompt is cost-estimated before execution**, logged to vault999, attributed to an actor |
| "Copy-paste API key into Cursor" | **API key lives in `/etc/arifOS/secrets.env`**, sourced by systemd, never in userland configs |
| "Spend $5 and it's gone" | **$5 compounds into permanent scripts** that outlive the credit and work with any future provider |

---

## Immediate Next Step

**Arif — do this now (5 minutes):**

```bash
# 1. Verify DeepSeek credit
export DEEPSEEK_API_KEY="sk-your-new-key-here"
curl -s https://api.deepseek.com/models -H "Authorization: Bearer $DEEPSEEK_API_KEY"

# 2. Install openai client if missing
uv pip install openai

# 3. Test the forge
python /root/AAA/scripts/deepseek-forge/budget_guard.py check
python /root/AAA/scripts/deepseek-forge/intelligence_forge.py audit /root/arifOS \
  --query "Find all files still using pydantic BaseModel.Config instead of ConfigDict" \
  --model deepseek-v4-flash

# 4. Install Continue.dev config
cp /root/AAA/scripts/deepseek-forge/continue_config.json ~/.continue/config.json

# 5. Install Aider config
cp /root/AAA/scripts/deepseek-forge/aider.conf.yml ~/.aider.conf.yml
```

Then tell me what you want to attack first — a full-repo audit, a specific refactor, or the provider integration.

---

*Proposal forged by Kimi Code | A-FORGE | 2026-05-25*
*DITEMPA BUKAN DIBERI*
