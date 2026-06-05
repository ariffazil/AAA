#!/usr/bin/env python3
"""
Intelligence Forge — DeepSeek Batch Analysis Engine
═════════════════════════════════════════════════════
Feeds entire codebases / document collections to DeepSeek V4 via 1M context.
Returns structured findings with file paths, line numbers, and remediation plans.

Usage:
    python intelligence_forge.py audit /root/arifOS --query "Find all pydantic V3 deprecation warnings"
    python intelligence_forge.py refactor /root/A-FORGE/src --query "Simplify error handling middleware"
    python intelligence_forge.py compare /root/arifOS /root/A-FORGE --query "Identify duplicate governance logic"
    python intelligence_forge.py testgen /root/AAA --query "Generate tests.md for all skills missing them"

DITEMPA BUKAN DIBERI — Forged, Not Given
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Add budget guard
sys.path.insert(0, str(Path(__file__).parent))
from budget_guard import check_budget, estimate_cost, log_usage

# DeepSeek client setup
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: uv pip install openai")
    raise SystemExit(1)

API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEFAULT_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

if not API_KEY:
    print("ERROR: DEEPSEEK_API_KEY not set. Export it or add to /etc/arifOS/secrets.env")
    raise SystemExit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# File inclusion patterns for different analysis types
PATTERNS = {
    "python": ["*.py", "*.pyi"],
    "typescript": ["*.ts", "*.tsx"],
    "javascript": ["*.js", "*.jsx"],
    "markdown": ["*.md", "*.mdx"],
    "yaml": ["*.yaml", "*.yml"],
    "all_code": ["*.py", "*.ts", "*.tsx", "*.js", "*.jsx", "*.json", "*.yaml", "*.yml"],
    "all": ["*"],
}

EXCLUDES = {
    "__pycache__",
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".ruff_cache",
    ".mypy_cache",
    "*.pyc",
}


def collect_files(root: Path, pattern: list[str], max_tokens: int = 900_000) -> tuple[str, int]:
    """Collect files into a context string, respecting token budget."""
    chunks: list[str] = []
    total_chars = 0
    max_chars = max_tokens * 3  # rough heuristic: 1 token ≈ 3-4 chars for code

    for pat in pattern:
        for path in sorted(root.rglob(pat)):
            if any(part.startswith(".") and part != ".github" for part in path.relative_to(root).parts):
                continue
            if any(x in str(path) for x in EXCLUDES):
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue

            header = f"\n{'='*60}\n# FILE: {path.relative_to(root)}\n{'='*60}\n"
            chunk = header + content

            if total_chars + len(chunk) > max_chars:
                chunks.append(f"\n[... truncated: remaining files skipped to fit context window ...]\n")
                break

            chunks.append(chunk)
            total_chars += len(chunk)

    context = f"# PROJECT ROOT: {root}\n# TOTAL FILES SCANNED: {len(chunks)}\n"
    context += "".join(chunks)
    # Rough token estimate
    tokens = len(context) // 3
    return context, tokens


def build_system_prompt(mode: str) -> str:
    prompts = {
        "audit": """You are a senior code auditor for the arifOS Constitutional Federation.
Analyze the provided codebase and produce a structured JSON report with these keys:
- "findings": list of objects with "severity" (critical/high/medium/low), "file", "line", "description", "remediation"
- "summary": brief overview
- "metrics": { "files_analyzed": N, "issues_found": N, "critical_count": N }
Be precise. Include exact file paths and line numbers where possible.""",

        "refactor": """You are a senior architect for the arifOS Constitutional Federation.
Analyze the provided codebase and produce a structured JSON refactoring plan:
- "targets": list of objects with "file", "current_code", "proposed_code", "rationale", "risk_level"
- "dependencies": list of files that would need co-changes
- "estimated_effort": "S|M|L"
Be conservative. Do not propose changes to constitutional files (floors.py, judgment.py) without 888_JUDGE escalation.""",

        "compare": """You are a federation governance analyst.
Compare the two provided codebases and produce a structured JSON diff:
- "duplicates": list of functions/logic duplicated across repos
- "conflicts": list of authority conflicts (two files claiming same canonical role)
- "gaps": list of functionality present in repo A but missing in repo B
- "recommendations": prioritized consolidation plan
Focus on governance, authority boundaries, and shared utilities.""",

        "testgen": """You are a test engineer for the arifOS Constitutional Federation.
For each skill or module in the provided codebase that lacks tests, generate:
- "test_plans": list of objects with "target_file", "test_framework", "test_cases" (list of {input, expected, forbidden, escalation})
- "coverage_gaps": list of untested critical paths
- "priority_order": which tests to write first
Use pytest for Python, node:test for TypeScript.""",
    }
    return prompts.get(mode, prompts["audit"])


def run_analysis(
    mode: str,
    query: str,
    context: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.3,
) -> dict:
    """Send context to DeepSeek and return structured response."""
    check_budget()  # raises if exceeded

    system_prompt = build_system_prompt(mode)
    user_prompt = f"""## ANALYSIS REQUEST
Mode: {mode}
Query: {query}

## CODEBASE CONTEXT
{context}

## INSTRUCTIONS
Respond ONLY with valid JSON. No markdown fences, no commentary outside the JSON."""

    est_input = len(user_prompt) // 3
    est_output = 4000  # conservative
    est_cost = estimate_cost(model, est_input, est_output)
    print(f"[forge] Estimated cost: ${est_cost:.4f} | Model: {model}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=8000,
        response_format={"type": "json_object"},
    )

    usage = response.usage
    cost_entry = log_usage(
        model=model,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        cache_hit_tokens=getattr(usage, "prompt_cache_hit_tokens", 0),
        purpose=f"intelligence_forge:{mode}:{query[:60]}",
        actor="kimi-forge",
    )

    print(f"[forge] Actual cost: ${cost_entry['cost_usd']:.6f} | Tokens: {usage.prompt_tokens} in / {usage.completion_tokens} out")

    try:
        result = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        result = {
            "error": "Failed to parse JSON response",
            "raw": response.choices[0].message.content[:2000],
            "parse_error": str(e),
        }

    result["_meta"] = {
        "model": model,
        "cost_usd": cost_entry["cost_usd"],
        "tokens_in": usage.prompt_tokens,
        "tokens_out": usage.completion_tokens,
        "query": query,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Intelligence Forge — DeepSeek Batch Analysis")
    parser.add_argument("mode", choices=["audit", "refactor", "compare", "testgen"])
    parser.add_argument("paths", nargs="+", help="Root directory(s) to analyze")
    parser.add_argument("--query", "-q", required=True, help="Analysis query/prompt")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="DeepSeek model")
    parser.add_argument("--pattern", "-p", default="all_code", help=f"File pattern: {list(PATTERNS.keys())}")
    parser.add_argument("--out", "-o", help="Output JSON file")
    parser.add_argument("--temp", type=float, default=0.3)

    args = parser.parse_args()

    # Budget check
    status = check_budget()
    print(f"[forge] Budget: ${status['spent_usd']:.2f} spent / ${status['ceiling_usd']:.2f} ceiling")

    # Collect context
    if args.mode == "compare" and len(args.paths) != 2:
        parser.error("compare mode requires exactly 2 paths")

    contexts = []
    total_tokens = 0
    for path_str in args.paths:
        root = Path(path_str).resolve()
        if not root.exists():
            print(f"ERROR: Path does not exist: {root}")
            raise SystemExit(1)

        pattern = PATTERNS.get(args.pattern, PATTERNS["all_code"])
        ctx, tokens = collect_files(root, pattern)
        contexts.append(ctx)
        total_tokens += tokens

    combined = "\n\n".join(contexts)
    print(f"[forge] Collected ~{total_tokens:,} tokens of context from {len(args.paths)} path(s)")

    # Run
    result = run_analysis(args.mode, args.query, combined, args.model, args.temp)

    # Output
    output = json.dumps(result, indent=2, default=str)
    if args.out:
        Path(args.out).write_text(output)
        print(f"[forge] Results saved to: {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
