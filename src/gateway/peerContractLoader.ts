import fs from 'fs';
import path from 'path';

const CONTRACT_DIR = path.resolve(__dirname, '../../a2a/peer-contracts');

export interface PeerContract {
  contract_version: string;
  source_organ: string;
  target_organ: string;
  authority_class: string;
  allowed_intents: string[];
  accepted_inputs: Array<{ schema_id: string; schema_url: string }>;
  emitted_outputs: string[];
  forbidden_actions: string[];
  max_risk_tier: string;
  lease_required: boolean;
  reversibility_score: number;
  trust_score: number;
  audit_sink: {
    vault999_endpoint: string;
    receipt_format: string;
    nats_subject: string;
  };
}

/**
 * loadPeerContract — immutable routing law lookup.
 *
 * Searches AAA/a2a/peer-contracts/<source>-<target>.json
 * Returns null if no contract exists (Default Deny).
 */
export function loadPeerContract(
  sourceOrgan: string,
  targetOrgan: string
): PeerContract | null {
  const variants = [
    `${sourceOrgan}-${targetOrgan}.json`,
    `${sourceOrgan}_to_${targetOrgan}.json`,
    `${sourceOrgan}->${targetOrgan}.json`,
  ];

  for (const name of variants) {
    const filePath = path.join(CONTRACT_DIR, name);
    if (fs.existsSync(filePath)) {
      const raw = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(raw) as PeerContract;
    }
  }

  return null;
}
