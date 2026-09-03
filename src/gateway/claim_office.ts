/**
 * Claim Office — Atomic work ownership via operation-bus
 * 
 * Pattern distilled from paperclipai/paperclip heartbeat.ts SELECT FOR UPDATE (MIT)
 * Doctrine: DITEMPA BUKAN DIBERI
 * 
 * Provides:
 *   - claimWork(workId, agentId, ttlSec) → atomic compare-and-set
 *   - releaseClaim(workId, agentId) → release ownership
 *   - getClaimStatus(workId) → current claim state
 * 
 * Event sourced: all claims are replayable from operations.jsonl
 * via the existing OperationBus.
 * 
 * Double-fire guard: second claimant gets 409-shaped response with
 * current owner + expiry (Paperclip "teaching denial").
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';
import { OperationBus, getOperationBus } from './operation-bus.js';

// ── Configuration ─────────────────────────────────────────────────────

const DEFAULT_CLAIMS_DIR = '/root/AAA/data/claims';
const CLAIMS_LOG = 'claims.jsonl';

// ── Types ─────────────────────────────────────────────────────────────

export interface ClaimRecord {
  work_id: string;
  agent_id: string;
  claimed_at: string;
  expires_at: string;
  ttl_seconds: number;
  claim_id: string;
}

export interface ClaimResult {
  claimed: boolean;
  owner?: string;
  expires_at?: string;
  claim_id?: string;
  /** When denied, contains teaching info on how to proceed */
  teaching?: {
    current_owner: string;
    expires_at: string;
    wait_seconds: number;
    hint: string;
  };
}

interface ClaimEntry extends ClaimRecord {
  status: 'ACTIVE' | 'RELEASED' | 'EXPIRED';
  released_at?: string;
  released_by?: string;
}

// ── Claim Office ─────────────────────────────────────────────────────

export class ClaimOffice {
  private claimsDir: string;
  private bus: OperationBus;
  private lockFile: string;

  constructor(claimsDir: string = DEFAULT_CLAIMS_DIR) {
    this.claimsDir = claimsDir;
    this.bus = getOperationBus();
    this.lockFile = path.join(claimsDir, '.claim.lock');
    fs.mkdirSync(claimsDir, { recursive: true });
  }

  // ── Claim ──────────────────────────────────────────────────────

  /**
   * Atomically claim a work item for an agent.
   * Uses file-based mutex (exclusive lock) for atomicity.
   * 
   * @returns ClaimResult — claimed=true on success, or teaching denial on conflict
   */
  claimWork(workId: string, agentId: string, ttlSec: number = 3600): ClaimResult {
    return this._withLock(() => {
      const existing = this._getActiveClaim(workId);

      if (existing) {
        // Already claimed — teaching denial (Paperclip pattern)
        const now = Date.now();
        const expiresMs = new Date(existing.expires_at).getTime();
        const waitSec = Math.max(0, Math.ceil((expiresMs - now) / 1000));

        // Emit event to operation bus
        this.bus.emitOperationStart({
          actor_id: agentId,
          session_id: 'claim-office',
          trace_id: `claim-denied-${workId}`,
          organ: 'AAA',
          capability: 'claim_work',
          stage: 'EXECUTE',
          params_summary: `DENIED: ${workId} already claimed by ${existing.agent_id}`,
        });

        return {
          claimed: false,
          owner: existing.agent_id,
          expires_at: existing.expires_at,
          teaching: {
            current_owner: existing.agent_id,
            expires_at: existing.expires_at,
            wait_seconds: waitSec,
            hint: `Work ${workId} is claimed by ${existing.agent_id} until ${existing.expires_at}. Wait ${waitSec}s or release claim first.`,
          },
        };
      }

      // No active claim — create one
      const now = new Date();
      const expiresAt = new Date(now.getTime() + ttlSec * 1000);
      const claimId = `claim-${crypto.randomBytes(8).toString('hex')}`;

      const entry: ClaimEntry = {
        work_id: workId,
        agent_id: agentId,
        claimed_at: now.toISOString(),
        expires_at: expiresAt.toISOString(),
        ttl_seconds: ttlSec,
        claim_id: claimId,
        status: 'ACTIVE',
      };

      this._appendClaim(entry);

      // Emit to operation bus
      const op = this.bus.emitOperationStart({
        actor_id: agentId,
        session_id: 'claim-office',
        trace_id: `claim-${workId}`,
        organ: 'AAA',
        capability: 'claim_work',
        stage: 'EXECUTE',
        params_summary: `CLAIMED: ${workId} by ${agentId} (ttl=${ttlSec}s)`,
      });
      this.bus.emitOperationComplete(op.op_id, true);

      return {
        claimed: true,
        owner: agentId,
        expires_at: expiresAt.toISOString(),
        claim_id: claimId,
      };
    });
  }

  // ── Release ────────────────────────────────────────────────────

  /**
   * Release a claim on a work item.
   * Only the current owner can release.
   */
  releaseClaim(workId: string, agentId: string): boolean {
    return this._withLock(() => {
      const existing = this._getActiveClaim(workId);

      if (!existing) {
        return false; // Nothing to release
      }

      if (existing.agent_id !== agentId) {
        // Not the owner — can't release someone else's claim
        return false;
      }

      const entry: ClaimEntry = {
        ...existing,
        status: 'RELEASED',
        released_at: new Date().toISOString(),
        released_by: agentId,
      };
      this._appendClaim(entry);

      // Emit to operation bus
      const op = this.bus.emitOperationStart({
        actor_id: agentId,
        session_id: 'claim-office',
        trace_id: `release-${workId}`,
        organ: 'AAA',
        capability: 'release_claim',
        stage: 'EXECUTE',
        params_summary: `RELEASED: ${workId} by ${agentId}`,
      });
      this.bus.emitOperationComplete(op.op_id, true);

      return true;
    });
  }

  // ── Query ──────────────────────────────────────────────────────

  /**
   * Get the current claim status for a work item.
   */
  getClaimStatus(workId: string): ClaimResult | null {
    const active = this._getActiveClaim(workId);
    if (!active) return null;

    return {
      claimed: true,
      owner: active.agent_id,
      expires_at: active.expires_at,
      claim_id: active.claim_id,
    };
  }

  // ── Internal ───────────────────────────────────────────────────

  private _getActiveClaim(workId: string): ClaimEntry | null {
    const entries = this._readClaims();
    const now = Date.now();

    // Find latest entry for this work_id
    const relevant = entries.filter(e => e.work_id === workId);
    const latest = relevant[relevant.length - 1] ?? null;

    if (!latest) return null;
    if (latest.status !== 'ACTIVE') return null;

    // Check expiry
    const expiresMs = new Date(latest.expires_at).getTime();
    if (now >= expiresMs) {
      // Expired — auto-release
      const expired: ClaimEntry = {
        ...latest,
        status: 'EXPIRED',
      };
      this._appendClaim(expired);
      return null;
    }

    return latest;
  }

  private _readClaims(): ClaimEntry[] {
    const logPath = path.join(this.claimsDir, CLAIMS_LOG);
    if (!fs.existsSync(logPath)) return [];

    const content = fs.readFileSync(logPath, 'utf-8');
    return content.trim().split('\n').filter(Boolean).map(line => {
      try {
        return JSON.parse(line) as ClaimEntry;
      } catch {
        return null as unknown as ClaimEntry;
      }
    }).filter(Boolean);
  }

  private _appendClaim(entry: ClaimEntry): void {
    const logPath = path.join(this.claimsDir, CLAIMS_LOG);
    fs.appendFileSync(logPath, JSON.stringify(entry) + '\n', 'utf-8');
  }

  /**
   * Execute a function while holding an exclusive file lock.
   * Ensures atomic compare-and-set semantics.
   */
  private _withLock<T>(fn: () => T): T {
    // File-based mutex via exclusive create
    const maxAttempts = 50;
    for (let i = 0; i < maxAttempts; i++) {
      try {
        // O_EXCL ensures atomicity — only one process gets the lock
        fs.writeFileSync(this.lockFile, `${process.pid}-${Date.now()}`, { flag: 'wx' });
        try {
          return fn();
        } finally {
          try { fs.unlinkSync(this.lockFile); } catch { /* best effort */ }
        }
      } catch {
        // Lock held — spin with exponential backoff
        const delay = Math.min(100, 5 * (i + 1));
        // Synchronous spin (acceptable for short-lived claims)
        const end = Date.now() + delay;
        while (Date.now() < end) { /* spin */ }
      }
    }
    throw new Error('ClaimOffice: failed to acquire lock after max attempts');
  }
}

// ── Singleton ────────────────────────────────────────────────────────

let _instance: ClaimOffice | null = null;

export function getClaimOffice(claimsDir?: string): ClaimOffice {
  if (!_instance) {
    _instance = new ClaimOffice(claimsDir);
  }
  return _instance;
}
