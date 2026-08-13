#!/usr/bin/env python3
"""
hermes-nudge-injector.py — Event-Driven Context Injection for AAA Warga Agents
══════════════════════════════════════════════════════════════════════════════

Soft-guidance middleware that replaces fat static system prompts with
conditional nudges fired at three hook points:

  1. pre_llm   — before the LLM receives the prompt (intake gate)
  2. pre_tool  — before a tool call is executed (falsification gate)
  3. post_llm  — before text is shown to a human (collapse gate)

Design principles:
  • Nudges live as YAML/JSON rows, not code.
  • One bad nudge cannot suppress the others (isolated evaluation).
  • Fail-closed: any error → passthrough with a logged receipt.
  • Zero cost when no condition matches.

Contract:
  stdin  : JSON envelope {event, ...event-specific fields..., context}
  stdout : JSON envelope with nudges_applied + modified payload

Usage:
  python3 hermes-nudge-injector.py --event pre_llm < prompt.json
  python3 hermes-nudge-injector.py --event pre_tool < tool_intent.json
  python3 hermes-nudge-injector.py --event post_llm < raw_output.json

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import yaml

    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# ═══════════════════════════════════════════════════════════════════════════════
# Defaults (override with --registry or env HERMES_NUDGE_REGISTRY)
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_REGISTRY = Path(__file__).parent / "hermes-nudges.yaml"
RECEIPT_PATH = Path(
    os.environ.get(
        "HERMES_NUDGE_RECEIPT_PATH",
        "/root/.local/share/arifos/hermes_nudge_injector.jsonl",
    )
)

# Token approximation: 1 token ≈ 0.75 words (English/BM mix).
TOKEN_RATIO = 0.75


# ═══════════════════════════════════════════════════════════════════════════════
# Safe logging
# ═══════════════════════════════════════════════════════════════════════════════
def _now() -> str:
    return datetime.now(UTC).isoformat()


def _write_receipt(record: dict[str, Any]) -> None:
    """Append an audit receipt. Never block on logging failure."""
    try:
        RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RECEIPT_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": _now(), **record}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _approx_tokens(text: str) -> int:
    return max(1, int(len(text.split()) / TOKEN_RATIO))


# ═══════════════════════════════════════════════════════════════════════════════
# Registry loading
# ═══════════════════════════════════════════════════════════════════════════════
def load_registry(registry_path: Path) -> dict[str, Any]:
    """Load nudge registry from YAML or JSON. Return empty on any error."""
    if not registry_path.exists():
        return {"nudges": [], "meta": {"source": str(registry_path), "error": "missing"}}

    try:
        text = registry_path.read_text(encoding="utf-8")
        if registry_path.suffix in (".yaml", ".yml") and _HAS_YAML:
            data = yaml.safe_load(text)
        elif registry_path.suffix in (".yaml", ".yml") and not _HAS_YAML:
            raise RuntimeError("PyYAML not installed; use JSON registry")
        else:
            data = json.loads(text)
        data = data or {}
        data.setdefault("nudges", [])
        data.setdefault("meta", {})
        data["meta"]["source"] = str(registry_path)
        return data
    except Exception as exc:
        _write_receipt(
            {
                "event": "registry_load_error",
                "registry": str(registry_path),
                "error": str(exc),
            }
        )
        return {"nudges": [], "meta": {"source": str(registry_path), "error": str(exc)}}


def _validate_nudge(nudge: Any) -> dict[str, Any] | None:
    """Return a sanitized nudge dict or None if structurally invalid."""
    if not isinstance(nudge, dict):
        return None
    nid = nudge.get("id")
    if not isinstance(nid, str) or not nid:
        return None
    event = nudge.get("event")
    if event not in {"pre_llm", "pre_tool", "post_llm"}:
        return None
    return {
        "id": nid,
        "event": event,
        "priority": int(nudge.get("priority", 100)),
        "condition": nudge.get("condition", {"always": True}),
        "inject_position": nudge.get("inject_position", "last"),
        "text": nudge.get("text", ""),
        "transforms": nudge.get("transforms", []),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Condition evaluation
# ═══════════════════════════════════════════════════════════════════════════════
def _match_condition(condition: dict[str, Any], context: dict[str, Any]) -> bool:
    """Evaluate a single nudge condition against the input context.

    Supported keys (AND-combined):
      always: true
      any_keyword: [list]   — match if ANY keyword present in haystack
      all_keywords: [list]  — match if ALL keywords present
      regex: str            — re.search against haystack
      tool_name: str|list   — exact match against tool_name
      message_count_min: int
      message_count_max: int
      any_of: [list]        — OR-combinator of sub-conditions
    """
    haystack = str(context.get("haystack", "")).lower()
    tool_name = context.get("tool_name", "")
    messages = context.get("messages", [])

    if condition.get("always") is True:
        return True

    if "any_of" in condition:
        sub_conditions = condition["any_of"]
        if not isinstance(sub_conditions, list):
            return False
        return any(_match_condition(sub, context) for sub in sub_conditions)

    # Tracks whether we evaluated at least one recognized constraint and
    # survived all checks. Without this, conditions that only set tool_name
    # or keyword filters would fall through to the final False.
    matched = False

    if "tool_name" in condition:
        wanted = condition["tool_name"]
        wanted_set = {wanted} if isinstance(wanted, str) else set(wanted)
        if tool_name not in wanted_set:
            return False
        matched = True

    if "any_keyword" in condition:
        keywords = condition["any_keyword"]
        if isinstance(keywords, str):
            keywords = [keywords]
        if not any(str(k).lower() in haystack for k in keywords):
            return False
        matched = True

    if "all_keywords" in condition:
        keywords = condition["all_keywords"]
        if isinstance(keywords, str):
            keywords = [keywords]
        if not all(str(k).lower() in haystack for k in keywords):
            return False
        matched = True

    if "regex" in condition:
        pattern = condition["regex"]
        try:
            if not re.search(pattern, haystack, re.IGNORECASE):
                return False
        except re.error:
            return False
        matched = True

    if "message_count_min" in condition:
        if len(messages) < int(condition["message_count_min"]):
            return False
        matched = True

    if "message_count_max" in condition:
        if len(messages) > int(condition["message_count_max"]):
            return False
        matched = True

    return matched


# ═══════════════════════════════════════════════════════════════════════════════
# Event processors
# ═══════════════════════════════════════════════════════════════════════════════
def _build_haystack(event: str, payload: dict[str, Any]) -> str:
    """Flatten relevant input text into a single searchable string."""
    parts: list[str] = []
    if event == "pre_llm":
        for m in payload.get("messages", []):
            parts.append(str(m.get("content", "")))
    elif event == "pre_tool":
        parts.append(str(payload.get("thought", "")))
        parts.append(str(payload.get("tool_name", "")))
        parts.append(json.dumps(payload.get("tool_input", {}), default=str))
    elif event == "post_llm":
        parts.append(str(payload.get("text", "")))
    return "\n".join(parts)


def _inject_message(
    messages: list[dict[str, Any]], text: str, position: str
) -> list[dict[str, Any]]:
    msg = {"role": "system", "content": text.strip()}
    if position == "first":
        return [msg, *messages]
    # default / last
    return [*messages, msg]


def _strip_receipt_blocks(text: str) -> str:
    """Remove [🦾ACT] / [EXE] receipt blocks (including multi-line)."""
    # Strip markdown blocks that start with [🦾ACT] or [EXE]
    text = re.sub(r"\[\s*🦾ACT[^\]]*\].*?(?=\n\[|\Z)", "", text, flags=re.DOTALL)
    text = re.sub(r"\[\s*EXE[^\]]*\].*?(?=\n\[|\Z)", "", text, flags=re.DOTALL)
    # Strip single-line receipt headers
    text = re.sub(r"^\s*\[\s*🦾ACT[^\]]*\].*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\[\s*EXE[^\]]*\].*$", "", text, flags=re.MULTILINE)
    return text


def _strip_epistemic_labels(text: str) -> str:
    """Remove [OBS]/[DER]/[INT]/[SPEC]/[UNKNOWN] tags."""
    return re.sub(
        r"\[\s*(OBS|DER|INT|SPEC|UNKNOWN)\s*\]",
        "",
        text,
        flags=re.IGNORECASE,
    )


def _collapse_blank_lines(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def _apply_post_transforms(text: str, transforms: list[dict[str, Any]]) -> str:
    for tx in transforms:
        if tx.get("strip_labels"):
            text = _strip_epistemic_labels(text)
        if tx.get("strip_receipt_blocks"):
            text = _strip_receipt_blocks(text)
        if tx.get("strip_tables"):
            # Best-effort: remove markdown table lines and their separators.
            lines = text.splitlines()
            kept: list[str] = []
            skip_next = False
            for line in lines:
                if skip_next:
                    skip_next = False
                    continue
                stripped = line.strip()
                if stripped.startswith("|") and stripped.endswith("|"):
                    # Drop this table row; also drop the next line if it is a separator.
                    skip_next = True
                    continue
                kept.append(line)
            text = "\n".join(kept)
        if tx.get("strip_markdown_headings"):
            text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
        if tx.get("collapse_blank_lines"):
            text = _collapse_blank_lines(text)
        if "replace_regex" in tx and "replacement" in tx:
            try:
                text = re.sub(tx["replace_regex"], tx["replacement"], text)
            except re.error:
                pass
    return text.strip()


def process_pre_llm(payload: dict[str, Any], nudges: list[dict[str, Any]]) -> dict[str, Any]:
    messages = list(payload.get("messages", []))
    haystack = _build_haystack("pre_llm", payload)
    applied: list[str] = []
    injected_tokens = 0

    for nudge in sorted(nudges, key=lambda n: n["priority"]):
        ctx = {"haystack": haystack, "messages": messages}
        try:
            if _match_condition(nudge["condition"], ctx):
                text = nudge["text"].strip()
                if not text:
                    continue
                messages = _inject_message(messages, text, nudge["inject_position"])
                applied.append(nudge["id"])
                injected_tokens += _approx_tokens(text)
        except Exception as exc:
            _write_receipt(
                {
                    "event": "nudge_eval_error",
                    "nudge_id": nudge["id"],
                    "hook": "pre_llm",
                    "error": str(exc),
                }
            )

    result = dict(payload)
    result["messages"] = messages
    return {
        "event": "pre_llm",
        "nudges_applied": applied,
        "tokens_injected": injected_tokens,
        "payload": result,
    }


def process_pre_tool(payload: dict[str, Any], nudges: list[dict[str, Any]]) -> dict[str, Any]:
    haystack = _build_haystack("pre_tool", payload)
    applied: list[str] = []
    injected_tokens = 0
    nudge_texts: list[str] = []

    for nudge in sorted(nudges, key=lambda n: n["priority"]):
        ctx = {
            "haystack": haystack,
            "tool_name": payload.get("tool_name", ""),
            "tool_input": payload.get("tool_input", {}),
        }
        try:
            if _match_condition(nudge["condition"], ctx):
                text = nudge["text"].strip()
                if text:
                    nudge_texts.append(text)
                    applied.append(nudge["id"])
                    injected_tokens += _approx_tokens(text)
        except Exception as exc:
            _write_receipt(
                {
                    "event": "nudge_eval_error",
                    "nudge_id": nudge["id"],
                    "hook": "pre_tool",
                    "error": str(exc),
                }
            )

    result = dict(payload)
    if nudge_texts:
        result["nudge_injection"] = "\n\n".join(nudge_texts)
    return {
        "event": "pre_tool",
        "nudges_applied": applied,
        "tokens_injected": injected_tokens,
        "payload": result,
    }


def process_post_llm(payload: dict[str, Any], nudges: list[dict[str, Any]]) -> dict[str, Any]:
    text = str(payload.get("text", ""))
    haystack = text
    applied: list[str] = []
    tokens_before = _approx_tokens(text)

    for nudge in sorted(nudges, key=lambda n: n["priority"]):
        ctx = {"haystack": haystack}
        try:
            if _match_condition(nudge["condition"], ctx):
                text = _apply_post_transforms(text, nudge.get("transforms", []))
                # If the nudge also has text, append as a final collapse instruction
                # (rare; post_llm nudges usually use transforms only).
                if nudge.get("text"):
                    text = text + "\n\n" + nudge["text"].strip()
                applied.append(nudge["id"])
                haystack = text
        except Exception as exc:
            _write_receipt(
                {
                    "event": "nudge_eval_error",
                    "nudge_id": nudge["id"],
                    "hook": "post_llm",
                    "error": str(exc),
                }
            )

    tokens_after = _approx_tokens(text)
    result = dict(payload)
    result["text"] = text
    return {
        "event": "post_llm",
        "nudges_applied": applied,
        "tokens_before": tokens_before,
        "tokens_after": tokens_after,
        "tokens_removed": max(0, tokens_before - tokens_after),
        "payload": result,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main entrypoint
# ═══════════════════════════════════════════════════════════════════════════════
def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hermes event-driven nudge injector",
    )
    parser.add_argument(
        "--event",
        choices=["pre_llm", "pre_tool", "post_llm"],
        help="Hook event to process (can also be supplied in stdin JSON).",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to nudge registry YAML/JSON.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Evaluate nudges but do not modify output payload.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print receipt summary to stderr.",
    )
    return parser.parse_args(argv)


def _passthrough(raw_input: str, reason: str) -> None:
    """Fail-closed: echo the original input unchanged and log the reason."""
    _write_receipt({"event": "passthrough", "reason": reason})
    if raw_input.strip():
        print(raw_input, end="")
    else:
        print(json.dumps({"passthrough": True, "reason": reason}), file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    raw = sys.stdin.read()

    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        _passthrough(raw, f"invalid_json: {exc}")
        return 0

    event = args.event or payload.get("event")
    if not event or event not in {"pre_llm", "pre_tool", "post_llm"}:
        _passthrough(raw, f"unknown_event: {event}")
        return 0

    try:
        registry = load_registry(args.registry)
        raw_nudges = registry.get("nudges", [])
        nudges = []
        for n in raw_nudges:
            sanitized = _validate_nudge(n)
            if sanitized and sanitized["event"] == event:
                nudges.append(sanitized)
            elif sanitized is None:
                _write_receipt({"event": "nudge_validation_error", "nudge": n})

        if event == "pre_llm":
            result = process_pre_llm(payload, nudges)
        elif event == "pre_tool":
            result = process_pre_tool(payload, nudges)
        else:
            result = process_post_llm(payload, nudges)

        result["registry"] = {"source": str(args.registry), "nudges_loaded": len(nudges)}

        if args.dry_run:
            result["dry_run"] = True
            # Do not emit modified payload; emit metadata only.
            dry = {
                "event": event,
                "nudges_applied": result["nudges_applied"],
                "tokens_injected": result.get("tokens_injected"),
                "tokens_removed": result.get("tokens_removed"),
                "dry_run": True,
            }
            print(json.dumps(dry, ensure_ascii=False))
            return 0

        print(json.dumps(result, ensure_ascii=False))

        if args.verbose:
            summary = (
                f"[hermes-nudge-injector] {event}: applied={result['nudges_applied']} "
                f"injected={result.get('tokens_injected', 0)} "
                f"removed={result.get('tokens_removed', 0)}"
            )
            print(summary, file=sys.stderr)

        _write_receipt(
            {
                "event": "nudge_run",
                "hook": event,
                "nudges_applied": result["nudges_applied"],
                "registry": str(args.registry),
            }
        )
        return 0
    except Exception as exc:
        _write_receipt({"event": "fatal_error", "error": str(exc), "trace": traceback.format_exc()})
        _passthrough(raw, f"fatal_error: {exc}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
