#!/usr/bin/env python3
"""
fed_router.py — FED Core MCP Server (Federation Router) · v3.2 Zen
═══════════════════════════════════════════════════════════
Port: 7074  ·  Unit: fed-router.service  ·  MCP prefix: fed_*
Answers: "Where should this agent route?"

Architecture:
  READ  → fed_state.db (provider_balance, route_latency, route_health)
  WRITE → token_bank_spend (on every routed call)
  NEVER → actively ping for latency (passive telemetry only)

Zen v3.2 (2026-09-01):
  1. DRY Pricing Tables — single _get_pricing_table() source of truth
  2. SQLite Context Managers — all DB calls use `with` for deterministic teardown
  3. Declarative Priority Matrix — RankGate class replaces procedural magic numbers
  4. Structured Concurrency — ThreadPoolExecutor replaces orphaned daemon threads
  5. Graceful Shutdown — SIGTERM/SIGINT handler with cancel_futures=True

Hardened v3.0 invariants (preserved):
  1. Asymmetric Balance Bypass (dual-track — Track A hard / Track B soft / UNVERIFIABLE)
  2. Constitutional Hard-Gate (tier ≥ 666 → direct only)
  3. Agent Cascade Contract (ranked array output)
  4. State Isolation (READ providers → WRITE token_bank_spend only)
  5. Balance Bypass Enforcement (Track A <$1 HARD, Track B <$5 SOFT, conf<0.50 UNVERIFIABLE)
  6. Model Route Tables (deepseek, qwen, gpt, claude, kimi, glm families)

Forged: 2026-07-30  ·  Zen-dated: 2026-08-02  ·  Zen-Optimized: 2026-09-01
DITEMPA BUKAN DIBERI
"""

import hashlib
import json
import os
import signal
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# ── Zen Priority Matrix ───────────────────────────────────────────────
class RankGate:
    """Declarative priority adjustments — isolates reasoning from execution."""
    VISION_MULEROUTER_BOOST = -2
    VISION_NATIVE_BOOST = -1
    NO_TELEMETRY = 1  # v3.3.1: was 2 — over-demoted every route while the telemetry loop
    # was unclosed. /report ingress now live (FED v3.3); light penalty until samples
    # accumulate. Revisit to 2 once median sample_count > 5 across live routes.
    LOW_TELEMETRY = 1
    LATENCY_DEGRADED = 3
    BALANCE_SOFT_DEMOTE = 5
    RATE_LIMITED = 8
    BALANCE_HARD_DEMOTE = 10

# ── Background Task Executor ──────────────────────────────────────────
_FED_BACKGROUND_TASKS = ThreadPoolExecutor(max_workers=4, thread_name_prefix="fed_sidecar")

# ── Graceful Shutdown Handler ─────────────────────────────────────────
_shutdown = False

def _graceful_exit(signum, frame):
    global _shutdown
    _shutdown = True
    # Cancel all pending sidecar futures instantly — no zombie threads
    _FED_BACKGROUND_TASKS.shutdown(wait=False, cancel_futures=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, _graceful_exit)
signal.signal(signal.SIGINT, _graceful_exit)

# ── ETCSOVG Harness Metadata (arxiv 2605.23950) ──────────────────────
def _build_hcsvog(
    execution: str = "bare",
    tools: str = "none",
    context: str = "unknown:none:none",
    schedule: str = "single:unlimited:none",
    observe: str = "none",
    verify: str = "none",
    gov: str = "333:yolo",
) -> dict:
    """Build ETCSOVG harness metadata dict with stable fingerprint."""
    hcsvog = {
        "v": 1,
        "h_execution": execution,
        "h_tools": tools,
        "h_context": context,
        "h_schedule": schedule,
        "h_observe": observe,
        "h_verify": verify,
        "h_gov": gov,
    }
    canonical = json.dumps(hcsvog, sort_keys=True, separators=(",", ":"))
    hcsvog["h_fingerprint"] = hashlib.sha256(canonical.encode()).hexdigest()[:8]
    return hcsvog

# ── JIT Intent Retrieval (P1.5) ────────────────────────────────────
# Lazily import intent_retriever to avoid loading sentence-transformers at boot.
_intent_retriever = None

def _get_intent_retriever():
    global _intent_retriever
    if _intent_retriever is None:
        try:
            from intent_retriever import build_jit_context as _build
            _intent_retriever = _build
        except ImportError:
            _intent_retriever = False  # Sentinel: failed to load
    return _intent_retriever if _intent_retriever is not False else None

# ── A2A Trace Propagation (P1.7) ────────────────────────────────────
try:
    from trace_propagation import make_trace_headers
    _trace_enabled = True
except ImportError:
    _trace_enabled = False
    def make_trace_headers(*args, **kwargs):
        return {}

# ── Config ───────────────────────────────────────────────────────────────
FED_STATE_DB = Path("/root/.local/share/arifos/token_bank.db")
FED_PORT = 7074

# ── SINGLE SOURCE OF TRUTH ───────────────────────────────────────────────
# Zen 2026-08-13 under F13 "make it all SOT": every static routing table
# below used to be a hardcoded dict in this file (710 lines across 16 dicts).
# They now load from one JSON SOT. Live balance/latency/health stay in
# token_bank.db and are deliberately NOT mirrored here — duplicating them is
# what let three stores disagree about mulerouter (SOT said DEAD, probe said
# HTTP 200).
#
# FAIL-CLOSED: a missing or malformed SOT aborts startup. It must never fall
# back to defaults — silent fallback is exactly what hid a revoked Kimi key
# and kept a DEAD route ranked #2.
FED_SOT_PATH = Path("/root/.config/federation-models.json")

_SOT_REQUIRED = (
    "pricing", "pricing_default", "model_routes", "capability_signatures",
    "emd_model_class", "emd_neutral_cap", "agent_default_operation",
    "vision_models", "constitutional_allowed", "effort",
)
_SOT_REQUIRED_PRICING = ("deepseek", "mulerouter", "tokenrouter", "kimi-moonshot", "flame")
_SOT_REQUIRED_EFFORT = ("model_map", "alt_models", "cost_multiplier", "reasoning_passes")


def _load_sot() -> dict:
    """Load the static federation SOT. Aborts startup on any defect."""
    if not FED_SOT_PATH.exists():
        raise SystemExit(f"FED FATAL: SOT missing at {FED_SOT_PATH}")
    try:
        sot = json.loads(FED_SOT_PATH.read_text())
    except Exception as exc:
        raise SystemExit(f"FED FATAL: SOT unparseable ({FED_SOT_PATH}): {exc}")

    for key in _SOT_REQUIRED:
        if key not in sot or not sot[key]:
            raise SystemExit(f"FED FATAL: SOT missing/empty required section '{key}'")
    for prov in _SOT_REQUIRED_PRICING:
        if prov not in sot["pricing"]:
            raise SystemExit(f"FED FATAL: SOT pricing missing provider '{prov}'")
    for sub in _SOT_REQUIRED_EFFORT:
        if sub not in sot["effort"]:
            raise SystemExit(f"FED FATAL: SOT effort missing '{sub}'")

    print(
        f"   SOT: {FED_SOT_PATH} — "
        f"{len(sot['model_routes'])} routes, "
        f"{len(sot['capability_signatures'])} capabilities, "
        f"{sum(len(v) for v in sot['pricing'].values())} prices, "
        f"{len(sot.get('providers', []))} providers, "
        f"{len(sot.get('models', []))} models"
    )
    return sot


_SOT = _load_sot()

# ── Pricing tables (inlined — shared logic with token_bank.py) ──────────
# Keep in sync with /root/AAA/scripts/token_bank.py pricing tables
# Zen 2026-08-02: Added DeepSeek direct pricing + all provider tables (LiteLLM model catalog pattern)

DEEPSEEK_PRICING = _SOT["pricing"]["deepseek"]
MULEROUTER_PRICING = _SOT["pricing"]["mulerouter"]
TOKENROUTER_PRICING = _SOT["pricing"]["tokenrouter"]
KIMI_PRICING = _SOT["pricing"]["kimi-moonshot"]
FLAME_PRICING = _SOT["pricing"]["flame"]
QWEN_TEAM_PRICING = _SOT["pricing"]["qwen-token-plan-team"]

# Zen 3.2: Single source of truth for pricing table lookups.
# Replaces duplicated inline dicts that existed in both _estimate_cost and
# _estimate_cost_per_1k functions — preventing asymmetric drift between them.

def _get_pricing_table(provider_id: str) -> dict:
    """Return the pricing dictionary for a given provider ID.
    
    Zen 3.2: Consolidated from twin inline dicts into single function.
    Returns empty dict for unknown providers (fallback handled by caller).
    """
    return {
        "deepseek": DEEPSEEK_PRICING,
        "mulerouter": MULEROUTER_PRICING,
        "tokenrouter": TOKENROUTER_PRICING,
        "flame": FLAME_PRICING,
        "kimi-moonshot": KIMI_PRICING,
        "qwen-token-plan-team": QWEN_TEAM_PRICING,
        "qwen-token-plan-individual": DEEPSEEK_PRICING,  # Qwen routes deepseek models at similar pricing
        "bailian-token-plan": DEEPSEEK_PRICING,           # Bailian also similar
    }.get(provider_id, {})


def _estimate_cost(provider_id: str, model_id: str, tokens_in: int, tokens_out: int) -> float:
    """Calculate estimated cost in USD. Zen 3.2: uses consolidated _get_pricing_table()."""
    pricing = _get_pricing_table(provider_id).get(model_id, {"input": 0.50, "output": 2.00})
    return round((tokens_in / 1_000_000) * pricing["input"] + (tokens_out / 1_000_000) * pricing["output"], 8)


def _estimate_cost_per_1k(provider_id: str, model_id: str) -> dict:
    """Return estimated cost per 1K tokens for a route. LiteLLM catalog pattern."""
    pricing = _get_pricing_table(provider_id).get(model_id, {"input": 0.50, "output": 2.00})
    return {
        "input_per_1m_usd": pricing["input"],
        "output_per_1m_usd": pricing["output"],
    }

mcp = FastMCP("FED — Federation Router")

@mcp.custom_route("/health", methods=["GET"])
async def fed_health(_request):
    """Organ probe surface — ADVISORY_ONLY. Never judges or mutates."""
    from starlette.responses import JSONResponse
    return JSONResponse(
        {
            "status": "healthy",
            "service": "FED",
            "role": "ADVISORY_ONLY",
            "port": FED_PORT,
            "mcp": "/mcp",
            "class": "route_advisor",
            "ceiling": "never judges, never hard-blocks",
            "tools": ["fed_route", "fed_classify", "fed_status", "fed_probe", "fed_contrast", "fed_health", "fed_report_latency"],
        }
    )


@mcp.custom_route("/report", methods=["POST"])
async def fed_report_http(_request):
    """HTTP telemetry ingress (Phase 0 fix #3, 2026-09-07).

    fed_report_latency existed but had ZERO callers — the telemetry loop was
    never closed (max sample_count = 6, NO_TELEMETRY demotion everywhere).
    This endpoint lets non-MCP callers (fed-aware middleware :4010, harness
    post-call hooks, cron probes) report latency with a plain POST:

        curl -X POST :7074/report -d '{"provider":"deepseek",
             "model":"deepseek-v4-pro","latency_ms":740,"status_code":200}'

    Same logic as the fed_report_latency MCP tool. ADVISORY data only.
    """
    from starlette.responses import JSONResponse

    try:
        body = await _request.json()
        result = fed_report_latency(
            provider=str(body["provider"]),
            model=str(body["model"]),
            latency_ms=float(body["latency_ms"]),
            status_code=int(body.get("status_code", 200)),
            tokens_in=int(body.get("tokens_in", 0)),
            tokens_out=int(body.get("tokens_out", 0)),
            agent_id=str(body.get("agent_id", "http")),
            hcsvog_fingerprint=str(body.get("hcsvog_fingerprint", "")),
        )
        return JSONResponse(result)
    except KeyError as e:
        return JSONResponse({"recorded": False, "error": f"missing field {e}"}, status_code=400)
    except Exception as e:  # noqa: BLE001 — ingress must not crash the router
        return JSONResponse({"recorded": False, "error": str(e)}, status_code=400)


@mcp.custom_route("/route", methods=["POST"])
async def fed_route_http(_request):
    """Plain-JSON advisory routing endpoint (FED v3.3, 2026-09-07).

    Restores the middleware→FED direct path: fed_aware_middleware.py :4010
    POSTed to /fed/route which never existed (HTTP 404 — every capability
    resolution attempt died). Same engine as the fed_route MCP tool.
    ADVISORY_ONLY — data, never verdicts.
    """
    from starlette.responses import JSONResponse

    try:
        body = await _request.json()
        _model = str(body.get("model", "deepseek-v4-pro"))
        _task = str(body.get("task", ""))
        # v3.3.1 fix: apply the same Capability Classifier auto-swap as the
        # fed_route MCP wrapper — the HTTP lane must not bypass classification.
        _cls = classify_capability(_task) if _task else None
        if (
            _cls
            and (
                _cls["confidence"] >= 0.90
                or (_cls["capability"] == "vision" and _cls["confidence"] >= 0.75)
            )
            and not _model.startswith("fed-")
            and not body.get("effort_level")
        ):
            _model = _cls["signature"]
        routes = fed_route_engine(
            task=_task,
            model=_model,
            modality=str(body.get("modality", "text")),
            agent_id=str(body.get("agent_id", "http")),
            constitutional_tier=int(body.get("constitutional_tier", 333)),
            effort_level=str(body.get("effort_level", "") or ""),
        )
        return JSONResponse(
            {
                "routes": routes,
                "classification": _cls,
                "model_applied": _model,
                "advisory": "ADVISORY_ONLY — execute in rank order; on failure cascade; never retry same provider twice.",
            }
        )
    except Exception as e:  # noqa: BLE001 — ingress must not crash the router
        return JSONResponse({"error": str(e)}, status_code=400)


# ── DB helpers (READ-ONLY for balances) ──────────────────────────────────
# Zen 3.2: All SQLite connections wrapped in `with` for deterministic teardown.
# Eliminates connection leak vectors if an exception occurs before .close().

def read_provider_balance(provider_id: str) -> dict | None:
    """Read from providers table in token_bank.db. Returns dict with balance_usd, confidence_score, track_type."""
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM providers WHERE provider_name = ?", (provider_id,)).fetchone()
        if not row:
            return None
        r = dict(row)
        # Normalize field names for backward compatibility with router logic
        r["balance_confidence"] = r.get("confidence_score", 1.0)
        r["track"] = r.get("track_type", "B")
        return r


def read_all_providers() -> list[dict]:
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM providers ORDER BY track_type, provider_name").fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["balance_confidence"] = r.get("confidence_score", 1.0)
            r["track"] = r.get("track_type", "B")
            result.append(r)
        return result


def read_route_latency(provider_id: str, model_id: str) -> dict | None:
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM route_latency WHERE provider_name = ? AND model_id = ?",
            (provider_id, model_id),
        ).fetchone()
        return dict(row) if row else None


def read_route_health(provider_id: str, model_id: str) -> dict | None:
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM route_health WHERE provider_name = ? AND model_id = ?",
            (provider_id, model_id),
        ).fetchone()
        return dict(row) if row else None


def log_spend(provider_id: str, model_id: str, tokens_in: int, tokens_out: int, agent_id: str):
    """Write spend to token_bank_spend. FED's ONLY write path."""
    cost = _estimate_cost(provider_id, model_id, tokens_in, tokens_out)
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.execute(
            """INSERT INTO token_bank_spend (provider_name, model_id, agent_id,
                                              tokens_in, tokens_out, estimated_cost_usd, called_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (provider_id, model_id, agent_id, tokens_in, tokens_out, cost, now),
        )


# ═══ EMD LANE AWARENESS — Fasa 1 (2026-08-08, F13 Arif directive) ═══
# Encode → Metabolize → Decode. Klasifikasi ikut mekanik model, bukan jenama.
# FLAG only — ADVISORY_ONLY ceiling preserved, never hard-blocks (F1).

EMD_MODEL_CLASS = _SOT["emd_model_class"]
_NEUTRAL_CAP = _SOT["emd_neutral_cap"]
AGENT_DEFAULT_OPERATION = _SOT["agent_default_operation"]


def _emd_check(agent_id: str, operation: str, model_id: str, modality: str) -> dict:
    """EMD lane check. FLAG only — never blocks (FED ceiling: ADVISORY_ONLY).

    Rules:
      R1 agent-shift   — agent nature vs requested operation
      R2 model-lane    — sense-optimized model on ACT work & inverse
      R3 modality gate — vision/audio/gen payload to capability-blind model (F2)
    """
    default_op = AGENT_DEFAULT_OPERATION.get(agent_id, "metabolize")
    resolved_op = operation if operation and operation != "auto" else default_op
    cap = EMD_MODEL_CLASS.get(model_id, _NEUTRAL_CAP)
    verdict, reasons, suggested = "EMD_ALIGNED", [], []

    # R1 — Agent lane shift
    if operation not in ("", "auto") and resolved_op != default_op:
        verdict = "EMD_MISMATCH"
        reasons.append(f"agent {agent_id} is {default_op.upper()}-nature, forced to {resolved_op.upper()} lane")

    # R2 — Model lane mismatch
    if resolved_op == "act" and cap["lane"] == "sense":
        verdict = "EMD_MISMATCH"
        reasons.append(f"ACT work on SENSE-optimized model {model_id}")
        suggested += ["deepseek-v4-pro", "deepseek-v4-flash"]
    elif resolved_op == "sense" and cap["lane"] == "act":
        verdict = "EMD_MISMATCH"
        reasons.append(f"SENSE work on ACT-optimized model {model_id}")
        suggested += ["qwen3.8-max", "MiniMax-M3"]

    # R3 — Modality capability gate (F2: vision payload to blind model)
    if modality in ("vision", "omni") and not cap["vision_in"]:
        verdict = "EMD_MISMATCH"
        reasons.append(f"vision payload to vision-blind {model_id}")
        suggested += ["qwen3.8-max", "mimo-v2.5"]
    if modality == "audio" and not cap["audio_in"]:
        verdict = "EMD_MISMATCH"
        reasons.append(f"audio payload to audio-blind {model_id}")
        suggested += ["mimo-v2.5"]
    if modality in ("image_out", "video_out") and not cap.get("image_out") and not cap.get("video_out"):
        verdict = "EMD_MISMATCH"
        reasons.append(f"generation payload to non-generation {model_id}")
        suggested += ["wan2.7-image-pro"]

    if verdict == "EMD_ALIGNED":
        reasons.append(f"{resolved_op.upper()} <-> {cap['lane'].upper()} aligned")

    return {
        "verdict": verdict,
        "operation": resolved_op,
        "model_class": cap["lane"],
        "reasons": reasons,
        "suggested": sorted(set(suggested))[:3],
    }


# ═══ CAPABILITY SIGNATURE ROUTING — Fasa 1 (2026-08-10, F13 directive) ═══
# Transition FED from static model routing to capability-based routing.
# Agents request a CAPABILITY, not a model name. FED resolves to model+provider cascade.
# Zen: "Decouple task from provider. Never hardcode model names. Use capability aliases."
#
# Each capability signature maps to a cascade of [model → provider_priority].
# Fallback arrays trigger in <80ms on 429/5xx — model-level cascading handles failover.
# The existing MODEL_ROUTES table resolves each model to provider cascades.

CAPABILITY_SIGNATURES = _SOT["capability_signatures"]


def resolve_capability(capability: str) -> list[str]:
    """Resolve a capability signature to its model cascade. Returns list of model IDs."""
    if capability in CAPABILITY_SIGNATURES:
        return CAPABILITY_SIGNATURES[capability]["models"]
    return []


def get_capability_meta(capability: str) -> dict | None:
    """Return metadata for a capability signature."""
    return CAPABILITY_SIGNATURES.get(capability)


# ── Capability Classifier v1 (Zen Card 2026-09-07 · Phase 0 fix #4) ───────
# BenchDrift (SEALED): "FED routes by live latency + TASK FITNESS." Until now
# the `task` param was decorative (dead JIT stub). This classifier makes it
# load-bearing. Deterministic, identity-blind — answers ONE question:
# "capability apa diperlukan?" Identity stays prompt-side (SOUL_STAMP/cards);
# FED never reads identity content (separation of powers, FED spec v0.2–v0.4).
CAPABILITY_CLASS_PATTERNS = {
    "vision": [
        "gambar", "gmbr", "foto", "photo", "image", "screenshot", "screen shot",
        "lukis", "visual", "ocr", "scan ", "camera", "render",
    ],
    "coding": [
        "debug", "python", "javascript", "typescript", "code", "kod", "coding",
        "stack trace", "traceback", "compile", "refactor", "unit test", "sql",
        "git ", "regex", "api endpoint",
    ],
    "long_context": [
        "summarize", "rumusan", "ringkas", "long document", "pages", "halaman",
        "pdf", "transcript", "whole file", "entire log", "long thread", "200 page",
    ],
    "reasoning": [
        "assignment", "tugasan", "homework", "explain", "terangkan", "analyze",
        "analisis", "essay", "compare", "argument", "derive", "prove", "study",
        "belajar", "exam", "kuiz", "why does", "evaluate", "implication",
    ],
    "action": [
        "search", "cari ", "google", "browse", "run ", "execute", "fetch",
        "scrape", "deploy", "restart", "cron", "send message", "book ",
    ],
}
CAPABILITY_CLASS_SIGNATURE = {
    "vision": "fed-multimodal-vision",
    "coding": "fed-coding",
    "long_context": "fed-long-context",
    "reasoning": "fed-reasoning-heavy",
    "action": "fed-agent-subagent",
    "conversation": "fed-conversational",
}


def classify_capability(task: str) -> dict:
    """Deterministic capability classifier.

    Returns {capability, signature, confidence, matched} — data, never verdicts.
    Auto-apply threshold in fed_route is 0.90 (≥2 term hits); single generic
    hits stay advisory only (prevents 'error'/'search' false reroutes).
    """
    text = f" {task.lower()} "
    best, best_hits, best_terms = "conversation", 0, []
    for _cls, _terms in CAPABILITY_CLASS_PATTERNS.items():
        _hits = [t for t in _terms if t in text]
        if len(_hits) > best_hits:
            best, best_hits, best_terms = _cls, len(_hits), _hits
    confidence = min(0.99, 0.60 + 0.15 * best_hits) if best_hits else 0.50
    return {
        "capability": best,
        "signature": CAPABILITY_CLASS_SIGNATURE[best],
        "confidence": round(confidence, 2),
        "matched": best_terms,
    }


# ── Routing tables ───────────────────────────────────────────────────────
# Model → [route] mapping. Priority: direct > gateway_clean > gateway_shadowed.
# Fed from AGENT_MODEL_MAP.json fed_routes + provider registry.

MODEL_ROUTES = _SOT["model_routes"]

# Modality boost map
# Zen 2026-08-08 (EMD lane audit): pruned 6 zombies. Aligned with
# litellm-config.yaml model_info.supports_image_input / supports_vision.
# F2 evidence: live audit 2026-08-08 — only qwen3.8-max + MiMo v2.5[/pro]
# are actually exposed as vision-capable in the LiteLLM federation cascade.
VISION_MODELS = set(_SOT["vision_models"])

# Constitutional tier → allowed router classes
CONSTITUTIONAL_ALLOWED = {int(k): set(v) for k, v in _SOT["constitutional_allowed"].items()}

# Effort level → preferred model (Thorsten Ball "Effort Dial" pattern · 2026-08-04)
# "Don't pick models, pick effort." — Thorsten Ball (Amp)
# Effort overrides model parameter when set. Constitutional tier still gates authority.
EFFORT_MODEL_MAP = _SOT["effort"]["model_map"]
EFFORT_ALT_MODELS = _SOT["effort"]["alt_models"]
EFFORT_COST_MULTIPLIER = _SOT["effort"]["cost_multiplier"]
EFFORT_REASONING_PASSES = _SOT["effort"]["reasoning_passes"]


# ── FED Route Engine (Zen-hardened v3.2 — Declarative Priority Matrix) ──
# Zen 2026-08-02: Absorbed LiteLLM patterns:
#   - Route health gate (cooldown DEGRADED, demote RATE_LIMITED)
#   - Cost estimate surfaced per route (catalog pricing)
#   - Insufficient telemetry demotion (low-sample routes deprioritized)
#
# Zen 3.2: Priority adjustments use RankGate class constants.
# No more procedural magic numbers — all penalty/boost values named and inspectable.
def fed_route_engine(
    task: str = "",
    model: str = "deepseek-v4-pro",
    modality: str = "text",
    agent_id: str = "opencode",
    constitutional_tier: int = 333,
    effort_level: str = "",
) -> list[dict]:
    """
    Zen-hardened 9-step routing logic (was 7, +2 LiteLLM patterns).
    Effort Dial added v3.2 (2026-08-04) — Thorsten Ball pattern.
    Priority Matrix added v3.2 (2026-09-01) — RankGate declarative class.

    Steps:
      0. EFFORT DIAL: if effort_level set, override model by effort tier
      0.5 CAPABILITY: if model is a fed-* capability, resolve to multi-model cascade
      1. FILTER: remove DEAD providers
      2. HEALTH GATE: skip DEGRADED, demote RATE_LIMITED (LiteLLM cooldown)
      3. RANK: by priority class (direct > gateway > shadowed)
      4. BOOST: vision modality → push VL-capable providers up
      5. DEGRADE: constitutional ≥ 666 → direct ONLY
      6. BALANCE GATE: dual-track (API hard, Token Bank soft, UNVERIFIABLE bypass)
      7. LATENCY GATE: read pre-computed p50/p95; demote if p95>5s
      8. TELEMETRY GATE: demote routes with <10 samples (LiteLLM: don't route to unproven paths)
      9. COST SURFACE: attach estimated cost per 1K tokens to each route
      10. RETURN: top 3 routes with reasoning
    """
    # ── Step 0: EFFORT DIAL — override model by effort tier ────────
    effort_applied = None
    if effort_level and effort_level in EFFORT_MODEL_MAP:
        effort_applied = effort_level
        model = EFFORT_MODEL_MAP[effort_level]
        # Constitutional tier still gates — effort can't override authority
        if constitutional_tier >= 666:
            model = "deepseek-v4-pro"  # Only constitutional models for judge/seal

    # ── Step 0.5: CAPABILITY SIGNATURE RESOLUTION ──────────────────
    capability_meta = None
    capability_models = []
    if model.startswith("fed-"):
        capability_models = resolve_capability(model)
        capability_meta = get_capability_meta(model)
        if not capability_models:
            return [{"rank": 0, "error": f"Unknown capability signature: {model}"}]
        # Use the capability's modality if not explicitly overridden
        if modality == "text" and capability_meta:
            modality = capability_meta.get("modality", "text")

    # ── Resolve routes: single model or capability cascade ──────────
    if capability_models:
        # Capability cascade: collect routes from all models in the capability
        all_routes = []
        for cap_model in capability_models:
            model_routes = MODEL_ROUTES.get(cap_model, [])
            for route in model_routes:
                route_with_model = dict(route)
                route_with_model["_capability_model"] = cap_model
                all_routes.append(route_with_model)
        routes = all_routes
    else:
        routes = MODEL_ROUTES.get(model, MODEL_ROUTES.get("deepseek-v4-pro", []))

    if not routes:
        return [{"rank": 0, "error": f"No routes defined for model: {model}"}]

    now = datetime.now(timezone.utc).isoformat()
    ranked = []

    for route in routes:
        provider_id = route["provider"]
        # If capability cascade, use the specific model from the cascade
        route_model = route.get("_capability_model", model)
        bal = read_provider_balance(provider_id)

        # ── Step 1: FILTER dead providers ────────────────────────────
        # FI-008 2026-09-07 corpse-route fix: notes carry richer truth than the
        # health table (probes historically wrote notes only). Honor hard markers.
        _notes_u = str(bal.get("notes") or "").upper() if bal else ""
        if any(_m in _notes_u for _m in ("DEAD", "DO NOT ROUTE", "DRAINED")):
            continue

        # ── Step 2: HEALTH GATE (Zen: LiteLLM cooldown pattern) ─────
        health = read_route_health(provider_id, route_model)
        # FI-008 2026-09-07 corpse-route fix: probes record status on the generic
        # 'probe' model row; the engine looked up per-model rows only, so a
        # provider killed by a probe (429 quota / 401 drained) kept rendering
        # LIVE and got ranked (witnessed: qwen-token-plan-team rank #2 while
        # notes said quota EXHAUSTED). Fall back to the provider-level probe row.
        if not health:
            _probe_health = read_route_health(provider_id, "probe")
            if _probe_health:
                health = _probe_health
        health_status = health["status"] if health else "LIVE"
        health_flag = None

        if health_status in ("DEGRADED", "DEAD"):
            # LiteLLM cooldown: skip failing deployments entirely.
            # Zen 2026-08-13: "DEAD" added. Step 1 only filters DEAD via provider
            # *notes*; a route_health row with status='DEAD' fell through this gate
            # and was still ranked (observed: deepseek/deepseek-v4-pro offered at
            # rank 2 while DEAD), burning the first fallback on a known-dead route.
            continue
        elif health_status == "RATE_LIMITED":
            # LiteLLM cooldown: demote but keep as last resort
            health_flag = "RATE_LIMITED"
            # Don't skip — just heavily demote below

        # ── Step 4: DEGRADE constitutional ───────────────────────────
        allowed = CONSTITUTIONAL_ALLOWED.get(constitutional_tier, {"direct", "gateway"})
        if route["class"] not in allowed:
            continue

        # ── Step 2: RANK — priority score (lower = better) ───────────
        priority = route["priority"]
        
        # Zen 3.2: Use RankGate constants instead of magic numbers
        if modality == "vision" and provider_id == "mulerouter":
            priority += RankGate.VISION_MULEROUTER_BOOST  # Boost MuleRouter for vision (4 VL models)
        if modality == "vision" and route_model in VISION_MODELS:
            priority += RankGate.VISION_NATIVE_BOOST
        if health_flag == "RATE_LIMITED":
            priority += RankGate.RATE_LIMITED  # Heavy demotion — last resort

        # ── Step 5: BALANCE GATE dual-track ──────────────────────────
        balance = bal["balance_usd"] if bal else None
        confidence = bal["balance_confidence"] if bal else 0.30
        track = bal["track"] if bal else "B"
        notes = str(bal.get("notes", "") or "") if bal else ""
        balance_flag = None

        # Monthly token plans (credit-based, not USD) — do not HARD-demote on $0 balance.
        # Track A + monthly_plan marker → check notes for "monthly" or "credit" to skip HARD gate.
        # Zen 2026-08-13: added "subscription" markers. Kimi Code bills by plan tier
        # (Moderato/Allegretto), so balance_usd is structurally 0 and the $1.00 hard
        # gate was demoting a healthy, entitled route.
        is_monthly_plan = any(
            tag in notes.lower()
            for tag in (
                "monthly_token_plan",
                "credit pack",
                "credit-based",
                "monthly plan",
                "credit_plan",
                "subscription",
                "subscription_quota",
                "plan quota",
            )
        )

        if track == "A" and confidence >= 0.95 and not is_monthly_plan:
            # Track A: API-probed, hard gate at $1.00
            if balance is not None and balance < 1.00:
                priority += RankGate.BALANCE_HARD_DEMOTE  # HARD demotion
                balance_flag = "LOW_BALANCE_HARD"
        elif track == "B":
            # Track B: Token Bank estimate, soft gate at $5.00
            if confidence < 0.50:
                balance_flag = "UNVERIFIABLE"
                # NEVER demote — retain rank, flag only
            elif balance is not None and balance < 5.00 and confidence > 0.70:
                priority += RankGate.BALANCE_SOFT_DEMOTE  # SOFT demotion
                balance_flag = "LOW_BALANCE_SOFT"
            elif balance is None:
                balance_flag = "UNVERIFIABLE"
                # NEVER demote for unknown balance

        # ── Step 6: LATENCY GATE (passive) ───────────────────────────
        lat = read_route_latency(provider_id, route_model)
        p50_ms = lat["p50_ms"] if lat else None
        p95_ms = lat["p95_ms"] if lat else None
        sample_count = lat["sample_count"] if lat else 0
        latency_flag = None

        if p50_ms:
            if p95_ms and p95_ms > 5000:
                latency_flag = "DEGRADED"
                priority += RankGate.LATENCY_DEGRADED

        # ── Step 7: TELEMETRY GATE (Zen: LiteLLM pattern) ────────────
        # Demote routes with insufficient telemetry — prefer proven paths
        if sample_count < 10:
            if sample_count == 0:
                latency_flag = "NO_TELEMETRY"
                priority += RankGate.NO_TELEMETRY  # Slight demotion for completely untested
            else:
                latency_flag = "INSUFFICIENT_TELEMETRY"
                # Only demote if we have some data that suggests slowness
                if p50_ms and p50_ms > 2000:
                    priority += RankGate.LOW_TELEMETRY

        # ── Step 8: COST SURFACE (Zen: LiteLLM model catalog) ────────
        cost_per_1k = _estimate_cost_per_1k(provider_id, route_model)

        ranked.append(
            {
                "rank": 0,  # filled after sort
                "priority": priority,
                "provider": provider_id,
                "model": route_model,
                "router": route["router"],
                "router_class": route["class"],
                "balance_usd": balance,
                "balance_confidence": confidence,
                "balance_track": track,
                "balance_flag": balance_flag,
                "latency_p50_ms": p50_ms,
                "latency_p95_ms": p95_ms,
                "latency_sample_count": sample_count,
                "latency_flag": latency_flag,
                "health": health_status,
                "health_flag": health_flag,
                "cost_per_1m_input_usd": cost_per_1k["input_per_1m_usd"],
                "cost_per_1m_output_usd": cost_per_1k["output_per_1m_usd"],
                "shadow": route.get("shadow"),
                "free": route.get("free", False),
                "reason": _build_reason(route, balance_flag, latency_flag, health_flag, constitutional_tier),
            }
        )

    # Sort by priority (ascending)
    ranked.sort(key=lambda r: r["priority"])

    # Assign ranks
    for i, r in enumerate(ranked[:3]):
        r["rank"] = i + 1
        r["effort_applied"] = effort_applied
        if effort_applied:
            r["effort_model"] = model
            r["reasoning_passes"] = EFFORT_REASONING_PASSES.get(effort_applied, 0)

    return ranked[:3]


def _build_reason(route, balance_flag, latency_flag, health_flag, tier):
    parts = []
    if tier >= 666:
        parts.append("666/999 constitutional — direct path required")
    if route["class"] == "direct":
        parts.append("zero gateway contamination")
    if route.get("free"):
        parts.append("FREE tier")
    if route.get("shadow"):
        parts.append(f"SHADOWED: {route['shadow']}")
    if health_flag == "RATE_LIMITED":
        parts.append("provider rate-limited (cooldown)")
    if balance_flag == "LOW_BALANCE_HARD":
        parts.append("balance < $1.00 (HARD demotion)")
    elif balance_flag == "LOW_BALANCE_SOFT":
        parts.append("balance < $5.00 (soft demotion)")
    elif balance_flag == "UNVERIFIABLE":
        parts.append("balance unverifiable — check dashboard")
    if latency_flag == "DEGRADED":
        parts.append("p95 latency >5s")
    elif latency_flag == "NO_TELEMETRY":
        parts.append("no telemetry — untested route")
    elif latency_flag == "INSUFFICIENT_TELEMETRY":
        parts.append("insufficient telemetry samples")
    return "; ".join(parts) if parts else "available"


# ── MCP Tools ────────────────────────────────────────────────────────────

@mcp.tool()
def fed_route(
    task: str = "",
    model: str = "deepseek-v4-pro",
    modality: str = "text",
    agent_id: str = "opencode",
    constitutional_tier: int = 333,
    effort_level: str = "",
    tokens_in_estimate: int = 0,
    tokens_out_estimate: int = 0,
    operation: str = "auto",  # sense|metabolize|act|auto — EMD lane awareness
) -> dict:
    """
    Primary routing tool. Returns ranked routes for a given task.

    Args:
        task: Natural language description of the task
        model: Target model (default: deepseek-v4-pro). Can also be a capability signature:
            fed-reasoning-heavy  → [deepseek-v4-pro, qwen3.8-max, MiniMax-M3]
            fed-multimodal-vision → [qwen-vl-max, mimo-v2.5, MiniMax-M3]
            fed-long-context     → [MiniMax-M3, mimo-v2.5-pro, qwen3.8-max]
            fed-agent-subagent   → [deepseek-v4-flash, qwen3.6-flash, mimo-v2.5]
            fed-realtime-voice   → [mimo-v2.5-tts, mimo-v2.5-asr]
            fed-local-uncensored → LOCAL RUNTIME: routes to ComfyUI :8188 with full audit
        modality: text, vision, video, audio, omni
        agent_id: Calling agent (opencode, hermes, asi-555, apex-888)
        constitutional_tier: 0=default, 333=primary, 555=research, 666=judge, 999=seal
        effort_level: Effort Dial — low/medium/high/ultra. Overrides model selection.
            low: flash models (cheap & fast)
            medium: pro models (default, balanced)
            high: pro + reasoning pass (complex tasks)
            ultra: frontier models + multiple reasoning passes (SEAL-grade)
        tokens_in_estimate: Estimated input tokens (for spend logging)
        tokens_out_estimate: Estimated output tokens (for spend logging)

    Returns:
        { routes: [...], meta: { query_time_ms, effort_applied, ... } }
    """
    t0 = time.time()

    # ── Capability Classifier v1 (2026-09-07, Phase 0 fix #4) ─────────
    # `task` graduates from decorative to load-bearing (BenchDrift SEALED:
    # "live latency + TASK FITNESS"). Deterministic, identity-blind.
    # Auto-apply only at confidence ≥ 0.90 (≥2 term hits) and only when the
    # caller did NOT explicitly choose a signature or effort level — explicit
    # caller intent always wins; classification is advisory beneath it.
    classification = classify_capability(task) if task else None
    if (
        classification
        and (
            classification["confidence"] >= 0.90
            or (classification["capability"] == "vision" and classification["confidence"] >= 0.75)
        )
        and not model.startswith("fed-")
        and not effort_level
    ):
        model = classification["signature"]
        if classification["capability"] == "vision" and modality == "text":
            modality = "vision"

    # Resolve capability signature for metadata
    cap_meta = get_capability_meta(model) if model.startswith("fed-") else None
    cap_models = resolve_capability(model) if model.startswith("fed-") else []
    routes = fed_route_engine(
        task=task,
        model=model,
        modality=modality,
        agent_id=agent_id,
        constitutional_tier=constitutional_tier,
        effort_level=effort_level,
    )
    elapsed = round((time.time() - t0) * 1000)

    # Log estimated spend if tokens provided
    primary = routes[0] if routes else None
    if (tokens_in_estimate or tokens_out_estimate) and primary:
        log_spend(primary["provider"], primary["model"], tokens_in_estimate, tokens_out_estimate, agent_id)

    meta = {
        "query_time_ms": elapsed,
        "state_db": str(FED_STATE_DB),
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "cascade_instruction": (
            "Execute routes in rank order. On failure (timeout/auth), "
            "emit telemetry and cascade to next rank. Never retry same provider twice."
        ),
    }
    if effort_level:
        meta["effort_applied"] = effort_level
        meta["effort_cost_multiplier"] = EFFORT_COST_MULTIPLIER.get(effort_level, 1.0)
        meta["reasoning_passes"] = EFFORT_REASONING_PASSES.get(effort_level, 0)
    if model.startswith("fed-"):
        meta["capability_signature"] = model
        meta["capability_description"] = cap_meta.get("description", "") if cap_meta else ""
        meta["capability_models"] = cap_models

    # ── ETCSOVG Harness Metadata (arxiv 2605.23950) ─────────────────
    meta["hcsvog"] = _build_hcsvog(
        execution="bare",
        tools="mcp-core",
        context="unknown:none:none",
        schedule="single:unlimited:none",
        observe="receipt-only",
        verify="none",
        gov=f"{constitutional_tier}:yolo",
    )

    # EMD lane check — advisory flag, never blocks (F1/F4)
    # FI-008 2026-09-04: KeyError 'model' fix — capability-cascade routes carry model_id, not model
    resolved_model = (routes[0].get("model") or routes[0].get("model_id") or model) if routes else model
    emd = _emd_check(agent_id, operation, resolved_model, modality)

    # ── JIT Intent Retrieval (P1.5) ────────────────────────────────
    # Fire-and-forget: runs in background thread pool to avoid blocking routing.
    # First call loads sentence-transformers (~7s), subsequent calls <10ms.
    jit_context = None
    if task and len(task) > 5:
        def _run_jit():
            nonlocal jit_context
            build_jit = _get_intent_retriever()
            if build_jit:
                try:
                    jit_context = build_jit(task)
                except Exception:
                    pass
        _FED_BACKGROUND_TASKS.submit(_run_jit)

    # ── A2A Trace Propagation (P1.7) ────────────────────────────────
    trace_headers = make_trace_headers()

    # ── Sidecar Auto-Ingest (P1.6) ─────────────────────────────────
    # Emit execution span to arifFlow asynchronously (fire-and-forget).
    # Self-attestation ban: the sidecar captures, not the agent.
    def _ingest_span():
        try:
            import urllib.request
            import uuid

            span = {
                "trace_id": trace_headers.get("arif_trace_id", uuid.uuid4().hex[:32]),
                "span_id": trace_headers.get("arif_span_id", uuid.uuid4().hex[:16]),
                "agent_id": agent_id,
                "session_id": "",
                "step_type": "Execute",
                "cost_ns": int(elapsed * 1_000_000),
                "epistemic_label": "Observation",
                "floor_verdict": "Pass",
                "payload": {
                    "operation": "fed_route",
                    "model": model,
                    "modality": modality,
                    "routes_count": len(routes),
                    "capability": model if model.startswith("fed-") else None,
                    "captured_by": "sidecar-auto-ingest",
                    "harness_fingerprint": meta.get("hcsvog", {}).get("h_fingerprint"),
                },
                "witness_organs": ["fed"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            req = urllib.request.Request(
                "http://127.0.0.1:7073/ingest",
                data=json.dumps(span).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=2)
        except Exception:
            pass  # arifFlow may be down — span loss is acceptable for routing telemetry

    _FED_BACKGROUND_TASKS.submit(_ingest_span)

    # ── S3-lite Invocation Contract passthrough (FI-008 2026-09-04, S1 ratification) ──
    # Agents asked "WHICH model" and guessed "HOW to call". The contract now rides the route.
    _modality_map = {
        "vision": "fed-multimodal-vision",
        "omni": "fed-multimodal-vision",
        "image": "fed-image-generation",
        "image-gen": "fed-image-generation",
        "audio": "fed-realtime-voice",
        "video": "fed-video-understanding",
    }
    _sig = model if model in CAPABILITY_SIGNATURES else _modality_map.get((modality or "").lower())
    invocation_contract = None
    if _sig and _sig in CAPABILITY_SIGNATURES:
        _s = CAPABILITY_SIGNATURES.get(_sig, {})
        invocation_contract = {"signature": _sig}
        invocation_contract.update(_s.get("invocation") or {})

    return {
        "routes": routes,
        "meta": meta,
        "emd": emd,
        "jit": jit_context,
        "trace": trace_headers if _trace_enabled else None,
        "invocation_contract": invocation_contract,
    }


@mcp.tool()
def fed_status() -> dict:
    """Return full FED state: all provider balances, route health, latency summary."""
    providers = read_all_providers()

    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row  # FI-008 2026-09-04: same tuple-access fix as fed_health
        lat_rows = conn.execute(
            "SELECT provider_name, model_id, p50_ms, p95_ms, sample_count, last_sample FROM route_latency"
        ).fetchall()
        health_rows = conn.execute("SELECT provider_name, model_id, status, shadow_id FROM route_health").fetchall()
        spend_total = conn.execute(
            "SELECT provider_name, SUM(estimated_cost_usd) as total FROM token_bank_spend GROUP BY provider_name"
        ).fetchall()

    return {
        "providers": providers,
        "latency": [dict(r) for r in lat_rows],
        "health": [dict(r) for r in health_rows],
        "spend_summary": {r["provider_name"]: round(r["total"], 6) for r in spend_total},
        "state_db": str(FED_STATE_DB),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def fed_probe() -> dict:
    """Probe LiteLLM gateway lanes + DB state (v3.3.1).

    Replaces the dead delegation to balance_probe.py (probed DeepSeek only,
    hardcoded provider_count=6). Reads live gateway health surfaces directly
    and reports honest DB counts. ADVISORY_ONLY — never judges.
    """
    import urllib.request

    lanes = {
        "litellm_local_4013": "http://127.0.0.1:4013/health/liveliness",
        "litellm_kvm4_4000": "http://100.64.0.5:4000/health/liveliness",
    }
    gateways: dict = {}
    for name, url in lanes.items():
        try:
            with urllib.request.urlopen(url, timeout=4) as r:
                body = r.read(2048).decode("utf-8", errors="replace")
                gateways[name] = {"status": "LIVE", "http": r.status, "body_head": body[:200]}
        except Exception as e:  # noqa: BLE001 — probe must report DOWN, not crash
            gateways[name] = {"status": "DOWN", "error": str(e)[:120]}
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row
        providers = conn.execute("SELECT COUNT(*) AS n FROM providers").fetchone()["n"]
        health_rows = conn.execute(
            "SELECT status, COUNT(*) AS n FROM route_health GROUP BY status"
        ).fetchall()
    return {
        "gateways": gateways,
        "db_providers": providers,
        "route_health": {r["status"]: r["n"] for r in health_rows},
        "note": "ADVISORY_ONLY — live probe over narrative (bijaksana audit discipline)",
    }


@mcp.tool()
def fed_contrast(route_a: str, route_b: str) -> dict:
    """Compare two routes side-by-side: cost, latency, shadow, constitutional fit."""

    # Parse provider:model strings
    def parse(r):
        parts = r.split(":", 1)
        return parts[0] if len(parts) > 1 else None, parts[1] if len(parts) > 1 else parts[0]

    prov_a, model_a = parse(route_a)
    prov_b, model_b = parse(route_b)

    bal_a = read_provider_balance(prov_a) if prov_a else None
    bal_b = read_provider_balance(prov_b) if prov_b else None
    lat_a = read_route_latency(prov_a, model_a) if prov_a else None
    lat_b = read_route_latency(prov_b, model_b) if prov_b else None

    # Build default harness metadata for contrast context
    hcsvog = _build_hcsvog()

    return {
        "route_a": {
            "provider": prov_a,
            "model": model_a,
            "balance": bal_a["balance_usd"] if bal_a else None,
            "latency_p50": lat_a["p50_ms"] if lat_a else None,
        },
        "route_b": {
            "provider": prov_b,
            "model": model_b,
            "balance": bal_b["balance_usd"] if bal_b else None,
            "latency_p50": lat_b["p50_ms"] if lat_b else None,
        },
        "hcsvog": hcsvog,
    }


# ── Health endpoint ──────────────────────────────────────────────────────
@mcp.tool()
def fed_health() -> dict:
    """FED health check — returns service status and DB integrity."""
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row  # FI-008 2026-09-04: fix tuple-access crash (fed_health TypeError)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()

    return {
        "status": "LIVE",
        "port": FED_PORT,
        "version": "3.3.0-zen-classifier",
        "tables": [t["name"] for t in tables],
        "state_db": str(FED_STATE_DB),
    }


# ── Capability Classifier verb (Zen Card 2026-09-07) ──────────────────────
@mcp.tool()
def fed_classify(task: str) -> dict:
    """Classify a message into a capability lane. Deterministic, identity-blind.

    Answers ONE question: "capability apa diperlukan oleh mesej ini?"
    Never identity, never emotion, never philosophy — those live prompt-side.

    Args:
        task: The message/task text to classify.

    Returns:
        { capability, signature, confidence, matched } — data, never verdicts.
    """
    return classify_capability(task)


# ── Latency telemetry ────────────────────────────────────────────────────
@mcp.tool()
def fed_report_latency(
    provider: str,
    model: str,
    latency_ms: float,
    status_code: int = 200,
    tokens_in: int = 0,
    tokens_out: int = 0,
    agent_id: str = "unknown",
    hcsvog_fingerprint: str = "",
) -> dict:
    """
    Report latency for a provider-model route. Agents call this after every
    API call to populate route_latency table with live telemetry.

    Args:
        provider: Provider name (deepseek, mulerouter, tokenrouter, etc.)
        model: Model ID (deepseek-v4-pro, qwen-vl-max, etc.)
        latency_ms: Round-trip latency in milliseconds
        status_code: HTTP status code (200, 429, 503, etc.)
        tokens_in: Input tokens used
        tokens_out: Output tokens generated
        agent_id: Reporting agent
        hcsvog_fingerprint: ETCSOVG harness fingerprint (SHA256-first-8) linking
            this latency sample to a specific harness configuration

    Returns:
        { recorded: true, p50_ms: ..., sample_count: ... }
    """
    now = datetime.now(timezone.utc).isoformat()
    
    with sqlite3.connect(str(FED_STATE_DB)) as conn:
        conn.row_factory = sqlite3.Row

        # Read existing stats
        existing = conn.execute(
            "SELECT p50_ms, p95_ms, sample_count FROM route_latency WHERE provider_name = ? AND model_id = ?",
            (provider, model),
        ).fetchone()

        if existing:
            n = existing["sample_count"] + 1
            old_p50 = existing["p50_ms"] or latency_ms
            old_p95 = existing["p95_ms"] or latency_ms
            # Welford-style online update (approximate)
            new_p50 = old_p50 + (latency_ms - old_p50) / n
            new_p95 = max(old_p95, latency_ms) - (max(old_p95, latency_ms) - latency_ms) * 0.05  # exponential decay
            conn.execute(
                """UPDATE route_latency SET p50_ms=?, p95_ms=?, sample_count=?, last_sample=? WHERE provider_name=? AND model_id=?""",
                (round(new_p50, 2), round(new_p95, 2), n, now, provider, model),
            )
        else:
            conn.execute(
                """INSERT INTO route_latency (provider_name, model_id, p50_ms, p95_ms, sample_count, last_sample)
                   VALUES (?, ?, ?, ?, 1, ?)""",
                (provider, model, latency_ms, latency_ms, now),
            )

        # Store harness fingerprint if provided and column exists
        if hcsvog_fingerprint:
            try:
                conn.execute(
                    """UPDATE route_latency SET h_fingerprint=? WHERE provider_name=? AND model_id=?""",
                    (hcsvog_fingerprint, provider, model),
                )
            except sqlite3.OperationalError:
                pass  # Column not yet added (Tier 4 migration pending)

        # Log spend if tokens used
        if tokens_in or tokens_out:
            cost = _estimate_cost(provider, model, tokens_in, tokens_out)
            conn.execute(
                """INSERT INTO token_bank_spend (provider_name, model_id, agent_id, tokens_in, tokens_out, estimated_cost_usd, called_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (provider, model, agent_id, tokens_in, tokens_out, cost, now),
            )

        # Update route health
        health_status = "LIVE" if status_code < 500 else "DEGRADED"
        if status_code == 429:
            health_status = "RATE_LIMITED"
        conn.execute(
            """INSERT INTO route_health (provider_name, model_id, status, last_checked)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(provider_name, model_id) DO UPDATE SET status=excluded.status, last_checked=excluded.last_checked""",
            (provider, model, health_status, now),
        )

        # Read updated stats
        final = conn.execute(
            "SELECT p50_ms, p95_ms, sample_count FROM route_latency WHERE provider_name = ? AND model_id = ?",
            (provider, model),
        ).fetchone()

    return {
        "recorded": True,
        "provider": provider,
        "model": model,
        "p50_ms": final["p50_ms"],
        "p95_ms": final["p95_ms"],
        "sample_count": final["sample_count"],
        "health": health_status,
    }


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.environ["FASTMCP_PORT"] = str(FED_PORT)
    print(f"🔀 FED Router v3.3 (Zen-Optimized + Capability Classifier) starting on :{FED_PORT}")
    print(f"   State DB: {FED_STATE_DB}")
    print(f"   Invariants: state-isolation, constitutional-hard-gate, dual-track-bypass")
    print(f"   Capabilities: fed-reasoning-heavy, fed-multimodal-vision, fed-long-context, fed-agent-subagent, fed-realtime-voice, fed-conversational, fed-coding")
    print(f"   v3.3 changes: task→capability classifier (BenchDrift), probe-row health fallback (corpse fix), fed_classify verb, /report telemetry ingress, notes hard-marker filter")
    print(f"   Zen Changes: DRY pricing, with(DB), RankGate matrix, ThreadPoolExecutor, SIGTERM guard")
    print(f"   Tools: fed_route, fed_status, fed_probe, fed_contrast, fed_health")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=FED_PORT, uvicorn_config={"ws": "websockets"})
