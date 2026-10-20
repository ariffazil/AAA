#!/usr/bin/env python3
"""Replace the sovereign-west block with providers proven live on the WORK path.

Correction (2026-10-20, claude-code-kvm8): the first cut used Gemini because
direct generateContent returned OK. Through the proxy it returned 402
("prepayment credits are depleted") — probe path ≠ work path. Groq
(gpt-oss-120b) answered on the work path via api.groq.com, so that becomes W1.
Dead-on-2026-10-20 providers are recorded in the comment, not deployed.
"""
import re
import sys
import yaml

CFG = "/root/A-FORGE/litellm-config.yaml"
WRITE = "--write" in sys.argv

NEW = """# ============================================================
# SOVEREIGN-WEST — origin-diversified LAST-RESORT rung
# Added 2026-10-20 by claude-code-kvm8 (FI-002). Work-path probe evidence:
#   GROQ gpt-oss-120b        -> 200 (W1, deployed here)
#   GEMINI 3.6-flash/2.5-flash -> 402 prepayment depleted (NOT deployed)
#   OPENCODE_GO rungs        -> Insufficient account funds (NOT deployed)
#   OPENROUTER               -> Insufficient credits (NOT deployed)
#   MISTRAL                  -> billing_payment_failure (prefix bug fixed anyway)
# CN providers stay primary (cost/capability). This rung exists so a
# single-origin cut-off degrades the federation instead of stopping it.
# Caveat: Groq free tier is rate-limited — emergency rung, not production.
# ============================================================
- model_name: sovereign-west
  litellm_params:
    model: openai/openai/gpt-oss-120b
    api_base: https://api.groq.com/openai/v1
    api_key: os.environ/GROQ_API_KEY
    order: 0
  model_info:
    max_input_tokens: 131072
    max_output_tokens: 32768
    mode: chat
    notes: 'sovereign-west W1 — Groq gpt-oss-120b, verified 200 on work path 2026-10-20.'
- model_name: sovereign-west
  litellm_params:
    model: openai/openai/gpt-oss-20b
    api_base: https://api.groq.com/openai/v1
    api_key: os.environ/GROQ_API_KEY
    order: 1
  model_info:
    max_input_tokens: 131072
    max_output_tokens: 32768
    mode: chat
    notes: 'sovereign-west W2 — Groq gpt-oss-20b, same key.'
"""


def main() -> int:
    lines = open(CFG, encoding="utf-8").read().split("\n")
    start = next(i for i, l in enumerate(lines) if "SOVEREIGN-WEST — origin-diversified LAST-RESORT rung" in l) - 1
    assert lines[start].startswith("# ==="), lines[start]
    end = lines.index("litellm_settings:")
    old = "\n".join(lines[start:end])
    assert "model_name: sovereign-west" in old, "refusing: block boundaries wrong"
    lines[start:end] = NEW.split("\n")
    text = "\n".join(lines)

    d = yaml.safe_load(text)
    sw = [m for m in d["model_list"] if m["model_name"] == "sovereign-west"]
    assert len(sw) == 2, f"sovereign-west deployments={len(sw)}"
    fb = d["router_settings"]["fallbacks"]
    miss = [k for x in fb for k, v in x.items() if "sovereign-west" not in v]
    assert not miss, f"ladders missing rung: {miss}"
    print(f"VALIDATE OK: deployments={len(d['model_list'])} sovereign-west={len(sw)} seats={len(fb)} missing={len(miss)}")
    if WRITE:
        open(CFG, "w", encoding="utf-8").write(text)
        print("WROTE")
    else:
        print("DRY RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
