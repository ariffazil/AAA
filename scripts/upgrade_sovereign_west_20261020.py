#!/usr/bin/env python3
"""upgrade_sovereign_west_20261020.py — origin-diversified last-resort rung.

Problem (proved by live probe 2026-10-20, claude-code-kvm8/FI-002):
  All 17 seat fallback ladders in litellm-config.yaml were 100% Chinese-origin
  (deepseek / minimax / glm / qwen / mimo). The only Western rungs were dead:
    - OPENCODE_GO rungs  -> "Insufficient account funds"
    - MISTRAL rungs      -> "billing_payment_failure" AND a bad `openai/mistral/<model>` prefix
    - GEMINI_API_KEY     -> LIVE (gemini-3.6-flash + gemini-2.5-flash both replied OK)
  So one origin cut-off (account, policy, network) drops every seat.

What this script changes (idempotent):
  1. adds model group `sovereign-west` (2 Gemini deployments, verified live)
  2. appends `sovereign-west` as the final rung of every seat fallback ladder
  3. fixes the `openai/mistral/<model>` double-prefix bug on 3 Mistral groups
  4. bumps the writer-of-record header

Read-only unless --write is passed. Rollback: git checkout -- litellm-config.yaml
"""
import re
import sys
import yaml

CFG = "/root/A-FORGE/litellm-config.yaml"
WRITE = "--write" in sys.argv
GROUP = "sovereign-west"

HEADER_ANCHOR = "Bump log: 2026-10-18 333-AGI — reconciled 9 unlogged upstream entries (8x go-* + fed/minimax-tts); NOT deployed (incarnation verify pending)."
HEADER_NEW = "Bump log: 2026-10-20 claude-code-kvm8 (FI-002) — added sovereign-west last-resort rung to all seat ladders + fixed mistral double-prefix; reason: 100% Chinese-origin single-point dependency (live probe evidence in script header)."

BLOCK = """# ============================================================
# SOVEREIGN-WEST — origin-diversified LAST-RESORT rung
# Added 2026-10-20 by claude-code-kvm8 (FI-002). Live probe evidence:
#   GEMINI_API_KEY  -> OK (gemini-3.6-flash, gemini-2.5-flash)
#   OPENCODE_GO     -> dead (Insufficient account funds)
#   MISTRAL         -> dead (billing_payment_failure)
# CN providers stay primary (cost/capability). This rung only exists so a
# single-origin cut-off degrades the federation instead of stopping it.
# ============================================================
- model_name: sovereign-west
  litellm_params:
    model: gemini/gemini-3.6-flash
    api_key: os.environ/GEMINI_API_KEY
    order: 0
  model_info:
    max_input_tokens: 1048576
    max_output_tokens: 65536
    mode: chat
    supports_vision: true
    notes: 'sovereign-west W1 — verified live 2026-10-20.'
- model_name: sovereign-west
  litellm_params:
    model: gemini/gemini-2.5-flash
    api_key: os.environ/GEMINI_API_KEY
    order: 1
  model_info:
    max_input_tokens: 1048576
    max_output_tokens: 65536
    mode: chat
    supports_vision: true
    notes: 'sovereign-west W2 — second model, same key (single-key caveat).'
"""


def main() -> int:
    lines = open(CFG, encoding="utf-8").read().split("\n")
    changed = []

    # 1) group definition
    if any(l.strip() == f"- model_name: {GROUP}" for l in lines):
        print("group already present")
    else:
        # append at the END of model_list (before the next top-level key)
        ml = lines.index("model_list:")
        idx = next(i for i in range(ml + 1, len(lines)) if re.match(r"^[a-z_]+:$", lines[i]))
        lines[idx:idx] = BLOCK.split("\n")
        changed.append("group+" + GROUP)

    # 2) fallback ladder rung (idempotent, every seat in `fallbacks:`)
    i0 = next(i for i, l in enumerate(lines) if l.rstrip() == "  fallbacks:")
    i1 = next(i for i in range(i0 + 1, len(lines)) if re.match(r"^  [a-z_]+:$", lines[i]))
    added = 0
    if not any(l.strip() == f"- {GROUP}" for l in lines[i0:i1]):
        seat_re = re.compile(r"^  - [a-zA-Z0-9._/-]+:$")
        out = []
        seen_seat = False
        for i in range(i0 + 1, i1):
            if seat_re.match(lines[i]) and seen_seat:
                out.append(f"    - {GROUP}")
                added += 1
            if seat_re.match(lines[i]):
                seen_seat = True
            out.append(lines[i])
        if seen_seat:
            out.append(f"    - {GROUP}")
            added += 1
        lines[i0 + 1:i1] = out
        changed.append(f"ladders+{added}")
    else:
        print("ladder rung already present")

    # 3) mistral double-prefix fix
    fixes = 0
    for i, l in enumerate(lines):
        m = re.match(r"^(\s*model: )openai/mistral/(.+)$", l)
        if m:
            lines[i] = f"{m.group(1)}openai/{m.group(2)}"
            fixes += 1
    if fixes:
        changed.append(f"mistral-prefix-fix+{fixes}")

    # 4) writer-of-record bump
    hit = next((i for i, l in enumerate(lines) if HEADER_ANCHOR in l), None)
    if hit is not None:
        lines.insert(hit + 1, "# " + HEADER_NEW)
        changed.append("header-bump")
    else:
        print("WARN header anchor not found")

    text = "\n".join(lines)

    # 5) validate BEFORE writing
    data = yaml.safe_load(text)
    groups = [m["model_name"] for m in data["model_list"]]
    assert GROUP in groups, "group missing after edit"
    fb = data["router_settings"]["fallbacks"]
    seats = [list(d)[0] for d in fb]
    missing = [s for d in fb for s in list(d) if GROUP not in d[s]]
    assert not missing, f"ladders missing rung: {missing}"
    print(f"VALIDATE OK: deployments={len(groups)} groups={len(set(groups))} seats={len(seats)} missing={len(missing)}")
    print("changes:", ", ".join(changed) or "none")

    if WRITE:
        open(CFG, "w", encoding="utf-8").write(text)
        print("WROTE", CFG)
    else:
        print("DRY RUN (pass --write to apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
