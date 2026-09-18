#!/usr/bin/env python3
"""
reality_binding_probe.py — Binding Ratio measurement

Measures: declared authority (Layer 3) vs effective OS physics (Layer 0-1)

Usage:
    python3 reality_binding_probe.py [--json] [--organ frame|geox|all]

Output:
    Binding Ratio = bound authorities / declared authorities
    Per-organ: declared_authority vs effective_uid, file_perms, etc.
    Vault protection: directory + ledger file permissions

This is the probe that makes Binding Ratio observable.
When wired into FRAME Chamber 7, it becomes a drift signal.

Doc: /root/AAA/canon/REALITY_BINDING_ARCHITECTURE.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ── Declared authorities (Layer 3: governance contracts) ─────────────────

# From /root/AAA/federation/organs.yaml — single source of truth for declared authority
DECLARED_AUTHORITIES = {
    "arifos":    {"authority": "JUDGE_ONLY",          "port": 8088,  "expected_user": "arifos"},
    "a-forge":   {"authority": "EXECUTE_AFTER_SEAL",  "port": 7071,  "expected_user": "forge"},
    "geox":      {"authority": "COMPUTE_ONLY",        "port": 8081,  "expected_user": "geox"},
    "wealth":    {"authority": "EVIDENCE_ONLY",       "port": 18082, "expected_user": "wealth"},
    "well":      {"authority": "REFLECT_ONLY",        "port": 18083, "expected_user": "well"},
    "frame":     {"authority": "OBSERVE_ONLY",        "port": 18085, "expected_user": "frame"},
    "arifflow":  {"authority": "METABOLISM_ONLY",     "port": 7073,  "expected_user": "arifflow"},
    "hermes":    {"authority": "RELAY_ONLY",          "port": 18087, "expected_user": "hermes"},
    "aaa":       {"authority": "COCKPIT_ONLY",        "port": 3001,  "expected_user": "ariffazil"},
    "vault999":  {"authority": "WITNESS_ONLY",        "port": None,  "expected_user": "ariffazil"},
}

# Map organ_id → systemd service unit(s)
SERVICE_MAP = {
    "arifos":    ["arifos.service"],
    "a-forge":   ["a-forge.service", "a-forge-mcp.service"],
    "geox":      ["geox-mcp.service"],
    "wealth":    ["wealth-organ.service"],
    "well":      ["well-organ.service"],
    "frame":     ["frame-mcp.service", "frame-organ.service"],
    "arifflow":  ["arifflow.service"],
    "hermes":    ["hermes-mcp.service"],
    "aaa":       ["aaa-preforge.service", "aaa-a2a.service"],
}

# Vault paths to check
VAULT_PATHS = [
    Path("/root/arifOS/VAULT999"),
    Path("/root/VAULT999"),
]


# ── Probe functions ───────────────────────────────────────────────────────

def get_service_user(unit: str) -> Optional[str]:
    """Read User= directive from systemd unit (Layer 1)."""
    try:
        result = subprocess.run(
            ["systemctl", "show", unit, "--property=User", "--value"],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def get_process_uid(process_name: str) -> Optional[int]:
    """Get effective UID of running process (Layer 0)."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", process_name],
            capture_output=True, text=True, timeout=5,
        )
        pids = result.stdout.strip().split("\n")
        if not pids or not pids[0]:
            return None
        pid = pids[0]
        # Read /proc/PID/status for Uid
        status_path = Path(f"/proc/{pid}/status")
        if not status_path.exists():
            return None
        content = status_path.read_text()
        for line in content.split("\n"):
            if line.startswith("Uid:"):
                # Uid: real effective saved fs
                parts = line.split()
                if len(parts) >= 3:
                    return int(parts[2])  # effective UID
    except Exception:
        pass
    return None


def check_path_owner(path: Path) -> dict:
    """Check ownership + permissions on a path (Layer 0 physics)."""
    result = {
        "path": str(path),
        "exists": path.exists(),
        "owner": None,
        "group": None,
        "perm": None,
        "world_readable": False,
        "world_writable": False,
        "immutable": None,
    }
    if not path.exists():
        return result
    try:
        st = path.stat()
        import grp
        import pwd
        result["owner"] = pwd.getpwuid(st.st_uid).pw_name
        result["group"] = grp.getgrgid(st.st_gid).gr_name
        result["perm"] = oct(st.st_mode)[-3:]
        result["world_readable"] = bool(st.st_mode & 0o004)
        result["world_writable"] = bool(st.st_mode & 0o002)
    except Exception as e:
        result["error"] = str(e)
    # Check immutable flags
    try:
        out = subprocess.run(
            ["lsattr", "-d", str(path)],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            flags = out.stdout.split()[0] if out.stdout.split() else ""
            result["immutable"] = "i" in flags or "a" in flags
    except Exception:
        pass
    return result


def probe_organ(organ_id: str) -> dict:
    """Probe one organ: declared authority vs effective physics.
    Binding measured on two dimensions:
      1. UID binding: does the service run as expected user?
      2. Sandbox binding: are kernel-level powers restricted?
    """
    declared = DECLARED_AUTHORITIES.get(organ_id, {})
    expected_user = declared.get("expected_user")
    services = SERVICE_MAP.get(organ_id, [])

    # Find any active process for this organ using more precise matching
    actual_uids = []
    import pwd
    for svc in services:
        # Use service name (with .service stripped) as pgrep pattern
        proc_name = svc.replace(".service", "")
        try:
            result = subprocess.run(
                ["pgrep", "-x", proc_name],
                capture_output=True, text=True, timeout=5,
            )
            pids = [p for p in result.stdout.strip().split("\n") if p]
            for pid in pids:
                status_path = Path(f"/proc/{pid}/status")
                if status_path.exists():
                    content = status_path.read_text()
                    for line in content.split("\n"):
                        if line.startswith("Uid:"):
                            parts = line.split()
                            if len(parts) >= 3:
                                euid = int(parts[2])
                                try:
                                    user = pwd.getpwuid(euid).pw_name
                                except KeyError:
                                    user = f"uid{euid}"
                                actual_uids.append({"service": svc, "pid": int(pid), "uid": euid, "user": user})
                                break
        except Exception:
            pass
        # Also try systemd unit User= as fallback evidence
        svc_user = get_service_user(svc)
        if svc_user:
            try:
                uid = pwd.getpwnam(svc_user).pw_uid
                actual_uids.append({"service": svc, "pid": None, "uid": uid, "user": svc_user, "source": "systemd-unit"})
            except KeyError:
                pass

    # Determine UID binding
    uid_bound = False
    expected_uid = None
    if expected_user:
        try:
            expected_uid = pwd.getpwnam(expected_user).pw_uid
        except KeyError:
            pass
        for entry in actual_uids:
            if entry["user"] == expected_user:
                uid_bound = True
                break

    # Determine sandbox binding — read systemd sandboxing primitives
    sandbox = {"services": {}}
    for svc in services:
        svc_sandbox = _read_sandbox(svc)
        if svc_sandbox:
            sandbox["services"][svc] = svc_sandbox
    sandbox["score"] = _compute_sandbox_score(sandbox["services"])

    # Composite status: BOUND if either uid_bound OR sandbox.score >= threshold
    if not actual_uids and not sandbox["services"]:
        bound_status = "NOT_RUNNING"
    elif uid_bound or sandbox["score"] >= 0.5:
        bound_status = "BOUND"
    else:
        bound_status = "UNBOUND"

    binding_dimensions = []
    if uid_bound:
        binding_dimensions.append("uid")
    if sandbox["score"] >= 0.5:
        binding_dimensions.append("sandbox")
    if not binding_dimensions:
        binding_dimensions.append("none")

    return {
        "organ": organ_id,
        "declared_authority": declared.get("authority"),
        "expected_user": expected_user,
        "expected_uid": expected_uid,
        "services": services,
        "running_processes": actual_uids,
        "uid_bound": uid_bound,
        "sandbox": sandbox,
        "bound": bound_status == "BOUND",
        "status": bound_status,
        "binding_dimensions": binding_dimensions,
        "binding_gap": (
            None if bound_status == "BOUND"
            else f"uid={'✅' if uid_bound else '❌'} sandbox={sandbox['score']:.0%}"
        ),
    }


# ── Sandbox probe ─────────────────────────────────────────────────────────

SANDBOX_PRIMITIVES = [
    "NoNewPrivileges",
    "ProtectSystem",
    "ProtectHome",
    "PrivateTmp",
    "PrivateDevices",
    "ProtectKernelTunables",
    "ProtectKernelModules",
    "ProtectControlGroups",
    "RestrictNamespaces",
    "RestrictRealtime",
    "RestrictSUIDSGID",
    "LockPersonality",
    "MemoryDenyWriteExecute",
]


def _read_sandbox(unit: str) -> dict:
    """Read sandboxing primitives from a systemd unit."""
    result = {}
    for prop in SANDBOX_PRIMITIVES:
        try:
            val = subprocess.run(
                ["systemctl", "show", unit, f"--property={prop}", "--value"],
                capture_output=True, text=True, timeout=5,
            ).stdout.strip()
            # Convert systemd yes/no/empty to bool
            if val.lower() in ("yes", "true", "1"):
                result[prop] = True
            elif val.lower() in ("no", "false", "0", ""):
                result[prop] = False
            else:
                result[prop] = val  # e.g. "strict", "full"
        except Exception:
            result[prop] = None
    # Also read capability bounding set
    try:
        cap = subprocess.run(
            ["systemctl", "show", unit, "--property=CapabilityBoundingSet", "--value"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        result["CapabilityBoundingSet"] = cap if cap else None
    except Exception:
        result["CapabilityBoundingSet"] = None
    return result


def _compute_sandbox_score(service_sandbox: dict) -> float:
    """Compute 0.0–1.0 sandbox binding score across all services."""
    if not service_sandbox:
        return 0.0
    scores = []
    for svc, props in service_sandbox.items():
        active = sum(1 for k in SANDBOX_PRIMITIVES if props.get(k) is True or props.get(k) in ("strict", "full"))
        score = active / len(SANDBOX_PRIMITIVES)
        scores.append(score)
    return sum(scores) / len(scores) if scores else 0.0


def compute_binding_ratio(organ_results: list[dict]) -> dict:
    """Compute aggregate Binding Ratio.
    Two dimensions:
      uid_ratio:    how many organs have UID binding
      sandbox_ratio: how many organs have sandbox binding (>=50%)
    """
    total = len(organ_results)
    uid_bound = sum(1 for o in organ_results if o["status"] == "BOUND" and "uid" in o.get("binding_dimensions", []))
    sandbox_bound = sum(1 for o in organ_results if o["status"] == "BOUND" and "sandbox" in o.get("binding_dimensions", []))
    not_running = sum(1 for o in organ_results if o["status"] == "NOT_RUNNING")
    bound = sum(1 for o in organ_results if o["status"] == "BOUND")

    return {
        "total_declared": total,
        "total_bound": bound,
        "uid_bound": uid_bound,
        "sandbox_bound": sandbox_bound,
        "total_not_running": not_running,
        "total_unbound": total - bound - not_running,
        "uid_ratio": f"{uid_bound}/{total}",
        "sandbox_ratio": f"{sandbox_bound}/{total}",
        "ratio": round(bound / total, 3) if total else 0.0,
        "ratio_pct": f"{round(bound/total*100)}%" if total else "N/A",
    }


def probe_vault() -> dict:
    """Probe VAULT999 directory + ledger file permissions."""
    result = {
        "directories": [],
        "ledger_files": [],
        "overall_risk": "LOW",
    }
    risk_score = 0

    for vault_path in VAULT_PATHS:
        if not vault_path.exists():
            continue
        dir_info = check_path_owner(vault_path)
        result["directories"].append(dir_info)
        if dir_info["world_writable"]:
            risk_score += 3
        elif dir_info["world_readable"]:
            risk_score += 1

        # Check jsonl ledger files
        for jsonl in vault_path.rglob("*.jsonl"):
            file_info = check_path_owner(jsonl)
            file_info["risk"] = (
                "HIGH" if file_info["world_readable"] else
                "MEDIUM" if file_info["perm"] in ("644", "664") else "LOW"
            )
            result["ledger_files"].append(file_info)
            if file_info["world_readable"]:
                risk_score += 2
            elif file_info["perm"] in ("644", "664"):
                risk_score += 1

    if risk_score >= 10:
        result["overall_risk"] = "HIGH"
    elif risk_score >= 5:
        result["overall_risk"] = "MEDIUM"
    elif risk_score >= 1:
        result["overall_risk"] = "LOW"

    return result


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Measure Binding Ratio across the federation")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--organ", default="all", help="Organ to probe (default: all)")
    args = parser.parse_args()

    if args.organ == "all":
        organs = list(DECLARED_AUTHORITIES.keys())
    else:
        organs = [args.organ]

    organ_results = [probe_organ(o) for o in organs]
    vault_result = probe_vault()
    binding = compute_binding_ratio(organ_results)

    output = {
        "binding_ratio": binding,
        "per_organ": organ_results,
        "vault_protection": vault_result,
        "overall_verdict": (
            "FULLY_BOUND" if binding["ratio"] == 1.0 else
            "MOSTLY_BOUND" if binding["ratio"] >= 0.8 else
            "PARTIALLY_BOUND" if binding["ratio"] >= 0.5 else
            "PHYSICS_GAP"
        ),
        "doc": "/root/AAA/canon/REALITY_BINDING_ARCHITECTURE.md",
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("=" * 60)
        n = binding
        print(f"  BINDING RATIO: {n['ratio_pct']} ({n['total_bound']}/{n['total_declared']})")
        print(f"    UID binding:    {n['uid_ratio']}")
        print(f"    Sandbox binding: {n['sandbox_ratio']}")
        print(f"  VERDICT: {output['overall_verdict']}")
        print("=" * 60)
        print()
        print("PER-ORGAN BINDING:")
        print(f"  {'organ':<12} {'declared':<22} {'uid':<6} {'sandbox':<8} {'status':<10}")
        print(f"  {'-'*12} {'-'*22} {'-'*6} {'-'*8} {'-'*10}")
        for o in organ_results:
            uid = "✅" if "uid" in o.get("binding_dimensions", []) else ("—" if o["status"] == "NOT_RUNNING" else "❌")
            sandbox_pct = int(o["sandbox"]["score"] * 100) if o.get("sandbox", {}).get("services") else 0
            sandbox = f"{sandbox_pct}%" if o.get("sandbox", {}).get("services") else "—"
            icon = {"BOUND": "✅ BOUND", "UNBOUND": "❌ UNBOUND", "NOT_RUNNING": "⚠️  INACTIVE"}.get(o["status"], "?")
            print(f"  {o['organ']:<12} {o['declared_authority']:<22} {uid:<6} {sandbox:<8} {icon}")
            if o.get("binding_gap") and o["status"] != "BOUND":
                print(f"    └─ gap: {o['binding_gap']}")
        print()
        v = vault_result
        print("VAULT PROTECTION:")
        for d in v["directories"]:
            risk = "⚠️ " if d["world_writable"] else ("📖" if d["world_readable"] else "🔒")
            print(f"  {risk} {d['path']}: {d['perm']} {d['owner']}:{d['group']}")
        exposed = [f for f in v["ledger_files"] if f.get("world_readable")]
        append_only = sum(1 for f in v["ledger_files"] if f.get("immutable"))
        if exposed:
            tamper = f", {append_only} append-only" if append_only else ""
            print(f"  📖 {len(exposed)} ledger files readable for witnesses (644)")
            print(f"     {tamper}")
            for f in exposed[:3]:
                ao = "🔒" if f.get("immutable") else "  "
                print(f"      {ao} {f['path']}")
            if len(exposed) > 3:
                print(f"      ... and {len(exposed) - 3} more")
        print(f"  VAULT RISK: {v['overall_risk']}")
        print()


if __name__ == "__main__":
    main()
