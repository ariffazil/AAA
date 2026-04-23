"""
arifos_plan — Planning Organ Tool
=================================
Constitutional planning tool for external state mutations.

Modes:
  propose_plan   — create SovereignIntent + Plan from intent
  get_plan       — fetch plan by ID
  list_pending   — list plans awaiting approval
  update_status  — transition plan (with PlanReceipt)
  abort_plan     — transition to ABORTED with reason

SEAL authority: NONE. This tool emits CLAIM_ONLY.
All plans require 888_JUDGE verification before EXECUTION.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations
import uuid
import json
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any, List

# ─── Enums ────────────────────────────────────────────────────────────────────

class PlanStatus(Enum):
    DRAFT             = "DRAFT"
    PENDING_APPROVAL  = "PENDING_APPROVAL"
    APPROVED          = "APPROVED"
    IN_EXECUTION      = "IN_EXECUTION"
    COMPLETED         = "COMPLETED"
    ABORTED           = "ABORTED"
    FAILED            = "FAILED"

class RiskBand(Enum):
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"

# ─── Schemas ───────────────────────────────────────────────────────────────────

@dataclass
class SovereignIntent:
    intent_id: str
    description: str
    constraints: Dict[str, Any]
    floors: Dict[str, str]
    risk_prelude: Dict[str, Any]
    created_by: str
    created_at: str
    status: str = "ACTIVE"

    def to_json(self) -> dict:
        return asdict(self)

@dataclass
class Task:
    task_id: str
    description: str
    tool: str
    mutates_external_state: bool
    target_surface: str
    reversible: bool
    risk_band: str
    status: str = "PLANNED"
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Dict] = None
    created_at: str = ""

    def to_json(self) -> dict:
        return asdict(self)

@dataclass
class Plan:
    plan_id: str
    intent_id: str
    epoch_id: str
    status: str
    risk_band: str
    irreversible: bool
    tasks: List[Task]
    created_by: str
    created_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    hold_reason: Optional[str] = None

    def requires_888_hold(self) -> bool:
        return self.irreversible or self.risk_band in ("HIGH", "CRITICAL")

    def to_json(self) -> dict:
        d = asdict(self)
        d['requires_888_hold'] = self.requires_888_hold()
        return d

@dataclass
class PlanReceipt:
    receipt_id: str
    plan_id: str
    decision: str
    decided_by: str
    decided_at: str
    notes: str
    floor_signatures: List[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return asdict(self)

# ─── In-Memory Store (MVP — swap for Postgres in production) ──────────────────

class PlanStore:
    """Ephemeral plan store. Persist to Vault999 in production."""
    def __init__(self):
        self.intents: Dict[str, SovereignIntent] = {}
        self.plans: Dict[str, Plan] = {}
        self.receipts: Dict[str, PlanReceipt] = {}

    def add_intent(self, intent: SovereignIntent):
        self.intents[intent.intent_id] = intent

    def add_plan(self, plan: Plan):
        self.plans[plan.plan_id] = plan

    def add_receipt(self, receipt: PlanReceipt):
        self.receipts[receipt.receipt_id] = receipt

    def get_plan(self, plan_id: str) -> Optional[Plan]:
        return self.plans.get(plan_id)

    def get_plans_by_status(self, status: PlanStatus) -> List[Plan]:
        return [p for p in self.plans.values() if p.status == status.value]

    def get_receipt(self, plan_id: str) -> Optional[PlanReceipt]:
        candidates = [r for r in self.receipts.values() if r.plan_id == plan_id]
        return sorted(candidates, key=lambda r: r.decided_at)[-1] if candidates else None

_store = PlanStore()

# ─── Tool Modes ────────────────────────────────────────────────────────────────

def propose_plan(
    description: str,
    constraints: Optional[Dict[str, Any]] = None,
    floors: Optional[Dict[str, str]] = None,
    risk_prelude: Optional[Dict[str, Any]] = None,
    tasks: Optional[List[Dict]] = None,
    created_by: str = "arifOS_bot",
    epoch_id: str = "",
    risk_band: str = "MEDIUM",
    irreversible: bool = False,
    metadata: Optional[Dict] = None
) -> dict:
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    intent_id = f"intent-{uuid.uuid4().hex[:12]}"
    plan_id = f"plan-{uuid.uuid4().hex[:12]}"

    intent = SovereignIntent(
        intent_id=intent_id,
        description=description,
        constraints=constraints or {},
        floors=floors or {},
        risk_prelude=risk_prelude or {},
        created_by=created_by,
        created_at=now,
    )
    _store.add_intent(intent)

    task_objects = []
    for t in (tasks or []):
        task = Task(
            task_id=f"task-{uuid.uuid4().hex[:8]}",
            description=t.get("description", ""),
            tool=t.get("tool", "unknown"),
            mutates_external_state=t.get("mutates_external_state", True),
            target_surface=t.get("target_surface", "unknown"),
            reversible=t.get("reversible", False),
            risk_band=t.get("risk_band", "LOW"),
            dependencies=t.get("dependencies", []),
            status="PLANNED",
            created_at=now,
        )
        task_objects.append(task)

    plan = Plan(
        plan_id=plan_id,
        intent_id=intent_id,
        epoch_id=epoch_id or now,
        status="DRAFT",
        risk_band=risk_band.upper(),
        irreversible=irreversible,
        tasks=task_objects,
        created_by=created_by,
        created_at=now,
        metadata=metadata or {},
    )

    if plan.requires_888_hold():
        plan.status = "PENDING_APPROVAL"
        plan.hold_reason = (
            f"888_HOLD: risk_band={risk_band} and/or irreversible={irreversible}. "
            f"Sovereign approval required before EXECUTION."
        )
    else:
        plan.status = "APPROVED"

    _store.add_plan(plan)

    return {
        "CLAIM_ONLY": True,
        "verdict": "SEAL" if plan.status == "APPROVED" else "HOLD",
        "hold_reason": plan.hold_reason,
        "plan": plan.to_json(),
        "intent": intent.to_json(),
    }

def get_plan(plan_id: str) -> dict:
    plan = _store.get_plan(plan_id)
    if not plan:
        return {"CLAIM_ONLY": True, "verdict": "VOID", "reason": f"Plan {plan_id} not found"}
    receipt = _store.get_receipt(plan_id)
    return {
        "CLAIM_ONLY": True,
        "plan": plan.to_json(),
        "receipt": receipt.to_json() if receipt else None,
    }

def list_pending(epoch_id: str = "") -> dict:
    pending = _store.get_plans_by_status(PlanStatus.PENDING_APPROVAL)
    plans = [p.to_json() for p in pending if not epoch_id or p.epoch_id == epoch_id]
    return {"CLAIM_ONLY": True, "count": len(plans), "plans": plans}

def update_status(
    plan_id: str,
    decision: str,
    decided_by: str = "arifOS_bot",
    notes: str = "",
    floor_signatures: Optional[List[str]] = None
) -> dict:
    plan = _store.get_plan(plan_id)
    if not plan:
        return {"CLAIM_ONLY": True, "verdict": "VOID", "reason": f"Plan {plan_id} not found"}

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    receipt = PlanReceipt(
        receipt_id=f"receipt-{uuid.uuid4().hex[:12]}",
        plan_id=plan_id,
        decision=decision.upper(),
        decided_by=decided_by,
        decided_at=now,
        notes=notes,
        floor_signatures=floor_signatures or [],
    )
    _store.add_receipt(receipt)

    if decision.upper() == "APPROVED":
        if plan.status == "PENDING_APPROVAL":
            plan.status = "APPROVED"
        return {"CLAIM_ONLY": True, "verdict": "SEAL", "plan": plan.to_json(), "receipt": receipt.to_json()}
    elif decision.upper() == "REJECTED":
        plan.status = "ABORTED"
        return {"CLAIM_ONLY": True, "verdict": "VOID", "plan": plan.to_json(), "receipt": receipt.to_json()}
    elif decision.upper() == "HOLD":
        return {"CLAIM_ONLY": True, "verdict": "HOLD", "plan": plan.to_json(), "receipt": receipt.to_json()}

    return {"CLAIM_ONLY": True, "verdict": "VOID", "reason": f"Unknown decision: {decision}"}

def abort_plan(plan_id: str, reason: str, aborted_by: str = "arifOS_bot") -> dict:
    plan = _store.get_plan(plan_id)
    if not plan:
        return {"CLAIM_ONLY": True, "verdict": "VOID", "reason": f"Plan {plan_id} not found"}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    receipt = PlanReceipt(
        receipt_id=f"receipt-{uuid.uuid4().hex[:12]}",
        plan_id=plan_id,
        decision="REJECTED",
        decided_by=aborted_by,
        decided_at=now,
        notes=f"Abort: {reason}",
        floor_signatures=["F1"],
    )
    _store.add_receipt(receipt)
    plan.status = "ABORTED"
    return {"CLAIM_ONLY": True, "verdict": "SEAL", "plan": plan.to_json(), "receipt": receipt.to_json()}

# ─── MCP Shim ─────────────────────────────────────────────────────────────────

def arifos_plan(mode: str, payload: dict) -> dict:
    """
    Main entry point.
    mode in {propose_plan, get_plan, list_pending, update_status, abort_plan}
    All calls emit CLAIM_ONLY. 888_JUDGE must ratify before EXECUTION.
    """
    if mode == "propose_plan":
        return propose_plan(**payload)
    elif mode == "get_plan":
        return get_plan(payload.get("plan_id"))
    elif mode == "list_pending":
        return list_pending(payload.get("epoch_id", ""))
    elif mode == "update_status":
        return update_status(
            plan_id=payload["plan_id"],
            decision=payload["decision"],
            decided_by=payload.get("decided_by", "arifOS_bot"),
            notes=payload.get("notes", ""),
            floor_signatures=payload.get("floor_signatures"),
        )
    elif mode == "abort_plan":
        return abort_plan(
            plan_id=payload["plan_id"],
            reason=payload.get("reason", "Sovereign abort"),
            aborted_by=payload.get("aborted_by", "arifOS_bot"),
        )
    else:
        return {"CLAIM_ONLY": True, "verdict": "VOID", "reason": f"Unknown mode: {mode}"}
