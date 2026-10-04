#!/usr/bin/env python3
"""Supply-Chain Pin Gate — E-2 instance of the Gate Promotion doctrine (AAA/instructions/gate-promotion.md).

Fails closed: registry missing, unreadable config, OR any unpinned npx/uvx install
in a watched config -> exit 1. Enforced at the AAA pre-commit boundary.

Structural scanner: JSON parsed as JSON, YAML parsed as YAML — no text regexes.

Usage:
  supply_chain_gate.py --all          scan every watch_path (pre-commit mode)
  supply_chain_gate.py --path FILE    scan a single file (ad-hoc/test mode)
"""
import json
import re
import sys
from pathlib import Path

REGISTRY = Path("/root/AAA/registries/supply_chain_pins.json")
# Pin syntax is runner-specific: npm uses pkg@x.y.z, uv/PEP 508 uses pkg==x.y.z.
# A single npm-only pattern reported exactly-pinned uvx specs as unpinned.
PINNED_NPM = re.compile(r"^(@[^/@\s]+/)?[^@\s=]+@\d+\.\d+")
PINNED_PEP508 = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(\[[^\]]+\])?==\d+\.\d+")
NATIVE_FOR_RUNNER = {"npx": PINNED_NPM, "uvx": PINNED_PEP508}
RUNNERS = {"npx", "uvx"}
FLAGS_WITH_ARG = {"-p", "--package", "--from", "--registry", "--timeout"}


def is_pinned(token: str) -> bool:
    """This gate's contract is 'an exact version is present' (supply-chain risk).
    Either exact-pin syntax satisfies it; a floating/range/bare spec does not."""
    return bool(PINNED_NPM.match(token) or PINNED_PEP508.match(token))


def load_registry() -> dict:
    if not REGISTRY.is_file():
        print(f"SUPPLY-CHAIN GATE [FAIL-CLOSED]: registry missing: {REGISTRY}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(REGISTRY.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"SUPPLY-CHAIN GATE [FAIL-CLOSED]: registry unreadable: {exc}", file=sys.stderr)
        sys.exit(1)


def tokens_from_command(cmd, args):
    """Given runner name + args list, return the package spec token(s) to verify.

    Only the FIRST non-flag token is the package spec; later tokens are program
    arguments (connection strings, project refs) and are ignored.
    """
    args = args if isinstance(args, list) else ([args] if args else [])
    skip_next = False
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if not isinstance(a, str):
            continue
        if a in FLAGS_WITH_ARG:
            skip_next = True
            continue
        if a.startswith("-") or "://" in a:
            continue
        return [a]
    return []


def walk(node, violations, warnings, path):
    """Walk parsed JSON/YAML: find runner invocations however nested.

    violations = floating/range/bare specs (supply-chain risk) -> block.
    warnings   = exact version present but in the other runner's syntax -> report only,
                 because this gate owns pinning, not runner-syntax validity.
    """
    if isinstance(node, dict):
        cmd = node.get("command")
        runner = None
        args = None
        if isinstance(cmd, str) and (cmd in RUNNERS or Path(cmd).name in RUNNERS):
            runner = cmd if cmd in RUNNERS else Path(cmd).name
            args = node.get("args")
        # opencode style: "command": ["npx", "-y", "pkg"]
        elif isinstance(cmd, list) and cmd and isinstance(cmd[0], str) and (cmd[0] in RUNNERS):
            runner = cmd[0]
            args = cmd[1:]
        if runner is not None:
            native = NATIVE_FOR_RUNNER[runner]
            for t in tokens_from_command(runner, args):
                if not is_pinned(t):
                    violations.append((path, runner, t))
                elif not native.match(t):
                    warnings.append((path, runner, t))
        for v in node.values():
            walk(v, violations, warnings, path)
    elif isinstance(node, list):
        for v in node:
            walk(v, violations, warnings, path)


def parse(path: str):
    text = Path(path).read_text()
    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return json.loads(text)
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return None  # unparseable YAML without yaml lib -> skip file (gate only fails closed on known-readable)


def main() -> None:
    args = sys.argv[1:]
    reg = load_registry()
    if "--all" in args:
        paths = reg.get("watch_paths", [])
    elif "--path" in args:
        paths = [args[args.index("--path") + 1]]
    else:
        print(__doc__)
        sys.exit(2)

    violations = []
    warnings = []
    for p in paths:
        f = Path(p)
        if not f.is_file():
            continue  # agent not installed / config absent = not this gate's problem
        try:
            data = parse(p)
            if data is None:
                continue
            walk(data, violations, warnings, p)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"SUPPLY-CHAIN GATE [FAIL-CLOSED]: unreadable {p}: {exc}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:  # yaml.YAMLError
            print(f"SUPPLY-CHAIN GATE [FAIL-CLOSED]: unparseable {p}: {exc}", file=sys.stderr)
            sys.exit(1)

    for p, runner, token in sorted(set(warnings)):
        want = "pkg@x.y.z" if runner == "npx" else "pkg==x.y.z"
        print(f"SUPPLY-CHAIN GATE [WARN]: '{token}' under {runner} in {p} is exactly pinned but in the "
              f"other runner's syntax ({runner} expects {want}). Not blocking — pinning is this gate's "
              f"contract, runner-syntax validity is not.", file=sys.stderr)

    if violations:
        for p, runner, token in sorted(set(violations)):
            hint = "pkg@x.y.z" if runner == "npx" else "pkg==x.y.z"
            print(f"SUPPLY-CHAIN GATE [BLOCK]: unpinned {runner} install '{token}' in {p} — pin it ({hint}) and register in {REGISTRY}", file=sys.stderr)
        sys.exit(1)
    print(f"SUPPLY-CHAIN GATE [PASS]: {len(paths)} watched config(s), all external installs pinned ({len(reg.get('pins', {}))} pins registered)")


if __name__ == "__main__":
    main()
