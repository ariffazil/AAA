import agentCard from './agent-card.json';

export interface AgentIdentity {
  name: string;
  version: string;
  description: string;
  creator: string;
  runtime: string;
}

export const CONSTITUTION_DEFAULTS = {
  version: 'v888.1.0-CONSTITUTION',
  floors: ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13'],
  governance_model: 'arifOS Constitutional AI',
  authority: 'Muhammad Arif bin Fazil (888 Judge)'
};

export function getBootstrapConfig(agentId: string) {
  return {
    agent_id: agentId,
    identity: agentCard.agent,
    constitution: CONSTITUTION_DEFAULTS,
    endpoints: agentCard.endpoints,
    capabilities: agentCard.capabilities,
    timestamp: new Date().toISOString()
  };
}

export function getAgentCard() {
  return agentCard;
}
