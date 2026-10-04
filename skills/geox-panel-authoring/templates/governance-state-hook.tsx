/**
 * Tri-State Authority Machine — Governance State Hook
 * ═══════════════════════════════════════════════════════════
 *
 * V10/V11 pattern: replaces mock SEAL gates (receipt_hash as authority)
 * with an explicit tri-state flow in React state. Used when geological
 * picks or interpretation commits need governance gating.
 *
 * States:
 *   DRAFT          — reversible, local state only. Canvas active.
 *   PENDING REVIEW — canvas LOCKED (read-only). Uncertainty acknowledged.
 *   ATTESTED       — sealed at VAULT999. No further editing.
 *
 * Wire into component:
 *   const { claim, toDraft, requestReview, attest } = useGeologicalClaim('horizon');
 *   const isReadOnly = claim.state !== 'draft';
 *
 * Then pass readOnly={isReadOnly} to child canvas components and guard
 * click handlers with `if (readOnly) return;`.
 *
 * IMPORTANT: receipt_hash is evidence, NOT authority. The attestation ref
 * must come from VAULT999 (or future sovereign signer), never from a
 * compute receipt (geox_petrophysics, geox_judge_verdict, etc.).
 */

import { useState, useCallback } from 'react';
import { useGEOXStore } from '../store/geoxStore';

export type ClaimState = 'draft' | 'pending_review' | 'attested';

export interface GeologicalClaim {
  id: string;
  type: 'horizon' | 'fault' | 'correlation' | 'reservoir_boundary';
  state: ClaimState;
  createdAt: string;
  payload: Record<string, unknown>;
  receiptHash?: string;       // NOT authority — only evidence
  attestationRef?: string;    // VAULT999 ref after real SEAL
}

export function useGeologicalClaim(claimType: GeologicalClaim['type']) {
  const { updateFloorStatus } = useGEOXStore();
  const [claim, setClaim] = useState<GeologicalClaim>({
    id: `${claimType}-${Date.now()}`,
    type: claimType,
    state: 'draft',
    createdAt: new Date().toISOString(),
    payload: {},
  });

  /** Transition to DRAFT — payload is the current picks/state. */
  const toDraft = useCallback((payload: Record<string, unknown>) => {
    setClaim((prev) => ({ ...prev, payload, state: 'draft' }));
    updateFloorStatus('F1', 'amber', 'DRAFT: reversible, local state only');
  }, [updateFloorStatus]);

  /** Transition to PENDING REVIEW — canvas locks, F11 halt. */
  const requestReview = useCallback(() => {
    setClaim((prev) => ({ ...prev, state: 'pending_review' }));
    updateFloorStatus('F11', 'amber', 'PENDING REVIEW: canvas locked (F1 halt)');
  }, [updateFloorStatus]);

  /** Transition to ATTESTED — requires a VAULT999 attestation ref. */
  const attest = useCallback((attestationRef: string) => {
    setClaim((prev) => ({ ...prev, state: 'attested', attestationRef }));
    updateFloorStatus('F13', 'green', `ATTESTED: ${attestationRef} — VAULT999`);
  }, [updateFloorStatus]);

  return { claim, toDraft, requestReview, attest };
}
