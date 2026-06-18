"""
substrate_gate.py — Substrate Gate handler for 000♎️ @arifOS_bot
Owner: arif
Forged: 2026-06-10
Scope: forge-only (C4/C5 forge decisions)
Authority: arifOS F1/F2/F13 floors + WELL substrate data

Constitutional anchor:
  The bot's job is SUBTRACTION, not addition.
  If the bot talked more than the human, it failed.

Usage:
  from substrate_gate import GateHandler, GatePolicy
  handler = GateHandler(policy_path=POLICY_PATH, well_endpoint=WELL_URL)
  # In a /forge handler:
  decision = await handler.evaluate(action_type="commit", payload=...)
  if decision.hold:
      await update.message.reply_text(decision.message, reply_markup=decision.keyboard)
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, time, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

import yaml

log = logging.getLogger("substrate-gate")

# Default policy path; override via env SUBSTRATE_GATE_POLICY
DEFAULT_POLICY_PATH = Path(
    os.environ.get(
        "SUBSTRATE_GATE_POLICY",
        "/root/AAA/registries/SUBSTRATE_GATE_POLICY.yaml",
    )
)
DEFAULT_AUDIT_PATH = Path(
    os.environ.get(
        "SUBSTRATE_GATE_AUDIT",
        "/root/.hermes/cache/substrate-gate/audit.jsonl",
    )
)

# WELL MCP endpoint (local)
WELL_MCP_URL = os.environ.get("WELL_MCP_URL", "http://127.0.0.1:18083/mcp")
WELL_TIMEOUT_S = 5.0

# MYT timezone (Malaysia does not observe DST)
MYT = timezone(timedelta(hours=8))


# ─── Data classes ─────────────────────────────────────────────────────


@dataclass
class SubstrateReading:
    """WELL substrate snapshot at decision time."""

    fatigue: float = 0.0
    sleep_h: float = 0.0
    sleep_debt_days: int = 0
    stress: float = 0.0
    clarity: float = 0.0
    accumulated_session_fatigue: float = 0.0
    measured_at: Optional[str] = None  # ISO-8601 local
    source: str = "no_probe"  # F2 TRUTH: name what is measured vs not


@dataclass
class GateDecision:
    """Result of substrate gate evaluation."""

    hold: bool
    hard_hold: bool = False
    message: str = ""
    inline_keyboard: Optional[list[list[dict[str, str]]]] = None
    defer_target: Optional[str] = None  # ISO-8601 local
    reason: str = ""
    decision_class: str = "C1"
    action_type: str = ""


# ─── Policy loader ────────────────────────────────────────────────────


def load_policy(path: Path = DEFAULT_POLICY_PATH) -> dict:
    """Load the Substrate Gate policy YAML. Fails closed if missing."""
    try:
        with path.open() as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        log.error(f"Substrate Gate policy not found: {path}")
        return _minimal_fail_closed_policy()
    except Exception as exc:
        log.error(f"Substrate Gate policy load failed: {exc}")
        return _minimal_fail_closed_policy()


def _minimal_fail_closed_policy() -> dict:
    """If policy file missing, default to: HOLD everything, fail closed."""
    return {
        "scope": "forge-only",
        "hold_rules": [
            {
                "name": "policy_missing_fail_closed",
                "when": "True",  # always
                "action": "HOLD",
                "bot_message": (
                    "Arif — Substrate Gate policy file missing. "
                    "HOLD semua forge actions until policy restored. "
                    "888 untuk override."
                ),
            }
        ],
        "presence": {"default": "silent"},
        "substrate_thresholds": {
            "decision_fatigue_high": 0.0,  # hold everything
        },
    }


# ─── WELL substrate probe ─────────────────────────────────────────────


async def probe_well_substrate() -> SubstrateReading:
    """
    Probe WELL for current substrate state.

    F2 TRUTH: returns source='no_probe' if WELL is unreachable.
    We do NOT fabricate numbers. The gate falls back to conservative
    (HOLD) defaults when substrate cannot be measured.
    """
    import aiohttp

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "well_assess_homeostasis",
            "arguments": {"mode": "fatigue"},
        },
    }
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=WELL_TIMEOUT_S)) as session:
            async with session.post(WELL_MCP_URL, json=payload) as resp:
                if resp.status != 200:
                    log.warning(f"WELL probe HTTP {resp.status}")
                    return SubstrateReading(source="no_probe_http_error")
                data = await resp.json()
    except Exception as exc:
        log.warning(f"WELL probe failed: {type(exc).__name__}: {exc}")
        return SubstrateReading(source="no_probe_exception")

    # Parse WELL response shape
    result = data.get("result", {})
    try:
        content = json.loads(result.get("content", [{}])[0].get("text", "{}"))
    except Exception:
        return SubstrateReading(source="no_probe_parse_error")

    return SubstrateReading(
        fatigue=float(content.get("decision_fatigue", 0.0)),
        sleep_h=float(content.get("sleep_hours_last_night", 0.0)),
        sleep_debt_days=int(content.get("sleep_debt_days", 0)),
        stress=float(content.get("stress_load", 0.0)),
        clarity=float(content.get("cognitive_clarity", 1.0)),
        accumulated_session_fatigue=float(content.get("accumulated_session_fatigue", 0.0)),
        measured_at=datetime.now(MYT).isoformat(),
        source="well_mcp",
    )


# ─── Time helpers ─────────────────────────────────────────────────────


def is_sleep_window(now: Optional[datetime] = None) -> bool:
    """MYT sleep window 23:00–07:00."""
    if now is None:
        now = datetime.now(MYT)
    h = now.hour
    return h >= 23 or h < 7


def next_8am_myt(now: Optional[datetime] = None) -> datetime:
    """Default defer target: 08:00 MYT tomorrow (or today if before 8am)."""
    if now is None:
        now = datetime.now(MYT)
    target = now.replace(hour=8, minute=0, second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
    return target


# ─── Gate handler ─────────────────────────────────────────────────────


class GateHandler:
    """Substrate Gate evaluation for forge actions."""

    def __init__(self, policy_path: Path = DEFAULT_POLICY_PATH, audit_path: Path = DEFAULT_AUDIT_PATH):
        self.policy = load_policy(policy_path)
        self.audit_path = audit_path
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        self.thresholds = self.policy.get("substrate_thresholds", {})

    async def evaluate(
        self,
        action_type: str,
        decision_class: str,
        substrate: Optional[SubstrateReading] = None,
        now: Optional[datetime] = None,
    ) -> GateDecision:
        """
        Evaluate whether to HOLD a forge action.

        decision_class: C1/C2/C3/C4/C5
        action_type: commit, push, merge, vault_seal, gh_pr, docker_deploy, file_write_shared, etc.
        substrate: optional pre-fetched WELL reading. If None, will probe WELL.
        """
        if now is None:
            now = datetime.now(MYT)

        # Step 1: C1/C2/C3 = silent (never intervene for low-stakes)
        if decision_class in ("C1_low", "C2_medium", "C3_reversible_significant", "C1", "C2", "C3"):
            return GateDecision(
                hold=False,
                reason="decision_class_below_gate",
                decision_class=decision_class,
                action_type=action_type,
            )

        # Step 2: C5 = always HOLD (irreversible)
        if decision_class == "C5_irreversible" or decision_class == "C5":
            return GateDecision(
                hold=True,
                hard_hold=True,
                message=(
                    f"Arif — **{action_type}** ni C5 (irreversible). HOLD.\n"
                    f"Saya tak proceed tanpa ack dari arifOS MCP."
                ),
                inline_keyboard=[
                    [{"text": "HOLD", "callback_data": f"sg:hold:{action_type}"}],
                    [{"text": "888 (ack)", "callback_data": f"sg:proceed:{action_type}"}],
                ],
                reason="c5_always_hold",
                decision_class="C5",
                action_type=action_type,
            )

        # Step 3: C4 = check substrate
        if decision_class == "C4_reversible_substantial" or decision_class == "C4":
            if substrate is None:
                substrate = await probe_well_substrate()

            # Sleep window = silent for C4 unless violation
            if is_sleep_window(now):
                return GateDecision(
                    hold=True,
                    message=(
                        f"Arif — {action_type} ni C4, tapi sekarang {now.strftime('%H:%M')} MYT "
                        f"(sleep window 23:00–07:00). HOLD ke 08:00."
                    ),
                    inline_keyboard=[
                        [{"text": "HOLD 08:00", "callback_data": f"sg:hold:{action_type}"}],
                        [{"text": "888 proceed", "callback_data": f"sg:proceed:{action_type}"}],
                    ],
                    defer_target=next_8am_myt(now).isoformat(),
                    reason="sleep_window_c4",
                    decision_class="C4",
                    action_type=action_type,
                )

            # No substrate data → fail closed (HOLD)
            if substrate.source != "well_mcp":
                return GateDecision(
                    hold=True,
                    message=(
                        f"Arif — {action_type} ni C4. WELL substrate tak dapat diukur "
                        f"({substrate.source}). HOLD sebagai precaution."
                    ),
                    inline_keyboard=[
                        [{"text": "HOLD 08:00", "callback_data": f"sg:hold:{action_type}"}],
                        [{"text": "888 proceed", "callback_data": f"sg:proceed:{action_type}"}],
                    ],
                    defer_target=next_8am_myt(now).isoformat(),
                    reason="substrate_unmeasured_fail_closed",
                    decision_class="C4",
                    action_type=action_type,
                )

            # Substrate measured → apply thresholds
            f_thresh = self.thresholds.get("decision_fatigue_high", 0.6)
            crit_f_thresh = self.thresholds.get("decision_fatigue_critical", 0.85)
            sleep_crit = self.thresholds.get("sleep_debt_days_critical", 3)
            stress_thresh = self.thresholds.get("stress_load_high", 0.7)

            # Critical fatigue or sleep debt → HARD_HOLD
            if substrate.fatigue >= crit_f_thresh or substrate.sleep_debt_days >= sleep_crit:
                return GateDecision(
                    hold=True,
                    hard_hold=True,
                    message=(
                        f"Arif — **{action_type}** C4. Fatigue {substrate.fatigue:.2f}, "
                        f"tidur {substrate.sleep_h:.1f}h, debt {substrate.sleep_debt_days}d.\n"
                        f"Substrate Gate auto-HOLD. 888 override? (rare)"
                    ),
                    inline_keyboard=[
                        [{"text": "HOLD", "callback_data": f"sg:hold:{action_type}"}],
                        [{"text": "888 (rare override)", "callback_data": f"sg:proceed:{action_type}"}],
                    ],
                    defer_target=next_8am_myt(now).isoformat(),
                    reason="c4_critical_hold",
                    decision_class="C4",
                    action_type=action_type,
                )

            # High fatigue or stress → standard HOLD
            if substrate.fatigue >= f_thresh or substrate.stress >= stress_thresh:
                defer = next_8am_myt(now)
                return GateDecision(
                    hold=True,
                    message=(
                        f"Arif — **{action_type}** C4. "
                        f"Fatigue {substrate.fatigue:.2f}, tidur {substrate.sleep_h:.1f}h.\n"
                        f"HOLD ke {defer.strftime('%H:%M')} MYT, atau 888?"
                    ),
                    inline_keyboard=[
                        [{"text": f"HOLD {defer.strftime('%H:%M')}", "callback_data": f"sg:hold:{action_type}"}],
                        [{"text": "888 proceed", "callback_data": f"sg:proceed:{action_type}"}],
                    ],
                    defer_target=defer.isoformat(),
                    reason="c4_fatigue_hold",
                    decision_class="C4",
                    action_type=action_type,
                )

            # Substrate OK → proceed (silent)
            return GateDecision(
                hold=False,
                reason="c4_substrate_ok",
                decision_class="C4",
                action_type=action_type,
            )

        # Unknown class → fail closed
        return GateDecision(
            hold=True,
            message=f"Arif — {action_type} class '{decision_class}' tak dikenali. HOLD.",
            reason="unknown_class_fail_closed",
            decision_class=decision_class,
            action_type=action_type,
        )

    def log_audit(
        self,
        decision: GateDecision,
        substrate: SubstrateReading,
        arif_choice: Optional[str] = None,
    ) -> None:
        """F2 TRUTH: log to audit JSONL."""
        record = {
            "ts_local": datetime.now(MYT).isoformat(),
            "decision_class": decision.decision_class,
            "action_type": decision.action_type,
            "fatigue": substrate.fatigue,
            "sleep_h": substrate.sleep_h,
            "stress": substrate.stress,
            "clarity": substrate.clarity,
            "sleep_debt_days": substrate.sleep_debt_days,
            "substrate_source": substrate.source,
            "hold_or_proceed": "hold" if decision.hold else "proceed",
            "hard_hold": decision.hard_hold,
            "defer_target": decision.defer_target,
            "reason": decision.reason,
            "arif_choice": arif_choice,
            "audit_id": f"sg-{datetime.now(MYT).strftime('%Y%m%d-%H%M%S')}-{os.getpid()}",
        }
        try:
            with self.audit_path.open("a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as exc:
            log.error(f"Audit log failed: {exc}")


# ─── Inline keyboard helper (for python-telegram-bot) ────────────────


def build_inline_keyboard(decision: GateDecision):
    """Convert GateDecision.inline_keyboard to python-telegram-bot InlineKeyboardMarkup."""
    try:
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    except ImportError:
        return None

    if not decision.inline_keyboard:
        return None

    rows = []
    for row in decision.inline_keyboard:
        buttons = [
            InlineKeyboardButton(text=btn["text"], callback_data=btn["callback_data"])
            for btn in row
        ]
        rows.append(buttons)
    return InlineKeyboardMarkup(rows)
