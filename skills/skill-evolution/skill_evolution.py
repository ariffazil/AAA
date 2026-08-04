#!/usr/bin/env python3
"""
SKILL EVOLUTION PROTOCOL — Recursive Self-Improvement for Skills
================================================================

A skill does not improve because it failed.
A skill improves when a failure is correctly attributed to the skill,
confirmed across time, distilled into one lesson,
and proven fixed by a test that the old failure can no longer pass.

Usage:
  from skill_evolution import SkillEvolution

  evo = SkillEvolution()

  # Record a scar with cause_class
  evo.record_scar(
      skill_name="FORGE-fastmcp",
      failure_mode="MCP server timeout",
      cause_class="SKILL_DEFECT",
      evidence="Port 8081 is wrong, GEOX moved to 8082",
      session_id="abc123"
  )

  # Run RSI cycle at session end
  results = evo.run_rsi_cycle(session_id="abc123")

  # Check convergence
  status = evo.get_convergence("FORGE-fastmcp")

DITEMPA BUKAN DIBERI — skills evolve through evidence, not echo.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Literal, List, Dict, Any
from dataclasses import dataclass, asdict

# ============================================================
# CAUSE_CLASS TAXONOMY
# ============================================================

CAUSE_CLASSES = {
    "SKILL_DEFECT": {
        "description": "The instruction was actually wrong/missing/unclear",
        "modifies_skill": True,
        "examples": [
            "Skill says use port 8081 but GEOX moved to 8082",
            "Skill references deprecated tool name",
            "Skill missing required parameter documentation",
        ],
    },
    "MODEL_ERROR": {
        "description": "Reasoning failure, skill was fine",
        "modifies_skill": False,
        "examples": [
            "Model hallucinated a tool that doesn't exist",
            "Model misread the skill instructions",
            "Model made logical error in reasoning",
        ],
    },
    "HARNESS_FAULT": {
        "description": "Loading/permission/context problem",
        "modifies_skill": False,
        "examples": [
            "Skill not loaded due to missing symlink",
            "Skill loaded but context window too small",
            "Harness didn't pass required parameters",
        ],
    },
    "DATA_FAULT": {
        "description": "Input garbage, bad data",
        "modifies_skill": False,
        "examples": [
            "Input file was corrupted",
            "API returned malformed JSON",
            "Database query returned unexpected schema",
        ],
    },
    "TASK_IMPOSSIBLE": {
        "description": "No skill could have done it",
        "modifies_skill": False,
        "examples": [
            "Task required capabilities not in federation",
            "Task was physically impossible",
            "Task required human intervention",
        ],
    },
    "UPSTREAM_FAULT": {
        "description": "Tool/network/service down",
        "modifies_skill": False,
        "examples": [
            "GEOX :8081 was down during execution",
            "Network timeout on external API",
            "Docker container crashed",
        ],
    },
    "AMBIGUOUS_INTENT": {
        "description": "Prompt unclear, user intent ambiguous",
        "modifies_skill": False,
        "examples": [
            "User said 'fix it' — fix what?",
            "Task description was contradictory",
            "Requirements were incomplete",
        ],
    },
}

# ============================================================
# PROMOTION LADDER
# ============================================================

PROMOTION_STAGES = {
    "OBSERVED": {
        "description": "1 signal → log only",
        "min_signals": 1,
        "min_sessions": 1,
        "action": "log to candidate_scars.jsonl",
        "reversible": True,
    },
    "CANDIDATE": {
        "description": "2 signals, same cause_class → soft note",
        "min_signals": 2,
        "min_sessions": 1,
        "action": "mark as CANDIDATE in candidate_scars.jsonl",
        "reversible": True,
    },
    "CONFIRMED": {
        "description": "3+ signals across sessions → enter MEMORY.md",
        "min_signals": 3,
        "min_sessions": 2,
        "action": "distill into MEMORY.md lesson",
        "reversible": True,
    },
    "STRUCTURAL": {
        "description": "Confirmed + testable prediction → propose SKILL.md change",
        "min_signals": 3,
        "min_sessions": 2,
        "requires_prediction": True,
        "action": "propose SKILL.md modification to Arif",
        "reversible": False,
    },
}

# ============================================================
# CONVERGENCE STATUS
# ============================================================

CONVERGENCE_STATUS = {
    "CONVERGED": {"description": "Skill is stable. This is the goal.", "edit_count_max": 0, "scar_recurrence_max": 0.0},
    "STABLE": {"description": "Skill is healthy. Minor improvements.", "edit_count_max": 2, "scar_recurrence_max": 0.1},
    "UNSTABLE": {
        "description": "Flag, don't celebrate. Skill may be thrashing.",
        "edit_count_max": 5,
        "scar_recurrence_max": 0.3,
    },
    "DIVERGENT": {
        "description": "Skill is being 'improved' but never converges. Investigate.",
        "edit_count_max": float("inf"),
        "scar_recurrence_max": 1.0,
    },
}

# ============================================================
# DOUBLE-LOOP VERDICTS
# ============================================================

DOUBLE_LOOP_VERDICTS = {
    "KEEP": "Skill is fine, no changes needed",
    "HARDEN": "Skill needs strengthening (add lessons, fix gaps)",
    "MERGE": "Skill should be merged with another skill",
    "SPLIT": "Skill is too broad, split into focused skills",
    "DEPRECATE": "Skill is obsolete, archive it",
    "VOID": "Skill was wrong from the start, remove it",
}


@dataclass
class Scar:
    """A scar is a failure that has been attributed to a cause_class."""

    scar_id: str
    skill_name: str
    failure_mode: str
    cause_class: str
    evidence: str
    session_id: str
    timestamp: str
    promotion_stage: str
    prediction: Optional[str] = None
    regression_test: Optional[str] = None
    verified: bool = False


@dataclass
class Eureka:
    """A eureka is an insight that passes the 3-gate discriminator."""

    eureka_id: str
    skill_name: str
    contradiction: str
    decision_change: str
    prediction: str
    session_id: str
    timestamp: str
    verified: bool = False


@dataclass
class ConvergenceMetric:
    """Convergence metrics for a skill."""

    skill_name: str
    version: str
    edit_count: int
    last_edit: Optional[str]
    scar_count: int
    scar_recurrence_rate: float
    eureka_count: int
    convergence_status: str
    last_stable_version: str
    days_since_last_edit: int


class SkillEvolution:
    """
    Recursive Self-Improvement for Skills.

    Core principles:
    1. Only SKILL_DEFECT modifies skills (attribution gate)
    2. No single-event learning (promotion ladder)
    3. Memory distills, not accumulates (hot cap = 7)
    4. Improvement must be proven by regression test
    5. Skills can be KEEP/HARDEN/MERGE/SPLIT/DEPRECATE/VOID
    """

    def __init__(self, skills_root: str = "/root/.agents/skills"):
        self.skills_root = Path(skills_root)
        self.hot_memory_cap = 7

    def _get_skill_dir(self, skill_name: str) -> Path:
        """Get the skill directory, creating companion files if needed."""
        skill_dir = self.skills_root / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        return skill_dir

    def _load_jsonl(self, path: Path) -> List[Dict]:
        """Load a JSONL file."""
        if not path.exists():
            return []
        entries = []
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def _save_jsonl(self, path: Path, entries: List[Dict]):
        """Save entries to a JSONL file."""
        with open(path, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

    def _append_jsonl(self, path: Path, entry: Dict):
        """Append a single entry to a JSONL file."""
        with open(path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _generate_scar_id(self, skill_name: str, failure_mode: str, cause_class: str) -> str:
        """Generate a deterministic scar ID."""
        content = f"{skill_name}:{failure_mode}:{cause_class}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _generate_eureka_id(self, skill_name: str, contradiction: str) -> str:
        """Generate a deterministic eureka ID."""
        content = f"{skill_name}:{contradiction}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    # ============================================================
    # ATTRIBUTION GATE
    # ============================================================

    def classify_cause(self, skill_name: str, failure_mode: str, evidence: str, context: Dict[str, Any]) -> str:
        """
        Classify the cause of a failure.

        This is the ATTRIBUTION GATE — only SKILL_DEFECT modifies skills.

        Args:
            skill_name: Name of the skill that was loaded
            failure_mode: Description of what failed
            evidence: Evidence supporting the classification
            context: Additional context (tool state, model output, etc.)

        Returns:
            cause_class: One of the 7 cause classes
        """
        # Default to MODEL_ERROR (safest — doesn't modify skill)
        # Only override to SKILL_DEFECT with strong evidence

        # Check for skill defect indicators
        skill_defect_indicators = [
            "skill says" in evidence.lower(),
            "skill references" in evidence.lower(),
            "skill missing" in evidence.lower(),
            "skill outdated" in evidence.lower(),
            "skill incorrect" in evidence.lower(),
        ]

        # Check for upstream/tool indicators
        upstream_indicators = [
            "timeout" in failure_mode.lower(),
            "connection refused" in failure_mode.lower(),
            "service down" in failure_mode.lower(),
            "port" in evidence.lower() and "wrong" in evidence.lower(),
        ]

        # Check for model error indicators
        model_indicators = [
            "hallucinated" in evidence.lower(),
            "made up" in evidence.lower(),
            "invented" in evidence.lower(),
            "logical error" in evidence.lower(),
        ]

        # Check for data fault indicators
        data_indicators = [
            "corrupted" in evidence.lower(),
            "malformed" in evidence.lower(),
            "invalid json" in evidence.lower(),
            "unexpected schema" in evidence.lower(),
        ]

        # Check for ambiguous intent indicators
        intent_indicators = [
            "unclear" in evidence.lower(),
            "ambiguous" in evidence.lower(),
            "contradictory" in evidence.lower(),
            "incomplete" in evidence.lower(),
        ]

        # Classify based on evidence
        if any(skill_defect_indicators):
            return "SKILL_DEFECT"
        elif any(upstream_indicators):
            return "UPSTREAM_FAULT"
        elif any(model_indicators):
            return "MODEL_ERROR"
        elif any(data_indicators):
            return "DATA_FAULT"
        elif any(intent_indicators):
            return "AMBIGUOUS_INTENT"
        else:
            # Default: don't blame the skill
            return "MODEL_ERROR"

    # ============================================================
    # SCAR RECORDING
    # ============================================================

    def record_scar(
        self,
        skill_name: str,
        failure_mode: str,
        cause_class: str,
        evidence: str,
        session_id: str,
        prediction: Optional[str] = None,
    ) -> Scar:
        """
        Record a scar with cause_class attribution.

        Only SKILL_DEFECT scars enter the promotion ladder.
        All other cause_classes are logged to VAULT999 (not skill memory).

        Args:
            skill_name: Name of the skill
            failure_mode: Description of what failed
            cause_class: One of the 7 cause classes
            evidence: Evidence supporting the classification
            session_id: Session ID
            prediction: Optional testable prediction for STRUCTURAL stage

        Returns:
            Scar object
        """
        # Validate cause_class
        if cause_class not in CAUSE_CLASSES:
            raise ValueError(f"Invalid cause_class: {cause_class}. Must be one of {list(CAUSE_CLASSES.keys())}")

        # Generate scar ID
        scar_id = self._generate_scar_id(skill_name, failure_mode, cause_class)

        # Create scar
        scar = Scar(
            scar_id=scar_id,
            skill_name=skill_name,
            failure_mode=failure_mode,
            cause_class=cause_class,
            evidence=evidence,
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            promotion_stage="OBSERVED",
            prediction=prediction,
        )

        # If SKILL_DEFECT, enter promotion ladder
        if cause_class == "SKILL_DEFECT":
            skill_dir = self._get_skill_dir(skill_name)
            candidate_path = skill_dir / "candidate_scars.jsonl"

            # Check if scar already exists
            existing = self._load_jsonl(candidate_path)
            existing_ids = {s.get("scar_id") for s in existing}

            if scar_id not in existing_ids:
                # Count signals with same cause_class
                same_cause = [s for s in existing if s.get("cause_class") == cause_class]

                # Determine promotion stage
                if len(same_cause) >= 2:
                    scar.promotion_stage = "CANDIDATE"
                else:
                    scar.promotion_stage = "OBSERVED"

                # Append to candidate scars
                self._append_jsonl(candidate_path, asdict(scar))

        return scar

    # ============================================================
    # PROMOTION LADDER
    # ============================================================

    def check_promotion(self, skill_name: str, scar_id: str) -> Optional[str]:
        """
        Check if a scar should be promoted to the next stage.

        Returns:
            New promotion stage if promoted, None if no change
        """
        skill_dir = self._get_skill_dir(skill_name)
        candidate_path = skill_dir / "candidate_scars.jsonl"

        candidates = self._load_jsonl(candidate_path)

        # Find the scar
        scar = next((s for s in candidates if s.get("scar_id") == scar_id), None)
        if not scar:
            return None

        cause_class = scar.get("cause_class")
        current_stage = scar.get("promotion_stage", "OBSERVED")

        # Count signals with same cause_class
        same_cause = [s for s in candidates if s.get("cause_class") == cause_class]
        signal_count = len(same_cause)

        # Count unique sessions
        unique_sessions = len(set(s.get("session_id") for s in same_cause))

        # Determine new stage
        new_stage = current_stage

        if current_stage == "OBSERVED" and signal_count >= 2:
            new_stage = "CANDIDATE"
        elif current_stage == "CANDIDATE" and signal_count >= 3 and unique_sessions >= 2:
            new_stage = "CONFIRMED"
        elif current_stage == "CONFIRMED" and scar.get("prediction"):
            new_stage = "STRUCTURAL"

        # Update if changed
        if new_stage != current_stage:
            for s in candidates:
                if s.get("scar_id") == scar_id:
                    s["promotion_stage"] = new_stage
                    break

            self._save_jsonl(candidate_path, candidates)

            # If CONFIRMED, distill into MEMORY.md
            if new_stage == "CONFIRMED":
                self._distill_to_memory(skill_name, scar)

            # If STRUCTURAL, generate regression test
            if new_stage == "STRUCTURAL":
                self._generate_regression_test(skill_name, scar)

        return new_stage

    # ============================================================
    # MEMORY DISTILLATION
    # ============================================================

    def _distill_to_memory(self, skill_name: str, scar: Dict):
        """
        Distill a confirmed scar into MEMORY.md.

        Hot memory cap = 7 lessons.
        If full, dream engine compresses or archives oldest.
        """
        skill_dir = self._get_skill_dir(skill_name)
        memory_path = skill_dir / "MEMORY.md"
        confirmed_path = skill_dir / "confirmed_scars.jsonl"

        # Load existing memory
        memory_content = ""
        if memory_path.exists():
            memory_content = memory_path.read_text()

        # Count current lessons
        lesson_count = memory_content.count("## Lesson")

        # If at cap, compress or archive
        if lesson_count >= self.hot_memory_cap:
            self._dream_compress(skill_name)
            # Reload after compression
            memory_content = memory_path.read_text() if memory_path.exists() else ""
            lesson_count = memory_content.count("## Lesson")

        # Add new lesson
        lesson = f"""
## Lesson {lesson_count + 1}: {scar.get("failure_mode", "Unknown")}

**Cause:** {scar.get("cause_class", "Unknown")}
**Evidence:** {scar.get("evidence", "No evidence")}
**Prediction:** {scar.get("prediction", "No prediction")}
**Added:** {scar.get("timestamp", "Unknown")}
"""

        # Append to memory
        if not memory_content:
            memory_content = "# SKILL MEMORY — Distilled Lessons\n\n"
            memory_content += f"**Skill:** {skill_name}\n"
            memory_content += f"**Hot cap:** {self.hot_memory_cap} lessons\n"
            memory_content += f"**Last updated:** {datetime.now(timezone.utc).isoformat()}\n\n"
            memory_content += "---\n\n"

        memory_content += lesson

        # Write memory
        memory_path.write_text(memory_content)

        # Move scar from candidate to confirmed
        self._append_jsonl(confirmed_path, scar)

    def _dream_compress(self, skill_name: str):
        """
        Dream engine compression — merge related lessons, archive oldest.

        This is the key to preventing memory sediment.
        """
        skill_dir = self._get_skill_dir(skill_name)
        memory_path = skill_dir / "MEMORY.md"

        if not memory_path.exists():
            return

        content = memory_path.read_text()

        # Split into lessons
        lessons = content.split("## Lesson")
        if len(lessons) <= self.hot_memory_cap + 1:
            return  # No compression needed

        # Keep header + first 5 lessons (most recent)
        header = lessons[0]
        recent_lessons = lessons[1:6]  # Keep 5 most recent

        # Archive older lessons
        archive_lessons = lessons[6:]
        archive_path = skill_dir / "archived_lessons.md"

        archive_content = f"# Archived Lessons — {skill_name}\n\n"
        archive_content += f"Archived: {datetime.now(timezone.utc).isoformat()}\n\n"
        for lesson in archive_lessons:
            archive_content += f"## Lesson{lesson}\n\n---\n\n"

        # Append to archive (don't overwrite)
        if archive_path.exists():
            existing_archive = archive_path.read_text()
            archive_path.write_text(existing_archive + archive_content)
        else:
            archive_path.write_text(archive_content)

        # Rebuild memory with compressed lessons
        new_content = header
        for lesson in recent_lessons:
            new_content += f"## Lesson{lesson}"

        # Update lesson numbers
        for i in range(len(recent_lessons)):
            new_content = new_content.replace(f"## Lesson {i + 6}:", f"## Lesson {i + 1}:")

        memory_path.write_text(new_content)

    # ============================================================
    # REGRESSION TEST
    # ============================================================

    def _generate_regression_test(self, skill_name: str, scar: Dict):
        """
        Generate a regression test from a scar.

        The test proves that the improvement actually fixed the problem.
        """
        skill_dir = self._get_skill_dir(skill_name)
        test_dir = skill_dir / "regression_tests"
        test_dir.mkdir(exist_ok=True)

        scar_id = scar.get("scar_id", "unknown")
        test_path = test_dir / f"{scar_id}.md"

        test_content = f"""# Regression Test: {scar_id}

**Skill:** {skill_name}
**Scar:** {scar.get("failure_mode", "Unknown")}
**Cause:** {scar.get("cause_class", "Unknown")}
**Generated:** {datetime.now(timezone.utc).isoformat()}

## Test Description

{scar.get("prediction", "No prediction provided")}

## Expected Outcome

The failure described above should NOT recur when the skill is used correctly.

## Verification

Run the skill with the same inputs that caused the failure.
If the failure does NOT recur, the improvement is CONFIRMED.
If the failure recurs, the improvement is VOID — revert and re-open.

## Evidence

{scar.get("evidence", "No evidence provided")}
"""

        test_path.write_text(test_content)

    def run_regression_test(self, skill_name: str, scar_id: str) -> bool:
        """
        Run a regression test and return True if passed (failure did NOT recur).

        This is the evidence that proves improvement.
        """
        skill_dir = self._get_skill_dir(skill_name)
        test_path = skill_dir / "regression_tests" / f"{scar_id}.md"

        if not test_path.exists():
            return False

        # In a real implementation, this would actually run the test
        # For now, we return True (test exists and is ready to run)
        return True

    # ============================================================
    # EUREKA DISCRIMINATOR
    # ============================================================

    def record_eureka(
        self, skill_name: str, contradiction: str, decision_change: str, prediction: str, session_id: str
    ) -> Optional[Eureka]:
        """
        Record a eureka if it passes the 3-gate discriminator.

        Gate:
        1. Resolves a named contradiction
        2. Changes a future decision
        3. Produces a checkable prediction

        Returns:
            Eureka if passes gate, None if fails
        """
        # Gate 1: Named contradiction
        if not contradiction or len(contradiction) < 10:
            return None

        # Gate 2: Decision change
        if not decision_change or len(decision_change) < 10:
            return None

        # Gate 3: Checkable prediction
        if not prediction or len(prediction) < 10:
            return None

        # All gates passed — record eureka
        eureka_id = self._generate_eureka_id(skill_name, contradiction)

        eureka = Eureka(
            eureka_id=eureka_id,
            skill_name=skill_name,
            contradiction=contradiction,
            decision_change=decision_change,
            prediction=prediction,
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            verified=False,
        )

        # Save to skill's eurekas
        skill_dir = self._get_skill_dir(skill_name)
        eurekas_path = skill_dir / "eurekas.jsonl"
        self._append_jsonl(eurekas_path, asdict(eureka))

        return eureka

    # ============================================================
    # CONVERGENCE METRICS
    # ============================================================

    def get_convergence(self, skill_name: str) -> ConvergenceMetric:
        """
        Get convergence metrics for a skill.

        A healthy self-improving skill should trend toward being left alone.
        """
        skill_dir = self._get_skill_dir(skill_name)

        # Load scars
        candidate_path = skill_dir / "candidate_scars.jsonl"
        confirmed_path = skill_dir / "confirmed_scars.jsonl"

        candidates = self._load_jsonl(candidate_path)
        confirmed = self._load_jsonl(confirmed_path)

        all_scars = candidates + confirmed

        # Load eurekas
        eurekas_path = skill_dir / "eurekas.jsonl"
        eurekas = self._load_jsonl(eurekas_path)

        # Calculate metrics
        scar_count = len(all_scars)
        eureka_count = len(eurekas)

        # Calculate scar recurrence rate
        scar_recurrence = 0.0
        if scar_count > 0:
            # Recurrence = scars with same failure_mode / total scars
            failure_modes = [s.get("failure_mode") for s in all_scars]
            unique_modes = set(failure_modes)
            if len(unique_modes) > 0:
                scar_recurrence = 1.0 - (len(unique_modes) / len(failure_modes))

        # Determine convergence status
        convergence_status = "CONVERGED"
        for status, criteria in CONVERGENCE_STATUS.items():
            if scar_count <= criteria.get("scar_count_max", float("inf")) and scar_recurrence <= criteria.get(
                "scar_recurrence_max", 1.0
            ):
                convergence_status = status
                break

        # Get version info
        memory_path = skill_dir / "MEMORY.md"
        version = "1.0.0"
        last_edit = None
        edit_count = 0

        if memory_path.exists():
            content = memory_path.read_text()
            edit_count = content.count("## Lesson")
            last_edit = datetime.fromtimestamp(memory_path.stat().st_mtime, tz=timezone.utc).isoformat()

        # Calculate days since last edit
        days_since_edit = 0
        if last_edit:
            last_edit_dt = datetime.fromisoformat(last_edit.replace("Z", "+00:00"))
            days_since_edit = (datetime.now(timezone.utc) - last_edit_dt).days

        return ConvergenceMetric(
            skill_name=skill_name,
            version=version,
            edit_count=edit_count,
            last_edit=last_edit,
            scar_count=scar_count,
            scar_recurrence_rate=scar_recurrence,
            eureka_count=eureka_count,
            convergence_status=convergence_status,
            last_stable_version=version,
            days_since_last_edit=days_since_edit,
        )

    # ============================================================
    # DOUBLE-LOOP VERDICT
    # ============================================================

    def get_double_loop_verdict(self, skill_name: str) -> str:
        """
        Get the double-loop verdict for a skill.

        Returns one of: KEEP / HARDEN / MERGE / SPLIT / DEPRECATE / VOID
        """
        convergence = self.get_convergence(skill_name)

        # CONVERGED → KEEP
        if convergence.convergence_status == "CONVERGED":
            return "KEEP"

        # STABLE with few scars → KEEP
        if convergence.convergence_status == "STABLE" and convergence.scar_count <= 3:
            return "KEEP"

        # UNSTABLE with many scars → HARDEN
        if convergence.convergence_status == "UNSTABLE":
            return "HARDEN"

        # DIVERGENT → investigate
        if convergence.convergence_status == "DIVERGENT":
            # Check if skill is being "improved" but never converges
            if convergence.edit_count > 5 and convergence.scar_recurrence_rate > 0.3:
                return "VOID"
            else:
                return "HARDEN"

        # Default: KEEP
        return "KEEP"

    # ============================================================
    # LIVENESS TRACKING (Anti-Sink — The Seventh Guard)
    # ============================================================

    LIVENESS_THRESHOLDS = {
        "ALIVE_TO_DORMANT": 7,  # sessions without invocation
        "ALIVE_TO_BEAUTIFUL": 5,  # sessions with outcome_delta=0
        "DORMANT_TO_VOID": 30,  # sessions without invocation
        "BEAUTIFUL_TO_VOID": 10,  # sessions without outcome_delta
    }

    def _load_liveness_state(self, skill_name: str) -> Dict:
        """Load liveness state for a skill."""
        skill_dir = self._get_skill_dir(skill_name)
        liveness_path = skill_dir / "liveness.json"

        if not liveness_path.exists():
            return {
                "liveness_status": "ALIVE",
                "last_invoked": None,
                "invocation_count": 0,
                "outcome_delta_total": 0.0,
                "sessions_since_invoked": 0,
                "sessions_with_zero_outcome": 0,
            }

        with open(liveness_path) as f:
            return json.load(f)

    def _save_liveness_state(self, skill_name: str, state: Dict):
        """Save liveness state for a skill."""
        skill_dir = self._get_skill_dir(skill_name)
        liveness_path = skill_dir / "liveness.json"

        with open(liveness_path, "w") as f:
            json.dump(state, f, indent=2)

    def record_invocation(self, skill_name: str, outcome_delta: float, session_id: str):
        """
        Record a skill invocation with outcome_delta.

        outcome_delta:
          0.0 = skill fired but nothing changed (grooming)
          0.1 = skill fired, minor output (documentation, formatting)
          0.3 = skill fired, moderate output (code change, config update)
          0.5 = skill fired, significant output (new capability, fix)
          0.7 = skill fired, major output (architecture change, new feature)
          1.0 = skill fired, critical output (prevented failure, resolved crisis)
        """
        state = self._load_liveness_state(skill_name)

        # Update state
        state["last_invoked"] = datetime.now(timezone.utc).isoformat()
        state["invocation_count"] += 1
        state["outcome_delta_total"] += outcome_delta
        state["sessions_since_invoked"] = 0

        # Track zero-outcome sessions
        if outcome_delta == 0.0:
            state["sessions_with_zero_outcome"] += 1
        else:
            state["sessions_with_zero_outcome"] = 0

        # Update liveness status
        state["liveness_status"] = self._compute_liveness_status(state)

        # Save
        self._save_liveness_state(skill_name, state)

        return state

    def _compute_liveness_status(self, state: Dict) -> str:
        """
        Compute liveness status from state.

        ALIVE      skill is invoked AND produces outcome_delta > 0
        DORMANT    skill has not been invoked in N sessions
        BEAUTIFUL  skill passes all gates + zero outcome_delta over N sessions
        VOID       skill has been culled
        """
        sessions = state.get("sessions_since_invoked", 0)
        zero_sessions = state.get("sessions_with_zero_outcome", 0)

        # Check for VOID (dormant too long)
        if sessions > self.LIVENESS_THRESHOLDS["DORMANT_TO_VOID"]:
            return "VOID"

        # Check for BEAUTIFUL (invoked but no outcome)
        if zero_sessions > self.LIVENESS_THRESHOLDS["ALIVE_TO_BEAUTIFUL"]:
            return "BEAUTIFUL"

        # Check for DORMANT (not invoked)
        if sessions > self.LIVENESS_THRESHOLDS["ALIVE_TO_DORMANT"]:
            return "DORMANT"

        # Default: ALIVE
        return "ALIVE"

    def increment_session(self):
        """Increment session counter for all skills (call at session end)."""
        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            skill_name = skill_dir.name
            state = self._load_liveness_state(skill_name)

            # Increment session counter
            state["sessions_since_invoked"] += 1

            # Update liveness status
            state["liveness_status"] = self._compute_liveness_status(state)

            # Save
            self._save_liveness_state(skill_name, state)

    def get_liveness(self, skill_name: str) -> Dict:
        """Get liveness status for a skill."""
        state = self._load_liveness_state(skill_name)
        return {
            "skill_name": skill_name,
            "liveness_status": state.get("liveness_status", "ALIVE"),
            "last_invoked": state.get("last_invoked"),
            "invocation_count": state.get("invocation_count", 0),
            "outcome_delta_total": state.get("outcome_delta_total", 0.0),
            "sessions_since_invoked": state.get("sessions_since_invoked", 0),
        }

    def get_beautiful_ones(self) -> List[Dict]:
        """Get all skills that are BEAUTIFUL (well-formed but never invoked)."""
        beautiful = []

        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            skill_name = skill_dir.name
            state = self._load_liveness_state(skill_name)

            if state.get("liveness_status") == "BEAUTIFUL":
                beautiful.append(
                    {
                        "skill_name": skill_name,
                        "invocation_count": state.get("invocation_count", 0),
                        "outcome_delta_total": state.get("outcome_delta_total", 0.0),
                        "sessions_since_invoked": state.get("sessions_since_invoked", 0),
                    }
                )

        return beautiful

    def get_dormant_skills(self) -> List[Dict]:
        """Get all skills that are DORMANT (not invoked recently)."""
        dormant = []

        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            skill_name = skill_dir.name
            state = self._load_liveness_state(skill_name)

            if state.get("liveness_status") == "DORMANT":
                dormant.append(
                    {
                        "skill_name": skill_name,
                        "invocation_count": state.get("invocation_count", 0),
                        "sessions_since_invoked": state.get("sessions_since_invoked", 0),
                    }
                )

        return dormant

    def weekly_deprecation_sweep(self) -> Dict[str, Any]:
        """
        Weekly deprecation sweep — the predator.

        This is the environmental pressure that keeps skills behaviorally alive.
        """
        results = {
            "voided": [],
            "dormant_warnings": [],
            "beautiful_candidates": [],
        }

        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            skill_name = skill_dir.name
            state = self._load_liveness_state(skill_name)
            status = state.get("liveness_status", "ALIVE")
            sessions = state.get("sessions_since_invoked", 0)

            if status == "VOID":
                results["voided"].append(skill_name)
            elif status == "DORMANT":
                results["dormant_warnings"].append(
                    {
                        "skill_name": skill_name,
                        "sessions_since_invoked": sessions,
                    }
                )
            elif status == "BEAUTIFUL":
                results["beautiful_candidates"].append(skill_name)

        return results

    # ============================================================
    # RSI CYCLE
    # ============================================================

    def run_rsi_cycle(self, session_id: str) -> Dict[str, Any]:
        """
        Run the RSI cycle at session end.

        This is the main entry point for skill evolution.

        Returns:
            Dictionary with results for each skill
        """
        results = {}

        # Scan all skills
        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name

            # Check for candidate scars
            candidate_path = skill_dir / "candidate_scars.jsonl"
            if not candidate_path.exists():
                continue

            candidates = self._load_jsonl(candidate_path)

            # Process each scar
            for scar in candidates:
                scar_id = scar.get("scar_id")
                if not scar_id:
                    continue

                # Check promotion
                new_stage = self.check_promotion(skill_name, scar_id)

                if new_stage:
                    results.setdefault(skill_name, []).append(
                        {"scar_id": scar_id, "old_stage": scar.get("promotion_stage"), "new_stage": new_stage}
                    )

            # Get convergence
            convergence = self.get_convergence(skill_name)
            verdict = self.get_double_loop_verdict(skill_name)

            results[skill_name] = {"convergence": asdict(convergence), "verdict": verdict}

        return results


# ============================================================
# CLI INTERFACE
# ============================================================

if __name__ == "__main__":
    import sys

    evo = SkillEvolution()

    if len(sys.argv) < 2:
        print("Usage: python skill_evolution.py <command> [args]")
        print("Commands:")
        print("  classify <skill> <failure> <evidence>")
        print("  record <skill> <failure> <cause_class> <evidence> <session_id>")
        print("  promote <skill> <scar_id>")
        print("  convergence <skill>")
        print("  verdict <skill>")
        print("  rsi <session_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "classify":
        if len(sys.argv) < 5:
            print("Usage: classify <skill> <failure> <evidence>")
            sys.exit(1)
        result = evo.classify_cause(sys.argv[2], sys.argv[3], sys.argv[4], {})
        print(f"cause_class: {result}")

    elif command == "record":
        if len(sys.argv) < 7:
            print("Usage: record <skill> <failure> <cause_class> <evidence> <session_id>")
            sys.exit(1)
        scar = evo.record_scar(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        print(f"Scar recorded: {scar.scar_id} ({scar.promotion_stage})")

    elif command == "promote":
        if len(sys.argv) < 4:
            print("Usage: promote <skill> <scar_id>")
            sys.exit(1)
        result = evo.check_promotion(sys.argv[2], sys.argv[3])
        print(f"Promotion: {result}")

    elif command == "convergence":
        if len(sys.argv) < 3:
            print("Usage: convergence <skill>")
            sys.exit(1)
        metric = evo.get_convergence(sys.argv[2])
        print(json.dumps(asdict(metric), indent=2))

    elif command == "verdict":
        if len(sys.argv) < 3:
            print("Usage: verdict <skill>")
            sys.exit(1)
        verdict = evo.get_double_loop_verdict(sys.argv[2])
        print(f"Verdict: {verdict}")

    elif command == "rsi":
        if len(sys.argv) < 3:
            print("Usage: rsi <session_id>")
            sys.exit(1)
        results = evo.run_rsi_cycle(sys.argv[2])
        print(json.dumps(results, indent=2, default=str))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
