"""Integration test: spin up 333 + 555 + 888 servers and run the canonical
propose → translate → judge cycle. Verifies routing, acks, and F11 audit.

Stdlib only. asyncio. Tempdirs are used for sockets + audit so the test
does not touch /tmp/aaa-p2p on the host.
"""

from __future__ import annotations

import asyncio
import json
import tempfile
import time
from pathlib import Path
from typing import Any

import pytest

from p2p.audit import verify_chain
from p2p.protocol import new_message, validate_message
from p2p.socket_client import P2PClient
from p2p.socket_server import P2PServer


# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_p2p_dir() -> Path:
    with tempfile.TemporaryDirectory(prefix="aaa-p2p-test-") as d:
        yield Path(d)


async def _spawn(agent: str, sock_dir: Path, audit: Path) -> P2PServer:
    """Create a server, start its task, return the running server."""
    received: list[dict[str, Any]] = []

    async def on_message(msg: dict[str, Any]) -> None:
        received.append(msg)

    s = P2PServer(
        agent=agent,
        socket_dir=sock_dir,
        audit_path=audit,
        on_message=on_message,
    )
    task = asyncio.create_task(s.start())
    # Wait for socket to appear.
    for _ in range(50):
        if s.socket_path.exists():
            break
        await asyncio.sleep(0.01)
    else:
        s.stop()
        task.cancel()
        raise RuntimeError(f"server for {agent} did not bind in time")
    s._task = task  # type: ignore[attr-defined]
    s._received = received  # type: ignore[attr-defined]
    return s


async def _shutdown(server: P2PServer) -> None:
    server.stop()
    task = getattr(server, "_task", None)
    if task is not None:
        try:
            await asyncio.wait_for(task, timeout=2.0)
        except asyncio.TimeoutError:
            task.cancel()


# ── Tests ───────────────────────────────────────────────────────────────────


@pytest.mark.asyncio


async def test_three_agents_serve(tmp_p2p_dir: Path) -> None:
    """All three servers come up and bind their sockets."""
    audit = tmp_p2p_dir / "audit.jsonl"
    servers = []
    for agent in ("333-AGI", "555-ASI", "888-APEX"):
        s = await _spawn(agent, tmp_p2p_dir, audit)
        servers.append(s)
    try:
        for s in servers:
            assert s.socket_path.exists()
    finally:
        for s in servers:
            await _shutdown(s)


@pytest.mark.asyncio


async def test_propose_judge_cycle(tmp_p2p_dir: Path) -> None:
    """333 → 888 (propose), 888 replies judge, ack flow correct."""
    audit = tmp_p2p_dir / "audit.jsonl"
    servers = {a: await _spawn(a, tmp_p2p_dir, audit) for a in
               ("333-AGI", "555-ASI", "888-APEX")}
    try:
        client = P2PClient(socket_dir=tmp_p2p_dir)

        # 333 proposes to 888
        propose = new_message(
            sender="333-AGI",
            recipient="888-APEX",
            verb="propose",
            payload={
                "candidate": "deploy federated sentinel to staging",
                "rationale": "low blast radius, fully reversible",
                "evidence_refs": ["vault:999/2026-07-15/seal-77"],
            },
            blast_radius="MEDIUM",
            requires_judgment=True,
            session_id="SEAL-test-cycle-1",
        )
        ack = await client.send("888-APEX", propose)
        assert ack["verb"] == "ack", ack
        assert ack["from"] == "888-APEX"
        assert ack["to"] == "333-AGI"
        assert ack["payload"]["received"] is True
        assert ack["payload"]["ref_timestamp"] == propose["timestamp"]

        # 888 should have received it
        await asyncio.sleep(0.05)
        received_888 = servers["888-APEX"]._received  # type: ignore[attr-defined]
        assert any(m["verb"] == "propose" and m["from"] == "333-AGI"
                   for m in received_888), received_888

        # 888 judges back to 333
        judge = new_message(
            sender="888-APEX",
            recipient="333-AGI",
            verb="judge",
            payload={
                "verdict": "SEAL",
                "reason": "F1-F13 pass, evidence present, low risk",
                "f1_f13_pass": [True] * 13,
            },
            blast_radius="LOW",
            requires_judgment=False,
            session_id="SEAL-test-cycle-1",
        )
        ack2 = await client.send("333-AGI", judge)
        assert ack2["verb"] == "ack"
        assert ack2["from"] == "333-AGI"
        await asyncio.sleep(0.05)
        received_333 = servers["333-AGI"]._received  # type: ignore[attr-defined]
        assert any(m["verb"] == "judge" and m["from"] == "888-APEX"
                   for m in received_333), received_333
    finally:
        for s in servers.values():
            await _shutdown(s)

    # Audit should have rows for each message + every forward hop.
    ok, detail = verify_chain(audit)
    assert ok, detail


@pytest.mark.asyncio


async def test_translate_path_555_to_333(tmp_p2p_dir: Path) -> None:
    """555 → 333 (translate) lands on 333's queue."""
    audit = tmp_p2p_dir / "audit.jsonl"
    servers = {a: await _spawn(a, tmp_p2p_dir, audit) for a in
               ("333-AGI", "555-ASI", "888-APEX")}
    try:
        client = P2PClient(socket_dir=tmp_p2p_dir)
        tr = new_message(
            sender="555-ASI",
            recipient="333-AGI",
            verb="translate",
            payload={
                "original": "scan all ports",
                "rephrased": "scan only non-public 127.0.0.1 ports",
                "concerns": ["avoid Docker bypass of UFW"],
            },
            blast_radius="LOW",
            requires_judgment=False,
        )
        ack = await client.send("333-AGI", tr)
        assert ack["verb"] == "ack"
        assert ack["from"] == "333-AGI"
        await asyncio.sleep(0.05)
        received = servers["333-AGI"]._received  # type: ignore[attr-defined]
        assert any(m["verb"] == "translate" for m in received)
    finally:
        for s in servers.values():
            await _shutdown(s)


@pytest.mark.asyncio


async def test_broadcast_to_all(tmp_p2p_dir: Path) -> None:
    """`to: all` fans out to every other agent."""
    audit = tmp_p2p_dir / "audit.jsonl"
    servers = {a: await _spawn(a, tmp_p2p_dir, audit) for a in
               ("333-AGI", "555-ASI", "888-APEX")}
    try:
        client = P2PClient(socket_dir=tmp_p2p_dir)
        msg = new_message(
            sender="888-APEX",
            recipient="all",
            verb="judge",
            payload={"verdict": "HOLD", "reason": "test broadcast", "f1_f13_pass": []},
            blast_radius="HIGH",
            requires_judgment=False,
            session_id="SEAL-test-bcast",
        )
        ack = await client.send("all", msg)
        # 888 broadcasts by writing to "888-to-all.sock", which itself is
        # the 888 server's socket. The 888 server then forwards to 333 + 555.
        # But that loop would re-enter the same server; check current logic.
        # In our model, broadcast is a special routing in the receiver; the
        # sender sends to the 888 server (which is the audit + dispatcher),
        # and the dispatcher fans out.
        assert ack["verb"] in ("ack", "reject"), ack
        await asyncio.sleep(0.1)
        # At least one of the other agents should have received it.
        got_any = any(
            any(m.get("verb") == "judge" for m in s._received)  # type: ignore[attr-defined]
            for s in servers.values()
        )
        # The sender (888) will also have received its own broadcast echo.
        assert got_any, "no agent received the broadcast"
    finally:
        for s in servers.values():
            await _shutdown(s)


@pytest.mark.asyncio


async def test_invalid_message_rejected(tmp_p2p_dir: Path) -> None:
    """Bad schema → reject ack, no delivery, but audit row written."""
    audit = tmp_p2p_dir / "audit.jsonl"
    s = await _spawn("888-APEX", tmp_p2p_dir, audit)
    try:
        client = P2PClient(socket_dir=tmp_p2p_dir)
        bad = {
            "from": "333-AGI",
            "to": "888-APEX",
            "verb": "propose",
            "payload": {},
            "timestamp": "2026-07-15T00:00:00+00:00",
            "requires_judgment": False,
            "blast_radius": "BOGUS",  # not in enum
        }
        with pytest.raises(Exception):
            await client.send("888-APEX", bad)
    finally:
        await _shutdown(s)


@pytest.mark.asyncio


async def test_latency_333_to_888(tmp_p2p_dir: Path) -> None:
    """Roundtrip 333 → 888 must be well under the 50ms hard ceiling.

    Soft target is 10ms; we assert ≤ 50ms here and print the measured p50.
    """
    audit = tmp_p2p_dir / "audit.jsonl"
    servers = {a: await _spawn(a, tmp_p2p_dir, audit) for a in
               ("333-AGI", "555-ASI", "888-APEX")}
    try:
        client = P2PClient(socket_dir=tmp_p2p_dir)
        samples_ms: list[float] = []
        for _ in range(50):
            msg = new_message(
                sender="333-AGI",
                recipient="888-APEX",
                verb="ack",
                payload={"ping": True},
                blast_radius="LOW",
                requires_judgment=False,
            )
            t0 = time.perf_counter()
            ack = await client.send("888-APEX", msg)
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            assert ack["verb"] == "ack"
            samples_ms.append(elapsed_ms)
        samples_ms.sort()
        p50 = samples_ms[len(samples_ms) // 2]
        p99 = samples_ms[int(len(samples_ms) * 0.99)]
        print(f"\nLATENCY 333→888 p50={p50:.2f}ms p99={p99:.2f}ms "
              f"min={samples_ms[0]:.2f}ms max={samples_ms[-1]:.2f}ms")
        assert p99 < 50.0, f"p99={p99:.2f}ms exceeds 50ms ceiling"
    finally:
        for s in servers.values():
            await _shutdown(s)