#!/usr/bin/env python3
"""
Agent Evaluation Harness — DeepSeek Batch Testing
═══════════════════════════════════════════════════
Run N iterations of a task through DeepSeek V4, measure:
- success_rate, avg_latency, cost_per_run, total_cost
- failure modes, hallucination rate, tool-call accuracy

Usage:
    python agent_eval_harness.py \
        --task "Generate a Python function that validates email addresses" \
        --iterations 50 \
        --model deepseek-v4-flash \
        --criteria "function_exists,valid_regex,edge_cases_handled"

DITEMPA BUKAN DIBERI — Forged, Not Given
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from budget_guard import check_budget, estimate_cost, log_usage

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: uv pip install openai")
    raise SystemExit(1)

API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEFAULT_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

if not API_KEY:
    print("ERROR: DEEPSEEK_API_KEY not set.")
    raise SystemExit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def _eval_response(response_text: str, criteria: list[str]) -> dict:
    """Simple heuristic evaluation. Override with proper eval logic."""
    text = response_text.lower()
    scores = {}
    for crit in criteria:
        scores[crit] = crit.lower().replace("_", " ") in text or crit.lower() in text
    return scores


def run_single(
    task: str,
    model: str,
    system_prompt: str,
    criteria: list[str],
    temperature: float,
) -> dict:
    """Run one iteration."""
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task},
            ],
            temperature=temperature,
            max_tokens=4000,
        )
        latency = time.perf_counter() - start
        content = response.choices[0].message.content

        cost_entry = log_usage(
            model=model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            purpose=f"eval_harness:{task[:40]}",
            actor="kimi-eval",
        )

        eval_scores = _eval_response(content, criteria)
        passed = all(eval_scores.values())

        return {
            "success": True,
            "passed": passed,
            "latency_ms": round(latency * 1000, 1),
            "cost_usd": cost_entry["cost_usd"],
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
            "eval_scores": eval_scores,
            "response_preview": content[:500],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "cost_usd": 0.0,
        }


def run_harness(
    task: str,
    iterations: int,
    model: str,
    criteria: list[str],
    temperature: float,
    parallel: int = 4,
) -> dict:
    """Run full harness."""
    check_budget()

    system_prompt = """You are an agent in the arifOS Constitutional Federation.
Execute the given task precisely. Respond with working code or structured data.
Do not include explanatory text outside the requested output format."""

    est = estimate_cost(model, 500, 1500) * iterations
    print(f"[harness] Est. total cost: ${est:.4f} for {iterations} iterations")
    print(f"[harness] Running {iterations} iterations with concurrency={parallel}...")

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {
            pool.submit(run_single, task, model, system_prompt, criteria, temperature): i
            for i in range(iterations)
        }
        for future in as_completed(futures):
            i = futures[future]
            try:
                res = future.result()
            except Exception as e:
                res = {"success": False, "error": str(e)}
            results.append(res)
            status = "PASS" if res.get("passed") else ("FAIL" if res.get("success") else "ERR")
            print(f"  [{i+1}/{iterations}] {status} | ${res.get('cost_usd', 0):.6f} | {res.get('latency_ms', 0):.0f}ms")

    # Aggregate
    successes = [r for r in results if r.get("success")]
    passes = [r for r in results if r.get("passed")]
    total_cost = sum(r.get("cost_usd", 0) for r in successes)
    latencies = [r["latency_ms"] for r in successes if "latency_ms" in r]

    report = {
        "meta": {
            "task": task,
            "model": model,
            "iterations": iterations,
            "timestamp": datetime.now(UTC).isoformat(),
        },
        "summary": {
            "success_rate": round(len(successes) / iterations * 100, 1),
            "pass_rate": round(len(passes) / iterations * 100, 1),
            "total_cost_usd": round(total_cost, 4),
            "avg_cost_per_run_usd": round(total_cost / max(len(successes), 1), 6),
            "avg_latency_ms": round(sum(latencies) / max(len(latencies), 1), 1) if latencies else 0,
            "max_latency_ms": round(max(latencies), 1) if latencies else 0,
        },
        "failures": [r for r in results if not r.get("success")],
        "passes": [r for r in results if r.get("passed")],
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", "-t", required=True)
    parser.add_argument("--iterations", "-n", type=int, default=10)
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL)
    parser.add_argument("--criteria", "-c", default="function_exists,valid_output", help="Comma-separated pass criteria")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--temp", type=float, default=0.5)
    parser.add_argument("--out", "-o", help="Output JSON file")
    args = parser.parse_args()

    criteria = [c.strip() for c in args.criteria.split(",")]
    report = run_harness(args.task, args.iterations, args.model, criteria, args.temp, args.parallel)

    output = json.dumps(report, indent=2, default=str)
    if args.out:
        Path(args.out).write_text(output)
        print(f"\n[harness] Report saved to: {args.out}")
    print(output)


if __name__ == "__main__":
    main()
