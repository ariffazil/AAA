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
import json
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


REGISTRY_PATH = Path("/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml")
LAUNCHER_MAP_PATH = Path("/root/AAA/federation/launcher_map.yaml")
MCP_JSON_PATH = Path("/root/.kimi-code/mcp.json")
RECEIPT_DIR = Path("/root/AAA/federation/init_receipts")


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
                    emitted.append((backend_name, launcher))
                elif enabled and seal != "sealed":
                    enabled_not_sealed.append(backend_name)

    return emitted, catalogued_enabled_sealed, enabled_not_sealed, enabled_no_launcher


def build_mcp_servers(
    emitted: list[tuple[str, dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    """
    Translate (backend_name, launcher_entry) pairs into a Kimi
    mcpServers dict. Only stdio and http transports are valid for Kimi;
    filesystem (e.g. VAULT999) is not an MCP and is skipped here.
    """
    servers: dict[str, dict[str, Any]] = {}
    for backend_name, launcher in emitted:
        transport = launcher.get("transport")
        if transport not in ("stdio", "http"):
            # filesystem or other — Kimi does not spawn these
            continue
        entry: dict[str, Any] = {"description": launcher.get("description", "")}
        if transport == "stdio":
            command = launcher.get("command")
            if not command:
                raise ValueError(
                    f"Launcher for '{backend_name}' is stdio but has no command"
                )
            entry["command"] = command
            args = launcher.get("args") or []
            if args:
                entry["args"] = list(args)
            env = launcher.get("env") or {}
            if env:
                entry["env"] = dict(env)
        else:  # http
            url = launcher.get("url")
            if not url:
                raise ValueError(
                    f"Launcher for '{backend_name}' is http but has no url"
                )
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

    emitted, catalogued_es, enabled_not_sealed, enabled_no_launcher = collect_enabled_sealed(
        registry, launcher_map
    )

    servers = build_mcp_servers(emitted)

    backup = backup_existing(mcp_json_path)
    if backup:
        print(f"[{ts}] [MCPGEN]  backup={backup}")

    write_mcp_json(mcp_json_path, servers)

    n_servers = validate_roundtrip(mcp_json_path)

    # Indicators (subset of INIT format, scoped to this generator's job)
    print(f"[{ts}] [MCPGEN]  catalogued_enabled_sealed={len(catalogued_es)}")
    print(f"[{ts}] [MCPGEN]  emitted={n_servers}")
    print(f"[{ts}] [MCPGEN]  enabled_not_sealed={len(enabled_not_sealed)} "
          f"({','.join(enabled_not_sealed) or 'none'})")
    print(f"[{ts}] [MCPGEN]  enabled_no_launcher={len(enabled_no_launcher)} "
          f"({','.join(enabled_no_launcher) or 'none'})")
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
        "emitted": [name for name, _ in emitted],
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
