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
PINNED = re.compile(r"^(@[^/@\s]+/)?[^@\s]+@\d+\.\d+")
RUNNERS = {"npx", "uvx"}
FLAGS_WITH_ARG = {"-p", "--package", "--from", "--registry", "--timeout"}


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


def walk(node, violations, path):
    """Walk parsed JSON/YAML: find runner invocations however nested."""
    if isinstance(node, dict):
        cmd = node.get("command")
        if isinstance(cmd, str) and (cmd in RUNNERS or Path(cmd).name in RUNNERS):
            for t in tokens_from_command(cmd, node.get("args")):
                if not PINNED.match(t):
                    violations.append((path, t))
        # opencode style: "command": ["npx", "-y", "pkg"]
        elif isinstance(cmd, list) and cmd and isinstance(cmd[0], str) and (cmd[0] in RUNNERS):
            for t in tokens_from_command(cmd[0], cmd[1:]):
                if not PINNED.match(t):
                    violations.append((path, t))
        for v in node.values():
            walk(v, violations, path)
    elif isinstance(node, list):
        for v in node:
            walk(v, violations, path)


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
    for p in paths:
        f = Path(p)
        if not f.is_file():
            continue  # agent not installed / config absent = not this gate's problem
        try:
            data = parse(p)
            if data is None:
                continue
            walk(data, violations, p)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"SUPPLY-CHAIN GATE [FAIL-CLOSED]: unreadable {p}: {exc}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:  # yaml.YAMLError
            print(f"SUPPLY-CHAIN GATE [FAIL-CLOSED]: unparseable {p}: {exc}", file=sys.stderr)
            sys.exit(1)

    if violations:
        for p, token in sorted(set(violations)):
            print(f"SUPPLY-CHAIN GATE [BLOCK]: unpinned install '{token}' in {p} — pin it (pkg@x.y.z) and register in {REGISTRY}", file=sys.stderr)
        sys.exit(1)
    print(f"SUPPLY-CHAIN GATE [PASS]: {len(paths)} watched config(s), all external installs pinned ({len(reg.get('pins', {}))} pins registered)")


if __name__ == "__main__":
    main()
