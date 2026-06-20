#!/usr/bin/env python3
"""
MalayMMLU format-fix audit script.

Reproduces the Faysal format-fix critique: compare model accuracy on MalayMMLU
in its native format vs a standardised fixed format.

Usage:
    export OPENAI_API_KEY=sk-...
    export ILMU_API_KEY=...
    python malmmlu_format_audit.py --model gpt-4o --n 100 --output results.json

Requires:
    pip install datasets openai requests pandas
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from dataclasses import asdict, dataclass
from typing import Any

import requests

# Optional HF datasets loader
try:
    from datasets import load_dataset

    HF_DATASETS_AVAILABLE = True
except Exception:  # pragma: no cover
    HF_DATASETS_AVAILABLE = False


DEFAULT_DATASET = "UMxYTLAILabs/MalayMMLU"
ILMU_API_URL = "https://api.ilmu.ai/v1/chat/completions"


@dataclass
class AuditConfig:
    model: str
    n_questions: int
    seed: int
    output: str
    dataset: str
    condition: str  # "both", "native", "fixed"
    openai_key: str | None
    ilmu_key: str | None
    anthropic_key: str | None


@dataclass
class Question:
    id: str
    question: str
    choices: list[str]
    answer: str  # "A", "B", "C", or "D"
    subject: str | None
    source_format: dict[str, Any]


def parse_args() -> AuditConfig:
    parser = argparse.ArgumentParser(description="MalayMMLU format-fix audit")
    parser.add_argument("--model", default="gpt-4o", help="Model identifier")
    parser.add_argument("--n", type=int, default=100, help="Number of questions")
    parser.add_argument("--seed", type=int, default=20260620, help="Random seed")
    parser.add_argument("--output", default="malmmlu_format_audit_results.json", help="Output JSON path")
    parser.add_argument("--dataset", default=DEFAULT_DATASET, help="Hugging Face dataset name")
    parser.add_argument(
        "--condition",
        default="both",
        choices=["both", "native", "fixed"],
        help="Which format condition to run",
    )
    args = parser.parse_args()

    return AuditConfig(
        model=args.model,
        n_questions=args.n,
        seed=args.seed,
        output=args.output,
        dataset=args.dataset,
        condition=args.condition,
        openai_key=os.environ.get("OPENAI_API_KEY"),
        ilmu_key=os.environ.get("ILMU_API_KEY"),
        anthropic_key=os.environ.get("ANTHROPIC_API_KEY"),
    )


def load_malmmlu(dataset_name: str, n: int, seed: int) -> list[Question]:
    """Load MalayMMLU and sample n questions."""
    if not HF_DATASETS_AVAILABLE:
        raise RuntimeError(
            "Hugging Face datasets library not available. "
            "Install with: pip install datasets"
        )

    ds = load_dataset(dataset_name, split="train")
    total = len(ds)
    if n > total:
        n = total

    rng = random.Random(seed)
    indices = rng.sample(range(total), n)

    questions: list[Question] = []
    for idx in indices:
        row = ds[idx]
        # MalayMMLU schema: prompt (question + embedded choices), options (list),
        # key (letter A-D), subject, category, level, num_options
        question_text, choices = parse_prompt_and_options(row)
        answer_letter = str(row.get("key", "")).strip().upper()
        if not answer_letter or answer_letter not in "ABCD":
            continue
        if not choices:
            continue
        questions.append(
            Question(
                id=f"q-{idx}",
                question=question_text,
                choices=[str(c) for c in choices],
                answer=answer_letter,
                subject=str(row.get("subject", row.get("category", "unknown"))),
                source_format=dict(row),
            )
        )
    return questions


def parse_prompt_and_options(row: dict[str, Any]) -> tuple[str, list[str]]:
    """Extract clean question text and options from MalayMMLU row."""
    options = [str(c) for c in row.get("options") or []]
    prompt = str(row.get("prompt", ""))
    if not options:
        return prompt, []
    # Remove the choice lines from the prompt to get clean question text.
    # The prompt ends with lines like "A. ...\nB. ..."
    clean = prompt
    for opt in options:
        clean = clean.replace(opt, "")
    # Remove dangling option letters that may remain if options list is incomplete
    clean = re.sub(r"\n[A-D]\.\s*$", "", clean.strip())
    clean = re.sub(r"\n[A-D]\)\s*$", "", clean.strip())
    return clean.strip(), options


def build_native_prompt(q: Question) -> str:
    """Use the dataset's native layout as closely as possible."""
    return q.source_format.get("prompt", q.question)


def strip_choice_prefix(choice: str) -> str:
    """Remove leading letter/prefix like 'A. ' or 'A) ' from option text."""
    return re.sub(r"^[A-D][\.\)]\s*", "", choice).strip()


def build_fixed_prompt(q: Question) -> str:
    """Standardise to clear A/B/C/D format with explicit instruction."""
    prompt = "Question:\n" + q.question + "\n\nChoices:\n"
    letters = ["A", "B", "C", "D"]
    for letter, choice in zip(letters, q.choices):
        clean_choice = strip_choice_prefix(choice)
        prompt += f"{letter}) {clean_choice}\n"
    prompt += "\nAnswer with only the letter A, B, C, or D."
    return prompt


def extract_letter(text: str) -> str | None:
    """Extract the first A/B/C/D from model output."""
    if not text:
        return None
    # Look for isolated letter at start or after punctuation/whitespace
    match = re.search(r"\b([A-D])\b", text.strip())
    if match:
        return match.group(1)
    return None


def call_openai(model: str, prompt: str, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 50,
    }
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def call_anthropic(model: str, prompt: str, api_key: str) -> str:
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": 50,
        "temperature": 0.0,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["content"][0]["text"]


def call_ilmu(model: str, prompt: str, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 200,
    }
    resp = requests.post(
        ILMU_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def call_model(config: AuditConfig, prompt: str) -> str:
    if config.model.startswith("gpt-") or config.model.startswith("o"):
        if not config.openai_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        return call_openai(config.model, prompt, config.openai_key)
    if config.model.startswith("claude-"):
        if not config.anthropic_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        return call_anthropic(config.model, prompt, config.anthropic_key)
    if config.model.startswith("ilmu-"):
        if not config.ilmu_key:
            raise RuntimeError("ILMU_API_KEY not set")
        return call_ilmu(config.model, prompt, config.ilmu_key)
    raise ValueError(f"Unsupported model: {config.model}")


def run_condition(config: AuditConfig, questions: list[Question], condition: str) -> list[dict[str, Any]]:
    results = []
    for q in questions:
        prompt = build_native_prompt(q) if condition == "native" else build_fixed_prompt(q)
        try:
            raw_response = call_model(config, prompt)
        except Exception as e:
            raw_response = f"ERROR: {e}"
        predicted = extract_letter(raw_response)
        results.append(
            {
                "id": q.id,
                "condition": condition,
                "subject": q.subject,
                "ground_truth": q.answer,
                "predicted": predicted,
                "correct": predicted == q.answer,
                "raw_response": raw_response,
                "prompt": prompt,
            }
        )
    return results


def compute_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    correct = sum(1 for r in results if r.get("correct"))
    accuracy = correct / total if total else 0.0
    return {
        "n": total,
        "correct": correct,
        "accuracy": round(accuracy, 4),
        "accuracy_percent": round(accuracy * 100, 2),
    }


def main() -> int:
    config = parse_args()
    print(f"Loading {config.dataset} and sampling {config.n_questions} questions...")
    questions = load_malmmlu(config.dataset, config.n_questions, config.seed)
    print(f"Loaded {len(questions)} questions.")

    all_results: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "model": config.model,
        "dataset": config.dataset,
        "n_questions": len(questions),
        "seed": config.seed,
        "conditions": {},
    }

    conditions = []
    if config.condition in ("both", "native"):
        conditions.append("native")
    if config.condition in ("both", "fixed"):
        conditions.append("fixed")

    for condition in conditions:
        print(f"\nRunning condition: {condition}")
        results = run_condition(config, questions, condition)
        all_results.extend(results)
        summary["conditions"][condition] = compute_metrics(results)
        print(f"  Accuracy: {summary['conditions'][condition]['accuracy_percent']}%")

    # Add per-subject breakdown for fixed condition if available
    if "fixed" in summary["conditions"]:
        fixed_results = [r for r in all_results if r["condition"] == "fixed"]
        by_subject: dict[str, dict[str, Any]] = {}
        for r in fixed_results:
            sub = r.get("subject") or "unknown"
            by_subject.setdefault(sub, []).append(r)
        summary["by_subject_fixed"] = {
            sub: compute_metrics(items) for sub, items in by_subject.items()
        }

    output = {
        "config": asdict(config),
        "summary": summary,
        "results": all_results,
    }

    with open(config.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResults written to {config.output}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
