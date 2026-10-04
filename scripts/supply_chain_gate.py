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
# Two exact-pin syntaxes are in use: npm's pkg@x.y.z and PEP 508's pkg==x.y.z.
# The original single npm-only pattern reported exactly-pinned uvx specs as unpinned,
# which blocked every commit in the repo. Both now count as pinned; a syntax the runner
# cannot resolve is reported as a warning, because that is a runtime defect, not a
# supply-chain one.
PINNED_NPM = re.compile(r"^(@[^/@\s]+/)?[^@\s=]+@\d+\.\d+")
PINNED_PEP508 = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(\[[^\]]+\])?==\d+\.\d+")
# Which exact-pin syntaxes each runner actually resolves. Measured on uv 0.11.8:
# `uvx pkg@x.y.z` and `uvx pkg==x.y.z` BOTH resolve, so uvx accepts either and
# warning on `@` there would be a false alarm on every commit. npm resolves only `@`.
ACCEPTED_FOR_RUNNER = {"npx": (PINNED_NPM,), "uvx": (PINNED_NPM, PINNED_PEP508)}
RUNNERS = {"npx", "uvx"}
# Flags whose argument IS a package spec, so it must be pinned too.
SPEC_FLAGS = {"-p", "--package", "--from", "--with"}
# Flags whose argument is a plain value — skip the flag and its argument.
VALUE_FLAGS = {"--registry", "--timeout"}
# These supply the runnable spec, so a later positional is program argv, not a package.
PRIMARY_SUPPLIED_BY_FLAG = {"--from", "-p", "--package"}


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
    """Return EVERY package-spec token in a runner invocation.

    Covers the three real shapes:
      uvx PKG [argv...]            -> [PKG]
      uvx --with DEP PKG [argv...] -> [DEP, PKG]      (both are installs; both must be pinned)
      uvx --from PKG CMD [argv...] -> [PKG]           (CMD is argv, not a package)
    Everything after the primary spec is a program argument (connection string,
    project ref) and is ignored.

    The previous version skipped the argument of every flag uniformly, so with
    `--with DEP PKG` it returned DEP and never looked at PKG — an unpinned primary
    package passed the gate. `--from PKG` was skipped outright for the same reason.
    """
    args = args if isinstance(args, list) else ([args] if args else [])
    specs = []
    primary_taken = False
    i = 0
    while i < len(args):
        a = args[i]
        if not isinstance(a, str):
            i += 1
            continue
        if a in SPEC_FLAGS:
            if i + 1 < len(args) and isinstance(args[i + 1], str) and args[i + 1]:
                specs.append(args[i + 1])
                if a in PRIMARY_SUPPLIED_BY_FLAG:
                    primary_taken = True
            i += 2
            continue
        if a in VALUE_FLAGS:
            i += 2
            continue
        if a.startswith("-") or "://" in a:
            i += 1
            continue
        if not primary_taken:
            specs.append(a)
        break  # the first positional ends the spec region
    return specs


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
            accepted = ACCEPTED_FOR_RUNNER[runner]
            for t in tokens_from_command(runner, args):
                if not is_pinned(t):
                    violations.append((path, runner, t))
                elif not any(p.match(t) for p in accepted):
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
        print(f"SUPPLY-CHAIN GATE [WARN]: '{token}' under {runner} in {p} carries an exact version but in a "
              f"syntax {runner} does not resolve ({runner} wants {want}) — that install will likely fail at "
              f"runtime. Not blocking: pinning is this gate's contract, runner-syntax validity is not.",
              file=sys.stderr)

    if violations:
        for p, runner, token in sorted(set(violations)):
            hint = "pkg@x.y.z" if runner == "npx" else "pkg==x.y.z"
            print(f"SUPPLY-CHAIN GATE [BLOCK]: unpinned {runner} install '{token}' in {p} — pin it ({hint}) and register in {REGISTRY}", file=sys.stderr)
        sys.exit(1)
    print(f"SUPPLY-CHAIN GATE [PASS]: {len(paths)} watched config(s), all external installs pinned ({len(reg.get('pins', {}))} pins registered)")


if __name__ == "__main__":
    main()
