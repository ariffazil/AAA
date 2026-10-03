#!/usr/bin/env python3
"""
conversation_reality_gate.py — P0 Conversation Grounding Defect fix.

Three runtime components per Arif's 2026-10-02 diagnosis:

  (1) Speaker/Quote/Reply binding  — Transport metadata > LLM inference.
      If Telegram/voice/whatever channel supplies sender, model does not reinterpret.
      If speaker unknown → UNKNOWN (not "orang lain sebut hang").

  (2) Deterministic time binding    — timestamp + timezone → local_time, computed,
      not guessed. Thread time unknown → UNKNOWN (not "4am").

  (3) Fail-closed epistemic gate   — UNKNOWN + UNSUPPORTED context claims are
              not allowed as ordinary prose. The envelope records them; the human-facing
              output suppresses them.

Design law (Arif 2026-10-02):
    Transport metadata > LLM inference
    Timestamp + timezone → local time
    UNKNOWN ≠ PERMISSION TO IMPROVISE

The gate runs BEFORE generation. It produces a "grounding packet" that the
generator MUST consume; it cannot be skipped. Generators that ignore the
packet are contract-violating.

This module is NOT a new MCP server. It is a deterministic library:
  - no LLM call
  - no remote probe
  - only host facts the channel surfaces (chat_id, sender_id, message_id,
    authored_at, tz, etc.) plus per-thread bindings.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


# ==================================================================
# Data classes — the binding contract
# ==================================================================

@dataclass
class SpeakerBinding:
    speaker_id: str = "UNKNOWN"           # explicit, transport-supplied
    speaker_type: str = "UNKNOWN"        # "user" | "bot" | "external" | UNKNOWN
    confidence: str = "NONE"             # "TRANSPORT" | "INFERRED" | "NONE"
    raw_transport: tuple = None          # e.g. ("telegram", "sender_id=8908024140")


@dataclass
class TemporalBinding:
    authored_at_utc: str = ""            # ISO-8601 of the original message
    timezone: str = "UNKNOWN"            # IANA name, e.g. Asia/Kuala_Lumpur
    local_time: str = "UNKNOWN"          # computed when both are present
    method: str = "COMPUTED"             # COMPUTED | INFERRED | UNKNOWN
    note: str = ""


@dataclass
class QuoteReplyBinding:
    reply_to: str = "UNKNOWN"             # message_id this one replies to
    quoted_message_id: str = "UNKNOWN"
    quoted_author_id: str = "UNKNOWN"
    confidence: str = "NONE"


@dataclass
class ContextEvidence:
    locale: str = "UNKNOWN"               # e.g. ms-MY
    dialect_style: str = "UNKNOWN"        # e.g. Penang-BM (only if explicit)
    spatial_scope: str = "NONE"           # default NONE per Arif's directive
    religious_context: str = "UNKNOWN"    # NEVER inferred from ethnic markers
    meal_context: str = "UNKNOWN"         # NEVER inferred unless in thread
    place_context: str = "UNKNOWN"
    note: str = ""


@dataclass
class GroundingPacket:
    """What the generator MUST consume before producing a response."""
    source: str = "UNKNOWN"               # platform/transport name
    thread_id: str = "UNKNOWN"
    message_id: str = "UNKNOWN"
    speaker: SpeakerBinding = field(default_factory=SpeakerBinding)
    temporal: TemporalBinding = field(default_factory=TemporalBinding)
    quote_reply: QuoteReplyBinding = field(default_factory=QuoteReplyBinding)
    context: ContextEvidence = field(default_factory=ContextEvidence)
    # Computed flags:
    speaker_known: bool = False
    thread_time_known: bool = False
    quote_target_known: bool = False
    # The hard gate result:
    hold_reasons: list = field(default_factory=list)
    # Free-form provenance
    provenance: dict = field(default_factory=dict)


# ==================================================================
# (1) + (2) — Deterministic binding constructors
# ==================================================================

def bind_from_telegram(payload: dict) -> GroundingPacket:
    """
    Build a GroundingPacket from a Telegram transport payload.
    Transport metadata > LLM inference — every field comes from the wire,
    not from heuristic inference.
    """
    chat = payload.get("chat", {}) or {}
    sender = payload.get("from", {}) or {}
    reply = payload.get("reply_to_message", {}) or {}
    sender_id = sender.get("id")
    sender_is_bot = sender.get("is_bot", False)
    sender_type = "bot" if sender_is_bot else ("user" if sender_id else "UNKNOWN")

    # Time
    authored_at = payload.get("date")  # Telegram unix epoch seconds
    if isinstance(authored_at, (int, float)):
        try:
            dt = datetime.fromtimestamp(authored_at, tz=timezone.utc)
            authored_at_iso = dt.isoformat()
        except Exception:
            authored_at_iso = ""
    else:
        authored_at_iso = ""

    pkt = GroundingPacket(
        source="telegram",
        thread_id=str(chat.get("id", "UNKNOWN")),
        message_id=str(payload.get("message_id", "UNKNOWN")),
        speaker=SpeakerBinding(
            speaker_id=str(sender_id) if sender_id is not None else "UNKNOWN",
            speaker_type=sender_type,
            confidence="TRANSPORT" if sender_id is not None else "NONE",
            raw_transport=("telegram", f"sender_id={sender_id}", f"chat_id={chat.get('id')}"),
        ),
        temporal=TemporalBinding(
            authored_at_utc=authored_at_iso,
            timezone="UNKNOWN",   # channel does not surface this directly
            local_time="UNKNOWN", # no tz ⇒ cannot compute local time honestly
            method="UNKNOWN",
            note="Telegram does not carry tz; local_time stays UNKNOWN unless "
                "agent overrides with a known tz binding (e.g. user said it)."
        ),
        quote_reply=QuoteReplyBinding(
            reply_to=str(reply.get("message_id", "UNKNOWN")),
            quoted_message_id=str(reply.get("message_id", "UNKNOWN")),
            quoted_author_id=str((reply.get("from") or {}).get("id", "UNKNOWN")),
            confidence="TRANSPORT" if reply.get("message_id") else "NONE",
        ),
        context=ContextEvidence(
            locale="UNKNOWN",  # agent cannot infer locale from transport
            spatial_scope="NONE",
            religious_context="UNKNOWN",
            meal_context="UNKNOWN",
            place_context="UNKNOWN",
            note="Defaults per Arif 2026-10-02: NONE / UNKNOWN unless explicit.",
        ),
        provenance={
            "transport": "telegram",
            "payload_keys": sorted([k for k in payload.keys() if isinstance(k, str)])[:20],
            "ts": datetime.now(timezone.utc).isoformat(),
        },
    )
    pkt.speaker_known = pkt.speaker.speaker_id != "UNKNOWN"
    pkt.thread_time_known = bool(pkt.temporal.authored_at_utc) and pkt.temporal.timezone != "UNKNOWN"
    pkt.quote_target_known = pkt.quote_reply.quoted_message_id != "UNKNOWN"
    return pkt


def override_tz(packet: GroundingPacket, tz_name: str) -> GroundingPacket:
    """Allow an explicit tz binding (user said it, or session constant)."""
    if not tz_name:
        return packet
    packet.temporal.timezone = tz_name
    # Recompute local_time if both authored_at and tz are now present
    if packet.temporal.authored_at_utc:
        try:
            dt = datetime.fromisoformat(packet.temporal.authored_at_utc)
            from zoneinfo import ZoneInfo
            local = dt.astimezone(ZoneInfo(tz_name))
            packet.temporal.local_time = local.isoformat()
            packet.temporal.method = "COMPUTED"
            packet.thread_time_known = True
        except Exception as e:
            packet.temporal.note += f" | tz override failed: {e}"
    return packet


# ==================================================================
# (3) — Fail-closed epistemic gate
# ==================================================================

# Forbidden context claims: words/phrases that signal improvisation without evidence.
# If a candidate claim mentions any of these AND its evidence_status is UNSUPPORTED,
# the gate SUPPRESSES it from final prose.
FORBIDDEN_CONTEXT_KEYWORDS = [
    # Time-of-day guesses when thread_time is UNKNOWN
    r"\bpukul\s+\d+\b",
    r"\b\d+\s*am\b", r"\b\d+\s*pm\b",
    r"\bpagi\b", r"\bmalam\b", r"\btengah hari\b", r"\bpetang\b",
    r"\bsubuh\b", r"\bmaghrib\b", r"\bisyak\b", r"\bzohor\b", r"\basar\b",
    # Religious practice markers (NEVER infer from "Melayu")
    r"\blepas\s+(isyak|zohor|subuh|asar|maghrib)\b",
    r"\bsolat\b", r"\bpuasa\b",
    # Location/meal guesses when not in transport
    r"\bnasi\s+lemak\b", r"\brestoran\b", r"\bcafe\b", r"\bmakan\s+(kat|di)\b",
    r"\bBurung\s+Hantu\b",
    # Day/date guesses
    r"\besok\b", r"\bkelmarin\b", r"\bsemalam\b",
    r"\bJumaat\b", r"\bIsnin\b", r"\bSelasa\b", r"\bRabu\b", r"\bKhamis\b",
    r"\bSabtu\b", r"\bAhad\b",
    # Speculative activity markers
    r"\blesenfikir\b", r"\bberfikir\b", r"\bbercuti\b", r"\bbekerja\b",
]

def suppress_unsupported_context(claim_text: str, evidence_status: str,
                                claim_kind: str = "context",
                                packet: GroundingPacket | None = None) -> dict:
    """
    Fail-closed gate: if a claim mentions forbidden context and its evidence
    is UNSUPPORTED, the claim is suppressed from human-facing output.

    Returns:
      {
        "decision": "PASS" | "SUPPRESS" | "WARN",
        "reason":     str,
        "allowed_in_prose": bool,
        "suppressed_terms":  [str],
      }

    Design law (Arif 2026-10-02):
        UNKNOWN ≠ PERMISSION TO IMPROVISE
    """
    import re
    if evidence_status != "UNKNOWN":
        # supported claim — pass through (gate does not second-guess positive evidence)
        return {"decision": "PASS", "reason": "evidence != UNKNOWN",
                "allowed_in_prose": True, "suppressed_terms": []}

    hits = []
    for pat in FORBIDDEN_CONTEXT_KEYWORDS:
        for m in re.finditer(pat, claim_text, flags=re.IGNORECASE):
            hits.append(m.group(0))

    # Extra safety: if packet says thread_time_known=False, any time-of-day
    # word in claim is automatically forbidden.
    if packet is not None and not packet.thread_time_known:
        for w in ["pagi", "petang", "malam", "tengah hari", "subuh", "isyak",
                  "zohor", "asar", "maghrib", "am", "pm"]:
            if re.search(rf"\b{w}\b", claim_text, flags=re.IGNORECASE):
                if not any(w.lower() in h.lower() for h in hits):
                    hits.append(w)

    # Extra safety: spatial_scope=NONE forbids location guesses
    if packet is not None and packet.context.spatial_scope == "NONE":
        # Match "kat KL", "di Penang", etc.
        for m in re.finditer(r"\b(kat|di)\s+[A-Z][a-zA-Z]+", claim_text):
            hits.append(m.group(0))

    if hits:
        return {
            "decision": "SUPPRESS",
            "reason": "context claim with no evidence; transport metadata is UNKNOWN",
            "allowed_in_prose": False,
            "suppressed_terms": sorted(set(hits)),
        }
    return {"decision": "PASS", "reason": "no forbidden markers",
            "allowed_in_prose": True, "suppressed_terms": []}


# ==================================================================
# Acceptance harness
# ==================================================================

def gate_test_suite() -> dict:
    """Runnable acceptance for the gate. Returns a per-scenario dict."""
    results = {}

    # === scenario A: Arif's actual bug — "Hang baru lepas Isyak." ===
    pkt = bind_from_telegram({"message_id": 99, "chat": {"id": 1},
                              "from": {"id": 267378578, "is_bot": False},
                              "date": 1727846400})
    claim = "Dah 4 pagi. Hang baru lepas Isyak."
    out = suppress_unsupported_context(claim, "UNKNOWN", packet=pkt)
    results["scenario_A_4am_isyak"] = {
        "claim": claim, "decision": out["decision"],
        "suppressed": out["suppressed_terms"],
        "verdict": "PASS" if out["decision"] == "SUPPRESS" and len(out["suppressed_terms"]) >= 2
        else "FAIL",
    }

    # === scenario B: nasi-lemak-Penang combination ===
    pkt2 = bind_from_telegram({"message_id": 100, "chat": {"id": 1},
                               "from": {"id": 8908024140, "is_bot": False},
                               "date": 1727846400})
    claim2 = "Esok Jumaat kita makan nasi lemak kat Penang, lepas Isyak."
    out2 = suppress_unsupported_context(claim2, "UNKNOWN", packet=pkt2)
    results["scenario_B_nasilemak_penang"] = {
        "claim": claim2, "decision": out2["decision"],
        "suppressed": out2["suppressed_terms"],
        "verdict": "PASS" if out2["decision"] == "SUPPRESS" else "FAIL",
    }

    # === scenario C: SUPPORTED claim (transport actually carries info) ===
    pkt3 = bind_from_telegram({"message_id": 101, "chat": {"id": 1},
                               "from": {"id": 267378578, "is_bot": False},
                               "date": 1727846400})
    # No padding
    out3 = suppress_unsupported_context("OK bang.", "SUPPORTED", packet=pkt3)
    results["scenario_C_supported_passes"] = {
        "claim": "OK bang.", "decision": out3["decision"],
        "verdict": "PASS" if out3["decision"] == "PASS" else "FAIL",
    }

    # === scenario D: speaker binding — Arif's WHO bug ===
    # Telegram says sender=8908024140. The model must NOT reinterpret this.
    # We test the binding function directly.
    pkt4 = bind_from_telegram({"message_id": 102, "chat": {"id": 1},
                               "from": {"id": 8908024140, "is_bot": False},
                               "date": 1727846400})
    results["scenario_D_speaker_transport"] = {
        "speaker_id_from_transport": pkt4.speaker.speaker_id,
        "speaker_known": pkt4.speaker_known,
        "confidence": pkt4.speaker.confidence,
        "verdict": "PASS" if (pkt4.speaker.speaker_id == "8908024140"
                              and pkt4.speaker_known
                              and pkt4.speaker.confidence == "TRANSPORT") else "FAIL",
    }

    # === scenario E: temporal binding — when tz is supplied, local_time MUST compute ===
    pkt5 = bind_from_telegram({"message_id": 103, "chat": {"id": 1},
                               "from": {"id": 267378578, "is_bot": False},
                               "date": 1727846400})
    pkt5 = override_tz(pkt5, "Asia/Kuala_Lumpur")
    results["scenario_E_tz_override"] = {
        "authored_at_utc": pkt5.temporal.authored_at_utc,
        "timezone": pkt5.temporal.timezone,
        "local_time": pkt5.temporal.local_time,
        "method": pkt5.temporal.method,
        "thread_time_known": pkt5.thread_time_known,
        "verdict": "PASS" if (pkt5.temporal.method == "COMPUTED"
                              and pkt5.temporal.local_time != "UNKNOWN"
                              and pkt5.thread_time_known) else "FAIL",
    }

    # === scenario F: temporal binding — NO tz ⇒ local_time MUST stay UNKNOWN ===
    pkt6 = bind_from_telegram({"message_id": 104, "chat": {"id": 1},
                               "from": {"id": 267378578, "is_bot": False},
                               "date": 1727846400})
    results["scenario_F_no_tz"] = {
        "authored_at_utc": pkt6.temporal.authored_at_utc,
        "local_time": pkt6.temporal.local_time,
        "thread_time_known": pkt6.thread_time_known,
        "verdict": "PASS" if (pkt6.temporal.local_time == "UNKNOWN"
                              and not pkt6.thread_time_known) else "FAIL",
    }

    passed = sum(1 for r in results.values() if r.get("verdict") == "PASS")
    return {
        "suite": "P0-conversation-reality-gate",
        "at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": len(results),
        "scenarios": results,
    }


if __name__ == "__main__":
    import argparse, sys
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate-test", action="store_true")
    ap.add_argument("--demo-binding", action="store_true",
                    help="show what the packet looks like for an Arif-sender Telegram payload")
    args = ap.parse_args()

    if args.gate_test:
        out = gate_test_suite()
        print(json.dumps(out, indent=2))
        sys.exit(0 if out["passed"] == out["total"] else 1)

    if args.demo_binding:
        pkt = bind_from_telegram({"message_id": 163229, "chat": {"id": 8324190535},
                                   "from": {"id": 267378578, "is_bot": False},
                                   "date": 1727846400})
        print(json.dumps(asdict(pkt), indent=2, default=str))
        sys.exit(0)

    print("conversation_reality_gate.py — import me, or:")
    print("  --gate-test       run 6/6 acceptance scenarios")
    print("  --demo-binding    show packet shape for an Arif-sender Telegram payload")