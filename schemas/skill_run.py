#!/usr/bin/env python3
"""
skill_run.py — SkillRun contract schema.

Every skill execution produces a SkillRun record. It pins:
  - skill_sha256: hash of SKILL.md at execution time — detects tampering
  - capsule_id:   the inbound CAPSULE that triggered this run
  - steps:        each tool call with args_hash + output_hash + signature
  - verdict:      constitutional outcome
  - receipt_sig:  did:arif:a-forge signs the whole run

Without skill_sha256, you cannot answer: "was the skill modified between
when it was registered and when it ran?" That is the supply-chain gap.

Usage (in A-FORGE skill runner):
    from schemas.skill_run import SkillRun, SkillStep, build_skill_run
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field


Verdict = Literal["SEAL", "HOLD", "VOID", "SABAR", "UNKNOWN"]


class SkillStep(BaseModel):
    """One tool call within a skill execution."""
    step_index: int
    tool: str          = Field(description="Tool name called, e.g. 'forge_github_pr'")
    args_hash: str     = Field(description="SHA256(json.dumps(args, sort_keys=True))")
    output_hash: str   = Field(description="SHA256(json.dumps(output, sort_keys=True))")
    floor_gates: list[str] = Field(default_factory=list, description="F1–F13 gates checked")
    passed: bool       = Field(description="True if step completed without floor violation")
    signature: str     = Field(description="Ed25519 sig by did:arif:a-forge over step canonical bytes")

    def canonical_bytes(self) -> bytes:
        return json.dumps({
            "step_index": self.step_index,
            "tool":       self.tool,
            "args_hash":  self.args_hash,
            "output_hash": self.output_hash,
        }, sort_keys=True, separators=(",", ":")).encode()


class SkillRun(BaseModel):
    """
    Complete record of one skill execution.
    VAULT999-admissible: self-contained, deterministically serialisable.
    """
    run_id: str        = Field(description="SHA256(skill_id || capsule_id || started_at)")
    skill_id: str
    skill_sha256: str  = Field(
        description="SHA256 of SKILL.md content at execution time. "
                    "Detects if skill was modified after registration."
    )
    capsule_id: str    = Field(description="event_id of the triggering CAPSULE")
    authority_tier: str
    started_at: str    = Field(description="ISO8601 UTC")
    finished_at: Optional[str] = None
    steps: list[SkillStep] = Field(default_factory=list)
    verdict: Verdict   = "UNKNOWN"
    verdict_reason: str = ""
    receipt_signature: str = Field(
        description="Ed25519 sig by did:arif:a-forge over canonical_bytes(run)"
    )

    def canonical_bytes(self) -> bytes:
        """Deterministic bytes for signing. Excludes receipt_signature itself."""
        return json.dumps({
            "run_id":       self.run_id,
            "skill_id":     self.skill_id,
            "skill_sha256": self.skill_sha256,
            "capsule_id":   self.capsule_id,
            "authority_tier": self.authority_tier,
            "started_at":   self.started_at,
            "verdict":      self.verdict,
        }, sort_keys=True, separators=(",", ":")).encode()

    def is_tamper_evident(self, skill_md_path: Path) -> bool:
        """
        Verify that the SKILL.md on disk matches the hash recorded at run time.
        Returns False if the file was modified after the run was sealed.
        """
        if not skill_md_path.exists():
            return False
        current_hash = hashlib.sha256(skill_md_path.read_bytes()).hexdigest()
        return current_hash == self.skill_sha256


# ── Builder ───────────────────────────────────────────────────────────────────

def build_skill_run(
    skill_id: str,
    skill_md_path: Path,
    capsule_id: str,
    authority_tier: str,
) -> SkillRun:
    """
    Initialise a SkillRun. Call this before executing any steps.
    Pins skill_sha256 immediately — so we capture the pre-execution state.
    """
    import sys
    _root = str(Path(__file__).resolve().parent.parent)
    if _root not in sys.path:
        sys.path.insert(0, _root)

    started_at = datetime.now(timezone.utc).isoformat()
    skill_sha256 = hashlib.sha256(skill_md_path.read_bytes()).hexdigest()
    run_id = hashlib.sha256(
        f"{skill_id}{capsule_id}{started_at}".encode()
    ).hexdigest()

    run = SkillRun(
        run_id=run_id,
        skill_id=skill_id,
        skill_sha256=skill_sha256,
        capsule_id=capsule_id,
        authority_tier=authority_tier,
        started_at=started_at,
        receipt_signature="pending",
    )
    return run


def seal_skill_run(run: SkillRun) -> SkillRun:
    """Sign the completed SkillRun with did:arif:a-forge."""
    import sys
    from pathlib import Path as _Path
    _root = str(_Path(__file__).resolve().parent.parent)
    if _root not in sys.path:
        sys.path.insert(0, _root)
    try:
        from auth.gen_did import sign  # type: ignore[import]
        sig = sign(run.canonical_bytes(), organ_id="a-forge")
        return run.model_copy(update={
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "receipt_signature": sig,
        })
    except Exception as e:
        return run.model_copy(update={
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "receipt_signature": f"UNSIGNED:{e}",
        })


def hash_tool_args(args: dict) -> str:
    return hashlib.sha256(
        json.dumps(args, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def hash_tool_output(output: object) -> str:
    return hashlib.sha256(
        json.dumps(output, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


# ── Smoke test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    skill_path = Path(__file__).parent.parent / "skills" / "github-pr-review" / "SKILL.md"
    if not skill_path.exists():
        print(f"Skill not found at {skill_path}")
        sys.exit(1)

    run = build_skill_run(
        skill_id="github-pr-review",
        skill_md_path=skill_path,
        capsule_id="test-capsule-abc123",
        authority_tier="Tier1",
    )
    print(f"run_id       : {run.run_id[:16]}…")
    print(f"skill_sha256 : {run.skill_sha256[:16]}…")
    print(f"capsule_id   : {run.capsule_id}")
    print(f"started_at   : {run.started_at}")

    # Simulate a step
    step = SkillStep(
        step_index=0,
        tool="forge_github_pr",
        args_hash=hash_tool_args({"pr_url": "https://github.com/ariffazil/AAA/pull/1"}),
        output_hash=hash_tool_output({"title": "Test PR", "state": "open"}),
        floor_gates=["F1", "F4"],
        passed=True,
        signature="placeholder",
    )
    run.steps.append(step)
    run = run.model_copy(update={"verdict": "SEAL"})
    run = seal_skill_run(run)

    print(f"verdict      : {run.verdict}")
    print(f"receipt_sig  : {run.receipt_signature[:32]}…")
    print(f"tamper check : {run.is_tamper_evident(skill_path)}")
    print("\nSkillRun schema OK.")
