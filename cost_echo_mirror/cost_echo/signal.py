"""Signal classification for cost-echo.

Defaults (CLI-configurable):
  green  if drain_score < 0.8 AND closure_rate >= 0.6
  yellow if drain_score < 2.0
  red    otherwise
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ledger import LedgerRow

GREEN = "green"
YELLOW = "yellow"
RED = "red"


@dataclass(frozen=True)
class Thresholds:
    green_drain: float = 0.8
    green_closure: float = 0.6
    yellow_drain: float = 2.0


@dataclass(frozen=True)
class Signal:
    chat_id: str
    actor: str
    display_name: str
    level: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "chat_id": self.chat_id,
            "actor": self.actor,
            "display_name": self.display_name,
            "level": self.level,
            "reason": self.reason,
        }


def classify(row: LedgerRow, th: Thresholds = Thresholds()) -> Signal:
    """Classify one ledger row into green/yellow/red with a reason."""
    if row.drain_score < th.green_drain and row.closure_rate >= th.green_closure:
        return Signal(
            chat_id=row.chat_id,
            actor=row.actor,
            display_name=row.display_name,
            level=GREEN,
            reason=(
                f"balanced: drain {row.drain_score:.2f} < {th.green_drain} "
                f"and closure {row.closure_rate:.2f} >= {th.green_closure}"
            ),
        )
    if row.drain_score < th.yellow_drain:
        return Signal(
            chat_id=row.chat_id,
            actor=row.actor,
            display_name=row.display_name,
            level=YELLOW,
            reason=(
                f"watch: drain {row.drain_score:.2f} below red line "
                f"{th.yellow_drain} but energy or closure slipping "
                f"(closure {row.closure_rate:.2f})"
            ),
        )
    return Signal(
        chat_id=row.chat_id,
        actor=row.actor,
        display_name=row.display_name,
        level=RED,
        reason=(
            f"drain: gives {row.asymmetry:.2f}x what returns and "
            f"{(1 - row.closure_rate) * 100:.0f}% of threads left hanging"
        ),
    )


def classify_all(
    rows: list[LedgerRow], th: Thresholds = Thresholds()
) -> list[Signal]:
    """Classify all rows. Deterministic: same order as input rows."""
    return [classify(r, th) for r in rows]
