#!/usr/bin/env python3
"""
aaa_mcp_json_generator.py — derive Kimi mcp.json from capability registry.

Reads:
  - /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml  (source of truth)
  - /root/AAA/federation/launcher_map.yaml            (process binding)

Writes:
  - /root/.kimi-code/mcp.json                          (regenerated)

Behavior (F1 AMANAH):
  - Backs up existing mcp.json to mcp.json.<UTC>.bak before overwriting
  - Emits ONLY backends that are enabled: true AND seal: sealed
  - Validates the new mcp.json is parseable before declaring success
  - Verdict logged to stdout in INIT format; receipts to /root/AAA/federation/init_receipts/

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Registry/launcher declaration is ambiguous or incomplete — fail closed."""


class AuthorityClassificationError(ValueError):
    """A tool surface contains unclassified or contradictory authority — fail closed."""


REGISTRY_PATH = Path("/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml")
LAUNCHER_MAP_PATH = Path("/root/AAA/federation/launcher_map.yaml")
MCP_JSON_PATH = Path("/root/.kimi-code/mcp.json")
RECEIPT_DIR = Path(os.environ.get("MCPGEN_RECEIPT_DIR", "/root/AAA/federation/init_receipts"))


def _now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _now_utc_compact() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Registry not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Registry root must be a mapping, got {type(data).__name__}")
    return data


def load_launcher_map(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"launchers": {}}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Launcher map root must be a mapping, got {type(data).__name__}")
    return data


def collect_enabled_sealed(
    registry: dict[str, Any],
    launcher_map: dict[str, Any],
) -> list[tuple[str, dict[str, Any]]]:
    """
    Walk the registry axes and collect every backend that is
    (a) enabled: true AND (b) seal: sealed.
    Return list of (backend_name, launcher_entry) pairs.
    """
    launchers = launcher_map.get("launchers", {})
    emitted: list[tuple[str, dict[str, Any]]] = []
    seen: set[str] = set()
    catalogued_enabled_sealed: list[tuple[str, str]] = []  # (name, reason)
    enabled_not_sealed: list[str] = []
    enabled_no_launcher: list[str] = []

    for axis_name, axis_data in registry.get("axes", {}).items():
        if not isinstance(axis_data, dict):
            continue
        for cap_name, cap_data in axis_data.get("canonical_capabilities", {}).items():
            if not isinstance(cap_data, dict):
                continue
            for backend_name, backend_raw in (cap_data.get("backends") or {}).items():
                if not isinstance(backend_raw, dict):
                    continue
                enabled = bool(backend_raw.get("enabled", False))
                seal = backend_raw.get("seal", "pending")
                if enabled and seal == "sealed":
                    catalogued_enabled_sealed.append((backend_name, axis_name))
                    if backend_name in seen:
                        continue  # already processed
                    launcher = launchers.get(backend_name)
                    if launcher is None:
                        enabled_no_launcher.append(backend_name)
                        continue
                    seen.add(backend_name)
                    emitted.append((backend_name, launcher, backend_raw))
                elif enabled and seal != "sealed":
                    enabled_not_sealed.append(backend_name)

    return emitted, catalogued_enabled_sealed, enabled_not_sealed, enabled_no_launcher


def tool_surface_sha256(tools: list[str] | set[str]) -> str:
    """Canonical hash of a tool surface: sorted names, newline-separated, trailing NL."""
    canonical = "\n".join(sorted(tools)) + "\n"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_authority(backend_name: str, backend: dict[str, Any]) -> None:
    """
    Fail-closed authority classification for explicit READ_ONLY backends.

    Rules (S-01 canary):
      - READ_ONLY requires a non-empty positive allowlist.
      - known_tools must be explicitly classified into allowed ∪ forbidden.
      - allowed ∩ forbidden must be empty.
      - mutation_allowed must be false.
      - the declared tool-surface hash must match the sorted known_tools.
    Unknown/unclassified tools are never implicitly allowed.
    """
    if backend.get("authority_class") != "READ_ONLY":
        return

    allowed = backend.get("allowed_tools")
    forbidden = backend.get("forbidden_tools")
    known = backend.get("known_tools")

    if not isinstance(allowed, list) or not allowed:
        raise ConfigurationError(f"backend '{backend_name}': READ_ONLY requires an explicit non-empty allowed_tools")
    if not isinstance(known, list) or not known:
        raise ConfigurationError(f"backend '{backend_name}': READ_ONLY requires known_tools (fail-closed surface)")
    if not isinstance(forbidden, list):
        raise ConfigurationError(f"backend '{backend_name}': READ_ONLY requires forbidden_tools (may be empty)")
    if backend.get("mutation_allowed") is not False:
        raise ConfigurationError(f"backend '{backend_name}': READ_ONLY requires mutation_allowed: false")

    a, f, k = set(allowed), set(forbidden), set(known)
    if a & f:
        raise AuthorityClassificationError(
            f"backend '{backend_name}': tools both allowed and forbidden: {sorted(a & f)}"
        )
    unclassified = k - (a | f)
    if unclassified:
        raise AuthorityClassificationError(
            f"backend '{backend_name}': unclassified tools detected (fail closed): {sorted(unclassified)}"
        )
    extra = (a | f) - k
    if extra:
        raise AuthorityClassificationError(
            f"backend '{backend_name}': classified tools absent from known_tools: {sorted(extra)}"
        )

    declared = backend.get("tool_surface_sha256")
    actual = tool_surface_sha256(k)
    if declared != actual:
        raise ConfigurationError(
            f"backend '{backend_name}': tool surface hash mismatch (declared={declared} actual={actual})"
        )


def _inject_allowlist(
    backend_name: str,
    backend: dict[str, Any],
    args: list[str],
) -> list[str]:
    """Insert the positive allowlist flag before the backend separator."""
    flag = backend.get("allowlist_flag")
    allowed = backend.get("allowed_tools") or []
    if not flag:
        raise ConfigurationError(f"backend '{backend_name}': READ_ONLY requires allowlist_flag")
    if not allowed:
        raise ConfigurationError(f"backend '{backend_name}': READ_ONLY requires allowed_tools to emit")
    inject = [str(flag), ",".join(allowed)]
    if "--" in args:
        i = args.index("--")
        return args[:i] + inject + args[i:]
    return args + inject


def build_mcp_servers(
    emitted: list[tuple[str, dict[str, Any], dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    """
    Translate (backend_name, launcher_entry, backend_declaration) triples into a
    Kimi mcpServers dict. Only stdio and http transports are valid for Kimi;
    filesystem (e.g. VAULT999) is not an MCP and is skipped here.
    """
    servers: dict[str, dict[str, Any]] = {}
    for backend_name, launcher, backend in emitted:
        validate_authority(backend_name, backend)
        transport = launcher.get("transport")
        if transport not in ("stdio", "http"):
            # filesystem or other — Kimi does not spawn these
            continue
        entry: dict[str, Any] = {"description": launcher.get("description", "")}
        if transport == "stdio":
            command = launcher.get("command")
            if not command:
                raise ValueError(f"Launcher for '{backend_name}' is stdio but has no command")
            entry["command"] = command
            args = list(launcher.get("args") or [])
            if backend.get("authority_class") == "READ_ONLY":
                args = _inject_allowlist(backend_name, backend, args)
            if args:
                entry["args"] = args
            env = launcher.get("env") or {}
            if env:
                entry["env"] = dict(env)
        else:  # http
            url = launcher.get("url")
            if not url:
                raise ValueError(f"Launcher for '{backend_name}' is http but has no url")
            entry["url"] = url
        if "startup_timeout_ms" in launcher:
            entry["startupTimeoutMs"] = int(launcher["startup_timeout_ms"])
        if "tool_timeout_ms" in launcher:
            entry["toolTimeoutMs"] = int(launcher["tool_timeout_ms"])
        entry["enabled"] = True
        servers[backend_name] = entry
    return servers


def backup_existing(path: Path) -> Path | None:
    if not path.exists():
        return None
    backup = path.with_suffix(path.suffix + f".{_now_utc_compact()}.bak")
    shutil.copy2(path, backup)
    return backup


def write_mcp_json(path: Path, servers: dict[str, dict[str, Any]]) -> None:
    payload = {"mcpServers": servers}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def validate_roundtrip(path: Path) -> int:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("mcp.json root must be an object")
    servers = data.get("mcpServers", {})
    if not isinstance(servers, dict):
        raise ValueError("mcpServers must be an object")
    return len(servers)


def main(argv: list[str]) -> int:
    registry_path = Path(argv[1]) if len(argv) > 1 else REGISTRY_PATH
    launcher_map_path = Path(argv[2]) if len(argv) > 2 else LAUNCHER_MAP_PATH
    mcp_json_path = Path(argv[3]) if len(argv) > 3 else MCP_JSON_PATH

    ts = _now_utc_iso()
    print(f"[{ts}] [MCPGEN]  registry={registry_path}")
    print(f"[{ts}] [MCPGEN]  launcher_map={launcher_map_path}")
    print(f"[{ts}] [MCPGEN]  target={mcp_json_path}")

    registry = load_registry(registry_path)
    launcher_map = load_launcher_map(launcher_map_path)

    emitted, catalogued_es, enabled_not_sealed, enabled_no_launcher = collect_enabled_sealed(registry, launcher_map)

    servers = build_mcp_servers(emitted)

    backup = backup_existing(mcp_json_path)
    if backup:
        print(f"[{ts}] [MCPGEN]  backup={backup}")

    write_mcp_json(mcp_json_path, servers)

    n_servers = validate_roundtrip(mcp_json_path)

    # Indicators (subset of INIT format, scoped to this generator's job)
    print(f"[{ts}] [MCPGEN]  catalogued_enabled_sealed={len(catalogued_es)}")
    print(f"[{ts}] [MCPGEN]  emitted={n_servers}")
    print(f"[{ts}] [MCPGEN]  enabled_not_sealed={len(enabled_not_sealed)} ({','.join(enabled_not_sealed) or 'none'})")
    print(
        f"[{ts}] [MCPGEN]  enabled_no_launcher={len(enabled_no_launcher)} ({','.join(enabled_no_launcher) or 'none'})"
    )
    print(f"[{ts}] [MCPGEN]  emitted_names={','.join(sorted(servers.keys())) or '(none)'}")
    print(f"[{ts}] [MCPGEN]  verdict=REGENERATED")

    # Persist a structured receipt
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{_now_utc_compact()}__mcp_gen.json"
    receipt = {
        "ts": ts,
        "registry_path": str(registry_path),
        "launcher_map_path": str(launcher_map_path),
        "mcp_json_path": str(mcp_json_path),
        "mcp_json_backup": str(backup) if backup else None,
        "catalogued_enabled_sealed": catalogued_es,
        "emitted": [name for name, *_ in emitted],
        "emitted_count": n_servers,
        "enabled_not_sealed": enabled_not_sealed,
        "enabled_no_launcher": enabled_no_launcher,
        "verdict": "REGENERATED",
    }
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
    print(f"[{ts}] [MCPGEN]  receipt={receipt_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
