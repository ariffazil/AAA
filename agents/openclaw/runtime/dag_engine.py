#!/usr/bin/env python3
"""
OpenClaw DAG Workflow Engine v1.0.0

Declarative JSON workflow execution with:
  - Fan-out (parallel sub-agent execution)
  - Fan-in (result aggregation)
  - Checkpoint/resume on failure
  - Dependency-aware ordering
  - Integration with forge_parallel for concurrent execution

Workflow format: JSON DAG with phases, tasks, dependencies.

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import time
import uuid
import urllib.request
import urllib.error
from enum import Enum
from typing import Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict


# ─── Constants ───────────────────────────────────────────────────────────
AAA_A2A_URL = "http://127.0.0.1:3001/a2a"
FORGE_PARALLEL_URL = "http://127.0.0.1:7071/mcp"  # A-FORGE for forge_parallel
CHECKPOINT_DIR = os.environ.get("DAG_CHECKPOINT_DIR", "/tmp/openclaw-dag-checkpoints")
MAX_PARALLEL = int(os.environ.get("DAG_MAX_PARALLEL", "8"))
TASK_TIMEOUT_SECONDS = int(os.environ.get("DAG_TASK_TIMEOUT", "120"))
FLOW_TIMEOUT_SECONDS = int(os.environ.get("DAG_FLOW_TIMEOUT", "600"))


class TaskState(str, Enum):
    PENDING = "pending"
    READY = "ready"  # dependencies met, ready to execute
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"  # dependency failed, skip this task
    CANCELLED = "cancelled"


class FlowState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"  # checkpoint saved, can resume
    CANCELLED = "cancelled"


@dataclass
class TaskDef:
    """Definition of a single task in the DAG."""

    id: str
    agent: str  # Target agent (hermes-asi, 333-AGI, geox, wealth, well)
    skill: str = "agent-dispatch"  # Skill/tool to invoke
    query: str = ""  # Task prompt/query
    depends_on: list[str] = field(default_factory=list)  # Task IDs this depends on
    fan_out: bool = False  # If true, query is split across parallel instances
    fan_out_items: list[str] = field(default_factory=list)  # Items for fan-out
    merge_strategy: str = "concat"  # How to merge fan-out results: concat|vote|best|first
    timeout_seconds: int = TASK_TIMEOUT_SECONDS
    retry_count: int = 0
    priority: str = "normal"
    context: dict = field(default_factory=dict)
    # Runtime state
    state: str = TaskState.PENDING
    result: Any = None
    error: str = ""
    started_at: float = 0
    completed_at: float = 0
    attempts: int = 0


@dataclass
class FlowDef:
    """Definition of a workflow (DAG of tasks)."""

    id: str
    name: str
    description: str = ""
    tasks: list[TaskDef] = field(default_factory=list)
    context: dict = field(default_factory=dict)  # Shared context for all tasks
    # Runtime state
    state: str = FlowState.PENDING
    started_at: float = 0
    completed_at: float = 0
    checkpoint_path: str = ""


class DAGValidationError(Exception):
    """Raised when DAG has cycles or missing dependencies."""

    pass


class DAGEngine:
    """
    Declarative DAG workflow executor for OpenClaw.

    Supports:
    - Sequential task chains (A → B → C)
    - Parallel fan-out (A → [B1, B2, B3] → C)
    - Dependency-aware ordering
    - Checkpoint/resume on failure
    - Integration with forge_parallel for concurrent execution
    """

    def __init__(self):
        self._flows: dict[str, FlowDef] = {}
        self._task_executor: Callable | None = None
        os.makedirs(CHECKPOINT_DIR, exist_ok=True)
        self._load_all_checkpoints()

    # ─── Public API ──────────────────────────────────────────────────

    def define_flow(self, flow_json: dict) -> FlowDef:
        """
        Define a workflow from JSON spec.

        JSON format:
        {
            "id": "flow_xxx",
            "name": "Multi-step research",
            "description": "Research + analyze + report",
            "context": {"person_id": "ARIF"},
            "tasks": [
                {
                    "id": "t1_research",
                    "agent": "hermes-asi",
                    "skill": "deep-research",
                    "query": "Research gold trends",
                    "depends_on": []
                },
                {
                    "id": "t2_analyze",
                    "agent": "wealth",
                    "skill": "capital-market",
                    "query": "Analyze impact on portfolio",
                    "depends_on": ["t1_research"]
                },
                {
                    "id": "t3_report",
                    "agent": "hermes-asi",
                    "skill": "artifact-delivery",
                    "query": "Draft brief from analysis",
                    "depends_on": ["t2_analyze"]
                }
            ]
        }
        """
        flow_id = flow_json.get("id", f"flow-{uuid.uuid4().hex[:8]}")

        tasks = []
        for t in flow_json.get("tasks", []):
            task = TaskDef(
                id=t["id"],
                agent=t["agent"],
                skill=t.get("skill", "agent-dispatch"),
                query=t.get("query", ""),
                depends_on=t.get("depends_on", []),
                fan_out=t.get("fan_out", False),
                fan_out_items=t.get("fan_out_items", []),
                merge_strategy=t.get("merge_strategy", "concat"),
                timeout_seconds=t.get("timeout_seconds", TASK_TIMEOUT_SECONDS),
                retry_count=t.get("retry_count", 0),
                priority=t.get("priority", "normal"),
                context=t.get("context", {}),
            )
            tasks.append(task)

        flow = FlowDef(
            id=flow_id,
            name=flow_json.get("name", flow_id),
            description=flow_json.get("description", ""),
            tasks=tasks,
            context=flow_json.get("context", {}),
        )

        # Validate DAG
        self._validate_dag(flow)

        self._flows[flow_id] = flow
        self._save_checkpoint(flow)  # Persist to disk for cross-subprocess access
        return flow

    def execute(
        self,
        flow_id: str,
        *,
        dry_run: bool = False,
        resume_from: str | None = None,
    ) -> dict:
        """
        Execute a workflow. Returns final flow state with all results.

        Args:
            flow_id: Flow to execute
            dry_run: If true, show execution plan without running
            resume_from: Checkpoint to resume from
        """
        flow = self._flows.get(flow_id)
        if not flow:
            return {"error": f"Flow {flow_id} not found"}

        if dry_run:
            return self._execution_plan(flow)

        # Resume from checkpoint if specified
        if resume_from:
            self._load_checkpoint(flow, resume_from)

        flow.state = FlowState.RUNNING
        flow.started_at = time.time()

        try:
            self._execute_dag(flow)
        except Exception as e:
            flow.state = FlowState.FAILED
            self._save_checkpoint(flow)
            return self._flow_result(flow, error=str(e))

        flow.completed_at = time.time()
        flow.state = FlowState.COMPLETED

        # Check if any tasks failed
        if any(t.state == TaskState.FAILED for t in flow.tasks):
            flow.state = FlowState.FAILED

        return self._flow_result(flow)

    def get_status(self, flow_id: str) -> dict:
        """Get current flow status without executing."""
        flow = self._flows.get(flow_id)
        if not flow:
            return {"error": f"Flow {flow_id} not found"}
        return self._flow_result(flow)

    def cancel(self, flow_id: str) -> dict:
        """Cancel a running flow."""
        flow = self._flows.get(flow_id)
        if not flow:
            return {"error": f"Flow {flow_id} not found"}

        flow.state = FlowState.CANCELLED
        for task in flow.tasks:
            if task.state in (TaskState.PENDING, TaskState.READY, TaskState.RUNNING):
                task.state = TaskState.CANCELLED

        return self._flow_result(flow)

    # ─── DAG Execution Engine ────────────────────────────────────────

    def _execute_dag(self, flow: FlowDef) -> None:
        """Execute DAG respecting dependency order."""
        remaining = {
            t.id
            for t in flow.tasks
            if t.state not in (TaskState.COMPLETED, TaskState.FAILED, TaskState.SKIPPED, TaskState.CANCELLED)
        }

        while remaining:
            # Find tasks whose dependencies are all met
            ready_tasks = []
            for task in flow.tasks:
                if task.id not in remaining:
                    continue
                if task.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.SKIPPED, TaskState.CANCELLED):
                    remaining.discard(task.id)
                    continue

                deps_met = all(self._get_task(flow, dep_id).state == TaskState.COMPLETED for dep_id in task.depends_on)

                if deps_met:
                    # Check if any dependency failed
                    deps_failed = any(
                        self._get_task(flow, dep_id).state == TaskState.FAILED for dep_id in task.depends_on
                    )
                    if deps_failed:
                        task.state = TaskState.SKIPPED
                        remaining.discard(task.id)
                        continue

                    task.state = TaskState.READY
                    ready_tasks.append(task)

            if not ready_tasks and remaining:
                # Deadlock detected — all remaining tasks have unmet deps
                for task in flow.tasks:
                    if task.id in remaining:
                        task.state = TaskState.FAILED
                        task.error = "Deadlock: dependencies cannot be satisfied"
                break

            # Execute ready tasks (parallel if possible)
            if ready_tasks:
                self._execute_parallel(flow, ready_tasks)
                for task in ready_tasks:
                    remaining.discard(task.id)

            # Checkpoint after each wave
            self._save_checkpoint(flow)

    def _execute_parallel(self, flow: FlowDef, tasks: list[TaskDef]) -> None:
        """Execute a batch of tasks in parallel."""
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
            futures = {}
            for task in tasks:
                task.state = TaskState.RUNNING
                task.started_at = time.time()
                task.attempts += 1

                if task.fan_out and task.fan_out_items:
                    future = executor.submit(self._execute_fan_out, flow, task)
                else:
                    future = executor.submit(self._execute_single, flow, task)
                futures[future] = task

            for future in concurrent.futures.as_completed(futures, timeout=FLOW_TIMEOUT_SECONDS):
                task = futures[future]
                try:
                    result = future.result(timeout=task.timeout_seconds)
                    task.result = result
                    task.state = TaskState.COMPLETED
                except Exception as e:
                    task.error = str(e)
                    task.state = TaskState.FAILED
                    # Retry if configured
                    if task.attempts <= task.retry_count:
                        task.state = TaskState.PENDING
                        task.error = ""
                finally:
                    task.completed_at = time.time()

    def _execute_single(self, flow: FlowDef, task: TaskDef) -> Any:
        """Execute a single task via A2A dispatch."""
        # Merge flow context with task context
        merged_context = {**flow.context, **task.context}

        # Inject results from dependencies
        for dep_id in task.depends_on:
            dep_task = self._get_task(flow, dep_id)
            if dep_task and dep_task.result:
                merged_context[f"result_{dep_id}"] = dep_task.result

        # Build A2A task payload
        payload = {
            "jsonrpc": "2.0",
            "id": f"dag-{task.id}-{uuid.uuid4().hex[:8]}",
            "method": "tasks/send",
            "params": {
                "id": f"dag-{task.id}-{uuid.uuid4().hex[:8]}",
                "sessionId": f"dag-session-{flow.id}",
                "targetAgent": task.agent,
                "message": {
                    "role": "agent",
                    "parts": [{"type": "text", "text": task.query}],
                },
                "skill": task.skill,
                "metadata": {
                    "flow_id": flow.id,
                    "task_id": task.id,
                    "priority": task.priority,
                    "source_agent": "openclaw-dag",
                    "context": merged_context,
                },
            },
        }

        return self._emit_a2a(payload, timeout=task.timeout_seconds)

    def _execute_fan_out(self, flow: FlowDef, task: TaskDef) -> Any:
        """Execute fan-out: split query across items, then merge results."""
        results = []

        for item in task.fan_out_items:
            item_query = task.query.replace("{item}", item)
            item_task = TaskDef(
                id=f"{task.id}__{item}",
                agent=task.agent,
                skill=task.skill,
                query=item_query,
                timeout_seconds=task.timeout_seconds,
                context={**task.context, "fan_out_item": item},
            )
            try:
                result = self._execute_single(flow, item_task)
                results.append({"item": item, "result": result, "success": True})
            except Exception as e:
                results.append({"item": item, "error": str(e), "success": False})

        return self._merge_fan_out(results, task.merge_strategy)

    def _merge_fan_out(self, results: list[dict], strategy: str) -> Any:
        """Merge fan-out results based on strategy."""
        successful = [r for r in results if r.get("success")]

        if strategy == "first":
            return successful[0]["result"] if successful else {"error": "All fan-out items failed"}
        elif strategy == "concat":
            return {
                "merged": True,
                "strategy": "concat",
                "results": results,
                "success_count": len(successful),
                "total_count": len(results),
            }
        elif strategy == "vote":
            # Majority vote on success/failure
            success_count = len(successful)
            return {
                "merged": True,
                "strategy": "vote",
                "verdict": "pass" if success_count > len(results) / 2 else "fail",
                "results": results,
            }
        elif strategy == "best":
            # Return the result with most content
            if successful:
                best = max(successful, key=lambda r: len(str(r.get("result", ""))))
                return best["result"]
            return {"error": "All fan-out items failed"}
        else:
            return results

    # ─── A2A Communication ───────────────────────────────────────────

    def _emit_a2a(self, payload: dict, timeout: int = 30) -> dict:
        """POST A2A task to AAA gateway."""
        payload_bytes = json.dumps(payload).encode()

        req = urllib.request.Request(
            AAA_A2A_URL,
            data=payload_bytes,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "A2A-Version": "1.0",
                "X-Actor-Id": "openclaw-dag",
            },
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
            return data.get("result", data)

    # ─── Checkpoint/Resume ───────────────────────────────────────────

    def _save_checkpoint(self, flow: FlowDef) -> None:
        """Save flow state to checkpoint file."""
        checkpoint = {
            "flow_id": flow.id,
            "state": flow.state,
            "tasks": [
                {
                    "id": t.id,
                    "state": t.state,
                    "result": t.result,
                    "error": t.error,
                    "attempts": t.attempts,
                    "started_at": t.started_at,
                    "completed_at": t.completed_at,
                }
                for t in flow.tasks
            ],
            "timestamp": time.time(),
        }

        path = os.path.join(CHECKPOINT_DIR, f"{flow.id}.json")
        with open(path, "w") as f:
            json.dump(checkpoint, f, indent=2, default=str)
        flow.checkpoint_path = path

    def _load_checkpoint(self, flow: FlowDef, checkpoint_path: str) -> None:
        """Load flow state from checkpoint."""
        with open(checkpoint_path) as f:
            checkpoint = json.load(f)

        for saved in checkpoint.get("tasks", []):
            task = self._get_task(flow, saved["id"])
            if task:
                task.state = saved.get("state", TaskState.PENDING)
                task.result = saved.get("result")
                task.error = saved.get("error", "")
                task.attempts = saved.get("attempts", 0)

    def _load_all_checkpoints(self) -> None:
        """Load all persisted flow definitions from checkpoint directory."""
        if not os.path.exists(CHECKPOINT_DIR):
            return
        for fname in os.listdir(CHECKPOINT_DIR):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(CHECKPOINT_DIR, fname)
            try:
                with open(path) as f:
                    data = json.load(f)
                flow_id = data.get("flow_id", "")
                if not flow_id:
                    continue
                # Reconstruct FlowDef from checkpoint
                tasks = []
                for t in data.get("tasks", []):
                    task = TaskDef(
                        id=t.get("id", ""),
                        agent=t.get("agent", "unknown"),
                        skill=t.get("skill", "agent-dispatch"),
                        query=t.get("query", ""),
                        depends_on=t.get("depends_on", []),
                        state=t.get("state", TaskState.PENDING),
                        result=t.get("result"),
                        error=t.get("error", ""),
                        attempts=t.get("attempts", 0),
                    )
                    tasks.append(task)
                flow = FlowDef(
                    id=flow_id,
                    name=data.get("name", flow_id),
                    tasks=tasks,
                    state=data.get("state", FlowState.PENDING),
                    checkpoint_path=path,
                )
                self._flows[flow_id] = flow
            except Exception:
                continue  # Skip corrupted checkpoints

    # ─── Validation ──────────────────────────────────────────────────

    def _validate_dag(self, flow: FlowDef) -> None:
        """Validate DAG has no cycles and all deps exist."""
        task_ids = {t.id for t in flow.tasks}

        # Check all dependencies exist
        for task in flow.tasks:
            for dep in task.depends_on:
                if dep not in task_ids:
                    raise DAGValidationError(f"Task '{task.id}' depends on '{dep}' which doesn't exist")

        # Check for cycles using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            task = self._get_task(flow, task_id)
            if task:
                for dep in task.depends_on:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True
            rec_stack.discard(task_id)
            return False

        for task in flow.tasks:
            if task.id not in visited:
                if has_cycle(task.id):
                    raise DAGValidationError(f"Cycle detected involving task '{task.id}'")

    # ─── Helpers ─────────────────────────────────────────────────────

    def _get_task(self, flow: FlowDef, task_id: str) -> Optional[TaskDef]:
        """Get task by ID within a flow."""
        for task in flow.tasks:
            if task.id == task_id:
                return task
        return None

    def _execution_plan(self, flow: FlowDef) -> dict:
        """Generate execution plan (dry run)."""
        # Topological sort for execution order
        levels = []
        remaining = {t.id for t in flow.tasks}
        completed = set()

        while remaining:
            level = []
            for task in flow.tasks:
                if task.id in remaining and all(d in completed for d in task.depends_on):
                    level.append(task.id)
            if not level:
                break
            levels.append(level)
            completed.update(level)
            remaining -= set(level)

        return {
            "flow_id": flow.id,
            "name": flow.name,
            "dry_run": True,
            "execution_levels": levels,
            "total_tasks": len(flow.tasks),
            "parallel_waves": len(levels),
            "tasks": [
                {
                    "id": t.id,
                    "agent": t.agent,
                    "skill": t.skill,
                    "depends_on": t.depends_on,
                    "fan_out": t.fan_out,
                    "fan_out_items": t.fan_out_items,
                }
                for t in flow.tasks
            ],
        }

    def _flow_result(self, flow: FlowDef, error: str = "") -> dict:
        """Generate flow result summary."""
        return {
            "flow_id": flow.id,
            "name": flow.name,
            "state": flow.state,
            "error": error,
            "started_at": flow.started_at,
            "completed_at": flow.completed_at,
            "duration_seconds": round(flow.completed_at - flow.started_at, 2) if flow.completed_at else 0,
            "tasks": [
                {
                    "id": t.id,
                    "agent": t.agent,
                    "state": t.state,
                    "error": t.error,
                    "duration_seconds": round(t.completed_at - t.started_at, 2) if t.completed_at else 0,
                    "result_preview": str(t.result)[:200] if t.result else None,
                }
                for t in flow.tasks
            ],
            "checkpoint_path": flow.checkpoint_path,
        }


# ─── Module-level singleton ─────────────────────────────────────────────
_engine: DAGEngine | None = None


def get_dag_engine() -> DAGEngine:
    """Get or create the singleton DAGEngine."""
    global _engine
    if _engine is None:
        _engine = DAGEngine()
    return _engine


def define_workflow(flow_json: dict) -> dict:
    """Convenience: define a workflow from JSON."""
    flow = get_dag_engine().define_flow(flow_json)
    return {"flow_id": flow.id, "name": flow.name, "tasks": len(flow.tasks)}


def execute_workflow(flow_id: str, *, dry_run: bool = False) -> dict:
    """Convenience: execute a workflow."""
    return get_dag_engine().execute(flow_id, dry_run=dry_run)


# ─── Pre-built workflow templates ───────────────────────────────────────

TEMPLATES = {
    "research_and_report": {
        "id": "tmpl_research_report",
        "name": "Research → Analyze → Report",
        "description": "Deep research, then domain analysis, then human-facing report",
        "tasks": [
            {
                "id": "research",
                "agent": "hermes-asi",
                "skill": "deep-research",
                "query": "{query}",
            },
            {
                "id": "analyze",
                "agent": "{domain_agent}",
                "skill": "{domain_skill}",
                "query": "Analyze findings from research: {query}",
                "depends_on": ["research"],
            },
            {
                "id": "report",
                "agent": "hermes-asi",
                "skill": "artifact-delivery",
                "query": "Draft human-facing brief from analysis",
                "depends_on": ["analyze"],
            },
        ],
    },
    "multi_domain_synthesis": {
        "id": "tmpl_multi_domain",
        "name": "Multi-Domain Fan-Out → Synthesis",
        "description": "Query multiple domain organs in parallel, then synthesize",
        "tasks": [
            {
                "id": "fanout",
                "agent": "auto",
                "skill": "domain-query",
                "query": "{query}",
                "fan_out": True,
                "fan_out_items": ["geox", "wealth", "well"],
                "merge_strategy": "concat",
            },
            {
                "id": "synthesize",
                "agent": "hermes-asi",
                "skill": "deep-research",
                "query": "Synthesize multi-domain findings: {query}",
                "depends_on": ["fanout"],
            },
        ],
    },
    "code_review_pipeline": {
        "id": "tmpl_code_review",
        "name": "Code → Review → Test → Deploy",
        "description": "Full code change pipeline with review gate",
        "tasks": [
            {
                "id": "implement",
                "agent": "333-AGI",
                "skill": "code-execute",
                "query": "{query}",
            },
            {
                "id": "review",
                "agent": "555-ASI",
                "skill": "code-review",
                "query": "Review implementation",
                "depends_on": ["implement"],
            },
            {
                "id": "test",
                "agent": "333-AGI",
                "skill": "code-execute",
                "query": "Run tests and verify",
                "depends_on": ["review"],
            },
        ],
    },
}


def create_from_template(template_name: str, variables: dict) -> dict:
    """Create a workflow from a pre-built template."""
    template = TEMPLATES.get(template_name)
    if not template:
        return {"error": f"Template '{template_name}' not found. Available: {list(TEMPLATES.keys())}"}

    # Deep copy and substitute variables
    import copy

    flow_json = copy.deepcopy(template)

    def substitute(obj):
        if isinstance(obj, str):
            for key, value in variables.items():
                obj = obj.replace(f"{{{key}}}", str(value))
            return obj
        elif isinstance(obj, dict):
            return {k: substitute(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [substitute(item) for item in obj]
        return obj

    flow_json = substitute(flow_json)
    flow_json["context"] = variables

    return define_workflow(flow_json)


# ─── CLI ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python dag_engine.py plan <flow_json_file>")
        print("  python dag_engine.py execute <flow_id>")
        print("  python dag_engine.py template <name> key=value ...")
        print(f"\nTemplates: {list(TEMPLATES.keys())}")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "plan":
        with open(sys.argv[2]) as f:
            flow_json = json.load(f)
        result = define_workflow(flow_json)
        plan = execute_workflow(result["flow_id"], dry_run=True)
        print(json.dumps(plan, indent=2))

    elif cmd == "execute":
        result = execute_workflow(sys.argv[2])
        print(json.dumps(result, indent=2, default=str))

    elif cmd == "template":
        name = sys.argv[2]
        variables = {}
        for arg in sys.argv[3:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                variables[k] = v
        result = create_from_template(name, variables)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
