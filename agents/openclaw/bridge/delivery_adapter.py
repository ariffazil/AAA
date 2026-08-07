#!/usr/bin/env python3
"""
OpenClaw Delivery Adapter
-------------------------

Channels:    Telegram (MarkdownV2), A2A JSON, Local file (forge_work/sessions),
             CLI stdout.

Inputs:      A2A gateway response payload (JSON-RPC 2.0 result) OR a
             pre-routed delivery request from the bridge.

Conventions: Telegram — 4096 char limit, MarkdownV2 safe, respect
             "DITEMPA BUKAN DIBERI" footer & epistemic tags. A2A JSON —
             passthrough with delivery envelope. Local file — append to
             /root/forge_work/sessions/<session_id>.jsonl.

Dependency:  Optional import of httpx for A2A delivery delegate.

Forged: 2026-08-07  ·  Part of OpenClaw AA completion
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# ──────────────────────────── paths ────────────────────────────

SESSIONS_DIR = Path(
    os.environ.get(
        "OPENCLAW_SESSIONS_DIR",
        "/root/forge_work/sessions",
    )
)
RECEIPTS_FILE = Path(
    os.environ.get(
        "OPENCLAW_RECEIPTS_FILE",
        "/root/forge_work/session-receipts.jsonl",
    )
)
AGENT_NAME = "OpenClaw"
DOSSIER_FOOTER = "\n\nDITEMPA BUKAN DIBERI ⚒️"

# Telegram limits
TG_MAX = 4096

# ──────────────────────────── formatters ────────────────────────────

def _esc(text: str) -> str:
    """Escape MarkdownV2 special chars (subset)."""
    if not text:
        return ""
    out = str(text)
    # Escape backslash first
    out = out.replace("\\", "\\\\")
    for ch in r"_*[]()~`>#+-=|{}.!":
        out = out.replace(ch, f"\\{ch}")
    return out


def _soft_split(text: str, max_len: int) -> list[str]:
    """Split text at paragraph boundaries, never mid-word."""
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    cur = ""
    for para in text.split("\n\n"):
        if len(cur) + len(para) + 2 > max_len:
            if cur:
                chunks.append(cur)
                cur = ""
            # Single para too long → split on lines
            if len(para) > max_len:
                for line in para.split("\n"):
                    # Hard-split a single line longer than max_len (never mid-word when avoidable)
                    while len(line) > max_len:
                        cut = line.rfind(" ", 0, max_len)
                        if cut < max_len // 2:  # no usable word boundary → hard cut
                            cut = max_len
                        head, line = line[:cut], line[cut:].lstrip()
                        if cur:
                            chunks.append(cur)
                            cur = ""
                        chunks.append(head)
                    if len(cur) + len(line) + 1 > max_len:
                        if cur:
                            chunks.append(cur)
                        cur = line
                    else:
                        cur = (cur + "\n" + line) if cur else line
            else:
                cur = para
        else:
            cur = (cur + "\n\n" + para) if cur else para
    if cur:
        chunks.append(cur)
    return chunks


def format_telegram(payload: dict) -> list[str]:
    """Render A2A response payload as Telegram MarkdownV2 chunks.

    Strategy: light Markdown→MD2 escape, epilogue footer, soft-split at 4096.
    """
    # Unpack common shapes
    if "result" in payload:
        result = payload["result"]
    else:
        result = payload

    body = result.get("artifacts", [{}])[0].get("text", "") if result.get("artifacts") else ""
    if not body:
        history = result.get("history", [])
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                parts = msg.get("parts") or msg.get("content", [])
                if isinstance(parts, list):
                    body = " ".join(
                        p.get("text", "") for p in parts if p.get("kind") in ("text", "text/plain")
                    )
                else:
                    body = str(parts)
                break
    if not body:
        body = "_(no payload returned)_"

    # Strip trailing whitespace, attach footer
    body = body.rstrip() + DOSSIER_FOOTER

    # Build header with rule + organ (read from metadata if present)
    meta = (result.get("metadata") or {}).get("routing")
    if meta:
        if isinstance(meta, dict):
            header = (
                f"*Rule:* `{_esc(meta.get('rule_id', '?'))}`  "
                f"*→*  `{_esc(meta.get('organ', meta.get('tool', '?')))}`  "
                f"*•*  `{_esc(meta.get('intent_class', '?'))}`\n\n"
            )
        else:
            rule_id = result.get("id", "?")
            header = (
                f"*Agent:* `{_esc(str(meta))}`  "
                f"*•*  `task={_esc(str(rule_id))}`\n\n"
            )
    else:
        header = ""

    full = header + body
    return _soft_split(full, TG_MAX)


def format_a2a(payload: dict) -> dict:
    """Pass-through with delivery envelope (A2A JSON)."""
    return {
        "delivery": {
            "kind": "a2a_json",
            "agent": AGENT_NAME,
            "ts": int(time.time() * 1000),
            "delivery_id": f"oc-del-{uuid.uuid4().hex[:12]}",
            "payload": payload,
        }
    }


def format_local(payload: dict, session_id: str) -> dict:
    """Write to local sessions JSONL with one entry per delivery."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": int(time.time() * 1000),
        "agent": AGENT_NAME,
        "session_id": session_id,
        "delivery_id": f"oc-del-{uuid.uuid4().hex[:12]}",
        "payload": payload,
    }
    fp = SESSIONS_DIR / f"{session_id}.jsonl"
    with fp.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"delivery": {"kind": "local_file", "path": str(fp), "session_id": session_id}}


def format_stdout(payload: dict) -> str:
    """Plain JSON to stdout (for piping)."""
    return json.dumps(payload, indent=2, ensure_ascii=False)


# ──────────────────────────── dispatcher ────────────────────────────

def deliver(
    payload: dict,
    *,
    channel: str = "telegram",
    session_id: Optional[str] = None,
    chat_id: Optional[str] = None,
    extra_meta: Optional[dict] = None,
) -> dict:
    """Dispatch payload to one channel. Returns a delivery report."""
    if channel == "telegram":
        chunks = format_telegram(payload)
        # Emit receipt only — actual Telegram send is via hermes-telegram/etc.
        # The bridge caller is responsible for handing chunks to outbound.
        report = {
            "channel": "telegram",
            "chunks": chunks,
            "chunk_count": len(chunks),
            "chunk_lengths": [len(c) for c in chunks],
            "total_length": sum(len(c) for c in chunks),
            "session_id": session_id,
            "chat_id": chat_id,
            "ts": int(time.time() * 1000),
        }
    elif channel == "a2a":
        report = format_a2a(payload)
    elif channel == "local":
        sid = session_id or f"oc-{uuid.uuid4().hex[:12]}"
        report = format_local(payload, sid)
    elif channel in ("stdout", "json"):
        out = format_stdout(payload)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
        report = {"channel": "stdout", "bytes": len(out)}
    else:
        raise ValueError(f"unknown channel: {channel}")

    if extra_meta:
        report["meta"] = extra_meta

    # Append to session-receipts
    write_receipt({**report, "channel": channel})
    return report


def write_receipt(entry: dict) -> None:
    """Append a delivery receipt (reversible audit trail)."""
    try:
        RECEIPTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with RECEIPTS_FILE.open("a") as f:
            f.write(json.dumps(
                {**entry, "ts": int(time.time() * 1000), "agent": AGENT_NAME},
                ensure_ascii=False,
            ) + "\n")
    except Exception as e:
        # Receipts are best-effort — never fail delivery on receipt failure
        print(f"[warn] receipt write failed: {e}", file=sys.stderr)


# ──────────────────────────── CLI ────────────────────────────

def _read_payload(arg: str) -> str:
    if arg == "-":
        return sys.stdin.read()
    if os.path.exists(arg):
        return Path(arg).read_text()
    return arg


def main():
    p = argparse.ArgumentParser(description="OpenClaw delivery adapter")
    p.add_argument("payload", help="payload text, @file, or - for stdin")
    p.add_argument(
        "--channel",
        choices=["telegram", "a2a", "local", "stdout"],
        default="stdout",
    )
    p.add_argument("--session-id", help="session id (default: auto)")
    p.add_argument("--chat-id", help="telegram chat_id")
    p.add_argument("--meta", help="extra metadata JSON string")
    args = p.parse_args()

    raw = _read_payload(args.payload)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {"artifacts": [{"text": raw}], "metadata": {}}

    extra = json.loads(args.meta) if args.meta else None
    report = deliver(
        payload,
        channel=args.channel,
        session_id=args.session_id,
        chat_id=args.chat_id,
        extra_meta=extra,
    )
    if args.channel != "stdout":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
