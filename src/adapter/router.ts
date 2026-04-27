import { TaskMessage, Task } from '../gateway/schema';

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface RoutingDecision {
  path: 'FORGE' | 'HOLD';
  reason: string;
  riskLevel: RiskLevel;
  requiresConfirmation: boolean;
  irreversibilityBond?: string;
}

export class GovernanceAdapter {
  private afForgeUrl = process.env.AF_FORGE_URL || 'http://af-forge:7071';

  async assessRisk(message: TaskMessage): Promise<RoutingDecision> {
    const prompt = this.extractText(message);
    
    try {
      // Call A-FORGE /sense for authoritative risk assessment
      const response = await fetch(`${this.afForgeUrl}/sense`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, version: '0.1.0' })
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
        irreversibilityBond: requiresConfirmation ? `Required for ${riskTier} risk operations` : undefined
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

  async routeIntent(message: TaskMessage): Promise<any> {
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
    
    // In this phase, we return the intent to route to forge
    return { 
      status: 'authorized', 
      source: 'A-FORGE',
      proof: {
        witness_type: 'agent',
        signature: 'af-forge-sig-' + Date.now(),
        timestamp: new Date().toISOString()
      }
    };
  }
}
