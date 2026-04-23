import { TaskMessage, Task } from '../gateway/schema';

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface RoutingDecision {
  path: 'MCP' | 'KERNEL' | 'HOLD';
  reason: string;
  riskLevel: RiskLevel;
}

export class GovernanceAdapter {
  async assessRisk(message: TaskMessage): Promise<RoutingDecision> {
    const text = this.extractText(message).toLowerCase();
    
    // 1. Critical/High Risk detection
    if (text.includes('delete') || text.includes('destroy') || text.includes('override') || text.includes('seal')) {
      return { path: 'HOLD', reason: 'High-risk destructive or sovereign action detected', riskLevel: 'CRITICAL' };
    }

    // 2. Medium Risk - requires Kernel mediation (content generation, judgment)
    if (text.includes('judge') || text.includes('evaluate') || text.includes('predict') || text.includes('reason')) {
      return { path: 'KERNEL', reason: 'Constitutional judgment required', riskLevel: 'MEDIUM' };
    }

    // 3. Low Risk - Direct to MCP (read-only, status checks)
    return { path: 'MCP', reason: 'Low-risk operational query', riskLevel: 'LOW' };
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
    
    switch (decision.path) {
      case 'HOLD':
        throw new Error(`888_HOLD: ${decision.reason}`);
      case 'KERNEL':
        return this.mediateViaKernel(message);
      case 'MCP':
        return this.executeDirectMCP(message);
    }
  }

  private async mediateViaKernel(message: TaskMessage) {
    // In production, this calls the arifOS Kernel API
    console.log('[Adapter] Routing to Kernel for Floor validation...');
    return { status: 'mediated', source: 'KERNEL' };
  }

  private async executeDirectMCP(message: TaskMessage) {
    // In production, this calls the MCP tool directly
    console.log('[Adapter] Routing directly to MCP capability...');
    return { status: 'executed', source: 'MCP' };
  }
}
