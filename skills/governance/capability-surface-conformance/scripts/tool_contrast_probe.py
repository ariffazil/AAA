#!/usr/bin/env python3
"""tool_contrast_probe.py — find stub / constant-return tools in a server module.

WHY
    Protocol conformance proves a tool is REACHABLE. It says nothing about whether the body
    COMPUTES. A tool that accepts a rich payload and returns a hard-coded envelope passes a
    smoke call, lists correctly, and carries a valid schema. Its only symptom is that it never
    gives an answer -- it only ever gives the same answer.

HOW
    Two maximally different inputs. Strip every result value the tool merely echoed back
    (any dict key whose name matches a parameter name, recursively) plus volatile timestamp
    fields. Compare what survives:
        differs -> VARIES    the tool responds to its input
        same    -> CONSTANT  the tool ignores its arguments (candidate stub)

USAGE
    python3 tool_contrast_probe.py /path/to/server.py
    python3 tool_contrast_probe.py /path/to/server.py --limit 80 --json

EXIT
    0 = probe ran (verdicts on stdout)
    3 = module could not be imported (wrong interpreter -- NOT evidence about the tool)

READ BEFORE ACTING ON A RESULT
    * Run it with the interpreter that owns the server's dependencies. An ImportError is a
      fact about YOUR interpreter, never evidence about the tool.
    * CONSTANT is a LEAD, not a verdict. A fixed refusal is constant BY DESIGN. Read the
      tool's source before writing it up.
    * Tools with no contrastable parameters are reported UNTESTABLE, never silently skipped.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

VOLATILE = re.compile(r"(^_)|(_at$)|(_ms$)|(^timestamp$)|(^ts$)|(chain_hash)|(^generated$)")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("probe_target", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load a module from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["probe_target"] = mod
    spec.loader.exec_module(mod)
    return mod


def value_for(annotation, profile: str):
    a = str(annotation).lower()
    resp = profile == "B"
    if "bool" in a:
        return resp
    if "int" in a and "float" not in a:
        return 9 if resp else 1
    if "float" in a:
        return 0.9 if resp else 0.1
    if a.startswith("list") or a.startswith("["):
        return ["probe-b-longer-distinct"] if resp else ["probe-a"]
    if a.startswith("dict") or a.startswith("{"):
        return {"k": "probe-b-longer-distinct"} if resp else {"k": "probe-a"}
    return "probe-b-a-much-longer-distinct-value" if resp else "probe-a"


def strip(obj, pnames, depth=0):
    """Drop keys that merely echo a parameter name, and volatile fields."""
    if depth > 6:
        return obj
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in pnames or VOLATILE.search(k):
                continue
            out[k] = strip(v, pnames, depth + 1)
        return out
    if isinstance(obj, list):
        return [strip(v, pnames, depth + 1) for v in obj]
    return obj


def probe(fn):
    sig = inspect.signature(fn)
    params = [p for p in sig.parameters.values()
              if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
    if not params:
        return "UNTESTABLE", "no contrastable parameters"
    outs, errs = [], []
    for profile in ("A", "B"):
        kwargs = {p.name: value_for(p.annotation, profile) for p in params}
        try:
            raw = fn(**kwargs)
            outs.append(json.dumps(strip(raw, set(sig.parameters)), sort_keys=True, default=str))
        except Exception as exc:  # noqa: BLE001 - any raise is a finding about the call
            errs.append(f"{type(exc).__name__}: {exc}")
    if errs:
        # same error for both profiles is itself a constant-return signal
        return ("CONSTANT", errs[0][:200]) if len(errs) == 2 and errs[0] == errs[1] else ("ERROR", errs[0][:200])
    if outs[0] == outs[1]:
        return "CONSTANT", outs[0][:240]
    return "VARIES", ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect constant-return / stub tools in a module.")
    ap.add_argument("path", type=Path)
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        mod = load_module(args.path)
    except Exception as exc:  # noqa: BLE001
        print(f"IMPORT_FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("Wrong interpreter is the usual cause. This is NOT evidence about the tool.", file=sys.stderr)
        return 3

    names = [n for n in dir(mod) if not n.startswith("_") and callable(getattr(mod, n, None))]
    results, counts = [], {"VARIES": 0, "CONSTANT": 0, "UNTESTABLE": 0, "ERROR": 0}
    for name in sorted(names)[: args.limit]:
        fn = getattr(mod, name)
        if not inspect.isfunction(fn) or getattr(fn, "__module__", "") != mod.__name__:
            continue
        verdict, detail = probe(fn)
        counts[verdict] = counts.get(verdict, 0) + 1
        results.append({"tool": name, "verdict": verdict, "detail": detail})

    if args.json:
        print(json.dumps({"module": str(args.path), "counts": counts, "results": results}, indent=2))
    else:
        print(f"module: {args.path}")
        print(f"{'tool':<44} verdict")
        for r in results:
            mark = "  <-- READ THE SOURCE" if r["verdict"] == "CONSTANT" else ""
            print(f"{r['tool']:<44} {r['verdict']}{mark}")
            if r["detail"]:
                print(f"    {r['detail']}")
        print()
        print("counts:", counts)
        print("CONSTANT is a lead, not a verdict -- a fixed refusal is constant by design.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
