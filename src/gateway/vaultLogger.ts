import fs from 'fs';
import path from 'path';

const VAULT_TELEMETRY_DIR = '/root/VAULT999/telemetry';

export interface VaultLogEntry {
  timestamp?: string;
  level: string;
  category: string;
  message: string;
  source_organ?: string;
  target_organ?: string;
  intent_type?: string;
  verdict?: string;
  reason?: string;
}

/**
 * logToVault — append-only telemetry log for delegation events.
 *
 * Writes to /root/VAULT999/telemetry/delegation-<date>.jsonl.
 * Does not block the caller on write failure.
 */
export function logToVault(entry: VaultLogEntry): void {
  try {
    if (!fs.existsSync(VAULT_TELEMETRY_DIR)) {
      fs.mkdirSync(VAULT_TELEMETRY_DIR, { recursive: true });
    }

    const line = JSON.stringify({
      timestamp: new Date().toISOString(),
      ...entry,
    });

    const date = new Date().toISOString().split('T')[0];
    const filePath = path.join(VAULT_TELEMETRY_DIR, `delegation-${date}.jsonl`);
    fs.appendFileSync(filePath, line + '\n', 'utf8');
  } catch (err) {
    // Fail-safe: do not block routing on logging failure
    console.error('[vaultLogger] Failed to write telemetry:', err);
  }
}
