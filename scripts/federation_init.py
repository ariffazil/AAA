"""
federation_init.py — Unified Federation Init Contract v1.0.0
arifOS federation | DITEMPA BUKAN DIBERI

Implements the 5-stage init pattern from /root/AAA/docs/INIT_CONTRACT.md:
  1. mcp_initialize    — MCP 2025-11-25 initialize handshake
  2. bearer_attach     — attach shared agentmesh.token (F1 AMANAH)
  3. a2a_card_fetch    — fetch A2A v1.0.1 Agent Card from /.well-known/agent.json
  4. constitutional_bind — arif_init() for arifOS/A-FORGE; stage-only for L1
  5. dedupe_check      — TOOLREGISTRY overlap check (F4 CLARITY)

Usage:
  python3 /root/AAA/federation_init.py --actor forge --organ all
  python3 /root/AAA/federation_init.py --actor arif --organ arifos
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

BEARER_PATH = "/root/.secrets/aaa-identity/agentmesh.token"
MCP_PROTOCOL = "2025-11-25"
A2A_VERSION = "1.0.1"
INIT_TIMEOUT = 5.0
TOOLREGISTRY_PATH = "/root/AAA/docs/TOOLREGISTRY.json"
WELLKNOWN_PATH = "/root/AAA/public/.well-known/agent.json"
GATEWAY_PORT = 3001


class Stage(str, Enum):
    MCP_INIT = "mcp_initialize"
    BEARER = "bearer_attach"
    A2A = "a2a_card_fetch"
    CONST = "constitutional_bind"
    DEDUPE = "dedupe_check"


@dataclass
class Organ:
    name: str
    port: int
    constitutional: bool
    skills: List[str]
    notes: str = ""


ORGANS: Dict[str, Organ] = {
    "arifos": Organ(
        "arifos",
        8088,
        True,
        ["arifos-arconstitutional-audit", "arifos-mcp-federation"],
        "Sovereign kernel. F1-F13 judgment. Mints leases + seals.",
    ),
    "aforge": Organ(
        "aforge",
        7071,
        True,
        ["aforge-governed-execution"],
        "Execution shell. Delegates judgment to arifOS via forge_judge_proxy.",
    ),
    "aaa": Organ(
        "aaa",
        3001,
        False,
        ["aaa-state-cockpit", "a2a-federation-builder"],
        "Cockpit + A2A gateway. Displays state; does not judge.",
    ),
    "geox": Organ(
        "geox", 8081, False, ["geox-constitution", "geox-earth-evidence"], "L1 substrate (Earth). Evidence only."
    ),
    "wealth": Organ(
        "wealth", 18082, False, ["wealth-capital-reasoning"], "L1 substrate (Capital). Computes; arifOS judges."
    ),
    "well": Organ(
        "well", 18083, False, ["well-substrate-readiness"], "L1 substrate (Human readiness). Reflects; never decides."
    ),
}


@dataclass
class StageResult:
    stage: str
    success: bool
    elapsed_ms: float
    detail: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class InitReceipt:
    actor: str
    organ: str
    started_at: float
    finished_at: Optional[float] = None
    overall_success: bool = False
    bearer_attached: bool = False
    bearer_source: str = BEARER_PATH
    a2a_protocol: str = A2A_VERSION
    mcp_protocol: str = MCP_PROTOCOL
    stages: List[StageResult] = field(default_factory=list)

    def add(self, r: StageResult) -> None:
        self.stages.append(r)

    def finalize(self) -> None:
        self.finished_at = time.time()
        self.overall_success = all(s.success for s in self.stages) and bool(self.stages)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["duration_ms"] = (self.finished_at - self.started_at) * 1000 if self.finished_at is not None else 0.0
        return d


def _http_post(url: str, payload: Dict[str, Any], bearer: str = "", timeout: float = INIT_TIMEOUT) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode("utf-8"), method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _http_get(url: str, timeout: float = INIT_TIMEOUT) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def stage_mcp_init(organ: Organ, actor: str) -> StageResult:
    t0 = time.time()
    if organ.name == "aaa":
        return StageResult(
            Stage.MCP_INIT.value,
            True,
            0.0,
            {
                "server": "AAA Gateway",
                "note": "A2A gateway; not MCP-native",
            },
        )
    try:
        port = 7072 if organ.name == "aforge" else organ.port
        data = _http_post(
            f"http://localhost:{port}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": MCP_PROTOCOL,
                    "capabilities": {"tools": {}, "resources": {}, "prompts": {}, "elicitation": {}, "logging": {}},
                    "clientInfo": {"name": "federation_init", "version": "1.0.0"},
                    "actor": actor,
                },
            },
        )
        elapsed = (time.time() - t0) * 1000
        if "result" in data:
            info = data["result"].get("serverInfo", {})
            return StageResult(
                Stage.MCP_INIT.value,
                True,
                elapsed,
                {
                    "server": info.get("name"),
                    "version": info.get("version"),
                    "protocol": data["result"].get("protocolVersion"),
                },
            )
        return StageResult(Stage.MCP_INIT.value, False, elapsed, error=f"no result: {data}")
    except Exception as e:
        return StageResult(Stage.MCP_INIT.value, False, (time.time() - t0) * 1000, error=str(e))


def stage_bearer(path: str = BEARER_PATH) -> StageResult:
    t0 = time.time()
    try:
        p = Path(path)
        if not p.exists():
            return StageResult(Stage.BEARER.value, False, (time.time() - t0) * 1000, error=f"missing: {path}")
        token = p.read_text(encoding="utf-8").strip()
        ok = len(token) >= 16
        return StageResult(
            Stage.BEARER.value,
            ok,
            (time.time() - t0) * 1000,
            {
                "source": str(p),
                "token_len": len(token),
                "prefix": token[:8] + "..." if token else "",
            },
        )
    except Exception as e:
        return StageResult(Stage.BEARER.value, False, (time.time() - t0) * 1000, error=str(e))


def stage_a2a_card(organ: Organ) -> StageResult:
    t0 = time.time()
    urls = [
        f"http://localhost:{organ.port}/.well-known/agent.json",
        f"http://localhost:{organ.port}/a2a/agent-card.json",
        f"http://localhost:{GATEWAY_PORT}/.well-known/agent-card.json",
    ]
    last_err = None
    for url in urls:
        try:
            data = _http_get(url)
            elapsed = (time.time() - t0) * 1000
            return StageResult(
                Stage.A2A.value,
                True,
                elapsed,
                {
                    "url": url,
                    "name": data.get("name"),
                    "protocol": data.get("protocolVersion", data.get("protocol_version")),
                    "skills": len(data.get("skills", [])),
                },
            )
        except Exception as e:
            last_err = str(e)
            continue
    return StageResult(Stage.A2A.value, False, (time.time() - t0) * 1000, error=f"card not found: {last_err}")


def stage_constitutional_bind(organ: Organ, actor: str, bearer: str) -> StageResult:
    t0 = time.time()
    if not organ.constitutional:
        return StageResult(
            Stage.CONST.value,
            True,
            (time.time() - t0) * 1000,
            {
                "organ": organ.name,
                "delegated_to": "arifOS",
                "note": "L1 substrate; no sovereign bind",
            },
        )
    try:
        port = 7072 if organ.name == "aforge" else organ.port
        tool_name = "forge_session_init" if organ.name == "aforge" else "arif_init"
        args = {"actor_id": actor, "intent": "federation_init", "mode": "external"} if organ.name == "aforge" else {"actor_id": actor, "intent": "federation_init", "mode": "init"}
        data = _http_post(
            f"http://localhost:{port}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": args,
                },
            },
            bearer=bearer,
        )
        elapsed = (time.time() - t0) * 1000
        if "result" in data:
            r = data["result"]
            content = r.get("content", [{}])
            text = content[0].get("text", "{}") if isinstance(content, list) else "{}"
            try:
                parsed = json.loads(text)
            except Exception:
                parsed = {"raw": text[:200]}
            return StageResult(
                Stage.CONST.value,
                True,
                elapsed,
                {
                    "organ": organ.name,
                    "session_id": parsed.get("session_id"),
                    "authority": parsed.get("authority_level"),
                    "next_tool": parsed.get("next_tool"),
                },
            )
        return StageResult(Stage.CONST.value, False, elapsed, error=f"no result: {data}")
    except Exception as e:
        return StageResult(Stage.CONST.value, False, (time.time() - t0) * 1000, error=str(e))


def stage_dedupe(organ: Organ, registry_path: str = TOOLREGISTRY_PATH) -> StageResult:
    t0 = time.time()
    try:
        p = Path(registry_path)
        if not p.exists():
            return StageResult(
                Stage.DEDUPE.value,
                True,
                (time.time() - t0) * 1000,
                {
                    "status": "no_registry",
                    "note": "TOOLREGISTRY absent — dedupe deferred",
                },
            )
        reg = json.loads(p.read_text(encoding="utf-8"))
        skills = reg.get("skills", [])
        existing = {s.get("name") for s in skills if s.get("organ") == organ.name}
        manifest = set(organ.skills)
        overlap = existing & manifest
        new_skills = manifest - existing
        return StageResult(
            Stage.DEDUPE.value,
            True,
            (time.time() - t0) * 1000,
            {
                "organ": organ.name,
                "existing": len(existing),
                "manifest": len(manifest),
                "overlap": sorted(overlap),
                "new_candidates": sorted(new_skills),
            },
        )
    except Exception as e:
        return StageResult(Stage.DEDUPE.value, False, (time.time() - t0) * 1000, error=str(e))


def init_organ(organ_name: str, actor: str) -> InitReceipt:
    organ = ORGANS[organ_name]
    receipt = InitReceipt(actor=actor, organ=organ_name, started_at=time.time())

    # Stage 1: MCP initialize
    receipt.add(stage_mcp_init(organ, actor))

    # Stage 2: Bearer attach (shared)
    bearer_result = stage_bearer()
    receipt.add(bearer_result)
    receipt.bearer_attached = bearer_result.success
    bearer = Path(BEARER_PATH).read_text(encoding="utf-8").strip() if bearer_result.success else ""

    # Stage 3: A2A card fetch
    receipt.add(stage_a2a_card(organ))

    # Stage 4: Constitutional bind
    receipt.add(stage_constitutional_bind(organ, actor, bearer))

    # Stage 5: Dedupe check
    receipt.add(stage_dedupe(organ))

    receipt.finalize()
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Federation init contract v1.0.0")
    parser.add_argument("--actor", default="forge", help="Acting actor id")
    parser.add_argument("--organ", default="all", help="Organ to init: arifos|aforge|aaa|geox|wealth|well|all")
    args = parser.parse_args()

    targets = list(ORGANS.keys()) if args.organ == "all" else [args.organ]
    targets = [t for t in targets if t in ORGANS]
    if not targets:
        print(json.dumps({"error": f"unknown organ: {args.organ}", "available": list(ORGANS.keys())}, indent=2))
        return 2

    receipts: List[InitReceipt] = []
    for name in targets:
        r = init_organ(name, args.actor)
        receipts.append(r)
        finished = r.finished_at if r.finished_at is not None else time.time()
        ms = (finished - r.started_at) * 1000
        print(f"[{'OK' if r.overall_success else 'FAIL'}] {name:8s} ({ms:.0f} ms)")
        for s in r.stages:
            mark = "✓" if s.success else "✗"
            err = f"  err={s.error}" if s.error else ""
            print(f"  {mark} {s.stage:22s} {s.elapsed_ms:6.1f} ms{err}")

    summary = {
        "actor": args.actor,
        "protocols": {"mcp": MCP_PROTOCOL, "a2a": A2A_VERSION},
        "organs": [r.to_dict() for r in receipts],
        "all_success": all(r.overall_success for r in receipts),
    }
    print("\n" + json.dumps(summary, indent=2))
    return 0 if summary["all_success"] else 1


if __name__ == "__main__":
    sys.exit(main())
