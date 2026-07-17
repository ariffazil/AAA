/**
 * Session A — Operation + ReceiptOutbox Types
 * ═══════════════════════════════════════════════════
 * 
 * Durable operation pipeline + receipt outbox.
 * Feeds observatory edges, metabolism stages, and VAULT999 seal candidates.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

// ── Operation Event ───────────────────────────────────────────────────────

export type OperationStatus = 'STARTED' | 'EXECUTING' | 'COMPLETED' | 'FAILED' | 'COMPENSATING';

export type MetabolismStage =
  | '000_INIT'
  | '010_FORGE'
  | '111_OBSERVE'
  | '222_EVIDENCE'
  | '333_THINK'
  | '444_ROUTE'
  | '555_MEMORY'
  | '666_CRITIQUE'
  | '777_MEASURE'
  | '888_JUDGE'
  | '999_RECEIPT';

export interface OperationEvent {
  /** Unique operation ID (idempotency key) */
  op_id: string;
  /** Actor who initiated */
  actor_id: string;
  /** Governing session */
  session_id: string;
  /** Trace ID for distributed tracing */
  trace_id: string;
  /** Which organ executed */
  organ: string;
  /** Capability/tool invoked */
  capability: string;
  /** Parameters (summary, not full payload) */
  params_summary?: string;
  /** ISO-8601 timestamp */
  timestamp: string;
  /** Current status */
  status: OperationStatus;
  /** Metabolism stage this operation maps to */
  stage: MetabolismStage;
  /** Duration in ms (set on completion) */
  duration_ms?: number;
  /** Error message if failed */
  error?: string;
}

// ── Receipt Event ─────────────────────────────────────────────────────────

export interface ReceiptEvent {
  /** Unique receipt ID */
  receipt_id: string;
  /** Links to operation */
  op_id: string;
  /** Governing session */
  session_id: string;
  /** Trace continuity */
  trace_id: string;
  /** Organ that produced the receipt */
  organ: string;
  /** 1-line summary of result */
  result_summary: string;
  /** URI to evidence (snapshot, artifact, log) */
  evidence_uri?: string;
  /** ISO-8601 timestamp */
  timestamp: string;
  /** Cryptographic signature (optional initially) */
  signature?: string;
  /** Whether this receipt is a VAULT999 seal candidate */
  vault_candidate: boolean;
}

// ── Bus Statistics ────────────────────────────────────────────────────────

export interface BusStats {
  /** Total operations logged */
  total_operations: number;
  /** Operations by status */
  by_status: Record<OperationStatus, number>;
  /** Operations by stage */
  by_stage: Record<MetabolismStage, number>;
  /** Total receipts */
  total_receipts: number;
  /** Receipts marked as vault candidates */
  vault_candidates: number;
  /** Last operation timestamp */
  last_operation_at?: string;
  /** Last receipt timestamp */
  last_receipt_at?: string;
}

// ── Edge Attestation (fed by bus) ─────────────────────────────────────────

export type EdgeColumnState = 'NOT_EVALUATED' | 'PRESENT' | 'MISSING' | 'ERROR';

export interface EdgeAttestation {
  source: string;
  target: string;
  transport: 'reachable' | 'unreachable' | 'unknown';
  identity: EdgeColumnState;
  schema: EdgeColumnState;
  session: EdgeColumnState;
  actor: EdgeColumnState;
  trace: EdgeColumnState;
  receipt: EdgeColumnState;
  overall: 'ALIGNED' | 'DEGRADED' | 'UNKNOWN';
}
