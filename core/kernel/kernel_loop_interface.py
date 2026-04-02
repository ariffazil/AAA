"""
arifOS KernelLoop Interface
Based on Claude Code Agent SDK patterns (512K leak analysis)
Ditempa Bukan Diberi — structural enforcement, not vibes

This is the core loop library — standalone, reusable, wired to arifOS MCP.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
import json


# ─────────────────────────────────────────────
# Events — structured log output every turn
# ─────────────────────────────────────────────

class LoopEvent(Enum):
    TURN_STARTED = "TurnStarted"
    MODEL_OUTPUT = "ModelOutput"
    TOOL_CALL = "ToolCall"
    TOOL_RESULT = "ToolResult"
    TURN_COMPLETED = "TurnCompleted"
    BUDGET_EXCEEDED = "BudgetExceeded"
    CONSTITUTIONAL_VIOLATION = "ConstitutionalViolation"
    LOOP_COMPLETED = "LoopCompleted"


@dataclass
class Event:
    type: LoopEvent
    turn: int
    data: dict
    timestamp: str  # ISO8601


# ─────────────────────────────────────────────
# Tool Registry
# ─────────────────────────────────────────────

@dataclass
class ToolDef:
    name: str
    description: str
    schema: dict  # JSON Schema
    risk_tier: str  # "safe" | "guarded" | "high_risk" | "critical"
    mcp_server: str
    requires_audit: bool = False
    concurrent_limit: int = 10
    modes_allowed: list[str] = field(default_factory=lambda: ["internal"])
    example_chain: str | None = None


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDef] = {}

    def register(self, tool: ToolDef):
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDef | None:
        return self._tools.get(name)

    def list_by_tier(self, tier: str) -> list[ToolDef]:
        return [t for t in self._tools.values() if t.risk_tier == tier]

    def list_by_mode(self, mode: str) -> list[ToolDef]:
        return [t for t in self._tools.values() if mode in t.modes_allowed]

    def get_chain(self, chain_name: str, available_tools: list[str]) -> list[str]:
        """Resolve chain name → list of tool names, filtered by what's available."""
        chains = {
            "fix_bug": ["grep", "view", "edit", "bash", "test"],
            "deploy": ["build", "verify_signature", "push", "health_check"],
            "research": ["web_search", "web_fetch", "summarize", "store_memory"],
        }
        chain = chains.get(chain_name, [])
        return [t for t in chain if t in available_tools]


# ─────────────────────────────────────────────
# Tool Policy Engine
# ─────────────────────────────────────────────

class PolicyResult(Enum):
    ALLOWED = "allowed"
    DENIED_TIER = "denied_tier"
    DENIED_MODE = "denied_mode"
    DENIED_CONCURRENT = "denied_concurrent"
    DENIED_RATE = "denied_rate"
    REQUIRES_CONFIRMATION = "requires_confirmation"


@dataclass
class PolicyCheck:
    result: PolicyResult
    reason: str | None = None
    tool_name: str | None = None


class ToolPolicyEngine:
    """
    Central policy layer — tool firewall living in the kernel, not per-tool.
    Enforces: risk_tier → permission → concurrent limits → mode validation.
    """

    PERMISSION_MATRIX = {
        "safe": {
            "requires_audit": False,
            "max_per_minute": 120,
            "concurrent_limit": 10,
            "modes": ["internal", "external_open", "external_undercover"],
        },
        "guarded": {
            "requires_audit": True,
            "max_per_minute": 20,
            "concurrent_limit": 3,
            "modes": ["internal", "external_open"],
        },
        "high_risk": {
            "requires_audit": True,
            "max_per_minute": 5,
            "concurrent_limit": 1,
            "modes": ["internal"],
        },
        "critical": {
            "requires_audit": True,
            "max_per_minute": 1,
            "concurrent_limit": 1,
            "modes": ["internal"],
            "require_explicit_confirmation": True,
        },
    }

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self._active_concurrent: dict[str, int] = {}  # tool_name → count
        self._rate_window: dict[str, list[float]] = {}  # tool_name → timestamps

    def check(self, tool_name: str, mode: str) -> PolicyCheck:
        tool = self.registry.get(tool_name)
        if not tool:
            return PolicyCheck(PolicyResult.DENIED_TIER, f"Tool {tool_name} not found", tool_name)

        tier_config = self.PERMISSION_MATRIX.get(tool.risk_tier, {})
        allowed_modes = tier_config.get("modes", [])
        if mode not in allowed_modes:
            return PolicyCheck(
                PolicyResult.DENIED_MODE,
                f"Mode '{mode}' not permitted for risk tier '{tool.risk_tier}'",
                tool_name,
            )

        concurrent_limit = tier_config.get("concurrent_limit", 1)
        active = self._active_concurrent.get(tool_name, 0)
        if active >= concurrent_limit:
            return PolicyCheck(
                PolicyResult.DENIED_CONCURRENT,
                f"Concurrent limit reached ({active}/{concurrent_limit})",
                tool_name,
            )

        return PolicyCheck(PolicyResult.ALLOWED, None, tool_name)

    def pre_tool_call(self, tool_name: str, mode: str) -> PolicyCheck:
        """Called before each tool execution."""
        return self.check(tool_name, mode)

    def post_tool_call(self, tool_name: str, cost: float):
        """Called after each tool execution — record for rate limiting."""
        if tool_name not in self._active_concurrent:
            self._active_concurrent[tool_name] = 0
        self._active_concurrent[tool_name] -= 1
        self._active_concurrent[tool_name] = max(0, self._active_concurrent[tool_name])

    def release_concurrent(self, tool_name: str):
        self._active_concurrent[tool_name] = max(0, self._active_concurrent.get(tool_name, 1) - 1)


# ─────────────────────────────────────────────
# Kernel Loop
# ─────────────────────────────────────────────

@dataclass
class KernelConfig:
    max_turns: int = 50
    max_cost_per_turn: float = 0.50
    max_total_cost: float = 10.0
    parallel_tools: bool = True
    early_exit_on: list[str] = field(
        default_factory=lambda: ["no_tools", "explicit_done", "budget_exceeded"]
    )
    mode: str = "internal"  # internal | external_open | external_undercover


class KernelLoop:
    """
    Core agent loop — takes model handle, tool registry, policy engine.
    Runs the full agent loop internally, emits structured events.
    
    Aligns to arifOS Trinity:
      - Architect = KernelLoop (controls routing, budgets)
      - Auditor = 888_JUDGE (watches traces, validates)
      - Agent = MCP tool hosts (execute, stateless)
    """

    def __init__(
        self,
        model_handle: Any,  # LLM provider (OpenRouter/minimax/Claude)
        tool_registry: ToolRegistry,
        policy_engine: ToolPolicyEngine,
        auditor_handle: Any = None,  # 888_JUDGE instance
        config: KernelConfig = None,
    ):
        self.model = model_handle
        self.registry = tool_registry
        self.policy = policy_engine
        self.auditor = auditor_handle
        self.config = config or KernelConfig()
        self.events: list[Event] = []
        self.turn = 0
        self.total_cost = 0.0

    def _emit(self, event_type: LoopEvent, data: dict):
        self.events.append(Event(
            type=event_type,
            turn=self.turn,
            data=data,
            timestamp="ISO8601_HERE",  # filled by caller
        ))

    def run(self, task: str, system_prompt: str | None = None) -> dict:
        """
        Main entry point — runs the agent loop until:
          - model outputs no tool calls
          - budget exceeded
          - max turns reached
          - explicit done signal
        Returns final state + event log.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": task})

        while self.turn < self.config.max_turns:
            self.turn += 1
            self._emit(LoopEvent.TURN_STARTED, {"turn": self.turn})

            # ── Model call ──────────────────────────────────────
            response = self.model.chat(messages)
            self._emit(LoopEvent.MODEL_OUTPUT, {"content": response.content})
            messages.append({"role": "assistant", "content": response.content})

            # ── Parse tool calls ─────────────────────────────────
            tool_calls = response.tool_calls or []
            if not tool_calls:
                self._emit(LoopEvent.LOOP_COMPLETED, {"reason": "no_tools", "turn": self.turn})
                break

            if "no_tools" in self.config.early_exit_on:
                pass  # continue to tool execution

            # ── Policy pre-check ─────────────────────────────────
            for tc in tool_calls:
                check = self.policy.pre_tool_call(tc.name, self.config.mode)
                if check.result != PolicyResult.ALLOWED:
                    self._emit(
                        LoopEvent.CONSTITUTIONAL_VIOLATION,
                        {"tool": tc.name, "reason": check.reason},
                    )
                    if self.auditor:
                        self.auditor.review(tc.name, check.reason)
                    # Deny: replace with error result
                    tc.result = {"error": check.reason}
                    messages.append({
                        "role": "user",
                        "content": f"Tool '{tc.name}' was denied: {check.reason}",
                    })
                    continue

                # ── Execute tool ───────────────────────────────
                self._emit(LoopEvent.TOOL_CALL, {"tool": tc.name, "args": tc.args})
                tool_result = self._execute_tool(tc)
                self._emit(LoopEvent.TOOL_RESULT, {"tool": tc.name, "result": tool_result})
                messages.append({
                    "role": "user",
                    "content": json.dumps(tool_result),
                })
                self.total_cost += tool_result.get("cost", 0)

            # ── Budget check ────────────────────────────────────
            if self.total_cost >= self.config.max_total_cost:
                self._emit(LoopEvent.BUDGET_EXCEEDED, {"total_cost": self.total_cost})
                break

            # ── Early exit signals ───────────────────────────────
            # (checked in next iteration's model response)

        return {
            "final_message": messages[-1]["content"] if messages else "",
            "turns": self.turn,
            "total_cost": self.total_cost,
            "events": [e.__dict__ for e in self.events],
        }

    def _execute_tool(self, tool_call) -> dict:
        """Execute a tool via MCP server, record cost."""
        # MCP tool execution delegated to arifOS MCP server at port 8080
        # This is where the MCP client calls tools
        raise NotImplementedError("Wire to your MCP server client")


# ─────────────────────────────────────────────
# Coordinator agent pattern
# ─────────────────────────────────────────────

class CoordinatorAgent:
    """
    First-class coordinator — spawns child agents with constrained tool scopes.
    Never touches shell/FS directly. Tools: spawn, list, aggregate, kill.
    """
    
    def spawn_child(
        self,
        agent_profile: str,
        task: str,
        tool_allowlist: list[str],
        kernel_config: KernelConfig,
    ) -> str:
        """Spawn a child agent. Returns agent_id."""
        child_registry = ToolRegistry()
        for tool_name in tool_allowlist:
            parent_tool = self.registry.get(tool_name)
            if parent_tool:
                child_registry.register(parent_tool)
        
        child_kernel = KernelLoop(
            model_handle=self.model,
            tool_registry=child_registry,
            policy_engine=self.policy,
            config=kernel_config,
        )
        return child_kernel.run(task)

    def aggregate_reports(self, agent_ids: list[str]) -> str:
        """Collect and summarize child agent reports."""
        raise NotImplementedError("Wire to session management")


# ─────────────────────────────────────────────
# Pre-loop and post-loop hooks
# ─────────────────────────────────────────────

class ConstitutionalHooks:
    """
    Pre-loop: system prompt injection + regex filters
    Post-loop: git validation + bashSecurity + secret stripping
    """

    INTERNAL_CODENAME_PATTERN = r"(Capybara|Tengu|Fennec|Marmoset|Wolverine)\b"
    SLACK_URL_PATTERN = r"https://anthropic\.slack\.com/[^\s]*"
    VERSION_PATTERN = r"(opus|sonnet|haiku)-4\.\d+"

    @staticmethod
    def pre_loop_system_prompt(mode: str) -> str:
        templates = {
            "internal": "You are ARIF-MAIN. Ditempa Bukan Diberi. F1: reduce entropy. F4: every action witnessed. F7: stay within uncertainty band.",
            "external_open": "You are a helpful coding assistant. Disclose AI involvement. Do not mention internal codenames.",
            "external_undercover": "You are a developer. Write commits as if you are the author. Do not reveal AI involvement or internal names.",
        }
        return templates.get(mode, templates["internal"])

    @staticmethod
    def strip_internal(content: str) -> str:
        """Strip codenames, Slack URLs, unreleased versions from output."""
        import re
        content = re.sub(ConstitutionalHooks.INTERNAL_CODENAME_PATTERN, "[REDACTED]", content)
        content = re.sub(ConstitutionalHooks.SLACK_URL_PATTERN, "[INTERNAL_LINK]", content)
        content = re.sub(ConstitutionalHooks.VERSION_PATTERN, "[UNRELEASED_MODEL]", content)
        return content

    @staticmethod
    def post_git_check(commit_message: str) -> bool:
        """Return True if git commit message passes constitutional check."""
        stripped = ConstitutionalHooks.strip_internal(commit_message)
        return stripped == commit_message  # False means something was redacted

    @staticmethod
    def bash_security_check(command: str) -> dict:
        """Run 23-point bash security validation. Returns {passed: bool, failed_check: int}."""
        # Wired to bashSecurity.ts equivalent in arifOS
        # Placeholder — implement against your bashSecurity module
        return {"passed": True, "failed_check": None}
