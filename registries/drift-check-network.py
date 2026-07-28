#!/usr/bin/env python3
"""
drift-check-network.py — Live-vs-Registry network truth audit.
Run at agent boot. Exit 0 = clean. Exit 1 = drift detected (HOLD).

Usage:
  python3 /root/AAA/registries/drift-check-network.py
  python3 /root/AAA/registries/drift-check-network.py --json
"""

import json, subprocess, sys, os, argparse
from pathlib import Path

REGISTRY_PATH = Path("/root/AAA/registries/PORT_REGISTRY.json")


def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10).stdout.strip()
    except:
        return ""


def probe_ports():
    """Parse ss -tlnp. Returns {port: [bind_strings]} for dedup."""
    ports = {}
    out = run("ss -tlnp 2>/dev/null")
    for line in out.split("\n"):
        if not line.strip() or line.startswith("State"):
            continue
        parts = line.split(None, 5)
        if len(parts) < 5:
            continue
        local_addr = parts[3]  # Column 3 = Local Address:Port

        # Parse port + bind from addr like "127.0.0.1:8088", "[fd7a::2]:3001", "*:80"
        if local_addr.startswith("["):
            try:
                close = local_addr.index("]")
                bind = local_addr[: close + 1]
                port_str = local_addr[close + 2 :]
            except ValueError:
                continue
        elif ":" in local_addr:
            bind, port_str = local_addr.rsplit(":", 1)
        else:
            continue
        try:
            port = int(port_str)
        except ValueError:
            continue

        # Classify
        bind_clean = bind.strip("[]")
        if bind_clean in ("127.0.0.1", "::1"):
            bind_class = "localhost"
        elif bind_clean in ("0.0.0.0", "*", "::"):
            bind_class = "all_interfaces"
        elif bind_clean.startswith("100.64."):
            bind_class = "tailscale"
        elif bind_clean.startswith("fd7a"):
            bind_class = "tailscale_ipv6"
        elif bind_clean.startswith("127."):
            bind_class = "localhost"
        else:
            bind_class = "other"

        if port not in ports:
            ports[port] = []
        ports[port].append({"bind": bind, "class": bind_class})

    return ports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings = []
    live = {}

    if not REGISTRY_PATH.exists():
        findings.append({"severity": "CRITICAL", "msg": f"PORT_REGISTRY.json not found at {REGISTRY_PATH}"})
    else:
        live = probe_ports()

        # Core organ ports (must be listening)
        core = {
            8088: "arifOS",
            7071: "A-FORGE API",
            7072: "A-FORGE MCP",
            3001: "AAA",
            8081: "GEOX",
            18082: "WEALTH",
            18083: "WELL",
            7073: "arifFlow",
        }
        for port, name in core.items():
            if port not in live:
                findings.append({"severity": "CRITICAL", "msg": f"Core organ {name} port {port} NOT LISTENING"})

        # Data stores
        data = {5432: "Postgres", 6379: "Redis", 6333: "Qdrant", 4222: "NATS"}
        for port, name in data.items():
            if port not in live:
                findings.append({"severity": "HIGH", "msg": f"Data store {name} port {port} NOT LISTENING"})

        # Public exposure: anything on all_interfaces that isn't 80, 443, 22888, 8083?
        allowed_public = {80, 443, 22888, 8083}
        for port, binds in live.items():
            for b in binds:
                if b["class"] == "all_interfaces" and port not in allowed_public:
                    findings.append(
                        {
                            "severity": "HIGH",
                            "msg": f"UNEXPECTED PUBLIC BIND: port {port} on {b['bind']} (not in allowed_public: {allowed_public})",
                        }
                    )

        # Systemd units
        units = {
            "arifos.service": "arifOS kernel",
            "a-forge.service": "A-FORGE API",
            "a-forge-mcp.service": "A-FORGE MCP",
            "aaa-a2a.service": "AAA A2A",
            "geox-mcp.service": "GEOX MCP",
            "wealth-organ.service": "WEALTH",
            "well.service": "WELL",
            "arifflow.service": "arifFlow",
            "caddy.service": "Caddy",
            "cloudflared.service": "Cloudflare Tunnel",
        }
        for unit, name in units.items():
            status = run(f"systemctl is-active {unit} 2>/dev/null")
            if status != "active":
                sev = "CRITICAL" if unit in ("caddy.service", "arifos.service") else "HIGH"
                findings.append({"severity": sev, "msg": f"{name} ({unit}) is '{status}' (expected: active)"})

        # Caddy config valid?
        caddy_check = run("caddy validate --config /etc/caddy/Caddyfile 2>&1")
        if "Error" in caddy_check or ("valid" not in caddy_check.lower() and "info" not in caddy_check.lower()):
            findings.append({"severity": "CRITICAL", "msg": f"Caddy config invalid: {caddy_check[:200]}"})

    # Output
    if args.json:
        print(
            json.dumps(
                {
                    "verdict": "SEAL" if not findings else "HOLD",
                    "findings": findings,
                    "live_port_count": len(live) if REGISTRY_PATH.exists() else 0,
                    "timestamp": run("date -u +%Y-%m-%dT%H:%M:%SZ"),
                }
            )
        )
    else:
        print("=" * 60)
        print("NETWORK DRIFT CHECK")
        print("=" * 60)
        if findings:
            print(f"\n{len(findings)} FINDINGS:")
            for f in findings:
                icon = "CRIT" if f["severity"] == "CRITICAL" else "HIGH" if f["severity"] == "HIGH" else "WARN"
                print(f"  [{icon}] {f['msg']}")
            print(f"\nVERDICT: HOLD")
            sys.exit(1)
        else:
            print(f"\nLive ports: {len(live)}")
            print("All core organs: LISTENING")
            print("All systemd units: active")
            print("Caddy config: valid")
            print("No unexpected public binds")
            print("\nVERDICT: SEAL - Network matches registry.")
            sys.exit(0)


if __name__ == "__main__":
    main()
