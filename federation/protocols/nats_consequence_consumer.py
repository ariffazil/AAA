#!/usr/bin/env python3
"""
nats_consequence_consumer.py — Cross-Organ Event Consumer for arifOS Consequence Bus.

Subscribes to NATS JetStream stream 'arifos-consequence' (subjects 'arifos.consequence.>').
Dispatches consequence events to subscribing organs (WELL, WEALTH, GEOX, KERNEL)
and records them in each organ's consequence_inbox.jsonl.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("consequence-consumer")

NATS_URL = os.getenv("NATS_URL", "nats://127.0.0.1:4222")
STREAM_NAME = "arifos-consequence"
CONSUMER_DURABLE = "federation-organ-consequence-v1"

ORGAN_INBOXES = {
    "WELL": Path("/var/lib/well/consequence_inbox.jsonl"),
    "WEALTH": Path("/var/lib/wealth/consequence_inbox.jsonl"),
    "AAA": Path("/root/AAA/ledger/consequence_inbox.jsonl"),
}

# Subscriptions routing table
# Pattern matching rule: subject prefixes routed to interested organs
ROUTING_TABLE = {
    "well": ["WELL", "AAA"],
    "aforge": ["WELL", "AAA"],
    "geox": ["WEALTH", "AAA"],
    "wealth": ["WEALTH", "AAA"],
    "kernel": ["WELL", "WEALTH", "AAA"],
    "hermes": ["AAA"],
}


def dispatch_event(subject: str, payload: dict[str, Any]) -> list[str]:
    """Route consequence event to relevant organ inboxes."""
    parts = subject.split(".")
    # subject format: arifos.consequence.<organ>.<event_type>
    source_organ = parts[2] if len(parts) > 2 else "unknown"
    recipients = ROUTING_TABLE.get(source_organ.lower(), ["AAA"])

    now_iso = datetime.now(timezone.utc).isoformat()
    record = {
        "received_at": now_iso,
        "subject": subject,
        "source_organ": source_organ,
        "payload": payload,
    }
    line = json.dumps(record, separators=(",", ":")) + "\n"

    delivered = []
    for organ in recipients:
        inbox = ORGAN_INBOXES.get(organ)
        if inbox:
            try:
                inbox.parent.mkdir(parents=True, exist_ok=True)
                with open(inbox, "a") as f:
                    f.write(line)
                delivered.append(organ)
            except Exception as e:
                logger.error("Failed to deliver to %s inbox (%s): %s", organ, inbox, e)

    return delivered


async def process_message(msg: Any) -> None:
    subject = msg.subject
    try:
        data = json.loads(msg.data.decode("utf-8"))
    except Exception as e:
        logger.warning("Unparseable payload on %s: %s", subject, e)
        data = {"raw": msg.data.decode("utf-8", errors="replace")}

    delivered = dispatch_event(subject, data)
    logger.info("Processed %s -> delivered to %s", subject, delivered)
    await msg.ack()


async def run_consumer(run_once: bool = False) -> int:
    import nats
    from nats.js.errors import NotFoundError

    logger.info("Connecting to NATS at %s...", NATS_URL)
    nc = await nats.connect(NATS_URL)
    js = nc.jetstream()

    try:
        await js.stream_info(STREAM_NAME)
    except NotFoundError:
        logger.error("Stream %s not found on NATS", STREAM_NAME)
        await nc.close()
        return 1

    sub = await js.subscribe(
        "arifos.consequence.>",
        durable=CONSUMER_DURABLE,
        manual_ack=True,
    )
    logger.info("Durable subscriber '%s' active on 'arifos.consequence.>'", CONSUMER_DURABLE)

    processed_count = 0
    if run_once:
        logger.info("Running in drain/once mode...")
        while True:
            try:
                msg = await sub.next_msg(timeout=1.0)
                await process_message(msg)
                processed_count += 1
            except asyncio.TimeoutError:
                break
        logger.info("Drain complete. Processed %d messages.", processed_count)
    else:
        logger.info("Running in continuous daemon mode. Press Ctrl+C to terminate.")
        try:
            while True:
                msg = await sub.next_msg(timeout=None)
                await process_message(msg)
                processed_count += 1
        except asyncio.CancelledError:
            pass

    await nc.close()
    return 0


def main():
    parser = argparse.ArgumentParser(description="arifOS Consequence Consumer")
    parser.add_argument("--once", action="store_true", help="Process available messages and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuously as daemon")
    args = parser.parse_args()

    mode_once = args.once or (not args.daemon)
    sys.exit(asyncio.run(run_consumer(run_once=mode_once)))


if __name__ == "__main__":
    main()
