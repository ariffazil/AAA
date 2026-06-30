import { TaskMessage } from '../gateway/schema';
import { deliberate } from '../gateway/deliberation';

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface RoutingDecision {
  path: 'FORGE' | 'HOLD';
  reason: string;
  riskLevel: RiskLevel;
  requiresConfirmation: boolean;
  irreversibilityBond?: string;
}

export class GovernanceAdapter {
  private afForgeUrl = process.env.AF_FORGE_URL || 'http://af-bridge-prod:7071';

  async assessRisk(message: TaskMessage): Promise<RoutingDecision> {
    const prompt = this.extractText(message);
    const peer_contract_id = this.extractPeerContractId(message);

    // AAA local constitutional pre-flight (888 deliberation)
    const local = deliberate(message);
    if (local.verdict === 'VOID') {
      return {
        path: 'HOLD',
        reason: `AAA deliberation VOID: ${local.rationale}`,
        riskLevel: 'CRITICAL',
        requiresConfirmation: true,
        irreversibilityBond: 'Constitutional void — cannot proceed',
        peer_contract_id,
      };
    }
    if (local.verdict === 'HOLD_888' || local.verdict === 'SABAR') {
      return {
        path: 'HOLD',
        reason: `AAA deliberation ${local.verdict}: ${local.rationale}`,
        riskLevel: local.verdict === 'HOLD_888' ? 'HIGH' : 'MEDIUM',
        requiresConfirmation: true,
        irreversibilityBond: `Required after AAA ${local.verdict}`,
        peer_contract_id,
      };
    }

    try {
      // Call A-FORGE /sense for authoritative risk assessment
      const response = await fetch(`${this.afForgeUrl}/sense`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, version: '0.1.0', peer_contract_id })
      });
      
      const data = await response.json();
      const riskTier = data.judge?.verdict === 'SEAL' ? 'LOW' : 
                       (data.judge?.verdict === 'SABAR' ? 'MEDIUM' : 'HIGH');
      
      const requiresConfirmation = riskTier !== 'LOW';

      return {
        path: requiresConfirmation ? 'HOLD' : 'FORGE',
        reason: data.judge?.reason || 'A-FORGE risk assessment completed',
        riskLevel: riskTier as RiskLevel,
        requiresConfirmation,
        irreversibilityBond: requiresConfirmation ? `Required for ${riskTier} risk operations` : undefined,
        peer_contract_id,
      };

    } catch (error) {
      console.error('[Adapter] A-FORGE sense error, failing closed to HOLD:', error);
      return { 
        path: 'HOLD', 
        reason: 'A-FORGE connectivity failure - manual review required', 
        riskLevel: 'CRITICAL',
        requiresConfirmation: true
      };
    }
  }

  private extractText(message: TaskMessage): string {
    return message.parts
      .filter((p): p is { kind: 'text'; text: string } => p.kind === 'text')
      .map(p => p.text)
      .join(' ');
  }

  private extractPeerContractId(message: TaskMessage): string | undefined {
    const meta = message.metadata;
    if (meta && typeof meta.peer_contract_id === 'string') {
      return meta.peer_contract_id;
    }
    return undefined;
  }

  async routeIntent(message: TaskMessage): Promise<Record<string, unknown>> {
    const decision = await this.assessRisk(message);
    console.log(`[Adapter] Risk Assessment: ${decision.riskLevel} -> Path: ${decision.path} (${decision.reason})`);
    
    if (decision.requiresConfirmation) {
      // Return a hold state that the UI will use to request human approval
      return { 
        status: 'HOLD', 
        source: 'A-FORGE', 
        reason: decision.reason,
        riskLevel: decision.riskLevel,
        irreversibilityBond: decision.irreversibilityBond,
        requiresHuman: true
      };
    }

    return this.executeViaForge(message);
  }

  private async executeViaForge(message: TaskMessage) {
    // Architectural Law: All tool calls must route via A-FORGE
    console.log('[Adapter] Routing to A-FORGE for execution...');

    const prompt = this.extractText(message);
    const peer_contract_id = this.extractPeerContractId(message);

    try {
      const response = await fetch(`${this.afForgeUrl}/route`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, mode: 'external', peer_contract_id })
      });

      if (!response.ok) {
        const text = await response.text().catch(() => '<unreadable>');
        console.error(`[Adapter] A-FORGE /route returned HTTP ${response.status}: ${text.slice(0, 500)}`);
        return {
          status: 'HOLD',
          source: 'A-FORGE',
          reason: `A-FORGE /route failed with HTTP ${response.status}`,
          riskLevel: 'CRITICAL' as RiskLevel,
          requiresHuman: true,
        };
      }

      const data = await response.json();
      
      if (data.is_hold || data.routing_decision === '888_HOLD') {
        return {
          status: 'HOLD',
          source: 'A-FORGE',
          reason: data.routing_decision ?? 'Routing decision returned HOLD',
          riskLevel: 'HIGH' as RiskLevel,
          routing_decision: data.routing_decision,
          session_id: data.session_id,
          requiresHuman: true,
        };
      }

      return {
        status: 'authorized',
        source: 'A-FORGE',
        routing_decision: data.routing_decision,
        agent_id: data.agent_id,
        session_id: data.session_id,
        coordinator: data.coordinator,
        peer_contract_id,
        proof: {
          witness_type: 'agent',
          signature: `routed-${data.routing_decision}-${Date.now()}`,
          timestamp: new Date().toISOString(),
        },
      };
    } catch (error) {
      console.error('[Adapter] A-FORGE /route error:', error);
      return {
        status: 'HOLD',
        source: 'A-FORGE',
        reason: error instanceof Error ? error.message : 'A-FORGE /route unreachable',
        riskLevel: 'CRITICAL' as RiskLevel,
        requiresHuman: true,
      };
    }
  }
}
