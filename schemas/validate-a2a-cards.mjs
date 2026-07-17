#!/usr/bin/env node
/**
 * A2A 1.0 Agent Card Schema Validator
 * ═══════════════════════════════════════════
 * 
 * Validates agent cards against the pinned A2A v1.0 JSON Schema.
 * Used in CI (npm run validate:a2a-cards) to enforce conformance.
 * 
 * Usage: node schemas/validate-a2a-cards.mjs [card-path...]
 *        If no paths given, validates all known cards from card inventory.
 */
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

import Ajv from 'ajv';

// Load schema
const schemaPath = resolve(__dirname, 'a2a-v1.0.schema.json');
const schema = JSON.parse(readFileSync(schemaPath, 'utf-8'));

const ajv = new Ajv({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

// Known card paths to validate
const DEFAULT_CARDS = [
  '../.well-known/agent-card.json',
  '../agent-card.json',
  '../src/seed/agent-card.json',
  '../src/seed/agent-card-official.json',
  '../public/.well-known/agent-card.json',
  '../public/a2a/agent-card.json',
  '../agent-cards/pillars/aaa-gateway/agent-card.json',
  '../agent-cards/pillars/aaa-gateway/agent-card-extended.json',
];

const cardPaths = process.argv.slice(2).length > 0
  ? process.argv.slice(2)
  : DEFAULT_CARDS;

let totalCards = 0;
let validCards = 0;
let invalidCards = 0;
let errors = [];

for (const relPath of cardPaths) {
  const absPath = resolve(__dirname, relPath);
  totalCards++;
  
  try {
    const card = JSON.parse(readFileSync(absPath, 'utf-8'));
    const valid = validate(card);
    
    if (valid) {
      console.log(`✅ ${relPath}`);
      validCards++;
    } else {
      console.log(`❌ ${relPath}`);
      for (const err of validate.errors || []) {
        const msg = `  - ${err.instancePath || '(root)'}: ${err.message}`;
        console.log(msg);
        errors.push({ card: relPath, ...err });
      }
      invalidCards++;
    }
  } catch (err) {
    console.log(`❌ ${relPath} (parse error: ${err.message})`);
    errors.push({ card: relPath, parseError: err.message });
    invalidCards++;
  }
}

console.log(`\n${'═'.repeat(50)}`);
console.log(`Total: ${totalCards} | ✅ ${validCards} | ❌ ${invalidCards}`);

if (invalidCards > 0) {
  console.log('\nFAILED: Some cards do not conform to A2A 1.0 schema.');
  process.exit(1);
}

console.log('PASSED: All cards conform to A2A 1.0 schema.');
process.exit(0);
