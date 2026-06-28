import { loadPeerContract } from './peerContractLoader';
import { logToVault } from './vaultLogger';

export interface Intent {
  type: string;
  [key: string]: any;
}

export interface DelegationResult {
  status: 'PROCEED' | 'VOID';
  reason?: string;
}

/**
 * enforceDelegation — Default Deny (Fail-Hard)
 *
 * Checks whether sourceOrgan is contractually allowed to delegate intent.type
 * to targetOrgan. No contract = VOID. Intent not in allowed list = VOID.
 *
 * F13 SOVEREIGN: Every routing decision is logged to VAULT999.
 */
export function enforceDelegation(
  sourceOrgan: string,
  targetOrgan: string,
  intent: Intent
): DelegationResult {
  const contract = loadPeerContract(sourceOrgan, targetOrgan);

  if (!contract) {
    const msg = `F13 BREACH: Unauthorized routing attempt from ${sourceOrgan} to ${targetOrgan}`;
    logToVault({
      level: 'CRITICAL',
      category: 'DELEGATION_VIOLATION',
      message: msg,
      source_organ: sourceOrgan,
      target_organ: targetOrgan,
      intent_type: intent.type,
      verdict: 'VOID',
      reason: 'NO_PEER_CONTRACT',
    });
    return { status: 'VOID', reason: 'NO_PEER_CONTRACT' };
  }

  const allowed: string[] = contract.allowed_intents || [];
  if (!allowed.includes(intent.type)) {
    const msg = `F13 BREACH: Intent ${intent.type} not delegated from ${sourceOrgan} to ${targetOrgan}`;
    logToVault({
      level: 'CRITICAL',
      category: 'DELEGATION_VIOLATION',
      message: msg,
      source_organ: sourceOrgan,
      target_organ: targetOrgan,
      intent_type: intent.type,
      verdict: 'VOID',
      reason: 'INTENT_NOT_DELEGATED',
    });
    return { status: 'VOID', reason: 'INTENT_NOT_DELEGATED' };
  }

  return { status: 'PROCEED' };
}
