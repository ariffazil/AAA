---
id: fi-mesh-check
name: fi-mesh-check
version: 1.0.0
description: "Probe all FI coder CLIs live (qwen/kimi/opencode/codex/claude/grok/gemini) with a minimal falsification prompt and report the mesh matrix. Use when Arif says 'mesh check', 'test all coder CLIs', 'FI mesh health', 'are all harnesses alive', or before/after cross-FI plumbing work."
owner: 333-AGI
risk_tier: low
floor_scope: [F2, F4]
capability_tier: fed-long-context
ecology_state: WARM
---

# FI Mesh Check — falsification probe

Probe every FI coder CLI in the federation with a minimal falsification prompt. For each: run the CLI's one-shot mode asking it to reply with an exact marker string, capture output tail, and classify **PASS / FAIL / EXTERNAL**.

## Current invocations (verify against disk before trusting — these drift)

- Kimi: `kimi -m zai-coding-plan/glm-5.3 -p "Reply with exactly: KIMI-MESH-OK"`
- OpenCode: `opencode run --model litellm-federation/forge-777 "Reply with exactly: OPENCODE-MESH-OK"`
- Codex: `codex exec --skip-git-repo-check "Reply with exactly: CODEX-MESH-OK"` (goes through :4010 middleware)
- Grok: `grok -p "..."` (402 = balance exhausted → EXTERNAL flag, not a mesh defect)
- Gemini: `GEMINI_CLI_TRUST_WORKSPACE=true gemini -p "..."` (429 = quota → EXTERNAL)

## Rules

- Timeout each probe at 90s; one retry only for transient network.
- Never mask an error as pass. One marker mismatch = FAIL.
- Classify external billing/quota failures (402/429) separately from mesh defects — EXTERNAL ≠ FAIL.
- Probe the correct layer before claiming absence: 401 on a health endpoint = service UP (auth-gated); conn-refused/timeout = DOWN.
- When a CLI reports "high demand" / load errors, probe its endpoint directly — middleware faults masquerade as vendor load (scar: :4010 responses-path, 2026-08-21).

## Output

End with the matrix table (FI × verdict × latency × hcsvog × note) + any root-cause fix performed. Root-cause fixes go to the responsible FI lane, not self-assigned cross-lane edits.

### hcsvog columns (ETCSOVG harness metadata, arxiv 2605.23950)

Capture per-FI harness identity during probe. Minimum: `h_fingerprint` + `h_tools` + `h_gov`.

| Column | Source | Example |
|---|---|---|
| h_fingerprint | SHA256-first-8 of harness config | `a3f1c902` |
| h_tools | Tool availability tier | `full`, `mcp-core`, `minimal`, `none` |
| h_gov | Governance config | `333:yolo`, `333:confirm` |

If harness metadata cannot be determined for an FI, mark as `—` (never infer).
