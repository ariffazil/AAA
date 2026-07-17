/**
 * Session A — Operation + ReceiptOutbox Bus
 * ═══════════════════════════════════════════════
 * 
 * Append-only durable event bus for operations and receipts.
 * Feeds observatory edges, metabolism stages, and VAULT999.
 * 
 * Storage: append-only JSONL files (crash-safe, human-readable, replayable).
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';

import {
  type OperationEvent,
  type ReceiptEvent,
  type BusStats,
  type MetabolismStage,
  type EdgeAttestation,
  type EdgeColumnState,
} from './operation-bus-types.js';

// ── Configuration ─────────────────────────────────────────────────────────

const DEFAULT_BUS_DIR = '/root/AAA/data/bus';
const OPERATIONS_LOG = 'operations.jsonl';
const RECEIPTS_LOG = 'receipts.jsonl';

// ── Helpers ───────────────────────────────────────────────────────────────

function isoNow(): string {
  return new Date().toISOString();
}

function generateId(prefix: string): string {
  const rand = crypto.randomBytes(8).toString('hex');
  return `${prefix}-${isoNow().replace(/[^0-9]/g, '').slice(0, 14)}-${rand}`;
}

function ensureDir(dir: string): void {
  fs.mkdirSync(dir, { recursive: true });
}

// ── Write (append-only) ───────────────────────────────────────────────────

function appendLine(filePath: string, obj: Record<string, unknown>): void {
  const line = JSON.stringify(obj) + '\n';
  fs.appendFileSync(filePath, line, 'utf-8');
}

// ── Read (replay) ─────────────────────────────────────────────────────────

function readLines<T>(filePath: string): T[] {
  if (!fs.existsSync(filePath)) return [];
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n').filter(Boolean);
  return lines.map(line => JSON.parse(line) as T);
}

// ── Operation Bus ─────────────────────────────────────────────────────────

export class OperationBus {
  private busDir: string;

  constructor(busDir: string = DEFAULT_BUS_DIR) {
    this.busDir = busDir;
    ensureDir(busDir);
  }

  // ── Emit ────────────────────────────────────────────────────────────

  /** Emit an operation start event */
  emitOperationStart(params: {
    actor_id: string;
    session_id: string;
    trace_id: string;
    organ: string;
    capability: string;
    stage: MetabolismStage;
    params_summary?: string;
  }): OperationEvent {
    const event: OperationEvent = {
      op_id: generateId('op'),
      actor_id: params.actor_id,
      session_id: params.session_id,
      trace_id: params.trace_id,
      organ: params.organ,
      capability: params.capability,
      params_summary: params.params_summary,
      timestamp: isoNow(),
      status: 'STARTED',
      stage: params.stage,
    };
    appendLine(path.join(this.busDir, OPERATIONS_LOG), event as unknown as Record<string, unknown>);
    return event;
  }

  /** Emit operation completion (success or failure) */
  emitOperationComplete(op_id: string, success: boolean, error?: string): OperationEvent | null {
    const ops = readLines<OperationEvent>(path.join(this.busDir, OPERATIONS_LOG));
    const idx = ops.findLastIndex(o => o.op_id === op_id);
    if (idx < 0) return null;

    const prev = ops[idx]!;
    const startMs = new Date(prev.timestamp).getTime();
    const event: OperationEvent = {
      ...prev,
      status: success ? 'COMPLETED' : 'FAILED',
      duration_ms: Date.now() - startMs,
      error,
      timestamp: isoNow(),
    };
    appendLine(path.join(this.busDir, OPERATIONS_LOG), event as unknown as Record<string, unknown>);
    return event;
  }

  // ── Receipts ────────────────────────────────────────────────────────

  /** Emit a receipt for a completed operation */
  emitReceipt(params: {
    op_id: string;
    session_id: string;
    trace_id: string;
    organ: string;
    result_summary: string;
    evidence_uri?: string;
    vault_candidate?: boolean;
  }): ReceiptEvent {
    const event: ReceiptEvent = {
      receipt_id: generateId('rcpt'),
      op_id: params.op_id,
      session_id: params.session_id,
      trace_id: params.trace_id,
      organ: params.organ,
      result_summary: params.result_summary,
      evidence_uri: params.evidence_uri,
      timestamp: isoNow(),
      vault_candidate: params.vault_candidate ?? false,
    };
    appendLine(path.join(this.busDir, RECEIPTS_LOG), event as unknown as Record<string, unknown>);
    return event;
  }

  // ── Stats ───────────────────────────────────────────────────────────

  /** Compute bus statistics */
  stats(): BusStats {
    const ops = readLines<OperationEvent>(path.join(this.busDir, OPERATIONS_LOG));
    const receipts = readLines<ReceiptEvent>(path.join(this.busDir, RECEIPTS_LOG));

    const by_status: Record<string, number> = {};
    const by_stage: Record<string, number> = {};
    for (const op of ops) {
      by_status[op.status] = (by_status[op.status] ?? 0) + 1;
      by_stage[op.stage] = (by_stage[op.stage] ?? 0) + 1;
    }

    return {
      total_operations: ops.length,
      by_status: by_status as BusStats['by_status'],
      by_stage: by_stage as BusStats['by_stage'],
      total_receipts: receipts.length,
      vault_candidates: receipts.filter(r => r.vault_candidate).length,
      last_operation_at: ops.length > 0 ? ops[ops.length - 1]!.timestamp : undefined,
      last_receipt_at: receipts.length > 0 ? receipts[receipts.length - 1]!.timestamp : undefined,
    };
  }

  // ── Edge attestation ────────────────────────────────────────────────

  /**
   * Derive edge attestation from the bus.
   * Operations and receipts provide session/actor/trace/receipt evidence.
   */
  deriveEdgeAttestation(source: string, target: string): EdgeAttestation {
    const ops = readLines<OperationEvent>(path.join(this.busDir, OPERATIONS_LOG));
    const receipts = readLines<ReceiptEvent>(path.join(this.busDir, RECEIPTS_LOG));

    const relevantOps = ops.filter(o =>
      (o.organ === source || o.organ === target) &&
      o.status === 'COMPLETED'
    );
    const relevantReceipts = receipts.filter(r =>
      (r.organ === source || r.organ === target)
    );

    const checkColumn = (has: boolean): EdgeColumnState =>
      has ? 'PRESENT' : 'NOT_EVALUATED';

    const session = checkColumn(relevantOps.some(o => o.session_id));
    const actor = checkColumn(relevantOps.some(o => o.actor_id));
    const trace = checkColumn(relevantOps.some(o => o.trace_id));
    const receipt = checkColumn(relevantReceipts.length > 0);

    const allPresent = [session, actor, trace, receipt].every(c => c === 'PRESENT');
    const anyPresent = [session, actor, trace, receipt].some(c => c === 'PRESENT');

    return {
      source,
      target,
      transport: 'reachable', // Must be verified separately
      identity: 'NOT_EVALUATED', // Identity requires organ attestation
      schema: 'NOT_EVALUATED', // Schema requires tools/list comparison
      session,
      actor,
      trace,
      receipt,
      overall: allPresent ? 'ALIGNED' : anyPresent ? 'DEGRADED' : 'UNKNOWN',
    };
  }

  // ── Replay ──────────────────────────────────────────────────────────

  /** Replay all operations (for observatory, audit, recovery) */
  replayOperations(): OperationEvent[] {
    return readLines<OperationEvent>(path.join(this.busDir, OPERATIONS_LOG));
  }

  /** Replay all receipts */
  replayReceipts(): ReceiptEvent[] {
    return readLines<ReceiptEvent>(path.join(this.busDir, RECEIPTS_LOG));
  }
}

// ── Singleton ─────────────────────────────────────────────────────────────

let _instance: OperationBus | null = null;

export function getOperationBus(busDir?: string): OperationBus {
  if (!_instance) {
    _instance = new OperationBus(busDir);
  }
  return _instance;
}
