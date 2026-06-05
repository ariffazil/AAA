#!/usr/bin/env python3
"""
TREE777 Workflow Runtime Engine — v1.3.0
=========================================
Fixes from v1.2.0:
- D3 FIX: reflect_attempts counter persisted in state.json
- MAX_REFLECT=3 before escalation to 888_HOLD
- Counter resets when REFLECT returns worked=False
- Fixed loop guard placement
- All state persisted to disk, not memory
"""

import json, sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


class WorkflowEngine:
    def __init__(self, workflow_id: str, dry_run: bool = False, resume: bool = False):
        self.workflow_id = workflow_id
        self.dry_run = dry_run
        self.resume = resume
        self.base = Path("/root/AAA/wiki/workflows/" + workflow_id)
        self.plan = self._load_plan()
        self.state = self._load_state()
        self.steps = {s["step_id"]: s for s in self.plan["steps"]}

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _load_plan(self) -> dict:
        with open(self.base / "plan.json") as f:
            return json.load(f)

    def _load_state(self) -> dict:
        path = self.base / "state.json"
        if self.resume and path.exists():
            with open(path) as f:
                return json.load(f)
        defaults = {
            "workflow_id": self.workflow_id,
            "status": "init",
            "current_step": None,
            "completed_steps": [],
            "artifacts": {},
            "error_log": [],
            "reflect_attempts": 0,
        }
        if self.resume and path.exists():
            with open(path) as f:
                saved = json.load(f)
                # Preserve reflect_attempts from prior runs (D3 fix)
                saved.setdefault("reflect_attempts", 0)
                return saved
        return defaults

    def _save_state(self):
        self.state["last_updated"] = self._now()
        with open(self.base / "state.json", "w") as f:
            json.dump(self.state, f, indent=2)

    def _gate_path(self, step_id: str) -> Path:
        return self.base / "gates" / (step_id + ".json")

    def _read_gate(self, step_id: str) -> dict:
        p = self._gate_path(step_id)
        if p.exists():
            return json.load(open(p))
        return {"step_id": step_id, "status": "pending", "passed": None, "retry_count": 0}

    def _write_gate(self, step_id: str, gate_data: dict):
        with open(self._gate_path(step_id), "w") as f:
            json.dump(gate_data, f, indent=2)
        self._save_state()

    def _verify(self, step: dict) -> tuple[bool, str]:
        v = step.get("verification", "").strip()
        if not v or v == "none":
            return True, "no verification"
        if self.dry_run:
            return True, "DRY RUN — verification skipped"
        base = str(self.base)
        config_path = self.state.get("config_path", "")
        if v.startswith("test -f"):
            path = v.replace("test -f", "").strip().replace("<config_path>", config_path)
            if not path.startswith("/"):
                path = base + "/" + path
            r = Path(path).exists()
            return r, "test -f " + Path(path).name + " → " + str(r)
        if v.startswith("grep"):
            parts = v.split(None, 2)
            pat = parts[1]
            fp = parts[2] if len(parts) > 2 else None
            if fp:
                fp = fp.replace("<config_path>", config_path)
                if not fp.startswith("/"):
                    fp = base + "/" + fp
            else:
                fp = str(self.base / "state.json")
            try:
                with open(fp) as f:
                    found = pat in f.read()
                return found, "grep '" + pat + "' → " + str(found)
            except Exception as e:
                return False, "grep error: " + str(e)
        if v.startswith("ls "):
            results = list(self.base.glob(v[3:].strip()))
            return len(results) > 0, "ls → " + str(len(results)) + " matches"
        return True, v

    def _run_step(self, step: dict) -> tuple[bool, Any]:
        tool = step.get("tool", "internal")
        mode = step.get("mode", "")
        step["step_id"]
        print("    [" + tool + "/" + (mode or "default") + "]")
        if self.dry_run:
            output = {"dry_run": True, "tool": tool, "mode": mode}
            if tool == "arif_heart_critique":
                output["worked"] = True
            return True, output
        handlers = {
            "arif_session_init": lambda s: (True, {"session_id": self.state.get("session_id", "")}),
            "arif_mind_reason": lambda s: (True, {"tool": "arif_mind_reason"}),
            "arif_forge_execute": lambda s: (True, {"tool": "arif_forge_execute"}),
            "arif_sense_observe": lambda s: (True, {"tool": "arif_sense_observe"}),
            "arif_heart_critique": lambda s: (True, {"tool": "arif_heart_critique", "worked": True}),
            "arif_memory_recall": lambda s: (True, {"memory_id": self.state.get("memory_id", "")}),
            "arif_kernel_route": lambda s: (True, {"continue_flag": True}),
            "arif_ops_measure": lambda s: (True, {"status": "healthy"}),
            "arif_judge_deliberate": lambda s: (True, {"verdict": "SEAL"}),
            "arif_vault_seal": lambda s: (True, {"entry_id": self.state.get("entry_id", "")}),
            "internal": lambda s: (True, {"tool": "internal"}),
        }
        if tool in handlers:
            try:
                success, output = handlers[tool](step)
                return success, output
            except Exception as e:
                return False, {"error": str(e)}
        return False, {"error": "unknown tool: " + tool}

    def _write_artifact(self, step_id: str, data: dict):
        self.base.joinpath("artifacts").mkdir(exist_ok=True)
        p = self.base / "artifacts" / (step_id + ".json")
        with open(p, "w") as f:
            json.dump(data, f, indent=2)
        self.state["artifacts"][step_id] = str(p)
        self._save_state()

    def _check_voids(self, step: dict, output: Any) -> tuple[bool, list]:
        voids = step.get("void_conditions", [])
        triggered = [v for v in voids if v in str(output)]
        return len(triggered) == 0, triggered

    def _resolve_branch(self, step: dict, output: Any) -> str | None:
        branch = step.get("branch", {})
        if not branch:
            return None
        out_str = str(output).lower()
        if "worked" in out_str:
            is_worked = "true" in out_str or '"worked": true' in str(output).lower()
            if step["step_id"] == "step-05":
                if is_worked:
                    self.state["reflect_attempts"] = self.state.get("reflect_attempts", 0) + 1
                    self._save_state()
                    print("    🔄 REFLECT loop #" + str(self.state["reflect_attempts"]))
                    if self.state["reflect_attempts"] >= 3:
                        print("    🚨 LOOP GUARD: " + str(self.state["reflect_attempts"]) + " REFLECT attempts — 888_HOLD")
                        return None
                    for k in branch:
                        if "continue" in k or "worked" in k:
                            return k
                    return list(branch.values())[0]
                else:
                    self.state["reflect_attempts"] = 0
                    self._save_state()
                    print("    ✅ REFLECT worked=False — counter reset")
                    for k in branch:
                        if "exit" in k or "failed" in k:
                            return k
                    return list(branch.values())[-1]
        if "alternative" in out_str:
            if "none" in out_str:
                return branch.get("no_alternative", list(branch.values())[-1])
            return branch.get("has_alternative", list(branch.values())[0])
        return list(branch.values())[0]

    def _find_step_idx(self, step_id: str) -> int:
        return next((i for i, s in enumerate(self.plan["steps"]) if s["step_id"] == step_id), 0)

    def execute(self) -> dict:
        print("\n=== TREE777 Engine v1.3.0 ===")
        print("Workflow: " + self.workflow_id + " | Dry: " + str(self.dry_run) + " | Resume: " + str(self.resume))
        print("Steps: " + str(len(self.plan["steps"])) + " | Risk: " + self.plan.get("risk_band", "?"))

        step_idx = 0
        if self.resume:
            last_completed = None
            for s in self.plan["steps"]:
                g = self._read_gate(s["step_id"])
                if g.get("passed") == True:
                    last_completed = s["step_id"]
            if last_completed:
                step_idx = self._find_step_idx(last_completed) + 1
                self.state["completed_steps"] = [
                    s["step_id"] for s in self.plan["steps"]
                    if self._read_gate(s["step_id"]).get("passed") == True
                ]
                print("\nResume: last=" + str(last_completed) + ", next_idx=" + str(step_idx))

        max_iter = len(self.plan["steps"]) * 3 + 3
        for iteration in range(max_iter):
            if step_idx >= len(self.plan["steps"]):
                self.state["status"] = "completed"
                self._save_state()
                n = str(len(self.state["completed_steps"]))
                print("\n✅ COMPLETED — " + n + " steps")
                return self.state

            step = self.plan["steps"][step_idx]
            step_id = step["step_id"]
            # Loop guard: block re-execution of non-REFLECT completed steps
            # IMPORTANT: step-05 REFLECT is DESIGNED to loop — don't block it
            if step_id in self.state.get("completed_steps", []) and iteration > 0:
                if step_id == "step-05":
                    # REFLECT is designed to loop — let it run, reflect_attempts counter governs it
                    pass
                else:
                    print("    🚨 LOOP DETECTED: re-executing completed step " + step_id + ", escalating")
                    self.state["status"] = "hold"
                    self.state["hold_reason"] = "loop_guard_reexecute_" + step_id
                    self._save_state()
                    return self.state

            gate = self._read_gate(step_id)
            if gate.get("passed") == True and not self.resume:
                step_idx += 1
                continue

            print("\n[" + step_id + "] " + step["name"])
            gate["status"] = "entered"
            gate["entered_at"] = self._now()
            self._write_gate(step_id, gate)

            success, output = self._run_step(step)
            void_ok, voids = self._check_voids(step, output)
            verified, verify_msg = self._verify(step)

            gate["verified_at"] = self._now()
            gate["verification_output"] = verify_msg
            gate["step_output"] = output

            if success and void_ok and verified:
                gate["passed"] = True
                gate["status"] = "passed"
                if step_id not in self.state["completed_steps"]:
                    self.state["completed_steps"].append(step_id)
                self.state["current_step"] = step_id
                print("    ✅ PASS — " + verify_msg)

                if "branch" in step:
                    target = self._resolve_branch(step, output)
                    if target is None:
                        n = str(self.state.get("reflect_attempts", 0))
                        self.state["status"] = "hold"
                        self.state["hold_reason"] = "D3_loop_guard_REFLECT_" + n + "_exceeded_3"
                        self._save_state()
                        return self.state
                    target_idx = self._find_step_idx(target)
                    print("    → BRANCH → [" + target + "]")
                    step_idx = target_idx
                else:
                    step_idx += 1

                self._write_gate(step_id, gate)
            else:
                print("    ❌ FAIL — " + verify_msg)
                if voids:
                    print("       Voids: " + str(voids))
                gate["passed"] = False
                gate["status"] = "failed"
                gate["voids_triggered"] = voids

                if "branch" in step:
                    target = step["branch"].get("failed", list(step["branch"].values())[-1])
                    target_idx = self._find_step_idx(target)
                    print("    → FAIL-BRANCH → [" + target + "]")
                    step_idx = target_idx
                    self._write_gate(step_id, gate)
                    continue

                retry = step.get("retry_budget", 0)
                if gate.get("retry_count", 0) < retry:
                    gate["retry_count"] = gate.get("retry_count", 0) + 1
                    print("    ⚠️ RETRY " + str(gate["retry_count"]) + "/" + str(retry))
                    self._write_gate(step_id, gate)
                    continue

                if step.get("escalation") == "888_HOLD":
                    print("    🚨 888_HOLD")
                    self.state["status"] = "hold"
                    self._save_state()
                    return self.state

                self.state["status"] = "failed"
                self._save_state()
                return self.state

        self.state["status"] = "failed"
        self.state["error_log"].append("max iterations reached")
        self._save_state()
        return self.state


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: tree777_executor.py <workflow_id> [--resume] [--dry-run]")
        sys.exit(1)
    wf = sys.argv[1]
    engine = WorkflowEngine(wf, dry_run="--dry-run" in sys.argv, resume="--resume" in sys.argv)
    result = engine.execute()
    print("\nFinal: " + result["status"] + " | Steps: " + str(len(result.get("completed_steps", []))))
    sys.exit(0 if result["status"] == "completed" else 1)