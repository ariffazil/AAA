/**
 * =====================================================================
 * DRAFT — pending F13 ratification
 * Author:   Kimi (FI-008) · 333-AGI warga
 * Session:  SEAL-d6554349604948eb
 * Loop:     loop_20260802_hermes_opencode_circuit
 * Created:  2026-08-02T18:47Z
 *
 * Purpose:  The standard return shape for every MCP tool in the
 *           arifOS federation. Replaces ad-hoc `{text: "..."}`
 *           returns with a discriminated union that lets the agent
 *           reason about failure and route around it.
 *
 * Why:      Today, 18 MCP servers return different shapes. Some
 *           return strings, some JSON, some throw. The agent has to
 *           string-match to know if something failed. This envelope
 *           gives the agent a typed signal.
 *
 * Floors:   F2 TRUTH (ok field is OBS-anchored), F4 CLARITY
 *           (discriminated union — type narrowing is mechanical),
 *           F7 HUMILITY (G band reported, not confidence), F9
 *           ANTIHANTU (no fake ok=true on errors), F11 AUDIT
 *           (receipt_id present in every variant).
 *
 * Ratification path:
 *   1. ARIF diffs this file
 *   2. ARIF signs ACK_F13_TOOL_RESULT_ENVELOPE
 *   3. A-FORGE compiles & publishes to /root/AAA/schemas/
 *   4. Each MCP server migrates to envelope (per-server, no big-bang)
 *   5. Receives backward-compat shim (text return → envelope)
 *   6. After 7-day soak, shim removed
 * =====================================================================
 */

// ── Envelope types ──────────────────────────────────────────────────

/** Failure kind — drives the agent's recovery policy */
export type FailureKind =
  | 'transient_fail'   // retry with backoff
  | 'recoverable'      // re-acquire lease / escalate to user
  | 'permanent_fail'   // route around — do not retry
  | 'void';            // F1–F13 rejected the intent — do not retry

/** Tool result — discriminated by `ok` */
export type ToolResult<T = unknown> =
  | ToolSuccess<T>
  | ToolFailure;

/** Happy path */
export interface ToolSuccess<T = unknown> {
  ok: true;
  kind: 'result';
  value: T;
  /** F11 — receipt id (or null if tool is receipt-less) */
  receipt_id: string | null;
  /** F2 + EUR-002 — cost of the call */
  cost: {
    latency_ms: number;
    tokens_in?: number;
    tokens_out?: number;
    /** 'small' | 'medium' | 'large' | 'xlarge' */
    band: 'small' | 'medium' | 'large' | 'xlarge';
  };
  /** F2 + F7 — epistemic truth band, not confidence */
  truth_band?: 'OBS' | 'DER' | 'INT' | 'SPEC' | 'UNKNOWN';
  /** F2 + F7 — Ω₀ for this call, if measured (cap ∈ [0.95, 0.97]) */
  omega_zero?: number;
  /** Free-form additional metadata (organ, version, etc.) */
  meta?: Record<string, unknown>;
}

/** Failure path */
export interface ToolFailure {
  ok: false;
  /** Discriminated — drives recovery policy */
  kind: FailureKind;
  /** Human-readable error (F11) */
  error: string;
  /** Machine-readable code (F4 — agent branches on this) */
  code:
    | 'timeout'
    | 'denylist_pattern_match'
    | 'lease_expired'
    | 'arif_judge_void'
    | 'actor_unrecognised'
    | 'insufficient_evidence'
    | 'k001_physics_violation'
    | 'cwd_not_found'
    | 'division_by_zero'
    | 'unsupported_type'
    | 'session_not_authorized'
    | 'payload_hash_mismatch'
    | 'hrm_band_breach'
    | 'G_below_threshold'
    | 'c_dark_above_threshold'
    | 'contradictory_claims'
    | 'rate_limited'
    | 'agent_unreachable'
    | 'empty_data'
    | 'majority_wins_tie'
    | 'unknown';
  /** For transient/recoverable: suggested delay before retry (ms) */
  retry_after_ms?: number;
  /** For recoverable: hint the agent can act on */
  recovery_hint?: string;
  receipt_id: string | null;
  cost: {
    latency_ms: number;
    band: 'small' | 'medium' | 'large' | 'xlarge';
  };
  meta?: Record<string, unknown>;
}

// ── Constructor helpers ─────────────────────────────────────────────

/** Build a success result */
export function ok<T>(
  value: T,
  opts: {
    receipt_id?: string | null;
    latency_ms: number;
    tokens_in?: number;
    tokens_out?: number;
    truth_band?: ToolSuccess['truth_band'];
    omega_zero?: number;
    meta?: Record<string, unknown>;
  }
): ToolSuccess<T> {
  return {
    ok: true,
    kind: 'result',
    value,
    receipt_id: opts.receipt_id ?? null,
    cost: {
      latency_ms: opts.latency_ms,
      tokens_in: opts.tokens_in,
      tokens_out: opts.tokens_out,
      band: deriveBand(opts.latency_ms, opts.tokens_in, opts.tokens_out),
    },
    truth_band: opts.truth_band,
    omega_zero: opts.omega_zero,
    meta: opts.meta,
  };
}

/** Build a failure result */
export function fail(
  kind: FailureKind,
  error: string,
  code: ToolFailure['code'],
  opts: {
    retry_after_ms?: number;
    recovery_hint?: string;
    receipt_id?: string | null;
    latency_ms: number;
    meta?: Record<string, unknown>;
  }
): ToolFailure {
  return {
    ok: false,
    kind,
    error,
    code,
    retry_after_ms: opts.retry_after_ms,
    recovery_hint: opts.recovery_hint,
    receipt_id: opts.receipt_id ?? null,
    cost: {
      latency_ms: opts.latency_ms,
      band: deriveBand(opts.latency_ms),
    },
    meta: opts.meta,
  };
}

// ── Backward-compat shim (drop after 7-day soak) ──────────────────

/** Wrap a legacy `{text: "..."}` or string return into a ToolResult */
export function fromLegacy(legacy: unknown, latency_ms: number, receipt_id?: string): ToolResult {
  // String return
  if (typeof legacy === 'string') {
    // Heuristic: if it starts with `[error`, `[timeout`, etc → fail
    if (/^\[error|^\[timeout|^\[connect failed|^\[no text/i.test(legacy)) {
      return fail('recoverable', legacy, 'unknown', { latency_ms, receipt_id });
    }
    return ok(legacy, { latency_ms, receipt_id });
  }

  // {text: "..."} return
  if (legacy && typeof legacy === 'object' && 'text' in (legacy as any)) {
    const text = String((legacy as any).text);
    return fromLegacy(text, latency_ms, receipt_id);
  }

  // {result: ..., content: [...]} return
  if (legacy && typeof legacy === 'object' && 'result' in (legacy as any)) {
    return ok((legacy as any).result, { latency_ms, receipt_id });
  }

  // {error: ...} return
  if (legacy && typeof legacy === 'object' && 'error' in (legacy as any)) {
    return fail('recoverable', String((legacy as any).error), 'unknown', { latency_ms, receipt_id });
  }

  // Unknown shape — wrap as-is
  return ok(legacy, { latency_ms, receipt_id, meta: { _legacy: true } });
}

// ── Band derivation (feeds EUR-002) ─────────────────────────────────
function deriveBand(latency_ms: number, tokens_in?: number, tokens_out?: number): ToolSuccess['cost']['band'] {
  if (latency_ms < 100 && (tokens_in ?? 0) < 1000) return 'small';
  if (latency_ms < 1000 && (tokens_in ?? 0) < 10000) return 'medium';
  if (latency_ms < 10000 && (tokens_in ?? 0) < 100000) return 'large';
  return 'xlarge';
}

// ── Recovery policy (the part the agent cares about) ────────────────
export const recoveryPolicy = {
  transient_fail: {
    retry: true,
    backoff: 'exponential',
    max_attempts: 3,
  },
  recoverable: {
    retry: true,
    backoff: 'linear',
    max_attempts: 1,
    require_hint: true,
  },
  permanent_fail: {
    retry: false,
    action: 'route_around',
  },
  void: {
    retry: false,
    action: 'escalate_to_arif_judge',
  },
} as const;

// ── Migration checklist (per server) ───────────────────────────────
/**
 * For each MCP server, the migration is:
 *
 *   1. Add this file to the server's types/
 *   2. Wrap every tool implementation:
 *        return ok(result, { latency_ms, receipt_id, ... });
 *      or
 *        return fail('void', '...', 'hrm_band_breach', { ... });
 *   3. Test against existing client (use fromLegacy to read old shape)
 *   4. Mark server as v2-envelope in CAPABILITY_INDEX v2
 *   5. After ALL servers migrated, remove fromLegacy shim
 *
 * Per-server effort: ~30 min. Federation-wide: ~6 hours.
 *
 * Order (least risky first):
 *   1. capital_primitive  (pure compute, no side effects)
 *   2. geox_basin         (read-only)
 *   3. arif_observe       (read-only)
 *   4. forge_chart        (read-only)
 *   5. forge_probe        (read-only)
 *   6. (then) mutating tools, one at a time
 *
 * Last: arif_judge, arif_seal (these SEAL — extra careful)
 */

// ── Draft footer ────────────────────────────────────────────────────
// STATUS: DRAFT — no production code touched
// LOC:    ~150
// Compile target: /root/AAA/schemas/tool-result-envelope.d.ts
// Rollback: keep fromLegacy shim, agents continue to see legacy shape
// Self-test:
//   ok({ x: 1 }, { latency_ms: 50 }).ok  // true
//   fail('void', '...', 'hrm_band_breach', { latency_ms: 100 }).kind  // 'void'
//   fromLegacy('[timeout]', 1000).ok  // false
//   fromLegacy({text: 'hello'}, 50).ok  // true
