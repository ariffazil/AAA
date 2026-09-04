/**
 * JWKS Endpoint Handler for AAA A2A Gateway
 * Serves /.well-known/jwks.json for Agent Card signature verification.
 * 
 * STATUS: STAGING-READY
 */

import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const JWKS_PATH = join(__dirname, 'jwks.json');

export function getJWKS() {
  try {
    return JSON.parse(readFileSync(JWKS_PATH, 'utf8'));
  } catch {
    return { keys: [] };
  }
}

/**
 * Express route handler:
 * app.get('/.well-known/jwks.json', (req, res) => {
 *   res.json(getJWKS());
 * });
 */
